import sys
import pandas as pd
import matplotlib.pyplot as plt
import os

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
measures_df_hosp_adm = pd.read_csv(
    'output/measures/measure_smr_by_hospital_admission.csv')
measures_df_total = pd.read_csv(
    'output/measures/measure_smr_total.csv')


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
to_datetime_sort(measures_df_hosp_adm)
to_datetime_sort(measures_df_falls)
to_datetime_sort(measures_df_care_home_status)


def calculate_rate(df, value_col='had_smr', population_col='population'):
    num_per_hundred_thousand = df[value_col]/(df[population_col]/100000)
    df['num_per_hundred_thousand'] = num_per_hundred_thousand


calculate_rate(measures_df_sex)
calculate_rate(measures_df_age)
calculate_rate(measures_df_region)
calculate_rate(measures_df_total)
calculate_rate(measures_df_hosp_adm)
calculate_rate(measures_df_falls)
calculate_rate(measures_df_care_home_status)


def plot_measures(df, title, filename, column_to_plot, category=False, y_label='Number per 100, 000'):

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
              'SMR use by Sex per 100, 000', 'sex_rates', 'num_per_hundred_thousand', category='sex', )
plot_measures(measures_df_region,
              'SMR use by Region per 100, 000', 'region_rates', 'num_per_hundred_thousand', category='region')
plot_measures(measures_df_age,
              'SMR use by Age Band per 100, 000',  'age_rates', 'num_per_hundred_thousand', category='age_band')


plot_measures(measures_df_care_home_status,
              'SMR use by care home status per 100, 000',  'care_home_status_rates', 'num_per_hundred_thousand', category='care_home_status')
plot_measures(measures_df_falls,
              'SMR use by fall status per 100, 000',  'falls_rates', 'num_per_hundred_thousand', category='falls')

plot_measures(measures_df_hosp_adm,
              'SMR use following recent hospital admision',  'hosp_adm_rates', 'num_per_hundred_thousand', category='hospital_admission')
