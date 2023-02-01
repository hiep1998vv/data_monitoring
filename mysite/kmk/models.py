from django.db import models
from re import template
from tkinter import Button
from turtle import bgcolor, tilt, title
from django.db import models
from django.http import request
from collections import Counter
from matplotlib.axis import YAxis
from matplotlib.figure import Figure
import pyodbc
import time
from time import sleep
from datetime import datetime, date, timedelta
import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys
import base64
from io import BytesIO
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from plotly.offline import plot
from time import sleep
import calendar
import plotly.io as pio
from statistics import mean

# from sqlalchemy import null

pio.templates.default = "plotly_white"

# --------------------------GLOBAL VARIABLE-------------------------

# -------------------------DEFINE CONNECTION STRING ---------------------------------------
# SQL server connection
def connection():
    s = 'CVN-VENG;' #Your server name 
    d = 'ASSYChecker' 
    u = 'sa' #Your login
    p = 'tim@2020;' #Your login password
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    conn = pyodbc.connect(cstr)
    return conn

conn_CVN_VENG = connection()

#---------------------------------MODEL FOR TIME PICKER-------------------------------
#---------------------------------------------------------------------------------
class DTModel(models.Model):
    date_start = models.DateField(null = True)
    time_start = models.TimeField(null = True)
    date_time = models.DateTimeField(null = True)

# ----------------------------------------------GENERAL FUNCTION-----------------------------------------------
def get_quantity(conn, strSql):  # count number of data 
    cursor = conn.cursor()
    cursor.execute(strSql)
    records = cursor.fetchall()
    return len(records)

def get_json(conn, strSql):  # count number of data 
    cursor = conn.cursor()
    cursor.execute(strSql)
    records = cursor.fetchall()
    return records

def dataTable(conn, strSql):     # return data with object definition
    cursor = conn.cursor()
    cursor.execute(strSql)
    records = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in records:
        insertObject.append( dict( zip( columnNames , record ) ) )
    return insertObject

def filter_data(data_raw, name):   # filter data with condition 'name'
    list_1 =[]
    for i in range(len(data_raw)):
      list_1.append(data_raw[i][name])
    Filter_data = list(set(list_1))
    return Filter_data

def convert_str_to_Date(date_string): 
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    return date

def date_range_list(startdate, enddate):
    # Return list of datetime.date objects between start_date and end_date (inclusive).
    start_date = convert_str_to_Date(startdate)
    end_date = convert_str_to_Date(enddate)
    date_list = []
    curr_date = start_date
    while (curr_date <= end_date):
        date_list.append(curr_date)
        curr_date += timedelta(days=1)
    return date_list

# ------------------------------------------------FUNCTON TO GET DATA FOR COMBOBOX-----------------------------------------------------
def GetModel():
    str_getName = "select Model from Model_KMK_Define where Checker = 'KMK' and Enable = '1'"
    name = dataTable(conn_CVN_VENG, str_getName)
    
    return name

def GetLine(model):
    str_getName = "select distinct Line from "+model+"KMK"
    #print(str_getName)
    line = dataTable(conn_CVN_VENG, str_getName)
    #print(line)
    return line

def get_rib(model):
    str_query = "select * from Model_KMK_Define where Model = '"+model+"' and Checker = 'KMK'"
    data = dataTable(conn_CVN_VENG, str_query)
    #print(data[0]["Upper"])
    rib = data[0]["Upper"].split('-')
    #print(rib)
    return rib

# -----------------------------------------------------------------KMK VISUALIZE-------------------------------------------------------------------

def convert_to_dict(data):
    data.split('-')
def Average(lst):
    return sum(lst) / len(lst)

def Histogram_value(data):      # ----------------Return value MAX, MIN, MEAN, CPL, CPK, SIGMA,......
    mean_rib2ul = mean(data)   # --------------rib2ul----------------
    Max_rib2ul = max(data)
    Min_rib2ul = min(data)
    sigma_rib2ul = np.std(data)
    sigma3_pos_rib2ul = mean_rib2ul + 3*sigma_rib2ul
    sigma3_neg_rib2ul = mean_rib2ul - 3*sigma_rib2ul
    sigma4_pos_rib2ul = mean_rib2ul + 4*sigma_rib2ul
    sigma4_neg_rib2ul = mean_rib2ul - 4*sigma_rib2ul
    CpL_rib2ul = (mean_rib2ul - Min_rib2ul)/(3*sigma_rib2ul)
    CpH_rib2ul = (Max_rib2ul - mean_rib2ul)/(3*sigma_rib2ul)
    CpK_rib2ul = min(CpL_rib2ul, CpH_rib2ul)

    return {'max': Max_rib2ul, 'min': Min_rib2ul, 'mean': mean_rib2ul, 'sigma': sigma_rib2ul,
            '+3sigma': sigma3_pos_rib2ul, '-3sigma': sigma3_neg_rib2ul, '+4sigma': sigma4_pos_rib2ul, '-4sigma': sigma4_neg_rib2ul,
            'cpl': CpL_rib2ul, 'cph':CpH_rib2ul, 'cpk': CpK_rib2ul
            }

def Layout_histogram(data, min_spec, max_spec, name):                                               #---------------------------LAYOUT FOR HISTOGRAM CHARTS-----------------------------------
    if (len(data)>0):
        layout_rib2u = go.Layout(
            # Mean lines, 3sigma, -3sigma,
            yaxis_title = "<b>frequence</b>", 
            shapes= [{'line': {'color': 'rgba(255, 16, 20, 0.8)', 'dash': 'solid', 'width': 3},      #---------------------------MEAN LINE-----------------------------------
            'type': 'line','x0': mean(data),
            'x1': mean(data),
            'xref': 'x','y0': -0.0,'y1': 1,
            'yref': 'paper'},
            {'line': {'color': 'rgba(232, 96, 25, 1)', 'dash': 'solid', 'width': 3},                #---------------------------"+3" SIGMA LINE-----------------------------------
            'type': 'line','x0': Histogram_value(data)['+3sigma'],
            'x1': Histogram_value(data)['+3sigma'],
            'xref': 'x','y0': -0.0,'y1': 0.5,
            'yref': 'paper'},
            {'line': {'color': 'rgba(232, 96, 25, 1)', 'dash': 'solid', 'width': 3},                #---------------------------"-3" SIGMA LINE-----------------------------------
            'type': 'line','x0': Histogram_value(data)['-3sigma'],
            'x1': Histogram_value(data)['-3sigma'],
            'xref': 'x','y0': -0.0,'y1': 0.5,
            'yref': 'paper'},
            {'line': {'color': 'rgba(5, 5, 5, 0.83)', 'dash': 'dash', 'width': 3},                  #---------------------------MIN_SPEC LINE-----------------------------------
            'type': 'line','x0': float(min_spec),
            'x1': float(min_spec),
            'xref': 'x','y0': -0.0,'y1': 0.9,
            'yref': 'paper'},
            {'line': {'color': 'rgba(5, 5, 5, 0.83)', 'dash': 'dash', 'width': 3},                  #---------------------------MAX_SPEC LINE-----------------------------------
            'type': 'line','x0': float(max_spec),
            'x1': float(max_spec),
            'xref': 'x','y0': -0.0,'y1': 0.9,
            'yref': 'paper'},
            
            ],
            # Annotations
            annotations=[
                dict(                                #---------------------------annotation for MEAN value -----------------------------------
                    x=mean(data),
                    y=1,
                    xref='x',
                    yref='paper',
                    text="<b>Mean = %.3f" %mean(data)+'</b>',
                    showarrow=True,
                    arrowhead=7, font = dict(color = 'red')
                ),
                dict(                                #---------------------------annotation for +3 SIGMA value -----------------------------------
                    x=Histogram_value(data)['+3sigma'],
                    y=0.5, xref='x', yref='paper',
                    text="<b>+3σ = %.3f" %Histogram_value(data)['+3sigma']+'</b>',
                    showarrow=True, arrowhead=7, font = dict(color = 'red')
                ),
                dict(                                #---------------------------annotation for -3 SIGMA value -----------------------------------
                    x=Histogram_value(data)['-3sigma'],
                    y=0.5, xref='x', yref='paper',
                    text="<b>-3σ = %.3f" %Histogram_value(data)['-3sigma']+'</b>',align = 'right',
                    showarrow=True, arrowhead=7, font = dict(color = 'red')
                )
                ,
                dict(                                #---------------------------annotation for MIN_SPEC value -----------------------------------
                    x= float(min_spec),
                    y=0.95, xref='x', yref='paper',
                    text='<b>'+str(min_spec)+'</b>',align = 'right',
                    showarrow=False, arrowhead=7, font = dict(color = 'red')
                ),
                dict(                               #---------------------------annotation for MAX_SPEC value -----------------------------------
                    x= float(max_spec),
                    y=0.95, xref='x', yref='paper',
                    text='<b>'+str(max_spec)+'</b>',align = 'right',
                    showarrow=False, arrowhead=7, font = dict(color = 'red')
                ),
                dict(                               #---------------------------annotation for MAX, MIN, SIGMA value -----------------------------------
                    text='<b>Max: '+str(max(data))+'<br>Min: '+str(min(data))+'<br>Sigma: '+str(format(np.std(data),".3f"))+'</b>',
                    align='left',showarrow=False, xref='paper', yref='paper', x=-0.1, y=1.4,
                    bordercolor='blue',
                    borderwidth=1, font = dict(size = 15)
                ),
                dict(                               #---------------------------annotation for CPH, CPL, CPK value -----------------------------------
                    text='<b>CpL: '+str(format(Histogram_value(data)['cpl'],'.3f'))+'<br>CpH: '+str(format(Histogram_value(data)['cph'],'.3f'))+'<br>CpK: '+str(format(Histogram_value(data)['cpk'],".3f"))+'</b>',
                    align='left',showarrow=False, xref='paper', yref='paper', x=1.0, y=1.4,
                    bordercolor='blue',borderwidth=0.5, font = dict(size = 15)
                )],
            xaxis_range=[float(min_spec) - 0.05, float(max_spec)+0.05],          #--------------- x axis range define ---------------------------
            xaxis_title = "<b>"+name+"</b>",
            margin=dict(t=140,  # top margin: 30px, you want to leave around 30 pixels to
                                # display the modebar above the graph.
                        b=20,   # bottom margin: 10px
                        l=30,   # left margin: 10px
                        r=10    # right margin: 10px
            )
        ) 
        return layout_rib2u
    else:
        layout_rib2u = go.Layout()
        return layout_rib2u

