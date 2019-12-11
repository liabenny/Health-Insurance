import re
from tabulate import tabulate


def get_num_int(value):
    res = re.findall("[0-9,]+", value)
    if res:
        return res[0].replace(",", "")
    else:
        return None


def get_num_decimal(value):
    res = re.findall("[0-9.,]+", value)
    if res:
        return res[0].replace(",", "")
    else:
        return 0


def get_desc(value):
    res = re.findall("[a-zA-Z ]+", value)
    if res:
        return res[0].strip()
    else:
        return None


def get_age_pair(age_str):
    if age_str == '0-14':
        return 0, 14
    elif age_str == '64 and over':
        return 64, 100
    else:
        return age_str, age_str


def print_series(series, header, showindex=False):
    tmp = list()
    for element in series:
        tmp.append([element])
    print(tabulate(tmp, headers=[header], tablefmt="fancy_grid", showindex=showindex))


def print_data_frame(data_frame, headers, showindex=False):
    print(tabulate(data_frame, headers=headers, tablefmt="fancy_grid", showindex=showindex))
