import database as db
from tabulate import tabulate


# Helper Function
def list_to_dict(keys, user_input):
    """
    :param keys, user_input: list, list
    :return: dictionary
    """
    res = {keys[i]: user_input[i] for i in range(len(keys))}
    return res


# User Input
# setup the main menu list for healthcare insurance system query
def print_menu_list(header_list, user_input):
    print("************************Insurance Search List:************************")
    print(tabulate(user_input, headers=header_list, showindex="always"))
    print()


def get_insurance_type():
    values = [["Medical"], ["Dental"]]
    print(tabulate(values, headers=["Insurance Type"], showindex="always"))
    num = input("-Please enter the insurance type number: ")
    print()
    return values[int(num)][0]


def get_subscriber():
    values = [["Individual"], ["Family"]]
    print(tabulate(values, headers=["Primary Subscriber"], showindex="always"))
    num = input("-Please enter the primary subscriber number: ")
    print()
    return values[int(num)][0]


def get_cover_range():
    values = [["Adult and Child"], ["Child Only"], ["Adult Only"]]
    print(tabulate(values, headers=["Cover Range"], showindex="always"))
    num = input("-Please enter the cover range number: ")
    print()
    return values[int(num)][0]


def get_metal_level_dental():
    values = [['High'],
              ['Low']]
    print(tabulate(values, headers=["Metal Level"], showindex="always"))
    num = input("-Please enter the metal level number: ")
    print()
    return values[int(num)][0]


def get_metal_level_medical():
    values = [['Platinum'], ['Gold'],
              ['Silver'], ['Bronze'],
              ['Catastrophic']]
    print(tabulate(values, headers=["Metal Level"], showindex="always"))
    num = input("-Please enter the metal level number: ")
    print()
    return values[int(num)][0]


def get_wellness():
    while True:
        num = input("-Whether need wellness program (YES/NO): ")
        print()
        if num not in ("YES", "NO"):
            print("Oops Wrong input!")
            continue
        else:
            break
    return num


def get_out_of_country():
    while True:
        num = input("-Whether need out of country coverage (YES/NO): ")
        print()
        if num not in ("YES", "NO"):
            print("Oops Wrong input!")
            continue
        else:
            break
    return num


def get_exchange():
    values = [['On Exchange'], ['Off Exchange'], ['Both']]
    print(tabulate(values, headers=["Exchange Preference"], showindex="always"))
    num = input("-Please enter the exchange preference number: ")
    print()
    return values[int(num)][0]


def get_payment():
    values = [["Copay"], ["Coin"]]
    print(tabulate(values, headers=["Payment Type"], showindex="always"))
    num = input("-Please enter the payment type number: ")
    print()
    return values[int(num)][0]


def get_state():
    state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
                  'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM',
                  'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
                  'WI', 'WY']
    while True:
        state = input("-Please enter the state code: ")
        print()
        if state not in state_list:
            print("Oops Wrong State Code!")
            continue
        else:
            break
    return state


def get_family_type():
    header_list = ["Family Type"]
    value_list = [['Couple'], ['PrimarySubscriberAndOneDependent'], ['PrimarySubscriberAndTwoDependents'],
                  ['PrimarySubscriberAndThreeOrMoreDependents'],
                  ['CoupleAndOneDependent'], ['CoupleAndTwoDependents'], ['CoupleAndThreeOrMoreDependents']]
    print(tabulate(value_list, headers=header_list, showindex="always"))
    type = input("-Please enter the family type number: ")
    print()
    return value_list[int(type)][0]


def get_age():
    age = input("-Please enter the primary subscriber age: ")
    print()
    return age


# Function for processing the user input
def input_processing():
    header_list = ["Insurance Type", "Subscriber", "Cover Range", "Metal Level", "Wellness Program",
                   "Exchange", "Out of Country", "Payment Type", "Age", "State", "Family Type"]
    user_input = []
    print_menu_list(header_list, user_input)
    type_str = get_insurance_type()
    subscribe_str = get_subscriber()
    if type_str == "Medical" and subscribe_str == 'Individual':
        user_input = [type_str, subscribe_str, get_cover_range(), get_metal_level_medical(),
                      get_wellness(),
                      get_exchange(), get_out_of_country(), get_payment(), get_age(), get_state(),
                      ""]

    elif type_str == 'Dental' and subscribe_str == 'Individual':
        user_input = [type_str, subscribe_str, get_cover_range(), get_metal_level_dental(),
                      "",
                      get_exchange(), get_out_of_country(), get_payment(), get_age(), get_state(),
                      ""]

    elif type_str == "Medical" and subscribe_str == 'Family':
        user_input = [type_str, subscribe_str, get_cover_range(), get_metal_level_medical(),
                      get_wellness(),
                      get_exchange(), get_out_of_country(), get_payment(), get_age(), get_state(),
                      get_family_type()]

    elif type_str == 'Dental' and subscribe_str == 'Family':
        user_input = [type_str, subscribe_str, get_cover_range(), get_metal_level_dental(),
                      "",
                      get_exchange(), get_out_of_country(), get_payment(), get_age(), get_state(),
                      get_family_type()]

    assert (len(header_list) == len(user_input))
    print_menu_list(header_list, [user_input])
    return list_to_dict(header_list, user_input)


def main():
    print("Welcome to Healthcare Insurance Database System!")
    print("Data Source: The Centers for Medicare & Medicaid Services(CMS)\n")
    while True:
        print("======Initializing new search======")
        db.Query(input_processing()).run_query()


main()
