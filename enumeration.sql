-- Individual
-- SHOP (Small Group)
CREATE TABLE market_coverage_type
(
    id        INT,
    type_name VARCHAR(31),
    primary key (id)
);

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

-- On Exchange
-- Off Exchange
-- Both
CREATE TABLE QHP_type
(
    id        INT,
    type_name VARCHAR(15),
    primary key (id)
);


-- Allows Adult and Child-Only
-- Allows Adult-Only
-- Allows Child-Only
CREATE TABLE child_only_offering_type
(
    id        INT,
    type_name VARCHAR(31),
    primary key (id)
);


-- HIOS
-- SERFF
-- OPM
CREATE TABLE source_name_type
(
    id        INT,
    type_name VARCHAR(7),
    primary key (id)
);

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

-- High
-- Low
CREATE TABLE dental_metal_level_type
(
    id        INT,
    type_name VARCHAR(7),
    primary key (id)
);

-- No Preference
-- Tobacco User/Non-Tobacco User
CREATE TABLE tobacco_type
(
    id        INT,
    type_name VARCHAR(31),
    primary key (id)
);



CREATE TABLE age_type
(
    id      INT,
    minimum INT,
    maximum INT,
    primary key (id)
);

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
INSERT INTO QHP_type
VALUES (1, 'On Exchange');
INSERT INTO QHP_type
VALUES (2, 'Off Exchange');
INSERT INTO QHP_type
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

