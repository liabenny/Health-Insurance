import re


def get_num_int(value):
    res = re.findall("[0123456789,]+", value)
    if res:
        return res[0].replace(",", "")
    else:
        return None
