

# Import functions
from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    Measure
)



# Import codelists
from codelists.codelists import *



# Specifiy study defeinition
study = StudyDefinition(
    index_date = "2019-01-01",
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "exponential_increase",
        "incidence": 0.8,
    },

    population=patients.registered_as_of(start_date),
    
    # had_smr_date=patients.with_these_clinical_events(
    #     smr_codes,
    #     returning="date",
    #     between=[start_date, end_date],
    #     date_format='YYYY-MM-DD',
    #     return_expectations={"incidence": 0.2}
    # ),

    had_smr=patients.with_these_clinical_events(
        smr_codes,
        returning="binary_flag",
        between=[start_date, end_date],
        include_date_of_match=True,
        date_format='YYYY-MM-DD',
        return_expectations={"incidence": 0.2}
    ),




    care_home_status=patients.with_these_clinical_events(
        nhse_care_homes_codes,
        returning="binary_flag",
        between=[start_date, end_date],
        return_expectations={"incidence": 0.2}
    ),


    
    falls= patients.with_these_clinical_events(
        fall_codes,
        returning="binary_flag",
        between=[start_date, end_date],
        include_date_of_match=True,
        date_format='YYYY-MM-DD',
        return_expectations={"incidence": 0.2}
    ),

    had_smr_after_falls=patients.with_these_clinical_events(
        smr_codes,
        returning="binary_flag",
        between=["falls_date",
                 "falls_date + 3 months"],
        return_expectations={"incidence": 0.2}
    ),



    region=patients.registered_practice_as_of(
        start_date,
        returning="nuts1_region_name",
        return_expectations={"category": {"ratios": {
            "North East": 0.1,
            "North West": 0.1,
            "Yorkshire and the Humber": 0.1,
            "East Midlands": 0.1,
            "West Midlands": 0.1,
            "East of England": 0.1,
            "London": 0.2,
            "South East": 0.2, }}}
    ),

    age=patients.age_as_of(
        start_date,
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),

    age_band=patients.categorised_as(
        {
            "0": "DEFAULT",
            "0-19": """ age >= 0 AND age < 20""",
            "20-29": """ age >=  20 AND age < 30""",
            "30-39": """ age >=  30 AND age < 40""",
            "40-49": """ age >=  40 AND age < 50""",
            "50-59": """ age >=  50 AND age < 60""",
            "60-69": """ age >=  60 AND age < 70""",
            "70-79": """ age >=  70 AND age < 80""",
            "80+": """ age >=  80 AND age < 120""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0-19": 0.125,
                    "20-29": 0.125,
                    "30-39": 0.125,
                    "40-49": 0.125,
                    "50-59": 0.125,
                    "60-69": 0.125,
                    "70-79": 0.125,
                    "80+": 0.125,
                }
            },
        },

    ),


    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),

    practice=patients.registered_practice_as_of(
        start_date,
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5}, "incidence": 0.5}
    ),


)

measures = [
    Measure(
        id="smr_by_sex",
        numerator="had_smr",
        denominator="population",
        group_by=["sex"],
    ),

    Measure(
        id="smr_by_region",
        numerator="had_smr",
        denominator="population",
        group_by=["region"],
    ),

    Measure(
        id="smr_by_age_band",
        numerator="had_smr",
        denominator="population",
        group_by=["age_band"],
    ),

    Measure(
        id="smr_by_care_home_status",
        numerator="had_smr",
        denominator="population",
        group_by=["care_home_status"],
    ),

    Measure(
        id="smr_by_falls",
        numerator="had_smr_after_falls",
        denominator="population",
        group_by=["had_smr_after_falls"],
    ),


    Measure(
        id="smr_total",
        numerator="had_smr",
        denominator="population",
        group_by=None,
    ),

    Measure(
        id="smr_total_by_practice",
        numerator="had_smr",
        denominator="population",
        group_by=["practice"],
    ),
]

