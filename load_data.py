import csv
import psycopg2.extras
import pymongo

import utils
import constants as const
from datetime import datetime
from enumeration import Enum
from psycopg2.extensions import AsIs

file_plan = "2020-dataset/Plan_Attributes_PUF.csv"
file_benefits = "2020-dataset/Benefits_Cost_Sharing_PUF.csv"
file_rate = "2020-dataset/Rate_PUF.csv"
file_business_rules = "2020-dataset/Business_Rules_PUF.csv"


def save_data(table, attributes):
    """
    Insert tuple into postgres
    :param table: relation name
    :param attributes: relation attributes and value
    :return: N/A
    """
    columns = attributes.keys()
    values = [attributes[column] for column in columns]

    insert_statement = 'insert into %s (%s) values %s'
    cursor.execute(insert_statement, (AsIs(table),
                                      AsIs(','.join(columns)),
                                      tuple(values)))


def load_plans():
    """
    Load Plan_Attributes CSV file into database
    :return:
    """
    print("------LOAD Plan_Attributes_PUF.csv------")
    collection = mongodb[const.COL_MEDICAL_DISEASE]

    with open(file_plan, mode='r', encoding='iso-8859-1') as fd:
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

            # Plans that use multiple tiers
            if raw_data[const.CSV_MULTI_NETWORK] == 'Yes':
                add_plan_multi_network(raw_data)

            # Divide plan into dental and medical
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

                if raw_data[const.CSV_DISEASE_PROGRAM]:
                    add_medical_plan_disease(raw_data, collection)

            count += 1
            print('\rLoading Process:{:.2f}%'.format(count * 100 / rows), end='')

    conn.commit()
    print("\nDONE!")


def add_plan_general_info(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ISSUER_ID]:
        attr[const.PLAN_ISSUER_ID] = raw[const.CSV_PLAN_ISSUER_ID]

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_PLAN_VAR_NAME]:
        attr[const.PLAN_VAR_NAME] = raw[const.CSV_PLAN_VAR_NAME]

    if raw[const.CSV_PLAN_MARK_NAME]:
        attr[const.PLAN_MARK_NAME] = raw[const.CSV_PLAN_MARK_NAME]

    if raw[const.CSV_STD_COMP_ID]:
        attr[const.STD_COMP_ID] = raw[const.CSV_STD_COMP_ID]

    if raw[const.CSV_PLAN_YEAR]:
        attr[const.PLAN_YEAR] = raw[const.CSV_PLAN_YEAR]

    if raw[const.CSV_PLAN_STATE]:
        attr[const.PLAN_STATE] = raw[const.CSV_PLAN_STATE]

    if raw[const.CSV_SOURCE_NAME]:
        attr[const.SOURCE_NAME] = raw[const.CSV_SOURCE_NAME]

    if raw[const.CSV_IMPORT_DATE]:
        ts = datetime.strptime(raw[const.CSV_IMPORT_DATE], "%m/%d/%Y %H:%M")
        attr[const.IMPORT_DATE] = ts.strftime("%Y-%m-%d %H:%M:%S")

    if raw[const.CSV_HIOS_PROD_ID]:
        attr[const.HIOS_PROD_ID] = raw[const.CSV_HIOS_PROD_ID]

    if raw[const.CSV_HPID]:
        attr[const.HPID] = raw[const.CSV_HPID]

    if raw[const.CSV_NETWORK_ID]:
        attr[const.NETWORK_ID] = raw[const.CSV_NETWORK_ID]

    if raw[const.CSV_SERV_AREA_ID]:
        attr[const.SERV_AREA_ID] = raw[const.CSV_SERV_AREA_ID]

    if raw[const.CSV_FORMULARY_ID]:
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

    if raw[const.CSV_OUT_COUNTRY_COV_DESC]:
        attr[const.OUT_COUNTRY_COV_DESC] = raw[const.CSV_OUT_COUNTRY_COV_DESC]

    if raw[const.CSV_OUT_SERV_AREA_COV] == 'Yes':
        attr[const.OUT_SERV_AREA_COV] = True
    else:
        attr[const.OUT_SERV_AREA_COV] = False

    if raw[const.CSV_OUT_SERV_AREA_COV_DESC]:
        attr[const.OUT_SERV_AREA_COV_DESC] = raw[const.CSV_OUT_SERV_AREA_COV_DESC]

    if raw[const.CSV_PLAN_EXCLUSIONS]:
        attr[const.PLAN_EXCLUSIONS] = raw[const.CSV_PLAN_EXCLUSIONS]

    if raw[const.CSV_EFFECTIVE_DATE]:
        attr[const.EFFECTIVE_DATE] = raw[const.CSV_EFFECTIVE_DATE]

    if raw[const.CSV_EXPIRATION_DATE]:
        attr[const.EXPIRATION_DATE] = raw[const.CSV_EXPIRATION_DATE]

    if raw[const.CSV_URL_ENROLLMENT]:
        attr[const.URL_ENROLLMENT] = raw[const.CSV_URL_ENROLLMENT]

    if raw[const.CSV_URL_FORMULARY]:
        attr[const.URL_FORMULARY] = raw[const.CSV_URL_FORMULARY]

    if raw[const.CSV_URL_BROCHURE]:
        attr[const.URL_BROCHURE] = raw[const.CSV_URL_BROCHURE]

    save_data(const.TABLE_PLAN, attr)

    return True


