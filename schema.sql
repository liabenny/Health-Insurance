CREATE USER manager WITH PASSWORD 'manager';
CREATE DATABASE insurance;
GRANT ALL PRIVILEGES ON DATABASE insurance TO manager;

\connect insurance

/* -------------------------Enumeration Tables--------------------------- */

-- Individual
-- SHOP (Small Group)
CREATE TABLE market_coverage_type
(
    id        INT,
    type_name VARCHAR(31),
    primary key (id)
);

ALTER TABLE market_coverage_type
    OWNER TO manager;

-- Indemnity
-- PPO
-- HMO
-- POS
-- EPO
CREATE TABLE plan_type
(
    id        INT,
    type_name VARCHAR(15),
    primary key (id)
);

ALTER TABLE plan_type
    OWNER TO manager;

-- On Exchange
-- Off Exchange
-- Both
CREATE TABLE qhp_type
(
    id        INT,
    type_name VARCHAR(31),
    primary key (id)
);

ALTER TABLE qhp_type
    OWNER TO manager;


-- Allows Adult and Child-Only
-- Allows Adult-Only
-- Allows Child-Only
CREATE TABLE child_only_offering_type
(
    id        INT,
    type_name VARCHAR(31),
    primary key (id)
);

ALTER TABLE child_only_offering_type
    OWNER TO manager;


-- HIOS
-- SERFF
-- OPM
CREATE TABLE source_name_type
(
    id        INT,
    type_name VARCHAR(7),
    primary key (id)
);

ALTER TABLE source_name_type
    OWNER TO manager;

-- Platinum
-- Gold
-- Silver
-- Bronze
-- Catastrophic
CREATE TABLE medical_metal_level_type
(
    id        INT,
    type_name VARCHAR(15),
    primary key (id)
);

ALTER TABLE medical_metal_level_type
    OWNER TO manager;

-- High
-- Low
CREATE TABLE dental_metal_level_type
(
    id        INT,
    type_name VARCHAR(7),
    primary key (id)
);

ALTER TABLE dental_metal_level_type
    OWNER TO manager;

-- No Preference
-- Tobacco User/Non-Tobacco User
CREATE TABLE tobacco_type
(
    id        INT,
    type_name VARCHAR(31),
    primary key (id)
);

ALTER TABLE tobacco_type
    OWNER TO manager;

CREATE TABLE age_type
(
    id      INT,
    minimum INT,
    maximum INT,
    primary key (id)
);

ALTER TABLE age_type
    OWNER TO manager;


-- Couple
-- PrimarySubscriberAndOneDependent
-- PrimarySubscriberAndTwoDependents
-- PrimarySubscriberAndThreeOrMoreDependents
-- CoupleAndOneDependent
-- CoupleAndTwoDependents
-- CoupleAndThreeOrMoreDependents
CREATE TABLE family_type
(
    id        INT,
    type_name VARCHAR(63),
    primary key (id)
);

ALTER TABLE family_type
    OWNER TO manager;

-- No Charge
-- No Charge after deductible
-- $X Copay
-- $X Copay after deductible
-- $X Copay before deductible
-- $X Copay with deductible
-- $X Copay per Day
-- $X Copay per Stay
-- $X Copay per Day after deductible
-- $X Copay per Stay after deductible
-- $X Copay per Day before deductible
-- $X Copay per Stay before deductible
-- $X Copay per Day with deductible
-- $X Copay per Stay with deductible
-- Not Applicable
CREATE TABLE copay_type
(
    id        INT,
    type_name VARCHAR(63),
    primary key (id)
);

ALTER TABLE copay_type
    OWNER TO manager;

-- No Charge
-- No Charge after deductible
-- X%
-- X% Coinsurance after deductible
-- Not Applicable
CREATE TABLE coin_type
(
    id        INT,
    type_name VARCHAR(63),
    primary key (id)
);

ALTER TABLE coin_type
    OWNER TO manager;

-- Hours per week
-- Hours per month
-- Hours per year
-- Days per week
-- Days per month
-- Days per year
-- Months per year
-- Visits per week
-- Visits per month
-- Visits per year
-- Lifetime visits
-- Treatments per week
-- Treatments per month
-- Lifetime treatments
-- Lifetime admissions
-- Procedures per week
-- Procedures per month
-- Procedures per year
-- Lifetime procedures
-- Dollars per year
-- Dollars per visit
-- Days per admission
-- Procedures per episode
CREATE TABLE limit_unit_type
(
    id        INT,
    type_name VARCHAR(31),
    primary key (id)
);

