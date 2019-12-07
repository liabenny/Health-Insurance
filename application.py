import database as db
from tabulate import tabulate


# User Input
# setup the main menu list for healthcare insurance system query
def print_menu_list():
    print("************************Insurance Search List:************************")
    header_list = ["Insurance Type", "Subscriber", "Cover Range", "Metal Level", "Wellness Program",
                   "Exchange", "Out of Country", "Payment Type", "Tier1", "Tier2", "Out of Net",
                   "Maximum Out of Pocket", "Plan Description"]
    # 1
    option1 = get_option1()
    assert (len(option1) == len(header_list))
    # 2
    option2 = get_option2()
    assert (len(option2) == len(header_list))
    # 3
    option3 = get_option3()
    assert (len(option3) == len(header_list))
    # 4
    option4 = get_option4()
    assert (len(option4) == len(header_list))
    # 5
    option5 = get_option5()
    assert (len(option5) == len(header_list))
    # 6
    option6 = get_option6()
    assert (len(option6) == len(header_list))

    table = [option1, option2, option3, option4, option5, option6]
    print(tabulate(table, headers=header_list, showindex="always"))


# Function tailored to get the parameters for each options
def get_option1():
    return ["Medical", "Individual", "Adult Only", "Catastrophic", "NO", "YES", "NO", "Not Applicable",
            "No Charge after deductible", "No Charge after deductible", "No Charge after deductible", "8000",
            "Low monthly premiums and very high deductibles"]


def get_option2():
    return ["Medical", "Family", "Adult and Child", "Bronze", "NO", "YES", "NO", "Copay",
            "$500 Copay after deductible", "$550 Copay after deductible", "NO", "1000",
            "Relatively low monthly premiums and medium deductibles"]


def get_option3():
    return ["Medical", "Family", "Adult and Child", "Platinum", "YES", "NO", "YES", "Coinsurance",
            "No Charge after deductible", "50.00% Coinsurance after deductible", "100%", "500",
            "High monthly premiums and low deductibles"]


def get_option4():
    return ["Dental", "Individual", "Child Only", "High", "Not Applicable", "NO", "NO", "Coin", "100%",
            "Not Applicable", "100%", "Not Applicable", "High monthly premiums"]


def get_option5():
    return ["Dental", "Individual", "Adult Only", "High", "Not Applicable", "NO", "NO", "Coin", "50%",
            "Not Applicable", "50%", "Not Applicable", "Basic Plan"]


def get_option6():
    return ["Medical", "Family", "Adult and Child", "Silver", "No", "YES", "NO", "Copay", "$30", "Not Applicable",
            "$30", "5850", "Premera Blue Cross Preferred Silver 4500 CSR1"]


# Helper Function
def list_to_dict(option):
    """
    :param option: list
    :return: dictionary
    """
    keys = ["Insurance Type", "Subscriber", "Cover Range", "Metal Level", "Wellness Program",
            "Exchange", "Out of Country", "Payment Type", "Tier1", "Tier2", "Out of Net",
            "Maximum Out of Pocket", "Plan Description"]
    res = {keys[i]: option[i] for i in range(len(keys))}
    return res


# Second level menus
def state_2nd():
    state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
                  'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM',
                  'NY',
                  'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
                  'WI', 'WY']
    while True:
        state = input("Please enter the state code: ")
        if state not in state_list:
            print("Oops Wrong State Code!")
            continue
        else:
            break
    return state


def individual_2nd():
    age = input("Please enter the subscriber age: ")
    return age


def family_2nd():
    print("Family Type List:")
    header_list = ["Family Type"]
    value_list = [['Couple'], ['PrimarySubscriberAndOneDependent'], ['PrimarySubscriberAndTwoDependents'],
                  ['PrimarySubscriberAndThreeOrMoreDependents'],
                  ['CoupleAndOneDependent'], ['CoupleAndTwoDependents'], ['CoupleAndThreeOrMoreDependents']]
    print(tabulate(value_list, headers=header_list, showindex="always"))
    type = input("Please enter the family type number: ")
    return value_list[int(type)][0]


# Function for processing the user input
def input_processing(user_input):
    """
    :param user_input: string
    :return: None
    """
    if user_input == '0':
        option1 = list_to_dict(get_option1())
        option1["State"] = state_2nd()
        age = individual_2nd()
        if int(age) > 30:
            print("Not Eligible Subscriber!")
        else:
            option1["Age"] = int(age)
            db.Query(option1).run_option1()

    elif user_input == '1':
        option2 = list_to_dict(get_option2())
        option2["Family Type"] = family_2nd()
        option2["State"] = state_2nd()
        db.Query(option2).run_option2()

    elif user_input == '2':
        option3 = list_to_dict(get_option3())
        option3["Family Type"] = family_2nd()
        option3["State"] = state_2nd()
        db.Query(option3).run_option3()

    elif user_input == '3':
        option4 = list_to_dict(get_option4())
        option4["State"] = state_2nd()
        db.Query(option4).run_option4()

    elif user_input == '4':
        option5 = list_to_dict(get_option5())
        option5["State"] = state_2nd()
        db.Query(option5).run_option5()

    elif user_input == '5':
        option6 = list_to_dict(get_option6())
        option6["Family Type"] = family_2nd()
        option6["State"] = state_2nd()
        db.Query(option6).run_option6()

    elif user_input == 'quit':
        print("Thank you for your visiting!")
        exit()

    else:
        print("Oops, Something is going wrong here :(")


def main():
    print("Welcome to Healthcare Insurance Database System!")
    while True:
        print_menu_list()
        user_input = input("Please enter the option number: ")
        input_processing(user_input)


main()
