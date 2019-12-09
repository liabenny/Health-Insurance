# database related code
import tabulate as tabulate

"""
input
["Insurance Type", "Subscriber", "Cover Range", "Metal Level", "Wellness Program",
"Exchange", "Out of Country", "Payment Type", "Age", "State", "Family Type"]

output
["Plan Id", "State", "Plan Name", "family/individual_rate", "Plan Benefit", "coin/copay_inn_tier1", 
"coin/copay_inn_tier1_type", "coin/copay_inn_tier2", "coin/copay_inn_tier2_type", "coin/copay_oon", 
"coin/copay_oon_type", "benefit_limit_qty", "limit_unit"]
"""


class Query:
    """
    @:arg: request
    @:type: dictionary
    """

    def __init__(self, request):
        self.request = request
        self._insurance_type = self.request["Insurance Type"]
        self._subscriber = self.request["Subscriber"]
        self._payment = self.request["Payment Type"]

    def run_query(self):
        self.build_str()
        pass

    def build_str(self):
        return self.get_select() + self.get_from() + self.get_where()

    # TODO
    def get_select(self):
        res = "SELECT plans.plan_id, plans.state, plans.plan_marketing_name, %s, plan_benefit.benefit_name, %s, %s" \
              % (self.select_rate(), self.select_payment(), self.select_benefit_limit())
        print(res)
        return res

    def select_rate(self):
        if self._subscriber == "Individual":
            return "rate_individual.individual_rate"
        else:
            return "rate_family.family_rate "

    # TODO: Differentiate the type name for each tier
    def select_payment(self):
        if self._payment == "Copay":
            return "plan_benefit.copay_inn_tier1, plan_benefit.copay_inn_tier2, plan_benefit.copay_oon"
        else:
            return "plan_benefit.coin_inn_tier1, plan_benefit.coin_inn_tier2, plan_benefit.coin_oon"

    def select_benefit_limit(self):
        return "plan_benefit_limitation.limit_qty, plan_benefit_limitation.limit_unit"

    def get_from(self):
        res = "FROM %s%s%s%s" % (
            self.find_table_general(), self.find_table_insurance_type(),
            self.find_table_subscriber(),
            self.find_table_payment())
        print(res)
        return res

    def get_where(self):
        res = "WHERE plans.plan_id = %s AND " \
              "plans.market_coverage = market_coverage_type.id AND market_coverage_type.type_name = %s AND " \
              "plans.child_only_offering = child_only_offering_type.id AND child_only_offering_type.type_name = %s AND " \
              "%s AND " \
              "%s AND " \
              "%s AND " \
              "%s AND " \
              "plan_benefit.plan_id = plan_benefit_limitation.plan_id AND " \
              "plan_benefit.benefit_name = plan_benefit_limitation.benefit_name AND " \
              "%s AND " \
              "%s AND " \
              "plans.state = '%s' AND " \
              "%s" \
              % (self.condition_insurance_type(), self.condition_subscriber(), self.condition_cover_range(),
                 self.condition_metal_level(), self.condition_wellness(), self.condition_qhp(),
                 self.condition_out_of_country(), self.condition_payment(), self.condition_age(),
                 self.condition_state(),
                 self.condition_family_type())
        print(res)
        return res

    def condition_insurance_type(self):
        if self._insurance_type == 'Medical':
            return "medical_plans.plan_id"
        else:
            return "dental_plans.plan_id"

    def condition_subscriber(self):
        if self._subscriber == "Individual":
            return "'Individual'"
        else:
            return "'SHOP (Small Group)'"

    def condition_cover_range(self):
        if self.request["Cover Range"] == "Adult and Child":
            return "'Allows Adult and Child-Only'"
        elif self.request["Cover Range"] == "Child Only":
            return "'Allows Child-Only'"
        else:
            return "'Allows Adult-Only'"

    def condition_metal_level(self):
        if self._insurance_type == "Medical":
            return "medical_plans.metal_level = medical_metal_level_type.id AND medical_metal_level_type.type_name = '%s'" \
                   % self.request["Metal Level"]
        else:
            return "dental_plans.metal_level = dental_metal_level_type.id AND dental_metal_level_type.type_name = '%s'" \
                   % self.request["Metal Level"]

    def condition_wellness(self):
        if self._insurance_type == "Medical":
            if self.request["Wellness Program"] == "YES":
                return "medical_plans.is_wellness_program_offered = TRUE"
            else:
                return "medical_plans.is_wellness_program_offered = FALSE"
        return ""  # Dental plan no this attribute

    def condition_qhp(self):
        return "plans.qhp_type = qhp_type.id AND qhp_type.type_name = '%s'" % self.request["Exchange"]

    def condition_out_of_country(self):
        if self.request["Out of Country"] == "YES":
            return "plans.out_of_country_coverage = TRUE"
        else:
            return "plans.out_of_country_coverage = FALSE"

    # TODO: TO BE DETERMINED How to add more
    def condition_payment(self):
        if self._payment == 'Copay':
            return "plan_benefit.coins_inn_tier1_type = coins_type.id AND " \
                   "plan_benefit.coins_inn_tier2_type = coins_type.id AND plan.benefit.coins_oon_type = coins_type.id"
        else:  # Coin
            return "plan_benefit.copay_inn_tier1_type = copay_type.id AND " \
                   "plan_benefit.copay_inn_tier2_type = copay_type.id AND plan_benefit.copay_oon_type = copay_type.id"

    def condition_age(self):
        return "rate_individual.age = %s" % self.request["Age"]

    def condition_state(self):
        return self.request["State"]

    def condition_family_type(self):
        if self._subscriber == "Family":
            return "rate_family.family_type = family_type.id AND family_type.type_name = '%s'" \
                   % self.request["Family Type"]
        return ""  # Individual no this attribute

    # The database tables can be apply for all query
    def find_table_general(self):
        return "plans, plan_benefit, plan_benefit_limitation, qhp_type"

    def find_table_insurance_type(self):
        if self._insurance_type == 'Medical':
            return ', medical_plans, medical_metal_level_type'
        else:  # Dental
            return ', dental_plans, dental_metal_level_type'

    def find_table_subscriber(self):
        if self._subscriber == 'Individual':
            return ", rate_individual, age_type"
        else:  # Family
            return ", rate_family, family_type"

    # TODO: TO BE DETERMINED
    def find_table_payment(self):
        if self._payment == 'Copay':
            return ", copay_type"
        else:  # coin
            return ", coin_type"