ALTER TABLE limit_unit_type
    OWNER TO manager;

-- Design Type 1
-- Design Type 2
-- Design Type 3
-- Design Type 4
-- Design Type 5
-- Not Applicable
CREATE TABLE design_type
(
    id        INT,
    type_name VARCHAR(15),
    primary key (id)
);

ALTER TABLE design_type
    OWNER TO manager;

/* -------------------------Plan Attributes Data Set--------------------------- */

CREATE TABLE issuer
(
    issuer_id CHAR(5),
    tin       CHAR(10),
    PRIMARY KEY (issuer_id)
);

ALTER TABLE issuer
    OWNER TO manager;

CREATE TABLE plans
(
    plan_id                              CHAR(17),
    plan_variant_name                    VARCHAR(63),
    std_component_id                     CHAR(14),
    plan_marketing_name                  VARCHAR(63),
    year                                 CHAR(4),
    state                                CHAR(2),
    source_name                          INT REFERENCES source_name_type (id),
    import_date                          TIMESTAMP,
    hios_product_id                      CHAR(10),
    hpid                                 CHAR(10),
    network_id                           CHAR(6),
    service_area_id                      CHAR(6),
    formulary_id                         CHAR(6),
    is_new_plan                          BOOLEAN,
    market_coverage                      INT REFERENCES market_coverage_type (id),
    plan_type                            INT REFERENCES plan_type (id),
    qhp_type                             INT REFERENCES qhp_type (id),
    design_type                          INT REFERENCES design_type (id),
    child_only_offering                  INT REFERENCES child_only_offering_type (id),
    composite_rate_offered               BOOLEAN,
    out_of_country_coverage              BOOLEAN,
    out_of_country_coverage_desc         VARCHAR(255),
    out_of_service_area_coverage         BOOLEAN,
    out_of_service_area_coverage_desc    VARCHAR(255),
    plan_level_exclusions                VARCHAR(255),
    est_advanced_payment_for_indian_plan DECIMAL(5, 2),
    csr_variant_type                     INT,
    multiple_in_network_tiers            BOOLEAN,
    first_tier_utilization               INT,
    second_tier_utilization              INT,
    effective_date                       DATE,
    expiration_date                      DATE,
    PRIMARY KEY (plan_id)
);

ALTER TABLE plans
    OWNER TO manager;

CREATE TABLE medical_plans
(
    plan_id                          CHAR(17) REFERENCES plans (plan_id),
    metal_level                      INT REFERENCES medical_metal_level_type (id),
    is_notice_required_for_pregnancy BOOLEAN,
    is_wellness_program_offered      BOOLEAN,
    unique_design                    BOOLEAN,
    ehb_percent_total_premium        DECIMAL,
    primary key (plan_id)
);

ALTER TABLE medical_plans
    OWNER TO manager;

CREATE TABLE medical_plan_referal
(
    plan_id            CHAR(17) REFERENCES plans (plan_id),
    specialist_referal VARCHAR(255),
    PRIMARY KEY (plan_id)
);

ALTER TABLE medical_plan_referal
    OWNER TO manager;

CREATE TABLE medical_plan_disease
(
    plan_id CHAR(17) REFERENCES medical_plans (plan_id),
    disease VARCHAR(31)
);

ALTER TABLE medical_plan_disease
    OWNER TO manager;

CREATE TABLE medical_plan_sbc
(
    plan_id                            CHAR(17) REFERENCES plans (plan_id),
    having_baby_deductible             INT,
    having_baby_copayment              INT,
    having_baby_coinsurance            INT,
    having_baby_limit                  INT,
    having_diabetes_deductible         INT,
    having_diabetes_copayment          INT,
    having_diabetes_coinsurance        INT,
    having_diabetes_limit              INT,
    having_simple_fracture_deductible  INT,
    having_simple_fracture_copayment   INT,
    having_simple_fracture_coinsurance INT,
    having_simple_fracture_limit       INT,
    PRIMARY KEY (plan_id)
);

ALTER TABLE medical_plan_sbc
    OWNER TO manager;

