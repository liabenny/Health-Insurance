# ======= For application.py============
def handle_search_eye_plan():
    print("\n==============Eye Insurance Plan==============")

    # 1. Decides eye insurance plan type
    instruction = "\nWhich type of insurance do you want to query? (Eye Exam/ Eye Glasses):"
    values = ["Eye Exam", "Eye Glasses"]
    insurance_type = wait_input(instruction, values)
    if insurance_type == -1:
        return

    # 2. Decides groups
    instruction = "\nWhat is the group of searching? (Adult/ Child):"
    values = ["Adult", "Child"]
    group_type = wait_input(instruction, values)
    if group_type == -1:
        return

    # 3. Decides age
    instruction = "\nWhat is the age of searching? (1-99):"
    values = list(str(i) for i in range(1, 99))
    age = wait_input(instruction, values)
    if age == -1:
        return

    # 3. Decide Metal Level
    instruction = "\nWhich metal level are you looking for:"
    utils.print_series(Enum.m_metal_type.keys(), "Metal Level")
    values = Enum.m_metal_type.keys()

    metal_level = wait_input(instruction, values)
    if metal_level == -1:
        return
    metal_level_id = Enum.m_metal_type[metal_level]

    # Query for the result
    results = Query.get_eye_insurance(insurance_type=insurance_type, group_type=group_type, age=age,
                                      metal_level_id=metal_level_id)
    utils.print_data_frame(results,
                           ["Plan ID", "Effective Date", "Expiration Date", "Benefit Name", "Estimated Average",
                            "Quantity Limit", "Unit Limit"])

    input("\nPress any key to continue.")

    # =========== For database.py =============
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
        print(query)
        return cls.__query__(query, (metal_level_id, age, key1, key2))
