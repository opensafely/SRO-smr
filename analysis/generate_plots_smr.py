import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from ebmdatalab import charts
from cohortextractor import Measure

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
        numerator="had_smr",
        denominator="population",
        group_by=["recent_falls"],
    ),

    Measure(
        id="smr_by_hospital_admission",
        numerator="had_smr",
        denominator="population",
        group_by=["recent_hospital_admission"],
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


if not os.path.exists('output/figures'):
    os.mkdir('output/figures')



measures_df_sex = pd.read_csv('output/measures/measure_smr_by_sex.csv')
measures_df_region = pd.read_csv(
    'output/measures/measure_smr_by_region.csv')
measures_df_age = pd.read_csv(
    'output/measures/measure_smr_by_age_band.csv')
measures_df_falls = pd.read_csv(
    'output/measures/measure_smr_by_falls.csv')
measures_df_care_home_status = pd.read_csv(
    'output/measures/measure_smr_by_care_home_status.csv')
measures_df_total = pd.read_csv(
    'output/measures/measure_smr_total.csv')
measures_df_total_by_practice = pd.read_csv(
    'output/measures/measure_smr_total_by_practice.csv')
measures_df_hospital_admission = pd.read_csv(
    'output/measures/measure_smr_by_hospital_admission.csv')

#not producing collpased csv so loop through dates and create combined df
# df_list = []
# for file in os.listdir('output/measures'):
#     if file.startswith('measure_smr_by_hospital_admission'):
#         df = pd.read_csv(os.path.join('output/measures', file))
#         date = file.split('_')[-1][:-4]
#         df['date'] = date
#         df_list.append(df)

# measures_smr_by_hospital_admission = pd.concat(df_list)


# df_list = []
# for file in os.listdir('output/measures'):
#     if file.startswith('measure_smr_by_falls'):
#         df = pd.read_csv(os.path.join('output/measures', file))
#         date = file.split('_')[-1][:-4]
#         df['date'] = date
#         df_list.append(df)

# measures_smr_by_falls = pd.concat(df_list)



# temporary fix for population not working in Measures
measures_df_total = measures_df_total.groupby(
    ['date'])['had_smr', 'population'].sum().reset_index()
measures_df_total['value'] = measures_df_total['had_smr'] / \
    measures_df_total['population']


def to_datetime_sort(df):
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by='date', inplace=True)


to_datetime_sort(measures_df_sex)
to_datetime_sort(measures_df_region)
to_datetime_sort(measures_df_age)
to_datetime_sort(measures_df_total)
to_datetime_sort(measures_df_falls)
to_datetime_sort(measures_df_care_home_status)
to_datetime_sort(measures_df_total_by_practice)
to_datetime_sort(measures_df_hospital_admission)


def redact_small_numbers(df, n, m):
    """
    Takes measures df and converts any row to nana where value of denominator or numerater in measure m equal to 
    or below n
    Returns df of same shape.
    """
    mask_n = df[m.numerator].isin(list(range(0, n+1)))
    mask_d = df[m.denominator].isin(list(range(0, n+1)))
    mask = mask_n | mask_d
    df.loc[mask, :] = np.nan
    return df


# falls_measure = Measure(
#     id="smr_by_falls",
#     numerator="had_falls_before_smr",
#     denominator="population",
#     group_by=None,
# )

# hosp_admission_measure = Measure(
#     id="smr_by_hospital_admission",
#     numerator="had_hospital_admission_before_smr",
#     denominator="population",
#     group_by=None,
# )

redact_small_numbers(measures_df_sex, 10, measures[0])
redact_small_numbers(measures_df_region, 10, measures[1])
redact_small_numbers(measures_df_age, 10, measures[2])
redact_small_numbers(measures_df_care_home_status, 10, measures[3])
redact_small_numbers(measures_df_falls, 10, measures[4])
redact_small_numbers(measures_df_hospital_admission,
                     10, measures[5])
redact_small_numbers(measures_df_total,10, measures[6])





def calculate_rate(df, value_col='had_smr', population_col='population'):
    # round value col and population to nearest 100
    df[value_col] = df[value_col].round(-2)
    df[population_col] = df[population_col].round(-2)
    num_per_thousand = df[value_col]/(df[population_col]/1000)
    # round to 4 decimal places
    num_per_thousand = num_per_thousand.round(4)
    # drop value col
    df.drop(value_col, axis=1, inplace=True)
    df['num_per_thousand'] = num_per_thousand


