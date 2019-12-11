# Health Insurance Database System

## Authors
Liangbin Zhu, Yujue Wang


## Dataset
Data Source: [The Centers for Medicare & Medicaid Services (CMS) ](https://www.cms.gov/cciio/resources/data-resources/marketplace-puf) 
>[Benefits and Cost Sharing Data](https://www.cms.gov/CCIIO/Resources/Data-Resources/Downloads/BenefitsCostSharing-DataDictionary-20.pdf)\
>[Rate Data](https://www.cms.gov/CCIIO/Resources/Data-Resources/Downloads/Rate-DataDictionary-PY20.pdf)\
>[Plan Attributes Data](https://www.cms.gov/CCIIO/Resources/Data-Resources/Downloads/PlanAttributes-DataDictionary-PY20.pdf)\
>[Business Rules Data](https://www.cms.gov/CCIIO/Resources/Data-Resources/Downloads/BusinessRules-DataDictionary-PY20.pdf)

## Setup Guide
#### Deployment Environment
- Operating System: Linux (centos 7.7.1908)
- Platform: Microsoft Azure
- Container: Docker PostgreSQL & MongoDB
```dockerfile
$ docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
$ docker run --name some-mongo -d mongo:tag
```
#### Database
- PostgreSQL
- MongoDB

#### Programming Language
- Python (3.x)

#### Package
- psycopg2
- tabulate
- csv
- pymongo

#### File Structure
1. schema.sql
2. load_data.py
3. constants.py
4. enumeration.py
5. utils.py
6. application.py
7. database.py

#### Data Loading
#### SQL
```python
python3 load_data.py
```
*load_data.py* supports reading the .csv files and loading into the specific 
database based on the database design of *schema.sql*.

The enumeration data type generated from the allowable values of official 
document file instructions, supported by *enumeration.py*.

#### NON-SQL

## Run
```python
python3 application.py
```
*application.py* supports the user interface by command line and pass the parameters
to *database.py*. It provides multiple-level menu selection and dynamic 
query functions, which delivers the real-time query result as the next step
user options and enables user to add/remove query conditions arbitrarily.

*database.py* bridges the database and python execution. It generates the sql syntax 
based on the use input arguments.

### Data Exploration


## Functions
- [x] SQL and NON-SQL Database
- [x] Dynamic and Real-Time Query
- [x] Automatic Data Loading and Supporting the Long-tern Reuse
- [x] Page Turning
- [x] Avoiding SQL-injection Vulnerabilities

### Acknowledgment
> Professor Samuel B. Johnson\
> Coffee :)

