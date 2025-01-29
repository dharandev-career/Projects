#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np


# In[3]:


df = pd.read_csv('Assignment1Data_Sample.csv')
df


# In[4]:


df.info()


# In[5]:


required_fields = [
    'Object ID', 'Department', 'Object Name', 'Title', 
    'Culture', 'Artist Nationality', 'Object Begin Date', 
    'Object End Date', 'Medium', 'Credit Line', 'Country'
]


# In[6]:


# Select only the required fields and store in dataframe
df_clean = df[required_fields].copy()
df_clean


# In[7]:


# Entering into Log
log_file = open('Assignment1_log.txt', 'w')


# In[8]:


#Data types of data
df_clean.dtypes


# In[9]:


# Shape of data
df_clean.shape


# In[10]:


pd.isnull(df_clean)


# In[12]:


# Getting in percentage of null values in columns
for col in df_clean.columns:
    pct_missing = np.mean(df_clean[col].isnull())
    if pct_missing >=0.20:
        print('{} - {}%'.format(col, round(pct_missing*100)))
        log_file.write(f'Percentage of null values in columns:\n{col}\n\n')


# In[13]:


# 2. Handling missing values and Replacing values in Culture, Country and Artist Nationality 

missing_country = df_clean[df_clean['Country'].isnull()]
log_file.write(f'Missing Country values before handling:\n')

df_clean['Country'].fillna(df_clean['Culture'], inplace=True)
df_clean['Country'].fillna(df_clean['Artist Nationality'], inplace=True)
df_clean['Country'].fillna('Unknown', inplace=True)
log_file.write(f'Filled missing Country values with "Unknown"\n\n')

missing_artist_nationality = df_clean[df_clean['Artist Nationality'].isnull()]
log_file.write(f'Missing Artist Nationality values before handling:\n')

df_clean['Artist Nationality'].fillna(df_clean['Country'], inplace=True)
df_clean['Artist Nationality'].fillna(df_clean['Culture'], inplace=True)
df_clean['Artist Nationality'].fillna('Unknown', inplace=True)
log_file.write(f'Filled missing Country values with "Unknown"\n\n')


df_clean['Culture'].fillna('Unknown', inplace=True)
log_file.write(f'Filled missing Culture values with "Unknown"\n\n')


df_clean


# In[15]:


# 3. Inconsistent_dates and Replacing dates

inconsistent_dates = df_clean[df_clean['Object Begin Date'] > df_clean['Object End Date']]
log_file.write(f'Inconsistent dates:\n{inconsistent_dates}\n\n')

# Drop inconsistent dates
df_clean = df_clean[df_clean['Object Begin Date'] <= df_clean['Object End Date']]

#Replacing decimal
df_clean.loc[:, 'Object End Date'] = df_clean['Object End Date'].astype(str).str.replace('.0', '').astype(int)
df_clean


# In[16]:


# 4. Irrelevant Columns are removed

irrelevant_columns = [col for col in required_fields if col not in df.columns]
if irrelevant_columns:
    df_clean.drop(columns=irrelevant_columns, inplace=True)
    log_file.write(f'Removed irrelevant columns:\n{irrelevant_columns}\n\n')
df_clean


# In[18]:


# 5. Duplicate records are checked and removed Because Object ID is Unique

duplicate_records = df_clean[df_clean.duplicated(subset='Object ID', keep=False)]
log_file.write(f'Duplicate records:\n{duplicate_records}\n\n')

# Remove duplicate records
df_clean = df_clean.drop_duplicates(subset='Object ID', keep='first')
log_file.write(f'Removed Duplicates\n\n')


# In[20]:


# 6.Outlier condition here is Object Begin date from = 1000 to Object End Date = 2024


outlier_condition = (df_clean['Object Begin Date'] < 1000) | (df_clean['Object End Date'] > 2024)
outliers = df_clean[outlier_condition]
log_file.write(f'Outliers:\n{outliers}\n\n')
df_clean = df_clean[~outlier_condition]
df_clean


# In[21]:


# 7. Handling string capitalization

string_fields = ['Object Name', 'Title', 'Medium', 'Credit Line']
for field in string_fields:
    df_clean.loc[:, field] = df_clean[field].str.title()
df_clean


# In[22]:


# Store cleaned data in csv file
df_clean.to_csv('Cleaned_data.csv', index=False)


# In[23]:


# Closing Log

log_file.close()


# In[ ]:




