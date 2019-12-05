CREATE USER manager WITH PASSWORD 'manager';
CREATE DATABASE insurance;
GRANT ALL PRIVILEGES ON DATABASE insurance TO manager;

\connect insurance

-- 1. Plan Attributes Data Set

CREATE TABLE plans
(
    plan_id                      CHAR(17),
    plan_variant_name            VARCHAR(63),
    std_component_id             CHAR(14),
    plan_marketing_name          VARCHAR(63),
    year                         CHAR(4),
    state                        CHAR(2),
    market_coverage              INT,
    plan_type                    INT,
    qhp_type                     INT,
    child_only_offering          INT,
    out_of_country_coverage      BOOLEAN,
    out_of_country_coverage_desc VARCHAR(255),
    effective_date               DATE,
    expiration_date              DATE,
    PRIMARY KEY (plan_id)
);

ALTER TABLE plans
    OWNER TO manager;

CREATE TABLE medical_plans
(
    plan_id                          CHAR(17) REFERENCES plans (plan_id),
    metal_level                      INT,
    is_notice_required_for_pregnancy BOOLEAN,
    is_wellness_program_offered      BOOLEAN,
    ehb_percent_total_premium        DECIMAL,
    primary key (plan_id)
);

ALTER TABLE medical_plans
    OWNER TO manager;

CREATE TABLE medical_plan_disease
(
    plan_id CHAR(17) REFERENCES medical_plans (plan_id),
    disease VARCHAR(31)
);

ALTER TABLE medical_plan_disease
    OWNER TO manager;

CREATE TABLE medical_plan_moop_ded
(
    plan_id           CHAR(17) REFERENCES medical_plans (plan_id),
    moop_or_ded       INT, -- MOOP, DEDUCTIBLE
    medical_drug_type INT, -- MEDICAL, DRUG, INTEGRATED
    network_type      INT, -- INN_TIER1, INN_TIER2, OON, COMB_INN_OON
    object_type       INT, -- INDIVIDUAL, FAMILY_PER_PERSON, FAMILY_PER_GROUP
    amount            INT
);

ALTER TABLE medical_plan_moop_ded
    OWNER TO manager;

CREATE TABLE dental_plans
(
    plan_id     CHAR(17) REFERENCES plans (plan_id),
    metal_level INT, -- HIGH, LOW
    PRIMARY KEY (plan_id)
);

ALTER TABLE dental_plans
    OWNER TO manager;

CREATE TABLE dental_plan_moop_ded
(
    plan_id      CHAR(17) REFERENCES plans (plan_id),
    moop_or_ded  INT, -- MOOP, DEDUCTIBLE
    network_type INT, -- INN_TIER1, INN_TIER2, OON, COMB_INN_OON
    object_type  INT, -- INDIVIDUAL, FAMILY_PER_PERSON, FAMILY_PER_GROUP
    amount       INT
);

ALTER TABLE dental_plan_moop_ded
    OWNER TO manager;

-- 2. Benefits Data Set

CREATE TABLE benefits
(
    id   INT PRIMARY KEY,
    name VARCHAR(31)
);

ALTER TABLE benefits
    OWNER TO manager;

CREATE TABLE plan_benefit
(
    plan_id               CHAR(17),
    benefit_id            INT,
    copay_inn_tier1       NUMERIC(5, 2),
    copay_inn_tier1_type  INT,
    copay_inn_tier2       NUMERIC(5, 2),
    copay_inn_tier2_type  INT,
    copay_oon             NUMERIC(5, 2),
    copay_oon_type        INT,
    coins_inn_tier1       NUMERIC(5, 2),
    coins_inn_tier1_type  INT,
    coins_inn_tier2       NUMERIC(5, 2),
    coins_inn_tier2_type  INT,
    coins_oon             NUMERIC(5, 2),
    coins_oon_type        INT,
    is_ehb                BOOLEAN,
    is_excl_from_inn_moop BOOLEAN,
    is_excl_from_oon_moop BOOLEAN,
    PRIMARY KEY (plan_id, benefit_id),
    FOREIGN KEY (benefit_id) REFERENCES benefits (id),
    FOREIGN KEY (plan_id) REFERENCES plans (plan_id)
);

ALTER TABLE plan_benefit
    OWNER TO manager;

CREATE TABLE plan_benefit_limitation
(
    plan_id     CHAR(17),
    benefit_id  INT,
    limit_qty   INT,
    limit_unit  INT,
    exclusions  VARCHAR(255),
    explanation VARCHAR(255),
    PRIMARY KEY (plan_id, benefit_id),
    FOREIGN KEY (plan_id, benefit_id) REFERENCES plan_benefit (plan_id, benefit_id)
);

ALTER TABLE plan_benefit_limitation
    OWNER TO manager;


-- 3. Rate Data Set

CREATE TABLE rate_individual
(
    effective_date          DATE,
    expiration_date         DATE,
    std_component_id        CHAR(14),
    rating_area_id          INT,
    tobacco                 INT,
    age                     INT,
    individual_rate         NUMERIC(6, 2),
    individual_tobacco_rate NUMERIC(6, 2),
    PRIMARY KEY (effective_date, expiration_date, std_component_id, rating_area_id, age)
);

ALTER TABLE rate_individual
    OWNER TO manager;

CREATE TABLE rate_family
(
    effective_date   DATE,
    expiration_date  DATE,
    std_component_id CHAR(14),
    rating_area_id   INT,
    individual       NUMERIC(6, 2),
    family_type      INT,
    family_rate      NUMERIC(6, 2),
    PRIMARY KEY (effective_date, expiration_date, std_component_id, rating_area_id)
);

ALTER TABLE rate_family
    OWNER TO manager;