import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read data from file
    with open('adult.data.csv', 'r') as f:
      df = pd.read_csv(f, header = 0)
    
    # print (df.dtypes)
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    # find unique races
    race_count = df['race'].value_counts()

    # What is the average age of men?
    men_df = df[df['sex'] == 'Male']
    average_age_men = (men_df['age'].mean()).round(decimals=1)

    # What is the percentage of people who have a Bachelor's degree?
    education_count = df['education'].value_counts(normalize=True)
    percentage_bachelors = (education_count['Bachelors'] * 100).round(decimals=1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[df['education'].isin(['Bachelors', 'Masters','Doctorate'])]
    lower_education = df[~df['education'].isin(['Bachelors', 'Masters','Doctorate'])]

    # percentage with salary >50K
    higher_education_rich = (higher_education['salary'].value_counts(normalize=True)['>50K'] * 100).round(decimals=1)
    lower_education_rich = (lower_education['salary'].value_counts(normalize=True)['>50K'] * 100).round(decimals=1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[df['hours-per-week'] == 1]

    rich_percentage = (num_min_workers['salary'].value_counts(normalize=True)['>50K'] * 100).round(decimals=0)

    # What country has the highest percentage of people that earn >50K?
    df_by_country = df.groupby('native-country')
    percent_rich_by_country = pd.Series(dtype = 'int32')
    for country, data in df_by_country:
      sorted_by_salary = data['salary'].value_counts(normalize=True)
      percent_rich_by_country[country] = ((1 - sorted_by_salary['<=50K']) * 100).round(decimals=1)
    highest_earning_country = percent_rich_by_country.idxmax()
    highest_earning_country_percentage = percent_rich_by_country.max()

    # Identify the most popular occupation for those who earn >50K in India.
    india_data = df_by_country.get_group('India')
    in_df_by_occ = india_data.groupby('occupation')
    rich_by_occupation_india = pd.Series(dtype = 'int32')
    for occupation, data in in_df_by_occ:
      salary_counts = data['salary'].value_counts()
      if '>50K' in salary_counts.index:
        rich_by_occupation_india[occupation] = salary_counts['>50K']
      else:
        rich_by_occupation_india[occupation] = 0

    top_IN_occupation = rich_by_occupation_india.idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

if __name__ == '__main__':
  calculate_demographic_data()
