# PHYS121_Functions
- last updated May 29, 2022

Python functions written for use in the PHYS 121 lab at UBC Okanagan.

To use the functions described below, place the PHYS121.py file in the same directory as your main Python code.  Then import PHYS121 using:
```python
import PHYS121
```

The following functions are currently aavailable:
* Generate scatter plots
* Weighted and unweighted linear fits
* Plot a histogram and generate basic statistics
* Overlay multiple histograms
* Generate multiple scatter plots on a single graph

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

The two examples above are demonstrated in the code cells below.  The 'm, b, dm, db, fig = ...' syntax is used to store the function outputs in varibles.
