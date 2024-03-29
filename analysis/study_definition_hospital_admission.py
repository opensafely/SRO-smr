

# Import functions
from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    Measure
)


# Import codelists
from codelists import *



end_date = "2020-09-01"

# Specifiy study defeinition
study = StudyDefinition(
    index_date="2020-09-01",
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": "2020-09-01", "latest": end_date},
        "rate": "exponential_increase",
        "incidence": 0.8,
    },

    #select population that have been admitted to hospital
    population=patients.satisfying(
        """
        registered AND 
        (NOT died)
        """,
        
        
        ),



    registered=patients.registered_as_of(
        "index_date",
        return_expectations={"incidence": 0.9},
    ),
    died=patients.died_from_any_cause(
        on_or_before="index_date",
        return_expectations={"incidence": 0.1}
    ),


    hospital_admission=patients.admitted_to_hospital(
        returning="binary_flag",
        between=["index_date", "last_day_of_month(index_date)"],
        date_format='YYYY-MM-DD',
        return_expectations={"incidence": 0.2}
    ),

    

    had_smr=patients.with_these_clinical_events(
        smr_codes,
        returning="binary_flag",
        between=["index_date", "last_day_of_month(index_date)"],
        include_date_of_match=True,
        date_format='YYYY-MM-DD',
        return_expectations={"incidence": 0.2}
    ),

 

    had_hospital_admission_before_smr=patients.admitted_to_hospital(
        returning="binary_flag",
        between=["had_smr_date - 3 months", "had_smr_date"],
        date_format='YYYY-MM-DD',
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
        id="smr_by_hospital_admission",
        numerator="had_hospital_admission_before_smr",
        denominator="population",
        group_by=["practice"],
    ),

]
