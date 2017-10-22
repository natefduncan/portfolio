import os

os.chdir("/Users/Nathan/Desktop/Programming/")

import pandas as pd
import datetime as dt
import seaborn as sns
import numpy as np
import warnings
from ggplot import *

warnings.simplefilter("ignore")

class bcolors: #This allows for changes to terminal print output. 
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Read in CSV file. 

hours = pd.read_csv("hours.csv")

####Functions used in the Program####

#This function changes the dates to a sortable time. 
def cor_dates(df): 
    dates = list(df.Date)

    for x in range(len(list(df.Date))):
        dates[x] = dt.datetime.strftime(dt.datetime.strptime(dates[x], "%m/%d/%y"), "%m/%d/%y")

    df.Date = dates #Corrects csv date format error to make them all the same & sortable

cor_dates(hours)

#This function gives daily, weekly, and monthly means, sums, and counts. 
def proj_stats(project, x, days):
    dates = hours[hours.Project == project].Date.unique()

    dates_ord = []

    for i in range(len(dates)-1, -1, -1):
        dates_ord.append(dt.datetime.strptime(dates[i], "%m/%d/%y").toordinal())
    
    dates_ord = np.asarray(dates_ord) 

    now_start = dt.datetime.now()
    date = "%s/%s/%s" % (now_start.month, now_start.day, str(now_start.year)[2:4])
    today_ord = dt.datetime.strptime(date, "%m/%d/%y").toordinal()

    durs = hours.groupby(["Project", 'Date'])['Duration'].sum()[["%s" % project]].tolist()
    durs = np.asarray(durs)[::-1] #To array and reverse order. 
    
    if x.lower() == "count":
        #Days Count
        print "Worked on %s" % project, sum(dates_ord > today_ord - days), "of the last %s days" % days 
    elif x.lower() == "sum":
        #Days Total
        print "Worked on %s" % project, round(durs[dates_ord > today_ord - days].sum(), 2), "hours in the last %s days" % days 
    elif x.lower() == "mean":
        #Daily mean for days
        print "Worked on %s an average of" % project, round(durs[dates_ord > today_ord - days].mean(), 2), "hours per day for the last %s days" % days   #Gives counts, sums, means for projects.  
    
#Shows day streak.     
def streak(project):
    dates = hours[hours.Project == project].Date.unique()

    dates_ord = []

    for i in range(len(dates)-1, -1, -1):
        dates_ord.append(dt.datetime.strptime(dates[i], "%m/%d/%y").toordinal())

    now_start = dt.datetime.now()
    date = "%s/%s/%s" % (now_start.month, now_start.day, str(now_start.year)[2:4])
    today_ord = dt.datetime.strptime(date, "%m/%d/%y").toordinal()

    streak = []

    if today_ord == dates_ord[0]:
        for ord in dates_ord:
            streak.append(today_ord == ord)
            today_ord = today_ord - 1
        print streak.index(False), "day(s) in a row (including today)"    

    else:
        for ord in dates_ord:
            today_ord = today_ord - 1
            streak.append(today_ord == ord)
        print streak.index(False), "day(s) in a row (not including today)" #Shows day streak for project. 

#Takes a military clock time and add duration (hours) to ouput new clock time. 
def add_time(time, duration):
    
    duration = float(duration)
    
    hours = int(duration - duration % 1)
    minutes = int((duration % 1) * 60)
    
    hour_hand = int(time.split(":")[0]) + hours
    minute_hand = int(time.split(":")[1]) + minutes
    
    if hour_hand > 24:
        hour_hand = hour_hand - 24

    if minute_hand > 60:
        hour_hand = int(hour_hand) + 1
        minute_hand = minute_hand - 60
    
    if minute_hand < 10:
        minute_hand = "0" + str(int(minute_hand))

    if hour_hand < 10:
        hour_hand = "0" + str(int(hour_hand))
    
    return "%s:%s:%s" % (hour_hand, minute_hand, "00")

print 30 * "-"
print 30 * ""
print 10 * "", bcolors.BOLD + "TIME TRACKER" + bcolors.ENDC
print 30 * ""
print 30 * "-"

while True: 
    print 30 * ""
    print bcolors.BOLD + "Existing Projects: " + bcolors.ENDC
    print 30 * ""
    for i in sorted(hours.Project[hours.Type == 'Current'].unique()):
        print i
    print 30 * ""
    print 30 * ""
    
    print bcolors.BOLD + "Archived Projects: " + bcolors.ENDC
    print 30 * ""
    for i in sorted(hours.Project[hours.Type == 'Archived'].unique()):
        print i
    print 30 * ""

