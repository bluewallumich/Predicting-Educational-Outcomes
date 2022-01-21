# This quick program cleans the following inconsistencies in the dataframe.
# If additional data sources are added, please note the changes needed and
# add them to the dictionary as old_value:cleaned_value pairs.

# 'Unted Kingdom' to 'United Kingdom'
# 'Unisted States of America' to 'United States of America'
# 'Egypt, Arab Rep.' to 'Egypt'
# 'United States' to 'United States of America'
# 'USA' to 'United States of America'
# 'Russia' to 'Russian Federation'
# 'Slovak Republic' to 'Slovakia'
# 'Iran, Islamic Rep.' to 'Iran'
# 'Korea, Rep.' to 'South Korea'
# 'Korea, Republic of' to 'South Korea'
# '  Russian Federation' to 'Russian Federation'
# '  Brazil' to 'Brazil'

# To run this cleaner,
# from country_cleaner import country_clean
# df[country_column] = df[country_column].apply(lambda x: country_clean(x))

import pandas as pd

repl_dict = {'Unted Kingdom': 'United Kingdom',
  'Unisted States of America': 'United States of America',
  'United States':'United States of America',
  'Egypt, Arab Rep.': 'Egypt',
  'USA': 'United States of America',
  'Russia': 'Russian Federation',
  'Slovak Republic': 'Slovakia',
  'Iran, Islamic Rep.': 'Iran',
  'Korea, Rep.': 'South Korea',
  'Korea, Republic of': 'South Korea',
  '  Russian Federation': 'Russian Federation',
  '  Brazil': 'Brazil'}
def country_clean(country):
    if country in repl_dict.keys():
        output = repl_dict[country]
    else:
        output = country
    return output