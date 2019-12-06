import csv
import psycopg2
import psycopg2.extras

import constants as const
from enumeration import Enum
from psycopg2.extensions import AsIs

# file_name = "C:\\RPI\\Database-Systems\\project\\datasets\\Benefits_Cost_Sharing_PUF.csv"
# file_name = "C:\\Study\\Database-Systems\\project\\datasets\\Plan_Attributes_PUF.csv"
file_name = "Plan_Attributes_PUF.csv"


def load_plans(conn, cursor):
    print("------LOAD PLAN ATTRIBUTES------")

    with open(file_name, mode='r') as fd:
        reader = csv.DictReader(fd)
        for raw_plan in reader:
            succeed = add_plan_general_info(cursor, raw_plan)
            if not succeed:
                print("Fail")
                break
            else:
                conn.commit()

            is_dental_plan = raw_plan['DentalOnlyPlan']
            if is_dental_plan == "YES":
                add_dental_plan()
            else:
                add_medical_plan()


def add_plan_general_info(cursor, raw):
    plan = dict()

    if raw[const.CSV_PLAN_ID].strip():
        plan[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_PLAN_VAR_NAME].strip():
        plan[const.PLAN_VAR_NAME] = raw[const.CSV_PLAN_VAR_NAME]

    if raw[const.CSV_PLAN_MARK_NAME].strip():
        plan[const.PLAN_MARK_NAME] = raw[const.CSV_PLAN_MARK_NAME]

    if raw[const.CSV_STD_COMP_ID].strip():
        plan[const.STD_COMP_ID] = raw[const.CSV_STD_COMP_ID]

    if raw[const.CSV_PLAN_YEAR].strip():
        plan[const.PLAN_YEAR] = raw[const.CSV_PLAN_YEAR]

    if raw[const.CSV_PLAN_STATE].strip():
        plan[const.PLAN_STATE] = raw[const.CSV_PLAN_STATE]

    if raw[const.CSV_SOURCE_NAME] in Enum.src_name_type:
        plan[const.SOURCE_NAME] = Enum.src_name_type[raw[const.CSV_SOURCE_NAME]]
    else:
        return False

    # TODO plan[constants.IMPORT_DATE] = raw[]

    if raw[const.CSV_HIOS_PROD_ID].strip():
        plan[const.HIOS_PROD_ID] = raw[const.CSV_HIOS_PROD_ID]

    if raw[const.CSV_HPID].strip():
        plan[const.HPID] = raw[const.CSV_HPID]

    if raw[const.CSV_NETWORK_ID].strip():
        plan[const.NETWORK_ID] = raw[const.CSV_NETWORK_ID]

    if raw[const.CSV_SERV_AREA_ID].strip():
        plan[const.SERV_AREA_ID] = raw[const.CSV_SERV_AREA_ID]

    if raw[const.CSV_FORMULARY_ID].strip():
        plan[const.FORMULARY_ID] = raw[const.CSV_FORMULARY_ID]

    if raw[const.CSV_IS_NEW_PLAN] == 'New':
        plan[const.IS_NEW_PLAN] = True
    else:
        plan[const.IS_NEW_PLAN] = False

    if raw[const.CSV_MARK_COVERAGE] in Enum.mark_cov_type:
        plan[const.MARK_COVERAGE] = Enum.mark_cov_type[raw[const.CSV_MARK_COVERAGE]]
    else:
        print("MARK_COVERAGE")
        return False

    if raw[const.CSV_PLAN_TYPE] in Enum.plan_type:
        plan[const.PLAN_TYPE] = Enum.plan_type[raw[const.CSV_PLAN_TYPE]]
    else:
        print("PLAN_TYPE")
        return False

    if raw[const.CSV_QHP_TYPE] in Enum.qhp_type:
        plan[const.QHP_TYPE] = Enum.qhp_type[raw[const.CSV_QHP_TYPE]]
    else:
        print("QHP_TYPE")
        return False

    if raw[const.CSV_DESIGN_TYPE] in Enum.design_type:
        plan[const.DESIGN_TYPE] = Enum.design_type[raw[const.CSV_DESIGN_TYPE]]
    else:
        print("DESIGN_TYPE")
        return False

    if raw[const.CSV_CHILD_ONLY] in Enum.child_only_type:
        plan[const.CHILD_ONLY] = Enum.child_only_type[raw[const.CSV_CHILD_ONLY]]
    else:
        print("CHILD_ONLY")
        return False

    if raw[const.CSV_COMPOSITE_RATE] == 'Yes':
        plan[const.COMPOSITE_RATE] = True
    else:
        plan[const.COMPOSITE_RATE] = False

    if raw[const.CSV_OUT_COUNTRY_COV] == 'Yes':
        plan[const.OUT_COUNTRY_COV] = True
    else:
        plan[const.OUT_COUNTRY_COV] = False

    if raw[const.CSV_OUT_COUNTRY_COV_DESC].strip():
        plan[const.OUT_COUNTRY_COV_DESC] = raw[const.CSV_OUT_COUNTRY_COV_DESC]

    if raw[const.CSV_OUT_SERV_AREA_COV] == 'Yes':
        plan[const.OUT_SERV_AREA_COV] = True
    else:
        plan[const.OUT_SERV_AREA_COV] = False

    if raw[const.CSV_OUT_SERV_AREA_COV_DESC].strip():
        plan[const.OUT_SERV_AREA_COV_DESC] = raw[const.CSV_OUT_SERV_AREA_COV_DESC]

    if raw[const.CSV_PLAN_EXCLUSIONS].strip():
        plan[const.PLAN_EXCLUSIONS] = raw[const.CSV_PLAN_EXCLUSIONS]

    if raw[const.CSV_EST_ADV_PAYMENT_INDIAN].strip():
        plan[const.EST_ADV_PAYMENT_INDIAN] = raw[const.CSV_EST_ADV_PAYMENT_INDIAN].lstrip("$")

    if raw[const.CSV_MULTI_NETWORK] == 'Yes':
        plan[const.MULTI_NETWORK] = True
    else:
        plan[const.MULTI_NETWORK] = False

    if raw[const.CSV_FIRST_TIER_UTIL].strip():
        plan[const.FIRST_TIER_UTIL] = raw[const.CSV_FIRST_TIER_UTIL].rstrip("%")

    if raw[const.CSV_SECOND_TIER_UTIL].strip():
        plan[const.SECOND_TIER_UTIL] = raw[const.CSV_SECOND_TIER_UTIL].rstrip("%")

    # TODO effective_date
    # TODO expiration_date

    print(plan)

    columns = plan.keys()
    values = [plan[column] for column in columns]

    insert_statement = 'insert into plans (%s) values %s'
    cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
    return True


def add_dental_plan():
    pass


def add_medical_plan():
    pass


def load_benefits():
    pass


def load_rates():
    pass


if __name__ == '__main__':
    # Connect to database
    conn = psycopg2.connect("host=%s dbname=%s user=%s" % (const.HOST_NAME,
                                                           const.DB_NAME,
                                                           const.DB_USER))
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Load Plan_Attributes_PUF.csv
    load_plans(conn, cursor)
    conn.commit()