def add_plan_multi_network(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_FIRST_TIER_UTIL]:
        attr[const.FIRST_TIER_UTIL] = raw[const.CSV_FIRST_TIER_UTIL].rstrip("%")

    if raw[const.CSV_SECOND_TIER_UTIL]:
        attr[const.SECOND_TIER_UTIL] = raw[const.CSV_SECOND_TIER_UTIL].rstrip("%")

    save_data(const.TABLE_PLAN_MULTI_NET, attr)


def add_dental_plan(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_METAL_LEVEL] in Enum.d_metal_type:
        attr[const.D_METAL_LEVEL] = Enum.d_metal_type[raw[const.CSV_METAL_LEVEL]]
    else:
        return False

    if raw[const.CSV_EHB_PEDIATRIC_QTY]:
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

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_MOOP]:
        attr[const.INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_MOOP]:
        attr[const.INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_MOOP]:
        attr[const.INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_MOOP])

    if raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_MOOP]:
        attr[const.INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_MOOP]:
        attr[const.INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_MOOP]:
        attr[const.INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_MOOP])

    if raw[const.CSV_MEHB_OON_INDIVIDUAL_MOOP]:
        attr[const.OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_OON_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_OON_FAM_PERSON_MOOP]:
        attr[const.OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_OON_FAM_GROUP_MOOP]:
        attr[const.OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_GROUP_MOOP])

    if raw[const.CSV_MEHB_COMB_INDIVIDUAL_MOOP]:
        attr[const.COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_COMB_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_COMB_FAM_PERSON_MOOP]:
        attr[const.COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_COMB_FAM_GROUP_MOOP]:
        attr[const.COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_GROUP_MOOP])

    save_data(const.TABLE_D_PLAN_MOOP, attr)


def add_dental_plan_ded(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_DED]:
        attr[const.INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_DED]:
        attr[const.INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_DED]:
        attr[const.INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_DED])

    if raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_DED]:
        attr[const.INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_DED]:
        attr[const.INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_DED]:
        attr[const.INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_DED])

    if raw[const.CSV_MEHB_OON_INDIVIDUAL_DED]:
        attr[const.OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_OON_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_OON_FAM_PERSON_DED]:
        attr[const.OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_OON_FAM_GROUP_DED]:
        attr[const.OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_GROUP_DED])

    if raw[const.CSV_MEHB_COMB_INDIVIDUAL_DED]:
        attr[const.COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_COMB_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_COMB_FAM_PERSON_DED]:
        attr[const.COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_COMB_FAM_GROUP_DED]:
        attr[const.COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_GROUP_DED])

    save_data(const.TABLE_D_PLAN_DED, attr)


def add_medical_plan(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID]:
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

    if raw[const.CSV_EHB_PERCENT]:
        attr[const.EHB_PERCENT] = raw[const.CSV_EHB_PERCENT]

    # print(medical_plan)
    save_data(const.TABLE_MEDICAL_PLAN, attr)

    return True


def add_medical_plan_referral(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_REFERRAL]:
        attr[const.REFERRAL] = raw[const.CSV_REFERRAL]

    # print(attr)

    save_data(const.TABLE_M_PLAN_REFERRAL, attr)


def add_medical_plan_sbc(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_DED_BABY]:
        attr[const.DED_BABY] = utils.get_num_int(raw[const.CSV_DED_BABY])

    if raw[const.CSV_COPAY_BABY]:
        attr[const.COPAY_BABY] = utils.get_num_int(raw[const.CSV_COPAY_BABY])

    if raw[const.CSV_COINS_BABY]:
        attr[const.COINS_BABY] = utils.get_num_int(raw[const.CSV_COINS_BABY])

    if raw[const.CSV_LIMIT_BABY]:
        attr[const.LIMIT_BABY] = utils.get_num_int(raw[const.CSV_LIMIT_BABY])

    if raw[const.CSV_DED_DIABETES]:
        attr[const.DED_DIABETES] = utils.get_num_int(raw[const.CSV_DED_DIABETES])

    if raw[const.CSV_COPAY_DIABETES]:
        attr[const.COPAY_DIABETES] = utils.get_num_int(raw[const.CSV_COPAY_DIABETES])

    if raw[const.CSV_COINS_DIABETES]:
        attr[const.COINS_DIABETES] = utils.get_num_int(raw[const.CSV_COINS_DIABETES])

    if raw[const.CSV_LIMIT_DIABETES]:
        attr[const.LIMIT_DIABETES] = utils.get_num_int(raw[const.CSV_LIMIT_DIABETES])

    if raw[const.CSV_DED_FRACTURE]:
        attr[const.DED_FRACTURE] = utils.get_num_int(raw[const.CSV_DED_FRACTURE])

    if raw[const.CSV_COPAY_FRACTURE]:
        attr[const.COPAY_FRACTURE] = utils.get_num_int(raw[const.CSV_COPAY_FRACTURE])

    if raw[const.CSV_COINS_FRACTURE]:
        attr[const.COINS_FRACTURE] = utils.get_num_int(raw[const.CSV_COINS_FRACTURE])

    if raw[const.CSV_LIMIT_FRACTURE]:
        attr[const.LIMIT_FRACTURE] = utils.get_num_int(raw[const.CSV_LIMIT_FRACTURE])

    save_data(const.TABLE_M_PLAN_SBC, attr)


