from django.urls import path
from .import views

urlpatterns =[
   path('',views.index, name='dashboard-index'),
   path('home',views.index, name='dashboard-index'),
   path('kleve',views.district, name='dashboard-dist_sel'),
   path('wesel',views.district, name='dashboard-dist_sel'),
   path('visualKleve',views.visual, name='dashboard-visulize'),
    path('map',views.map, name='dashboard-map'),
]