CREATE TABLE medical_plan_moop
(
    plan_id                                CHAR(17) REFERENCES medical_plans (plan_id),
    medical_inn_tier1_individual           INT,
    medical_inn_tier1_family_per_person    INT,
    medical_inn_tier1_family_per_group     INT,
    medical_inn_tier2_individual           INT,
    medical_inn_tier2_family_per_person    INT,
    medical_inn_tier2_family_per_group     INT,
    medical_oon_individual                 INT,
    medical_oon_family_per_person          INT,
    medical_oon_family_per_group           INT,
    medical_comb_inn_oon_individual        INT,
    medical_comb_inn_oon_family_per_person INT,
    medical_comb_inn_oon_family_per_group  INT,

    drug_inn_tier1_individual              INT,
    drug_inn_tier1_family_per_person       INT,
    drug_inn_tier1_family_per_group        INT,
    drug_inn_tier2_individual              INT,
    drug_inn_tier2_family_per_person       INT,
    drug_inn_tier2_family_per_group        INT,
    drug_oon_individual                    INT,
    drug_oon_family_per_person             INT,
    drug_oon_family_per_group              INT,
    drug_comb_inn_oon_individual           INT,
    drug_comb_inn_oon_family_per_person    INT,
    drug_comb_inn_oon_family_per_group     INT,
    PRIMARY KEY (plan_id)
);

ALTER TABLE medical_plan_moop
    OWNER TO manager;

CREATE TABLE medical_plan_moop_integrated
(
    plan_id                              CHAR(17) REFERENCES medical_plans (plan_id),
    total_inn_tier1_individual           INT,
    total_inn_tier1_family_per_person    INT,
    total_inn_tier1_family_per_group     INT,
    total_inn_tier2_individual           INT,
    total_inn_tier2_family_per_person    INT,
    total_inn_tier2_family_per_group     INT,
    total_oon_individual                 INT,
    total_oon_family_per_person          INT,
    total_oon_family_per_group           INT,
    total_comb_inn_oon_individual        INT,
    total_comb_inn_oon_family_per_person INT,
    total_comb_inn_oon_family_per_group  INT,
    PRIMARY KEY (plan_id)
);

ALTER TABLE medical_plan_moop_integrated
    OWNER TO manager;

CREATE TABLE medical_plan_ded
(
    plan_id                                CHAR(17) REFERENCES medical_plans (plan_id),
    medical_inn_tier1_individual           INT,
    medical_inn_tier1_family_per_person    INT,
    medical_inn_tier1_family_per_group     INT,
    medical_inn_tier2_individual           INT,
    medical_inn_tier2_family_per_person    INT,
    medical_inn_tier2_family_per_group     INT,
    medical_oon_individual                 INT,
    medical_oon_family_per_person          INT,
    medical_oon_family_per_group           INT,
    medical_comb_inn_oon_individual        INT,
    medical_comb_inn_oon_family_per_person INT,
    medical_comb_inn_oon_family_per_group  INT,

    drug_inn_tier1_individual              INT,
    drug_inn_tier1_family_per_person       INT,
    drug_inn_tier1_family_per_group        INT,
    drug_inn_tier2_individual              INT,
    drug_inn_tier2_family_per_person       INT,
    drug_inn_tier2_family_per_group        INT,
    drug_oon_individual                    INT,
    drug_oon_family_per_person             INT,
    drug_oon_family_per_group              INT,
    drug_comb_inn_oon_individual           INT,
    drug_comb_inn_oon_family_per_person    INT,
    drug_comb_inn_oon_family_per_group     INT,
    PRIMARY KEY (plan_id)
);

ALTER TABLE medical_plan_ded
    OWNER TO manager;

CREATE TABLE medical_plan_ded_integrated
(
    plan_id                              CHAR(17) REFERENCES medical_plans (plan_id),
    total_inn_tier1_individual           INT,
    total_inn_tier1_family_per_person    INT,
    total_inn_tier1_family_per_group     INT,
    total_inn_tier2_individual           INT,
    total_inn_tier2_family_per_person    INT,
    total_inn_tier2_family_per_group     INT,
    total_oon_individual                 INT,
    total_oon_family_per_person          INT,
    total_oon_family_per_group           INT,
    total_comb_inn_oon_individual        INT,
    total_comb_inn_oon_family_per_person INT,
    total_comb_inn_oon_family_per_group  INT,
    PRIMARY KEY (plan_id)
);