def add_medical_plan_moop(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_MOOP]:
        attr[const.MEHB_INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_MOOP]:
        attr[const.MEHB_INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_MOOP]:
        attr[const.MEHB_INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_MOOP])

    if raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_MOOP]:
        attr[const.MEHB_INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_MOOP]:
        attr[const.MEHB_INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_MOOP]:
        attr[const.MEHB_INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_MOOP])

    if raw[const.CSV_MEHB_OON_INDIVIDUAL_MOOP]:
        attr[const.MEHB_OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_OON_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_OON_FAM_PERSON_MOOP]:
        attr[const.MEHB_OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_OON_FAM_GROUP_MOOP]:
        attr[const.MEHB_OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_GROUP_MOOP])

    if raw[const.CSV_MEHB_COMB_INDIVIDUAL_MOOP]:
        attr[const.MEHB_COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_COMB_INDIVIDUAL_MOOP])

    if raw[const.CSV_MEHB_COMB_FAM_PERSON_MOOP]:
        attr[const.MEHB_COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_PERSON_MOOP])

    if raw[const.CSV_MEHB_COMB_FAM_GROUP_MOOP]:
        attr[const.MEHB_COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_GROUP_MOOP])

    if raw[const.CSV_DEHB_INN_TIER1_INDIVIDUAL_MOOP]:
        attr[const.DEHB_INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_INDIVIDUAL_MOOP])

    if raw[const.CSV_DEHB_INN_TIER1_FAM_PERSON_MOOP]:
        attr[const.DEHB_INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_FAM_PERSON_MOOP])

    if raw[const.CSV_DEHB_INN_TIER1_FAM_GROUP_MOOP]:
        attr[const.DEHB_INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_FAM_GROUP_MOOP])

    if raw[const.CSV_DEHB_INN_TIER2_INDIVIDUAL_MOOP]:
        attr[const.DEHB_INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_INDIVIDUAL_MOOP])

    if raw[const.CSV_DEHB_INN_TIER2_FAM_PERSON_MOOP]:
        attr[const.DEHB_INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_FAM_PERSON_MOOP])

    if raw[const.CSV_DEHB_INN_TIER2_FAM_GROUP_MOOP]:
        attr[const.DEHB_INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_FAM_GROUP_MOOP])

    if raw[const.CSV_DEHB_OON_INDIVIDUAL_MOOP]:
        attr[const.DEHB_OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_OON_INDIVIDUAL_MOOP])

    if raw[const.CSV_DEHB_OON_FAM_PERSON_MOOP]:
        attr[const.DEHB_OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_OON_FAM_PERSON_MOOP])

    if raw[const.CSV_DEHB_OON_FAM_GROUP_MOOP]:
        attr[const.DEHB_OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_OON_FAM_GROUP_MOOP])

    if raw[const.CSV_DEHB_COMB_INDIVIDUAL_MOOP]:
        attr[const.DEHB_COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_COMB_INDIVIDUAL_MOOP])

    if raw[const.CSV_DEHB_COMB_FAM_PERSON_MOOP]:
        attr[const.DEHB_COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_COMB_FAM_PERSON_MOOP])

    if raw[const.CSV_DEHB_COMB_FAM_GROUP_MOOP]:
        attr[const.DEHB_COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_COMB_FAM_GROUP_MOOP])

    save_data(const.TABLE_M_PLAN_MOOP, attr)


def add_medical_plan_moop_int(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_TEHB_INN_TIER1_INDIVIDUAL_MOOP]:
        attr[const.TEHB_INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_INDIVIDUAL_MOOP])

    if raw[const.CSV_TEHB_INN_TIER1_FAM_PERSON_MOOP]:
        attr[const.TEHB_INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_FAM_PERSON_MOOP])

    if raw[const.CSV_TEHB_INN_TIER1_FAM_GROUP_MOOP]:
        attr[const.TEHB_INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_FAM_GROUP_MOOP])

    if raw[const.CSV_TEHB_INN_TIER2_INDIVIDUAL_MOOP]:
        attr[const.TEHB_INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_INDIVIDUAL_MOOP])

    if raw[const.CSV_TEHB_INN_TIER2_FAM_PERSON_MOOP]:
        attr[const.TEHB_INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_FAM_PERSON_MOOP])

    if raw[const.CSV_TEHB_INN_TIER2_FAM_GROUP_MOOP]:
        attr[const.TEHB_INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_FAM_GROUP_MOOP])

    if raw[const.CSV_TEHB_OON_INDIVIDUAL_MOOP]:
        attr[const.TEHB_OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_OON_INDIVIDUAL_MOOP])

    if raw[const.CSV_TEHB_OON_FAM_PERSON_MOOP]:
        attr[const.TEHB_OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_OON_FAM_PERSON_MOOP])

    if raw[const.CSV_TEHB_OON_FAM_GROUP_MOOP]:
        attr[const.TEHB_OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_OON_FAM_GROUP_MOOP])

    if raw[const.CSV_TEHB_COMB_INDIVIDUAL_MOOP]:
        attr[const.TEHB_COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_COMB_INDIVIDUAL_MOOP])

    if raw[const.CSV_TEHB_COMB_FAM_PERSON_MOOP]:
        attr[const.TEHB_COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_COMB_FAM_PERSON_MOOP])

    if raw[const.CSV_TEHB_COMB_FAM_GROUP_MOOP]:
        attr[const.TEHB_COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_COMB_FAM_GROUP_MOOP])

    save_data(const.TABLE_M_PLAN_MOOP_INT, attr)


