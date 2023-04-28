from django.shortcuts import render
import pandas as pd
from .models import CityData 
from .models import myData
from datetime import datetime
import plotly.express as plot
import json
import utm

# Create your views here.
def index(request):
    mydata = CityData.Cname
    context = {
        'data': mydata,
    }
    return render(request,'dashboard/index.html', context)


def district(request):
    district = str(request.POST['dist'])
    print(f'This is on the Post{district}')
    kleveCityList = CityData.Cname.loc[CityData.data['district'] == district]
    main= pd.read_csv('./merged_data.csv')
    sts = main.describe()

    json_data = sts.reset_index().to_json(orient ='records')
    myjson = json_data
    data = []
    data = json.loads(myjson)
    # print(data)
    context = {
        'list' : kleveCityList,
        'data' : data,
        'district': district
    }
    return render(request,'dashboard/dist_sel.html', context)




def visual(request):
    city2 = str(request.POST['city'])
    kleveValue = myData.city_datas.loc[myData.city_data['name'] == city2] 
    kleveDate = myData.city_dates.loc[myData.city_data['name'] == city2]
    # kleveDate = kleveDate.str.replace("00:00:00", " " )

    # sortig on range 1984-1994 

    kleveData_1984 = kleveDate.loc[(kleveDate <= "1994-12-31")]
    
    # sortig on range 1984-1994 

    kleveData_1995 = kleveDate.loc[(kleveDate >= "1995-01-01")]
    kleveData_1995 = kleveData_1995.loc[(kleveData_1995 <= "2005-12-31")]

    
    # # # sortig on range 1984-1994 

    kleveData_2006 = kleveDate.loc[(kleveDate >= "2006-01-01")]
    kleveValue_2006 = kleveData_2006.loc[kleveData_2006.between('2006-01-01', '2021-01-01')]


    cleanTime_list = CityData.data['year']

    
    # CityData.data.sort_values(by='year', inplace=True)
    # CityData.data['datum_pn'] = CityData.data['year'].str.replace("00:00:00", " " )
    
    # mesDate = CityData.data['messergebnis_c'].loc[CityData.data['name']== city2]
    # conClusion = CityData.data['messergebnis_cm'].loc[CityData.data['name']== city2]
   
   
    #for table data in json
    main_json = CityData.data.loc[CityData.data['name']== city2]
    json_data = main_json.reset_index().to_json(orient ='records')
    myjson = json_data
    data = []
    data = json.loads(myjson)



    kleveCityDataa = {
        'city' : city2,
        'cdata' : kleveDate,
        'value' : kleveValue,
        # 'newdata': mesDate,
        # 'conclu' : conClusion,
        'cdate' : cleanTime_list,
        'tab_data' : data,
        'c1data': kleveData_1984,
        'c2data': kleveData_1995,
        'c3data': kleveData_2006,
        'value06': kleveValue
        

        
        
    } 
    return render(request, 'dashboard/visualize.html', kleveCityDataa )



def map(request):
   
    data = pd.read_csv('./merged_data.csv')
    def getUTMs(row):
        tup = utm.to_latlon(row.iloc[0],row.iloc[1], 32, 'U')
        return pd.Series(tup[:2])

    data[['lat','long']] = data[['e32','n32']].apply(getUTMs , axis=1)
    fig = plot.scatter_geo(data, lat='lat', lon='long', hover_name='name')
    fig = plot.scatter_mapbox(
    data,  
    lat='lat',
    lon='long',
    center={"lat": 51.6615158, "lon": 6.454320}, 
    width=1024,  
    height=720,  
    color='messergebnis_c',
    hover_data=["name"],  
    
        )

    fig.update_layout(mapbox_style="open-street-map")

    fig.show()
   
    map = {
        'map':fig
    }

    return render(request, 'dashboard/map.html',map)








 