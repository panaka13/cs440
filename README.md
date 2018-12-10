Dataset: from [www.ncei.noaa.gov](www.ncei.noaa.gov)<br/>
Order ID: [1520589](https://www.ncdc.noaa.gov/cdo-web/orders?id=1520589&email=lionboy589@gmail.com) <br/>
Email: lionboy589@gmail.com

Order ID: [1520617](https://www.ncdc.noaa.gov/cdo-web/orders?id=1520617&email=lionboy589@gmail.com) <br/>
Email: lionboy589@gmail.com

Order ID: [1520669](https://www.ncdc.noaa.gov/cdo-web/orders?id=1520669&email=lionboy589@gmail.com) <br/>
Email: lionboy589@gmail.com

Order ID: [1520741](https://www.ncdc.noaa.gov/cdo-web/orders?id=1520741&email=lionboy589@gmail.com) <br/>
Email: lionboy589@gmail.com

Link: [github](https://github.com/panaka13/cs440)

Requirement: 
* Python 3.4 or newer
* Matplotlib 2.2.3
* numpy 1.15.1

Important file:
* Main.py: main function	
* StatFunction.py: function related to stat
* Data.py: read data file
* Piecewise.py: piecewise interpolation
* Projection.py: do projection 
* LinearSystem.py: solve linear system of equation
* 1520741.csv: Raw data file

Comment: To get data
```python
# get whole data
	(index, interval) = Data.getMin(startYear, startMonth, startDay, endYear, endMonth, endDate)
# get random data
	(index, interval) = Data.getMinRandom(startYear, startMonth, startDay, endYear, endMonth, endDate, numberOfPoint)
# get every k-th point
	(index, interval) = Data.getMin(startYear, startMonth, startDay, endYear, endMonth, endDate, k)
```
To run interpolation
```python
# best fit polynomial
func = Projection.degreePolynomial(index, temp, degree)
f = lambda x: numpy.polyval(func)
# linear spline
(func, interval) = Piecewise.LinearSpline(index, temp, degree)
f = lambda x: piecewise.cal(interval, func, x)
# quadratic spline
(func, interval) = Piecewise.QuadraticSpline(index, temp, degree)
f = lambda x: piecewise.cal(interval, func, x)
# cubic spline
(func, interval) = Piecewise.CubicSpline1(index, temp, degree)
f = lambda x: piecewise.cal(interval, func, x)
```

To visualize the interpolation:
```python
(wholeIndex, wholeTemp) = Data.getMin(year, 1, 1, year+1, 1, 1)
Projection.graphProjection(wholeIndex, wholeTemp, f)
```
