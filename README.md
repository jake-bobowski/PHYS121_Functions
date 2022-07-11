# PHYS121_Functions
- last updated July 11, 2022

Note that the Jupyter Notebook included in this repository (PHYS_121_Functions_demonstration.ipynb) makes use of a module called 'data_entry' (accessed via PHYS121.py) which was written by Dr. Carl Michal from UBC.  The original source code for the module (data_entry.py) can be found here: https://phas.ubc.ca/~michal/data_entry.py.

Python functions written for use in the PHYS 121 lab at UBC Okanagan.

To use the functions described below, place the PHYS121.py file in the same directory as your main Python code.  Then import PHYS121 using:
```python
import PHYS121
```

The following functions are currently aavailable:
* Generate scatter plots
* Weighted and unweighted linear fits
* Weighted and unweighted power law fits
* Weighted and unweighted $RC$-charging fits
* Weighted and unweighted fits for the Eddy-current braking lab
* Plot a histogram and generate basic statistics
* Overlay multiple histograms
* Generate multiple scatter plots on a single graph
* Import and display an image with a figure caption
* Data entry using a spreadsheet-like envirnoment

Example implementations of the various fuunctions are described below.  These examples are implmented in the Jupyter notebook file 'PHYS_121_Functions_demonstration.ipynb' provided in this repository.

-----------------------------
-----------------------------

### LinearFit...

The linear-fit function is called as follows:
```python
LinearFit(xData, yData, yErrors = [], xlabel = 'x-axis', ylabel = 'y-axis', xUnits = '', yUnits = '', fill = False)
```
The xData and yData lists are required.  The others are optional with default values set.  The function returns the following outputs:
```python
Slope, Yintercept, errSlope, errYintercept, fig
```
The first four outputs are numerical values and 'fig' is the formatted plot. 

If $y$-uncertainities are provided, the function will perform a weighted fit.  The $y$-uncertainties list must be the same length as $x$- and $y$-data lists.  If $y$-uncertainties are not provided, the fit will be unweighted.  The other optional arguments include $x$- and $y$-axis names and units for the $x$- and $y$-datasets.  These must be entered as strings (enclosed in quotations) and they are used for formatting the outputs of the function.  If 'fill' is set to True, shading will be added around the best-fit line representing confindence intervals. 

### Unweighted Fit Example Implmentation
The code block below shows the most basic use of 'LinearFit' for an unweighted fit without any of the optional arguments.
```python
import PHYS121
V = [1, 2, 3, 4]
I = [0.12, 0.198, 0.285, 0.412]
m, b, dm, db, fig1 = PHYS121.LinearFit(V, I)
```

### Weighted Fit Example Implmentation
This second blcok of code shows how to use 'LinearFit' to do a weighted fit.  It also makes use of all of the other optional arguments.  
```python
import PHYS121
V = [1, 2, 3, 4]
I = [0.12, 0.198, 0.285, 0.412]
errI = [0.005, 0.012, 0.020, 0.025]
m, b, dm, db, fig1 = PHYS121.LinearFitFunction(V, I, errI, 'voltage' , 'current', 'V', 'A', True)
```

-----------------------------
-----------------------------

### Spreadsheet

First, we introduce a very useful fuction called 'Spreadsheet'.  This function uses the 'data_entry' module which was written by Carl Michal, a physicist from UBC's Vancouver campus.  The original source code can be found here: https://www.phas.ubc.ca/~michal/data_entry.py.

The data_entry function allows you to enter data into a spreadsheet-like environment.  The function will also generate vectors from the columns of data which can then be used to process the data (calculations, plotting, fitting, etc.).  Once a table to data has been entered, a file of column separated values (csv file) will be created in the same directory as the working Jupyter Notebook.  Once this file has been created, the spreadsheet will be auto-populated if the csv file is called using data_entry.

To use Spreadsheet, the files PHYS121.py and data_entry.py must be in the same directory as the working Jupyter Notebook.  

Here is an example implemntation of Spreadsheet:
```python
import numpy as np
import PHYS121
de = PHYS121.Spreadsheet("example")
```

-----------------------------
-----------------------------

### Statistics...

The statistics function is called as follows:
```python
Statistics(data, nbins = 10, xlabel = 'x-axis', xUnits = '', normalized = False)
```
The data input is required, all other arguments are optional with default values set.  The function returns the following outputs:
```python
counts, centres, average, stdDev, stdError, fig
```
The first two outputs are lists, the next three are numerical values, and 'fig' is the formatted plot. 

The function calculates and reports the mean, standard deviation, and standard error of the provided data.  It also plots a histogram of the data.  

### Statistics Example Implmentation
The code block below shows an implementation of 'Statistics'.
```python
import PHYS121
theta20a = [2.02, 1.93, 1.92, 1.96, 2.03, 2.03, 1.96, 2.03, 2.06, 2, 2.03, 2.12, 2.07, 1.99, 1.99, 1.95, 2.03, 2.12, 2.03, 2.09, 2.03, 2.03, 2.01, 2.04, 2.03, 2.04, 1.99, 1.99, 1.97, 1.98]
cnts, ctrs, mean, stdDev, stdError, fig20a = PHYS121.Statistics(theta20a, 12, 'Period', 's', True)
```