def add_medical_plan_ded(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_DED]:
        attr[const.MEHB_INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_DED]:
        attr[const.MEHB_INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_DED]:
        attr[const.MEHB_INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_FAM_GROUP_DED])

    if raw[const.CSV_MEHB_INN_TIER1_COINS_DED]:
        attr[const.MEHB_INN_TIER1_COINS] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER1_COINS_DED])

    if raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_DED]:
        attr[const.MEHB_INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_DED]:
        attr[const.MEHB_INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_DED]:
        attr[const.MEHB_INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_FAM_GROUP_DED])

    if raw[const.CSV_MEHB_INN_TIER2_COINS_DED]:
        attr[const.MEHB_INN_TIER2_COINS] = utils.get_num_int(raw[const.CSV_MEHB_INN_TIER2_COINS_DED])

    if raw[const.CSV_MEHB_OON_INDIVIDUAL_DED]:
        attr[const.MEHB_OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_OON_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_OON_FAM_PERSON_DED]:
        attr[const.MEHB_OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_OON_FAM_GROUP_DED]:
        attr[const.MEHB_OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_OON_FAM_GROUP_DED])

    if raw[const.CSV_MEHB_COMB_INDIVIDUAL_DED]:
        attr[const.MEHB_COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_MEHB_COMB_INDIVIDUAL_DED])

    if raw[const.CSV_MEHB_COMB_FAM_PERSON_DED]:
        attr[const.MEHB_COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_PERSON_DED])

    if raw[const.CSV_MEHB_COMB_FAM_GROUP_DED]:
        attr[const.MEHB_COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_MEHB_COMB_FAM_GROUP_DED])

    if raw[const.CSV_DEHB_INN_TIER1_INDIVIDUAL_DED]:
        attr[const.DEHB_INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_INDIVIDUAL_DED])

    if raw[const.CSV_DEHB_INN_TIER1_FAM_PERSON_DED]:
        attr[const.DEHB_INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_FAM_PERSON_DED])

    if raw[const.CSV_DEHB_INN_TIER1_FAM_GROUP_DED]:
        attr[const.DEHB_INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_FAM_GROUP_DED])

    if raw[const.CSV_DEHB_INN_TIER1_COINS_DED]:
        attr[const.DEHB_INN_TIER1_COINS] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER1_COINS_DED])

    if raw[const.CSV_DEHB_INN_TIER2_INDIVIDUAL_DED]:
        attr[const.DEHB_INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_INDIVIDUAL_DED])

    if raw[const.CSV_DEHB_INN_TIER2_FAM_PERSON_DED]:
        attr[const.DEHB_INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_FAM_PERSON_DED])

    if raw[const.CSV_DEHB_INN_TIER2_FAM_GROUP_DED]:
        attr[const.DEHB_INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_FAM_GROUP_DED])

    if raw[const.CSV_DEHB_INN_TIER2_COINS_DED]:
        attr[const.DEHB_INN_TIER2_COINS] = utils.get_num_int(raw[const.CSV_DEHB_INN_TIER2_COINS_DED])

    if raw[const.CSV_DEHB_OON_INDIVIDUAL_DED]:
        attr[const.DEHB_OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_OON_INDIVIDUAL_DED])

    if raw[const.CSV_DEHB_OON_FAM_PERSON_DED]:
        attr[const.DEHB_OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_OON_FAM_PERSON_DED])

    if raw[const.CSV_DEHB_OON_FAM_GROUP_DED]:
        attr[const.DEHB_OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_OON_FAM_GROUP_DED])

    if raw[const.CSV_DEHB_COMB_INDIVIDUAL_DED]:
        attr[const.DEHB_COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_DEHB_COMB_INDIVIDUAL_DED])

    if raw[const.CSV_DEHB_COMB_FAM_PERSON_DED]:
        attr[const.DEHB_COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_DEHB_COMB_FAM_PERSON_DED])

    if raw[const.CSV_DEHB_COMB_FAM_GROUP_DED]:
        attr[const.DEHB_COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_DEHB_COMB_FAM_GROUP_DED])

    save_data(const.TABLE_M_PLAN_DED, attr)


