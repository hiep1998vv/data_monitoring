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



# --------------------------------------------------function for color ----------------------------------------------
def color_bychecker(checker):
    if (checker == 'VE'):
        return ['rgba(223, 84, 4, 1)', 'rgba(223, 84, 4, 1)']
    elif (checker == 'FINAL'):
        return ['rgba(106, 180, 140, 1)', 'rgba(106, 180, 140, 1)']
    elif (checker == 'KMK CONFIRM'):
        return ['rgba(39, 131, 245, 0.72)', 'rgba(39, 131, 245, 0.72)']
    elif (checker == 'KMK ADJUST'):
        return ['rgba(253, 187, 121, 1)', 'rgba(253, 187, 121, 1)']
    elif (checker == 'ISS'):
        return ['rgba(39, 131, 245, 1)', 'rgba(39, 131, 245, 1)']
    elif (checker == 'IMA'):
        return ['rgba(168, 121, 253, 1)', 'rgba(168, 121, 253, 1)']
    elif (checker == 'EMIP'):
        return ['rgba(168, 14, 176, 1.0)', 'rgba(168, 14, 176, 1.0)']
    elif (checker == 'EOS'):
        return ['rgba(14, 176, 171, 1.0)', 'rgba(14, 176, 171, 1.0)']
    elif (checker == 'IMA2'):
        return ['rgba(100, 0, 171, 1.0)', 'rgba(100, 0, 171, 1.0)']
    elif (checker == 'IMA-KMK'):
        return ['rgba(55, 181, 181, 1)', 'rgba(55, 181, 181, 1)']
    elif (checker == 'IMA VE ISS'):
        return ['rgba(0, 255, 181, 1)', 'rgba(0, 255, 181, 1)']
    elif (checker == 'KMKC'):
        return ['rgba(3, 91, 39, 1)', 'rgba(3, 91, 39, 1)']
    elif (checker == 'MTC'):
        return ['rgba(3, 179, 0, 1)', 'rgba(3, 179, 0, 1)']
  
