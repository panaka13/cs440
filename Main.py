import Data
import Projection
import numpy
import StatFunction as Stat
import time
import Piecewise

def xlsxPrinting(poly):
	for i in range(0, len(poly)):
		print(poly[i], end=' ')
	print()

def getPolynomial(year, degree = 2, step = 1, graph = False):
	tic = time.process_time()
	year = max(year, 2010)
	year = min(year, 2017)
	(index, temp) = Data.getMin(year, 1, 1, year+1, 1, 1, step)
	index = [x/20 for x in index]
	poly = Projection.degreePolynomial(index, temp, degree)
	# poly = numpy.polyfit(index, temp, degree)
	# print(poly-numpypoly)
	toc = time.process_time()
	f = lambda x: numpy.polyval(poly, x)
	(index, temp) = Data.getMin(year, 1, 1, year+1, 1, 1, 1)
	index = [x/20 for x in index]
	if graph:
		Projection.graphProjection(index, temp, f)
	# print("Year {0}, degree {1}, step {2}: error {3}".format(year, degree, step, Stat.sumOfSquareError(temp, list(map(f, index)))))
	# print("Finish in {0}".format(toc-tic))
	# print(Stat.sumOfSquareError(temp, list(map(f, index))), end=',')
	return poly

def polynomialPrediction(year, degree = 2, step = 1, compareYear = 2018, graph = False):
	tic = time.process_time()
	year = max(year, 2010)
	year = min(year, 2017)
	(index, temp) = Data.getMin(year, 1, 1, year+1, 1, 1, step)
	index = [x/20 for x in index]
	poly = Projection.degreePolynomial(index, temp, degree)
	f = lambda x: numpy.polyval(poly, x)
	(index, temp) = Data.getMin(compareYear, 1, 1, compareYear+1, 1, 1)
	index = [x/20 for x in index]
	# print("Year {0}, degree {1}, step {2}: error {3}".format(year, degree, step, Stat.sumOfSquareError(temp, list(map(f, index)))))
	if graph:
		Projection.graphProjection(index, temp, f)
	toc = time.process_time()
	# print("Finish in {0}".format(toc-tic))
	# print(Stat.sumOfSquareError(temp, list(map(f, index))), end=',')
	# xlsxPrinting(numpy.flip(poly))
	return poly

# f1: f(h)
# f2: f(h/2)
def polynomialRichardson(f1, f2, degree):
	power = 2**(degree+1)
	from numpy.polynomial import polynomial as P
	tmp = P.polysub(P.polymul(f2, [power]), f1)
	return P.polymul(tmp, [1/(power-1)])

a = []
for i in range(11):
	tmp0 = []
	for j in range(9):
		tmp1 = []
		for k in range(4):
			tmp2 = []
			for h in range(4):
				tmp2.append([])
			tmp1.append(tmp2)
		tmp0.append(tmp1)
	a.append(tmp0)

for degree in range(1, 11):
	for year in range(2010, 2018):
		a[degree-1][year-2010][0][0] = getPolynomial(year, degree, 8, False)
		a[degree-1][year-2010][1][0] = getPolynomial(year, degree, 4, False)
		a[degree-1][year-2010][2][0] = getPolynomial(year, degree, 2, False)
		a[degree-1][year-2010][3][0] = getPolynomial(year, degree, 1, False)
		for col in range(1, 4):
			for row in range(col, 4):
				f1 = a[degree-1][year-2010][row-1][col-1]
				f2 = a[degree-1][year-2010][row][col-1]
				a[degree-1][year-2010][row][col] = numpy.array(polynomialRichardson(f1, f2, degree+col-1))
	
for row in range(0, 4):
	for col in range(0, row+1):
		# print("row {0} col {1}".format(row, col))
		for degree in range(1, 11):
			for year in range(2010, 2018):
				f = lambda x: numpy.polyval(a[degree-1][year-2010][row][col], x)
				(index, temp) = Data.getMin(year, 1, 1, year+1, 1, 1, 1)
				index = [x/20 for x in index]
				# Projection.graphProjection(index, temp, f)
				# print(Stat.sumOfSquareError(temp, list(map(f, index))), end=',')
			# print()