def add_medical_plan_ded_int(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_TEHB_INN_TIER1_INDIVIDUAL_DED]:
        attr[const.TEHB_INN_TIER1_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_INDIVIDUAL_DED])

    if raw[const.CSV_TEHB_INN_TIER1_FAM_PERSON_DED]:
        attr[const.TEHB_INN_TIER1_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_FAM_PERSON_DED])

    if raw[const.CSV_TEHB_INN_TIER1_FAM_GROUP_DED]:
        attr[const.TEHB_INN_TIER1_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_FAM_GROUP_DED])

    if raw[const.CSV_TEHB_INN_TIER1_COINS_DED]:
        attr[const.TEHB_INN_TIER1_COINS] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER1_COINS_DED])

    if raw[const.CSV_TEHB_INN_TIER2_INDIVIDUAL_DED]:
        attr[const.TEHB_INN_TIER2_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_INDIVIDUAL_DED])

    if raw[const.CSV_TEHB_INN_TIER2_FAM_PERSON_DED]:
        attr[const.TEHB_INN_TIER2_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_FAM_PERSON_DED])

    if raw[const.CSV_TEHB_INN_TIER2_FAM_GROUP_DED]:
        attr[const.TEHB_INN_TIER2_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_FAM_GROUP_DED])

    if raw[const.CSV_TEHB_INN_TIER2_COINS_DED]:
        attr[const.TEHB_INN_TIER2_COINS] = utils.get_num_int(raw[const.CSV_TEHB_INN_TIER2_COINS_DED])

    if raw[const.CSV_TEHB_OON_INDIVIDUAL_DED]:
        attr[const.TEHB_OON_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_OON_INDIVIDUAL_DED])

    if raw[const.CSV_TEHB_OON_FAM_PERSON_DED]:
        attr[const.TEHB_OON_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_OON_FAM_PERSON_DED])

    if raw[const.CSV_TEHB_OON_FAM_GROUP_DED]:
        attr[const.TEHB_OON_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_OON_FAM_GROUP_DED])

    if raw[const.CSV_TEHB_COMB_INDIVIDUAL_DED]:
        attr[const.TEHB_COMB_INDIVIDUAL] = utils.get_num_int(raw[const.CSV_TEHB_COMB_INDIVIDUAL_DED])

    if raw[const.CSV_TEHB_COMB_FAM_PERSON_DED]:
        attr[const.TEHB_COMB_FAM_PERSON] = utils.get_num_int(raw[const.CSV_TEHB_COMB_FAM_PERSON_DED])

    if raw[const.CSV_TEHB_COMB_FAM_GROUP_DED]:
        attr[const.TEHB_COMB_FAM_GROUP] = utils.get_num_int(raw[const.CSV_TEHB_COMB_FAM_GROUP_DED])

    save_data(const.TABLE_M_PLAN_DED_INT, attr)


def add_medical_plan_disease(raw, collection):
    record = dict()

    record["_id"] = raw[const.CSV_PLAN_ID]
    record["disease"] = raw[const.CSV_DISEASE_PROGRAM]

    collection.insert_one(record)


def load_benefits():
    """
    Load Benefits Cost Sharing CSV file into database
    :return:
    """
    print("------LOAD Benefits_Cost_Sharing_PUF.csv------")

    with open(file_benefits, mode='r', encoding='iso-8859-1') as fd:
        # Count total row number
        reader = csv.DictReader(fd)
        count = 0
        rows = sum(1 for _ in reader)
        fd.seek(0)

        # Loading data into database
        reader = csv.DictReader(fd)
        for raw_data in reader:
            if raw_data[const.CSV_IS_COVER] == 'Covered':
                add_plan_benefits(raw_data)

                if raw_data[const.CSV_QUANT_LIMIT] == 'Yes':
                    add_plan_benefits_limit(raw_data)

            count += 1
            print('\rLoading Process:{:.2f}%'.format(count * 100 / rows), end='')

    conn.commit()
    print("\nDONE!")