#---------------------------------------------CLASS VISUALIZE DATA ----------------------------------------------------
class VisualizeData():
    def __init__(self, date_start, date_end, Model):
        self.__init__ = VisualizeData
        self.date_start = date_start
        self.date_end = date_end     
        self.model = Model
    
    def get_Data(self):

        date_list = date_range_list(self.date_start, self.date_end)
        sql_dataChecker = "select distinct Process from OPR where Date >= '"+str(self.date_start)+"' and Date <= '"+str(self.date_end)+"' and Model = '"+self.model+"' "
        Checker = dataTable(conn_CVN_VENG, sql_dataChecker)
        
        list_newdate_bychecker = []
        list_failrate_byChecker = []
        list_sum = []
        for i in range(len(Checker)):
            
            # -------------------------------define value ----------------------------
            
            data_OPR_byChecker = []
            new_dateList= []
            for date in date_list:
                
                # ----------------------------GET TOTAL ITEM OF MODEL-------------------------
                # Model data
                str_getdata = "select * from OPR where Date = '"+str(date)+"' and Model = '"+self.model+"'"
                data = dataTable(conn_CVN_VENG, str_getdata)          
                pass_bydate = 0           
                fail_bydate = 0
                if(len(data) > 0):
                    for a in range(len(data)):
                        pass_bydate += int(data[a]["Pass"])
                        fail_bydate += int(data[a]["Fail"])
                totalItem = pass_bydate + fail_bydate
                if (totalItem > 20):
                    totalFailRate = 100*fail_bydate/totalItem
                    list_sum.append(totalFailRate)


                #str_checkdate = "select * from OPR where Date = '"+str(date)+"' and Model = '"+self.model+"' and Process = '"+Checker[i]["Process"]+"'"
                #checkDate = dataTable(conn_CVN_VENG, str_checkdate)
                checkDate = list(filter(lambda x: x['Process'] == Checker[i]["Process"], data))
                if (len(checkDate) > 0):
                    passItem = 0
                    failItem = 0
                    for k in range(len(checkDate)):
                        datapass = checkDate[k]["Pass"]
                        passItem += int(datapass)
                        datafail = checkDate[k]["Fail"]
                        failItem += int(datafail)
                    failRate = float(str(format((100*int(failItem)/totalItem), ".2f")))
                    if (totalItem >20):
                        data_OPR_byChecker.append(failRate)
                        new_dateList.append(str(date))
            list_newdate_bychecker.append(new_dateList)
            list_failrate_byChecker.append(data_OPR_byChecker)

        return [Checker, list_newdate_bychecker, list_failrate_byChecker, list_sum]
    
    def OPR_Bymodel(self):
        
            # -------------------------------DEFINE VALUE FOR VISUALIZE ------------------------------
            list_passRateF58_bydate = []
            
            totalPassF58 = 0
            totalFailF58 = 0 

            list_passRateF36_bydate = []
            totalPassF36 = 0
            totalFailF36 = 0

            list_passRateG29_bydate = []
            totalPassG29 = 0
            totalFailG29 = 0
            # ---------------------------------GET DATA FROM SQL SERVER.OPR ------------------------
            date_list = date_range_list(self.date_start, self.date_end)
            new_dateListF58 = []
            new_dateListF36 = []
            new_dateListG29 = []
            for date in date_list:
                # F58 data
                str_getdata = "select * from OPR where Date = '"+str(date)+"' and Model = 'F58'"
                dataF58 = dataTable(conn_CVN_VENG, str_getdata)          
                passF58_bydate = 0           
                failF58_bydate = 0
                if(len(dataF58) > 0):
                    for i in range(len(dataF58)):
                        passF58_bydate += int(dataF58[i]["Pass"])
                        failF58_bydate += int(dataF58[i]["Fail"])
                    passRateF58 = float(str(format((100*int(passF58_bydate)/(int(passF58_bydate)+int(failF58_bydate))), ".2f")))
                    list_passRateF58_bydate.append(passRateF58)
                    new_dateListF58.append(date)
                totalPassF58 += passF58_bydate
                totalFailF58 += failF58_bydate
                
                # E91 data
                str_getdata = "select * from OPR where Date = '"+str(date)+"' and Model = 'F36'"
                dataF36 = dataTable(conn_CVN_VENG, str_getdata)          
                passF36_bydate = 0           
                failF36_bydate = 0
                if(len(dataF36) > 0):
                    for i in range(len(dataF36)):
                        passF36_bydate += int(dataF36[i]["Pass"])
                        failF36_bydate += int(dataF36[i]["Fail"])
                    passRateF36 = float(str(format((100*int(passF36_bydate)/(int(passF36_bydate)+int(failF36_bydate))), ".2f")))
                    list_passRateF36_bydate.append(passRateF36)
                    new_dateListF36.append(date)
                totalPassF36 += passF36_bydate
                totalFailF36 += failF36_bydate

                # G29 data
                str_getdata = "select * from OPR where Date = '"+str(date)+"' and Model = 'G29'"
                dataG29 = dataTable(conn_CVN_VENG, str_getdata)          
                passG29_bydate = 0           
                failG29_bydate = 0
                if(len(dataG29) > 0):
                    for i in range(len(dataG29)):
                        passG29_bydate += int(dataG29[i]["Pass"])
                        failG29_bydate += int(dataG29[i]["Fail"])
                    passRateG29 = float(str(format((100*int(passG29_bydate)/(int(passG29_bydate)+int(failG29_bydate))), ".2f")))
                    list_passRateG29_bydate.append(passRateG29)
                    new_dateListG29.append(date)
                totalPassG29 += passG29_bydate
                totalFailG29 += failG29_bydate

            PassRateF58_bymultipleDate = str(format((100*int(totalPassF58)/(int(totalFailF58)+int(totalPassF58))), ".2f"))
            PassRateF36_bymultipleDate = str(format((100*int(totalPassF36)/(int(totalFailF36)+int(totalPassF36))), ".2f"))
            PassRateG29_bymultipleDate = str(format((100*int(totalPassG29)/(int(totalFailG29)+int(totalPassG29))), ".2f"))

            fig = make_subplots(rows = 1, cols= 3, subplot_titles= ("F58 - TOTAL PASSRATE: " +PassRateF58_bymultipleDate, "F36 - TOTAL PASSRATE: "+PassRateF36_bymultipleDate, "G29 - TOTAL PASSRATE: "+PassRateG29_bymultipleDate))
            fig.add_trace(go.Scatter(x=new_dateListF58, y = list_passRateF58_bydate, name= "F58"), row=1, col=1)
            fig.add_trace(go.Scatter(x=new_dateListF36, y = list_passRateF36_bydate, name= "F36"), row=1, col=2)
            fig.add_trace(go.Scatter(x=new_dateListG29, y = list_passRateG29_bydate, name= "G29"), row=1, col=3)
            fig.update_layout(height = 600, width = 1800, title_text = "OPR DATA IN: "+ self.date_start + "-->" + self.date_end )
            graph1 = plot(fig, output_type='div')

            return graph1

    def visualize_Bymonth(self):
         # -------------------------------DEFINE VALUE FOR VISUALIZE ------------------------------
            list_passRateF58_bydate = []
            
            totalPassF58 = 0
            totalFailF58 = 0 

            list_passRateF36_bydate = []
            totalPassF36 = 0
            totalFailF36 = 0

            list_passRateG29_bydate = []
            totalPassG29 = 0
            totalFailG29 = 0
            # ---------------------------------GET DATA FROM SQL SERVER.OPR ------------------------
            date_list = date_range_list(self.date_start, self.date_end)
            new_dateListF58 = []
            new_dateListF36 = []
            new_dateListG29 = []
            for date in date_list:
                # F58 data
                str_getdata = "select * from OPR where Date = '"+str(date)+"' and Model = 'F58'"
                dataF58 = dataTable(conn_CVN_VENG, str_getdata)          
                passF58_bydate = 0           
                failF58_bydate = 0
                if(len(dataF58) > 0):
                    for i in range(len(dataF58)):
                        passF58_bydate += int(dataF58[i]["Pass"])
                        failF58_bydate += int(dataF58[i]["Fail"])
                    passRateF58 = float(str(format((100*int(passF58_bydate)/(int(passF58_bydate)+int(failF58_bydate))), ".2f")))
                    list_passRateF58_bydate.append(passRateF58)
                    new_dateListF58.append(date)
                totalPassF58 += passF58_bydate
                totalFailF58 += failF58_bydate
                
                # E91 data
                str_getdata = "select * from OPR where Date = '"+str(date)+"' and Model = 'F36'"
                dataF36 = dataTable(conn_CVN_VENG, str_getdata)          
                passF36_bydate = 0           
                failF36_bydate = 0
                if(len(dataF36) > 0):
                    for i in range(len(dataF36)):
                        passF36_bydate += int(dataF36[i]["Pass"])
                        failF36_bydate += int(dataF36[i]["Fail"])
                    passRateF36 = float(str(format((100*int(passF36_bydate)/(int(passF36_bydate)+int(failF36_bydate))), ".2f")))
                    list_passRateF36_bydate.append(passRateF36)
                    new_dateListF36.append(date)
                totalPassF36 += passF36_bydate
                totalFailF36 += failF36_bydate

                # G29 data
                str_getdata = "select * from OPR where Date = '"+str(date)+"' and Model = 'G29'"
                dataG29 = dataTable(conn_CVN_VENG, str_getdata)          
                passG29_bydate = 0           
                failG29_bydate = 0
                if(len(dataG29) > 0):
                    for i in range(len(dataG29)):
                        passG29_bydate += int(dataG29[i]["Pass"])
                        failG29_bydate += int(dataG29[i]["Fail"])
                    passRateG29 = float(str(format((100*int(passG29_bydate)/(int(passG29_bydate)+int(failG29_bydate))), ".2f")))
                    list_passRateG29_bydate.append(passRateG29)
                    new_dateListG29.append(date)
                totalPassG29 += passG29_bydate
                totalFailG29 += failG29_bydate

            PassRateF58_bymultipleDate = str(format((100*int(totalPassF58)/(int(totalFailF58)+int(totalPassF58))), ".2f"))
            PassRateF36_bymultipleDate = str(format((100*int(totalPassF36)/(int(totalFailF36)+int(totalPassF36))), ".2f"))
            PassRateG29_bymultipleDate = str(format((100*int(totalPassG29)/(int(totalFailG29)+int(totalPassG29))), ".2f"))

            fig = make_subplots(rows = 1, cols= 3, subplot_titles= ("F58 - TOTAL PASSRATE: " +PassRateF58_bymultipleDate, "F36 - TOTAL PASSRATE: "+PassRateF36_bymultipleDate, "G29 - TOTAL PASSRATE: "+PassRateG29_bymultipleDate))
            fig.add_trace(go.Scatter(x=new_dateListF58, y = list_passRateF58_bydate, name= "F58"), row=1, col=1)
            fig.add_trace(go.Scatter(x=new_dateListF36, y = list_passRateF36_bydate, name= "F36"), row=1, col=2)
            fig.add_trace(go.Scatter(x=new_dateListG29, y = list_passRateG29_bydate, name= "G29"), row=1, col=3)
            fig.update_layout(height = 600, width = 1800, title_text = "OPR DATA IN: "+ self.date_start + "-->" + self.date_end )
            graph1 = plot(fig, output_type='div')

            return graph1
    

    def visualize_ModelBymonth(self):
            date = datetime.date.today()

            datenow = str(date.strftime("%m/%Y"))
         # -------------------------------DEFINE VALUE FOR VISUALIZE ------------------------------
            list_passRate_bydate = []
            
            totalPass = 0
            totalFail = 0 
            # ---------------------------------GET DATA FROM SQL SERVER.OPR ------------------------
            date_list = date_range_list(self.date_start, self.date_end)
            new_dateList = []

            for date in date_list:
                # Model data
                str_getdata = "select Model, Pass, Fail from OPR where Date = '"+str(date)+"' and Model = '"+self.model+"'"
                data = dataTable(conn_CVN_VENG, str_getdata)          
                pass_bydate = 0           
                fail_bydate = 0
                if(len(data) > 0):
                    for i in range(len(data)):
                        pass_bydate += int(data[i]["Pass"])
                        fail_bydate += int(data[i]["Fail"])
                    totalItem = pass_bydate + fail_bydate
                    passRate = float(str(format((100*pass_bydate/totalItem), ".2f")))
                    
                    if (totalItem > 20):
                        list_passRate_bydate.append(passRate)                               # ----data for line OPR    
                        new_dateList.append(date)
                totalPass += pass_bydate
                totalFail += fail_bydate

            if (int(totalFail)+int(totalPass) > 0):
                PassRate_bymultipleDate = float(str(format((100*int(totalPass)/(int(totalFail)+int(totalPass))), ".2f")))
            else: 
                PassRate_bymultipleDate = 0
            # data for graph failrate checker
            totaldata_fail = self.get_Data()
            list_datelist_forProcess = totaldata_fail[1]
            list_byprocess = totaldata_fail[0]
            list_failrate_bychecker = totaldata_fail[2]
            if (len(totaldata_fail[3])>0):
                yaxis_Range = max(totaldata_fail[3])*1.5
            # graph for OPR data by month
            fig = go.Figure()
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=new_dateList, y = list_passRate_bydate, name= self.model +" PASS",
                                    mode= "lines+markers+text",
                                    text= [str(value) + '%' for value in list_passRate_bydate], 
                                    textposition= 'bottom center'
                                    ), secondary_y= True )
            for process_number in range(len(list_byprocess)):
                fig.add_trace(go.Bar(x=list_datelist_forProcess[process_number], y=list_failrate_bychecker[process_number],  #data
                                    name= list_byprocess[process_number]["Process"]+ " Fail",                                #lengend
                                    yaxis = 'y2',                                                                            #y axis define
                                    text= [str(value) +'%' for value in list_failrate_bychecker[process_number]],            #text for piont in graph
                                    textposition='inside',                                                                   #text position
                                    insidetextanchor = "middle",                                                             # "INSIDE" mode : "middle", "start", "end"
                                    textfont = dict(color = "rgb(255,255,255)"),                                             # define text font
                                    marker=dict(color= color_bychecker(list_byprocess[process_number]["Process"].strip())[0] ,       #define maker
                                                line=dict(color=color_bychecker(list_byprocess[process_number]["Process"].strip())[1], 
                                                width=2))
                                    
                                    ), secondary_y=False)
            if (len(list_passRate_bydate)>0):
                fig.update(layout_yaxis2_range=[min(list_passRate_bydate) - 10,101])
                fig.update(layout_yaxis_range=[0, yaxis_Range]) 
            fig.update_layout(barmode="relative", title =  'Data in: '+datenow  , margin=dict(
                                            t=35, # top margin: 30px, you want to leave around 30 pixels to
                                                # display the modebar above the graph.
                                            b=10, # bottom margin: 10px
                                            l=10, # left margin: 10px
                                            r=10, # right margin: 10px
                                            ),yaxis = dict(side ="right"),
                                             yaxis2 = dict(anchor="x",
                                                        overlaying="y",
                                                        side="left"),
                                            yaxis2_title = 'Avarage passrate (%)')

            graph = plot(fig, output_type='div')

            # graph for bar chart status
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(y=[''], x=[PassRate_bymultipleDate], text =str(PassRate_bymultipleDate)+ '%', name='Pass ratio', orientation='h',
                                marker=dict(color='rgba(60, 179, 113, 0.6)',line=dict(color='rgba(60, 178, 113, 1.0)', width=2))
                            ))
            fig1.add_trace(go.Bar(y=[''], x=[100-PassRate_bymultipleDate], name='Fail ratio', orientation='h',
                                marker=dict(color='rgba(246, 78, 139, 0.6)',line=dict(color='rgba(246, 78, 139, 1.0)', width=2))
                            ))

            fig1.update_layout(title = 'OPR Graph',height = 100 ,barmode='stack', margin=dict(
                                                                    t=35, # top margin: 30px, you want to leave around 30 pixels to
                                                                        # display the modebar above the graph.
                                                                    b=20, # bottom margin: 10px
                                                                    l=10, # left margin: 10px
                                                                    r=10, # right margin: 10px
                                                                    ),)
            graph_bar = plot(fig1, output_type='div')

            return [graph , graph_bar]         

    # ------------------------------------function display worst item by month ----------------------------------------
    def visualize_WorstItem_bymonth(self):   
        # data for graph
        list_failcode_byProcess = []
        newProcesslist =[]
        
        # get data from SQL server database
        str_wit = "select Process, FailCode, Quantity from WorstItem where Date >= '"+self.date_start+"' and Date <= '"+self.date_end+"' and model = '"+self.model+"' "
        data_wit = dataTable(conn_CVN_VENG, str_wit)
        Listprocess = filter_data(data_wit, "Process")
        
        for process in Listprocess:
            
            #if (process.strip() != 'KMK ADJUST'):
                newProcesslist.append(process.strip())
                data_wit_byProcess = list(filter(lambda x: x['Process'] == process, data_wit))
                List_Failcode = filter_data(data_wit_byProcess, "FailCode")
                Failcode_quantity = {}
                for failcode in List_Failcode:
                    failcodestrip = failcode.strip()
                    data_wit_byProcess_eachFailCode = list(filter(lambda x: x['FailCode'] == failcode, data_wit_byProcess))
                    total_quantity = 0
                    if (len(data_wit_byProcess_eachFailCode)>0):
                        for i in range(len(data_wit_byProcess_eachFailCode)):
                            total_quantity += int(data_wit_byProcess_eachFailCode[i]["Quantity"])
                    Failcode_quantity.update({failcodestrip : total_quantity})
                filter_threebigitem = Counter(Failcode_quantity).most_common(3)
                new_data = []
                a=[]
                b=[] 
                for item in filter_threebigitem:
                    a.append(process.strip() +" "+item[0]+" Fail")
                    b.append(item[1])
                new_data.append(a)
                new_data.append(b)
                
                list_failcode_byProcess.append(new_data)

        #print(self.date_start + '--->'+ self.date_end)
        fig = go.Figure()
        for num in range(len(newProcesslist)):
            fig.add_trace(go.Bar(x = list_failcode_byProcess[num][0], y = list_failcode_byProcess[num][1],
                                name = newProcesslist[num],
                                text = list_failcode_byProcess[num][1],
                                textposition= 'outside',
                                marker=dict(color= color_bychecker(newProcesslist[num])[0] ,line=dict(color=color_bychecker(newProcesslist[num])[1], width=2))
                                    ))
        fig.update_layout(barmode='group', margin=dict(
                                                        t=35, # top margin: 30px, you want to leave around 30 pixels to
                                                                # display the modebar above the graph.
                                                        b=20, # bottom margin: 10px
                                                        l=10, # left margin: 10px
                                                        r=10, # right margin: 10px
                                                        ),
                                        yaxis_title = 'Number of failcode')
        graph_wit = plot(fig,output_type='div')
        return graph_wit

    #----------------------------------------function display worst item in day ----------------------------------------    
    def visualize_WorstItem_today(self):   

        date = datetime.date.today()
        datenow = str(date.strftime("%Y-%m-%d"))

        # data for graph
        list_failcode_byProcess = []
        newProcesslist =[]
        
        # take data from SQL database
        str_wit = "select * from WorstItem where Date = '"+datenow+"' and model = '"+self.model+"' "
        data_wit = dataTable(conn_CVN_VENG, str_wit)
        Listprocess = filter_data(data_wit, "Process")
        
        for process in Listprocess:
            #if (process.strip() != 'KMK ADJUST'):
                newProcesslist.append(process.strip())
                data_wit_byProcess = list(filter(lambda x: x['Process'] == process, data_wit))
                List_Failcode = filter_data(data_wit_byProcess, "FailCode")
                Failcode_quantity = {}
                for failcode in List_Failcode:
                    failcodestrip = failcode.strip()
                    data_wit_byProcess_eachFailCode = list(filter(lambda x: x['FailCode'] == failcode, data_wit_byProcess))
                    total_quantity = 0
                    if (len(data_wit_byProcess_eachFailCode)>0):
                        for i in range(len(data_wit_byProcess_eachFailCode)):
                            total_quantity += int(data_wit_byProcess_eachFailCode[i]["Quantity"])
                    Failcode_quantity.update({failcodestrip : total_quantity})
                filter_threebigitem = Counter(Failcode_quantity).most_common(3)
                new_data = []
                a=[]
                b=[] 
                for item in filter_threebigitem:
                    a.append(process.strip() +" "+item[0]+" Fail")
                    b.append(item[1])
                new_data.append(a)
                new_data.append(b)
                
                list_failcode_byProcess.append(new_data)
        
        
        fig = go.Figure()
        for num in range(len(newProcesslist)):
            fig.add_trace(go.Bar(x = list_failcode_byProcess[num][0], y = list_failcode_byProcess[num][1], name = newProcesslist[num], 
                                  marker=dict(color= color_bychecker(newProcesslist[num])[0] ,line=dict(color=color_bychecker(newProcesslist[num])[1], width=2))  
                                    , text= list_failcode_byProcess[num][1], textposition= "outside"
                                    ))
        fig.update_layout(barmode='group', margin=dict(
                                                        t=35, # top margin: 30px, you want to leave around 30 pixels to
                                                                # display the modebar above the graph.
                                                        b=20, # bottom margin: 10px
                                                        l=10, # left margin: 10px
                                                        r=10, # right margin: 10px
                                                        ),
                                        yaxis_title = 'Number of failcode')
        graph_wit = plot(fig,output_type='div')
        return graph_wit

