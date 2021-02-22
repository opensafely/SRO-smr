from cohortextractor import (
    codelist_from_csv
)

smr_codes = codelist_from_csv("codelists/opensafely-structured-medication-review-nhs-england.csv",
                              system="ctv3",
                              column="code",)

nhse_care_homes_codes = codelist_from_csv("codelists/opensafely-nhs-england-care-homes-residential-status.csv",
                                    system="ctv3",
                                    column="code",)

fall_codes = codelist_from_csv("codelists/opensafely-falls.csv",
                               system="ctv3",
                               column="CTV3Code",)


