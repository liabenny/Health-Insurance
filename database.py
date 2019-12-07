# database related code
import tabulate as tabulate


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
        pass

    def get_select(self):
        pass

    def get_from(self):
        pass

    def get_where(self):
        pass
