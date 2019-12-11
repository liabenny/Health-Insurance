/**
  OPTION1: Find a Medical Plan
  INPUT:
        market coverage (required)
        plan type
        QHP type
        child only offering
        metal level
        notice for pregnancy required
        wellness program offered
  OUTPUT:
        state
        plan id
        plan name
        plan brochure url
 */
-- TODO Add some rate information
SELECT state, plan_id, plan_variant_name, url_plan_brochure
FROM plans
WHERE plan_type = 2
  AND qhp_type = 3
  AND market_coverage = 1
  AND child_only_offering = 1
  AND plan_id IN (
    SELECT medical_plans.plan_id
    FROM medical_plans
    WHERE is_wellness_program_offered = false
      AND metal_level = 3
      AND is_notice_required_for_pregnancy = false
)
ORDER BY state;

/**
  OPTION2: Find a Dental Plan
  INPUT:
        market coverage (required)
        plan type
        QHP type
        child only offering
        metal level
  OUTPUT:
        state
        plan id
        plan name
        plan brochure url
 */
SELECT state, plan_id, plan_variant_name, url_plan_brochure
FROM plans
WHERE plan_type = 2
  AND qhp_type = 3
  AND market_coverage = 1
  AND child_only_offering = 1
  AND plan_id IN (
    SELECT dental_plans.plan_id
    FROM dental_plans
    WHERE metal_level = 2
)
ORDER BY state;

/**
  OPTION2: Find State Average Individual Rate for specific age.(medical/dental)
  (can implement interactive date range)
  INPUT:
        dental/medical (required) - only for individual plan
        age (required)
        metal level (required)

  OUTPUT:
        state
        effective date
        expiration date
        average rate
 */
-- Dental Plan
SELECT state, AVG(individual_rate)
FROM rate_individual,
     (
         SELECT DISTINCT plans.std_component_id, state
         FROM dental_plans
                  JOIN plans ON dental_plans.plan_id = plans.plan_id
         WHERE metal_level = 1
     ) r1
WHERE r1.std_component_id = rate_individual.std_component_id
  AND age_range_from <= 1
  AND age_range_to >= 1
  AND effective_date = '2020-01-01'
  AND expiration_date = '2020-12-31'
GROUP BY state, effective_date, expiration_date
ORDER BY state;

-- Medical Plan
SELECT state, AVG(individual_rate)
FROM rate_individual,
     (
         SELECT DISTINCT plans.std_component_id, state
         FROM medical_plans
                  JOIN plans ON medical_plans.plan_id = plans.plan_id
         WHERE metal_level = 5
     ) r1
WHERE r1.std_component_id = rate_individual.std_component_id
  AND age_range_from <= 15
  AND age_range_to >= 15
  AND effective_date = '2020-01-01'
  AND expiration_date = '2020-12-31'
GROUP BY state, effective_date, expiration_date
ORDER BY state;


/**
  OPTION3: Individual Plan
  INPUT:
        medical/dental (required)

 */
SELECT *
FROM plans
WHERE market_coverage = 2
  AND plan_id IN (
    SELECT medical_plans.plan_id
    FROM medical_plans
);

SELECT *
FROM plans
WHERE market_coverage = 1
  AND plan_id IN (
    SELECT dental_plans.plan_id
    FROM dental_plans
);


