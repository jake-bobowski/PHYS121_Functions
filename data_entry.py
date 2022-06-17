""" data_entry.py - A spreadsheet interface for data entry in Python/Jupyter 

    2022 Carl Michal

    To use:

    import data_entry

    then:
    de = data_entry.sheet("name")
    creates or loads name.csv and
    presents as a "live" spreadsheet-like interface. This is for data entry
    only, no calculations are possible in the spreadsheet.

    put a # in front of a row to comment it out
    put a $ in front of a column name to comment out the column (useful for
        non-numeric columns)

    Generate Vectors generates a series of arrays for each non-commented
    column.

    Two pandas data frames are also created:
    - one is self.df that contains just the data in the vectors.
    - the other, self.fdf is strings that has everything in the whole table.

    To take a snapshot of a current sheet and generate a new one:
    de2 = data_entry.sheet_copy("old", "new")

    if new.csv exists, it gets loaded, if not, old.csv is copied to new.csv.

    BUGS: the sheet doesn't render when the notebook is exported. This
    seems to be a limitation of the ipysheet extension. Its worked-around
    by diplaying the dataframe, which does export properly.

"""

import numpy as np
import os
import matplotlib.pyplot as plt
import ipysheet
import ipywidgets as widgets
import re
import pickle
from IPython import get_ipython
import pandas as pd
import time
import glob
import filecmp
import shutil

# Question: should the generated arrays be in global namespace or within the object?
# Question: should the undo file be hidden?
# Question: created array message could show how to do it?

BACKUP_DIR = 'csv_backups/'

