from cohortextractor import (
    codelist_from_csv
)

smr_codes = codelist_from_csv("codelists/opensafely-structured-medication-review-nhs-england.csv",
                              system="snomed",
                              column="code",)

care_home_codes = codelist_from_csv("codelists/opensafely-nhs-england-care-homes-residential-status.csv",
                                    system="snomed",
                                    column="code",)

fall_codes = codelist_from_csv("codelists/opensafely-falls.csv",
                               system="ctv3",
                               column="CTV3Code",)