ALTER TABLE medical_plan_ded_integrated
    OWNER TO manager;

CREATE TABLE dental_plans
(
    plan_id                                CHAR(17) REFERENCES plans (plan_id),
    metal_level                            INT REFERENCES dental_metal_level_type (id),
    ehb_pediatric_dental_apportionment_qty DECIMAL,
    is_guaranteed_rate                     BOOLEAN,
    PRIMARY KEY (plan_id)
);

ALTER TABLE dental_plans
    OWNER TO manager;

CREATE TABLE dental_plan_moop
(
    plan_id                        CHAR(17) REFERENCES plans (plan_id),
    inn_tier1_individual           INT,
    inn_tier1_family_per_person    INT,
    inn_tier1_family_per_group     INT,
    inn_tier2_individual           INT,
    inn_tier2_family_per_person    INT,
    inn_tier2_family_per_group     INT,
    oon_individual                 INT,
    oon_family_per_person          INT,
    oon_family_per_group           INT,
    comb_inn_oon_individual        INT,
    comb_inn_oon_family_per_person INT,
    comb_inn_oon_family_per_group  INT,
    PRIMARY KEY (plan_id)
);

ALTER TABLE dental_plan_moop
    OWNER TO manager;

CREATE TABLE dental_plan_ded
(
    plan_id                        CHAR(17) REFERENCES plans (plan_id),
    inn_tier1_individual           INT,
    inn_tier1_family_per_person    INT,
    inn_tier1_family_per_group     INT,
    inn_tier2_individual           INT,
    inn_tier2_family_per_person    INT,
    inn_tier2_family_per_group     INT,
    oon_individual                 INT,
    oon_family_per_person          INT,
    oon_family_per_group           INT,
    comb_inn_oon_individual        INT,
    comb_inn_oon_family_per_person INT,
    comb_inn_oon_family_per_group  INT,
    PRIMARY KEY (plan_id)
);

ALTER TABLE dental_plan_ded
    OWNER TO manager;

/* -------------------------Benefits Data Set--------------------------- */

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
    benefit_id            INT REFERENCES benefits (id),
    copay_inn_tier1       NUMERIC(5, 2),
    copay_inn_tier1_type  INT REFERENCES copay_type (id),
    copay_inn_tier2       NUMERIC(5, 2),
    copay_inn_tier2_type  INT REFERENCES copay_type (id),
    copay_oon             NUMERIC(5, 2),
    copay_oon_type        INT REFERENCES copay_type (id),
    coins_inn_tier1       NUMERIC(5, 2),
    coins_inn_tier1_type  INT REFERENCES coin_type (id),
    coins_inn_tier2       NUMERIC(5, 2),
    coins_inn_tier2_type  INT REFERENCES coin_type (id),
    coins_oon             NUMERIC(5, 2),
    coins_oon_type        INT REFERENCES coin_type (id),
    is_ehb                BOOLEAN,
    is_excl_from_inn_mood BOOLEAN,
    is_excl_from_oon_mood BOOLEAN,
    PRIMARY KEY (plan_id, benefit_id)
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


/* -------------------------Rate Data Set--------------------------- */

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

/* -------------------------Enumeration Initialization--------------------------- */

