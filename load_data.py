import csv
import psycopg2.extras

import utils
import constants as const
from datetime import datetime
from enumeration import Enum
from psycopg2.extensions import AsIs

# file_name = "C:\\RPI\\Database-Systems\\project\\datasets\\Benefits_Cost_Sharing_PUF.csv"
# file_name = "C:\\Study\\Database-Systems\\project\\datasets\\Plan_Attributes_PUF.csv"
file_name = "2020-dataset/Plan_Attributes_PUF.csv"


def save_data(table, attributes):
    columns = attributes.keys()
    values = [attributes[column] for column in columns]

    insert_statement = 'insert into %s (%s) values %s'
    cursor.execute(insert_statement, (AsIs(table),
                                      AsIs(','.join(columns)),
                                      tuple(values)))


def load_plans():
    print("------LOAD PLAN ATTRIBUTES------")

    with open(file_name, mode='r') as fd:
        # Count total row number
        reader = csv.DictReader(fd)
        count = 0
        rows = sum(1 for _ in reader)
        fd.seek(0)

        # Loading data into database
        reader = csv.DictReader(fd)
        for raw_data in reader:
            succeed = add_plan_general_info(raw_data)
            if not succeed:
                print("Fail")
                break

            if raw_data[const.CSV_DENTAL_ONLY] == "Yes":
                # Is dental plan
                add_dental_plan(raw_data)

                # Maximum out of pocket information for dental plan
                add_dental_plan_moop(raw_data)

                # Deductible information for dental plan
                add_dental_plan_ded(raw_data)

            else:
                # Is medical plan
                add_medical_plan(raw_data)

                # Has specialist referral
                if raw_data[const.CSV_REFERRAL_REQUIRED] == 'Yes':
                    add_medical_plan_referral(raw_data)

                # Summary of benefits and coverage information for medical plan
                add_medical_plan_sbc(raw_data)

                # Maximum out of pocket information for medical plan
                if raw_data[const.CSV_MOOP_INTEGRATED] == 'Yes':
                    add_medical_plan_moop_int(raw_data)
                else:
                    add_medical_plan_moop(raw_data)

                # Deductible information for medical plan
                if raw_data[const.CSV_DED_INTEGRATED] == 'Yes':
                    add_medical_plan_ded_int(raw_data)
                else:
                    add_medical_plan_ded(raw_data)

            conn.commit()
            count += 1
            print('\rLoading Process:{:.2f}%'.format(count * 100 / rows), end='')

    print("\nDONE!")


