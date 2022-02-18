from email import message
import sys
import csv
from os.path import exists
import colorama
from colorama import Fore

monthslist = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def findYear(filename, months):

  highest = 0
  lowest = 100
  humidity = 0
  highest_str = "Highest: No Record Found"
  lowest_str = "Lowest: No Record Found"
  humidity_str = "Humidity: No Record Found"

  for mon in months:
    current_month = filename + mon +".txt"
    # print(current_month)
    if exists(current_month):
      file = open(current_month)
      csvreader = csv.reader(file)
      # print(columns[0], "\t", columns[1], "\t", columns[3], "\t", columns[7])
      header = False
      for record in csvreader:

        if(len(record) != 23):
          continue

        if(header is False):
          header = True
          continue

        # print(record[0], "\t", record[1], "\t", record[3], "\t", record[7])
        # print(record)
        datee = str(record[0]).split("-")
        # print(datee)
        month = monthslist[int(datee[1])-1]
        day = datee[2]
        if(len(str(record[1]).strip())>0):
          if(int(str(record[1])) > highest):
            highest = int(str(record[1]))
            highest_str = "Highest: " + str(record[1]) + "C on " + month + " " + day

        if (len(str(record[3]).strip())>0):
          if(int(str(record[3])) < lowest):
            lowest = int(str(record[3]))
            lowest_str = "Lowest: " + str(record[3]) + "C on " + month + " " + day

        if (len(str(record[7]).strip())>0):
          if(int(str(record[7])) > humidity):
            humidity = int(str(record[7]))
            humidity_str = "Humid: " + str(record[7]) + "% on " + month + " " + day
    else:
      pass

  return highest_str + "\n" + lowest_str + "\n" +humidity_str + "\n"

def findAverageMonth(filename):

  highest = 0
  high_count = 0
  low_count = 0
  hum_count = 0
  lowest = 0
  humidity = 0
  highest_str = "Highest: No Record Found"
  lowest_str = "Lowest: No Record Found"
  humidity_str = "Humidity: No Record Found"

  if exists(filename):
    file = open(filename)
    csvreader = csv.reader(file)
    header = False
    for record in csvreader:
      # print(record)
      if(len(record) != 23):
        continue
      if(header is False):
        header = True
        continue

      if(len(str(record[1]).strip())>0):
        if(high_count == 0):
          highest = int(str(record[1]))
          high_count += 1
        else:
          highest = ((highest*high_count) + int(str(record[1])))/(high_count+1)
          high_count += 1
        highest_str = "Highest Average: " + str("{:.2f}".format(highest)) + "C"

      if (len(str(record[3]).strip())>0):
        if(low_count == 0):
          lowest = int(str(record[3]))
          low_count += 1
        else:
          lowest = ((lowest*low_count) + int(str(record[3])))/(low_count+1)
          low_count += 1
        lowest_str = "Lowest Average: " + str("{:.2f}".format(lowest)) + "C"

      if (len(str(record[8]).strip())>0):
        humidity = int(str(record[8]))
        if(hum_count == 0):
          humidity = int(str(record[8]))
          hum_count += 1
        else:
          humidity = ((humidity*hum_count) + int(str(record[8])))/(hum_count+1)
          hum_count += 1
        humidity_str = "Average Humidity: " + str("{:.2f}".format(humidity)) + "%"
  else:
    print("The File: ", filename, " does not exists")


  return highest_str + "\n" + lowest_str + "\n" + humidity_str + "\n"

def findMonth(filename, month, year):

  output = ""

  if exists(filename):
    print(monthslist[month-1]  +" "  + str(year))
    file = open(filename)
    csvreader = csv.reader(file)
    header = False
    for record in csvreader:
      if(len(record) != 23):
        continue
      if(header is False):
        header = True
        continue

      highest_str = ""
      lowest_str = ""
      day = (str(record[0]).split("-"))[2]

      if(len(str(record[1]).strip())>0):
        highest = int(str(record[1]))
        for i in range(highest):
           highest_str += "+"
        print(day.zfill(2) + " " + Fore.LIGHTRED_EX + highest_str + Fore.WHITE + " " + str(record[1]) + "C")
      else:
        print(day.zfill(2) + " Highest temperature record not found")

      if (len(str(record[3]).strip())>0):
        lowest = int(str(record[3]))
        for i in range(lowest):
          lowest_str += "+"

        print(day.zfill(2) + " " + Fore.BLUE + lowest_str + Fore.WHITE + " " + str(record[3]) + "C")
      else:
        print(day.zfill(2) + " Lowest temperature record not found")
  else:
   print("The File: " + filename + " does not exists")

  return ""

def findMonthBonus(filename, month, year):

  output = ""

  if exists(filename):
    print(monthslist[month-1] ," " , str(year))
    file = open(filename)
    csvreader = csv.reader(file)
    header = False
    for record in csvreader:
      if(len(record) != 23):
        continue
      if(header is False):
        header = True
        continue

      highest_str = ""
      lowest_str = ""
      highest = None
      lowest = None
      day = (str(record[0]).split("-"))[2]

      if(len(str(record[1]).strip())>0):
        highest = int(str(record[1]))
        for i in range(highest):
           highest_str += "+"

      if (len(str(record[3]).strip())>0):
        lowest = int(str(record[3]))
        for i in range(lowest):
          lowest_str += "+"

      if highest != None and lowest != None:
        print(day.zfill(2) + " "+ Fore.BLUE + lowest_str + Fore.LIGHTRED_EX + highest_str + Fore.WHITE + " " + str(record[1]) + "C - " + str(record[3]) + "C")
      elif highest == None and lowest == None:
        print(day.zfill(2) + " No Record Found")
      elif highest == None:
        print(day.zfill(2), " ", Fore.BLUE, lowest_str, Fore.WHITE, " ", str(record[3]), "C")
      elif lowest == None:
        print(day.zfill(2) + " " + Fore.LIGHTRED_EX + highest_str + Fore.WHITE + " " + str(record[1]) + "C")

  else:
   print("The File: " + filename + " does not exists")

  return ""

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
  # try:
  if(typee == "-e" and len(dates) == 1):
    if len(year_month) == 4:
      output = findYear(filename+"/"+filename+"_"+dates[0]+"_", months)
    else:
      print("Format of Year/Month is incorrect. exiting")
      quit()
  elif len(dates) == 2:
    if typee == "-a":
      output = findAverageMonth(filename+"/"+filename+"_"+dates[0]+"_"+months[int(dates[1])-1]+".txt")
    elif  typee == "-c":
      output = findMonth(filename+"/"+filename+"_"+dates[0]+"_"+months[int(dates[1])-1]+".txt", int(dates[1]), int(dates[0]))
    elif typee == "-ca":
      output = findMonthBonus(filename+"/"+filename+"_"+dates[0]+"_"+months[int(dates[1])-1]+".txt", int(dates[1]), int(dates[0]))
    else:
      print("The entered category is not correct. exiting")
      quit()
  else:
    print("The entered Date is not correct. exiting...")
    quit()
  # except Exception as e :
  #   print("Exception occured.. Code could not be executed properly")
  #   print(e)
  #   quit()

  print(output)


if __name__=="__main__":
  main()
