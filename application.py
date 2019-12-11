import constants as const
import utils
import collections
from enumeration import Enum
from tabulate import tabulate
from database import Query


def handle_search_plan():
    print("\n==============Insurance Plan==============")
    constrains = collections.OrderedDict()

    # 1. Decide plan objectives
    keys = list(Enum.mark_cov_type.keys())
    utils.print_series(keys, "Plan Coverage", showindex=True)
    instruction = "\nWhich plan coverage are you looking for?: "
    values = list(str(i) for i in range(len(keys)))
    plan_obj = wait_input(instruction, values)
    if plan_obj == -1:
        return
    constrains[const.MARK_COVERAGE] = (const.EQUAL, Enum.mark_cov_type[keys[int(plan_obj)]])

    # 2. Decide plan type (medical/dental)
    instruction = "\nWhich type of insurance do you want to query? (medical/dental): "
    values = ["medical", "dental"]
    insurance_type = wait_input(instruction, values)
    if insurance_type == -1:
        return

    # 3. Handle different plan type
    search_plan_sub_menu(constrains, insurance_type)


def search_plan_sub_menu(constrains, insurance_type):
    plans = list()
    options = list()
    options.append((1, "Select Plans"))
    options.append((2, "Add Filter"))
    options.append((3, "Remove Filter"))
    options.append((4, "Back to Menu"))
    attributes = [const.PLAN_ID, const.PLAN_VAR_NAME]
    detailed_constrains = collections.OrderedDict()

    while True:
        # Query the plans from database
        plans = Query.get_plans(attributes=attributes,
                                constrains=constrains,
                                detail_constrains=detailed_constrains,
                                insurance_type=insurance_type)
        # Update the record number
        options[0] = (1, "Show plans ({})".format(len(plans)))

        print("\n==========Insurance Plan - {} - {}=========="
              .format(Enum.mark_cov_type_rev[constrains[const.MARK_COVERAGE][1]], insurance_type.upper()))
        utils.print_data_frame(options, ["Index", "Option"])
        index = input("\nPlease select an option:")
        if index.strip() == "1":
            # Handle "Show Plans"
            plan_id = search_plan_select_plans(plans, attributes)
            if plan_id:
                search_plan_detail_information(plan_id)

        elif index.strip() == "2":
            # Handle "Add Filter"
            if insurance_type == "medical":
                search_plan_add_filter_medical(constrains, detailed_constrains)
            else:
                search_plan_add_filter_dental(constrains, detailed_constrains)

        elif index.strip() == "3":
            # Handle "Remove Filter"
            search_plan_remove_filter(constrains, detailed_constrains, insurance_type)

        elif index.strip() == "4":
            # Handle "Quit"
            print("Bye.")
            return

        else:
            print("Invalid Index.")


def search_plan_select_plans(data, headers):
    print("\n==========Select Plan==========")
    pageindex = 0
    pagesize = 10
    total_rows = len(data)

    # Print plans based on pages
    while True:
        # Print plan for current page
        print()
        utils.print_data_frame(data_frame=data,
                               headers=headers,
                               pageindex=pageindex,
                               pagesize=pagesize,
                               showindex=True)

        if (pageindex + 1) * pagesize < total_rows:
            # Continue to display
            instruction = "\nType 'it' for more plans, or type 'quit' to return.\n" \
                          "You can select a plan for detail information: "
            values = list(str(i) for i in range(pagesize))
            values.append("it")

        else:
            # Reach end of list
            instruction = "\nReach end of the list, type 'quit' to return.\n" \
                          "You can select a plan for detail information: "
            values = list(str(i) for i in range(pagesize))

        cmd = wait_input(instruction, values)
        if cmd == -1:
            return
        elif cmd == 'it':
            # Go to next page
            pageindex += 1
        else:
            # Return the selected plan id
            cur_index = int(cmd)
            plan_index = pageindex * pagesize + cur_index
            plan_id = data[plan_index][0]
            print(plan_id)
            return plan_id


def search_plan_detail_information(plan_id):
    options = list()
    options.append((1, "Disease Programs"))
    options.append((2, "Plan Benefits"))
    while True:
        print("\n==========Plan Information==========")
        utils.print_data_frame(options, ["Index", "Option"])
        instruction = "\nPlease select an option:"
        values = list(str(i) for i in range(1, 1 + len(options)))
        index = wait_input(instruction, values)
        if index == -1:
            return

        if index == '1':
            pass
        elif index == '2':
            attributes = [const.PLAN_ID, const.BENEFIT_NAME]
            attr_output = ["Plan ID", "Benefit Name"]
            constrains = dict()
            constrains[const.PLAN_ID] = (const.EQUAL, plan_id)
            info = Query.plain_query(attributes, const.TABLE_BENEFIT, constrains, order_by=const.BENEFIT_NAME)
            utils.print_data_frame(info, attr_output)

        elif index == 'quit':
            return
        else:
            print("Invalid Index.")


