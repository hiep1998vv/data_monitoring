from django.urls import path
from . import views

urlpatterns = [

    path('today/', views.plot_liveOPR_byday, name= 'today'),
    path('thismonth/', views.plotview, name= 'thismonth'),
    # path('', views.plotKMK, name= 'KMK'),
    # path('load-line/', views.load_Line, name='ajax_load_Line'),
    # path('realtime/', views.realtime, name='ajax_load_realtime'),
    # path('ajax_download_rawdata/', views.ajax_download_rawdata, name='ajax_download_rawdata'),
    
    ]