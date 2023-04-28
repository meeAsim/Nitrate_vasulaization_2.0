from django.db import models

import pandas as pd


# Create your models here.
#city ko naam ra overall dataset

class CityData(models.Model):
   
    data = pd.read_csv('./merged_data.csv')

    Cname = data['name'].drop_duplicates()
    
    print((Cname))

    # print(data)

    def __str__(self):
        return f'{self.Cname}'

#data and date

class myData(models.Model):
    
    city_data = pd.read_csv('./merged_data.csv', error_bad_lines=False)
    # cmdata_sort = city_data.sort_values(by='year', ascending = True, inplace=True)
    city_datas = city_data['messergebnis_c']
    city_dates = city_data['year']

pass


    