def add_plan_general_info(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID].strip():
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_PLAN_VAR_NAME].strip():
        attr[const.PLAN_VAR_NAME] = raw[const.CSV_PLAN_VAR_NAME]

    if raw[const.CSV_PLAN_MARK_NAME].strip():
        attr[const.PLAN_MARK_NAME] = raw[const.CSV_PLAN_MARK_NAME]

    if raw[const.CSV_STD_COMP_ID].strip():
        attr[const.STD_COMP_ID] = raw[const.CSV_STD_COMP_ID]

    if raw[const.CSV_PLAN_YEAR].strip():
        attr[const.PLAN_YEAR] = raw[const.CSV_PLAN_YEAR]

    if raw[const.CSV_PLAN_STATE].strip():
        attr[const.PLAN_STATE] = raw[const.CSV_PLAN_STATE]

    if raw[const.CSV_SOURCE_NAME] in Enum.src_name_type:
        attr[const.SOURCE_NAME] = Enum.src_name_type[raw[const.CSV_SOURCE_NAME]]
    else:
        return False

    if raw[const.CSV_IMPORT_DATE].strip():
        ts = datetime.strptime(raw[const.CSV_IMPORT_DATE], "%m/%d/%Y %H:%M")
        attr[const.IMPORT_DATE] = ts.strftime("%Y-%m-%d %H:%M:%S")

    if raw[const.CSV_HIOS_PROD_ID].strip():
        attr[const.HIOS_PROD_ID] = raw[const.CSV_HIOS_PROD_ID]

    if raw[const.CSV_HPID].strip():
        attr[const.HPID] = raw[const.CSV_HPID]

    if raw[const.CSV_NETWORK_ID].strip():
        attr[const.NETWORK_ID] = raw[const.CSV_NETWORK_ID]

    if raw[const.CSV_SERV_AREA_ID].strip():
        attr[const.SERV_AREA_ID] = raw[const.CSV_SERV_AREA_ID]

    if raw[const.CSV_FORMULARY_ID].strip():
        attr[const.FORMULARY_ID] = raw[const.CSV_FORMULARY_ID]

    if raw[const.CSV_IS_NEW_PLAN] == 'New':
        attr[const.IS_NEW_PLAN] = True
    else:
        attr[const.IS_NEW_PLAN] = False

    if raw[const.CSV_MARK_COVERAGE] in Enum.mark_cov_type:
        attr[const.MARK_COVERAGE] = Enum.mark_cov_type[raw[const.CSV_MARK_COVERAGE]]
    else:
        print("MARK_COVERAGE")
        return False

    if raw[const.CSV_PLAN_TYPE] in Enum.plan_type:
        attr[const.PLAN_TYPE] = Enum.plan_type[raw[const.CSV_PLAN_TYPE]]
    else:
        print("PLAN_TYPE")
        return False

    if raw[const.CSV_QHP_TYPE] in Enum.qhp_type:
        attr[const.QHP_TYPE] = Enum.qhp_type[raw[const.CSV_QHP_TYPE]]
    else:
        print("QHP_TYPE")
        return False

    if raw[const.CSV_DESIGN_TYPE] in Enum.design_type:
        attr[const.DESIGN_TYPE] = Enum.design_type[raw[const.CSV_DESIGN_TYPE]]
    else:
        print("DESIGN_TYPE")
        return False

    if raw[const.CSV_CHILD_ONLY] in Enum.child_only_type:
        attr[const.CHILD_ONLY] = Enum.child_only_type[raw[const.CSV_CHILD_ONLY]]
    else:
        print("CHILD_ONLY")
        return False

    if raw[const.CSV_COMPOSITE_RATE] == 'Yes':
        attr[const.COMPOSITE_RATE] = True
    else:
        attr[const.COMPOSITE_RATE] = False

    if raw[const.CSV_OUT_COUNTRY_COV] == 'Yes':
        attr[const.OUT_COUNTRY_COV] = True
    else:
        attr[const.OUT_COUNTRY_COV] = False

    if raw[const.CSV_OUT_COUNTRY_COV_DESC].strip():
        attr[const.OUT_COUNTRY_COV_DESC] = raw[const.CSV_OUT_COUNTRY_COV_DESC]

    if raw[const.CSV_OUT_SERV_AREA_COV] == 'Yes':
        attr[const.OUT_SERV_AREA_COV] = True
    else:
        attr[const.OUT_SERV_AREA_COV] = False

    if raw[const.CSV_OUT_SERV_AREA_COV_DESC].strip():
        attr[const.OUT_SERV_AREA_COV_DESC] = raw[const.CSV_OUT_SERV_AREA_COV_DESC]

    if raw[const.CSV_PLAN_EXCLUSIONS].strip():
        attr[const.PLAN_EXCLUSIONS] = raw[const.CSV_PLAN_EXCLUSIONS]

    # if raw[const.CSV_EST_ADV_PAYMENT_INDIAN].strip():
    #     plan[const.EST_ADV_PAYMENT_INDIAN] = raw[const.CSV_EST_ADV_PAYMENT_INDIAN].lstrip("$")

    if raw[const.CSV_MULTI_NETWORK] == 'Yes':
        attr[const.MULTI_NETWORK] = True
    else:
        attr[const.MULTI_NETWORK] = False

    if raw[const.CSV_FIRST_TIER_UTIL].strip():
        attr[const.FIRST_TIER_UTIL] = raw[const.CSV_FIRST_TIER_UTIL].rstrip("%")

    if raw[const.CSV_SECOND_TIER_UTIL].strip():
        attr[const.SECOND_TIER_UTIL] = raw[const.CSV_SECOND_TIER_UTIL].rstrip("%")

    if raw[const.CSV_EFFECTIVE_DATE].strip():
        attr[const.EFFECTIVE_DATE] = raw[const.CSV_EFFECTIVE_DATE]

    if raw[const.CSV_EXPIRATION_DATE].strip():
        attr[const.EXPIRATION_DATE] = raw[const.CSV_EXPIRATION_DATE]

    save_data(const.TABLE_PLAN, attr)

    return True


def add_dental_plan(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID].strip():
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_METAL_LEVEL] in Enum.d_metal_type:
        attr[const.D_METAL_LEVEL] = Enum.d_metal_type[raw[const.CSV_METAL_LEVEL]]
    else:
        return False

    if raw[const.CSV_EHB_PEDIATRIC_QTY].strip():
        attr[const.EHB_PEDIATRIC_QTY] = raw[const.CSV_EHB_PEDIATRIC_QTY]

    if raw[const.CSV_GUARANTEED_RATE] == 'Yes':
        attr[const.GUARANTEED_RATE] = True
    else:
        attr[const.GUARANTEED_RATE] = False

    # print(dental_plan)

    save_data(const.TABLE_DENTAL_PLAN, attr)

    return True


