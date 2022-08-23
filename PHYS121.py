# -*- coding: utf-8 -*-
"""
Created on Tue May 24 21:19:19 2022

@author: jbobowsk
"""

# Import some required modules.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm # used to generate a sequence of colours for plotting
from scipy.optimize import curve_fit
from IPython.display import HTML as html_print
from IPython.display import display, Markdown, Latex

###############################################################################
# Import a set of modules                                                     #
# - modified 20220817                                                         #
############################################################################### 
# Start the 'packages' function.
def packages():
    global np
    import numpy as np
    global math
    import math
    global plt
    import matplotlib.pyplot as plt
    install_and_import('httpimport')
    with httpimport.remote_repo(['PHYS121'], 'https://cmps-people.ok.ubc.ca/jbobowsk/PHYS_121_Lab/modules'):
        global PHYS121
        import PHYS121
    with httpimport.remote_repo(['uncertainties'], 'https://cmps-people.ok.ubc.ca/jbobowsk/PHYS_121_Lab/modules/uncertainties-3.1.7'):
        global uncertainties
        import uncertainties
    with httpimport.remote_repo(['ipysheet'], 'https://cmps-people.ok.ubc.ca/jbobowsk/PHYS_121_Lab/modules/ipysheet-0.5.0'):
        global ipysheet
        import ipysheet
    with httpimport.remote_repo(['data_entry'], 'https://cmps-people.ok.ubc.ca/jbobowsk/PHYS_121_Lab/modules'):
        global data_entry
        import data_entry
    return
    

###############################################################################
# For printing outputs in colour (copied from Stack Overflow)                 #
# - modified 20220607                                                         #
############################################################################### 
# Start the 'cstr' function.
def cstr(s, color = 'black'):
    return "<text style=color:{}>{}</text>".format(color, s)


###############################################################################
# Force a Float to be Printed w/o using Scientific Notation                   #
# - modified 20220527                                                         #
############################################################################### 
# Start the 'printStr' function.
def printStr(FloatNumber, Precision):
    # Print a float as a string with the number of digits after the decimal
    # determined by 'Precision'.
    return "%0.*f" % (Precision, FloatNumber)


###############################################################################
# Add a Package if it's not Already Installed                                 #
# - modified 20220527                                                         #
############################################################################### 
# Start the 'install_and_import' function.
# Check to see if 'package' is already installed.  If not, then attempt
# to do the install.
def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


###############################################################################
# Parsing Formatted Outputs from the Uncertainties Package                    #
# - modified 20220527                                                         #
############################################################################### 
# Start the 'Parse' function.
# The uncertainties package generates strings of the form '(x+/-y)eN' where 
# x and y are floats and N is an integer.  This functions separates out 
# x and y and counts the number of places after the decimal in x.
def Parse(uncertain):
    if uncertain[0] != '(':
        z = uncertain.split('+/-')
        num = float(z[0])
        err = float(z[1])
    else:
        uncertain = uncertain[1:]
        z = uncertain.split('+/-')
        num = float(z[0] + uncertain.split(')')[1])
        err = float(z[1].split(')')[0] + z[1].split(')')[1])
    places = len(z[0].split('.')[1])
    return num, err, places


###############################################################################
# Parsing Numbers in Scientific Notation for LaTeX Formatting                 #
# - modified 20220527                                                         #
############################################################################### 
# Start the 'eParse' function.
# This fuction determines the coefficient and power of a number of the form
# xeN, where x is the coefficient and N is the power.  If the number is not
# already expressed in scientific notation, this function will sill determine
# the value of the coefficient and power as if the number was expressed in 
# scientific notation.
def eParse(num, places):
    if isinstance(num, (float, int)) == False:
        print("'num' must be an integer or float.")
    else:
        z = str(num).split('e')
        coeff = float(z[0])
        if len(z) == 1:
            power = np.log10(abs(num)) - np.log10(abs(num)) % 1
            coeff = round(num/10**power, places) # Used to eliminate results such as 1.234000000000000001
        else:
            power = z[1]
    return coeff, int(power)