INSERT INTO market_coverage_type
VALUES (1, 'Individual');
INSERT INTO market_coverage_type
VALUES (2, 'SHOP (Small Group)');
INSERT INTO plan_type
VALUES (1, 'Indemnity');
INSERT INTO plan_type
VALUES (2, 'PPO');
INSERT INTO plan_type
VALUES (3, 'HMO');
INSERT INTO plan_type
VALUES (4, 'POS');
INSERT INTO plan_type
VALUES (5, 'EPO');
INSERT INTO qhp_type
VALUES (1, 'On the Exchange');
INSERT INTO qhp_type
VALUES (2, 'Off the Exchange');
INSERT INTO qhp_type
VALUES (3, 'Both');
INSERT INTO child_only_offering_type
VALUES (1, 'Allows Adult and Child-Only');
INSERT INTO child_only_offering_type
VALUES (2, 'Allows Adult-Only');
INSERT INTO child_only_offering_type
VALUES (3, 'Allows Child-Only');
INSERT INTO source_name_type
VALUES (1, 'HIOS');
INSERT INTO source_name_type
VALUES (2, 'SERFF');
INSERT INTO source_name_type
VALUES (3, 'OPM');
INSERT INTO medical_metal_level_type
VALUES (1, 'Platinum');
INSERT INTO medical_metal_level_type
VALUES (2, 'Gold');
INSERT INTO medical_metal_level_type
VALUES (3, 'Silver');
INSERT INTO medical_metal_level_type
VALUES (4, 'Bronze');
INSERT INTO medical_metal_level_type
VALUES (5, 'Catastrophic');
INSERT INTO dental_metal_level_type
VALUES (1, 'High');
INSERT INTO dental_metal_level_type
VALUES (2, 'Low');
INSERT INTO tobacco_type
VALUES (1, 'No Preference');
INSERT INTO tobacco_type
VALUES (2, 'Tobacco User/Non-Tobacco User');
INSERT INTO age_type
VALUES (1, 0, 14);
INSERT INTO age_type
VALUES (2, 15, 15);
INSERT INTO age_type
VALUES (3, 16, 16);
INSERT INTO age_type
VALUES (4, 17, 17);
INSERT INTO age_type
VALUES (5, 18, 18);
INSERT INTO age_type
VALUES (6, 19, 19);
INSERT INTO age_type
VALUES (7, 20, 20);
INSERT INTO age_type
VALUES (8, 21, 21);
INSERT INTO age_type
VALUES (9, 22, 22);
INSERT INTO age_type
VALUES (10, 23, 23);
INSERT INTO age_type
VALUES (11, 24, 24);
INSERT INTO age_type
VALUES (12, 25, 25);
INSERT INTO age_type
VALUES (21, 26, 26);
INSERT INTO age_type
VALUES (22, 27, 27);
INSERT INTO age_type
VALUES (23, 28, 28);
INSERT INTO age_type
VALUES (24, 29, 29);
INSERT INTO age_type
VALUES (25, 30, 30);
INSERT INTO age_type
VALUES (26, 31, 31);
INSERT INTO age_type
VALUES (27, 32, 32);
INSERT INTO age_type
VALUES (28, 33, 33);
INSERT INTO age_type
VALUES (29, 34, 34);
INSERT INTO age_type
VALUES (30, 35, 35);
INSERT INTO age_type
VALUES (31, 36, 36);
INSERT INTO age_type
VALUES (32, 37, 37);
INSERT INTO age_type
VALUES (33, 38, 38);
INSERT INTO age_type
VALUES (34, 39, 39);
INSERT INTO age_type
VALUES (35, 40, 40);
INSERT INTO age_type
VALUES (36, 41, 41);
INSERT INTO age_type
VALUES (37, 42, 42);
INSERT INTO age_type
VALUES (38, 43, 43);
INSERT INTO age_type
VALUES (39, 44, 44);
INSERT INTO age_type
VALUES (40, 45, 45);
INSERT INTO age_type
VALUES (41, 46, 46);
INSERT INTO age_type
VALUES (42, 47, 47);
INSERT INTO age_type
VALUES (43, 48, 48);
INSERT INTO age_type
VALUES (44, 49, 49);
INSERT INTO age_type
VALUES (45, 50, 50);
INSERT INTO age_type
VALUES (46, 51, 51);
INSERT INTO age_type
VALUES (47, 52, 52);
INSERT INTO age_type
VALUES (48, 53, 53);
INSERT INTO age_type
VALUES (49, 54, 54);
INSERT INTO age_type
VALUES (50, 55, 55);
INSERT INTO age_type
VALUES (51, 56, 56);
INSERT INTO age_type
VALUES (52, 57, 57);
INSERT INTO age_type
VALUES (53, 58, 58);
INSERT INTO age_type
VALUES (54, 59, 59);
INSERT INTO age_type
VALUES (55, 60, 60);
INSERT INTO age_type
VALUES (56, 61, 61);
INSERT INTO age_type
VALUES (57, 62, 62);
INSERT INTO age_type
VALUES (58, 63, 63);
INSERT INTO age_type
VALUES (59, 64, 127);
INSERT INTO family_type
VALUES (1, 'Couple');
INSERT INTO family_type
VALUES (2, 'PrimarySubscriberAndOneDependent');
INSERT INTO family_type
VALUES (3, 'PrimarySubscriberAndTwoDependents');
INSERT INTO family_type
VALUES (4, 'PrimarySubscriberAndThreeOrMoreDependents');
INSERT INTO family_type
VALUES (5, 'CoupleAndOneDependent');
INSERT INTO family_type
VALUES (6, 'CoupleAndTwoDependents');
INSERT INTO family_type
VALUES (7, 'CoupleAndThreeOrMoreDependents');
INSERT INTO copay_type
VALUES (1, 'No Charge');
INSERT INTO copay_type
VALUES (2, 'No Charge after deductible');
INSERT INTO copay_type
VALUES (3, 'Copay');
INSERT INTO copay_type
VALUES (4, 'Copay after deductible');
INSERT INTO copay_type
VALUES (5, 'Copay before deductible');
INSERT INTO copay_type
VALUES (6, 'Copay with deductible');
INSERT INTO copay_type
VALUES (7, 'Copay per Day');
INSERT INTO copay_type
VALUES (8, 'Copay per Stay');
INSERT INTO copay_type
VALUES (9, 'Copay per Day after deductible');
INSERT INTO copay_type
VALUES (10, 'Copay per Stay after deductible');
INSERT INTO copay_type
VALUES (11, 'Copay per Day before deductible');
INSERT INTO copay_type
VALUES (12, 'Copay per Stay before deductible');
INSERT INTO copay_type
VALUES (13, 'Copay per Day with deductible');
INSERT INTO copay_type
VALUES (14, 'Copay per Stay with deductible');
INSERT INTO copay_type
VALUES (15, 'Not Applicable');
INSERT INTO coin_type
VALUES (1, 'No Charge');
INSERT INTO coin_type
VALUES (2, 'No Charge after deductible');
INSERT INTO coin_type
VALUES (3, '%');
INSERT INTO coin_type
VALUES (4, '% Coinsurance after deductible');
INSERT INTO coin_type
VALUES (5, 'Not Applicable');
INSERT INTO limit_unit_type
VALUES (1, 'Hours per week');
INSERT INTO limit_unit_type
VALUES (2, 'Hours per month');
INSERT INTO limit_unit_type
VALUES (3, 'Hours per year');
INSERT INTO limit_unit_type
VALUES (4, 'Days per week');
INSERT INTO limit_unit_type
VALUES (5, 'Days per month');
INSERT INTO limit_unit_type
VALUES (6, 'Days per year');
INSERT INTO limit_unit_type
VALUES (7, 'Months per year');
INSERT INTO limit_unit_type
VALUES (8, 'Months per year');
INSERT INTO limit_unit_type
VALUES (9, 'Visits per week');
INSERT INTO limit_unit_type
VALUES (10, 'Visits per month');
INSERT INTO limit_unit_type
VALUES (11, 'Visits per year');
INSERT INTO limit_unit_type
VALUES (12, 'Lifetime visits');
INSERT INTO limit_unit_type
VALUES (13, 'Treatments per week');
INSERT INTO limit_unit_type
VALUES (14, 'Treatments per month');
INSERT INTO limit_unit_type
VALUES (15, 'Lifetime treatments');
INSERT INTO limit_unit_type
VALUES (16, 'Lifetime admissions');
INSERT INTO limit_unit_type
VALUES (17, 'Procedures per week');
INSERT INTO limit_unit_type
VALUES (18, 'Procedures per month');
INSERT INTO limit_unit_type
VALUES (19, 'Procedures per year');
INSERT INTO limit_unit_type
VALUES (20, 'Lifetime procedures');
INSERT INTO limit_unit_type
VALUES (21, 'Dollars per year');
INSERT INTO limit_unit_type
VALUES (22, 'Dollars per visit');
INSERT INTO limit_unit_type
VALUES (23, 'Days per admission');
INSERT INTO limit_unit_type
VALUES (24, 'Procedures per episode');
INSERT INTO design_type
VALUES (1, 'Design Type 1');
INSERT INTO design_type
VALUES (2, 'Design Type 2');
INSERT INTO design_type
VALUES (3, 'Design Type 3');
INSERT INTO design_type
VALUES (4, 'Design Type 4');
INSERT INTO design_type
VALUES (5, 'Design Type 5');
INSERT INTO design_type
VALUES (6, 'Not Applicable');