-----------------------------
-----------------------------

### HistOverlay...

The HistOverlay function is called as follows:
```python
HistOverlay(dataArray, nbins = 10, xlabel = 'x-axis', xUnits = '',  normalized = True, transparency = 0.75)
```
The dataArray (a list of lists) input is required, all other arguments are optional with default values set.  The function returns the following outputs:
```python
countsArray, centresArray, fig
```
The first two outputs are lists of lists and 'fig' is the formatted plot. 

The dataArray is of the form dataArray = [[dataset1], [dataset2], ... [datasetN]].  The function plots the histograms of each of the datasets on a single graph.  If the normalized argument is True, then histogram is scaled such that the area under the distributions is 1.  This is a good option when comparing two different distribtuions.  The transparency argument (a number between 0 and 1) sets the transparency of each of the individual histograms.

### HistOverlay Example Implmentation
The code block below shows an implementation of 'HistOverlay'.
```python
import PHYS121
cnts, ctrs, fig = PHYS121.HistOverlay([theta20a, theta20], 8, 'Period', 's', True, 0.75)
```

-----------------------------
-----------------------------

### Scatter...

The function for generating scatter plots is called as follows:
```python
Scatter(xData, yData, yErrors = [], xlabel = 'x-axis', ylabel = 'y-axis', xUnits = '', yUnits = '', fill = False, show = True)
```
The 'xData' and 'yData' inputs are required, all other arguments are optional with default values set.  The function returns the a single output (the formatted plot):
```python
fig
```

The function will do a simple scatter plot if no 'yError' are included.  It will included error bars if 'yErrors' are passed to the function.  The 'fill' and 'show' arguments should generally be false.  They are used by the linear fit function which calls the scatter plot function to generate its graphs.  

### Scatter Example Implmentation
The code block below shows an implementation of 'Scatter'.
```python
import PHYS121
theta = [10, 20, 30] # degrees
T = [mean10, mean20, mean30] # s
errT = [stdError10, stdError20, stdError30] # s
fig = PHYS121.Scatter(theta, T, errT, 'initial angle' , 'period', 'degrees', 's')
```

-----------------------------
-----------------------------

### MultiScatter...

The function for generating multiple scatter plots on a single graph is called as follows:
```python
MultiScatter(DataArray, xlabel = 'x-axis', ylabel = 'y-axis', xUnits = '', yUnits = '')
```
The 'DataArray' input is required, all other arguments are optional with default values set.  The function returns the a single output (the formatted plot):
```python
fig
```

DataArray takes the form of nested lists: DataArray = [[x1, y1, dy1], [x2, y2], [x3, y3, dy3], ...], where x1, y1, dy1, x2, y2, ... are themselves lists.  Notice that each sublist ([x1, y1, dy1] or [x2, y2]) can be either two or three elements long.  If the sublist contains three elements, a scatter plot with error bars will be generated.  If the sublist contains only two elements, a scatter plot with no error bars will be generated.  'DataArray' can mix sublists with two and three elements.

### MultiScatter Example Implmentation
The code block below shows an implementation of 'MultiScatter'.
```python
import PHYS121
V1 = [1, 2, 3, 4]
I1 = [0.12, 0.198, 0.285, 0.412]
errI1 = [0.005, 0.012, 0.020, 0.025]

V2 = [1, 2, 3, 4, 5]
I2 = [0.25, 0.31, 0.405, 0.602, .682]

V3 = [1, 2, 3, 4]
I3 = [0.05, 0.11, 0.155, 0.252]
errI3 = [0.005, 0.012, 0.020, 0.025]

V4 = np.array([1.5, 2.5, 3.5, 4.5])
I4 = [0.05, -0.11, -0.155, -.23]

DataArray = [[V1, I1, errI1], [V2, I2], [V3, I3, errI3], [V4, I4]]

fig = PHYS121.MultiScatter(DataArray, 'time', 'position', 's', 'cm')
```

-----------------------------
-----------------------------

### ImportImage...

The function for importing and displaying an image (with an optional caption) is called as follows:
```python
ImportImage(filename, caption = '', rotation = 0)
```
The 'filename' input is required.  The file name must be a string and it must have one of the following extentions:
 - png
 - jpg
 - jpeg
 - gif
 - eps
The figure file must also be located in the same directory as your working Jupyter Notebook file.

All other arguments are optional with default values set.  The first optional argument is a caption for the figure and it must be a string.  The second optional argument is a numerical value (float or integer).  It is the amount to rotate the image in degrees.   The function returns the a single output (the formatted figure):
```python
fig
```

### ImportImage Example Implmentation
The code block below shows an implementation of 'ImportImage'.
```python
import PHYS121
caption = 'Here is some example caption text.'
fig = PHYS121.ImportImage('pic.jpg', caption, -90)
```

-----------------------------
-----------------------------