# -------------------------------------------FUNCTION VISUALIZE DATA TODAY---------------------------------------------------
    def liveOPR_byday(self):

        # -------------------------------DEFINE VALUE FOR VISUALIZE ------------------------------
            timedata = ''

            date = datetime.date.today()
            datenow = str(date.strftime("%Y-%m-%d"))

            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")

            # ---------------------------------GET DATA FROM SQL SERVER.OPR ------------------------
            passRate_Model_bydate = 0
             
            str_getdata = "select * from OPR where Date = '"+datenow+"' and Model = '"+self.model+"'"
            data_model_bydate = dataTable(conn_CVN_VENG, str_getdata)          
            pass_bydate = 0           
            fail_bydate = 0
            if(len(data_model_bydate) > 0):
                    for i in range(len(data_model_bydate)):
                        pass_bydate += int(data_model_bydate[i]["Pass"])
                        fail_bydate += int(data_model_bydate[i]["Fail"])
                    total = pass_bydate + fail_bydate
                    if (total > 20):
                        passRate_Model_bydate = float(str(format((100*int(pass_bydate)/(int(pass_bydate)+int(fail_bydate))), ".2f")))
              
             # graph for bar chart status
            fig_graphbar_OPR = go.Figure()
            fig_graphbar_OPR.add_trace(go.Bar(y=[''], x=[passRate_Model_bydate], text =str(passRate_Model_bydate)+ '%', name='Pass ratio', orientation='h',
                                marker=dict(color='rgba(60, 179, 113, 0.6)',line=dict(color='rgba(60, 178, 113, 1.0)', width=2))
                            ))
            fig_graphbar_OPR.add_trace(go.Bar(y=[''], x=[100-passRate_Model_bydate], name='Fail ratio', orientation='h',
                                marker=dict(color='rgba(246, 78, 139, 0.6)',line=dict(color='rgba(246, 78, 139, 1.0)', width=2))
                            ))

            fig_graphbar_OPR.update_layout(title = 'OPR Graph: '+datenow, height = 100 ,barmode='stack', margin=dict(
                                                                    t=35, # top margin: 30px, you want to leave around 30 pixels to
                                                                        # display the modebar above the graph.
                                                                    b=20, # bottom margin: 10px
                                                                    l=10, # left margin: 10px
                                                                    r=10, # right margin: 10px
                                                                    ),)
            graphbar_OPR = plot(fig_graphbar_OPR, output_type='div')

            # ---------------------data for failrate by checker -----------------------------------

            list_failrate_bychecker = {}
            dataFailrate = []
            datacheckerName = filter_data(data_model_bydate, "Process")
            for checker in datacheckerName:
                data_OPR_byProcess = list(filter(lambda x: x['Process'] == checker, data_model_bydate))
                failItem = 0
                
                if (len(data_OPR_byProcess)>0):
                    for row in range(len(data_OPR_byProcess)):
                        failItem += int(data_OPR_byProcess[row]["Fail"] )
                       
                    failRate = float(str(format((100*int(failItem)/total), ".2f")))
                if (total > 20):
                    dataFailrate.append(failRate)
                    list_failrate_bychecker.update({checker: failRate})
                    timedata = current_time
            
            
            return [passRate_Model_bydate, graphbar_OPR, list_failrate_bychecker, dataFailrate, timedata]

    def OPR_today(self):
        def return_value_from_dict(data):   # function change dict data to list data
            listkey = list(data.keys())
            listvalue = []
            for key in listkey:
                listvalue.append(float(data[key]))
            return [listkey, listvalue]
            
        def convert_data_to_dict(data):
            split_1 =data.split(',')
            key = []
            value = []
            dic = {}
            for i in split_1:
                if (i !=''):  
                    A = i.split('#')
                    key.append(A[0].strip())
                    value.append(A[1])
            for i in range(len(key)):
                dic.update({key[i]:value[i]})
            
            return [dic, key]
        
        date = datetime.date.today()
        datenow = str(date.strftime("%Y-%m-%d"))

        # get data from SQL server data
        str_getdata = "select * from data__today__visuallize where Date = '"+datenow+"' and Model = '"+self.model+"'"
        data_model_bydate = dataTable(conn_CVN_VENG, str_getdata)

        passrate = 0
        list_passrate = []
        failrate = 0
        list_failrate = []
        timedata = []
        checker_raw = []
        dictvalue_checker = {'IMA': {},'VE': {}, 'FINAL': {}, 'KMK CONFIRM': {}, 'KMK ADJUST': {}, 'ISS': {}, 'EMIP': {}, 'IMA2':{}, 'IMA-KMK':{}, 'KMKC':{},'EOS':{}, 'MTC':{}, 'IMA VE ISS':{}}

        for i in range(len(data_model_bydate)):
            passrate = float(data_model_bydate[i]['PassRate'])
            list_passrate.append(float(passrate))
            failrate = float(data_model_bydate[i]['FailRate'])
            list_failrate.append(float(failrate))
            timedata.append(data_model_bydate[i]['Time'])
            checker_raw += convert_data_to_dict(data_model_bydate[i]['FailRate_bychecker'])[1]


            #data for list checker failrate
            sm_dictFailRate = convert_data_to_dict(data_model_bydate[i]['FailRate_bychecker'])[0]

            listchecker_bytime = convert_data_to_dict(data_model_bydate[i]['FailRate_bychecker'])[1]
            for check in listchecker_bytime:
                dictvalue_checker[check.strip()].update({data_model_bydate[i]['Time']:sm_dictFailRate[check.strip()]})
        #print(passrate)
        list_checker = list(set(checker_raw))
        
        #---------------------------------------------------graph OPR---------------------------------------------
        fig_OPR_bydate = go.Figure()
        fig_OPR_bydate = make_subplots(specs=[[{"secondary_y": True}]])
        fig_OPR_bydate.add_trace(go.Scatter(x=timedata, y = list_passrate, name= self.model, mode="lines+markers+text",
                                    marker = dict(color= 'rgba(0, 0, 255, 0.69)' ,line=dict(color= 'rgba(0, 0, 255, 1.0)', width=4)),
                                    line = dict(color='royalblue', width=4), 
                                    #text= [str(value)+ '%' for value in dataF58],
                                    #textposition="bottom right"
                                        ),secondary_y= True)

        for checker_get in list_checker:
            #text_graphbar = [str(value) + '%' for value in return_value_from_dict(listvalue_checker_F58[checkerF58_get])[1]]
            fig_OPR_bydate.add_trace(go.Bar(x=return_value_from_dict(dictvalue_checker[checker_get])[0], y = return_value_from_dict(dictvalue_checker[checker_get])[1], name = checker_get, yaxis='y2',
                                                marker=dict(color= color_bychecker(checker_get.strip())[0] ,line=dict(color=color_bychecker(checker_get.strip())[1], width=2)) ,   
                                                #text=text_graphbar, textposition= "inside", insidetextanchor = "middle",
                                                #textfont = dict(color = "rgb(255,255,255)"),
                                                    ), secondary_y= False)
        if(len(timedata)>0):
            fig_OPR_bydate.update(layout_yaxis2_range=[min(list_passrate) - 10,101])        # define y axis range
            fig_OPR_bydate.update(layout_yaxis_range=[0,max(list_failrate)*1.5])            # define y axis 2 range
                     
        fig_OPR_bydate.update_layout(barmode="relative", margin=dict(
                                            t=35, # top margin: 30px, you want to leave around 30 pixels to
                                                # display the modebar above the graph.
                                            b=10, # bottom margin: 10px
                                            l=10, # left margin: 10px
                                            r=10, # right margin: 10px
                                            ),yaxis = dict(side ="right"),
                                             yaxis2 = dict(anchor="x",
                                                        overlaying="y",
                                                        side="left"),
                                            yaxis2_title = 'Avarage passrate (%)' , 
                                            yaxis_title = 'Avarage failrate each checker %')
        fig_OPR_bydate.update_xaxes(visible=False, showticklabels=False)
        graph_OPR_bydate = plot(fig_OPR_bydate, output_type='div')

        # graph for bar chart status
        fig_graphbar_OPR = go.Figure()
        fig_graphbar_OPR.add_trace(go.Bar(y=[''], x=[passrate], text =str(passrate)+ '%', name='Pass ratio', orientation='h',
                                marker=dict(color='rgba(60, 179, 113, 0.6)',line=dict(color='rgba(60, 178, 113, 1.0)', width=2))
                            ))
        fig_graphbar_OPR.add_trace(go.Bar(y=[''], x=[failrate], name='Fail ratio', orientation='h',
                                marker=dict(color='rgba(246, 78, 139, 0.6)',line=dict(color='rgba(246, 78, 139, 1.0)', width=2))
                            ))

        fig_graphbar_OPR.update_layout(title = 'OPR Graph: '+datenow, height = 100 ,barmode='stack', margin=dict(
                                                                    t=35, # top margin: 30px, you want to leave around 30 pixels to
                                                                        # display the modebar above the graph.
                                                                    b=20, # bottom margin: 10px
                                                                    l=10, # left margin: 10px
                                                                    r=10, # right margin: 10px
                                                                    ),)
        graphbar_OPR = plot(fig_graphbar_OPR, output_type='div')

        return [graphbar_OPR, graph_OPR_bydate]


