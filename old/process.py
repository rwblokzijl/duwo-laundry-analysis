#!/usr/bin/env python3

import csv
import datetime
import pandas
import statistics

data = pandas.read_csv("availability.csv").values

print(type(data))

# list(list(int))


# for every month
#     for every weekday
#         for every 5 minutes

# month(weekday(5minslot()))


months = [1, 2, 3, 4, 5]
# daysOfWeek = [0, 1, 2, 3, 4, 5, 6]
daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
weekend_days = ["Saturday", "Sunday"]

processed_data_washer = {}
processed_data_dryer = {}

processed_data_average = {}


def init():
    for month in months:
        processed_data_washer[month] = {}
        processed_data_dryer[month] = {}
        processed_data_average[month] = {}
        for dayOfWeek in ["weekend", "weekday"]:
            processed_data_washer[month][dayOfWeek] = {}
            processed_data_dryer[month][dayOfWeek] = {}
            processed_data_average[month][dayOfWeek] = {}


def roundTime(dt=None, roundTo=300):
   """Round a datetime object to any time lapse in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)


def loop():
    i = 0
    for date_time_str, washers, dryers in data:
        # 2019/06/06 23:40:06
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y/%m/%d %H:%M:%S')

        month = date_time_obj.month
        dayOfWeek = daysOfWeek[date_time_obj.weekday()]
        timeOfDay = roundTime(date_time_obj).time()

        if month not in [1, 2, 3, 4, 5]:
            continue

        addDataPoint(month, dayOfWeek, timeOfDay, washers, dryers)

        # print(i)
        # print(date_time_obj)
        # print(month)
        # print(dayOfWeek)
        # print(timeOfDay.time())

        # i += 1

        # print(dryers)


def addDataPoint(month, dayOfWeek, timeOfDay, washers, dryers):
    if dayOfWeek in week_days:
        dayOfWeek = "weekday"
    else:
        dayOfWeek = "weekend"
    if timeOfDay not in processed_data_washer[month][dayOfWeek]:
        processed_data_washer[month][dayOfWeek][timeOfDay] = list()
    if timeOfDay not in processed_data_dryer[month][dayOfWeek]:
        processed_data_dryer[month][dayOfWeek][timeOfDay] = list()

    processed_data_washer[month][dayOfWeek][timeOfDay].append(washers)
    processed_data_dryer[month][dayOfWeek][timeOfDay].append(dryers)


def average():
    for month_id, month in processed_data_washer.items():
        for dayOfWeek, day in month.items():
            for time, slot in day.items():
                processed_data_average[month_id][dayOfWeek][time] = [str(time), str(statistics.mean(slot))]

    for month_id, month in processed_data_dryer.items():
        for dayOfWeek, day in month.items():
            for time, slot in day.items():
                processed_data_average[month_id][dayOfWeek][time].append(str(statistics.mean(slot)))


def write():
    for month_id, month in processed_data_dryer.items():
        for dayOfWeek, day in month.items():
            name = str(month_id) + "_" + dayOfWeek + "s.csv"
            header = ["time", "avg_washers", "avg_dryers"]
            with open(name, 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(header)
                for time, slot in day.items():
                    # writer.writerow(str(time) + ", " + processed_data_average[month_id][dayOfWeek][time])
                    # # print(str(time) + ", " + processed_data_average[month_id][dayOfWeek][time])
                    writer.writerow(processed_data_average[month_id][dayOfWeek][time])
                writeFile.close()


init()
loop()
average()
write()
