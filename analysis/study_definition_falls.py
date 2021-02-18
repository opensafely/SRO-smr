

# Import functions
from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    Measure
)


# Import codelists
from codelists.codelists import *


end_date = "2021-02-01"

# Specifiy study defeinition
study = StudyDefinition(
    index_date="2019-01-01",
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": "2019-01-01", "latest": end_date},
        "rate": "exponential_increase",
        "incidence": 0.8,
    },

    #select population that have been admitted to hospital
    population=patients.satisfying(
        """
        falls
        """,


    ),

    falls=patients.with_these_clinical_events(
        fall_codes,
        returning="binary_flag",
        between=["index_date", "last_day_of_month(index_date)"],
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


    practice=patients.registered_practice_as_of(
        "index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5}, "incidence": 0.5}
    ),



)

measures = [
   

    Measure(
        id="smr_by_falls",
        numerator="had_smr_after_falls",
        denominator="population",
        group_by=['practice'],
    ),

]