class sheet:
   
    # function called on every cell update:
    def my_callback(self, val):
        
        self.out.clear_output()
        with self.out:
            print("Data vectors need to be updated")
        cell = val.owner

        # sanitize - remove any commas:
        try:
            if ',' in cell.value:
                cell.value = cell.value.replace(',', ';')
                with self.out:
                    print("Comma in cell replaced with ;")
        except:
            pass
        
        # Deal with undo list:
        if self.doing_undo == False:
            if self.was_undoing:
                # move redo_list to undo_list:
                self.undo_list = self.undo_list + self.redo_list
                self.redo_list = []
                self.was_undoing = False
            
            # add this event to the undo list: undo/redo saves the list itself.
            self.undo_list = self.undo_list + [(cell.row_start, cell.column_start, self.mar[cell.row_start, cell.column_start])]
            self.save_undo_list(self.undo_list)
        # maybe only do this if we're not in the first row?
        # try: 
        #     number = float(cell.value)
            # set to normal colour
        # except:
        #     print("cell is not numeric?") 
        # cell.type = 'numeric'
                
        # save the sheet:
        self.mar = ipysheet.to_array(self.sh)
        try:
            np.savetxt(self.fname, self.mar, fmt='%s', delimiter=',')
        except:
            with self.out:
                print("Failed to save csv file!")

    def add_row(self, _):
        self.sh.rows += 1
        self.sh.row_headers = self.sh.row_headers + [str(self.sh.rows-3)]
        self.my_cells = np.vstack( (self.my_cells,np.empty((1, self.sh.columns), dtype='object')))
        # add cells in the new row!
        for i in range(self.sh.columns):
            cell = ipysheet.cell(self.sh.rows-1, i, '') # how to handle if multiple sheets?
            self.my_cells[self.sh.rows-1, i] = cell
            cell.observe(self.my_callback, 'value')
        self.mar = ipysheet.to_array(self.sh)

    def add_col(self, _):
        self.sh.columns += 1
        self.my_cells = np.hstack((self.my_cells,np.empty((self.sh.rows, 1), dtype='object')))
        # add cells to the new column
        for i in range(self.sh.rows):
            cell = ipysheet.cell(i, self.sh.columns-1, '') # multiple sheets?
            self.my_cells[i, self.sh.columns-1] = cell    
            cell.observe(self.my_callback, 'value')
        self.mar = ipysheet.to_array(self.sh)

    def undo(self, _):
        if len(self.undo_list) < 1:
            return
        self.was_undoing = True
        self.doing_undo = True 
        r,c,v = self.undo_list.pop()

        while (r >= self.sh.rows):
            self.add_row(0)
        while(c >= self.sh.columns):
            self.add_col(0)
        self.redo_list = self.redo_list + [(r,c,self.mar[r,c])]
        self.my_cells[r, c] .value = v
        self.doing_undo = False

        # for save:
        save_list = self.undo_list + self.redo_list
        self.save_undo_list(save_list)
        
    def redo(self, _):
        if len(self.redo_list) < 1:
            return
        self.was_undoing = True
        self.doing_undo = True 
        r,c,v = self.redo_list.pop()
        self.undo_list = self.undo_list + [(r,c,self.mar[r,c])]
        self.my_cells[r, c].value = v
        
        self.doing_undo = False

        # for save:
        save_list = self.undo_list + self.redo_list
        self.save_undo_list(save_list)
        
    def generate(self, _, silent=False):
        self.out.clear_output()
        with self.out:
            # Look at column names, sanitize and find commented columns
            vnames = []
            for j in range(self.sh.columns):
                vn = self.mar[0,j]
                # fix up so its a legal variable name: 
                # prepend v_ then convert any illegal character to _ but remove trailing _
                vn2 = 'v_' + re.sub("[^0-9a-zA-Z]+", "_", vn).rstrip('_')
                # print("col",j,", name is",vn2)
                # Check for duplicates
                if vn2 in vnames and vn2 != 'v_':
                    if silent == False:
                        print("Duplicate column name:",vn2)
                        print("Aborting")
                    return
                if vn2 == 'v_':
                    if silent == False:
                        print("Skipping column", j, "because it does not have a valid name")
                # names that start with $ are commented out columns:
                if len(vn) > 0:
                    if vn[0] == '$':
                        vn2 = 'v_'
                        if silent == False:
                            print("Skipping column",j , 'because it is commented')
                vnames = vnames + [vn2]
            # now go through rows and build array
            nar = np.zeros((self.sh.rows-2, self.sh.columns))
            mrow = 0
            row_indices = [] # for data frame
            for i in range(2, self.sh.rows):
                # within the row, check that all are legal numeric values:
                try:
                    for j in range(self.sh.columns):
                        if vnames[j] != 'v_':
                            nar[mrow, j] = float(self.mar[i, j])
                    row_indices = row_indices + [i-2]
                    mrow += 1
                except:
                    if silent == False:
                        print("Row #",i-2,"skipped")
            # make the arrays:
            if mrow > 0:
                if silent == False:
                    print("Found",mrow,"valid rows")
                # print(nar[:mrow])

                col_names = [] # for data frame
                col_arrays = []
                # ok, create the variables:
                for j in range(self.sh.columns):
                    if vnames[j] != 'v_':
                        # insert our array:
                        
                        # this inserts into our object, not a bad idea maybe?
                        # command = 'self.'+vnames[j]+' = np.array('+str(list(nar[:mrow, j]))+')'
                        # exec(command)
                        
                        # this is into the global module namespace. Not useful inside object.
                        # command = 'self.'+vnames[j]+' = np.array('+str(list(nar[:mrow, j]))+')'
                        # globals()[vnames[j]] = nar[:mrow, j]
                        
                        # this makes it global when in notebook:
                        command = vnames[j]+' = np.array('+str(list(nar[:mrow, j]))+')'
                        try:
                            get_ipython().ex(command)
                            
                            # prep to make dataframe.
                            col_names = col_names + [vnames[j][2:]] # chop off the v_ in the name
                            col_arrays = col_arrays + [nar[:mrow, j]]
                            if silent == False:
                                # print("\nCreated array:",vnames[j], "with values:")
                                # print(str(list(nar[:mrow, j])))
                                print("\nCreated array:\n", command)
                        except:
                            if silent == False:
                                print('Failed to create array. Please include "import numpy as np" in first code cell.')
                            break
                # make a data frame - place inside our object.
                if len(col_names) > 0 and len(row_indices) > 0:
                    # print(col_arrays)
                    # print(col_names)
                    col_arrays = np.array(col_arrays).transpose()
                    self.df = pd.DataFrame(col_arrays, row_indices, col_names)
                    
            else: # no valid rows found
                if silent == False:
                    print("No valid data rows found. Giving up")
            # Also build a dataframe out of text that looks like our entire sheet:
            self.fdf = pd.DataFrame(self.mar[1:], ['Units']+list(range(self.sh.rows-2)) , self.mar[0])
            display(self.fdf)
            
            # now do file checkpointing. If current file is different from most recent checkpoint, save a checkpoint.

            # need to find all checkpoints
            dir_entries = glob.glob(BACKUP_DIR + self.fname + '*')
            # print(dir_entries)
            # go through them, look for numerical suffixes and look for latest:
            maxtime = 0
            maxindex = 0
            mintime = int(time.time())
            minindex = 0
            num_backups = 0
            for i in range(len(dir_entries)):
                fields = dir_entries[i].split('.')
                # print(fields)
                try:
                    stime = int(fields[-1])
                    num_backups += 1
                    # print(stime)
                    if stime > maxtime:
                        maxtime = stime
                        maxindex = i
                    if stime < mintime:
                        mintime = stime
                        minindex = i
                except:
                    pass
                
            if num_backups > 1:
                if filecmp.cmp(dir_entries[maxindex], self.fname) == True:
                    return
                
            utime = int(time.time())
            backup_name = BACKUP_DIR + self.fname + '.' + str(utime)
            # print("backup_name will be",backup_name)
            shutil.copyfile(self.fname, backup_name)

            # If there are more than 10 checkpoints, remove the oldest.
            if num_backups > 9:
                os.remove(dir_entries[minindex])
                

    def save_undo_list(self, list_to_save):
        try:
            undo_file = open(self.undo_name, "wb")
            pickle.dump(list_to_save, undo_file)
            undo_file.close()
        except:
            with self.out:
                print("Couldn't save undo history file. Permisions?")



    def __init__ (self, name):
        
        
        self.mar = None
        oar = None
        
        self.undo_list = []
        self.redo_list = []

        self.doing_undo = False
        self.was_undoing = False
    
        self.out = widgets.Output()

        # if there are any / in the file name, give up.
        if name.find('/') != -1:
            print("file name cannot refer to a different path. Remove any / characters from file name.")
            return None
        
        if not os.path.exists(BACKUP_DIR):
            print("Creating directory for backups: ",BACKUP_DIR)
            os.makedirs(BACKUP_DIR)

        
        self.fname = name + '.csv'
        self.undo_name = BACKUP_DIR + name + '.csv.undo'
        if (len(name) >= 4): # if the user's name ends in .csv, don't add it again.
            if name[-4:] == '.csv':
                self.fname = name
                self.undo_name = BACKUP_DIR + name + '.undo'


        # oar = old array, loaded in
        # mar is always the current array
        # nar is used when generating final output vectors, local to generate()
        # oar and mar are arrays of strings. nar is an array of floats.
    
        # Here see if fname (.csv) exists, and if so load it:
        file_read_ok = False
        try:
            oar = np.loadtxt(self.fname, dtype=str, delimiter=',', comments=None)
            rows, cols = oar.shape
            # look for empty columns:
            # can we remove empty columns:
            col = cols-1 # cols is the number of cols, col is the one we're looking at.
            all_empty = True
            while (col > 0):
                for i in range(rows):
                    if oar[i, col] != "":
                        all_empty = False
                        col = 0
                        break
                if all_empty == True:
                    # print("removing col:",col)
                    cols = cols -1
                    col = col -1
            # can we remove empty rows:
            row = rows-1
            all_empty = True
            while (row > 0):
                for i in range(cols):
                    if oar[row, i] != "":
                        all_empty = False
                        row = 0
                        break
                if all_empty == True:
                    # print("removing row:",row)
                    rows = rows -1
                    row = row -1
            # if rows < 10:  This causes problems later...
            #     rows = 10
            # if cols < 3:
            #     cols = 3
            file_read_ok = True
        except:
            rows = 10
            cols = 3
        if file_read_ok:
            try:
                # print("trying to open undo file")
                undo_file = open(self.undo_name, 'rb')
                self.undo_list = pickle.load(undo_file)
                undo_file.close()
                # print("undo_list",self.undo_list)
                # limit length of undo list?
                if len(self.undo_list) > 500:
                    self.undo_list = self.undo_list[len-500:]
            except:
                print("Creating undo file")
                pass

                    
        add_row_button = widgets.Button(description='Add Row')
        add_row_button.on_click(self.add_row)

        add_col_button = widgets.Button(description='Add Column')
        add_col_button.on_click(self.add_col)

        undo_button = widgets.Button(description='Undo')
        undo_button.on_click(self.undo)

        redo_button = widgets.Button(description='Redo')
        redo_button.on_click(self.redo)

        generate_button = widgets.Button(description='Generate Vectors')
        generate_button.on_click(self.generate)

        # build row headers:
        rh = ['Variable:', 'Units:']
        for i in range(rows-2):
            rh = rh + [str(i)]
        self.sh = ipysheet.sheet(rows=rows, columns = cols, row_headers = rh, column_headers = False)
        
        # build an array to hold cells
        self.my_cells = np.empty((rows,cols), dtype='object')
        # create the cell entries and store them:
        for i in range(rows):
            for j in range(cols):
                if oar is not None:
                    cell = ipysheet.cell(i,j,oar[i,j])
                else:
                    cell = ipysheet.cell(i,j,'')
                self.my_cells[i,j] = cell
                cell.observe(self.my_callback, 'value')
        self.mar = ipysheet.to_array(self.sh)

        if file_read_ok == False:
            try:
                np.savetxt(self.fname, self.mar, fmt='%s', delimiter=',')
            except:
                with self.out:
                    print("Failed to save csv file!")
       
        self.save_undo_list(self.undo_list)
                
        hb=widgets.HBox([undo_button, redo_button, add_row_button, add_col_button, generate_button])
        # Display it:
        print("Sheet name:", self.fname)
        self.sheet = widgets.VBox([self.sh, hb, self.out])
        self.generate(self, silent = True)
        display(self.sheet)
        # cfg=get_ipython()
        # print(cfg)
        return None


    