def add_plan_benefits(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_BENEFIT_NAME]:
        attr[const.BENEFIT_NAME] = raw[const.CSV_BENEFIT_NAME]

    if raw[const.CSV_COPAY_INN_TIER1]:
        attr[const.COPAY_INN_TIER1] = utils.get_num_decimal(raw[const.CSV_COPAY_INN_TIER1])
        desc = utils.get_desc(raw[const.CSV_COPAY_INN_TIER1])
        if desc:
            if desc == 'Not Applicable':
                attr[const.COPAY_INN_TIER1] = None
            attr[const.COPAY_INN_TIER1_TYPE] = Enum.copay_type[desc]
        else:
            attr[const.COPAY_INN_TIER1_TYPE] = Enum.copay_type["Copay"]
    else:
        attr[const.COPAY_INN_TIER1] = None
        attr[const.COPAY_INN_TIER1_TYPE] = Enum.copay_type["Not Applicable"]

    if raw[const.CSV_COPAY_INN_TIER2]:
        attr[const.COPAY_INN_TIER2] = utils.get_num_decimal(raw[const.CSV_COPAY_INN_TIER2])
        desc = utils.get_desc(raw[const.CSV_COPAY_INN_TIER2])
        if desc:
            if desc == 'Not Applicable':
                attr[const.COPAY_INN_TIER2] = None
            attr[const.COPAY_INN_TIER2_TYPE] = Enum.copay_type[desc]
        else:
            attr[const.COPAY_INN_TIER2_TYPE] = Enum.copay_type["Copay"]
    else:
        attr[const.COPAY_INN_TIER2] = None
        attr[const.COPAY_INN_TIER2_TYPE] = Enum.copay_type["Not Applicable"]

    if raw[const.CSV_COPAY_OON]:
        attr[const.COPAY_OON] = utils.get_num_decimal(raw[const.CSV_COPAY_OON])
        desc = utils.get_desc(raw[const.CSV_COPAY_OON])
        if desc:
            if desc == 'Not Applicable':
                attr[const.COPAY_OON] = None
            attr[const.COPAY_OON_TYPE] = Enum.copay_type[desc]
        else:
            attr[const.COPAY_OON_TYPE] = Enum.copay_type["Copay"]
    else:
        attr[const.COPAY_OON] = None
        attr[const.COPAY_OON_TYPE] = Enum.copay_type["Not Applicable"]

    if raw[const.CSV_COINS_INN_TIER1]:
        attr[const.COINS_INN_TIER1] = utils.get_num_decimal(raw[const.CSV_COINS_INN_TIER1])
        desc = utils.get_desc(raw[const.CSV_COINS_INN_TIER1])
        if desc:
            if desc == 'Not Applicable':
                attr[const.COINS_INN_TIER1] = None
            attr[const.COINS_INN_TIER1_TYPE] = Enum.coins_type[desc]
        else:
            attr[const.COINS_INN_TIER1_TYPE] = Enum.coins_type["Coinsurance"]
    else:
        attr[const.COINS_INN_TIER1] = None
        attr[const.COINS_INN_TIER1_TYPE] = Enum.coins_type["Not Applicable"]

    if raw[const.CSV_COINS_INN_TIER2]:
        attr[const.COINS_INN_TIER2] = utils.get_num_decimal(raw[const.CSV_COINS_INN_TIER2])
        desc = utils.get_desc(raw[const.CSV_COINS_INN_TIER2])
        if desc:
            if desc == 'Not Applicable':
                attr[const.COINS_INN_TIER2] = None
            attr[const.COINS_INN_TIER2_TYPE] = Enum.coins_type[desc]
        else:
            attr[const.COINS_INN_TIER2_TYPE] = Enum.coins_type["Coinsurance"]
    else:
        attr[const.COINS_INN_TIER2] = None
        attr[const.COINS_INN_TIER2_TYPE] = Enum.coins_type["Not Applicable"]

    if raw[const.CSV_COINS_OON]:
        attr[const.COINS_OON] = utils.get_num_decimal(raw[const.CSV_COINS_OON])
        desc = utils.get_desc(raw[const.CSV_COINS_OON])
        if desc:
            if desc == 'Not Applicable':
                attr[const.COINS_OON] = None
            attr[const.COINS_OON_TYPE] = Enum.coins_type[desc]
        else:
            attr[const.COINS_OON_TYPE] = Enum.coins_type["Coinsurance"]
    else:
        attr[const.COINS_OON] = None
        attr[const.COINS_OON_TYPE] = Enum.coins_type["Not Applicable"]

    if raw[const.CSV_IS_EHB] == 'Yes':
        raw[const.IS_EHB] = True
    else:
        raw[const.IS_EHB] = False

    if raw[const.CSV_EXCL_FROM_INN_MOOP] == 'Yes':
        raw[const.EXCL_FROM_INN_MOOP] = True
    else:
        raw[const.EXCL_FROM_INN_MOOP] = False

    if raw[const.CSV_EXCL_FROM_OON_MOOP] == 'Yes':
        raw[const.EXCL_FROM_OON_MOOP] = True
    else:
        raw[const.EXCL_FROM_OON_MOOP] = False

    if raw[const.CSV_BENEFIT_EXCL]:
        attr[const.BENEFIT_EXCL] = raw[const.CSV_BENEFIT_EXCL]

    # print(attr)

    save_data(const.TABLE_BENEFIT, attr)


def add_plan_benefits_limit(raw):
    attr = dict()

    if raw[const.CSV_PLAN_ID]:
        attr[const.PLAN_ID] = raw[const.CSV_PLAN_ID]

    if raw[const.CSV_BENEFIT_NAME]:
        attr[const.BENEFIT_NAME] = raw[const.CSV_BENEFIT_NAME]

    if raw[const.CSV_BENEFIT_LIMIT_QTY]:
        attr[const.BENEFIT_LIMIT_QTY] = raw[const.CSV_BENEFIT_LIMIT_QTY]

    if raw[const.CSV_BENEFIT_LIMIT_UNIT]:
        attr[const.BENEFIT_LIMIT_UNIT] = raw[const.CSV_BENEFIT_LIMIT_UNIT]

    if raw[const.CSV_BENEFIT_EXPLANATION]:
        attr[const.BENEFIT_EXPLANATION] = raw[const.CSV_BENEFIT_EXPLANATION]

    # print(attr)

    save_data(const.TABLE_BENEFIT_LIMIT, attr)


def load_rate():
    """
    Load Rate CSV file into database
    :return:
    """
    print("------LOAD Rate_PUF.csv------")

    with open(file_rate, mode='r', encoding='iso-8859-1') as fd:
        # Count total row number
        reader = csv.DictReader(fd)
        count = 0
        rows = sum(1 for _ in reader)
        fd.seek(0)

        # Loading data into database
        reader = csv.DictReader(fd)
        for raw_data in reader:
            if raw_data[const.CSV_RATE_AGE] == 'Family Option':
                # Family Rate
                add_rate_family(raw_data)
            else:
                # Individual Rate
                add_rate_individual(raw_data)

            count += 1
            print('\rLoading Process:{:.2f}%'.format(count * 100 / rows), end='')

    conn.commit()
    print("\nDONE!")