def add_dental_plan_moop(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID].strip():
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_MOOP].strip():
        attr[const.INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_MOOP].strip():
        attr[const.INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_MOOP].strip():
        attr[const.INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_MOOP])

    if raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_MOOP].strip():
        attr[const.INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_MOOP].strip():
        attr[const.INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_MOOP].strip():
        attr[const.INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_MOOP])

    if raw[const.CSV_MEHB_OON_INDIVIDUAL_MOOP].strip():
        attr[const.OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_OON_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_OON_FAM_PERSON_MOOP].strip():
        attr[const.OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_OON_FAM_GROUP_MOOP].strip():
        attr[const.OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_GROUP_MOOP])

    if raw[const.CSV_MEHB_COMB_INDIVIDUAL_MOOP].strip():
        attr[const.COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_COMB_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_COMB_FAM_PERSON_MOOP].strip():
        attr[const.COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_COMB_FAM_GROUP_MOOP].strip():
        attr[const.COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_GROUP_MOOP])

    save_data(const.TABLE_D_PLAN_MOOP, attr)


def add_dental_plan_ded(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID].strip():
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_DED].strip():
        attr[const.INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_DED].strip():
        attr[const.INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_DED].strip():
        attr[const.INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_DED])

    if raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_DED].strip():
        attr[const.INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_DED].strip():
        attr[const.INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_DED].strip():
        attr[const.INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_DED])

    if raw[const.CSV_MEHB_OON_INDIVIDUAL_DED].strip():
        attr[const.OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_OON_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_OON_FAM_PERSON_DED].strip():
        attr[const.OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_OON_FAM_GROUP_DED].strip():
        attr[const.OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_GROUP_DED])

    if raw[const.CSV_MEHB_COMB_INDIVIDUAL_DED].strip():
        attr[const.COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_COMB_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_COMB_FAM_PERSON_DED].strip():
        attr[const.COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_COMB_FAM_GROUP_DED].strip():
        attr[const.COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_GROUP_DED])

    save_data(const.TABLE_D_PLAN_DED, attr)


def add_medical_plan(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID].strip():
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_METAL_LEVEL] in Enum.m_metal_type:
        attr[const.M_METAL_LEVEL] = Enum.m_metal_type[raw[const.CSV_METAL_LEVEL]]
    else:
        return False

    if raw[const.CSV_PREG_NOTICE] == 'Yes':
        attr[const.PREG_NOTICE] = True
    else:
        attr[const.PREG_NOTICE] = False

    if raw[const.CSV_WELLNESS_OFFER] == 'Yes':
        attr[const.WELLNESS_OFFER] = True
    else:
        attr[const.WELLNESS_OFFER] = False

    if raw[const.CSV_UNI_DESIGN] == 'Yes':
        attr[const.UNI_DESIGN] = True
    else:
        attr[const.UNI_DESIGN] = False

    if raw[const.CSV_EHB_PERCENT].strip():
        attr[const.EHB_PERCENT] = raw[const.CSV_EHB_PERCENT]

    # print(medical_plan)
    save_data(const.TABLE_MEDICAL_PLAN, attr)

    return True


def add_medical_plan_referral(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID].strip():
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_REFERRAL].strip():
        attr[const.REFERRAL] = raw[const.CSV_REFERRAL]

    print(attr)

    save_data(const.TABLE_M_PLAN_REFERRAL, attr)


