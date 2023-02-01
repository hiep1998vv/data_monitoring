from django.shortcuts import render
from tkinter import messagebox
from django.http import request
from django.shortcuts import render, redirect
from collections import Counter
import matplotlib.pyplot as plt
# import mpld3
# from mpld3._server import serve
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse

# from dashboard.test import dataTable
from . import models
# from . import forms
from datetime import datetime
import datetime
from datetime import date, timedelta
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from plotly.offline import plot
import plotly
import calendar
from .models import GetLine, GetModel, get_rib
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from  .models import DTModel
from django import forms
from django.template import loader
from django.http import JsonResponse
from django.contrib import messages
import json
# Create your views here.


#----------------------------------------FUNCTION TO TEST INPUT VALUE KMK-----------------
#-----------------------------------------------------------------------------------------

# ModelId = ''
# LineId = ''
# ProcessId = ''

# def check_rib(model, rib):
#     data = get_rib(model)
#     if rib in data:
#         return True
#     else:
#         return False


# def index(request):
#     Model = GetModel()
   
#     d = {
#         'Model': Model
#         }
#     return render(request,'OPR/index.html',d)

# def load_Line(request):
#     global ModelId
#     #print(request.GET.get('time_start'))
#     #print(request.GET.get('date_start'))
#     ModelId = request.GET.get('ModelId')
#     #print(ModelId)
#     Line = GetLine(ModelId)
#     rib = get_rib(ModelId)
#     return render(request, 'dashboard/Line_dropdown_list_options.html', {'Line': Line, 'rib':rib})




def Get_start_final_dayofmonth():
    
    currentMonth = datetime.datetime.now().month
    currentYear = datetime.datetime.now().year
    lastday = calendar.monthrange(currentYear, currentMonth)[1]
    month =''
    if (currentMonth < 10):
        month = "0" + str(currentMonth)
    else:
        month = str(currentMonth)

    return [str(currentYear) + '-'+ str(month) +'-01', str(currentYear) + '-'+ str(month) +'-'+ str(lastday)]
    