def add_rate_individual(raw):
    attr = dict()

    if raw[const.CSV_RATE_EFF_DATE]:
        attr[const.RATE_EFF_DATE] = raw[const.CSV_RATE_EFF_DATE]

    if raw[const.CSV_RATE_EXPI_DATE]:
        attr[const.RATE_EXPI_DATE] = raw[const.CSV_RATE_EXPI_DATE]

    if raw[const.CSV_RATE_STD_COMP_ID]:
        attr[const.RATE_STD_COMP_ID] = raw[const.CSV_RATE_STD_COMP_ID]

    if raw[const.CSV_RATE_AREA_ID]:
        attr[const.RATE_AREA_ID] = utils.get_num_int(raw[const.CSV_RATE_AREA_ID])

    if raw[const.CSV_RATE_TOBACCO] == 'Tobacco User/Non-Tobacco User':
        attr[const.RATE_TOBACCO] = True
    else:
        attr[const.RATE_TOBACCO] = False

    if raw[const.CSV_RATE_AGE]:
        age_pair = utils.get_age_pair(raw[const.CSV_RATE_AGE])
        attr[const.RATE_AGE_FROM] = age_pair[0]
        attr[const.RATE_AGE_TO] = age_pair[1]

    if raw[const.CSV_RATE_INDI_RATE]:
        attr[const.RATE_INDI_RATE] = raw[const.CSV_RATE_INDI_RATE]

    if raw[const.CSV_RATE_INDI_TOBACCO_RATE]:
        attr[const.RATE_INDI_TOBACCO_RATE] = raw[const.CSV_RATE_INDI_TOBACCO_RATE]

    save_data(const.TABLE_RATE_INDIVIDUAL, attr)


def add_rate_family(raw):
    attr = dict()

    if raw[const.CSV_RATE_EFF_DATE]:
        attr[const.RATE_FAM_EFF_DATE] = raw[const.CSV_RATE_EFF_DATE]

    if raw[const.CSV_RATE_EXPI_DATE]:
        attr[const.RATE_FAM_EXPI_DATE] = raw[const.CSV_RATE_EXPI_DATE]

    if raw[const.CSV_RATE_STD_COMP_ID]:
        attr[const.RATE_FAM_STD_COMP_ID] = raw[const.CSV_RATE_STD_COMP_ID]

    if raw[const.CSV_RATE_AREA_ID]:
        attr[const.RATE_FAM_AREA_ID] = utils.get_num_int(raw[const.CSV_RATE_AREA_ID])

    if raw[const.CSV_RATE_INDI_RATE]:
        attr[const.RATE_FAM_INDI_RATE] = raw[const.CSV_RATE_INDI_RATE]

    if raw[const.CSV_RATE_COUPLE]:
        family_type = Enum.family_type[const.CSV_RATE_COUPLE]
        attr[const.RATE_FAM_TYPE] = family_type
        attr[const.RATE_FAM_RATE] = raw[const.CSV_RATE_COUPLE]
        save_data(const.TABLE_RATE_FAMILY, attr)

    if raw[const.CSV_RATE_PRIM_ONE_DEPENDENT]:
        family_type = Enum.family_type[const.CSV_RATE_PRIM_ONE_DEPENDENT]
        attr[const.RATE_FAM_TYPE] = family_type
        attr[const.RATE_FAM_RATE] = raw[const.CSV_RATE_PRIM_ONE_DEPENDENT]
        save_data(const.TABLE_RATE_FAMILY, attr)

    if raw[const.CSV_RATE_PRIM_TWO_DEPENDENT]:
        family_type = Enum.family_type[const.CSV_RATE_PRIM_TWO_DEPENDENT]
        attr[const.RATE_FAM_TYPE] = family_type
        attr[const.RATE_FAM_RATE] = raw[const.CSV_RATE_PRIM_TWO_DEPENDENT]
        save_data(const.TABLE_RATE_FAMILY, attr)

    if raw[const.CSV_RATE_PRIM_THREE_DEPENDENT]:
        family_type = Enum.family_type[const.CSV_RATE_PRIM_THREE_DEPENDENT]
        attr[const.RATE_FAM_TYPE] = family_type
        attr[const.RATE_FAM_RATE] = raw[const.CSV_RATE_PRIM_THREE_DEPENDENT]
        save_data(const.TABLE_RATE_FAMILY, attr)

    if raw[const.CSV_RATE_COUPLE_ONE_DEPENDENT]:
        family_type = Enum.family_type[const.CSV_RATE_COUPLE_ONE_DEPENDENT]
        attr[const.RATE_FAM_TYPE] = family_type
        attr[const.RATE_FAM_RATE] = raw[const.CSV_RATE_COUPLE_ONE_DEPENDENT]
        save_data(const.TABLE_RATE_FAMILY, attr)

    if raw[const.CSV_RATE_COUPLE_TWO_DEPENDENT]:
        family_type = Enum.family_type[const.CSV_RATE_COUPLE_TWO_DEPENDENT]
        attr[const.RATE_FAM_TYPE] = family_type
        attr[const.RATE_FAM_RATE] = raw[const.CSV_RATE_COUPLE_TWO_DEPENDENT]
        save_data(const.TABLE_RATE_FAMILY, attr)

    if raw[const.CSV_RATE_COUPLE_THREE_DEPENDENT]:
        family_type = Enum.family_type[const.CSV_RATE_COUPLE_THREE_DEPENDENT]
        attr[const.RATE_FAM_TYPE] = family_type
        attr[const.RATE_FAM_RATE] = raw[const.CSV_RATE_COUPLE_THREE_DEPENDENT]
        save_data(const.TABLE_RATE_FAMILY, attr)