calculate_rate(measures_df_sex)
calculate_rate(measures_df_age)
calculate_rate(measures_df_region)
calculate_rate(measures_df_total)
calculate_rate(measures_df_falls)
calculate_rate(measures_df_care_home_status)
calculate_rate(measures_df_total_by_practice)
calculate_rate(measures_df_hospital_admission)

#https://github.com/opensafely/hospital-disruption-research/blob/master/analysis/rate_calculations.py


#Remove U/T in sex column
measures_df_sex = measures_df_sex[measures_df_sex['sex'].isin(["F", "M"])]

#Remove default age band
measures_df_age = measures_df_age[~measures_df_age['age_band'].isin(["0"])]

def plot_measures(df, title, filename, column_to_plot, category=False, y_label='Rate per 1000'):

    if category:
        for unique_category in df[category].unique():

            df_subset = df[df[category] == unique_category]

            plt.plot(df_subset['date'], df_subset[column_to_plot], marker='o')
    else:
        plt.plot(df['date'], df[column_to_plot], marker='o')

    plt.ylabel(y_label)
    plt.xlabel('Date')
    plt.xticks(rotation='vertical')
    plt.title(title)

    if category:
        plt.legend(df[category].unique(), bbox_to_anchor=(
            1.04, 1), loc="upper left")

    else:
        pass

    plt.savefig(f'output/figures/{filename}.jpeg', bbox_inches='tight')

    plt.clf()

# cut jan data to align with other charts

measures_df_total = measures_df_total.loc[measures_df_total['date'] < '2021-01-01',:]
measures_df_total_by_practice = measures_df_total_by_practice.loc[measures_df_total_by_practice['date'] < '2021-01-01',:]
measures_df_total.to_csv('output/measures/measures_df_total_for_plot.csv')


plot_measures(measures_df_total, 'SMR use across Whole Population',
              'population_rates', 'had_smr', category=False, y_label='Total Number')

plot_measures(measures_df_sex,
              'SMR use by Sex per 1000', 'sex_rates', 'num_per_thousand', category='sex', )
plot_measures(measures_df_region,
              'SMR use by Region per 1000', 'region_rates', 'num_per_thousand', category='region')
plot_measures(measures_df_age,
              'SMR use by Age Band per 1000',  'age_rates', 'num_per_thousand', category='age_band')


plot_measures(measures_df_care_home_status,
              'SMR use by care home status per 1000',  'care_home_status_rates', 'num_per_thousand', category='care_home_status')

plot_measures(measures_df_falls,
              'SMR use by falls status per 1000',  'falls_rates', 'num_per_thousand', category='recent_falls')


plot_measures(measures_df_hospital_admission,
              'SMR use by hospital_admission status per 1000',  'hospital_admission_rates', 'num_per_thousand', category='recent_hospital_admission')



smr_decile_chart = charts.deciles_chart(
    measures_df_total_by_practice,
    period_column="date",
    column="num_per_thousand",
    title="SMR by practice",
    ylabel="rate per 1000",
    show_outer_percentiles=False,
    show_legend=True,
)
plt.savefig(f'output/figures/smr_decile_chart.jpeg', bbox_inches='tight')
plt.clf()

# smr_decile_chart_falls = charts.deciles_chart(
#     measures_df_total_by_practice,
#     period_column="date",
#     column="value",
#     title="Recent falls in those with SMR",
#     ylabel="proportion",
#     show_outer_percentiles=False,
#     show_legend=True,
# )

# plt.savefig(f'output/figures/smr_decile_chart_falls.jpeg', bbox_inches='tight')
# plt.clf()

# smr_decile_chart_hospital_admission = charts.deciles_chart(
#     measures_smr_by_hospital_admission,
#     period_column="date",
#     column="value",
#     title="Recent hospitalisation in those with smr by practice",
#     ylabel="Proportion",
#     show_outer_percentiles=False,
#     show_legend=True,
# )

# plt.savefig(f'output/figures/smr_decile_chart_hospital_admission.jpeg', bbox_inches='tight')
# plt.clf()