def plotview(request):

    if request.method == "GET":
        now = datetime.datetime.now()
        current_time = str(now.strftime("%H:%M") )
        enddate = Get_start_final_dayofmonth()[1]
        startdate = Get_start_final_dayofmonth()[0]

        OPR_F58 = models.VisualizeData(startdate,enddate,'F58').visualize_ModelBymonth()
        graph_OPR_F58 = OPR_F58[0] 
        graph_bar_F58 = OPR_F58[1]
        graph_wit_F58 = models.VisualizeData(startdate,enddate,'F58').visualize_WorstItem_bymonth()

        OPR_F36 = models.VisualizeData(startdate,enddate,'F36').visualize_ModelBymonth()
        graph_OPR_F36 = OPR_F36[0] 
        graph_bar_F36 = OPR_F36[1]
        graph_wit_F36 = models.VisualizeData(startdate,enddate,'F36').visualize_WorstItem_bymonth()

        OPR_F37 = models.VisualizeData(startdate,enddate,'F37').visualize_ModelBymonth()
        graph_OPR_F37 = OPR_F37[0] 
        graph_bar_F37 = OPR_F37[1]
        graph_wit_F37 = models.VisualizeData(startdate,enddate,'F37').visualize_WorstItem_bymonth()

        OPR_F38 = models.VisualizeData(startdate,enddate,'F38').visualize_ModelBymonth()
        graph_OPR_F38 = OPR_F38[0] 
        graph_bar_F38 = OPR_F38[1]
        graph_wit_F38 = models.VisualizeData(startdate,enddate,'F38').visualize_WorstItem_bymonth()

        OPR_G29 = models.VisualizeData(startdate,enddate,'G29').visualize_ModelBymonth()
        graph_OPR_G29 = OPR_G29[0]
        graph_bar_G29 = OPR_G29[1]
        graph_wit_G29 = models.VisualizeData(startdate,enddate,'G29').visualize_WorstItem_bymonth()

        OPR_G10 = models.VisualizeData(startdate,enddate,'G10').visualize_ModelBymonth()
        graph_OPR_G10 = OPR_G10[0] 
        graph_bar_G10 = OPR_G10[1]
        graph_wit_G10 = models.VisualizeData(startdate,enddate,'G10').visualize_WorstItem_bymonth()

        OPR_G12 = models.VisualizeData(startdate,enddate,'G12').visualize_ModelBymonth()
        graph_OPR_G12 = OPR_G12[0] 
        graph_bar_G12 = OPR_G12[1]
        graph_wit_G12 = models.VisualizeData(startdate,enddate,'G12').visualize_WorstItem_bymonth()

        OPR_G14 = models.VisualizeData(startdate,enddate,'G14').visualize_ModelBymonth()
        graph_OPR_G14 = OPR_G14[0] 
        graph_bar_G14 = OPR_G14[1]
        graph_wit_G14 = models.VisualizeData(startdate,enddate,'G14').visualize_WorstItem_bymonth()

        OPR_G15 = models.VisualizeData(startdate,enddate,'G15').visualize_ModelBymonth()
        graph_OPR_G15 = OPR_G15[0] 
        graph_bar_G15 = OPR_G15[1]
        graph_wit_G15 = models.VisualizeData(startdate,enddate,'G15').visualize_WorstItem_bymonth()
        
        context = {
        
     
        "graph_OPR_F58" : graph_OPR_F58,
        "graph_bar_F58" : graph_bar_F58,
        "graph_wit_F58" : graph_wit_F58,

        "graph_OPR_F36" : graph_OPR_F36,
        "graph_bar_F36" : graph_bar_F36,
        "graph_wit_F36" : graph_wit_F36,

        "graph_OPR_F37" : graph_OPR_F37,
        "graph_bar_F37" : graph_bar_F37,
        "graph_wit_F37" : graph_wit_F37,

        "graph_OPR_F38" : graph_OPR_F38,
        "graph_bar_F38" : graph_bar_F38,
        "graph_wit_F38" : graph_wit_F38,

        "graph_OPR_G29" : graph_OPR_G29,
        "graph_bar_G29" : graph_bar_G29,
        "graph_wit_G29" : graph_wit_G29,

        "graph_OPR_G10" : graph_OPR_G10,
        "graph_bar_G10" : graph_bar_G10,
        "graph_wit_G10" : graph_wit_G10,
        
        "graph_OPR_G12" : graph_OPR_G12,
        "graph_bar_G12" : graph_bar_G12,
        "graph_wit_G12" : graph_wit_G12,
        
        "graph_OPR_G14" : graph_OPR_G14,
        "graph_bar_G14" : graph_bar_G14,
        "graph_wit_G14" : graph_wit_G14,

        "graph_OPR_G15" : graph_OPR_G15,
        "graph_bar_G15" : graph_bar_G15,
        "graph_wit_G15" : graph_wit_G15,

        

        "time_update": current_time,

        }
        return render(request, 'OPR/thismonth.html', context)



def return_value_from_dict(data):   # function change dict data to list data
    listkey = list(data.keys())
    listvalue = []
    for key in listkey:
        listvalue.append(data[key])
    return [listkey, listvalue]

