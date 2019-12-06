import sys


# Define Constant Type

class Const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise self.ConstError("Can't change const value!")
        if not key.isupper():
            raise self.ConstCaseError('const "%s" is not all letters are capitalized' % key)
        self.__dict__[key] = value


sys.modules[__name__] = Const()

# Constants - Configuration
Const.HOST_NAME = "172.17.0.2"
Const.DB_NAME = "insurance"
Const.DB_USER = "manager"

# Constants - TABLE NAME - Enumeration
Const.TABLE_SRC_NAME_TYPE = "source_name_type"
Const.TABLE_MARK_COV_TYPE = "market_coverage_type"
Const.TABLE_PLAN_TYPE = "plan_type"
Const.TABLE_QHP_TYPE = "qhp_type"
Const.TABLE_CHILD_ONLY_TYPE = "child_only_offering_type"
Const.TABLE_M_METAL_TYPE = "medical_metal_level_type"
Const.TABLE_D_METAL_TYPE = "dental_metal_level_type"
Const.TABLE_TOBACCO_TYPE = "tobacco_type"
Const.TABLE_AGE_TYPE = "age_type"
Const.TABLE_FAMILY_TYPE = "family_type"
Const.TABLE_COPAY_TYPE = "copay_type"
Const.TABLE_COINS_TYPE = "coin_type"
Const.TABLE_LIMIT_UNIT_TYPE = "limit_unit_type"
Const.TABLE_DESIGN_TYPE = "design_type"

# Constants - TABLE ATTRIBUTES - Plans
Const.PLAN_ID = "plan_id"
Const.PLAN_VAR_NAME = "plan_variant_name"
Const.STD_COMP_ID = "std_component_id"
Const.PLAN_MARK_NAME = "plan_marketing_name"
Const.PLAN_YEAR = "year"
Const.PLAN_STATE = "state"
Const.SOURCE_NAME = "source_name"
Const.IMPORT_DATE = "import_date"
Const.HIOS_PROD_ID = "hios_product_id"
Const.HPID = "hpid"
Const.NETWORK_ID = "network_id"
Const.SERV_AREA_ID = "service_area_id"
Const.FORMULARY_ID = "formulary_id"
Const.IS_NEW_PLAN = "is_new_plan"
Const.MARK_COVERAGE = "market_coverage"
Const.PLAN_TYPE = "plan_type"
Const.QHP_TYPE = "qhp_type"
Const.DESIGN_TYPE = "design_type"
Const.CHILD_ONLY = "child_only_offering"
Const.COMPOSITE_RATE = "composite_rate_offered"
Const.OUT_COUNTRY_COV = "out_of_country_coverage"
Const.OUT_COUNTRY_COV_DESC = "out_of_country_coverage_desc"
Const.OUT_SERV_AREA_COV = "out_of_service_area_coverage"
Const.OUT_SERV_AREA_COV_DESC = "out_of_service_area_coverage_desc"
Const.PLAN_EXCLUSIONS = "plan_level_exclusions"
Const.EST_ADV_PAYMENT_INDIAN = "est_advanced_payment_for_indian_plan"
Const.CSR_VAR_TYPE = "csr_variant_type"
Const.MULTI_NETWORK = "multiple_in_network_tiers"
Const.FIRST_TIER_UTIL = "first_tier_utilization"
Const.SECOND_TIER_UTIL = "second_tier_utilization"
Const.EFFECTIVE_DATE = "effective_date"
Const.EXPIRATION_DATE = "expiration_date"

# Constants - DATA SET - Plans
Const.CSV_PLAN_ID = "PlanId"
Const.CSV_PLAN_VAR_NAME = "PlanVariantMarketingName"
Const.CSV_PLAN_MARK_NAME = "PlanMarketingName"
Const.CSV_STD_COMP_ID = "StandardComponentId"
Const.CSV_PLAN_YEAR = "BusinessYear"
Const.CSV_PLAN_STATE = "StateCode"
Const.CSV_SOURCE_NAME = "SourceName"
Const.CSV_IMPORT_DATE = "ImportDate"
Const.CSV_HIOS_PROD_ID = "HIOSProductId"
Const.CSV_HPID = "HPID"
Const.CSV_NETWORK_ID = "NetworkId"
Const.CSV_SERV_AREA_ID = "ServiceAreaId"
Const.CSV_FORMULARY_ID = "FormularyId"
Const.CSV_IS_NEW_PLAN = "IsNewPlan"
Const.CSV_MARK_COVERAGE = "MarketCoverage"
Const.CSV_PLAN_TYPE = "PlanType"
Const.CSV_QHP_TYPE = "QHPNonQHPTypeId"
Const.CSV_DESIGN_TYPE = "DesignType"
Const.CSV_CHILD_ONLY = "ChildOnlyOffering"
Const.CSV_COMPOSITE_RATE = "CompositeRatingOffered"
Const.CSV_OUT_COUNTRY_COV = "OutOfCountryCoverage"
Const.CSV_OUT_COUNTRY_COV_DESC = "OutOfCountryCoverageDescription"
Const.CSV_OUT_SERV_AREA_COV = "OutOfServiceAreaCoverage"
Const.CSV_OUT_SERV_AREA_COV_DESC = "OutOfServiceAreaCoverageDescription"
Const.CSV_PLAN_EXCLUSIONS = "PlanLevelExclusions"
Const.CSV_EST_ADV_PAYMENT_INDIAN = "IndianPlanVariationEstimatedAdvancedPaymentAmountPerEnrollee"
Const.CSV_CSR_VAR_TYPE = "CSRVariationType"
Const.CSV_MULTI_NETWORK = "MultipleInNetworkTiers"
Const.CSV_FIRST_TIER_UTIL = "FirstTierUtilization"
Const.CSV_SECOND_TIER_UTIL = "SecondTierUtilization"
Const.CSV_EFFECTIVE_DATE = "PlanEffectiveDate"
Const.CSV_EXPIRATION_DATE = "PlanExpirationDate"