#Get the Project.

    existing_projects = hours.Project.unique()
 
    project = raw_input("Project: ")

    while True:
        if project in hours.Project.unique(): 
            break
        elif project not in hours.Project.unique():
            new = raw_input ("Do you want to create a new project? (y/n) ")
            if new == "y": 
                break
            elif new == "n": 
                project = raw_input("Project: ")
                print 30 * ""
            

    var1 = raw_input("Input: ").lower()        

    while True:
        if var1 == "start":
            now_start = dt.datetime.now()
            date = "%s/%s/%s" % (now_start.month, now_start.day, str(now_start.year)[2:4])
            start = "%s:%s:%s" % (now_start.hour, now_start.minute, now_start.second) #Get the start time
            print 30 * ""
            print "Timer Started"
            print 30 * ""
            var1 = raw_input("Input: ").lower()
            
        elif var1 == "archive":
            ind = np.where(hours.Project == project)[0].tolist()
            for i in ind: 
                hours[i:i+1][[5]] = "Archived"
            hours.to_csv("hours.csv", sep = ",", index = False) #update csv
            hours = pd.read_csv("hours.csv") #update dataframe
            cor_dates(hours) #Correct the dates
            print 30 * ""
            print "Project Archived"
            print 30 * ""
            agg_proj = hours.groupby(["Project"])['Duration'].sum()[["%s" % project]]
            print agg_proj
            print 30 * ""
            break
        
        elif var1 == "current":
            ind = np.where(hours.Project == project)[0].tolist()
            for i in ind:
                hours[i:i+1][[5]] = "Current"
            hours.to_csv("hours.csv", sep = ",", index = False) #update csv
            hours = pd.read_csv("hours.csv") #update dataframe
            cor_dates(hours) #Correct the dates. 
            print 30 * ""
            print "Project Current" 
            print 30 * ""
            break
        
        elif var1 == "show":
            now_show = dt.datetime.now()
            show = "%s:%s:%s" % (now_show.hour, now_show.minute, now_show.second)
            dur = dt.datetime.strptime(show, '%H:%M:%S') - dt.datetime.strptime(start, '%H:%M:%S')
            duration = dur.seconds / float(3600)
            duration = "%.2f" % duration
            print 30 * ""
            print "Been working on %s for %s hours." % (project, duration)
            print 30 * ""
            var1 = raw_input("Input: ").lower()
            
        elif var1 == "stop":
            now_end = dt.datetime.now()
            end = "%s:%s:%s" % (now_end.hour, now_end.minute, now_end.second) #Get the end time
            dur = dt.datetime.strptime(end, '%H:%M:%S') - dt.datetime.strptime(start, '%H:%M:%S') #Get Duration
            duration = dur.seconds / float(3600) #As a percentage of hour
            duration = "%.2f" % duration #Rounded to two decimal places
            hours.loc[len(hours)] = [project, date, start, end, duration, "Current"] #Add Data lines to end of Dataframe
            hours.to_csv("hours.csv", sep = ",", index = False)
            hours = pd.read_csv("hours.csv")
            cor_dates(hours) #Correct the dates. 
            print 30 * ""
            print "Worked on %s for %s hours." % (project, duration)
            print 30 * ""
            var1 = raw_input("Input: ").lower() 
        
        elif var1 == "list":
            print 30 * "-"
            agg_proj = hours.groupby(["Project", 'Date'])['Duration'].sum()[["%s" % project]]
            print agg_proj
            print 30 * ""
            var1 = raw_input("Input: ").lower()
            
        elif var1 == "total":
            print 30 * ""
            agg_proj = hours.groupby(["Project"])['Duration'].sum()[["%s" % project]]
            print agg_proj
            print 30 * ""
            var1 = raw_input("Input: ").lower()
        
        elif var1 == "streak":
            print 30 * ""
            streak(project)
            print 30 * ""
            var1 = raw_input("Input: ").lower()
            
        elif var1[0] == "(":
            temp = var1.split(",")
            x = temp[0][1:]
            days = int(temp[1][:-1])
            print 30 * ""
            if (x not in ['count', 'sum', 'mean']):
                print "Valid input is (x, days) where x = 'count', 'sum', or 'mean'." 
            else:
                proj_stats(project, x, days)
            print 30 * ""
            var1 = raw_input("Input: ").lower()
            
        elif var1 == "break":
            break
        
        elif var1 == "plot":
            index = range(0,len(hours))
            temp = pd.DataFrame({"Index" : index, "Duration" : hours.Duration, "Project" : hours.Project})
            (ggplot(temp, aes(x = "Index", y = "Duration", color = "Project")) + geom_point(size = 20) + theme_bw()).show()
            var1 = raw_input("Input: ").lower()
            
        elif var1 == "insert":
            print 30 * ""
            date = raw_input("Date (Example: 07/05/1995): ")
            print 30 * ""
            date = dt.datetime.strftime(dt.datetime.strptime(date, "%m/%d/%Y"), "%m/%d/%y")
            time_started = raw_input("Time Started (Military): ")
            time_started = time_started + ":00"
            print 30 * ""
            dur = raw_input("Duration (Hours): ")
            print 30 * ""
            time_ended = add_time(time_started, dur)
            hours.loc[len(hours)] = [project, date, time_started, time_ended, dur, "Current"] #Add Data lines to end of Dataframe
            hours.to_csv("hours.csv", sep = ",", index = False)
            hours = pd.read_csv("hours.csv")
            cor_dates(hours)
            print "Activity added."
            print 30 * ""
            var1 = raw_input("Input: ").lower()
          
        else: 
            print "Invalid Input"
            print 30 * ""
            var1 = raw_input("Input: ").lower()

#Write back to CSV. 

    hours.to_csv("hours.csv", sep = ",", index = False)
    hours = pd.read_csv("hours.csv")
    cor_dates(hours)
    print 30 * ""
    print 30 * "-"
    print 30 * ""
    if raw_input("Another project? (y/n) ") == "n":
        break


#Further Additions:

#Data Visualization. 

