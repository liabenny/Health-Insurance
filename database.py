# database related code
import psycopg2
import psycopg2.extras
import constants as const
from psycopg2 import sql


class Query:
    conn = None
    cursor = None

    @staticmethod
    def __generate_conditions__(conditions):
        results = list()
        for key, value in conditions.items():
            if value[0] == const.IN:
                tmp = sql.SQL("{} IN ({})").format(sql.Identifier(key), value[1])
            else:
                tmp = sql.SQL(value[0]).join([sql.Identifier(key), sql.Placeholder()])
            results.append(tmp)
        return sql.Composed(results)

    @classmethod
    def __query__(cls, query, parameters=()):
        cursor = cls.conn.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()

    @classmethod
    def init(cls, hostname, dbname, user):
        cls.conn = psycopg2.connect("host=%s dbname=%s user=%s" % (hostname, dbname, user))
        cls.cursor = cls.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    @classmethod
    def get_time_intervals(cls, metal_level_id, age):
        query = "SELECT effective_date, expiration_date FROM (" \
                "SELECT DISTINCT effective_date, expiration_date " \
                "FROM rate_individual, " \
                "(" \
                "SELECT DISTINCT plans.std_component_id, state " \
                "FROM medical_plans " \
                "JOIN plans ON medical_plans.plan_id = plans.plan_id " \
                "WHERE metal_level = %s" \
                ") r1 " \
                "WHERE r1.std_component_id = rate_individual.std_component_id " \
                "AND age_range_from <= %s " \
                "AND age_range_to >= %s) r2 " \
                "ORDER BY effective_date, expiration_date DESC"
        return cls.__query__(query, (metal_level_id, age, age))

    @classmethod
    def get_avg_rate(cls, metal_level_id, age, effective_date, expiration_date, insurance_type):
        # Table name of medical or dental plans
        table_name = const.TABLE_MEDICAL_PLAN if insurance_type == "medical" \
            else const.TABLE_DENTAL_PLAN

        # SQL Query
        query = "SELECT state, AVG(individual_rate) " \
                "FROM rate_individual, " \
                "(" \
                "SELECT DISTINCT plans.std_component_id, state " \
                "FROM " + table_name + " " \
                                       "JOIN plans ON " + table_name + ".plan_id = plans.plan_id " \
                                                                       "WHERE metal_level = %s" \
                                                                       ") r1 " \
                                                                       "WHERE r1.std_component_id = rate_individual.std_component_id " \
                                                                       "AND age_range_from <= %s " \
                                                                       "AND age_range_to >= %s " \
                                                                       "AND effective_date = %s " \
                                                                       "AND expiration_date = %s " \
                                                                       "GROUP BY state, effective_date, expiration_date " \
                                                                       "ORDER BY state"
        return cls.__query__(query, (metal_level_id, age, age, effective_date, expiration_date))

    @classmethod
    def get_plans(cls, attributes, constrains, insurance_type, detail_constrains):
        # Medical/Dental Plans
        table_name = const.TABLE_MEDICAL_PLAN if insurance_type == "medical" \
            else const.TABLE_DENTAL_PLAN

        if detail_constrains:
            # Having detailed constrains on medical/dental plans
            subquery = sql.SQL("SELECT {} FROM {} WHERE {}").format(
                sql.Identifier(const.PLAN_ID),
                sql.Identifier(table_name),
                sql.SQL(" AND ").join(cls.__generate_conditions__(detail_constrains))
            )
        else:
            # No detailed constrains
            subquery = sql.SQL("SELECT {} FROM {}").format(
                sql.Identifier(const.PLAN_ID),
                sql.Identifier(table_name)
            )

        # Add extra constrain to plan id
        constrains[const.PLAN_ID] = (const.IN, subquery)

        # Generate SQL query
        query = sql.SQL("SELECT {} FROM {} WHERE {}").format(
            sql.SQL(',').join(sql.Identifier(attr) for attr in attributes),
            sql.Identifier(const.TABLE_PLAN),
            sql.SQL(" AND ").join(cls.__generate_conditions__(constrains))).as_string(cls.conn)

        # Remove the extra constrain in plan id
        constrains.pop(const.PLAN_ID)

        return cls.__query__(query,
                             list(value[1] for value in constrains.values()) +
                             list(value[1] for value in detail_constrains.values()))


Query.init(const.HOST_NAME, const.DB_NAME, const.DB_USER)
