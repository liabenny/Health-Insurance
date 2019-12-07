import database as db
from tabulate import tabulate


# User Input
# setup the main menu list for healthcare insurance system query
def print_menu_list():
    print("Welcome to Healthcare Insurance Database System!")
    print("Insurance Search List:")
    header_list = ["Insurance Type", "Subscriber Type", "Cover Range", "Metal Level", "Wellness Program",
                   "Exchange Preference", "Out of Country", "Payment type", "Tier1", "Tier2", "Out of Net",
                   "Plan Description"]
    # 1
    option1 = ["Medical", "Individual", "Adult Only", "Catastrophic", "NO", "YES", "NO", "NOT APPLICABLE",
               "No Charge after deductible", "Not Applicable", "Not Applicable", "No",
               "Low monthly premiums and very high deductibles"]
    # 2
    option2 = ["Medical", "Family", "Adult and Child", "Bronze", "NO", "YES", "NO", "Copay", ""]
    # 3
    option3 = ["Medical", "Family", "Adult and Child", "Platinum", "YES", "NO", "YES", "Coinsurance",
               "No Charge after deductible"]
    # 4
    option4 = ["Dental", "Individual", "Child Only", "High", "NOT APPLICABLE", "BOTH", "NO", ]
    # 5
    option5 = ["Dental", "Individual", "Adult Only", "High", "NOT APPLICABLE", "NO", "NO", ]
    # 6
    option6 = ["Dental", "Family", "Adult and Child", "Low", "NOT APPLICABLE", "YES", "NO", ]

    table = [option1, option2, option3, option4, option5, option6]
    print(tabulate(table, headers=header_list))


# Function tailored to get the parameters for each options
def get_option1():
    pass


def get_option2():
    pass


def get_option3():
    pass


def get_option4():
    pass


def get_option5():
    pass


def get_option6():
    pass


# Function for processing the user input
def input_processing(user_input):
    if user_input == '1':
        db.Query.option_1(get_option1())
    elif user_input == '2':
        db.Query.option_2(get_option2())
    elif user_input == '3':
        db.Query.option_3(get_option3())
    elif user_input == '4':
        db.Query.option_4(get_option4())
    elif user_input == '5':
        db.Query.option_5(get_option5())
    elif user_input == '6':
        db.Query.option_6(get_option6())
    else:
        print("Oops, Something is going wrong here :(")


def main():
    while (True):
        print_menu_list()
        user_input = input("Please enter the option number: ")
        input_processing(user_input)


main()
