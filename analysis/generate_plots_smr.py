import sys
import pandas as pd
import matplotlib.pyplot as plt
import os
from ebmdatalab import charts

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
# measures_smr_by_hospital_admission = pd.read_csv(
#     'output/measures/measure_smr_by_hospital_admission.csv')



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
# to_datetime_sort(measures_smr_by_hospital_admission)

def calculate_rate(df, value_col='had_smr', population_col='population'):
    num_per_thousand = df[value_col]/(df[population_col]/1000)
    df['num_per_thousand'] = num_per_thousand


calculate_rate(measures_df_sex)
calculate_rate(measures_df_age)
calculate_rate(measures_df_region)
calculate_rate(measures_df_total)
# calculate_rate(measures_df_falls, value_col='had_smr_after_falls')
calculate_rate(measures_df_care_home_status)
calculate_rate(measures_df_total_by_practice)
# calculate_rate(measures_smr_by_hospital_admission, value_col='had_smr_after_hospital_admission')


def plot_measures(df, title, filename, column_to_plot, category=False, y_label='Rate per 1000'):

    if category:
        for unique_category in df[category].unique():

            df_subset = df[df[category] == unique_category]

            plt.plot(df_subset['date'], df_subset[column_to_plot])
    else:
        plt.plot(df['date'], df[column_to_plot])

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

smr_decile_chart_falls = charts.deciles_chart(
    measures_df_total_by_practice,
    period_column="date",
    column="num_per_thousand",
    title="SMR in those with recent falls by practice",
    ylabel="rate per 1000",
    show_outer_percentiles=False,
    show_legend=True,
)

plt.savefig(f'output/figures/smr_decile_chart_falls.jpeg', bbox_inches='tight')
plt.clf()

# smr_decile_chart_hospital_admission = charts.deciles_chart(
#     measures_smr_by_hospital_admission,
#     period_column="date",
#     column="num_per_thousand",
#     title="SMR in those hospitalised by practice",
#     ylabel="rate per 1000",
#     show_outer_percentiles=False,
#     show_legend=True,
# )

# plt.savefig(f'output/figures/smr_decile_chart_hospital_admission.jpeg', bbox_inches='tight')
# plt.clf()