def getFunction(year=2010, degree=2, row=0, col=0):
	return a[degree-1][year-2010][row][col]

def getError(year=2010, degree=2, row=0, col=0):
	f = lambda x: numpy.polyval(a[degree-1][year-2010][row][col], x)
	(index, temp) = Data.getMin(year, 1, 1, year+1, 1, 1, 1)
	index = [x/20 for x in index]
	return Stat.sumOfSquareError(temp, list(map(f, index)))

def getGraph(year=2010, degree=2, row=0, col=0):
	f = lambda x: numpy.polyval(a[degree-1][year-2010][row][col], x)
	(index, temp) = Data.getMin(year, 1, 1, year+1, 1, 1, 1)
	index = [x/20 for x in index]
	Projection.graphProjection(index, temp, f)

year = 2011
(index, temp) = Data.getMinRandom(year, 1, 1, year+1, 1, 1, 37)
(wholeIndex, wholeTemp) = Data.getMin(year, 1, 1, year+1, 1, 1)
# Stat.plotXY(wholeIndex, wholeTemp)
# Linear spline
(interval, func) = Piecewise.LinearSpline(index, temp)
f = lambda x: Piecewise.cal(interval, func, x)
print(Stat.sumOfSquareError(wholeTemp, list(map(f, wholeIndex))), end=',')
# Projection.graphProjection(wholeIndex, wholeTemp, f)
# Quadratic spline
(interval, func) = Piecewise.QuadraticSpline(index, temp)
f = lambda x: Piecewise.cal(interval, func, x)
print(Stat.sumOfSquareError(wholeTemp, list(map(f, wholeIndex))), end=',')
# Projection.graphProjection(wholeIndex, wholeTemp, f)
# Cubic spline
(interval, func) = Piecewise.CubicSpline1(index, temp)
f = lambda x: Piecewise.cal(interval, func, x)
# Projection.graphProjection(wholeIndex, wholeTemp, f)
print(Stat.sumOfSquareError(wholeTemp, list(map(f, wholeIndex))), end=',')
index = [x/20 for x in index]
wholeIndex = [x/20 for x in wholeIndex]
# best fit polynomial from 1 to 9
for degree in range(1, 10):
	func = Projection.degreePolynomial(index, temp, degree)
	f = lambda x: numpy.polyval(func, x)
	print(Stat.sumOfSquareError(wholeTemp, list(map(f, wholeIndex))), end=',')
	# Projection.graphProjection(wholeIndex, wholeTemp, f)
print()

for z0 in range(15810, 15830):
	(index, temp) = Data.getMin(year, 1, 1, year+1, 1, 1, 5)
	(wholeIndex, wholeTemp) = Data.getMin(year, 1, 1, year+1, 1, 1)
	(interval, func) = Piecewise.QuadraticSpline(index, temp, z0/1000)
	f = lambda x: Piecewise.cal(interval, func, x)
	print(z0, end=' ')
	print(Stat.sumOfSquareError(wholeTemp, list(map(f, wholeIndex))))
# 	(index, temp) = Data.getMin(year, 1, 1, year+1, 1, 1, 5)
(wholeIndex, wholeTemp) = Data.getMin(year, 1, 1, year+1, 1, 1)
(interval, func) = Piecewise.QuadraticSpline(index, temp)
f = lambda x: Piecewise.cal(interval, func, x)
print(Stat.sumOfSquareError(wholeTemp, list(map(f, wholeIndex))))
Projection.graphProjection(wholeIndex, wholeTemp, f)
(interval, func) = Piecewise.CubicSpline1(index, temp)
f = lambda x: Piecewise.cal(interval, func, x)
print(Stat.sumOfSquareError(wholeTemp, list(map(f, wholeIndex))))
Projection.graphProjection(wholeIndex, wholeTemp, f)
(interval, func) = Piecewise.LinearSpline(index, temp)
f = lambda x: Piecewise.cal(interval, func, x)
print(Stat.sumOfSquareError(wholeTemp, list(map(f, wholeIndex))))
Projection.graphProjection(wholeIndex, wholeTemp, f)
