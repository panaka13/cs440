import numpy

def derivative(poly):
	poly = poly[::-1]
	f = []
	for i in range(1, len(poly)):
		f.append(poly[i]*i)
	return f[::-1]

def cal(interval, poly, x):
	n = len(interval)
	for i in range(1, len(interval)):
		if interval[i-1] <= x and x <= interval[i]:
			return numpy.polyval(poly[i-1], x)
	fprime = derivative(poly[n-2])
	return numpy.polyval(poly[n-2], interval[n-1]) + numpy.polyval(fprime, x)*(x-interval[n-1])

def LinearSpline(x, y):
	func = []
	for i in range(1, len(x)):
		a = (y[i]-y[i-1]) / (x[i]-x[i-1])
		b = y[i-1] - a*x[i-1]
		func.append([a, b])
	return (x, func)

def QuadraticSpline(x, y, z0 = 0):
	func = []
	b = [z0]
	a = []
	for i in range(1, len(x)):
		b.append(-b[i-1] + 2*(y[i]-y[i-1])/(x[i]-x[i-1]))
		a.append((b[i]-b[i-1])/(2*(x[i]-x[i-1])))
	for i in range(0, len(x)-1):
		newA = a[i]
		newB = 2*a[i]*(-x[i]) + b[i]
		newC = a[i]*(x[i]**2) - b[i]*x[i] + y[i]
		func.append([newA, newB, newC])
	return (x, func)

def CubicSpline1(x, y):
	func = []
	a = y
	n = len(y)-1
	h = numpy.zeros(n+1)
	alpha = numpy.zeros(n)
	l = numpy.zeros(n+1)
	u = numpy.zeros(n+1)
	z = numpy.zeros(n+1)
	c = numpy.zeros(n+1)
	d = numpy.zeros(n+1)
	b = numpy.zeros(n+1)

	for i in range(n):
		h[i] = x[i+1]-x[i]
	for i in range(1, n):
		alpha[i] = 3*((a[i+1]-a[i])/h[i] - (a[i]-a[i-1])/h[i-1])
	l[0] = 1
	u[0] = 0
	z[0] = 0
	for i in range(1, n):
		l[i] = 2*(x[i+1]-x[i-1]) - h[i-1]*u[i-1]
		u[i] = h[i]/l[i]
		z[i] = (alpha[i]-h[i-1]*z[i-1])/l[i]
	l[n] = 1
	z[n] = 0
	c[n] = 0
	for i in range(n-1, -1, -1):
		c[i] = z[i]-u[i]*c[i+1]
		b[i] = (a[i+1]-a[i])/h[i] - h[i]*(c[i+1]+2*c[i])/3
		d[i] = (c[i+1]-c[i])/(3*h[i])
	for i in range(n):
		newA = a[i] + b[i]*(-x[i]) + c[i]*((-x[i])**2) + d[i]*((-x[i])**3)
		newB = b[i] + 2*c[i]*(-x[i]) + 3*d[i]*((-x[i])**2)
		newC = c[i] + 3*d[i]*(-x[i])
		newD = d[i]
		func.append([newD, newC, newB, newA])
	return (x, func)
