# database related code
import tabulate as tabulate

"""
["Insurance Type", "Subscriber", "Cover Range", "Metal Level", "Wellness Program",
"Exchange", "Out of Country", "Payment Type", "Age", "State", "Family Type"]
"""


class Query:
    """
    @:arg: request
    @:type: dictionary
    """

    def __init__(self, request):
        self.request = request

    def run_query(self):
        print("Begin to query")
        self.build_str()
        pass

    def build_str(self):
        return self.get_select() + self.get_from() + self.get_where()


    def get_select(self):
        res = "SELECT"
        print(res)
        return res

    def get_from(self):
        res = "FROM %s%s%s%s" % (
            self.find_table_general(), self.find_table_insurance_type(self.request["Insurance Type"]),
            self.find_table_subscriber(self.request["Subscriber"]),
            self.find_table_payment(self.request["Payment Type"]))
        print(res)
        return res

    def get_where(self):
        res = "WHERE"
        print(res)
        return res

    # The database tables can be apply for all query
    def find_table_general(self):
        return "plans, plan_benefit, plan_benefit_limitation, qhp_type"

    def find_table_insurance_type(self, val):
        if val == 'Medical':
            return ', medical_plans, medical_metal_level_type'
        else:  # Dental
            return ', dental_plans, dental_metal_level_type'

    def find_table_subscriber(self, val):
        if val == 'Individual':
            return ", rate_individual, age_type"
        else:  # Family
            return ", rate_family, family_type"

    # TODO: TO BE DETERMINED
    def find_table_payment(self, val):
        if val == 'Copay':
            return ", copay_type"
        else:  # coin
            return ", coin_type"
