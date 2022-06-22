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
# Check to see if ;package' is already installed.  If not, then attempt
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
    if len(xData) != len(yData):
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
# - modified 20220621                                                         #
############################################################################### 
# Start the 'PowerLaw' function.
def PowerLaw(xData, yData, yErrors = [], xlabel = 'x-axis', ylabel = 'y-axis', xUnits = '', yUnits = ''):
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
# - modified 20220607                                                         #
###############################################################################        
# Start the 'Import Image' function.
def ImportImage(filename, caption = '', rotation = 0):
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
        fig = plt.figure(figsize=(5, 5), dpi=100) # create a square figure.
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