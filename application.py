import constants as const
import utils
from enumeration import Enum
from tabulate import tabulate
from database import Query


def handle_search_medical_plan():
    pass


def handle_search_dental_plan():
    pass


def handle_find_avg_rate():
    print("\n==============Average Individual Rate==============")

    # 1. Decide insurance type
    instruction = "\nWhich type of insurance do you want to query? (medical/dental):"
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
    values = list(str(i) for i in range(1, 99))
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
    functions.append([1, "Search a Medical Plan"])
    functions.append([2, "Search a Dental Plan"])
    functions.append([3, "Find State Average Individual Rate for specific age"])


def main():
    print("Welcome to Healthcare Insurance Database System!")
    print("Data Source: The Centers for Medicare & Medicaid Services(CMS)\n")
    while True:
        print("\n==============Function Menu==============")
        functions = list()
        init(functions)
        print(tabulate(functions, ["Option", "Description"], tablefmt="fancy_grid"))
        index = input("\nPlease select an option:")
        if index.strip() == "1":
            handle_search_medical_plan()
        elif index.strip() == "2":
            handle_search_medical_plan()
        elif index.strip() == "3":
            handle_find_avg_rate()
        elif index == "quit":
            print("Bye.")
            exit(0)
        else:
            print("Invalid Index.")


if __name__ == '__main__':
    main()