def plot_liveOPR_byday(request):
    
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")


    if request.method == "GET":
        
        OPR_F58 = models.VisualizeData('2022-07-01', '2022-07-01', 'F58').OPR_today()
        graphbar_OPR_F58 = OPR_F58[0]
        graph_OPR_F58_bydate = OPR_F58[1]
        Graph_Wit_F58 = models.VisualizeData('2022-07-01', '2022-07-01', 'F58').visualize_WorstItem_today()

        OPR_F36 = models.VisualizeData('2022-07-01', '2022-07-01', 'F36').OPR_today()
        graphbar_OPR_F36 = OPR_F36[0]
        graph_OPR_F36_bydate = OPR_F36[1]
        Graph_Wit_F36 = models.VisualizeData('2022-07-01', '2022-07-01', 'F36').visualize_WorstItem_today()

        OPR_G29 = models.VisualizeData('2022-07-01', '2022-07-01', 'G29').OPR_today()
        graphbar_OPR_G29 = OPR_G29[0]
        graph_OPR_G29_bydate = OPR_G29[1]
        Graph_Wit_G29 = models.VisualizeData('2022-07-01', '2022-07-01', 'G29').visualize_WorstItem_today()

        OPR_G10 = models.VisualizeData('2022-07-01', '2022-07-01', 'G10').OPR_today()
        graphbar_OPR_G10 = OPR_G10[0]
        graph_OPR_G10_bydate = OPR_G10[1]
        Graph_Wit_G10 = models.VisualizeData('2022-07-01', '2022-07-01', 'G10').visualize_WorstItem_today()

        OPR_G12 = models.VisualizeData('2022-07-01', '2022-07-01', 'G12').OPR_today()
        graphbar_OPR_G12 = OPR_G12[0]
        graph_OPR_G12_bydate = OPR_G12[1]
        Graph_Wit_G12 = models.VisualizeData('2022-07-01', '2022-07-01', 'G12').visualize_WorstItem_today()

        OPR_G14 = models.VisualizeData('2022-07-01', '2022-07-01', 'G14').OPR_today()
        graphbar_OPR_G14 = OPR_G14[0]
        graph_OPR_G14_bydate = OPR_G14[1]
        Graph_Wit_G14 = models.VisualizeData('2022-07-01', '2022-07-01', 'G14').visualize_WorstItem_today()

        OPR_G15 = models.VisualizeData('2022-07-01', '2022-07-01', 'G15').OPR_today()
        graphbar_OPR_G15 = OPR_G15[0]
        graph_OPR_G15_bydate = OPR_G15[1]
        Graph_Wit_G15 = models.VisualizeData('2022-07-01', '2022-07-01', 'G15').visualize_WorstItem_today()

        OPR_E90 = models.VisualizeData('2022-07-01', '2022-07-01', 'E90').OPR_today()
        graphbar_OPR_E90 = OPR_E90[0]
        graph_OPR_E90_bydate = OPR_E90[1]
        Graph_Wit_E90 = models.VisualizeData('2022-07-01', '2022-07-01', 'E90').visualize_WorstItem_today()

        OPR_F37 = models.VisualizeData('2022-07-01', '2022-07-01', 'F37').OPR_today()
        graphbar_OPR_F37 = OPR_F37[0]
        graph_OPR_F37_bydate = OPR_F37[1]
        Graph_Wit_F37 = models.VisualizeData('2022-07-01', '2022-07-01', 'F37').visualize_WorstItem_today()

        OPR_F38 = models.VisualizeData('2022-07-01', '2022-07-01', 'F38').OPR_today()
        graphbar_OPR_F38 = OPR_F38[0]
        graph_OPR_F38_bydate = OPR_F38[1]
        Graph_Wit_F38 = models.VisualizeData('2022-07-01', '2022-07-01', 'F38').visualize_WorstItem_today()

        

        
        # --------------------------------------------------CONTEXT TO HTML------------------------------------------------------------------
        context = {
            "graphbar_OPR_F58": graphbar_OPR_F58,
            "Graph_Wit_F58": Graph_Wit_F58,
            "graph_OPR_F58_bydate": graph_OPR_F58_bydate,

            "graphbar_OPR_F36": graphbar_OPR_F36,
            "Graph_Wit_F36": Graph_Wit_F36,
            "graph_OPR_F36_bydate": graph_OPR_F36_bydate,

            "graphbar_OPR_G29": graphbar_OPR_G29,
            "Graph_Wit_G29": Graph_Wit_G29,
            "graph_OPR_G29_bydate": graph_OPR_G29_bydate,

            "graphbar_OPR_G12": graphbar_OPR_G12,
            "Graph_Wit_G12": Graph_Wit_G12,
            "graph_OPR_G12_bydate": graph_OPR_G12_bydate,

            "graphbar_OPR_G10": graphbar_OPR_G10,
            "Graph_Wit_G10": Graph_Wit_G10,
            "graph_OPR_G10_bydate": graph_OPR_G10_bydate,

            "graphbar_OPR_G14": graphbar_OPR_G14,
            "Graph_Wit_G14": Graph_Wit_G14,
            "graph_OPR_G14_bydate": graph_OPR_G14_bydate,

            "graphbar_OPR_G15": graphbar_OPR_G15,
            "Graph_Wit_G15": Graph_Wit_G15,
            "graph_OPR_G15_bydate": graph_OPR_G15_bydate,

            "graphbar_OPR_E90": graphbar_OPR_E90,
            "Graph_Wit_E90": Graph_Wit_E90,
            "graph_OPR_E90_bydate": graph_OPR_E90_bydate,

            "graphbar_OPR_F37": graphbar_OPR_F37,
            "Graph_Wit_F37": Graph_Wit_F37,
            "graph_OPR_F37_bydate": graph_OPR_F37_bydate,

            "graphbar_OPR_F38": graphbar_OPR_F38,
            "Graph_Wit_F38": Graph_Wit_F38,
            "graph_OPR_F38_bydate": graph_OPR_F38_bydate,

            "time_update": current_time,

            }
        return render(request, 'OPR/today.html', context)

# Create your views here.
