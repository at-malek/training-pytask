import sys
import csv
from os.path import exists
from colorama import Fore

MONTHS_LIST = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
EMPTY_HIGHEST = "Highest: No Record Found"
EMPTY_LOWEST = "Lowest: No Record Found"
EMPTY_HUMIDITY = "Humidity: No Record Found"
TEMP_HIGH_INDEX = 1
TEMP_LOW_INDEX = 3
HUMIDITY_HIGH_INDEX = 7
HUMIDITY_MEAN_INDEX = 8

highest = -100
lowest = 100
humidity = 0
highest_str = EMPTY_HIGHEST
lowest_str = EMPTY_LOWEST
humidity_str = EMPTY_HUMIDITY

high_count = 0
low_count = 0
hum_count = 0


def findRecords(filepath):

  if exists(filepath):
    file = open(filepath)
    csvreader = csv.reader(file)
    header = False

    for record in csvreader:
      if(len(record) != 23):
        continue
      if(header is False):
        header = True
        continue
      yield record

  else:
    yield None


def getDate(value):
  value = str(value).split("-")
  _month = MONTHS_LIST[int(value[1])-1]
  _day = value[2]
  _year = value[0]
  return _year, _month, _day.zfill(2)


def getTempAndHumidity(record):
  return str(record[TEMP_HIGH_INDEX]).strip(), str(record[TEMP_LOW_INDEX]).strip(), str(record[HUMIDITY_HIGH_INDEX]).strip(), str(record[HUMIDITY_MEAN_INDEX]).strip()


def isNotEmpty(item):
  return True if len(item)>0 else False


def getPlus(amount):
  s = ""
  for i in range(amount):
    s += "+"
  return s



def findYear(filename, months):

  global highest, lowest, humidity, highest_str, lowest_str, humidity_str
  fileExists = False

  for mon in months:
    current_month = filename + mon +".txt"
    records = findRecords(current_month)

    for current_record in records:
      fileExists = True
      _year, _month, _day = getDate(current_record[0])
      highest_temperature, lowest_temperature, humidity_highest, humidity_mean = getTempAndHumidity(current_record)

      if(isNotEmpty(highest_temperature)):
          if(int(highest_temperature) > highest):
            highest = int(highest_temperature)
            highest_str = "Highest: " + highest_temperature + "C on " + _month + " " + _day

      if (isNotEmpty(lowest_temperature)):
        if(int(lowest_temperature) < lowest):
          lowest = int(lowest_temperature)
          lowest_str = "Lowest: " + lowest_temperature + "C on " + _month + " " + _day

      if (isNotEmpty(humidity_highest)):
        if(int(humidity_highest) > humidity):
          humidity = int(humidity_highest)
          humidity_str = "Humid: " + humidity_highest + "% on " + _month + " " + _day

  if(fileExists):
    print(highest_str + "\n" + lowest_str + "\n" +humidity_str + "\n")
  else:
    print("The requested year has no entries (no files)")


def findAverageMonth(filename):


  global highest, lowest, humidity, highest_str, lowest_str, humidity_str, low_count, high_count, hum_count

  records = findRecords(filename)
  fileExists = False

  for current_record in records:
    fileExists = True
    _year, _month, _day = getDate(current_record[0])
    highest_temperature, lowest_temperature, humidity_highest, humidity_mean = getTempAndHumidity(current_record)
    if(isNotEmpty(highest_temperature)):
        if(high_count == 0):
          highest = int(highest_temperature)
          high_count += 1
        else:
          highest = ((highest*high_count) + int(highest_temperature))/(high_count+1)
          highest_str = "Highest Average: " + str("{:.2f}".format(highest)) + "C"
          high_count += 1

    if (isNotEmpty(lowest_temperature)):
      if(low_count == 0):
        lowest = int(lowest_temperature)
        low_count += 1
      else:
        lowest = ((lowest*low_count) + int(lowest_temperature))/(low_count+1)
        lowest_str = "Lowest Average: " + str("{:.2f}".format(lowest)) + "C"
        low_count += 1

    if (isNotEmpty(humidity_mean)):
      if(hum_count == 0):
        humidity = int(humidity_mean)
        hum_count += 1
      else:
        humidity = ((humidity*hum_count) + int(humidity_mean))/(hum_count+1)
        humidity_str = "Average Humidity: " + str("{:.2f}".format(humidity)) + "%"
        hum_count += 1

  if(fileExists):
   print(highest_str + "\n" + lowest_str + "\n" + humidity_str + "\n")
  else:
    print("The requested month has no file")


