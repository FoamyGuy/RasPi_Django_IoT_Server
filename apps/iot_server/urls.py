# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.iot_server import views
#from apps.iot_server.views import post_data

urlpatterns = [

    # The home page
    path('weather_dash/', views.WeatherDashView.as_view(), name='weather_dash'),
    path('post_data/', views.PostDataView.as_view(), name='post_data'),
    path('data_sources/', views.ListDataSources.as_view(), name='list_data_sources'),
    path('new_data_source/', views.NewDataSource.as_view(), name='new_data_source'),
    path('data_source/<int:data_source_id>/', views.DataSourceDetail.as_view(), name='data_source'),
    path('refresh_data_source_token/<int:data_source_id>/', views.RefreshDataSourceToken.as_view(), name='refresh_data_source_token'),
    path('download_values/<int:data_source_id>/', views.DownloadDataValues.as_view(), name="download_values")
    #path('post_data/', post_data, name='post_data')


]
