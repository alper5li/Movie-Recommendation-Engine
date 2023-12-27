import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df1 = pd.read_csv("C:\\Users\\alper\\Desktop\\dataset\\title.basics.tsv\\data.tsv", delimiter='\t', encoding='utf-8', low_memory=False)

df1.head()

df2 = pd.read_csv("C:\\Users\\alper\\Desktop\\dataset\\title.ratings.tsv\\data.tsv", delimiter='\t', encoding='utf-8')

df2.head()

merged_data = pd.merge(df1, df2, on='tconst')

merged_data.head()

merged_data

filtered_data = merged_data[merged_data['titleType'] == 'movie']

filtered_data.head()

merged_data['startYear'] = pd.to_numeric(merged_data['startYear'], errors='coerce')

filtered_data = merged_data[(merged_data['titleType'] == 'movie') & (merged_data['startYear'].notna()) & (merged_data['startYear'] >= 1990)]

filtered_data['startYear'] = filtered_data['startYear'].astype(int, errors='ignore')

filtered_data.head()

filtered_data.drop(['primaryTitle', 'endYear', 'runtimeMinutes'], axis=1, inplace=True)

filtered_data.head()

filtered_data = filtered_data[filtered_data['genres'] != '\\N']

filtered_data.head()

print(filtered_data.describe())

# Rating dağılımını görselleştir
plt.hist(filtered_data['averageRating'])
plt.xlabel('averageRating')
plt.ylabel('Film Sayısı')
plt.title('Rating Dağılımı')
plt.show()

kategori_counts = filtered_data['genres'].value_counts()
print(kategori_counts)

correlation_matrix = filtered_data.corr()
print(correlation_matrix)

filtered_data.isnull().sum()

filtered_data = pd.get_dummies(filtered_data, columns=['genres'])

# df, değiştirdiğiniz DataFrame'in adı olsun
filtered_data.to_csv('new_data.csv', index=False)