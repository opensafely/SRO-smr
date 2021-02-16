

# Import functions
from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    Measure
)


# Import codelists
from codelists.codelists import *


start_date = "2019-01-01"
end_date = "today"

# Specifiy study defeinition
study = StudyDefinition(
    index_date="2019-01-01",
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "exponential_increase",
        "incidence": 0.8,
    },

    #select population that have been admitted to hospital
    population=patients.satisfying(
        """
        hospital_admission
        """,
        
        
        ),

    
    hospital_admission_date=patients.admitted_to_hospital(
        returning="date_admitted",
        date_format='YYYY-MM-DD',
        return_expectations={"incidence": 1},
        between=[start_date, end_date]
    ),
    
    hospital_discharged_date=patients.admitted_to_hospital(
        returning="date_discharged",
        date_format='YYYY-MM-DD',
        return_expectations={"incidence": 1},
        between=[start_date, end_date]
    ),

    #hospital admission that was not day case
    #discharge date occur more >=1 after admission
    hospital_admission=patients.admitted_to_hospital(
        returning="binary_flag",
        return_expectations={"incidence": 0.2},
        between=["hospital_admission_date + 1 day",
                 "hospital_admission_date + 1 month"]
    ),


    had_smr_after_hospital_admission = patients.with_these_clinical_events(
        smr_codes,
        returning="binary_flag",
        between=["hospital_discharged_date",
                 "hospital_discharged_date + 3 months"],
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
        numerator="had_smr_after_hospital_admission",
        denominator="population",
        group_by=["practice"],
    ),

]
