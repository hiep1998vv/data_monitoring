# from django.shortcuts import render
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
# import forms
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



ModelId = ''
LineId = ''
ProcessId = ''

def check_rib(model, rib):
    data = get_rib(model)
    if rib in data:
        return True
    else:
        return False


def load_Line(request):
    global ModelId
    #print(request.GET.get('time_start'))
    #print(request.GET.get('date_start'))
    ModelId = request.GET.get('ModelId')
    #print(ModelId)
    Line = GetLine(ModelId)
    rib = get_rib(ModelId)
    return render(request, 'kmk/Line_dropdown_list_options.html', {'Line': Line, 'rib':rib})


kmkc = tuple()          # global value of kmk confirm data raw
kmka = tuple()          # global value of kmk ajust data raw
def plotKMK(request):
    Model = GetModel()
    date = datetime.date.today()
    datenow = str(date.strftime("%Y-%m-%d"))
    now = datetime.datetime.now()
    timenow = str(now.strftime("%H:%M:%S"))

    # rib_name = get_rib("E91")
    
    global kmka, kmkc
    if request.method == "GET":
        
        '''
        
        F36_rib = models.KMK_visualize(model = "F36", date_start =datenow, date_end =datenow , line = "", time_start = "00:00:01", time_end = "23:59:59", min_spec = -0.110, max_spec = 0.135).KMKtoday()
        F36_ribUpper = F36_rib[0]
        F36_ribAori = F36_rib[1]
        F36_histo_rib2u = F36_rib[2]
        F36_histo_rib3u = F36_rib[3]
        F36_histo_rib4u = F36_rib[4]
        F36_histo_rib5u = F36_rib[5]
        F36_histo_rib6u = F36_rib[6]
        F36_histo_rib7u = F36_rib[7]

        F36_histo_rib2ul = F36_rib[8]
        F36_histo_rib3ul = F36_rib[9]
        F36_histo_rib4ul = F36_rib[10]
        F36_histo_rib5ul = F36_rib[11]
        F36_histo_rib6ul = F36_rib[12]
        F36_histo_rib7ul = F36_rib[13]

        ribUpper_adj = F36_rib[14]
        ribAori_adj = F36_rib[15]
        histo_rib2u_adj = F36_rib[16]
        histo_rib7u_adj = F36_rib[17]
        histo_rib2ul_adj = F36_rib[18]
        histo_rib7ul_adj = F36_rib[19]
        context = {
                'Model':Model,
                'Modelname':'Model F36',
                'F36_ribUpper': F36_ribUpper,
                "F36_ribAori": F36_ribAori,
                'F36_histo_rib2u':F36_histo_rib2u, 
                'F36_histo_rib3u':F36_histo_rib3u, 
                'F36_histo_rib4u':F36_histo_rib4u, 
                'F36_histo_rib5u':F36_histo_rib5u, 
                'F36_histo_rib6u':F36_histo_rib6u, 
                'F36_histo_rib7u':F36_histo_rib7u,

                'F36_histo_rib2ul':F36_histo_rib2ul, 
                'F36_histo_rib3ul':F36_histo_rib3ul, 
                'F36_histo_rib4ul':F36_histo_rib4ul, 
                'F36_histo_rib5ul':F36_histo_rib5ul, 
                'F36_histo_rib6ul':F36_histo_rib6ul, 
                'F36_histo_rib7ul':F36_histo_rib7ul,

                "ribUpper_adj": ribUpper_adj,
                "ribAori_adj":ribAori_adj,
                "histo_rib2u_adj":histo_rib2u_adj,
                "histo_rib7u_adj":histo_rib7u_adj,
                "histo_rib2ul_adj":histo_rib2ul_adj,
                "histo_rib7ul_adj":histo_rib7ul_adj,

                "line_show": "All",
                "from": datenow+ '  00:00:01',
                'to': datenow+ '  23:59:59',
                "timenow": timenow
            } 
        return render(request, 'dashboard/KMK.html', context)
        '''
        
        rib = models.KMK_visualize(model = "E91", date_start =datenow, date_end =datenow , line = "", time_start = "00:00:01", time_end = "23:59:59", min_spec = -0.175, max_spec = 0.175).KMKtoday()
        ribUpper = rib[0]
        ribAori = rib[1]
        histo_rib1u = rib[2]
        histo_rib2u = rib[3]
        histo_rib3u = rib[4]
        histo_rib4u = rib[5]
        histo_rib5u = rib[6]
        histo_rib6u = rib[7]
        histo_rib7u = rib[8]
        histo_rib8u = rib[9]

        histo_rib1ul = rib[10]
        histo_rib2ul = rib[11]
        histo_rib3ul = rib[12]
        histo_rib4ul = rib[13]
        histo_rib5ul = rib[14]
        histo_rib6ul = rib[15]
        histo_rib7ul = rib[16]
        histo_rib8ul = rib[17]

        ribUpper_adj = rib[18]
        ribAori_adj = rib[19]
        histo_rib2u_adj = rib[20]
        histo_rib7u_adj = rib[21]
        histo_rib2ul_adj = rib[22]
        histo_rib7ul_adj = rib[23]

        differ_upper = rib[24]
        differ_Aori = rib[25]
        
        hist_rib2u_differ = rib[26]
        hist_rib7u_differ = rib[27]
        hist_rib2ul_differ = rib[28]
        hist_rib7ul_differ = rib[29]
        
        #differ_rib2u = rib[30]
        #differ_rib7u = rib[31]

        kmkc = rib[30]
        kmka = rib[31]
        
        context = {
                'Model':Model,
                'Modelname':"E91",
                'F36_ribUpper': ribUpper,
                "F36_ribAori": ribAori,
                'F36_histo_rib1u':histo_rib1u, 
                'F36_histo_rib2u':histo_rib2u, 
                'F36_histo_rib3u':histo_rib3u, 
                'F36_histo_rib4u':histo_rib4u, 
                'F36_histo_rib5u':histo_rib5u, 
                'F36_histo_rib6u':histo_rib6u, 
                'F36_histo_rib7u':histo_rib7u,
                'F36_histo_rib8u':histo_rib8u, 

                'F36_histo_rib1ul':histo_rib1ul, 
                'F36_histo_rib2ul':histo_rib2ul, 
                'F36_histo_rib3ul':histo_rib3ul, 
                'F36_histo_rib4ul':histo_rib4ul, 
                'F36_histo_rib5ul':histo_rib5ul, 
                'F36_histo_rib6ul':histo_rib6ul, 
                'F36_histo_rib7ul':histo_rib7ul,
                'F36_histo_rib8ul':histo_rib8ul, 


                "ribUpper_adj": ribUpper_adj,
                "ribAori_adj":ribAori_adj,
                "histo_rib2u_adj":histo_rib2u_adj,
                "histo_rib7u_adj":histo_rib7u_adj,
                "histo_rib2ul_adj":histo_rib2ul_adj,
                "histo_rib7ul_adj":histo_rib7ul_adj,
                
                "line_show": "All",
                "from": datenow + ' 00:00:01',
                'to': datenow+ ' 23:59:59',

                "differ_upper":differ_upper,
                "differ_Aori":differ_Aori,

                "hist_rib2u_differ":hist_rib2u_differ,
                "hist_rib7u_differ":hist_rib7u_differ,
                "hist_rib2ul_differ":hist_rib2ul_differ,
                "hist_rib7ul_differ":hist_rib7ul_differ,
                #"differ_rib2u":differ_rib2u,
                #"differ_rib7u":differ_rib7u
                "timenow": timenow,

                # "rib_name": rib_name
            } 
        return render(request, 'kmk/KMK_8rib.html', context)
        # return render(request, 'dashboard/KMK_2.html', context)
    
    elif request.method == "POST" and "btn_search" in request.POST:
           
        
        model_get = request.POST.get("Model")
        #print(model_get)
        Line_get = request.POST.get("Line")
        #print(Line_get)
        rib_get = request.POST.get("rib_name")
        #print(rib_get)

        if (Line_get == ""):
            line_show = "All"
        else:
            line_show = Line_get

        if (request.POST.get("date_start") == ""):
            date_start_get = datenow
        else:
            date_start_get = request.POST.get("date_start")
        
        if (request.POST.get("date_end")==""):
            date_end_get = datenow
        else:
            date_end_get = request.POST.get("date_end")

        if (request.POST.get("time-start") == ""):
            time_start_get = "00:00:01"
        else:
            time_start_get = request.POST.get("time-start")

        if (request.POST.get("time-end") == ""):
            time_end_get = "23:59:59"
        else:
            time_end_get = request.POST.get("time-end")


        #print(date_start_get)
        #print(date_end_get)
        #print(time_start_get)
        #print(time_end_get)
        if ( ((model_get =='F36') or (model_get == 'F37') or (model_get == 'F38')) & (rib_get == "")):
            rib = models.KMK_visualize(model = model_get, date_start = date_start_get, date_end=date_end_get, time_start=time_start_get, time_end=time_end_get, line = Line_get, min_spec = -0.110, max_spec = 0.135).KMKtoday()
            ribUpper = rib[0]
            ribAori = rib[1]
            histo_rib2u = rib[2]
            histo_rib3u = rib[3]
            histo_rib4u = rib[4]
            histo_rib5u = rib[5]
            histo_rib6u = rib[6]
            histo_rib7u = rib[7]

            histo_rib2ul = rib[8]
            histo_rib3ul = rib[9]
            histo_rib4ul = rib[10]
            histo_rib5ul = rib[11]
            histo_rib6ul = rib[12]
            histo_rib7ul = rib[13]

            ribUpper_adj = rib[14]
            ribAori_adj = rib[15]
            histo_rib2u_adj = rib[16]
            histo_rib7u_adj = rib[17]
            histo_rib2ul_adj = rib[18]
            histo_rib7ul_adj = rib[19]

            context = {
                    'Model':Model,
                    'Modelname':"Model "+model_get,
                    'F36_ribUpper': ribUpper,
                    "F36_ribAori": ribAori,
                    'F36_histo_rib2u':histo_rib2u, 
                    'F36_histo_rib3u':histo_rib3u, 
                    'F36_histo_rib4u':histo_rib4u, 
                    'F36_histo_rib5u':histo_rib5u, 
                    'F36_histo_rib6u':histo_rib6u, 
                    'F36_histo_rib7u':histo_rib7u,

                    'F36_histo_rib2ul':histo_rib2ul, 
                    'F36_histo_rib3ul':histo_rib3ul, 
                    'F36_histo_rib4ul':histo_rib4ul, 
                    'F36_histo_rib5ul':histo_rib5ul, 
                    'F36_histo_rib6ul':histo_rib6ul, 
                    'F36_histo_rib7ul':histo_rib7ul,

                    "ribUpper_adj": ribUpper_adj,
                    "ribAori_adj":ribAori_adj,
                    "histo_rib2u_adj":histo_rib2u_adj,
                    "histo_rib7u_adj":histo_rib7u_adj,
                    "histo_rib2ul_adj":histo_rib2ul_adj,
                    "histo_rib7ul_adj":histo_rib7ul_adj,

                    "line_show": line_show,
                    "from": date_start_get + ' '+ time_start_get,
                    'to': date_end_get+ ' '+ time_end_get,
                    "timenow": timenow,
                    # "rib_name": rib_name
                } 
            return render(request, 'kmk/KMK.html', context)

        elif (((model_get =='E90') or (model_get == 'E91') or (model_get == 'G31')) & (rib_get == "")):
    
            
            rib = models.KMK_visualize(model = model_get, date_start = date_start_get, date_end=date_end_get, time_start=time_start_get, time_end=time_end_get, line = Line_get, min_spec = -0.175, max_spec = 0.175).KMKtoday()
            ribUpper = rib[0]
            ribAori = rib[1]
            histo_rib1u = rib[2]
            histo_rib2u = rib[3]
            histo_rib3u = rib[4]
            histo_rib4u = rib[5]
            histo_rib5u = rib[6]
            histo_rib6u = rib[7]
            histo_rib7u = rib[8]
            histo_rib8u = rib[9]

            histo_rib1ul = rib[10]
            histo_rib2ul = rib[11]
            histo_rib3ul = rib[12]
            histo_rib4ul = rib[13]
            histo_rib5ul = rib[14]
            histo_rib6ul = rib[15]
            histo_rib7ul = rib[16]
            histo_rib8ul = rib[17]

            ribUpper_adj = rib[18]
            ribAori_adj = rib[19]
            histo_rib2u_adj = rib[20]
            histo_rib7u_adj = rib[21]
            histo_rib2ul_adj = rib[22]
            histo_rib7ul_adj = rib[23]

            differ_upper = rib[24]
            differ_Aori = rib[25]
            
            hist_rib2u_differ = rib[26]
            hist_rib7u_differ = rib[27]
            hist_rib2ul_differ = rib[28]
            hist_rib7ul_differ = rib[29]
            
            #differ_rib2u = rib[30]
            #differ_rib7u = rib[31]

            kmkc = rib[30]
            kmka = rib[31]
          
            context = {
                    'Model':Model,
                    'Modelname':model_get,
                    'F36_ribUpper': ribUpper,
                    "F36_ribAori": ribAori,
                    'F36_histo_rib1u':histo_rib1u, 
                    'F36_histo_rib2u':histo_rib2u, 
                    'F36_histo_rib3u':histo_rib3u, 
                    'F36_histo_rib4u':histo_rib4u, 
                    'F36_histo_rib5u':histo_rib5u, 
                    'F36_histo_rib6u':histo_rib6u, 
                    'F36_histo_rib7u':histo_rib7u,
                    'F36_histo_rib8u':histo_rib8u, 

                    'F36_histo_rib1ul':histo_rib1ul, 
                    'F36_histo_rib2ul':histo_rib2ul, 
                    'F36_histo_rib3ul':histo_rib3ul, 
                    'F36_histo_rib4ul':histo_rib4ul, 
                    'F36_histo_rib5ul':histo_rib5ul, 
                    'F36_histo_rib6ul':histo_rib6ul, 
                    'F36_histo_rib7ul':histo_rib7ul,
                    'F36_histo_rib8ul':histo_rib8ul, 


                    "ribUpper_adj": ribUpper_adj,
                    "ribAori_adj":ribAori_adj,
                    "histo_rib2u_adj":histo_rib2u_adj,
                    "histo_rib7u_adj":histo_rib7u_adj,
                    "histo_rib2ul_adj":histo_rib2ul_adj,
                    "histo_rib7ul_adj":histo_rib7ul_adj,
                    
                    "line_show": line_show,
                    "from": date_start_get + ' '+ time_start_get,
                    'to': date_end_get+ ' '+ time_end_get,

                    "differ_upper":differ_upper,
                    "differ_Aori":differ_Aori,

                    "hist_rib2u_differ":hist_rib2u_differ,
                    "hist_rib7u_differ":hist_rib7u_differ,
                    "hist_rib2ul_differ":hist_rib2ul_differ,
                    "hist_rib7ul_differ":hist_rib7ul_differ,
                    #"differ_rib2u":differ_rib2u,
                    #"differ_rib7u":differ_rib7u
                    "timenow": timenow,
                    # "rib_name": rib_name
                } 
            return render(request, 'kmk/KMK_8rib.html', context)
            # return render(request, 'dashboard/KMK_2.html', context)

        elif (((model_get =='E90') or (model_get == 'E91') or (model_get == 'G31')) & (rib_get != "")):
            
            if ((rib_get == "Rib2U") or (rib_get == "Rib7U")):
                data = models.KMK_visualize(model = model_get, date_start = date_start_get, date_end=date_end_get, time_start=time_start_get, time_end=time_end_get, line = Line_get, min_spec = -0.175, max_spec = 0.175).KMK_byrib(rib_get)
                scatter_rib = data[0]
                histogram_ribupper = data[1]
                histogram_ribaori = data[2]
                scatter_rib_kmkadj = data[3]
                histogram_ribupper_kmkadj = data[4]
                histogram_ribaori_kmkadj = data[5]
                context = {
                        'Model':Model,
                        'Modelname':model_get,
                        "line_show": line_show,
                        "from": date_start_get + ' '+ time_start_get,
                        'to': date_end_get+ ' '+ time_end_get,
                        'scatter_rib_kmkc': scatter_rib,
                        'histo_ribu_kmkc': histogram_ribupper,
                        'histo_riba_kmkc': histogram_ribaori,
                        'scatter_rib_kmka': scatter_rib_kmkadj,
                        'histo_ribu_kmka': histogram_ribupper_kmkadj,
                        'histo_riba_kmka': histogram_ribaori_kmkadj,
                }
                return render(request, 'kmk/KMK_1rib(adj).html', context)
            else:
                data = models.KMK_visualize(model = model_get, date_start = date_start_get, date_end=date_end_get, time_start=time_start_get, time_end=time_end_get, line = Line_get, min_spec = -0.175, max_spec = 0.175).KMK_byrib(rib_get)
                scatter_rib = data[0]
                histogram_ribupper = data[1]
                histogram_ribaori = data[2]
                context = {
                        'Model':Model,
                        'Modelname':model_get,
                        "line_show": line_show,
                        "from": date_start_get + ' '+ time_start_get,
                        'to': date_end_get+ ' '+ time_end_get,
                        'scatter_rib_kmkc': scatter_rib,
                        'histo_ribu_kmkc': histogram_ribupper,
                        'histo_riba_kmkc': histogram_ribaori,
                }
                return render(request, 'kmk/KMK_1rib.html', context)

        elif (((model_get =='F36') or (model_get == 'F37') or (model_get == 'F38')) & (rib_get != "")):
                
            if ((rib_get == "Rib2U") or (rib_get == "Rib7U")):
                data = models.KMK_visualize(model = model_get, date_start = date_start_get, date_end=date_end_get, time_start=time_start_get, time_end=time_end_get, line = Line_get, min_spec = -0.110, max_spec = 0.135).KMK_byrib(rib_get)
                scatter_rib = data[0]
                histogram_ribupper = data[1]
                histogram_ribaori = data[2]
                scatter_rib_kmkadj = data[3]
                histogram_ribupper_kmkadj = data[4]
                histogram_ribaori_kmkadj = data[5]
                context = {
                        'Model':Model,
                        'Modelname':model_get,
                        "line_show": line_show,
                        "from": date_start_get + ' '+ time_start_get,
                        'to': date_end_get+ ' '+ time_end_get,
                        'scatter_rib_kmkc': scatter_rib,
                        'histo_ribu_kmkc': histogram_ribupper,
                        'histo_riba_kmkc': histogram_ribaori,
                        'scatter_rib_kmka': scatter_rib_kmkadj,
                        'histo_ribu_kmka': histogram_ribupper_kmkadj,
                        'histo_riba_kmka': histogram_ribaori_kmkadj,
                }
                return render(request, 'kmk/KMK_1rib(adj).html', context)
            else:
                data = models.KMK_visualize(model = model_get, date_start = date_start_get, date_end=date_end_get, time_start=time_start_get, time_end=time_end_get, line = Line_get, min_spec = -0.110, max_spec = 0.135).KMK_byrib(rib_get)
                scatter_rib = data[0]
                histogram_ribupper = data[1]
                histogram_ribaori = data[2]
                context = {
                        'Model':Model,
                        'Modelname':model_get,
                        "line_show": line_show,
                        "from": date_start_get + ' '+ time_start_get,
                        'to': date_end_get+ ' '+ time_end_get,
                        'scatter_rib_kmkc': scatter_rib,
                        'histo_ribu_kmkc': histogram_ribupper,
                        'histo_riba_kmkc': histogram_ribaori,
                }
                return render(request, 'kmk/KMK_1rib.html', context)
        
    # elif (request.method == "POST") and ("btn-download" in request.POST):             # function to download data raw --> csv file
    #     model_get_ = request.POST.get("Modelname")
    #     print(model_get_)
    #     # condition_get = request.POST.get("line-date-time")
    #     # return HttpResponse("it")

        # if((model_get_ == "E90") or (model_get_ == "E91")):
        #     response = HttpResponse(
        #         content_type='text/csv',
        #         headers={'Content-Disposition': 'attachment; filename="data_raw.csv"'},
        #     )

        #     # The data is hard-coded here, but you could load it from a database or
        #     # some other source.
        #     csv_data = kmkc + kmka
        #     #print(csv_data)

        #     t = loader.get_template('my_template_name.txt')
        #     c = {'data': csv_data}
        #     response.write(t.render(c))
        #     return response

