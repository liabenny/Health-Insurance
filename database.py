# database related code
import tabulate as tabulate


class Query:
    """
    @:arg: option
    @:type: dictionary
    """
    def __init__(self, option):
        self.option = option

    def run_option1(self):
        pass

    def run_option2(self):
        pass

    def run_option3(self):
        pass

    def run_option4(self):
        pass

    def run_option5(self):
        pass

    def run_option6(self):
        pass

    def print_result(self, res_list):
        header_list = []
        print("-------------Search Result-------------")
        print(tabulate(res_list, headers=header_list, showindex="always"))
