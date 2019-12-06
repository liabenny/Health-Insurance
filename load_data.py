import csv
import psycopg2

# file_name = "C:\\RPI\\Database-Systems\\project\\datasets\\Benefits_Cost_Sharing_PUF.csv"
file_name = "C:\\RPI\\Database-Systems\\project\\datasets\\Plan_Attributes_PUF.csv"

with open(file_name, mode='r') as f:
    reader = csv.DictReader(f)
    print(type(reader))
    for row in reader:
        print(type(row))
        print(row["PlanId"])


def load_plans(cursor):
    print("------LOAD PLAN ATTRIBUTES------")
    with open(file_name, mode='r') as fd:
        reader = csv.DictReader(fd)
        for raw_plan in reader:
            add_plan_general_info(cursor, raw_plan)

            is_dental_plan = raw_plan['DentalOnlyPlan']
            if is_dental_plan == "YES":
                add_dental_plan()
            else:
                add_medical_plan()


def add_plan_general_info(cursor, raw):
    pass


def add_dental_plan():
    pass


def add_medical_plan():
    pass


def load_benefits():
    pass


def load_rates():
    pass


if __name__ == '__main__':
    # Connect to database
    hostname = "172.17.0.2"
    dbname = "insurance"
    user = "manager"
    conn = psycopg2.connect("host=%s dbname=%s user=%s" % (hostname, dbname, user))
    cursor = conn.cursor()

    # Load Plan_Attributes_PUF.csv
    load_plans(cursor)
    conn.commit()