def add_medical_plan_sbc(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID].strip():
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_DED_BABY].strip():
        attr[const.DED_BABY] = utils.get_num_int(raw[const.CSV_DED_BABY])

    if raw[const.CSV_COPAY_BABY].strip():
        attr[const.COPAY_BABY] = utils.get_num_int(raw[const.CSV_COPAY_BABY])

    if raw[const.CSV_COINS_BABY].strip():
        attr[const.COINS_BABY] = utils.get_num_int(raw[const.CSV_COINS_BABY])

    if raw[const.CSV_LIMIT_BABY].strip():
        attr[const.LIMIT_BABY] = utils.get_num_int(raw[const.CSV_LIMIT_BABY])

    if raw[const.CSV_DED_DIABETES].strip():
        attr[const.DED_DIABETES] = utils.get_num_int(raw[const.CSV_DED_DIABETES])

    if raw[const.CSV_COPAY_DIABETES].strip():
        attr[const.COPAY_DIABETES] = utils.get_num_int(raw[const.CSV_COPAY_DIABETES])

    if raw[const.CSV_COINS_DIABETES].strip():
        attr[const.COINS_DIABETES] = utils.get_num_int(raw[const.CSV_COINS_DIABETES])

    if raw[const.CSV_LIMIT_DIABETES].strip():
        attr[const.LIMIT_DIABETES] = utils.get_num_int(raw[const.CSV_LIMIT_DIABETES])

    if raw[const.CSV_DED_FRACTURE].strip():
        attr[const.DED_FRACTURE] = utils.get_num_int(raw[const.CSV_DED_FRACTURE])

    if raw[const.CSV_COPAY_FRACTURE].strip():
        attr[const.COPAY_FRACTURE] = utils.get_num_int(raw[const.CSV_COPAY_FRACTURE])

    if raw[const.CSV_COINS_FRACTURE].strip():
        attr[const.COINS_FRACTURE] = utils.get_num_int(raw[const.CSV_COINS_FRACTURE])

    if raw[const.CSV_LIMIT_FRACTURE].strip():
        attr[const.LIMIT_FRACTURE] = utils.get_num_int(raw[const.CSV_LIMIT_FRACTURE])

    save_data(const.TABLE_M_PLAN_SBC, attr)


def add_medical_plan_moop(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID].strip():
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_MOOP].strip():
        attr[const.MEHB_INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_MOOP].strip():
        attr[const.MEHB_INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_MOOP].strip():
        attr[const.MEHB_INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_MOOP])

    if raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_MOOP].strip():
        attr[const.MEHB_INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_MOOP].strip():
        attr[const.MEHB_INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_MOOP].strip():
        attr[const.MEHB_INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_MOOP])

    if raw[const.CSV_MEHB_OON_INDIVIDUAL_MOOP].strip():
        attr[const.MEHB_OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_OON_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_OON_FAM_PERSON_MOOP].strip():
        attr[const.MEHB_OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_OON_FAM_GROUP_MOOP].strip():
        attr[const.MEHB_OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_GROUP_MOOP])

    if raw[const.CSV_MEHB_COMB_INDIVIDUAL_MOOP].strip():
        attr[const.MEHB_COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_COMB_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_COMB_FAM_PERSON_MOOP].strip():
        attr[const.MEHB_COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_COMB_FAM_GROUP_MOOP].strip():
        attr[const.MEHB_COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_GROUP_MOOP])

    if raw[const.CSV_DEHB_INN_TIER1_INDIVIDUAL_MOOP].strip():
        attr[const.DEHB_INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_INDIVIDUAL_MOOP])

    if raw[const.CSV_DEHB_INN_TIER1_FAM_PERSON_MOOP].strip():
        attr[const.DEHB_INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_FAM_PERSON_MOOP])

    if raw[const.CSV_DEHB_INN_TIER1_FAM_GROUP_MOOP].strip():
        attr[const.DEHB_INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_FAM_GROUP_MOOP])

    if raw[const.CSV_DEHB_INN_TIER2_INDIVIDUAL_MOOP].strip():
        attr[const.DEHB_INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_INDIVIDUAL_MOOP])

    if raw[const.CSV_DEHB_INN_TIER2_FAM_PERSON_MOOP].strip():
        attr[const.DEHB_INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_FAM_PERSON_MOOP])

    if raw[const.CSV_DEHB_INN_TIER2_FAM_GROUP_MOOP].strip():
        attr[const.DEHB_INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_FAM_GROUP_MOOP])

    if raw[const.CSV_DEHB_OON_INDIVIDUAL_MOOP].strip():
        attr[const.DEHB_OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_OON_INDIVIDUAL_MOOP])

    if raw[const.CSV_DEHB_OON_FAM_PERSON_MOOP].strip():
        attr[const.DEHB_OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_OON_FAM_PERSON_MOOP])

    if raw[const.CSV_DEHB_OON_FAM_GROUP_MOOP].strip():
        attr[const.DEHB_OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_OON_FAM_GROUP_MOOP])

    if raw[const.CSV_DEHB_COMB_INDIVIDUAL_MOOP].strip():
        attr[const.DEHB_COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_COMB_INDIVIDUAL_MOOP])

    if raw[const.CSV_DEHB_COMB_FAM_PERSON_MOOP].strip():
        attr[const.DEHB_COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_COMB_FAM_PERSON_MOOP])

    if raw[const.CSV_DEHB_COMB_FAM_GROUP_MOOP].strip():
        attr[const.DEHB_COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_COMB_FAM_GROUP_MOOP])

    save_data(const.TABLE_M_PLAN_MOOP, attr)


