from email import message
import sys
import csv
from os.path import exists



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
      columns = next(csvreader)
      # print(columns[0], "\t", columns[1], "\t", columns[3], "\t", columns[7])
      for record in csvreader:

        # print(record[0], "\t", record[1], "\t", record[3], "\t", record[7])
        datee = str(record[0]).split("-")
        month = monthslist[int(datee[1])-1]
        day = datee[2]
        if(len(str(record[1]))>0):
          if(int(str(record[1])) > highest):
            highest = int(str(record[1]))
            highest_str = "Highest: " + str(record[1]) + "C on " + month + " " + day

        if (len(str(record[3]))>0):
          if(int(str(record[3])) < lowest):
            lowest = int(str(record[3]))
            lowest_str = "Lowest: " + str(record[3]) + "C on " + month + " " + day

        if (len(str(record[7]))>0):
          if(int(str(record[7])) > humidity):
            humidity = int(str(record[7]))
            humidity_str = "Humid: " + str(record[7]) + "% on " + month + " " + day
    else:
      pass

  output = highest_str + "\n" + lowest_str + "\n" +humidity_str + "\n"

  return output

def findAverageMonth(filename):
  print(filename)

  return ""

def findMonth(filename):
  print(filename)

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
  try:
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
        output = findMonth(filename+"/"+filename+"_"+dates[0]+"_"+months[int(dates[1])-1]+".txt")
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

  print("\n", output)


if __name__=="__main__":
  main()

