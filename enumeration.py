import psycopg2.extras
import constants


# Loading Enumeration Type Tables From Database
class Enum:
    # Table - <market_coverage_type>
    mark_cov_type = dict()

    # Table - <plan_type>
    plan_type = dict()

    # Table - <source_name_type>
    src_name_type = dict()

    # Table - <qhp_type>
    qhp_type = dict()

    # Table - <child_only_offering_type>
    child_only_type = dict()

    # Table - <medical_metal_level_type>
    m_metal_type = dict()

    # Table - <dental_metal_level_type>
    d_metal_type = dict()

    # Table - <tobacco_type>
    tobacco_type = dict()

    # TODO age type

    # Table - <family_type>
    family_type = dict()

    # Table - <copay_type>
    copay_type = dict()

    # Table - <coin_type>
    coins_type = dict()

    # Table - <limit_unit_type>
    limit_unit_type = dict()

    # Table - <design_type>
    design_type = dict()

    @classmethod
    def init(cls, hostname, dbname, user):
        conn = psycopg2.connect("host=%s dbname=%s user=%s" % (hostname, dbname, user))
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Read Enumeration Table into memory
        cls.load_type_table(cursor, cls.src_name_type, constants.TABLE_SRC_NAME_TYPE)
        cls.load_type_table(cursor, cls.plan_type, constants.TABLE_PLAN_TYPE)
        cls.load_type_table(cursor, cls.mark_cov_type, constants.TABLE_MARK_COV_TYPE)
        cls.load_type_table(cursor, cls.qhp_type, constants.QHP_TYPE)
        cls.load_type_table(cursor, cls.child_only_type, constants.TABLE_CHILD_ONLY_TYPE)
        cls.load_type_table(cursor, cls.m_metal_type, constants.TABLE_M_METAL_TYPE)
        cls.load_type_table(cursor, cls.d_metal_type, constants.TABLE_D_METAL_TYPE)
        cls.load_type_table(cursor, cls.tobacco_type, constants.TABLE_TOBACCO_TYPE)
        cls.load_type_table(cursor, cls.family_type, constants.TABLE_FAMILY_TYPE)
        cls.load_type_table(cursor, cls.copay_type, constants.TABLE_COPAY_TYPE)
        cls.load_type_table(cursor, cls.coins_type, constants.TABLE_COINS_TYPE)
        cls.load_type_table(cursor, cls.limit_unit_type, constants.TABLE_LIMIT_UNIT_TYPE)
        cls.load_type_table(cursor, cls.design_type, constants.TABLE_DESIGN_TYPE)

        conn.close()

    @staticmethod
    def load_type_table(cursor, obj, table_name):
        cursor.execute("SELECT * FROM %s" % (table_name,))
        records = cursor.fetchall()
        for record in records:
            obj[record['type_name']] = record['id']


# Init Enumeration Type
Enum.init(constants.HOST_NAME, constants.DB_NAME, constants.DB_USER)