def add_medical_plan_moop_int(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID].strip():
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_TEHB_INN_TIER1_INDIVIDUAL_MOOP].strip():
        attr[const.TEHB_INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_INDIVIDUAL_MOOP])

    if raw[const.CSV_TEHB_INN_TIER1_FAM_PERSON_MOOP].strip():
        attr[const.TEHB_INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_FAM_PERSON_MOOP])

    if raw[const.CSV_TEHB_INN_TIER1_FAM_GROUP_MOOP].strip():
        attr[const.TEHB_INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_FAM_GROUP_MOOP])

    if raw[const.CSV_TEHB_INN_TIER2_INDIVIDUAL_MOOP].strip():
        attr[const.TEHB_INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_INDIVIDUAL_MOOP])

    if raw[const.CSV_TEHB_INN_TIER2_FAM_PERSON_MOOP].strip():
        attr[const.TEHB_INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_FAM_PERSON_MOOP])

    if raw[const.CSV_TEHB_INN_TIER2_FAM_GROUP_MOOP].strip():
        attr[const.TEHB_INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_FAM_GROUP_MOOP])

    if raw[const.CSV_TEHB_OON_INDIVIDUAL_MOOP].strip():
        attr[const.TEHB_OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_OON_INDIVIDUAL_MOOP])

    if raw[const.CSV_TEHB_OON_FAM_PERSON_MOOP].strip():
        attr[const.TEHB_OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_OON_FAM_PERSON_MOOP])

    if raw[const.CSV_TEHB_OON_FAM_GROUP_MOOP].strip():
        attr[const.TEHB_OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_OON_FAM_GROUP_MOOP])

    if raw[const.CSV_TEHB_COMB_INDIVIDUAL_MOOP].strip():
        attr[const.TEHB_COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_COMB_INDIVIDUAL_MOOP])

    if raw[const.CSV_TEHB_COMB_FAM_PERSON_MOOP].strip():
        attr[const.TEHB_COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_COMB_FAM_PERSON_MOOP])

    if raw[const.CSV_TEHB_COMB_FAM_GROUP_MOOP].strip():
        attr[const.TEHB_COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_COMB_FAM_GROUP_MOOP])

    save_data(const.TABLE_M_PLAN_MOOP_INT, attr)


