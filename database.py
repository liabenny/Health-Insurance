# database related code
import psycopg2
import psycopg2.extras
import pymongo
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
    def __query_one__(cls, query, parameters=()):
        cursor = cls.conn.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchone()

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

    @classmethod
    def get_eye_insurance(cls, insurance_type, group_type, age, metal_level_id):
        if insurance_type == "Eye Glasses" and group_type == "Adult":
            insurance_type = "Eyeglasses"
        key1 = "%" + insurance_type + "%"
        key2 = "%" + group_type + "%"
        # SQL Query
        query = "SELECT r1.plan_id, rate_individual.effective_date, rate_individual.expiration_date, benefit_name, " \
                "Avg(individual_rate), limit_qty, limit_unit " \
                "FROM (SELECT plans.std_component_id, plans.plan_id FROM medical_plans " \
                "JOIN plans ON medical_plans.plan_id = plans.plan_id WHERE metal_level = %s) r1, " \
                "rate_individual, plan_benefit_limitation " \
                "WHERE r1.plan_id = plan_benefit_limitation.plan_id " \
                "AND rate_individual.std_component_id = r1.std_component_id " \
                "AND rate_individual.age_range_from = %s " \
                "AND plan_benefit_limitation.benefit_name LIKE ALL (ARRAY [%s, %s]) " \
                "GROUP BY r1.plan_id, rate_individual.effective_date, rate_individual.expiration_date, benefit_name, " \
                "limit_qty, limit_unit"
        return cls.__query__(query, (metal_level_id, age, key1, key2))

    @classmethod
    def get_benefit_list(cls):
        query = "SELECT DISTINCT benefit_name FROM plan_benefit ORDER BY benefit_name ASC"
        return cls.__query__(query)

    @classmethod
    def get_benefit(cls, benefit_type):
        query = "SELECT plan_benefit.plan_id, plan_benefit.benefit_name, plan_benefit_limitation.limit_qty, " \
                "plan_benefit_limitation.limit_unit FROM plan_benefit, plan_benefit_limitation " \
                "WHERE plan_benefit.benefit_name = %s AND plan_benefit.plan_id = plan_benefit_limitation.plan_id " \
                "GROUP BY plan_benefit.plan_id, plan_benefit.benefit_name, plan_benefit_limitation.limit_qty, " \
                "plan_benefit_limitation.limit_unit"
        return cls.__query__(query, (benefit_type,))

    @classmethod
    def get_plan_state(cls):
        query = "SELECT DISTINCT state FROM plans ORDER BY state"
        return cls.__query__(query)

    @classmethod
    def plain_query(cls, attributes, table_name, constrains, order_by=None):
        if order_by:
            query = sql.SQL("SELECT {} FROM {} WHERE {} ORDER BY {}").format(
                sql.SQL(',').join(sql.Identifier(attr) for attr in attributes),
                sql.Identifier(table_name),
                sql.SQL(" AND ").join(cls.__generate_conditions__(constrains)),
                sql.Identifier(order_by)
            )

        else:
            query = sql.SQL("SELECT {} FROM {} WHERE {}").format(
                sql.SQL(',').join(sql.Identifier(attr) for attr in attributes),
                sql.Identifier(table_name),
                sql.SQL(" AND ").join(cls.__generate_conditions__(constrains))
            )

        return cls.__query__(query, list(value[1] for value in constrains.values()))

    @classmethod
    def plain_query_one(cls, attributes, table_name, constrains):
        query = sql.SQL("SELECT {} FROM {} WHERE {}").format(
            sql.SQL(',').join(sql.Identifier(attr) for attr in attributes),
            sql.Identifier(table_name),
            sql.SQL(" AND ").join(cls.__generate_conditions__(constrains))
        )

        return cls.__query_one__(query, list(value[1] for value in constrains.values()))


class Mongo:
    client = None
    db = None

    @classmethod
    def init(cls, host, port, db_name):
        cls.client = pymongo.MongoClient("mongodb://%s:%s/" % (host, port))
        cls.db = cls.client[db_name]

    @classmethod
    def get_disease_programs(cls, col, plan_id):
        col = cls.db[col]
        res = col.find_one({"_id": plan_id})
        if res:
            return res[const.DISEASE]
        else:
            return None


Query.init(const.HOST_NAME, const.DB_NAME, const.DB_USER)
Mongo.init(const.MONGO_HOST, const.MONGO_PORT, const.MONGO_DB_NAME)