def search_plan_add_filter_medical(constrains, detail_constrains):
    filters = list()
    filters.append((1, "State"))
    filters.append((2, "Plan Type"))
    filters.append((3, "QHP Type"))
    filters.append((4, "Child Option"))
    filters.append((5, "Metal level"))
    filters.append((6, "Notice for pregnancy Required"))
    filters.append((7, "Wellness Program Offered"))
    filters.append((8, "Quit"))

    utils.print_data_frame(filters, ["Index", "Filter"])
    instruction = "\nPlease select an filter:"
    values = list(str(i) for i in range(1, 1 + len(filters)))
    index = wait_input(instruction, values)
    if index == -1:
        return
    if index.strip() == "1":
        state_list = Query.get_plan_state()
        utils.print_data_frame(state_list, ["State"])
        instruction = "\nPlease select a state: "
        values = list(value[0] for value in state_list)
        state = wait_input(instruction, values)
        if state == -1:
            return
        constrains[const.PLAN_STATE] = (const.EQUAL, state)

    elif index.strip() == "2":
        keys = list(Enum.plan_type.keys())
        utils.print_series(keys, "Plan Type", showindex=True)
        instruction = "\nWhich type of plan do you want?: "
        values = list(str(i) for i in range(len(keys)))
        index = wait_input(instruction, values)
        if index == -1:
            return
        constrains[const.PLAN_TYPE] = (const.EQUAL, Enum.plan_type[keys[int(index)]])

    elif index.strip() == "3":
        keys = list(Enum.qhp_type.keys())
        utils.print_series(keys, "QHP Type", showindex=True)
        instruction = "\nWhich QHP type do you want?: "
        values = list(str(i) for i in range(len(keys)))
        index = wait_input(instruction, values)
        if index == -1:
            return
        constrains[const.QHP_TYPE] = (const.EQUAL, Enum.qhp_type[keys[int(index)]])

    elif index.strip() == "4":
        keys = list(Enum.child_only_type.keys())
        utils.print_series(keys, "Child Option", showindex=True)
        instruction = "\nWhich child option do you want?: "
        values = list(str(i) for i in range(len(keys)))
        index = wait_input(instruction, values)
        if index == -1:
            return
        constrains[const.CHILD_ONLY] = (const.EQUAL, Enum.child_only_type[keys[int(index)]])

    elif index.strip() == "5":
        keys = list(Enum.m_metal_type.keys())
        utils.print_series(keys, "Metal Level", showindex=True)
        instruction = "\nWhich metal level do you want?: "
        values = list(str(i) for i in range(len(keys)))
        index = wait_input(instruction, values)
        if index == -1:
            return
        detail_constrains[const.M_METAL_LEVEL] = (const.EQUAL, Enum.m_metal_type[keys[int(index)]])

    elif index.strip() == "6":
        instruction = "\nWhether notice required for pregnancy?(yes/no): "
        values = ["yes", "no"]
        value = wait_input(instruction, values)
        if value == -1:
            return
        detail_constrains[const.PREG_NOTICE] = (const.EQUAL, True) if value == "yes" else (const.EQUAL, False)

    elif index.strip() == "7":
        instruction = "\nDo you want wellness program included?(yes/no): "
        values = ["yes", "no"]
        value = wait_input(instruction, values)
        if value == -1:
            return
        detail_constrains[const.WELLNESS_OFFER] = (const.EQUAL, True) if value == "yes" else (const.EQUAL, False)

    elif index.strip() == "8":
        print("Quit.")
        return
    else:
        print("Invalid Index.")


