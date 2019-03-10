import os
import pandas as pd
import math
from datetime import datetime
import sys

rootdir = "C:\Users\user\Google Drive\Ronin\Invoices"
template_file = "{}\\StatementImportTemplate.csv".format(rootdir)

# Get the Xero approved headings from the CSV template
template = pd.read_csv(template_file, nrows=1)
xero = pd.DataFrame([], columns=template.columns)
#print( xero.columns )


read_dir = "C:\Users\user\Google Drive\Ronin\Accounts"
# Get all the rows from all the tabs!
for filename in os.listdir(read_dir):
 
    fullpath = "{}\{}".format( read_dir, filename )  
    print( "Processing {}".format(fullpath)) 
    
    # Work out the tab range
    workbook = pd.ExcelFile( fullpath )
    quarters = list( workbook.sheet_names )
    
    for quarter in quarters:
        print( "{}".format( quarter ))

        current = workbook.parse(
                quarter, 
                usecols="A:D", 
                header=None,
                index = None,
                names = [ 'Dates','Details','safety', 'Amount'],
                #dtype = str,
                )
        
        write_flag = False
        sign = 1
        
        # identify individual bank payments
        for index, row in current.iterrows():
            
            details = row['Details']
            rdate = row['Dates']
            
            if details == 'BANK RECEIPTS':
                write_flag = True
            elif details == 'BANK PAYMENTS':
                write_flag = True
                sign = -1
            elif details == 'Check Calculation:':
                write_flag = False
            elif str( details ) == ' ' or ":{}:".format( details ) == ':nan:':
                # do we need to do anything?
                i = 0
            elif details== 'Nature of Expense':
                i = 0
            else:
                if write_flag:
                    if type( rdate ) == datetime:
                        
                        amount = float( row['Amount'] )
                        print( "{} - {} - {:.2f}".format( rdate , details, amount ) )
               
                        # write something to calculate tax rate from net and tax
                        line = pd.DataFrame({
                                "*Date":    ["{:%d/%m/%Y}".format( rdate )],
                                "*Amount" : ["{:.2f}".format(amount*sign)],
                                "Description" :   [details],
        
                                },
                                columns = template.columns
                        )
                        xero = xero.append( line, ignore_index = True )
                  
      
xero.to_csv( "{}/toad.csv".format( read_dir), index = False )