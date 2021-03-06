import re
import requests
import pandas as pd
import numpy as np

#### Importing csv data files into dataframes 
df = pd.read_csv('Input_Data/education_expenditure_supplementary_data.csv')#Public and private direct expenditures on education institutions as a percentage of gross domestic product
df1 = pd.read_csv('Input_Data/educational_attainment_supplementary_data.csv')#refined list of survey questions by country 
df2 = pd.read_csv('Input_Data/school_and_country_table.csv')
df3 = pd.read_csv('Input_Data/shanghaiData.csv')
df4 = pd.read_csv('Input_Data/timesData.csv')
df_GDP = pd.read_csv('Input_Data/GDP.csv')
df_GDP2 = pd.read_csv('Input_Data/GDP.csv')

#Cleaning GDP file and averaging out years 2001 through 2011. This will help smooth out missing data and lag between school investments vs results 
df_GDP.rename({'Country Name': 'country'}, axis=1, inplace=True)
df_GDP['avg_2000_2011'] = df_GDP[['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009', '2010','2011']].mean(axis=1)
df_GDP = df_GDP[['country', 'Country Code','Indicator Name', 'Indicator Code','avg_2000_2011']]
df_GDP.dropna(subset=['avg_2000_2011'],inplace=True)
df_GDP.reset_index(inplace=True,drop=True)
df_GDP.head()

#Cleaning school expenditure file. This file is missing many countries (only has around 30)
#Filtering on school spend and creating dataframe for each by category - e.g. All, k_12, and hihger education
#We may be able to run test on all 3 of these groups 
df['institute_type'] = df['institute_type'].str.strip()
df['direct_expenditure_type'] = df['direct_expenditure_type'].str.strip()

df[['1995','2000','2005','2009','2010','2011']] = df[['1995','2000','2005','2009','2010','2011']]/100
df['school_spend_2000_2011'] = df[['2000','2005','2009', '2010','2011']].mean(axis=1)

df = df[df['direct_expenditure_type']== 'Total']
df = df[['country', 'institute_type','school_spend_2000_2011']]

df_all_edu = df[df['institute_type']=='All Institutions']
df_k_12_edu = df[df['institute_type']=='Elementary and Secondary Institutions']
df_higher_edu = df[df['institute_type']=='Higher Education Institutions']

df_all_edu = df_all_edu.dropna(subset=['school_spend_2000_2011'])
df_k_12_edu = df_k_12_edu.dropna(subset=['school_spend_2000_2011'])
df_higher_edu = df_higher_edu.dropna(subset=['school_spend_2000_2011'])

df_all_edu.reset_index(inplace=True,drop=True)
df_k_12_edu.reset_index(inplace=True,drop=True)
df_higher_edu.reset_index(inplace=True,drop=True)

df_all_edu.head()
df_k_12_edu.head()
df_higher_edu.head()

#df.institute_type.unique()


#Merging GDP and expenditure data. The column "school expenditures will be the $$$ spend on schooling"
df_all_edu_1 = df_GDP.merge(df_all_edu, on='country', how='left').dropna(subset=['school_spend_2000_2011'])
df_k_12_edu_1 = df_GDP.merge(df_k_12_edu, on='country', how='left').dropna(subset=['school_spend_2000_2011'])
df_higher_edu_1 = df_GDP.merge(df_higher_edu, on='country', how='left').dropna(subset=['school_spend_2000_2011'])

df_all_edu_1.reset_index(inplace=True,drop=True)
df_k_12_edu_1.reset_index(inplace=True,drop=True)
df_higher_edu_1.reset_index(inplace=True,drop=True)

df_all_edu_1['school_expenditures'] = round(df_all_edu_1['school_spend_2000_2011'] * df_all_edu_1['avg_2000_2011'],2)
df_k_12_edu_1['school_expenditures'] = round(df_k_12_edu_1['school_spend_2000_2011'] * df_k_12_edu_1['avg_2000_2011'],2)
df_higher_edu_1['school_expenditures'] = round(df_higher_edu_1['school_spend_2000_2011'] * df_higher_edu_1['avg_2000_2011'],2)

df_all_edu_1.head()
df_k_12_edu_1.head()
df_higher_edu_1.head()

### data cleaning the survey file to narrow in on questions we may want to take a look at. Column "series name"
df1 = df1[df1['Keep or not']==1]
df1['avg_2005_2015'] = df1[['2005', '2006','2007','2008','2009','2010','2011','2012','2013','2015']].mean(axis=1)
df1.dropna(subset=['avg_2005_2015'],inplace=True)
df1.reset_index(inplace=True,drop=True)
df1.head()


#cleaning GDP file to use again. As many countries are missing expenditures, we can just use toal GDP vs school responses as well. This will be a broader dataset with more countries.
df_GDP2.rename({'Country Name': 'country'}, axis=1, inplace=True)
df_GDP2['avg_2000_2015'] = df_GDP2[['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009', '2010','2011','2012','2013','2014','2015']].mean(axis=1)
df_GDP2 = df_GDP2[['country', 'Country Code','Indicator Name', 'Indicator Code','avg_2000_2015']]
df_GDP2.dropna(subset=['avg_2000_2015'],inplace=True)
df_GDP2.reset_index(inplace=True,drop=True)
df_GDP2.head()


# joinning survey data_sets with expenditures dataset for final data sets to beging running test on.
df1.rename({'country_name': 'country'}, axis=1, inplace=True)

complete_expenditures_all = df1.merge(df_all_edu_1, on='country', how='left').dropna(subset=['school_spend_2000_2011'])
complete_expenditures_k_12 = df1.merge(df_k_12_edu_1, on='country', how='left').dropna(subset=['school_spend_2000_2011'])
complete_expenditures_higher_edu = df1.merge(df_higher_edu_1, on='country', how='left').dropna(subset=['school_spend_2000_2011'])

#final data-set with total GDP (not expenditures) to run test on as it will have more datapoints vs above compplete tables
complete_GDP = df1.merge(df_GDP2, on='country', how='left').dropna(subset=['avg_2000_2015'])