def layout_rib(**kwargs):
    min_s = kwargs["min_s"]
    max_s = kwargs["max_s"]
    bgcolor = kwargs["bgcolor"]
    

    layout = go.Layout(
        yaxis_title = "<b>mm</b>",
        shapes=[
                {'line': {'color': 'rgba(5, 5, 5, 0.83)', 'dash': 'dash', 'width': 3},                  #---------------------------MIN_SPEC LINE-----------------------------------
                'type': 'line','y0': float(min_s),
                'y1': float(min_s),
                'xref': 'paper','x0': -0.0,'x1': 1.0,
                'yref': 'y'},
                {'line': {'color': 'rgba(5, 5, 5, 0.83)', 'dash': 'dash', 'width': 3},                  #---------------------------MAX_SPEC LINE-----------------------------------
                'type': 'line','y0': float(max_s),
                'y1': float(max_s),
                'xref': 'paper','x0': -0.0,'x1': 1.0,
                'yref': 'y'},
        ],
        annotations=[
            dict(                                #---------------------------annotation for MIN_SPEC value -----------------------------------
                    x= 0.97 ,
                    y=float(min_s)-0.01, xref='paper', yref='y',
                    text='<b>'+str(min_s)+'</b>',align = 'right',
                    showarrow=False, arrowhead=7, font = dict(color = 'red')
                ),
                dict(                               #---------------------------annotation for MAX_SPEC value -----------------------------------
                    x= 0.97,
                    y=float(max_s)+0.01, xref='paper', yref='y',
                    text='<b>'+str(max_s)+'</b>',align = 'right',
                    showarrow=False, arrowhead=7, font = dict(color = 'red')
                ),
        ],
        yaxis_range=[float(min_s)- 0.05, float(max_s) +0.05],           #---------------------------y axis set range-------------------------
        margin=dict(
                    t=50, # top margin: 30px, you want to leave around 30 pixels to
                        # display the modebar above the graph.
                    b=10, # bottom margin: 10px
                    l=10, # left margin: 10px
                    r=10, # right margin: 10px
                    ),
        paper_bgcolor = bgcolor,                                       #--------------------------set background color----------------------
        
    )
    return layout
    
def check_outspec_ornot(value, min_spec, max_spec):             # -----------------------Function to check if items out spec or not--------------------
    for i in range(len(value)):
        if (float(value[i])> float(max_spec) or float(value[i])<float(min_spec)):
            return True
        
    return False

def sorted_and_return(data1, data2):
    list_key = data1.keys()
    sorted_key = sorted(list_key)
    sorted_value = []
    sorted_serial = []
    for i in sorted_key:
        sorted_value.append(data1[i])
        sorted_serial.append(data2[i])
    return {"key":sorted_key, "value":sorted_value, "serial":sorted_serial}

def time_tango(date, time):
    return datetime.datetime.combine(date, time)