def search_plan_add_filter_dental(constrains, detail_constrains):
    filters = list()
    filters.append((1, "State"))
    filters.append((2, "Plan Type"))
    filters.append((3, "QHP Type"))
    filters.append((4, "Child Option"))
    filters.append((5, "Metal level"))
    filters.append((6, "Quit"))

    utils.print_data_frame(filters, ["Index", "Filter"])
    instruction = "\nPlease select an filter:"
    values = list(str(i) for i in range(1, 1 + len(filters)))
    index = wait_input(instruction, values)
    if index == -1:
        return

    if index.strip() == "1":
        state_list = Query.get_plan_state()
        utils.print_data_frame(state_list, ["State"])
        instruction = "\nPlease select a state: "
        values = list(value[0] for value in state_list)
        state = wait_input(instruction, values)
        if state == -1:
            return
        constrains[const.PLAN_STATE] = (const.EQUAL, state)

    elif index.strip() == "2":
        keys = list(Enum.plan_type.keys())
        utils.print_series(keys, "Plan Type", showindex=True)
        instruction = "\nWhich type of plan do you want?: "
        values = list(str(i) for i in range(len(keys)))
        index = wait_input(instruction, values)
        if index == -1:
            return
        constrains[const.PLAN_TYPE] = (const.EQUAL, Enum.plan_type[keys[int(index)]])

    elif index.strip() == "3":
        keys = list(Enum.qhp_type.keys())
        utils.print_series(keys, "QHP Type", showindex=True)
        instruction = "\nWhich QHP type do you want?: "
        values = list(str(i) for i in range(len(keys)))
        index = wait_input(instruction, values)
        if index == -1:
            return
        constrains[const.QHP_TYPE] = (const.EQUAL, Enum.qhp_type[keys[int(index)]])

    elif index.strip() == "4":
        keys = list(Enum.child_only_type.keys())
        utils.print_series(keys, "Child Option", showindex=True)
        instruction = "\nWhich child option do you want?: "
        values = list(str(i) for i in range(len(keys)))
        index = wait_input(instruction, values)
        if index == -1:
            return
        constrains[const.CHILD_ONLY] = (const.EQUAL, Enum.child_only_type[keys[int(index)]])

    elif index.strip() == "5":
        keys = list(Enum.d_metal_type.keys())
        utils.print_series(keys, "Metal Level", showindex=True)
        instruction = "\nWhich metal level do you want?: "
        values = list(str(i) for i in range(len(keys)))
        index = wait_input(instruction, values)
        if index == -1:
            return
        detail_constrains[const.M_METAL_LEVEL] = (const.EQUAL, Enum.d_metal_type[keys[int(index)]])

    elif index.strip() == "6":
        print("Quit.")
        return
    else:
        print("Invalid Index.")


def search_plan_remove_filter(constrains, detail_constrains, insurance_type):
    # List current filter conditions
    cur_filters = list()
    if const.PLAN_TYPE in constrains:
        value = int(constrains[const.PLAN_TYPE][1])
        cur_filters.append(("Plan Type", Enum.plan_type_rev[value]))

    if const.QHP_TYPE in constrains:
        value = int(constrains[const.QHP_TYPE][1])
        cur_filters.append(("QHP Type", Enum.qhp_type_rev[value]))

    if const.CHILD_ONLY in constrains:
        value = int(constrains[const.CHILD_ONLY][1])
        cur_filters.append(("Child Option", Enum.child_only_type_rev[value]))

    if const.PLAN_STATE in constrains:
        value = constrains[const.PLAN_STATE][1]
        cur_filters.append(("State", value))

    if insurance_type == "medical":
        if const.M_METAL_LEVEL in detail_constrains:
            value = int(detail_constrains[const.M_METAL_LEVEL][1])
            cur_filters.append(("Metal Level", Enum.m_metal_type_rev[value]))

        if const.WELLNESS_OFFER in detail_constrains:
            value = detail_constrains[const.WELLNESS_OFFER][1]
            value_desc = "Yes" if value else "No"
            cur_filters.append(("Wellness Program", value_desc))

        if const.PREG_NOTICE in detail_constrains:
            value = detail_constrains[const.PREG_NOTICE][1]
            value_desc = "Yes" if value else "No"
            cur_filters.append(("Pregnancy Notice", value_desc))
    else:
        if const.D_METAL_LEVEL in detail_constrains:
            value = int(detail_constrains[const.D_METAL_LEVEL][1])
            cur_filters.append(("Metal Level", Enum.d_metal_type_rev[value]))

    # If do not have any filter, then return
    if not cur_filters:
        print("\nNo filter.")
        return
    cur_filters.append(("Quit", "-"))
    utils.print_data_frame(cur_filters, ["Filter", "Constrain"], showindex=True)

    # Decide the filter that want to be removed
    instruction = "\nPlease select filter you want to remove: "
    values = list(str(i) for i in range(len(cur_filters)))
    index = wait_input(instruction, values)
    if index == -1 or index == len(cur_filters) - 1:
        return

    # Remove the corresponding filter in the constrains
    filter_name = cur_filters[int(index)][0]
    if filter_name == "Plan Type":
        constrains.pop(const.PLAN_TYPE)

    elif filter_name == "QHP Type":
        constrains.pop(const.QHP_TYPE)

    elif filter_name == "Child Option":
        constrains.pop(const.CHILD_ONLY)

    elif filter_name == "State":
        constrains.pop(const.PLAN_STATE)

    elif filter_name == "Metal Level":
        if insurance_type == "medical":
            detail_constrains.pop(const.M_METAL_LEVEL)
        else:
            detail_constrains.pop(const.D_METAL_LEVEL)

    elif filter_name == "Wellness Program":
        detail_constrains.pop(const.WELLNESS_OFFER)

    elif filter_name == "Pregnancy Notice":
        detail_constrains.pop(const.PREG_NOTICE)