def findMonth(filename, month, year):

  global highest, lowest, humidity, highest_str, lowest_str, humidity_str
  records = findRecords(filename)
  fileExists = False
  print(MONTHS_LIST[month-1]  + " "  + str(year))
  for current_record in records:
    fileExists = True
    yr, mn, day = getDate(current_record[0])
    highest_temperature, lowest_temperature, highest_humidity, mean_humidity = getTempAndHumidity(current_record)
    if(isNotEmpty(highest_temperature)):
      print(day + " " + Fore.LIGHTRED_EX + getPlus(int(highest_temperature)) + Fore.WHITE + " " + highest_temperature + "C")
    else:
      print(day + " Highest temperature record not found")

    if (isNotEmpty(lowest_temperature)):
      print(day + " " + Fore.BLUE + getPlus(int(lowest_temperature)) + Fore.WHITE + " " + lowest_temperature + "C")
    else:
      print(day + " Lowest temperature record not found")

  if fileExists is False:
   print("The File: " + filename + " does not exists")


def findMonthBonus(filename, month, year):
  global highest, lowest, humidity, highest_str, lowest_str, humidity_str
  records = findRecords(filename)
  fileExists = False
  print(MONTHS_LIST[month-1]  + " "  + str(year))
  for current_record in records:
    fileExists = True
    yr, mn, day = getDate(current_record[0])
    highest_temperature, lowest_temperature, highest_humidity, mean_humidity = getTempAndHumidity(current_record)

    if isNotEmpty(highest_temperature) and isNotEmpty(lowest_temperature):
      print(day + " "+ Fore.BLUE + getPlus(int(lowest_temperature)) + Fore.LIGHTRED_EX + getPlus(int(highest_temperature)) + Fore.WHITE + " " + highest_temperature + "C - " + lowest_temperature + "C")
    elif not isNotEmpty(highest_temperature) and not isNotEmpty(lowest_temperature):
      print(day + " No Record Found")
    elif isNotEmpty(lowest_temperature):
      print(day.zfill(2), " ", Fore.BLUE, lowest_str, Fore.WHITE, " ", lowest_temperature, "C")
    elif isNotEmpty(highest_temperature):
      print(day.zfill(2) + " " + Fore.LIGHTRED_EX + highest_str + Fore.WHITE + " " + highest_temperature + "C")

  if fileExists is False:
   print("The File: " + filename + " does not exists")


def main():
  n = len(sys.argv)

  if(n > 4):
    print("Number of arguments passed are more than required. Exiting...")
    quit()

  typee = str(sys.argv[1])
  year_month = str(sys.argv[2])
  path = str(sys.argv[3]).split("/")
  filename = path[-1]
  months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

  dates = year_month.split("/")

  if(len(dates) > 2):
    print("Format of Year/Month is incorrect. exiting")
    quit()

  try:
    if(typee == "-e" and len(dates) == 1):
      if len(year_month) == 4:
        findYear(filename+"/"+filename+"_"+dates[0]+"_", months)
      else:
        print("Format of Year/Month is incorrect. exiting")
        quit()
    elif len(dates) == 2:
      if typee == "-a":
        findAverageMonth(filename+"/"+filename+"_"+dates[0]+"_"+months[int(dates[1])-1]+".txt")
      elif  typee == "-c":
        findMonth(filename+"/"+filename+"_"+dates[0]+"_"+months[int(dates[1])-1]+".txt", int(dates[1]), int(dates[0]))
      elif typee == "-ca":
        findMonthBonus(filename+"/"+filename+"_"+dates[0]+"_"+months[int(dates[1])-1]+".txt", int(dates[1]), int(dates[0]))
      else:
        print("The entered category is not correct. exiting")
        quit()
    else:
      print("The entered Date is not correct. exiting...")
      quit()
  except Exception as e :
    print("Exception occured.. Code could not be executed properly")
    print(e)
    quit()

if __name__=="__main__":
  main()
