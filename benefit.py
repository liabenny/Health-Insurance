# ========== For database.py

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
    print(query)
    return cls.__query__(query, (benefit_type,))



#===============for application.py
def handle_search_benefit():
    print("\n==============Plan Benefit==============")
    # Print given benefits list
    benefit_list = Query.get_benefit_list()
    flatten = [item for sublist in benefit_list for item in sublist]
    utils.print_series(flatten, "Benefit Item")
    instruction = "\nWhich benefit of do you want to query?:"
    benefit_type = wait_input(instruction, flatten)
    if benefit_type == -1:
        return
    print("!!!!", benefit_type)
    # Query for the result
    results = Query.get_benefit(benefit_type=benefit_type)
    utils.print_data_frame(results, ["Plan ID", "Benefit", "Quantity Limit", "Unit Limit"])
    input("\nPress any key to continue.")