def realtime(request):

    ModelId = request.GET.get('model')
    date = datetime.date.today()
    datenow = str(date.strftime("%Y-%m-%d"))
    time_start_get = request.GET.get("time_start")
    time_end_get = "23:59:59"
    now = datetime.datetime.now()
    timenow = str(now.strftime("%H:%M:%S"))
    #print("i came")
    #print(time_start_get)
    
    rib_name = get_rib("E91")

    if (ModelId == 'E90' or ModelId == 'E91' or ModelId == "G31"):
        #print("i came here")
        rib = models.KMK_visualize(model = ModelId, date_start = datenow, date_end=datenow, time_start=time_start_get, time_end=time_end_get, line = "", min_spec = -0.175, max_spec = 0.175).KMKtoday()
        ribUpper = rib[0]
        ribAori = rib[1]
        histo_rib1u = rib[2]
        histo_rib2u = rib[3]
        histo_rib3u = rib[4]
        histo_rib4u = rib[5]
        histo_rib5u = rib[6]
        histo_rib6u = rib[7]
        histo_rib7u = rib[8]
        histo_rib8u = rib[9]

        histo_rib1ul = rib[10]
        histo_rib2ul = rib[11]
        histo_rib3ul = rib[12]
        histo_rib4ul = rib[13]
        histo_rib5ul = rib[14]
        histo_rib6ul = rib[15]
        histo_rib7ul = rib[16]
        histo_rib8ul = rib[17]

        ribUpper_adj = rib[18]
        ribAori_adj = rib[19]
        histo_rib2u_adj = rib[20]
        histo_rib7u_adj = rib[21]
        histo_rib2ul_adj = rib[22]
        histo_rib7ul_adj = rib[23]

        differ_upper = rib[24]
        differ_Aori = rib[25]
        
        hist_rib2u_differ = rib[26]
        hist_rib7u_differ = rib[27]
        hist_rib2ul_differ = rib[28]
        hist_rib7ul_differ = rib[29]
        #print(ribUpper)

        data = {
                'ribUpper_kmkc':ribUpper,
                'ribAori_kmkc':ribAori,
                'histo_rib1u_kmkc':histo_rib1u,
                'histo_rib2u_kmkc':histo_rib2u,
                'histo_rib3u_kmkc':histo_rib3u,
                'histo_rib4u_kmkc':histo_rib4u,
                'histo_rib5u_kmkc':histo_rib5u,
                'histo_rib6u_kmkc':histo_rib6u,
                'histo_rib7u_kmkc':histo_rib7u,
                'histo_rib8u_kmkc':histo_rib8u,

                'histo_rib1ul_kmkc':histo_rib1ul,
                'histo_rib2ul_kmkc':histo_rib2ul,
                'histo_rib3ul_kmkc':histo_rib3ul,
                'histo_rib4ul_kmkc':histo_rib4ul,
                'histo_rib5ul_kmkc':histo_rib5ul,
                'histo_rib6ul_kmkc':histo_rib6ul,
                'histo_rib7ul_kmkc':histo_rib7ul,
                'histo_rib8ul_kmkc':histo_rib8ul,

                'ribUpper_adj':ribUpper_adj,
                'ribAori_adj':ribAori_adj,
                'histo_rib2u_adj':histo_rib2u_adj,
                'histo_rib7u_adj':histo_rib7u_adj,
                'histo_rib2ul_adj':histo_rib2ul_adj,
                'histo_rib7ul_adj':histo_rib7ul_adj,

                'differ_upper':differ_upper,
                'differ_aori':differ_Aori,
                'histo_rib2u_differ':hist_rib2u_differ,
                'histo_rib7u_differ':hist_rib7u_differ,
                'histo_rib2ul_differ':hist_rib2ul_differ,
                'histo_rib7ul_differ':hist_rib7ul_differ,
                'time-end':timenow,

                "rib_name": rib_name
                    }

        return JsonResponse(data)

def ajax_download_rawdata(request):
    
    model_get_ = request.POST.get("model")
    print(model_get_)
    # condition_get = request.POST.get("line-date-time")
    # return HttpResponse("it")

    # if((model_get_ == "E90") or (model_get_ == "E91")):
    #     response = HttpResponse(
    #         content_type='text/csv',
    #         headers={'Content-Disposition': 'attachment; filename="data_raw.csv"'},
    #     )

    #     # The data is hard-coded here, but you could load it from a database or
    #     # some other source.
    #     csv_data = kmkc + kmka
    #     #print(csv_data)

    #     t = loader.get_template('my_template_name.txt')
    #     c = {'data': csv_data}
    #     response.write(t.render(c))
    #     return response

    # return JsonResponse(data)