def search_plan_dental(constrains):
    pass


def handle_find_avg_rate():
    print("\n==============Average Individual Rate==============")

    # 1. Decide insurance type
    instruction = "\nWhich type of insurance do you want to query? (medical/dental): "
    values = ["medical", "dental"]
    insurance_type = wait_input(instruction, values)

    if insurance_type == -1:
        return

    # 2. Decide Metal Level
    instruction = "\nWhich metal level are you looking for:"
    if insurance_type == "medical":
        utils.print_series(Enum.m_metal_type.keys(), "Metal Level")
        values = Enum.m_metal_type.keys()
    else:
        utils.print_series(Enum.d_metal_type.keys(), "Metal Level")
        values = Enum.d_metal_type.keys()

    metal_level = wait_input(instruction, values)
    if metal_level == -1:
        return
    metal_level_id = Enum.m_metal_type[metal_level] if insurance_type == "medical" \
        else Enum.d_metal_type[metal_level]

    # 3. Decide age for query
    instruction = "\nWhat is the age of searching? (1-99):"
    values = list(str(i) for i in range(1, 100))
    age = wait_input(instruction, values)

    if age == -1:
        return

    # 4. Get time intervals
    time_intervals = Query.get_time_intervals(metal_level_id=metal_level_id, age=age)
    utils.print_data_frame(time_intervals, ["Effective Date", "Expiration Date"], showindex=True)
    instruction = "\nPlease choose a time intervals:"
    values = list(str(i) for i in range(len(time_intervals)))
    index = wait_input(instruction, values)
    if index == -1:
        return
    index = int(index)
    effective_date = time_intervals[index][0]
    expiration_date = time_intervals[index][1]

    # 5. Query for results
    results = Query.get_avg_rate(metal_level_id=metal_level_id,
                                 age=age,
                                 effective_date=effective_date,
                                 expiration_date=expiration_date,
                                 insurance_type=insurance_type)
    utils.print_data_frame(results, ["State", "Individual Rate (average)"])

    input("\nPress any key to continue.")


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
    utils.print_series(Enum.m_metal_type.keys(), "Metal Level", showindex=True)
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
                            "Quantity Limit", "Unit Limit"], showindex=True)

    input("\nPress any key to continue.")


def handle_search_benefit():
    # Print given benefits list
    benefit_list = Query.get_benefit_list()
    flatten = [item for sublist in benefit_list for item in sublist]
    print("\n==============Plan Benefit==============")
    utils.print_series(flatten, "Benefit Item", showindex=True)
    instruction = "\nWhich benefit of do you want to query?:"
    benefit_type = wait_input(instruction, flatten)
    if benefit_type == -1:
        return
    # Query for the result
    results = Query.get_benefit(benefit_type=benefit_type)
    utils.print_data_frame(results, ["Plan ID", "Benefit", "Quantity Limit", "Unit Limit"], showindex=True)
    input("\nPress any key to continue.")


def wait_input(instruction, values):
    tmp = input(instruction)
    # If user input 'quit', then return to menu
    if tmp.lower() == 'quit':
        print("Back to menu.")
        return -1

    # Keep waiting correct input
    while tmp not in values:
        print("Invalid value, please try again.")
        tmp = input(instruction)
        if tmp.lower() == 'quit':
            print("Back to menu.")
            return -1
    return tmp


def init(functions):
    functions.append([1, "Search Insurance Plan"])
    functions.append([2, "State Average Individual Rate"])
    functions.append([3, "Search Eye Plan"])
    functions.append([4, "Search Plan Benefits"])


def main():
    print("Welcome to Healthcare Insurance Database System!")
    print("Data Source: The Centers for Medicare & Medicaid Services(CMS)\n")
    while True:
        print("\n==============Menu==============")
        functions = list()
        init(functions)
        print(tabulate(functions, ["Option", "Description"], tablefmt="fancy_grid"))
        index = input("\nPlease select an option:")
        if index.strip() == "1":
            handle_search_plan()
        elif index.strip() == "2":
            handle_find_avg_rate()
        elif index.strip() == "3":
            handle_search_eye_plan()
        elif index.strip() == "4":
            handle_search_benefit()
        elif index == "quit":
            print("Bye.")
            exit(0)
        else:
            print("Invalid Index.")


if __name__ == '__main__':
    main()