###############################################################################
# Producing Scatter Plots                                                     #
# - modified 20220530                                                         #
############################################################################### 
# Start the 'Scatter' function.
def Scatter(xData, yData, yErrors = [], xlabel = 'x-axis', ylabel = 'y-axis', xUnits = '', yUnits = '', fill = False, show = True):
    fig = ''
    # Check that the lengths of the inputs are all the same.  Check that the other inputs are strings.
    if len(xData) != len(yData) and xData != []:
        display(html_print(cstr('The length of xData (' + str(len(xData)) + ') is not equal to the length of yData (' + str(len(yData)) + ').', color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in xData) != True: # Is dataArray a list of lists or arrays?
        display(html_print(cstr("The elements of 'xData' must be integers or floats.", color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in yData) != True: # Is dataArray a list of lists or arrays?
        display(html_print(cstr("The elements of 'yData' must be integers or floats.", color = 'magenta')))
    elif len(yErrors) != 0 and all(isinstance(x, (int, float)) for x in yErrors) != True: # Is dataArray a list of lists or arrays?
        display(html_print(cstr("The elements of 'yErrors' must be integers or floats.", color = 'magenta')))
    elif len(yErrors) != 0 and len(xData) != len(yErrors):  
        display(html_print(cstr('The length of xData (' + str(len(xData)) + ') is not equal to the length of yErrors (' + str(len(yErrors)) + ').', color = 'magenta')))
    elif len(yErrors) != 0 and len(yData) != len(yErrors):  
        display(html_print(cstr('The length of yData (' + str(len(yData)) + ') is not equal to the length of yErrors (' + str(len(yErrors)) + ').', color = 'magenta')))
    elif isinstance(xlabel, str) == False:
        display(html_print(cstr("'xlabel' must be a string.", color = 'magenta')))
    elif isinstance(ylabel, str) == False:
        display(html_print(cstr("'ylabel' must be a string.", color = 'magenta')))
    elif isinstance(xUnits, str) == False:
        display(html_print(cstr("'xUnits' must be a string.", color = 'magenta')))
    elif isinstance(yUnits, str) == False:
        display(html_print(cstr("'yUnits' must be a string.", color = 'magenta')))
    elif fill != True and fill != False:
        display(html_print(cstr("The 'fill' parameter must be set to either True or False.", color = 'magenta')))
    elif show != True and show != False:
        display(html_print(cstr("The 'show' parameter must be set to either True or False.", color = 'magenta')))
    else:
        fig = plt.figure(figsize=(5, 5), dpi=100) # create a square figure.
        ax = fig.add_subplot(111)
        if xData == []:
            xData = np.arange(1, len(yData) + 1, 1)
            xlabel = 'trial number'
            xUnits = ''
        if len(yErrors) == 0:
            # plot without error bars
            plt.plot(xData, yData, 'ko', markersize = 6,\
                        markeredgecolor = 'b',\
                        markerfacecolor = 'r')
        else:
            # plot with error bars
            plt.errorbar(xData, yData, yErrors, fmt = 'ko', markersize = 6,\
                        markeredgecolor = 'b',\
                        markerfacecolor = 'r',\
                        capsize = 6)
        
        # Used to add shading around a best-fit line.  The fill is determined
        # by the uncertainties in the parameters.
        if fill == True:
            # If a fill is requested and there are no error bars, generate a list of errors
            # that will equally weight all of the points.
            if len(yErrors) == 0:
                for i in range(len(yData)):
                    yErrors.append(1)
            install_and_import('lmfit') # install 'lmfit' if its not already installed
            # The following lines are neede to determine the shading (copied from Firas Moosvi) 
            from lmfit.models import LinearModel  # import the LinearModel from `lmfit` package
            model = LinearModel()
            params = model.guess(yData, xData)
            result = model.fit(yData, params, x = np.array(xData), weights = 1/np.array(yErrors))
            # Calculate parameter uncertainty
            delmodel = result.eval_uncertainty(x = np.array(xData))
                
        if xUnits != '':
            xlabel = xlabel + ' (' + xUnits + ')' # Add units if provided.
        if yUnits != '':
            ylabel = ylabel + ' (' + yUnits + ')' # Add units if provided.
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box') # Used to make the plot square
        if fill == True:
            # Used to calculate the fill shading
            ax.fill_between(xData, result.best_fit - delmodel, result.best_fit + delmodel, alpha=0.2)
        if show == True:
            plt.show()
    return fig
    

###############################################################################
# Produce Multiple Scatter Plots                                              #
# - modified 20220530                                                         #
############################################################################### 
# Start the 'MultiScatter' function.
def MultiScatter(DataArray, xlabel = 'x-axis', ylabel = 'y-axis', xUnits = '', yUnits = ''):
    fig = ''
    # Check that the lengths of the inputs are all the same.  Check that the other inputs are strings.
    if len(DataArray) == 0:
        display(html_print(cstr("The 'DataArray' list must not be empty.", color = 'magenta')))
    elif all(isinstance(x, list) or type(x).__module__ == np.__name__ for x in DataArray) != True: # Is dataArray a list of lists or arrays?
        display(html_print(cstr("The 'DataArray' must be a list of lists.", color = 'magenta')))
    elif isinstance(xlabel, str) == False:
        display(html_print(cstr("'xlabel' must be a string.", color = 'magenta')))
    elif isinstance(ylabel, str) == False:
        display(html_print(cstr("'ylabel' must be a string.", color = 'magenta')))
    elif isinstance(xUnits, str) == False:
        display(html_print(cstr("'xUnits' must be a string.", color = 'magenta')))
    elif isinstance(yUnits, str) == False:
        display(html_print(cstr("'yUnits' must be a string.", color = 'magenta')))
    else:
        for i in range(len(DataArray)):
            if len(DataArray[i]) != 2 and len(DataArray[i]) != 3:
                display(html_print(cstr("The elements of 'DataArray' must be lists of length 2 or 3.  Element " + str(i + 1) + ' does not satisfy this requirement.', color = 'magenta')))
                return fig
            elif all(isinstance(x, list) or type(x).__module__ == np.__name__ for x in DataArray[i]) != True: # Is dataArray a list of lists or arrays?
                display(html_print(cstr("The elements of 'DataArray' must be a list of lists.  Element " +  str(i + 1) + ' does not satisfy this requirement.', color = 'magenta')))
                return fig
            elif len(DataArray[i]) == 2:
                if len(DataArray[i][0]) != len(DataArray[i][1]):
                    display(html_print(cstr("In element " + str(i + 1) + " of 'DataArray', the x- and y-datasets are different lengths.", color = 'magenta')))
                    return fig
                elif len(DataArray[i]) == 3:
                    if len(DataArray[i][0]) != len(DataArray[i][1]) or len(DataArray[i][0]) != len(DataArray[i][2]):
                        display(html_print(cstr("In element " + str(i + 1) + " of 'DataArray', the x- y-, and y-error datasets are different lengths.", color = 'magenta')))
                        return fig
        if  type(DataArray).__module__ == np.__name__: # Check to see if DataArray is an array.  If it is, convert to a list.
            DataArray = DataArray.tolist()
        for i in range(len(DataArray)):
            if type(DataArray[i]).__module__ == np.__name__:
                DataArray[i] = DataArray[i].tolist()
            for j in range(len(DataArray[i])):
                if type(DataArray[i][j]).__module__ == np.__name__:
                    DataArray[i][j] = DataArray[i][j].tolist()
        # Convert DataArray to a single master list
        masterList = sum(sum(DataArray,[]),[])
        if all(isinstance(x, (int, float)) for x in masterList) != True:
            display(html_print(cstr('All elements of x- and y-data and y-errors must be integers or floats.', color = 'magenta')))
            return fig
        
        fig = plt.figure(figsize=(5, 5), dpi=100) # create a square figure.       
        ax = fig.add_subplot(111)
        colour = iter(cm.rainbow(np.linspace(0, 1, len(DataArray))))
        
        for i in range(len(DataArray)):
            c = next(colour)
            if len(DataArray[i]) == 2:
                # plot without error bars
                plt.plot(DataArray[i][0], DataArray[i][1], 'o', color = 'k', markersize = 6,\
                        markeredgecolor = 'b',\
                        markerfacecolor = c)
            elif len(DataArray[i]) == 3:
                # plot with error bars
                plt.errorbar(DataArray[i][0], DataArray[i][1], DataArray[i][2], fmt = 'o', color = 'k', markersize = 6,\
                        markeredgecolor = 'b',\
                        markerfacecolor = c,\
                        capsize = 6)
            
        if xUnits != '':
            xlabel = xlabel + ' (' + xUnits + ')' # Add units if provided.
        if yUnits != '':
            ylabel = ylabel + ' (' + yUnits + ')' # Add units if provided.
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box') # Used to make the plot square
        plt.show()
    return fig


###############################################################################
# Weighted & Unweighted Linear Fits                                           #
# - modified 20220621                                                         #
############################################################################### 
# Start the 'LinearFit' function.
def LinearFit(xData, yData, yErrors = [], xlabel = 'x-axis', ylabel = 'y-axis', xUnits = '', yUnits = '', fill = False):
    # Check to see if the elements of dataArray are numpy arrays.  If they are, convert to lists
    Slope = ''
    Yintercept = ''
    errSlope = ''
    errYintercept = ''
    fig = ''
    if  type(xData).__module__ == np.__name__:
        xData = xData.tolist()
    if  type(yData).__module__ == np.__name__:
        yData = yData.tolist()
    if  type(yErrors).__module__ == np.__name__:
        yErrors = yErrors.tolist()
    # Check that the lengths of the inputs are all the same.  Check that the other inputs are strings.
    if len(xData) != len(yData):
        display(html_print(cstr('The length of xData (' + str(len(xData)) + ') is not equal to the length of yData (' + str(len(yData)) + ').', color = 'magenta')))
    elif len(yErrors) != 0 and len(xData) != len(yErrors):  
        display(html_print(cstr('The length of xData (' + str(len(xData)) + ') is not equal to the length of yErrors (' + str(len(yErrors)) + ').', color = 'magenta')))
    elif len(yErrors) != 0 and len(yData) != len(yErrors):  
        display(html_print(cstr('The length of yData (' + str(len(yData)) + ') is not equal to the length of yErrors (' + str(len(yErrors)) + ').', color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in xData) != True:
        display(html_print(cstr("The elements of 'xData' must be integers or floats.", color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in yData) != True:
        display(html_print(cstr("The elements of 'yData' must be integers or floats.", color = 'magenta')))
    elif len(yErrors) != 0 and all(isinstance(x, (int, float)) for x in yErrors) != True:
        display(html_print(cstr("The elements of 'yErrors' must be integers or floats.", color = 'magenta')))
    elif isinstance(xlabel, str) == False:
        display(html_print(cstr("'xlabel' must be a string.", color = 'magenta')))
    elif isinstance(ylabel, str) == False:
        display(html_print(cstr("'ylabel' must be a string.", color = 'magenta')))
    elif isinstance(xUnits, str) == False:
        display(html_print(cstr("'xUnits' must be a string.", color = 'magenta')))
    elif isinstance(yUnits, str) == False:
        display(html_print(cstr("'yUnits' must be a string.", color = 'magenta')))
    elif fill != True and fill != False:
        display(html_print(cstr("The 'fill' parameter must be set to either True or False.", color = 'magenta')))
    else:
        # Uncertainties is a nice package that can be used to properly round
        # a numerical value based on its associated uncertainty.
        install_and_import('uncertainties') # check to see if uncertainties is installed.  If it isn't attempt to do the install
        import uncertainties

        # Define the linear function used for the fit.
        def linearFunc(x, intercept, slope):
            y = slope*x + intercept
            return y
        
        # If the yErrors list is empty, do an unweighted fit.  Otherwise, do a weighted fit.
        print('')
        display(Markdown('$y = m\,x + b$'))
        if len(yErrors) == 0: 
            a_fit, cov = curve_fit(linearFunc, xData, yData)
            display(Markdown('This is an **UNWEIGHTED** fit.'))
        else:
            a_fit, cov = curve_fit(linearFunc, xData, yData, sigma = yErrors)
            display(Markdown('This is a **WEIGHTED** fit.'))

        Slope = a_fit[1]
        errSlope = np.sqrt(np.diag(cov))[1]
        Yintercept = a_fit[0]
        errYintercept = np.sqrt(np.diag(cov))[0]

        # Use the 'uncertainties' package to format the best-fit parameters and the corresponding uncertainties.
        m = uncertainties.ufloat(Slope, errSlope)
        b = uncertainties.ufloat(Yintercept, errYintercept)

        # Make a formatted table that reports the best-fit parameters and their uncertainties        
        import pandas as pd
        if xUnits != '' and yUnits != '':
            my_dict = {'slope' :{'':'$m =$', 'Value': '{:0.2ug}'.format(m), 'Units': yUnits + '/' + xUnits},
                       '$y$-intercept':{'':'$b =$', 'Value': '{:0.2ug}'.format(b), 'Units': yUnits}}
        elif xUnits != '' and yUnits == '':
            my_dict = {'slope' :{'':'$m =$', 'Value': '{:0.2ug}'.format(m), 'Units': '1/' + xUnits},
              '$y$-intercept':{'':'$b =$', 'Value': '{:0.2ug}'.format(b), 'Units': yUnits}}
        elif xUnits == '' and yUnits != '':
            my_dict = {'slope' :{'':'$m =$', 'Value': '{:0.2ug}'.format(m), 'Units': yUnits},
              '$y$-intercept':{'':'$b =$', 'Value': '{:0.2ug}'.format(b), 'Units': yUnits}}
        else:
            my_dict = {'slope' :{'':'$m =$', 'Value': '{:0.2ug}'.format(m)},
              '$y$-intercept':{'':'$b =$', 'Value': '{:0.2ug}'.format(b)}}

        # Display the table
        df = pd.DataFrame(my_dict)
        display(df.transpose())
        
        # Generate the best-fit line. 
        fitFcn = np.polynomial.Polynomial(a_fit)
        
        # Call the Scatter function to create a scatter plot.
        fig = Scatter(xData, yData, yErrors, xlabel, ylabel, xUnits, yUnits, fill, False)
        
        # Determine the x-range.  Used to determine the x-values needed to produce the best-fit line.
        if np.min(xData) > 0:
            xmin = 0.9*np.min(xData)
        else:
            xmin = 1.1*np.min(xData)
        if np.max(xData) > 0:
            xmax = 1.1*np.max(xData)
        else:
            xmax = 0.9*np.max(xData)

        # Plot the best-fit line...
        xx = np.arange(xmin, xmax, (xmax-xmin)/5000)
        plt.plot(xx, fitFcn(xx), 'k-')

        # Show the final plot.
        plt.show()
    return Slope, Yintercept, errSlope, errYintercept, fig
        
        
        
###############################################################################
# Weighted & Unweighted Power Law Fits                                        #
# - modified 20220705                                                         #
############################################################################### 
# Start the 'PowerLaw' function.
def PowerLaw(xData, yData, yErrors = [], xlabel = 'x-axis', ylabel = 'y-axis', xUnits = '', yUnits = ''):
    # Check to see if the elements of dataArray are numpy arrays.  If they are, convert to lists
    Coeff = ''
    Power = ''
    Offset = ''
    errCoeff = ''
    errPower = ''
    errOffset = ''
    fig = ''
    if  type(xData).__module__ == np.__name__:
        xData = xData.tolist()
    if  type(yData).__module__ == np.__name__:
        yData = yData.tolist()
    if  type(yErrors).__module__ == np.__name__:
        yErrors = yErrors.tolist()
    # Check that the lengths of the inputs are all the same.  Check that the other inputs are strings.
    if len(xData) != len(yData):
        display(html_print(cstr('The length of xData (' + str(len(xData)) + ') is not equal to the length of yData (' + str(len(yData)) + ').', color = 'magenta')))
    elif len(yErrors) != 0 and len(xData) != len(yErrors):  
        display(html_print(cstr('The length of xData (' + str(len(xData)) + ') is not equal to the length of yErrors (' + str(len(yErrors)) + ').', color = 'magenta')))
    elif len(yErrors) != 0 and len(yData) != len(yErrors):  
        display(html_print(cstr('The length of yData (' + str(len(yData)) + ') is not equal to the length of yErrors (' + str(len(yErrors)) + ').', color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in xData) != True:
        display(html_print(cstr("The elements of 'xData' must be integers or floats.", color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in yData) != True:
        display(html_print(cstr("The elements of 'yData' must be integers or floats.", color = 'magenta')))
    elif len(yErrors) != 0 and all(isinstance(x, (int, float)) for x in yErrors) != True:
        display(html_print(cstr("The elements of 'yErrors' must be integers or floats.", color = 'magenta')))
    elif isinstance(xlabel, str) == False:
        display(html_print(cstr("'xlabel' must be a string.", color = 'magenta')))
    elif isinstance(ylabel, str) == False:
        display(html_print(cstr("'ylabel' must be a string.", color = 'magenta')))
    elif isinstance(xUnits, str) == False:
        display(html_print(cstr("'xUnits' must be a string.", color = 'magenta')))
    elif isinstance(yUnits, str) == False:
        display(html_print(cstr("'yUnits' must be a string.", color = 'magenta')))
    else:
        # Uncertainties is a nice package that can be used to properly round
        # a numerical value based on its associated uncertainty.
        install_and_import('uncertainties') # check to see if uncertainties is installed.  If it isn't attempt to do the install
        import uncertainties

        # Define the linear function used for the fit.
        def PowerFunc(x, coeff, power, offset):
            y = coeff*x**power + offset
            return y
        
        # If the yErrors list is empty, do an unweighted fit.  Otherwise, do a weighted fit.
        print('')
        if xUnits == '':
            display(Markdown('$y = A\,x^N + C$'))
        else:
            display(Markdown('$y = A\,(x/1$ ' + xUnits + '$)^N\,+ \,C$'))
        if len(yErrors) == 0: 
            a_fit, cov = curve_fit(PowerFunc, xData, yData)
            display(Markdown('This is an **UNWEIGHTED** fit.'))
        else:
            a_fit, cov = curve_fit(PowerFunc, xData, yData, sigma = yErrors)
            display(Markdown('This is a **WEIGHTED** fit.'))

        Coeff = a_fit[0]
        errCoeff = np.sqrt(np.diag(cov))[0]
        Power = a_fit[1]
        errPower = np.sqrt(np.diag(cov))[1]
        Offset = a_fit[2]
        errOffset = np.sqrt(np.diag(cov))[2]

        # Use the 'uncertainties' package to format the best-fit parameters and the corresponding uncertainties.
        A = uncertainties.ufloat(Coeff, errCoeff)
        N = uncertainties.ufloat(Power, errPower)
        C = uncertainties.ufloat(Offset, errOffset)

        # Make a formatted table that reports the best-fit parameters and their uncertainties        
        import pandas as pd
        if xUnits != '' and yUnits != '':
#            my_dict = {'coefficient' :{'':'$A =$', 'Value': '{:0.2ug}'.format(A), 'Units': yUnits + '/' + xUnits + eval(r'"\u00b' + str(Power) + '"')},
#                       'power':{'':'$N =$', 'Value': '{:0.2ug}'.format(N), 'Units': ''},
#                       'offset':{'':'$C =$', 'Value': '{:0.2ug}'.format(C), 'Units': yUnits}}
            my_dict = {'coefficient' :{'':'$A =$', 'Value': '{:0.2ug}'.format(A), 'Units': yUnits},
                       'power':{'':'$N =$', 'Value': '{:0.2ug}'.format(N), 'Units': ''},
                       'offset':{'':'$C =$', 'Value': '{:0.2ug}'.format(C), 'Units': yUnits}}
        elif xUnits != '' and yUnits == '':
            my_dict = {'coefficient' :{'':'$A =$', 'Value': '{:0.2ug}'.format(A), 'Units': yUnits},
                       'power':{'':'$N =$', 'Value': '{:0.2ug}'.format(N), 'Units': ''},
                       'offset':{'':'$C =$', 'Value': '{:0.2ug}'.format(C), 'Units': yUnits}}           
        elif xUnits == '' and yUnits != '':
            my_dict = {'coefficient' :{'':'$A =$', 'Value': '{:0.2ug}'.format(A), 'Units': yUnits},
                       'power':{'':'$N =$', 'Value': '{:0.2ug}'.format(N), 'Units': ''},
                       'offset':{'':'$C =$', 'Value': '{:0.2ug}'.format(C), 'Units': yUnits}} 
        else:
            my_dict = {'coefficient' :{'':'$A =$', 'Value': '{:0.2ug}'.format(A)},
                       'power':{'':'$N =$', 'Value': '{:0.2ug}'.format(N)},
                       'offset':{'':'$C =$', 'Value': '{:0.2ug}'.format(C)}} 

        # Display the table
        df = pd.DataFrame(my_dict)
        display(df.transpose())
        
        # Generate the best-fit line. 
        #fitFcn = np.polynomial.Polynomial(a_fit)
        
        # Call the Scatter function to create a scatter plot.
        fig = Scatter(xData, yData, yErrors, xlabel, ylabel, xUnits, yUnits, False, False)
        
        # Determine the x-range.  Used to determine the x-values needed to produce the best-fit line.
        if np.min(xData) > 0:
            xmin = 0.9*np.min(xData)
        else:
            xmin = 1.1*np.min(xData)
        if np.max(xData) > 0:
            xmax = 1.1*np.max(xData)
        else:
            xmax = 0.9*np.max(xData)

        # Plot the best-fit line...
        xx = np.arange(xmin, xmax, (xmax-xmin)/5000)
        plt.plot(xx, Coeff*xx**Power + Offset, 'k-')

        # Show the final plot.
        plt.show()
    return Coeff, Power, Offset, errCoeff, errPower, errOffset, fig



###############################################################################
# Weighted & Unweighted RC Charing Fits                                       #
# - modified 20220711                                                         #
############################################################################### 
# Start the 'Charging' function.
def Charging(xData, yData, yErrors = [], xlabel = 'x-axis', ylabel = 'y-axis', xUnits = '', yUnits = ''):
    # Check to see if the elements of dataArray are numpy arrays.  If they are, convert to lists
    V0_fit = ''
    tau_fit = ''
    errV0 = ''
    errTau = ''
    fig = ''
    if  type(xData).__module__ == np.__name__:
        xData = xData.tolist()
    if  type(yData).__module__ == np.__name__:
        yData = yData.tolist()
    if  type(yErrors).__module__ == np.__name__:
        yErrors = yErrors.tolist()
    # Check that the lengths of the inputs are all the same.  Check that the other inputs are strings.
    if len(xData) != len(yData):
        display(html_print(cstr('The length of xData (' + str(len(xData)) + ') is not equal to the length of yData (' + str(len(yData)) + ').', color = 'magenta')))
    elif len(yErrors) != 0 and len(xData) != len(yErrors):  
        display(html_print(cstr('The length of xData (' + str(len(xData)) + ') is not equal to the length of yErrors (' + str(len(yErrors)) + ').', color = 'magenta')))
    elif len(yErrors) != 0 and len(yData) != len(yErrors):  
        display(html_print(cstr('The length of yData (' + str(len(yData)) + ') is not equal to the length of yErrors (' + str(len(yErrors)) + ').', color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in xData) != True:
        display(html_print(cstr("The elements of 'xData' must be integers or floats.", color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in yData) != True:
        display(html_print(cstr("The elements of 'yData' must be integers or floats.", color = 'magenta')))
    elif len(yErrors) != 0 and all(isinstance(x, (int, float)) for x in yErrors) != True:
        display(html_print(cstr("The elements of 'yErrors' must be integers or floats.", color = 'magenta')))
    elif isinstance(xlabel, str) == False:
        display(html_print(cstr("'xlabel' must be a string.", color = 'magenta')))
    elif isinstance(ylabel, str) == False:
        display(html_print(cstr("'ylabel' must be a string.", color = 'magenta')))
    elif isinstance(xUnits, str) == False:
        display(html_print(cstr("'xUnits' must be a string.", color = 'magenta')))
    elif isinstance(yUnits, str) == False:
        display(html_print(cstr("'yUnits' must be a string.", color = 'magenta')))
    else:
        # Uncertainties is a nice package that can be used to properly round
        # a numerical value based on its associated uncertainty.
        install_and_import('uncertainties') # check to see if uncertainties is installed.  If it isn't attempt to do the install
        import uncertainties

        # Define the linear function used for the fit.
        def ChargingFcn(x, V0, tau):
            y = V0*(1 - np.exp(-x/tau))
            return y
        
        # If the yErrors list is empty, do an unweighted fit.  Otherwise, do a weighted fit.
        print('')
        display(Markdown('$y = V_0(1 - e^{-x/ \\tau})$'))
    
        if len(yErrors) == 0: 
            a_fit, cov = curve_fit(ChargingFcn, xData, yData)
            display(Markdown('This is an **UNWEIGHTED** fit.'))
        else:
            a_fit, cov = curve_fit(ChargingFcn, xData, yData, sigma = yErrors)
            display(Markdown('This is a **WEIGHTED** fit.'))

        V0_fit = a_fit[0]
        errV0 = np.sqrt(np.diag(cov))[0]
        tau_fit = a_fit[1]
        errTau = np.sqrt(np.diag(cov))[1]
        
        # Use the 'uncertainties' package to format the best-fit parameters and the corresponding uncertainties.
        V0 = uncertainties.ufloat(V0_fit, errV0)
        tau = uncertainties.ufloat(tau_fit, errTau)

        # Make a formatted table that reports the best-fit parameters and their uncertainties        
        import pandas as pd
        if xUnits != '' and yUnits != '':
#            my_dict = {'coefficient' :{'':'$A =$', 'Value': '{:0.2ug}'.format(A), 'Units': yUnits + '/' + xUnits + eval(r'"\u00b' + str(Power) + '"')},
#                       'power':{'':'$N =$', 'Value': '{:0.2ug}'.format(N), 'Units': ''},
#                       'offset':{'':'$C =$', 'Value': '{:0.2ug}'.format(C), 'Units': yUnits}}
            my_dict = {'equilibrium voltage' :{'':'$V_0 =$', 'Value': '{:0.2ug}'.format(V0), 'Units': yUnits},
                       'time constant':{'':'$\tau =$', 'Value': '{:0.2ug}'.format(tau), 'Units': xUnits}}
        elif xUnits != '' and yUnits == '':
            my_dict = {'equilibrium voltage' :{'':'$V_0 =$', 'Value': '{:0.2ug}'.format(V0), 'Units': yUnits},
                       'time constant':{'':'$\tau =$', 'Value': '{:0.2ug}'.format(tau), 'Units': xUnits}}       
        elif xUnits == '' and yUnits != '':
            my_dict = {'equilibrium voltage' :{'':'$V_0 =$', 'Value': '{:0.2ug}'.format(V0), 'Units': yUnits},
                       'time constant':{'':'$\tau =$', 'Value': '{:0.2ug}'.format(tau), 'Units': xUnits}}
        else:
            my_dict = {'equilibrium voltage' :{'':'$V_0 =$', 'Value': '{:0.2ug}'.format(V0)},
                       'time constant':{'':'$\tau =$', 'Value': '{:0.2ug}'.format(tau)}}

        # Display the table
        df = pd.DataFrame(my_dict)
        display(df.transpose())
        
        # Generate the best-fit line. 
        #fitFcn = np.polynomial.Polynomial(a_fit)
        
        # Call the Scatter function to create a scatter plot.
        fig = Scatter(xData, yData, yErrors, xlabel, ylabel, xUnits, yUnits, False, False)
        
        # Determine the x-range.  Used to determine the x-values needed to produce the best-fit line.
        if np.min(xData) > 0:
            xmin = 0.9*np.min(xData)
        else:
            xmin = 1.1*np.min(xData)
        if np.max(xData) > 0:
            xmax = 1.1*np.max(xData)
        else:
            xmax = 0.9*np.max(xData)

        # Plot the best-fit line...
        xx = np.arange(xmin, xmax, (xmax-xmin)/5000)
        plt.plot(xx, V0_fit*(1 - np.exp(-xx/tau_fit)), 'k-')

        # Show the final plot.
        plt.show()
    return V0_fit, tau_fit, errV0, errTau, fig
    

###############################################################################
# Magnetic Braking Nonlinear Fits                                             #
# - modified 20220710                                                         #
############################################################################### 
# Start the 'Braking' function.
def Braking(xData, yData, yErrors = [], xlabel = 'x-axis', ylabel = 'y-axis', xUnits = '', yUnits = ''):
    # Check to see if the elements of dataArray are numpy arrays.  If they are, convert to lists
    vterm = ''
    tau = ''
    errvterm = ''
    errtau = ''
    fig = ''
    if  type(xData).__module__ == np.__name__:
        xData = xData.tolist()
    if  type(yData).__module__ == np.__name__:
        yData = yData.tolist()
    if  type(yErrors).__module__ == np.__name__:
        yErrors = yErrors.tolist()
    # Check that the lengths of the inputs are all the same.  Check that the other inputs are strings.
    if len(xData) != len(yData):
        display(html_print(cstr('The length of xData (' + str(len(xData)) + ') is not equal to the length of yData (' + str(len(yData)) + ').', color = 'magenta')))
    elif len(yErrors) != 0 and len(xData) != len(yErrors):  
        display(html_print(cstr('The length of xData (' + str(len(xData)) + ') is not equal to the length of yErrors (' + str(len(yErrors)) + ').', color = 'magenta')))
    elif len(yErrors) != 0 and len(yData) != len(yErrors):  
        display(html_print(cstr('The length of yData (' + str(len(yData)) + ') is not equal to the length of yErrors (' + str(len(yErrors)) + ').', color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in xData) != True:
        display(html_print(cstr("The elements of 'xData' must be integers or floats.", color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in yData) != True:
        display(html_print(cstr("The elements of 'yData' must be integers or floats.", color = 'magenta')))
    elif len(yErrors) != 0 and all(isinstance(x, (int, float)) for x in yErrors) != True:
        display(html_print(cstr("The elements of 'yErrors' must be integers or floats.", color = 'magenta')))
    elif isinstance(xlabel, str) == False:
        display(html_print(cstr("'xlabel' must be a string.", color = 'magenta')))
    elif isinstance(ylabel, str) == False:
        display(html_print(cstr("'ylabel' must be a string.", color = 'magenta')))
    elif isinstance(xUnits, str) == False:
        display(html_print(cstr("'xUnits' must be a string.", color = 'magenta')))
    elif isinstance(yUnits, str) == False:
        display(html_print(cstr("'yUnits' must be a string.", color = 'magenta')))
    else:
        # Uncertainties is a nice package that can be used to properly round
        # a numerical value based on its associated uncertainty.
        install_and_import('uncertainties') # check to see if uncertainties is installed.  If it isn't attempt to do the install
        import uncertainties

        # Define the linear function used for the fit.
        def BrakingFcn(x, tau, vterm):
            y = vterm*tau*((x/tau) - 1 + np.exp(-x/tau))
            return y
        
        # If the yErrors list is empty, do an unweighted fit.  Otherwise, do a weighted fit.
        print('')
        display(Markdown('$y = v_\mathrm{T}\\tau\left[\dfrac{x}{\\tau} - 1 + e^{-x/ \\tau}\\right]$'))

        if len(yErrors) == 0: 
            a_fit, cov = curve_fit(BrakingFcn, xData, yData)
            display(Markdown('This is an **UNWEIGHTED** fit.'))
        else:
            a_fit, cov = curve_fit(BrakingFcn, xData, yData, sigma = yErrors)
            display(Markdown('This is a **WEIGHTED** fit.'))

        Vterm = a_fit[1]
        errVterm = np.sqrt(np.diag(cov))[1]
        Tau = a_fit[0]
        errTau = np.sqrt(np.diag(cov))[0]

        # Use the 'uncertainties' package to format the best-fit parameters and the corresponding uncertainties.
        v = uncertainties.ufloat(Vterm, errVterm)
        T = uncertainties.ufloat(Tau, errTau)

        # Make a formatted table that reports the best-fit parameters and their uncertainties        
        import pandas as pd
        if xUnits != '' and yUnits != '':
            my_dict = {'Terminal Velocity' :{'':'$v_\mathrm{t} =$', 'Value': '{:0.2ug}'.format(v), 'Units': yUnits + '/' + xUnits},
                       'Time Constant':{'':'$\tau =$', 'Value': '{:0.2ug}'.format(T), 'Units': yUnits}}
        elif xUnits != '' and yUnits == '':
            my_dict = {'Terminal Velocity' :{'':'$v_\mathrm{t} =$', 'Value': '{:0.2ug}'.format(v), 'Units': '1/' + xUnits},
              'Time Constant':{'':'$\tau =$', 'Value': '{:0.2ug}'.format(T), 'Units': yUnits}}
        elif xUnits == '' and yUnits != '':
            my_dict = {'Terminal Velocity' :{'':'$v_\mathrm{t} =$', 'Value': '{:0.2ug}'.format(v), 'Units': yUnits},
              'Time Constant':{'':'$\tau =$', 'Value': '{:0.2ug}'.format(T), 'Units': yUnits}}
        else:
            my_dict = {'Terminal Velocity' :{'':'$v_\mathrm{t} =$', 'Value': '{:0.2ug}'.format(v)},
              'Time Constant':{'':'$\tau =$', 'Value': '{:0.2ug}'.format(T)}}

        # Display the table
        df = pd.DataFrame(my_dict)
        display(df.transpose())
                
        # Call the Scatter function to create a scatter plot.
        fig = Scatter(xData, yData, yErrors, xlabel, ylabel, xUnits, yUnits, False, False)
        
        # Determine the x-range.  Used to determine the x-values needed to produce the best-fit line.
        if np.min(xData) > 0:
            xmin = 0.9*np.min(xData)
        else:
            xmin = 1.1*np.min(xData)
        if np.max(xData) > 0:
            xmax = 1.1*np.max(xData)
        else:
            xmax = 0.9*np.max(xData)

        # Plot the best-fit line...
        xx = np.arange(xmin, xmax, (xmax-xmin)/5000)
        # Generate the best-fit line. 
        fitFcn = Vterm*Tau*((xx/Tau) - 1 + np.exp(-xx/Tau))

        plt.plot(xx, fitFcn, 'k-')

        # Show the final plot.
        plt.show()
    return Vterm, Tau, errVterm, errTau, fig
    
        
###############################################################################
# Histograms & Statistics                                                     #
# - modified 20220529                                                         #
###############################################################################        
# Start the 'Statisitics' function.
def Statistics(data, nbins = 10, xlabel = 'x-axis', xUnits = '', normalized = False):
    counts = ''
    centres = ''
    average = ''
    stdDev = ''
    stdError = ''
    fig = ''
    if len(data)==0:
        display(html_print(cstr("The 'data' list must not be empty.", color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in data) != True:
        display(html_print(cstr("All elements of the 'data' list must be floats or integers.", color = 'magenta')))
    elif isinstance(nbins, int) == False or nbins < 0:
        display(html_print(cstr("'nbins' must be a positive integer.", color = 'magenta')))
    elif isinstance(xlabel, str) == False:
        display(html_print(cstr("'xlabel' must be a string.", color = 'magenta')))
    elif isinstance(xUnits, str) == False:
        display(html_print(cstr("'xUnits' must be a string.", color = 'magenta')))
    elif normalized != True and normalized != False:
        display(html_print(cstr("The 'normalized' parameter must be set to either True or False.", color = 'magenta')))
    else:
        # Determine the boundaries of the various histogram bins.
        binwidth = (np.max(data) - np.min(data))/nbins
        boundaries = np.arange(np.min(data), np.max(data) + binwidth, binwidth)
        
        # Prepare a square figure.
        fig = plt.figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot to histogram
        counts, edges, patches = plt.hist(data, bins = boundaries, color='lightskyblue', edgecolor='k', density = normalized)
        
        # Use the output from the histogram plot to determine the positions of the bin centres.
        centres = edges[0:len(counts)] + binwidth/2
        
        # Calculate some basic statistics
        average = np.mean(data)
        stdDev = np.std(data,  ddof=1)
        stdError = stdDev/np.sqrt(len(data))
        
        install_and_import('uncertainties') # check to see if uncertainties is installed.  If it isn't attempt to do the install
        import uncertainties
        
        # Use the uncertainties package and Parsing functions to help format the statistics 
        x = uncertainties.ufloat(average, stdError)
        y = '{:0.2ue}'.format(x)
        num, stdError, places = Parse(y)
        stdDev = float('{:0.3g}'.format(stdDev))
        coeff, power = eParse(num, places)
        print('')
        
        # Display some nicely-formatted results
        if abs(power) < 3:        
            stdError = printStr(stdError, places - power)
            display(Latex(f'$N = {len(data)}$.'))
            display(Latex(f'The average of the data is $\mu = {num}\, \mathrm{{ {xUnits} }}.$'))
            display(Latex(f'The standard deviation of the data is $\sigma = {stdDev}\, \mathrm{{ {xUnits} }}.$'))
            display(Latex(f'The standard error of the data is $\sigma_\mu = \sigma/\sqrt{{N}} = \mathrm{stdError}\, \mathrm{{ {xUnits} }}.$'))
        else:
            stdDevPrint = round(stdDev/10**power, places)
            stdErrorPrint = round(stdError/10**power, places)
            display(Latex(f'$N = {len(data)}$.'))
            display(Latex(f'The average of the data is $\mu = {coeff}' + r'\times' +  f'10^{{ {power} }}\, \mathrm{{ {xUnits} }}.$'))
            display(Latex(f'The standard deviation of the data is $\sigma = {stdDevPrint}' + r'\times' + f'10^{{ {power} }}\, \mathrm{{ {xUnits} }}.$'))
            display(Latex(f'The standard error of the data is $\sigma_\mu = \sigma/\sqrt{{N}} = {stdErrorPrint}' + r'\times' + f'10^{{ {power} }}\, \mathrm{{ {xUnits} }}.$'))
        
        # Add units if they were provided.
        if xUnits != '':
            xlabel = xlabel + ' (' + xUnits + ')'
        
        # Format and show the plot.
        plt.xlabel(xlabel)
        if normalized == True:
            plt.ylabel('Normalized Counts')
        else:
            plt.ylabel('Counts')
        ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
        plt.show()
        stdError = float(stdError)
    return counts, centres, average, stdDev, stdError, fig


###############################################################################
# Overlay Multiple Histograms                                                 #
# - modified 20220529                                                         #
###############################################################################        
# Start the 'HistOverlay' function.
def HistOverlay(dataArray, nbins = 10, xlabel = 'x-axis', xUnits = '',  normalized = True, transparency = 0.75):
    countsArray = ''
    centresArray = ''
    fig = ''
    if len(dataArray)==0:
        display(html_print(cstr("The 'dataArray' list must not be empty.", color = 'magenta')))
    elif all(isinstance(x, list) or type(x).__module__ == np.__name__ for x in dataArray) != True: # Is dataArray a list of lists or arrays?
        display(html_print(cstr("The 'dataArray' must be a list of lists.", color = 'magenta')))
    elif isinstance(nbins, int) == False or nbins < 0:
        display(html_print(cstr("'nbins' must be a positive integer.", color = 'magenta')))
    elif isinstance(xlabel, str) == False:
        display(html_print(cstr("'xlabel' must be a string.", color = 'magenta')))
    elif isinstance(xUnits, str) == False:
        display(html_print(cstr("'xUnits' must be a string.", color = 'magenta')))
    elif normalized != True and normalized != False:
        display(html_print(cstr("The 'normalized' parameter must be set to either True or False.", color = 'magenta')))
    elif isinstance(transparency, int) == False and isinstance(transparency, float) == False:
        display(html_print(cstr("The 'transparency' parameter must be a number between 0 (completely transparent) and 1 (opaque).", color = 'magenta')))
    elif transparency < 0 or transparency > 1:
        display(html_print(cstr("The 'transparency' parameter must be a number between 0 (completely transparent) and 1 (opaque).", color = 'magenta')))
    else:
        # Check to see if dataArray is a numpy array.  It it is, convert to a list.
        if  type(dataArray).__module__ == np.__name__:
            dataArray = dataArray.tolist()
        # Check to see if the elements of dataArray are numpy arrays.  If they are, convert to lists
        for i in range(len(dataArray)):
            if  type(dataArray[i]).__module__ == np.__name__:
                    dataArray[i] = dataArray[i].tolist()
        # Generate a sequence of colours used to plot the the multiple histograms.
        colour = iter(cm.rainbow(np.linspace(0, 1, len(dataArray))))
        tot = sum(dataArray, []) # Combine the list of lists into a single large list
        if all(isinstance(x, (int, float)) for x in tot) != True:
            display(html_print(cstr('All elements of the provided data must be integers or floats.', color = 'magenta')))
            return countsArray, centresArray, fig
        # Calculate the boundaries of the histogram bins
        binwidth = (np.max(tot) - np.min(tot))/nbins
        boundaries = np.arange(np.min(tot), np.max(tot) + binwidth, binwidth)
        
        # Perpare a squre figure
        fig = plt.figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot the histograms and store the outputs in lists.
        countsArray = []
        centresArray = []
        for i in range(len(dataArray)): 
            c = next(colour)
            c[3] = transparency
            counts, edges, patches = plt.hist(dataArray[i], bins = boundaries, fc = c, edgecolor='k', density = normalized)
            centres = edges[0:len(counts)] + binwidth/2
            countsArray.append(counts)
            centresArray.append(centres)           
        
        # Add units if they were provided.
        if xUnits != '':
            xlabel = xlabel + ' (' + xUnits + ')'
            
        # Format and show the plot.
        plt.xlabel(xlabel)
        if normalized == True:
            plt.ylabel('Normalized Counts')
        else:
            plt.ylabel('Counts')
        ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box') # Make the plot square
        plt.show()
    return countsArray, centresArray, fig


###############################################################################
# Import Image & Add a Caption                                                #
# - modified 20220711                                                         #
###############################################################################        
# Start the 'Import Image' function.
def ImportImage(filename, caption = '', size = 5, rotation = 0):
    from os.path import exists as file_exists
    fig = ''
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.eps')) == False:
        display(html_print(cstr('The file type must be one of the following: png, jpg, jpeg, gif, eps.', color = 'magenta')))
    elif file_exists(filename) == False:
        display(html_print(cstr("The file '" + filename + "'does not exist.  Check the file name and ensure that it is in the same directory as your current Jupyter Notebook.", color = 'magenta')))
    elif isinstance(caption, str) == False:
        display(html_print(cstr('The caption must be a string.', color = 'magenta')))
    elif "\\" in r"%r" % caption:
        display(html_print(cstr(r"The caption cannot contain backslashes '\'.", color = 'magenta')))
    elif isinstance(rotation, (float, int)) == False:
        display(html_print(cstr('The rotational angle must be a float or integer.  It represents the rotation angle in degrees.', color = 'magenta')))
    else:
        from PIL import Image
        fig = plt.figure(figsize=(size, size), dpi=100) # create a square figure.
        img = Image.open(filename) # Open the file
        img = img.rotate(rotation, expand = 1) # Rotate the file.
        plt.imshow(img)
        plt.axis('off') # Remove the axes from the 'plot'.
        plt.text(0, 4300,'%s' %caption, size = 14, color = "k") # Add the caption below the image.
        plt.show() # Show the image.
    return fig
    
    
###############################################################################
# Enter Data using a Spreadsheet-like Environment                             #
# Makes use of data_entry which was written by Carl Michal (UBCV)             #
# - modified 20220621                                                         #
###############################################################################       
# Check to see if ipysheet is installed.
def Spreadsheet(csvName):
    if isinstance(csvName, str) == False:
        display(html_print(cstr("'csvName' must be a string.", color = 'magenta')))
    else:
        install_and_import('ipysheet')
        import data_entry
        data_entry.sheet(csvName)
    return


###############################################################################
# Produce contour and vector field plots                                      #
# - modified 20220816                                                         #
###############################################################################       
# Check to see if ipysheet is installed.
def Mapping(x_coord, y_coord, potential, graphNum = 0, vectorField = True):
    
    import matplotlib.pyplot as plt
    import scipy.interpolate
    from matplotlib.pyplot import figure
    from scipy import interpolate
    from IPython.display import HTML as html_print
    from scipy.interpolate import interp1d

    fig = ''
    
    # Check for errors in the inputs.
    if len(x_coord) != len(y_coord):
        display(html_print(cstr('The length of x_coord (' + str(len(x_coord)) + ') is not equal to the length of y_coord (' + str(len(y_coord)) + ').', color = 'magenta')))
    elif len(x_coord) != len(potential):  
        display(html_print(cstr('The length of x_coord (' + str(len(x_coord)) + ') is not equal to the length of potential (' + str(len(potential)) + ').', color = 'magenta')))
    elif len(y_coord) != len(potential):  
        display(html_print(cstr('The length of y_coord (' + str(len(y_coord)) + ') is not equal to the length of potential (' + str(len(potential)) + ').', color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in x_coord) != True:
        display(html_print(cstr("The elements of 'x_coord' must be integers or floats.", color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in y_coord) != True:
        display(html_print(cstr("The elements of 'y_coord' must be integers or floats.", color = 'magenta')))
    elif all(isinstance(x, (int, float)) for x in potential) != True:
        display(html_print(cstr("The elements of 'potential' must be integers or floats.", color = 'magenta')))
    elif isinstance(graphNum, int) == False:
        display(html_print(cstr("'graphNum' must be an integer from 1 to 7 corresponding to the graph number on your board.", color = 'magenta')))
    else:
        
        x = x_coord
        y = y_coord
        V = potential
 
        # First, interpolate the data that was entered.  There's no extrapolation here.
        # We're using this method initially because it does not require a regular grid of input data and the data does not 
        # need to be sorted.
        N = 200
        xi = np.linspace(1, 24, N)
        yi = np.linspace(1, 18, N)
        zi = scipy.interpolate.griddata((x, y), V, (xi[None,:], yi[:,None]), method = 'cubic')
        
        # Check if there are any 'NaN' entries in zi, where 'NaN' means 'not a number'.  
        # If a 'NaN' is found, show the current potential map and go no further.  The 'NaN' will break the next step 
        # of the function.
        if np.isnan(np.min(zi)) == True:
            fig = plt.figure(figsize=(12, 8), dpi=100)
            ax = fig.add_subplot(111)
            plt.contourf(xi, yi, zi, levels = np.arange(-0.5, 11, 0.1), cmap='RdYlBu_r');
            plt.colorbar(ticks = np.linspace(0, 10, 11))
            plt.contour(xi, yi, zi, levels = np.arange(-0.5, 11, 0.5), colors = 'dimgray', linewidths = 0.5);
            plt.axis((0, 25, 0, 20))
            plt.xlabel('x (cm)')
            plt.ylabel('y (cm)')
            ax.set_xticks([0, 5, 10, 15, 20, 25])
            ax.set_yticks([0, 5, 10, 15, 20])
            plt.gca().set_aspect(1)
            print('There are gaps in the data.  Please collect more data to fill in parts of the plot that are empty.')
        else:
        
            # The interpolated data follows a grid and is sorted.  Now do a second interpolation that does include exprapolation.
            # The extrapolation will fill the plot from zero to 25 in the x direction and from zero to 20 in the y direction.
            xx, yy = np.meshgrid(xi, yi)
            Z = np.zeros(np.shape(xx))

            f = interpolate.interp2d(xi, yi, zi, kind='cubic')

            xnew = np.arange(0, 25.025, 0.025)
            ynew = np.arange(0, 20.025, 0.025)
            znew = f(xnew, ynew)

            if graphNum == 6:
                btm = -1
            else:
                btm = -0.5
            
            # Generate the contour plot.
            fig = plt.figure(figsize=(12, 8), dpi=100)
            ax = fig.add_subplot(111)
            plt.contourf(xnew, ynew, znew, levels = np.arange(btm, 11, 0.1), cmap='RdYlBu_r');
            plt.colorbar(ticks = np.linspace(0, 10, 11))
            CS = plt.contour(xnew, ynew, znew, levels = np.arange(btm, 11, 0.5), colors = 'dimgray', linewidths = 0.5);
            # ax.clabel(CS, CS.levels, inline=True, fontsize=10)
            plt.axis((0, 25, 0, 20))
            plt.xlabel('x (cm)')
            plt.ylabel('y (cm)')
            ax.set_xticks([0, 5, 10, 15, 20, 25])
            ax.set_yticks([0, 5, 10, 15, 20])
            plt.gca().set_aspect(1)

            Sc = 2
            fact = 1
            # The following if statement is used to mark the positions of the electrodes and/or conductive paint.
            if graphNum == 1:
                Sc = 2
                fact = 1
                plt.plot(6.5,10, marker = 'o', markersize = 7, markerfacecolor = 'r', markeredgecolor = 'white', linewidth = 3)
                plt.plot(18.5,10, marker = 'o', markersize = 7, markerfacecolor = 'k', markeredgecolor = 'white', linewidth = 3)
            elif graphNum == 2:
                Sc = 3
                fact = 1
                plt.plot(3.7,10, marker = 'o', markersize = 7, markerfacecolor = 'r', markeredgecolor = 'white', linewidth = 3)
                plt.plot(21.5,10, marker = 'o', markersize = 7, markerfacecolor = 'k', markeredgecolor = 'white', linewidth = 3)
                plt.gca().add_patch(plt.Circle((12.5, 10), 5.7, edgecolor='silver', facecolor = 'None', linewidth = 3)) 
            elif graphNum == 3:
                Sc = 2
                fact = 1
                point1 = [6.5, 4]
                point2 = [6.5, 16]
                x_values = [point1[0], point2[0]]
                y_values = [point1[1], point2[1]]
                plt.plot(x_values, y_values, color = 'silver', linestyle='solid', linewidth = 3)
                point3 = [18.7, 4]
                point4 = [18.7, 16]
                x_values = [point3[0], point4[0]]
                y_values = [point3[1], point4[1]]
                plt.plot(x_values, y_values, color = 'silver', linestyle='solid', linewidth = 3)    
            elif graphNum == 4:
                Sc = 2
                fact = 1
                point1 = [5.5, 4]
                point2 = [5.5, 16]
                x_values = [point1[0], point2[0]]
                y_values = [point1[1], point2[1]]
                plt.plot(x_values, y_values, color = 'silver', linestyle='solid', linewidth =3)
                # Enter a parametric equation that defines a 'teardrop' shape.
                tt = np.arange(0, 2*np.pi, 0.01)
                x4fcn = -np.cos(tt)*7.3/2 + 13 + 7.5/2
                y4fcn = np.sin(tt)*np.sin(tt/2)*5/1.5 + 10
                #x4 = [13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 20, 19.6, 19, 18.5, 18, 17.5, 17, 16.5, 16, 15.5, 15, 14.5, 14, 13.5, 13]
                #y4 = [10, 9.6, 9.2, 8.8, 8.5, 8.2, 8, 7.8, 7.7, 7.5, 7.4, 7.6, 7.9, 8.3, 9 , 10, 11, 11.7, 12.1, 12.4, 12.6, 12.5, 12.3, 12.2, 12, 11.8, 11.5, 11.2, 10.8, 10.4, 10]
                plt.plot(x4fcn, y4fcn, 'silver', linewidth = 3)
            elif graphNum == 5:
                Sc = 2
                fact = 1
                point1 = [6.5, 4]
                point2 = [6.5, 16]
                x_values = [point1[0], point2[0]]
                y_values = [point1[1], point2[1]]
                plt.plot(x_values, y_values, color = 'silver', linestyle='solid', linewidth = 3)
                point3 = [13.2, 4]
                point4 = [18.5, 16]
                x_values = [point3[0], point4[0]]
                y_values = [point3[1], point4[1]]
                plt.plot(x_values, y_values, color = 'silver', linestyle='solid', linewidth = 3)      
            elif graphNum == 6:
                Sc = 4
                fact = 1
                point1 = [6.5, 4]
                point2 = [6.5, 16]
                x_values = [point1[0], point2[0]]
                y_values = [point1[1], point2[1]]
                plt.plot(x_values, y_values, color = 'silver', linestyle='solid', linewidth = 3)
                point3 = [18.5, 4]
                point4 = [18.5, 16]
                x_values = [point3[0], point4[0]]
                y_values = [point3[1], point4[1]]
                plt.plot(x_values, y_values, color = 'silver', linestyle='solid', linewidth = 3)  
                plt.gca().add_patch(plt.Rectangle((11.5, 8), 2, 4, edgecolor='slategray', facecolor = 'slategray', linewidth = 3, alpha = 0.75))
                plt.gca().add_patch(plt.Rectangle((11.5, 8), 2, 4, edgecolor='k', facecolor = 'None', linewidth = 3))
            elif graphNum == 7:
                Sc = 10
                fact = 2
                plt.gca().add_patch(plt.Circle((12.5, 10), 5.6, edgecolor='silver', facecolor = 'None', linewidth = 3))
                plt.gca().add_patch(plt.Circle((12.5, 10), 1.6, edgecolor='silver', facecolor = 'None', linewidth = 3))
            else:
                print('Enter an integer from 1 to 7 corresponding to the Graph Number on your board to show the positions of the electrodes.')

            if vectorField == True:
                # Calculate the electric field at all the points in the interpolated/extrapolated potential.
                xEle, yEle = np.mgrid[0:25.025:0.025, 0:20.025:0.025]
                zEle = np.transpose(znew)
                Ex, Ey = np.gradient(zEle, 0.025, 0.025)
                Ex = -Ex
                Ey = -Ey

                # Sample some of the electric field points for plotting.
                x_E = np.zeros(np.shape(xEle))
                y_E = np.zeros(np.shape(xEle))
                ExSub = np.zeros(np.shape(xEle))
                EySub = np.zeros(np.shape(xEle))
                x_cnt = 0
                for i in range(0, np.shape(Ex)[0], int(100/fact)):
                    y_cnt = 0
                    for j in range(0, np.shape(Ey)[1], int(80/fact)):
                        x_E[x_cnt][y_cnt] = xEle[i][j]
                        y_E[x_cnt][y_cnt] = yEle[i][j]
                        ExSub[x_cnt][y_cnt] = Ex[i][j]
                        EySub[x_cnt][y_cnt] = Ey[i][j]
                        if graphNum == 6 and xEle[i][j] >= 11.5 and xEle[i][j] <= 13.5 and yEle[i][j] >= 8 and yEle[i][j] <= 12:
                            x_E[x_cnt][y_cnt] = -1
                            y_E[x_cnt][y_cnt] = -1
                            ExSub[x_cnt][y_cnt] = 0
                            EySub[x_cnt][y_cnt] = 0
                        y_cnt += 1
                    x_cnt += 1
        
                # Plot the electric field vectors.
                plt.quiver(x_E, y_E, ExSub, EySub, scale = Sc, scale_units = 'inches', width = 0.0035, color = 'k')

    return fig