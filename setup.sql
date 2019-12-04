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
    drug_comb_inn_oon_family_per_group     INT
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
    total_comb_inn_oon_family_per_group  INT
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
    drug_comb_inn_oon_family_per_group     INT
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
    total_comb_inn_oon_family_per_group  INT
);

ALTER TABLE medical_plan_ded_integrated
    OWNER TO manager;

CREATE TABLE dental_plans
(
    plan_id                        CHAR(17) REFERENCES plans (plan_id),
    metal_level                    INT,
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

ALTER TABLE dental_plans
    OWNER TO manager;

-- 2. Benefits Data Set

CREATE TABLE benefits
(
    id   INT,
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
    is_excl_from_inn_mood BOOLEAN,
    is_excl_from_oon_mood BOOLEAN
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
    explanation VARCHAR(255)
);

ALTER TABLE plan_benefit_limitation
    OWNER TO manager;


-- 3. Rate Data Set

CREATE TABLE rate_individual
(
    effective_date          DATE,
    expiration_date         DATE,
    plan_id                 CHAR(14),
    rating_area_id          INT,
    tobacco                 INT,
    age                     INT,
    individual_rate         NUMERIC(6, 2),
    individual_tobacco_rate NUMERIC(6, 2),
    primary key (effective_date, expiration_date, plan_id, rating_area_id, age)
);

ALTER TABLE rate_individual
    OWNER TO manager;

CREATE TABLE rate_family
(
    effective_date                       DATE,
    expiration_date                      DATE,
    plan_id                              CHAR(14),
    rating_area_id                       INT,
    individual                           NUMERIC(6, 2),
    couple                               NUMERIC(6, 2),
    primary_and_one_dependent            NUMERIC(6, 2),
    primary_and_two_dependents           NUMERIC(6, 2),
    primart_and_three_or_more_dependents NUMERIC(6, 2),
    couple_and_one_dependent             NUMERIC(6, 2),
    couple_and_two_dependent             NUMERIC(6, 2),
    couple_and_three_or_more_dependents  NUMERIC(6, 2),
    primary key (effective_date, expiration_date, plan_id, rating_area_id)
);

ALTER TABLE rate_family
    OWNER TO manager;