def add_medical_plan_ded(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID].strip():
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_DED].strip():
        attr[const.MEHB_INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_DED].strip():
        attr[const.MEHB_INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_DED].strip():
        attr[const.MEHB_INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_DED])

    if raw[const.CSV_MEHB_INN_TIER1_COINS_DED].strip():
        attr[const.MEHB_INN_TIER1_COINS] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_COINS_DED])

    if raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_DED].strip():
        attr[const.MEHB_INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_DED].strip():
        attr[const.MEHB_INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_DED].strip():
        attr[const.MEHB_INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_DED])

    if raw[const.CSV_MEHB_INN_TIER2_COINS_DED].strip():
        attr[const.MEHB_INN_TIER2_COINS] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_COINS_DED])

    if raw[const.CSV_MEHB_OON_INDIVIDUAL_DED].strip():
        attr[const.MEHB_OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_OON_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_OON_FAM_PERSON_DED].strip():
        attr[const.MEHB_OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_OON_FAM_GROUP_DED].strip():
        attr[const.MEHB_OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_GROUP_DED])

    if raw[const.CSV_MEHB_COMB_INDIVIDUAL_DED].strip():
        attr[const.MEHB_COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_COMB_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_COMB_FAM_PERSON_DED].strip():
        attr[const.MEHB_COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_COMB_FAM_GROUP_DED].strip():
        attr[const.MEHB_COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_GROUP_DED])

    if raw[const.CSV_DEHB_INN_TIER1_INDIVIDUAL_DED].strip():
        attr[const.DEHB_INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_INDIVIDUAL_DED])

    if raw[const.CSV_DEHB_INN_TIER1_FAM_PERSON_DED].strip():
        attr[const.DEHB_INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_FAM_PERSON_DED])

    if raw[const.CSV_DEHB_INN_TIER1_FAM_GROUP_DED].strip():
        attr[const.DEHB_INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_FAM_GROUP_DED])

    if raw[const.CSV_DEHB_INN_TIER1_COINS_DED].strip():
        attr[const.DEHB_INN_TIER1_COINS] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_COINS_DED])

    if raw[const.CSV_DEHB_INN_TIER2_INDIVIDUAL_DED].strip():
        attr[const.DEHB_INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_INDIVIDUAL_DED])

    if raw[const.CSV_DEHB_INN_TIER2_FAM_PERSON_DED].strip():
        attr[const.DEHB_INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_FAM_PERSON_DED])

    if raw[const.CSV_DEHB_INN_TIER2_FAM_GROUP_DED].strip():
        attr[const.DEHB_INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_FAM_GROUP_DED])

    if raw[const.CSV_DEHB_INN_TIER2_COINS_DED].strip():
        attr[const.DEHB_INN_TIER2_COINS] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_COINS_DED])

    if raw[const.CSV_DEHB_OON_INDIVIDUAL_DED].strip():
        attr[const.DEHB_OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_OON_INDIVIDUAL_DED])

    if raw[const.CSV_DEHB_OON_FAM_PERSON_DED].strip():
        attr[const.DEHB_OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_OON_FAM_PERSON_DED])

    if raw[const.CSV_DEHB_OON_FAM_GROUP_DED].strip():
        attr[const.DEHB_OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_OON_FAM_GROUP_DED])

    if raw[const.CSV_DEHB_COMB_INDIVIDUAL_DED].strip():
        attr[const.DEHB_COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_COMB_INDIVIDUAL_DED])

    if raw[const.CSV_DEHB_COMB_FAM_PERSON_DED].strip():
        attr[const.DEHB_COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_COMB_FAM_PERSON_DED])

    if raw[const.CSV_DEHB_COMB_FAM_GROUP_DED].strip():
        attr[const.DEHB_COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_COMB_FAM_GROUP_DED])

    save_data(const.TABLE_M_PLAN_DED, attr)


def add_medical_plan_ded_int(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID].strip():
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_TEHB_INN_TIER1_INDIVIDUAL_DED].strip():
        attr[const.TEHB_INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_INDIVIDUAL_DED])

    if raw[const.CSV_TEHB_INN_TIER1_FAM_PERSON_DED].strip():
        attr[const.TEHB_INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_FAM_PERSON_DED])

    if raw[const.CSV_TEHB_INN_TIER1_FAM_GROUP_DED].strip():
        attr[const.TEHB_INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_FAM_GROUP_DED])

    if raw[const.CSV_TEHB_INN_TIER1_COINS_DED].strip():
        attr[const.TEHB_INN_TIER1_COINS] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_COINS_DED])

    if raw[const.CSV_TEHB_INN_TIER2_INDIVIDUAL_DED].strip():
        attr[const.TEHB_INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_INDIVIDUAL_DED])

    if raw[const.CSV_TEHB_INN_TIER2_FAM_PERSON_DED].strip():
        attr[const.TEHB_INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_FAM_PERSON_DED])

    if raw[const.CSV_TEHB_INN_TIER2_FAM_GROUP_DED].strip():
        attr[const.TEHB_INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_FAM_GROUP_DED])

    if raw[const.CSV_TEHB_INN_TIER2_COINS_DED].strip():
        attr[const.TEHB_INN_TIER2_COINS] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_COINS_DED])

    if raw[const.CSV_TEHB_OON_INDIVIDUAL_DED].strip():
        attr[const.TEHB_OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_OON_INDIVIDUAL_DED])

    if raw[const.CSV_TEHB_OON_FAM_PERSON_DED].strip():
        attr[const.TEHB_OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_OON_FAM_PERSON_DED])

    if raw[const.CSV_TEHB_OON_FAM_GROUP_DED].strip():
        attr[const.TEHB_OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_OON_FAM_GROUP_DED])

    if raw[const.CSV_TEHB_COMB_INDIVIDUAL_DED].strip():
        attr[const.TEHB_COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_COMB_INDIVIDUAL_DED])

    if raw[const.CSV_TEHB_COMB_FAM_PERSON_DED].strip():
        attr[const.TEHB_COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_COMB_FAM_PERSON_DED])

    if raw[const.CSV_TEHB_COMB_FAM_GROUP_DED].strip():
        attr[const.TEHB_COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_COMB_FAM_GROUP_DED])

    save_data(const.TABLE_M_PLAN_DED_INT, attr)


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
    load_plans()
    conn.commit()