def sheet_copy(old_sheet, new_sheet):
    # check to see if filename(s) ends in .csv, and if so, don't add it again.
    old_name = old_sheet + '.csv'
    if len(old_sheet) > 4:
        if old_sheet[-4:] == '.csv':
            old_name = old_sheet
            
    new_name = new_sheet + '.csv'
    if len(new_sheet) > 4:
        if new_sheet[-4:] == '.csv':
            new_name = new_sheet

        
    if os.path.isfile(new_name) == False: # check to see if you already have an existing filename
        shutil.copyfile(old_name, new_name)
        print("Copied", old_name,"to", new_name)
    return sheet(new_name)



## if this module is executed as a script, install it into
# ~/.local/lib/pythonx.y/site-packages/

if __name__ == "__main__":
    import platform
    import sys
    print("Self installer for: data_entry.py")

    ver = platform.python_version_tuple()
    new_path = os.path.expanduser('~') + '/.local/lib/python%s.%s/site-packages'%(ver[0],ver[1])

    print(__file__," will be moved to:", new_path, "so that it can be imported.")
    val = 'y'
    if os.path.exists(new_path + '/data_entry.py'):
        print("File exists, proceeding will overwrite a previous version.")
        val = input("Do you wish to proceed: [y/n]? ")

    if val != 'y':
        print("Aborting")
        sys.exit()
    try:
        os.makedirs(new_path)
    except:
        pass
    try:
        shutil.move(__file__, new_path + '/data_entry.py')
        print("Installation complete")
    except:
        print("Installation failed")
    