def load_business_rules():
    """
    Load Business Rule CSV file into database
    :return:
    """
    print("------LOAD Business_Rules_PUF.csv------")

    with open(file_business_rules, mode='r', encoding='iso-8859-1') as fd:
        # Count total row number
        reader = csv.DictReader(fd)
        count = 0
        rows = sum(1 for _ in reader)
        fd.seek(0)

        # Loading data into database
        reader = csv.DictReader(fd)
        for raw_data in reader:
            add_business_rules(raw_data)

            add_business_rules_cohabit(raw_data)

            count += 1
            print('\rLoading Process:{:.2f}%'.format(count * 100 / rows), end='')

    conn.commit()
    print("\nDONE!")


def add_business_rules(raw):
    attr = dict()

    if raw[const.CSV_RULE_STD_COMP_ID]:
        attr[const.RULE_STD_COMP_ID] = raw[const.CSV_RULE_STD_COMP_ID]

    if raw[const.CSV_RULE_PROD_ID]:
        attr[const.RULE_PROD_ID] = raw[const.CSV_RULE_PROD_ID]

    if raw[const.CSV_RULE_RATE_RULE_TYPE] in Enum.rate_rule_type:
        attr[const.RULE_RATE_RULE_TYPE] = Enum.rate_rule_type[raw[const.CSV_RULE_RATE_RULE_TYPE]]

    if raw[const.CSV_RULE_SINGLE_PARENT_MAX_DEPENDENT]:
        attr[const.RULE_SINGLE_PARENT_MAX_DEPENDENT] = raw[const.CSV_RULE_SINGLE_PARENT_MAX_DEPENDENT]

    if raw[const.CSV_RULE_TWO_PARENTS_MAX_DEPENDENT]:
        attr[const.RULE_TWO_PARENTS_MAX_DEPENDENT] = raw[const.CSV_RULE_TWO_PARENTS_MAX_DEPENDENT]

    if raw[const.CSV_RULE_DEPENDENT_MAX_AGE] != 'Not Applicable':
        attr[const.RULE_DEPENDENT_MAX_AGE] = raw[const.CSV_RULE_DEPENDENT_MAX_AGE]

    if raw[const.CSV_RULE_CHILD_ONLY_MAX_CHILDREN]:
        attr[const.RULE_CHILD_ONLY_MAX_CHILDREN] = raw[const.CSV_RULE_CHILD_ONLY_MAX_CHILDREN]

    if raw[const.CSV_RULE_DOMESTIC_PARTNER_AS_SPOUSE] == 'Yes':
        attr[const.RULE_DOMESTIC_PARTNER_AS_SPOUSE] = True
    else:
        attr[const.RULE_DOMESTIC_PARTNER_AS_SPOUSE] = False

    if raw[const.CSV_RULE_SAME_SEX_PARTNER_AS_SPOUSE] == 'Yes':
        attr[const.RULE_SAME_SEX_PARTNER_AS_SPOUSE] = True
    else:
        attr[const.RULE_SAME_SEX_PARTNER_AS_SPOUSE] = False

    if raw[const.CSV_RULE_AGE_DETERMINE_RULE] in Enum.age_rule_type:
        attr[const.RULE_AGE_DETERMINE_RULE] = Enum.age_rule_type[raw[const.CSV_RULE_AGE_DETERMINE_RULE]]

    if raw[const.CSV_RULE_MIN_TOBACCO_FREE_MONTHS] != 'Not Applicable':
        attr[const.RULE_MIN_TOBACCO_FREE_MONTHS] = raw[const.CSV_RULE_MIN_TOBACCO_FREE_MONTHS]

    save_data(const.TABLE_BUSINESS_RULE, attr)


def add_business_rules_cohabit(raw):
    attr = dict()

    if raw[const.CSV_RULE_STD_COMP_ID]:
        attr[const.RULE_STD_COMP_ID] = raw[const.CSV_RULE_STD_COMP_ID]

    if raw[const.CSV_RULE_COHABIT_RULE]:
        cohabit_pairs = raw[const.CSV_RULE_COHABIT_RULE].split(';')
        for cohabit_pair in cohabit_pairs:
            pair = cohabit_pair.split(',')
            cohabit_obj = pair[0]
            cohabit_required = pair[1]
            attr[const.COHABIT_TYPE] = Enum.cohabit_type[cohabit_obj]
            if cohabit_required == 'Yes':
                attr[const.COHABIT_REQUIRED] = True
            else:
                attr[const.COHABIT_REQUIRED] = False
            save_data(const.TABLE_BUSINESS_RULE_COHABIT, attr)


if __name__ == '__main__':
    # Connect to postgres database
    conn = psycopg2.connect("host=%s dbname=%s user=%s" % (const.HOST_NAME,
                                                           const.DB_NAME,
                                                           const.DB_USER))
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Connect to mongoDB
    mongo = pymongo.MongoClient("mongodb://%s:%s/" % (const.MONGO_HOST, const.MONGO_PORT))
    dblist = mongo.list_database_names()
    if const.MONGO_DB_NAME in dblist:
        # Drop database if exist
        mongo.drop_database(const.MONGO_DB_NAME)
    mongodb = mongo[const.MONGO_DB_NAME]

    # Load Plan_Attributes_PUF.csv
    load_plans()

    # Load Benefits_Cost_Sharing_PUF.csv
    load_benefits()

    # Load Rate
    load_rate()

    # Load Business Rules
    load_business_rules()