class KMK_visualize():   
    def __init__(self, **kwargs):
        
        self.model = kwargs["model"]
        self.line = kwargs["line"]
        #self.process = kwargs["process"]
        self.date_start = kwargs["date_start"]
        self.date_end = kwargs["date_end"]
        self.time_start = kwargs["time_start"]
        self.time_end = kwargs["time_end"]
        #self.serial = kwargs["serial"]
        self.min_spec = kwargs["min_spec"]
        self.max_spec = kwargs["max_spec"]
        #self.up_spec = kwargs["up_spec"]
        #self.down_spec = kwargs["down_spec"]
        

    def KMKtoday(self):

        if ((self.model == 'F36') or (self.model == 'F37') or (self.model == 'F38')):
            str_getName_rib = "select * from Model_KMK_Define where Model = '"+self.model+"' and Checker = 'KMK' and Enable = '1'"
            data_nameRib = dataTable(conn_CVN_VENG, str_getName_rib)
            rib_upper = data_nameRib[0]["Upper"].split('-')
            rib_aori = data_nameRib[0]["Aori"].split('-')
            rib_upper_adj = ["Rib2U","Rib7U"]
            rib_aori_adj = ["Rib2Aori","Rib7Aori"]
            
            SQL_Stament = "SELECT * from "+self.model+"KMK where Date >='"+self.date_start+"' and Date <='"+self.date_end+"' and Time >= '"+self.time_start+"' and Time <= '"+self.time_end+"' "
            SQL_Stament += "and (Coalesce( '"+self.line+"', '' )='' or Line = '"+self.line+"') "
            SQL_Stament += " ORDER BY [No] ASC"

            SQL_Stament_adj = "SELECT * from "+self.model+"KMKADJ where Date >='"+self.date_start+"' and Date <='"+self.date_end+"' and Time >= '"+self.time_start+"' and Time <= '"+self.time_end+"' "
            SQL_Stament_adj += "and (Coalesce( '"+self.line+"', '' )='' or Line = '"+self.line+"') "
            SQL_Stament_adj += " ORDER BY [No] DESC"
            #print(SQL_Stament)
            data_raw = dataTable(conn_CVN_VENG, SQL_Stament)
            data_raw_adj = dataTable(conn_CVN_VENG, SQL_Stament_adj)

            kmk_conf = (("KMK CONFIRM"), ("SERIAL", "TIME", "RESULT", "RIB2U", "RIB2UL", "RIB3U", "RIB3UL", "RIB4U", "RIB4UL", "RIB5U", "RIB5UL", "RIB6U", "RIB6UL", "RIB7U", "RIB7UL"))
            kmk_adj = (("KMK ADJUST"), ("SERIAL", "TIME", "RESULT", "RIB2U", "RIB2UL", "RIB7U", "RIB7UL"))

            for d in range(len(data_raw)):
                data = (data_raw[d]["SERIAL"], data_raw[d]["Time"], data_raw[d]["Result"], str(data_raw[d]["Rib2U"]), str(data_raw[d]["Rib2UL"]), str(data_raw[d]["Rib3U"]), str(data_raw[d]["Rib3UL"]),
                        str(data_raw[d]["Rib4U"]), str(data_raw[d]["Rib4UL"]), str(data_raw[d]["Rib5U"]), str(data_raw[d]["Rib5UL"]), str(data_raw[d]["Rib6U"]), str(data_raw[d]["Rib6UL"]), str(data_raw[d]["Rib7U"]), 
                        str(data_raw[d]["Rib7UL"])
                )
                kmk_conf += data
            
            for A in range(len(data_raw_adj)):
                data = (data_raw_adj[A]["SERIAL"], data_raw_adj[A]["Time"], data_raw_adj[A]["Result"], 
                        str(data_raw_adj[A]["Rib2U"]), str(data_raw_adj[A]["Rib2Aori"]), str(data_raw_adj[A]["Rib7U"]), str(data_raw_adj[A]["Rib7Aori"])
                )
                kmk_adj += data
                
            
            #------------------------------------------------------------------------------------------------------------------
            #----------------------------------graph SCATTER RIB KMK CONFIRM---------------------------------------------------
            #------------------------------------------------------------------------------------------------------------------
            layout_ribupper_KMKC = layout_rib(min_s = self.min_spec, max_s = self.max_spec, bgcolor = "rgba(230, 221, 113, 0.8)")
            layout_ribAori_KMKC = layout_rib(min_s = self.min_spec, max_s = self.max_spec, bgcolor = 'rgba(147, 225, 235, 1.0)')
            fig_ribUpper = go.Figure(layout=layout_ribupper_KMKC)
            fig_ribAori = go.Figure(layout=layout_ribAori_KMKC)

            value_upper_all = {"Rib1U":[],"Rib2U":[],"Rib3U":[],"Rib4U":[],"Rib5U":[],"Rib6U":[],"Rib7U":[],"Rib8U":[]}                 #------------DATA FOR RIB HISTOGRAM CHART (use multiple time, no reset)------------
            value_aori_all = {"Rib1UL":[],"Rib2UL":[],"Rib3UL":[],"Rib4UL":[],"Rib5UL":[],"Rib6UL":[],"Rib7UL":[],"Rib8UL":[]}          #------------DATA FOR RIB HISTOGRAM CHART (use multiple time, no reset)------------

            outspec_upper_kmkC = 0   
            outspec_aori_kmkC = 0                                #-----------return value out spec---------------
            for i in range(len(data_raw)):
                value_upper = []                                    #------------DATA FOR RIB SCATTER CHART (use 1 time, reset after draw 1 scatter)------------
                value_aori = []                                     #------------DATA FOR RIB SCATTER CHART (use 1 time, reset after draw 1 scatter)------------
                
                for j in range(len(rib_upper)):
                    value_upper.append(float(data_raw[i][rib_upper[j]]))                        #1 data rib --> [value rib 1 upper, value rib2u, ......., value rib8u]
                    value_upper_all[rib_upper[j]].append(float(data_raw[i][rib_upper[j]]))      # All data save to here--> {"Rib1UL": [list value of Rib1UL], ....} 
                for k in range(len(rib_aori)):
                    value_aori.append(float(data_raw[i][rib_aori[k]]))
                    value_aori_all[rib_aori[k]].append(float(data_raw[i][rib_aori[k]]))
                
                if (check_outspec_ornot(value_upper, self.min_spec, self.max_spec)):       #-----------return value out spec rib upper---------------     
                    outspec_upper_kmkC += 1
                   
                if (check_outspec_ornot(value_aori, self.min_spec, self.max_spec)):       #-----------return value out spec rib Aori---------------     
                    outspec_aori_kmkC = outspec_aori_kmkC +1

                fig_ribUpper.add_trace(go.Scatter(x=rib_upper, y= value_upper, name= data_raw[i]["OriginID"]))
                fig_ribAori.add_trace(go.Scatter(x=rib_aori, y= value_aori, name= data_raw[i]["OriginID"]))
            
            fig_ribUpper.update_layout(title = "Total: "+str(len(data_raw))+ "    Out spec: "+ str(outspec_upper_kmkC))
            fig_ribAori.update_layout(title = "Total: "+str(len(data_raw))+ "    Out spec: "+ str(outspec_aori_kmkC))

            graph_upper = plot(fig_ribUpper, output_type='div')
            graph_aori = plot(fig_ribAori, output_type='div')
            


            #------------------------------------------------------------------------------------------------------------------
            #-----------------------------------------graph SCATTER RIB KMK ADJUST---------------------------------------------
            #------------------------------------------------------------------------------------------------------------------
            layout_ribupper_KMKA = layout_rib(min_s = self.min_spec, max_s = self.max_spec, bgcolor = "rgba(230, 221, 113, 0.8)")
            layout_ribAori_KMKA = layout_rib(min_s = self.min_spec, max_s = self.max_spec, bgcolor = 'rgba(147, 225, 235, 1.0)')
            fig_ribUpper_adj = go.Figure(layout=layout_ribupper_KMKA)                          
            fig_ribAori_adj = go.Figure(layout=layout_ribAori_KMKA)
            value_upper_adj = {"Rib2U":[],"Rib7U":[]}               #------------DATA FOR RIB HISTOGRAM CHART------------
            value_aori_adj = {"Rib2Aori":[],"Rib7Aori":[]}          #------------DATA FOR RIB HISTOGRAM CHART------------

            outspec_upper_kmka = 0   
            outspec_aori_kmka = 0                                #-----------return value out spec---------------
            for i in range(len(data_raw_adj)):
                value_upperadj = []                                 #------------DATA FOR RIB SCATTER CHART------------
                value_aoriadj = []                                  #------------DATA FOR RIB SCATTER CHART------------
                
                for j in range(len(rib_upper_adj)):
                    if data_raw_adj[i][rib_upper_adj[j]] is not None:                            #------------------------remove null value caused by PE1, MFE1 change tools----------------------
                        value_upperadj.append(float(data_raw_adj[i][rib_upper_adj[j]]))
                        value_upper_adj[rib_upper_adj[j]].append(float(data_raw_adj[i][rib_upper_adj[j]]))
                for k in range(len(rib_aori_adj)):
                    if data_raw_adj[i][rib_aori_adj[k]] is not None:                            #------------------------remove null value caused by PE1, MFE1 change tools----------------------
                        value_aoriadj.append(float(data_raw_adj[i][rib_aori_adj[k]]))
                        value_aori_adj[rib_aori_adj[k]].append(float(data_raw_adj[i][rib_aori_adj[k]]))

                if (check_outspec_ornot(value_upperadj, self.min_spec, self.max_spec)):       #-----------return value out spec rib upper---------------     
                    outspec_upper_kmka = outspec_upper_kmka + 1
                    
                if (check_outspec_ornot(value_upperadj, self.min_spec, self.max_spec)):       #-----------return value out spec rib Aori---------------     
                    outspec_aori_kmka = outspec_aori_kmka +1

                fig_ribUpper_adj.add_trace(go.Scatter(x=rib_upper_adj, y= value_upperadj, name= data_raw_adj[i]["SERIAL"]))
                fig_ribAori_adj.add_trace(go.Scatter(x=rib_aori_adj, y= value_aoriadj, name= data_raw_adj[i]["SERIAL"]))
            
            fig_ribUpper_adj.update_layout(title = "Total: "+str(len(data_raw_adj))+ "    Out spec: "+ str(outspec_upper_kmka))
            fig_ribAori_adj.update_layout(title = "Total: "+str(len(data_raw_adj))+ "    Out spec: "+ str(outspec_aori_kmka))
        
            graph_upper_adj = plot(fig_ribUpper_adj, output_type='div')
            graph_aori_adj = plot(fig_ribAori_adj, output_type='div')

            #---------------------------------------config layout for rib --------------------------------------
            #------------------------------ADDING MIN, MAX, MEAN, SIGMA, 3SIGMA, CPL, CPK,----------------------
            #---------------------------------------------------------------------------------------------------
            layout_rib2u = Layout_histogram(value_upper_all["Rib2U"], self.min_spec, self.max_spec, "Rib2U") #-----layout KMK CONFIRM-------  
            layout_rib3u = Layout_histogram(value_upper_all["Rib3U"], self.min_spec, self.max_spec, "Rib3U")
            layout_rib4u = Layout_histogram(value_upper_all["Rib4U"], self.min_spec, self.max_spec, "Rib4U")
            layout_rib5u = Layout_histogram(value_upper_all["Rib5U"], self.min_spec, self.max_spec, "Rib5U")
            layout_rib6u = Layout_histogram(value_upper_all["Rib6U"], self.min_spec, self.max_spec, "Rib6U")
            layout_rib7u = Layout_histogram(value_upper_all["Rib7U"], self.min_spec, self.max_spec, "Rib7U")

            layout_rib2ul = Layout_histogram(value_aori_all["Rib2UL"], self.min_spec, self.max_spec, "Rib2UL")
            layout_rib3ul = Layout_histogram(value_aori_all["Rib3UL"], self.min_spec, self.max_spec, "Rib3UL")
            layout_rib4ul = Layout_histogram(value_aori_all["Rib4UL"], self.min_spec, self.max_spec, "Rib4UL")
            layout_rib5ul = Layout_histogram(value_aori_all["Rib5UL"], self.min_spec, self.max_spec, "Rib5UL")
            layout_rib6ul = Layout_histogram(value_aori_all["Rib6UL"], self.min_spec, self.max_spec, "Rib6UL")
            layout_rib7ul = Layout_histogram(value_aori_all["Rib7UL"], self.min_spec, self.max_spec, "Rib7UL")
            
            

            fig_histogram_rib2u = go.Figure(layout=layout_rib2u) #------------Histogram KMK confirm--------------
            fig_histogram_rib3u = go.Figure(layout=layout_rib3u)
            fig_histogram_rib4u = go.Figure(layout=layout_rib4u)
            fig_histogram_rib5u = go.Figure(layout=layout_rib5u)
            fig_histogram_rib6u = go.Figure(layout=layout_rib6u)
            fig_histogram_rib7u = go.Figure(layout=layout_rib7u)

            fig_histogram_rib2ul = go.Figure(layout=layout_rib2ul)
            fig_histogram_rib3ul = go.Figure(layout=layout_rib3ul)
            fig_histogram_rib4ul = go.Figure(layout=layout_rib4ul)
            fig_histogram_rib5ul = go.Figure(layout=layout_rib5ul)
            fig_histogram_rib6ul = go.Figure(layout=layout_rib6ul)
            fig_histogram_rib7ul = go.Figure(layout=layout_rib7ul)




            fig_histogram_rib2u.add_trace(go.Histogram(x= value_upper_all["Rib2U"]))
            fig_histogram_rib3u.add_trace(go.Histogram(x= value_upper_all["Rib3U"]))
            fig_histogram_rib4u.add_trace(go.Histogram(x= value_upper_all["Rib4U"]))
            fig_histogram_rib5u.add_trace(go.Histogram(x= value_upper_all["Rib5U"]))
            fig_histogram_rib6u.add_trace(go.Histogram(x= value_upper_all["Rib6U"]))
            fig_histogram_rib7u.add_trace(go.Histogram(x= value_upper_all["Rib7U"]))

            fig_histogram_rib2ul.add_trace(go.Histogram(x = value_aori_all["Rib2UL"]))
            fig_histogram_rib3ul.add_trace(go.Histogram(x = value_aori_all["Rib3UL"]))
            fig_histogram_rib4ul.add_trace(go.Histogram(x = value_aori_all["Rib4UL"]))
            fig_histogram_rib5ul.add_trace(go.Histogram(x = value_aori_all["Rib5UL"]))
            fig_histogram_rib6ul.add_trace(go.Histogram(x = value_aori_all["Rib6UL"]))
            fig_histogram_rib7ul.add_trace(go.Histogram(x = value_aori_all["Rib7UL"]))



            graph_histo_rib2u = plot(fig_histogram_rib2u, output_type="div")
            graph_histo_rib3u = plot(fig_histogram_rib3u, output_type="div")
            graph_histo_rib4u = plot(fig_histogram_rib4u, output_type="div")
            graph_histo_rib5u = plot(fig_histogram_rib5u, output_type="div")
            graph_histo_rib6u = plot(fig_histogram_rib6u, output_type="div")
            graph_histo_rib7u = plot(fig_histogram_rib7u, output_type="div")

            graph_histo_rib2ul = plot(fig_histogram_rib2ul, output_type="div")
            graph_histo_rib3ul = plot(fig_histogram_rib3ul, output_type="div")
            graph_histo_rib4ul = plot(fig_histogram_rib4ul, output_type="div")
            graph_histo_rib5ul = plot(fig_histogram_rib5ul, output_type="div")
            graph_histo_rib6ul = plot(fig_histogram_rib6ul, output_type="div")
            graph_histo_rib7ul = plot(fig_histogram_rib7ul, output_type="div")

            ##################################################################################################################################

            layout_rib2u_adj = Layout_histogram(value_upper_adj["Rib2U"], self.min_spec, self.max_spec, "Rib2U") #-----layout KMK ADJUST-------  
            layout_rib7u_adj = Layout_histogram(value_upper_adj["Rib7U"], self.min_spec, self.max_spec, "Rib7U")
            layout_rib2ul_adj = Layout_histogram(value_aori_adj["Rib2Aori"], self.min_spec, self.max_spec, "Rib2UL")
            layout_rib7ul_adj = Layout_histogram(value_aori_adj["Rib7Aori"], self.min_spec, self.max_spec, "Rib7UL")

            fig_histogram_rib2u_adj = go.Figure(layout=layout_rib2u_adj) #------------Histogram KMK adjust-------------
            fig_histogram_rib7u_adj = go.Figure(layout=layout_rib7u_adj)
            fig_histogram_rib2ul_adj = go.Figure(layout=layout_rib2ul_adj)
            fig_histogram_rib7ul_adj = go.Figure(layout=layout_rib7ul_adj)

            fig_histogram_rib2u_adj.add_trace(go.Histogram(x= value_upper_adj["Rib2U"]))
            fig_histogram_rib7u_adj.add_trace(go.Histogram(x= value_upper_adj["Rib7U"]))

            fig_histogram_rib2ul_adj.add_trace(go.Histogram(x = value_aori_adj["Rib2Aori"]))
            fig_histogram_rib7ul_adj.add_trace(go.Histogram(x = value_aori_adj["Rib7Aori"]))

  
            graph_histo_rib2u_adj = plot(fig_histogram_rib2u_adj, output_type="div")
            graph_histo_rib7u_adj = plot(fig_histogram_rib7u_adj, output_type="div")

            graph_histo_rib2ul_adj = plot(fig_histogram_rib2ul_adj, output_type="div")
            graph_histo_rib7ul_adj = plot(fig_histogram_rib7ul_adj, output_type="div")


            
            
            return [graph_upper, graph_aori, 
                    graph_histo_rib2u,graph_histo_rib3u,graph_histo_rib4u,graph_histo_rib5u,graph_histo_rib6u,graph_histo_rib7u,
                    graph_histo_rib2ul,graph_histo_rib3ul,graph_histo_rib4ul,graph_histo_rib5ul,graph_histo_rib6ul,graph_histo_rib7ul,   
                    graph_upper_adj,graph_aori_adj,  
                    graph_histo_rib2u_adj, graph_histo_rib7u_adj,
                    graph_histo_rib2ul_adj, graph_histo_rib7ul_adj      
                        ]
        
        #---------------------------------------------------------------------------------------------------------------
        # ------------------------------------THIS IS FOR MODEL E90,E91, G31,F08 -------------------------------------------------
        #---------------------------------------------------------------------------------------------------------------
        else :                  
            str_getName_rib = "select * from Model_KMK_Define where Model = '"+self.model+"' and Checker = 'KMK' and Enable = '1'"
            data_nameRib = dataTable(conn_CVN_VENG, str_getName_rib)
            rib_upper = data_nameRib[0]["Upper"].split('-')
            rib_aori = data_nameRib[0]["Aori"].split('-')
            rib_upper_adj = ["Rib2U","Rib7U"]
            rib_aori_adj = ["Rib2Aori","Rib7Aori"]

            
            SQL_Stament = "SELECT * from "+self.model+"KMK where Date >='"+self.date_start+"' and Date <='"+self.date_end+"' and Time >= '"+self.time_start+"' and Time <= '"+self.time_end+"' "
            #SQL_Stament += " WHERE [Date] = '"+date_input+"' AND (Coalesce( '"+self.line+"', '')='' or [Line] = '"+ self.line + "') AND (Coalesce( '"+self.line+"', '' )='' or Line = '"+self.line+"') AND (Coalesce( '"+self.time+"', '' )='' or Time = '"+self.time+"') "
            SQL_Stament += "and (Coalesce( '"+self.line+"', '' )='' or Line = '"+self.line+"') "
            SQL_Stament += " ORDER BY [No] ASC"
            #print(SQL_Stament)
            SQL_Stament_adj = "SELECT * from "+self.model+"KMKADJ where Date >='"+self.date_start+"' and Date <='"+self.date_end+"' and Time >= '"+self.time_start+"' and Time <= '"+self.time_end+"' "
            SQL_Stament_adj += "and (Coalesce( '"+self.line+"', '' )='' or Line = '"+self.line+"') "
            SQL_Stament_adj += " ORDER BY [No] DESC"

            data_raw = dataTable(conn_CVN_VENG, SQL_Stament)
            data_raw_adj = dataTable(conn_CVN_VENG, SQL_Stament_adj)

            kmk_conf = (("KMK CONFIRM",), ("SERIAL", "TIME", "RESULT", "RIB1U", "RIB1UL", "RIB2U", "RIB2UL", "RIB3U", "RIB3UL", "RIB4U", "RIB4UL", "RIB5U", "RIB5UL", "RIB6U", "RIB6UL", "RIB7U", "RIB7UL", "RIB8U", "RIB8UL"))
            kmk_adj = (("KMK ADJUST",), ("SERIAL", "TIME", "RESULT", "RIB2U", "RIB2UL", "RIB7U", "RIB7UL"))

            for d in range(len(data_raw)):
                data = ((data_raw[d]["SERIAL"], data_raw[d]["Time"], data_raw[d]["Result"], (data_raw[d]["Rib1U"]), (data_raw[d]["Rib1UL"]), (data_raw[d]["Rib2U"]), (data_raw[d]["Rib2UL"]), (data_raw[d]["Rib3U"]), (data_raw[d]["Rib3UL"]),
                        (data_raw[d]["Rib4U"]), (data_raw[d]["Rib4UL"]), (data_raw[d]["Rib5U"]), (data_raw[d]["Rib5UL"]), (data_raw[d]["Rib6U"]), (data_raw[d]["Rib6UL"]), (data_raw[d]["Rib7U"]), 
                        (data_raw[d]["Rib7UL"]), (data_raw[d]["Rib8U"]), (data_raw[d]["Rib8UL"])
                ),)
                kmk_conf += data
            
            for A in range(len(data_raw_adj)):
                data = ((data_raw_adj[A]["SERIAL"], data_raw_adj[A]["Time"], data_raw_adj[A]["Result"], 
                        (data_raw_adj[A]["Rib2U"]), (data_raw_adj[A]["Rib2Aori"]), (data_raw_adj[A]["Rib7U"]), (data_raw_adj[A]["Rib7Aori"])
                ),)
                kmk_adj += data

            #------------------------------------------------------------------------------------------------------------------
            #----------------------------------graph SCATTER RIB KMK CONFIRM---------------------------------------------------
            #------------------------------------------------------------------------------------------------------------------
            layout_ribupper_KMKC = layout_rib(min_s = self.min_spec, max_s = self.max_spec, bgcolor = "rgba(230, 221, 113, 0.8)")
            layout_ribAori_KMKC = layout_rib(min_s = self.min_spec, max_s = self.max_spec, bgcolor = 'rgba(147, 225, 235, 1.0)')
            fig_ribUpper = go.Figure(layout=layout_ribupper_KMKC)
            fig_ribAori = go.Figure(layout=layout_ribAori_KMKC)

            outspec_upper_kmkC = 0   
            outspec_aori_kmkC = 0                                #-----------return value out spec---------------
            
            value_upper_all = {"Rib1U":[],"Rib2U":[],"Rib3U":[],"Rib4U":[],"Rib5U":[],"Rib6U":[],"Rib7U":[],"Rib8U":[]}
            value_aori_all = {"Rib1UL":[],"Rib2UL":[],"Rib3UL":[],"Rib4UL":[],"Rib5UL":[],"Rib6UL":[],"Rib7UL":[],"Rib8UL":[]}
            for i in range(len(data_raw)):
                value_upper = []
                value_aori = []
                
                for j in range(len(rib_upper)):
                    if data_raw[i][rib_upper[j]] is not None:               #------------------------remove null value if PE1, MFE1 change tools----------------------
                        value_upper.append(float(data_raw[i][rib_upper[j]]))
                        value_upper_all[rib_upper[j]].append(float(data_raw[i][rib_upper[j]]))
                for k in range(len(rib_aori)):
                    if data_raw[i][rib_aori[k]] is not None:                #------------------------remove null value if PE1, MFE1 change tools----------------------
                        value_aori.append(float(data_raw[i][rib_aori[k]]))
                        value_aori_all[rib_aori[k]].append(float(data_raw[i][rib_aori[k]]))

                fig_ribUpper.add_trace(go.Scatter(x=rib_upper, y= value_upper, name= data_raw[i]["SERIAL"]))
                fig_ribAori.add_trace(go.Scatter(x=rib_aori, y= value_aori, name= data_raw[i]["SERIAL"]))

                if (check_outspec_ornot(value_upper, self.min_spec, self.max_spec)):       #-----------return value out spec rib upper---------------     
                    outspec_upper_kmkC += 1

                if (check_outspec_ornot(value_aori, self.min_spec, self.max_spec)):       #-----------return value out spec rib Aori---------------     
                    outspec_aori_kmkC = outspec_aori_kmkC +1

            
            fig_ribUpper.update_layout(title = "Total: "+str(len(data_raw))+ "    Out spec: "+ str(outspec_upper_kmkC))
            fig_ribAori.update_layout(title = "Total: "+str(len(data_raw))+ "    Out spec: "+ str(outspec_aori_kmkC))

            graph_upper = plot(fig_ribUpper, output_type='div')
            graph_aori = plot(fig_ribAori, output_type='div')

            #----------------------------------------------------------------------------------------------------------------
            #------------------------------------------graph rib KMK ADJUST--------------------------------------
            #----------------------------------------------------------------------------------------------------------------
            layout_ribupper_KMKA = layout_rib(min_s = self.min_spec, max_s = self.max_spec, bgcolor = "rgba(230, 221, 113, 0.8)")
            layout_ribAori_KMKA = layout_rib(min_s = self.min_spec, max_s = self.max_spec, bgcolor = 'rgba(147, 225, 235, 1.0)')
            fig_ribUpper_adj = go.Figure(layout=layout_ribupper_KMKA)                          
            fig_ribAori_adj = go.Figure(layout=layout_ribAori_KMKA)
            value_upper_adj = {"Rib2U":[],"Rib7U":[]}
            value_aori_adj = {"Rib2Aori":[],"Rib7Aori":[]}

            outspec_upper_kmka = 0   
            outspec_aori_kmka = 0                                #-----------return value out spec---------------

            for i in range(len(data_raw_adj)):
                value_upperadj = []
                value_aoriadj = []
                for j in range(len(rib_upper_adj)):
                    if data_raw_adj[i][rib_upper_adj[j]] is not None:                   #------------------------remove null value if PE1, MFE1 change tools----------------------
                        value_upperadj.append(float(data_raw_adj[i][rib_upper_adj[j]]))
                        value_upper_adj[rib_upper_adj[j]].append(float(data_raw_adj[i][rib_upper_adj[j]]))
                for k in range(len(rib_aori_adj)):
                    if data_raw_adj[i][rib_aori_adj[k]] is not None:                    #------------------------remove null value if PE1, MFE1 change tools----------------------
                        value_aoriadj.append(float(data_raw_adj[i][rib_aori_adj[k]]))
                        value_aori_adj[rib_aori_adj[k]].append(float(data_raw_adj[i][rib_aori_adj[k]]))

                fig_ribUpper_adj.add_trace(go.Scatter(x=rib_upper_adj, y= value_upperadj, name= data_raw_adj[i]["SERIAL"]))
                fig_ribAori_adj.add_trace(go.Scatter(x=rib_aori_adj, y= value_aoriadj, name= data_raw_adj[i]["SERIAL"]))

                if (check_outspec_ornot(value_upperadj, self.min_spec, self.max_spec)):       #-----------return value out spec rib upper---------------     
                    outspec_upper_kmka = outspec_upper_kmka + 1
                    
                if (check_outspec_ornot(value_upperadj, self.min_spec, self.max_spec)):       #-----------return value out spec rib Aori---------------     
                    outspec_aori_kmka = outspec_aori_kmka +1
            
            fig_ribUpper_adj.update_layout(title = "Total: "+str(len(data_raw_adj))+ "    Out spec: "+ str(outspec_upper_kmka))
            fig_ribAori_adj.update_layout(title = "Total: "+str(len(data_raw_adj))+ "    Out spec: "+ str(outspec_aori_kmka))
           

            graph_upper_adj = plot(fig_ribUpper_adj, output_type='div')
            graph_aori_adj = plot(fig_ribAori_adj, output_type='div')

            #-------------------------------config layout for rib ----------------------------------------------
            #------------------------------ADDING MIN, MAX, MEAN, SIGMA, 3SIGMA , CPL, CPK,.......-----------------
            layout_rib1u = Layout_histogram(value_upper_all["Rib1U"], self.min_spec, self.max_spec, "Rib1U")   
            layout_rib2u = Layout_histogram(value_upper_all["Rib2U"], self.min_spec, self.max_spec, "Rib2U")   
            layout_rib3u = Layout_histogram(value_upper_all["Rib3U"], self.min_spec, self.max_spec, "Rib3U")
            layout_rib4u = Layout_histogram(value_upper_all["Rib4U"], self.min_spec, self.max_spec, "Rib4U")
            layout_rib5u = Layout_histogram(value_upper_all["Rib5U"], self.min_spec, self.max_spec, "Rib5U")
            layout_rib6u = Layout_histogram(value_upper_all["Rib6U"], self.min_spec, self.max_spec, "Rib6U")
            layout_rib7u = Layout_histogram(value_upper_all["Rib7U"], self.min_spec, self.max_spec, "Rib7U")
            layout_rib8u = Layout_histogram(value_upper_all["Rib8U"], self.min_spec, self.max_spec, "Rib8U")   

            layout_rib1ul = Layout_histogram(value_aori_all["Rib1UL"], self.min_spec, self.max_spec, "Rib1UL")
            layout_rib2ul = Layout_histogram(value_aori_all["Rib2UL"], self.min_spec, self.max_spec, "Rib2UL")
            layout_rib3ul = Layout_histogram(value_aori_all["Rib3UL"], self.min_spec, self.max_spec, "Rib3UL")
            layout_rib4ul = Layout_histogram(value_aori_all["Rib4UL"], self.min_spec, self.max_spec, "Rib4UL")
            layout_rib5ul = Layout_histogram(value_aori_all["Rib5UL"], self.min_spec, self.max_spec, "Rib5UL")
            layout_rib6ul = Layout_histogram(value_aori_all["Rib6UL"], self.min_spec, self.max_spec, "Rib6UL")
            layout_rib7ul = Layout_histogram(value_aori_all["Rib7UL"], self.min_spec, self.max_spec, "Rib7UL")
            layout_rib8ul = Layout_histogram(value_aori_all["Rib8UL"], self.min_spec, self.max_spec, "Rib8UL")
            

            
            fig_histogram_rib1u = go.Figure(layout=layout_rib1u)
            fig_histogram_rib2u = go.Figure(layout=layout_rib2u)
            fig_histogram_rib3u = go.Figure(layout=layout_rib3u)
            fig_histogram_rib4u = go.Figure(layout=layout_rib4u)
            fig_histogram_rib5u = go.Figure(layout=layout_rib5u)
            fig_histogram_rib6u = go.Figure(layout=layout_rib6u)
            fig_histogram_rib7u = go.Figure(layout=layout_rib7u)
            fig_histogram_rib8u = go.Figure(layout=layout_rib8u)

            fig_histogram_rib1ul = go.Figure(layout=layout_rib1ul)
            fig_histogram_rib2ul = go.Figure(layout=layout_rib2ul)
            fig_histogram_rib3ul = go.Figure(layout=layout_rib3ul)
            fig_histogram_rib4ul = go.Figure(layout=layout_rib4ul)
            fig_histogram_rib5ul = go.Figure(layout=layout_rib5ul)
            fig_histogram_rib6ul = go.Figure(layout=layout_rib6ul)
            fig_histogram_rib7ul = go.Figure(layout=layout_rib7ul)
            fig_histogram_rib8ul = go.Figure(layout=layout_rib8ul)

            fig_histogram_rib1u.add_trace(go.Histogram(x= value_upper_all["Rib1U"]))
            fig_histogram_rib2u.add_trace(go.Histogram(x= value_upper_all["Rib2U"]))
            fig_histogram_rib3u.add_trace(go.Histogram(x= value_upper_all["Rib3U"]))
            fig_histogram_rib4u.add_trace(go.Histogram(x= value_upper_all["Rib4U"]))
            fig_histogram_rib5u.add_trace(go.Histogram(x= value_upper_all["Rib5U"]))
            fig_histogram_rib6u.add_trace(go.Histogram(x= value_upper_all["Rib6U"]))
            fig_histogram_rib7u.add_trace(go.Histogram(x= value_upper_all["Rib7U"]))
            fig_histogram_rib8u.add_trace(go.Histogram(x= value_upper_all["Rib8U"]))

            fig_histogram_rib1ul.add_trace(go.Histogram(x = value_aori_all["Rib1UL"]))
            fig_histogram_rib2ul.add_trace(go.Histogram(x = value_aori_all["Rib2UL"]))
            fig_histogram_rib3ul.add_trace(go.Histogram(x = value_aori_all["Rib3UL"]))
            fig_histogram_rib4ul.add_trace(go.Histogram(x = value_aori_all["Rib4UL"]))
            fig_histogram_rib5ul.add_trace(go.Histogram(x = value_aori_all["Rib5UL"]))
            fig_histogram_rib6ul.add_trace(go.Histogram(x = value_aori_all["Rib6UL"]))
            fig_histogram_rib7ul.add_trace(go.Histogram(x = value_aori_all["Rib7UL"]))
            fig_histogram_rib8ul.add_trace(go.Histogram(x = value_aori_all["Rib8UL"]))


            graph_histo_rib1u = plot(fig_histogram_rib1u, output_type="div")
            graph_histo_rib2u = plot(fig_histogram_rib2u, output_type="div")
            graph_histo_rib3u = plot(fig_histogram_rib3u, output_type="div")
            graph_histo_rib4u = plot(fig_histogram_rib4u, output_type="div")
            graph_histo_rib5u = plot(fig_histogram_rib5u, output_type="div")
            graph_histo_rib6u = plot(fig_histogram_rib6u, output_type="div")
            graph_histo_rib7u = plot(fig_histogram_rib7u, output_type="div")
            graph_histo_rib8u = plot(fig_histogram_rib8u, output_type="div")

            graph_histo_rib1ul = plot(fig_histogram_rib1ul, output_type="div")
            graph_histo_rib2ul = plot(fig_histogram_rib2ul, output_type="div")
            graph_histo_rib3ul = plot(fig_histogram_rib3ul, output_type="div")
            graph_histo_rib4ul = plot(fig_histogram_rib4ul, output_type="div")
            graph_histo_rib5ul = plot(fig_histogram_rib5ul, output_type="div")
            graph_histo_rib6ul = plot(fig_histogram_rib6ul, output_type="div")
            graph_histo_rib7ul = plot(fig_histogram_rib7ul, output_type="div")
            graph_histo_rib8ul = plot(fig_histogram_rib8ul, output_type="div")

            ##################################################################################################################################
            #---------------------------------------------------------------------------------------------------------------------------------
            layout_rib2u_adj = Layout_histogram(value_upper_adj["Rib2U"], self.min_spec, self.max_spec, "Rib2U") #-----layout KMK ADJUST-------  
            layout_rib7u_adj = Layout_histogram(value_upper_adj["Rib7U"], self.min_spec, self.max_spec, "Rib7U")
            layout_rib2ul_adj = Layout_histogram(value_aori_adj["Rib2Aori"], self.min_spec, self.max_spec, "Rib2UL")
            layout_rib7ul_adj = Layout_histogram(value_aori_adj["Rib7Aori"], self.min_spec, self.max_spec, "Rib7UL")

            

            fig_histogram_rib2u_adj = go.Figure(layout=layout_rib2u_adj) #------------Histogram KMK adjust-------------
            fig_histogram_rib7u_adj = go.Figure(layout=layout_rib7u_adj)
            fig_histogram_rib2ul_adj = go.Figure(layout=layout_rib2ul_adj)
            fig_histogram_rib7ul_adj = go.Figure(layout=layout_rib7ul_adj)

            fig_histogram_rib2u_adj.add_trace(go.Histogram(x= value_upper_adj["Rib2U"]))
            fig_histogram_rib7u_adj.add_trace(go.Histogram(x= value_upper_adj["Rib7U"]))

            fig_histogram_rib2ul_adj.add_trace(go.Histogram(x = value_aori_adj["Rib2Aori"]))
            fig_histogram_rib7ul_adj.add_trace(go.Histogram(x = value_aori_adj["Rib7Aori"]))


            graph_histo_rib2u_adj = plot(fig_histogram_rib2u_adj, output_type="div")
            graph_histo_rib7u_adj = plot(fig_histogram_rib7u_adj, output_type="div")

            graph_histo_rib2ul_adj = plot(fig_histogram_rib2ul_adj, output_type="div")
            graph_histo_rib7ul_adj = plot(fig_histogram_rib7ul_adj, output_type="div")


            #----------------------------------------------------------------------------------------
            #----------------------------Function to draw differ-------------------------------------
            #----------------------------------------------------------------------------------------
            max_spec_differ = self.max_spec
            min_spec_differ = self.min_spec
            layout_differ_upper = layout_rib(bgcolor="rgba(230, 221, 113, 0.8)", max_s=max_spec_differ, min_s=min_spec_differ)
            layout_differ_aori = layout_rib(bgcolor="rgba(147, 225, 235, 1.0)", max_s=max_spec_differ, min_s=min_spec_differ)

            fig_differ_ribUpper = go.Figure()
            fig_differ_ribAori = go.Figure()

            items_notenough_2step = 0           # items lack of step KmK adjust (only use checker KMK confirm)
            list_serial_break_step = []
            out_spec_differUpper = 0
            out_spec_differAori = 0
            list_serial_fulldata = []
            list_time_kmKC = []
            list_time_kmKA = []
            list_differ_rib2u = []
            list_differ_rib7u = []
            list_differ_rib2ul = []
            list_differ_rib7ul = []

            serial_kmkc = filter_data(data_raw, 'SERIAL')    # return list distinct SERIAL
            for serial in serial_kmkc:
                data_in_kmkconfirm = list(filter(lambda x: x['SERIAL'] == serial, data_raw))          # return a list data of KMK confirm with "SERIAL"
                data_in_kmkadj = list(filter(lambda x: x['SERIAL'] == serial+"M", data_raw_adj))          # get data from data kmk adjust with 'SERIAL' of KMK confirm
                if (len(data_in_kmkadj)>0):
                    if (data_in_kmkadj[0]["Rib2U"] is not None and data_in_kmkconfirm[0]["Rib2U"] is not None):
                        differ_rib2U = float(format((float(data_in_kmkadj[0]["Rib2U"])-float(data_in_kmkconfirm[0]["Rib2U"])), ".3f" ) )        # differ value = kmkAdjust - kmkConfirm 
                        differ_rib7U = float(format((float(data_in_kmkadj[0]["Rib7U"])-float(data_in_kmkconfirm[0]["Rib7U"])) , ".3f")  )       # KMK ADJUST: get final data pass
                        differ_rib2Aori = float(format((float(data_in_kmkadj[0]["Rib2Aori"])-float(data_in_kmkconfirm[0]["Rib2UL"])), ".3f"))   # KMK CONFIRM: get first data fail/pass
                        differ_rib7Aori = float(format((float(data_in_kmkadj[0]["Rib7Aori"])-float(data_in_kmkconfirm[0]["Rib7UL"])),'.3f'))

                        list_differ_rib2u.append(differ_rib2U)
                        list_differ_rib7u.append(differ_rib7U)
                        list_differ_rib2ul.append(differ_rib2Aori)
                        list_differ_rib7ul.append(differ_rib7Aori)
                        list_time_kmKC.append(time_tango(data_in_kmkconfirm[0]["Date"], data_in_kmkconfirm[0]["Time"]) )

                        list_serial_fulldata.append(serial)

                        data_differ_upper = [differ_rib2U, differ_rib7U]
                        data_differ_aori = [differ_rib2Aori, differ_rib7Aori]

                        #fig_differ_ribUpper.add_trace(go.Scatter(x=['Rib2U_differ', 'Rib7U_differ'], y= data_differ_upper, name = serial))
                        #fig_differ_ribAori.add_trace(go.Scatter(x=['Rib2UL_differ', 'Rib7UL_differ'], y= data_differ_aori, name = serial))
                        
                        #if (check_outspec_ornot(data_differ_upper, min_spec_differ, max_spec_differ)):
                        #    out_spec_differUpper +=1
                        #if (check_outspec_ornot(data_differ_aori, min_spec_differ, max_spec_differ)):
                        #    out_spec_differAori +=1

                else:
                    items_notenough_2step +=1  
                    list_serial_break_step.append(serial)           # return list items break step
            define_time_differ_rib2u = {}
            define_time_differ_rib7u = {}
            define_time_differ_rib2ul = {}
            define_time_differ_rib7ul = {}
            define_serial_differ_rib2u = {}
            define_serial_differ_rib7u = {}
            define_serial_differ_rib2ul = {}
            define_serial_differ_rib7ul = {}
            for t in range(len(list_time_kmKC)):
                define_time_differ_rib2u.update({list_time_kmKC[t]:list_differ_rib2u[t]})
                define_time_differ_rib7u.update({list_time_kmKC[t]:list_differ_rib7u[t]})
                define_time_differ_rib2ul.update({list_time_kmKC[t]:list_differ_rib2ul[t]})
                define_time_differ_rib7ul.update({list_time_kmKC[t]:list_differ_rib7ul[t]})

                define_serial_differ_rib2u.update({list_time_kmKC[t]:list_serial_fulldata[t]})
                define_serial_differ_rib7u.update({list_time_kmKC[t]:list_serial_fulldata[t]})
                define_serial_differ_rib2ul.update({list_time_kmKC[t]:list_serial_fulldata[t]})
                define_serial_differ_rib7ul.update({list_time_kmKC[t]:list_serial_fulldata[t]})
            
            new_list_time = sorted_and_return(define_time_differ_rib2u, define_serial_differ_rib2u)["key"]
            new_list_value_differ_rib2u = sorted_and_return(define_time_differ_rib2u, define_serial_differ_rib2u)["value"]
            new_list_serial = sorted_and_return(define_time_differ_rib2u, define_serial_differ_rib2u)["serial"]
            new_list_value_differ_rib7u = sorted_and_return(define_time_differ_rib7u, define_serial_differ_rib7u)["value"]
            new_list_value_differ_rib2ul = sorted_and_return(define_time_differ_rib2ul, define_serial_differ_rib2ul)["value"]
            new_list_value_differ_rib7ul = sorted_and_return(define_time_differ_rib7ul, define_serial_differ_rib7ul)["value"]

            fig_differ_ribUpper.add_trace(go.Scatter(x = new_list_time, y = new_list_value_differ_rib2u,  name = 'Differ Rib2U'))
            fig_differ_ribUpper.add_trace(go.Scatter(x = new_list_time, y = new_list_value_differ_rib7u,  name ="Differ Rib7U"))
            fig_differ_ribAori.add_trace(go.Scatter(y= new_list_value_differ_rib2ul, x = new_list_time, name = 'Differ Rib2UL'))
            fig_differ_ribAori.add_trace(go.Scatter(y= new_list_value_differ_rib7ul, x = new_list_time, name ="Differ Rib7UL"))
            
            fig_differ_ribUpper.update_layout(yaxis_range = [self.min_spec, self.max_spec])
            fig_differ_ribAori.update_layout(yaxis_range = [self.min_spec, self.max_spec])

            fig_differ_ribUpper.update_layout(title = "Total: "+ str(len(serial_kmkc))+"   Items lack of step: "+ str(items_notenough_2step))  
            fig_differ_ribAori.update_layout(title = "Total: "+ str(len(serial_kmkc))+"   Items lack of step: "+ str(items_notenough_2step))  


            
            annotation_upper = []
            for s in list_serial_break_step:
                annotation_upper.append(
                    dict(label=s,
                            method="update",
                            args=[{"visible": True},
                                {"title": "Total: "+ str(len(serial_kmkc))+"   Items lack of step: "+ str(items_notenough_2step),
                                    "annotations": []}]),
                )
            fig_differ_ribUpper.update_layout(
                            updatemenus=[
                                dict(active=0,
                                    buttons=list(annotation_upper))
                            ]
                        )

            annotation_aori = []
            for s in list_serial_break_step:
                annotation_aori.append(
                    dict(label=s,
                            method="update",
                            args=[{"visible": True},
                                {"title": "Total: "+ str(len(serial_kmkc))+"   Items lack of step: "+ str(items_notenough_2step),
                                    "annotations": []}]),
                )
            fig_differ_ribAori.update_layout(
                            updatemenus=[
                                dict(active=0,
                                    buttons=list(annotation_aori))
                            ]
                        )

            graph_differ_upper = plot(fig_differ_ribUpper, output_type='div')
            graph_differ_aori = plot(fig_differ_ribAori, output_type='div')

            # histogram differ

            layout_hist_rib2upper_differ = Layout_histogram(list_differ_rib2u, self.min_spec, self.max_spec, "Rib2U_differ")
            layout_hist_rib2aori_differ = Layout_histogram(list_differ_rib2ul, self.min_spec, self.max_spec, "Rib2UL_differ")
            layout_hist_rib7upper_differ = Layout_histogram(list_differ_rib7u, self.min_spec, self.max_spec, "Rib7U_differ")
            layout_hist_rib7aori_differ = Layout_histogram(list_differ_rib7ul, self.min_spec, self.max_spec, "Rib7UL_differ")

            fig_hist_rib2u_differ = go.Figure(layout= layout_hist_rib2upper_differ)
            fig_hist_rib2ul_differ = go.Figure(layout= layout_hist_rib2aori_differ)
            fig_hist_rib7u_differ = go.Figure(layout= layout_hist_rib7upper_differ)
            fig_hist_rib7ul_differ = go.Figure(layout= layout_hist_rib7aori_differ)

            fig_hist_rib2u_differ.add_trace(go.Histogram(x= list_differ_rib2u))
            fig_hist_rib7u_differ.add_trace(go.Histogram(x= list_differ_rib7u))
            fig_hist_rib2ul_differ.add_trace(go.Histogram(x= list_differ_rib2ul))
            fig_hist_rib7ul_differ.add_trace(go.Histogram(x= list_differ_rib7ul))

            

            graph_histo_rib2u_differ = plot(fig_hist_rib2u_differ, output_type="div")
            graph_histo_rib7u_differ = plot(fig_hist_rib7u_differ, output_type="div")

            graph_histo_rib2ul_differ = plot(fig_hist_rib2ul_differ, output_type="div")
            graph_histo_rib7ul_differ = plot(fig_hist_rib7ul_differ, output_type="div")

            #----------------------------------------------------------------
            # --------------------test error y plot--------------------------
            #----------------------------------------------------------------
            """
            fig_show_errorY_data_rib2u = go.Figure()

            for se in range(len(new_list_serial)):
                data_by_serial = list(filter(lambda x: x['SERIAL'] == new_list_serial[se], data_raw))  
                if (len(data_by_serial)>0):
                    
                    fig_show_errorY_data_rib2u.add_trace(go.Scatter(
                        x = [data_by_serial[0]["Time"]],
                        y = [float(data_by_serial[0]["Rib2U"])],
                        error_y=dict(
                                    type='data',
                                    symmetric=False,
                                    array=[new_list_value_differ_rib2u[se]],
                                  ),
                                  name = new_list_serial[se]
                                )
                    )
            
            graph_show_errorY_data_rib2u = plot(fig_show_errorY_data_rib2u, output_type="div")
            
            #--------------------------rib7u detail------------------------
            fig_show_errorY_data_rib7u = go.Figure()
            for ser in range(len(new_list_serial)):
                data_by_serial = list(filter(lambda x: x['SERIAL'] == new_list_serial[ser], data_raw))  
                if (len(data_by_serial)>0):
                    
                    fig_show_errorY_data_rib7u.add_trace(go.Scatter(
                        x = [data_by_serial[0]["Time"]],
                        y = [float(data_by_serial[0]["Rib2U"])],
                        error_y=dict(
                                    type='data',
                                    symmetric=False,
                                    array=[new_list_value_differ_rib7u[ser]],
                                  ),
                                  name = new_list_serial[ser]
                                )
                    )
            
            graph_show_errorY_data_rib7u = plot(fig_show_errorY_data_rib7u, output_type="div")

            """


            return [graph_upper, graph_aori, 
                    graph_histo_rib1u,graph_histo_rib2u,graph_histo_rib3u,graph_histo_rib4u,graph_histo_rib5u,graph_histo_rib6u,graph_histo_rib7u,graph_histo_rib8u,
                    graph_histo_rib1ul,graph_histo_rib2ul,graph_histo_rib3ul,graph_histo_rib4ul,graph_histo_rib5ul,graph_histo_rib6ul,graph_histo_rib7ul, graph_histo_rib8ul  ,
                    graph_upper_adj, graph_aori_adj,  
                    graph_histo_rib2u_adj, graph_histo_rib7u_adj,
                    graph_histo_rib2ul_adj, graph_histo_rib7ul_adj,
                    graph_differ_upper, graph_differ_aori,
                    graph_histo_rib2u_differ,graph_histo_rib7u_differ,graph_histo_rib2ul_differ,graph_histo_rib7ul_differ,
                    #graph_show_errorY_data_rib2u, graph_show_errorY_data_rib7u,
                    kmk_conf, kmk_adj
                        ]
    def KMK_byrib(self, rib):

        SQL_Stament1 = "SELECT * from "+self.model+"KMK where Date >='"+self.date_start+"' and Date <='"+self.date_end+"' and Time >= '"+self.time_start+"' and Time <= '"+self.time_end+"' "
        SQL_Stament1 += "and (Coalesce( '"+self.line+"', '' )='' or Line = '"+self.line+"') "
        SQL_Stament1 += " ORDER BY [No] ASC"

        SQL_Stament2_adj = "SELECT * from "+self.model+"KMKADJ where Date >='"+self.date_start+"' and Date <='"+self.date_end+"' and Time >= '"+self.time_start+"' and Time <= '"+self.time_end+"' "
        SQL_Stament2_adj += "and (Coalesce( '"+self.line+"', '' )='' or Line = '"+self.line+"') "
        SQL_Stament2_adj += " ORDER BY [No] ASC"
        #print(SQL_Stament)
        data_raw = dataTable(conn_CVN_VENG, SQL_Stament1)
        data_raw_adj = dataTable(conn_CVN_VENG, SQL_Stament2_adj)
        
        #------------------------------------------------------------------------------------------------------------------
        #----------------------------------graph SCATTER RIB KMK CONFIRM---------------------------------------------------
        #------------------------------------------------------------------------------------------------------------------
        layout_rib_KMKC = layout_rib(min_s = self.min_spec, max_s = self.max_spec, bgcolor = "rgba(230, 221, 113, 0.8)")
        # layout_ribAori_KMKC = layout_rib(min_s = self.min_spec, max_s = self.max_spec, bgcolor = 'rgba(147, 225, 235, 1.0)')
        fig_ribUpper = go.Figure(layout=layout_rib_KMKC)
        # fig_ribAori = go.Figure(layout=layout_ribAori_KMKC)

        value_ribKMKconfirm_all = {rib:{},rib+'L':[]}                 #------------DATA FOR RIB HISTOGRAM CHART (use multiple time, no reset)------------
        
        list_val_datetime = []
        list_val_ribupper_kmkc = []
        list_val_ribaori_kmkc = []


        outspec_upper_kmkC = 0   
        outspec_aori_kmkC = 0                                #-----------return value out spec---------------
        for i in range(len(data_raw)):
            list_val_datetime.append(time_tango( data_raw[i]["Date"], data_raw[i]["Time"]))
            list_val_ribupper_kmkc.append(float(data_raw[i][rib]))
            list_val_ribaori_kmkc.append(float(data_raw[i][rib+"L"]))
            
            if ((float(data_raw[i][rib]) > self.max_spec) or ( float(data_raw[i][rib]) < self.min_spec)):       #-----------return value out spec rib upper---------------     
                outspec_upper_kmkC += 1
                
            if ((float(data_raw[i][rib+"L"]) > self.max_spec) or (float(data_raw[i][rib+"L"]) < self.min_spec)):       #-----------return value out spec rib Aori---------------     
                outspec_aori_kmkC = outspec_aori_kmkC +1
          
        fig_ribUpper.add_trace(go.Scatter(x=list_val_datetime, y = list_val_ribupper_kmkc, name=rib))
        fig_ribUpper.add_trace(go.Scatter(x=list_val_datetime, y = list_val_ribaori_kmkc, name=rib+"L"))
        fig_ribUpper.update_layout(title = "Total: "+str(len(data_raw))+ "    Out spec: "+ str(outspec_upper_kmkC))
        # fig_ribAori.update_layout(title = "Total: "+str(len(data_raw))+ "    Out spec: "+ str(outspec_aori_kmkC))

        graph_kmkc = plot(fig_ribUpper, output_type='div')

        # Histogram kmk confirm 
        layout_ribupper = Layout_histogram(list_val_ribupper_kmkc, self.min_spec, self.max_spec, rib) #-----layout KMK CONFIRM-------  
        layout_ribaori = Layout_histogram(list_val_ribaori_kmkc, self.min_spec, self.max_spec, rib+"L")
        fig_histogram_ribupper = go.Figure(layout=layout_ribupper) #------------Histogram KMK confirm--------------
        fig_histogram_ribaori = go.Figure(layout=layout_ribaori)

        fig_histogram_ribupper.add_trace(go.Histogram(x=list_val_ribupper_kmkc))
        fig_histogram_ribaori.add_trace(go.Histogram(x=list_val_ribaori_kmkc))

        graph_histo_ribupper_kmkc = plot(fig_histogram_ribupper, output_type="div")
        graph_histo_ribaori_kmkc = plot(fig_histogram_ribaori, output_type="div")

        

        if ((rib=="Rib2U") or (rib == "Rib7U")):

            # --------------------------------------------------------------KMK ADJUST------------------------------------------------------------------------------------
            layout_rib_KMKadj = layout_rib(min_s = self.min_spec, max_s = self.max_spec, bgcolor = "rgba(147, 225, 235, 1.0)")
            # layout_ribAori_KMKC = layout_rib(min_s = self.min_spec, max_s = self.max_spec, bgcolor = 'rgba(147, 225, 235, 1.0)')
            fig_ribkmkadj = go.Figure(layout=layout_rib_KMKadj)

            list_val_datetime_kmkadj = []
            list_val_ribupper_kmkadj = []
            list_val_ribaori_kmkadj = []


            outspec_upper_kmkadj = 0   
            outspec_aori_kmkadj = 0                                #-----------return value out spec---------------
            for i in range(len(data_raw_adj)):
                list_val_datetime_kmkadj.append(time_tango( data_raw_adj[i]["Date"], data_raw_adj[i]["Time"]))
                list_val_ribupper_kmkadj.append(float(data_raw_adj[i][rib]))
                list_val_ribaori_kmkadj.append(float(data_raw_adj[i][rib[0:4]+"Aori"]))
                
                if ((float(data_raw_adj[i][rib]) > self.max_spec) or ( float(data_raw_adj[i][rib]) < self.min_spec)):       #-----------return value out spec rib upper---------------     
                    outspec_upper_kmkadj += 1
                    
                if ((float(data_raw_adj[i][rib[0:4]+"Aori"]) > self.max_spec) or (float(data_raw_adj[i][rib[0:4]+"Aori"]) < self.min_spec)):       #-----------return value out spec rib Aori---------------     
                    outspec_aori_kmkadj = outspec_aori_kmkadj +1
            
            fig_ribkmkadj.add_trace(go.Scatter(x=list_val_datetime_kmkadj, y = list_val_ribupper_kmkadj, name=rib))
            fig_ribkmkadj.add_trace(go.Scatter(x=list_val_datetime_kmkadj, y = list_val_ribaori_kmkadj, name=rib[0:4]+"Aori"))
            fig_ribkmkadj.update_layout(title = "Total: "+str(len(data_raw))+ "    Out spec: "+ str(outspec_upper_kmkadj+outspec_aori_kmkadj))
            # fig_ribAori.update_layout(title = "Total: "+str(len(data_raw))+ "    Out spec: "+ str(outspec_aori_kmkC))

            graph_kmkadj = plot(fig_ribkmkadj, output_type='div')

             # --------------------------------------Histogram kmk adjust --------------------------------------------------------------------------------------
            layout_ribupper_adj = Layout_histogram(list_val_ribupper_kmkadj, self.min_spec, self.max_spec, rib) #-----layout KMK CONFIRM-------  
            layout_ribaori_adj = Layout_histogram(list_val_ribaori_kmkadj, self.min_spec, self.max_spec, rib+"L")
            fig_histogram_ribupper_adj = go.Figure(layout=layout_ribupper_adj) #------------Histogram KMK confirm--------------
            fig_histogram_ribaori_adj = go.Figure(layout=layout_ribaori_adj)

            fig_histogram_ribupper_adj.add_trace(go.Histogram(x=list_val_ribupper_kmkadj))
            fig_histogram_ribaori_adj.add_trace(go.Histogram(x=list_val_ribaori_kmkadj))

            graph_histo_ribupper_kmkadj = plot(fig_histogram_ribupper_adj, output_type="div")
            graph_histo_ribaori_kmkadj = plot(fig_histogram_ribaori_adj, output_type="div")

            return [graph_kmkc, graph_histo_ribupper_kmkc, graph_histo_ribaori_kmkc, graph_kmkadj, graph_histo_ribupper_kmkadj, graph_histo_ribaori_kmkadj]
            
        else:
            return [graph_kmkc, graph_histo_ribupper_kmkc, graph_histo_ribaori_kmkc]
        
