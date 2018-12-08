import csv
from datetime import datetime
import datetime as dt
import numpy
import random

def convertDate(s):
	year, month, day= s.split('-')
	return datetime(int(year), int(month), int(day))

inputFile = open("1520741.csv")
lines = csv.reader(inputFile)
cnt = 0
minIndex = []
minTemp = []
maxIndex = []
maxTemp = []
avgIndex = []
avgTemp = []
startDate = datetime(2010, 1, 1)
for line in lines:
	cnt += 1
	if line[0] == "USW00014939":
		current = convertDate(line[5])
		nDays = (current - startDate).days
		try:
			minIndex.append(nDays)
			minTemp.append(int(line[7]))
		except ValueError:
			minIndex.pop()
		try:
			maxIndex.append(nDays)
			maxTemp.append(int(line[7]))
		except ValueError:
			maxIndex.pop()
		try:
			avgIndex.append(nDays)
			avgTemp.append(int(line[7]))
		except ValueError:
			avgIndex.pop()

		
minTemp = numpy.array(minTemp)
maxTemp = numpy.array(maxTemp)
avgTemp = numpy.array(avgTemp)
minIndex = numpy.array(minIndex)
maxIndex = numpy.array(maxIndex)
avgIndex = numpy.array(avgIndex)

def getMin(startYear=2010, startMonth=1, startDay=1, endYear= 2017, endMonth=12, endDay=31, period=1):
	start = (datetime(startYear, startMonth, startDay) - startDate).days
	end = (datetime(endYear, endMonth, endDay) - startDate).days
	wholeTemp = minTemp[start:end]
	wholeIndex = minIndex[0:len(wholeTemp)]
	temp = wholeTemp[::period]
	index = wholeIndex[::period]
	if index[-1] != wholeIndex[-1]:
		index = numpy.append(index, wholeIndex[-1])
		temp = numpy.append(temp, wholeTemp[-1])
	return (index, temp)

def getMax(startYear=2010, startMonth=1, startDay=1, endYear= 2017, endMonth=12, endDay=31, period=1):
	start = (datetime(startYear, startMonth, startDay) - startDate).days
	end = (datetime(endYear, endMonth, endDay) - startDate).days
	temp = maxTemp[start:end:period]
	index = maxIndex[0:len(temp)]
	index = list(map(lambda x: x*period, index))
	return (index, temp)

def getAvg(startYear=2010, startMonth=1, startDay=1, endYear= 2017, endMonth=12, endDay=31, period=1):
	start = (datetime(startYear, startMonth, startDay) - startDate).days
	end = (datetime(endYear, endMonth, endDay) - startDate).days
	temp = avgTemp[start:end:period]
	index = avgIndex[0:len(temp)]
	index = list(map(lambda x: x*period, index))
	return (index, temp)

def getMinRandom(startYear=2010, startMonth=1, startDay=1, endYear= 2017, endMonth=12, endDay=31, k=-1):
	start = (datetime(startYear, startMonth, startDay) - startDate).days
	end = (datetime(endYear, endMonth, endDay) - startDate).days
	wholeTemp = minTemp[start:end]
	wholeIndex = minIndex[0:len(wholeTemp)]
	if k == -1 or k > len(wholeTemp):
		k = len(wholeTemp)
	k -= 2
	index = wholeIndex[1:k+1]
	temp = wholeTemp[1:k+1]
	for i in range(k+1, len(wholeTemp)-1):
		pos = random.randint(0, i-2)	
		if pos < k:
			index = numpy.delete(index, pos)
			temp = numpy.delete(temp, pos)
			index = numpy.append(index, wholeIndex[i])
			temp = numpy.append(temp, wholeTemp[i])
	index = numpy.append(index, wholeIndex[-1])
	temp = numpy.append(temp, wholeTemp[-1])
	index = numpy.insert(index, 0, wholeIndex[0])
	temp = numpy.insert(temp, 0, wholeTemp[0])
	return (index, temp)
