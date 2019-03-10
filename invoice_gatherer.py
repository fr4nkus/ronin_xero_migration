import os
import pandas as pd
import re
from pprint import pprint
import math
import sys
from datetime import datetime

rootdir = "C:\Users\user\Google Drive\Ronin\Invoices"
num_only = re.compile( r'^\d+(\.\d)?$' )
template_file = "{}\\SalesInvoiceTemplate.csv".format(rootdir)

# Get the Xero approved headings from the CSV template
template = pd.read_csv(template_file, nrows=1)
#print( template.columns )

xero = pd.DataFrame([], columns=template.columns)

# Get all the rows from all the tabs!
for filename in os.listdir(rootdir):
    if 'invoices_' not in filename:
        continue
    
    fullpath = "{}\{}".format( rootdir, filename )  

    # Work out the tab range
    workbook = pd.ExcelFile( fullpath )
    inv_nos = list( filter(lambda n: num_only.match(n), workbook.sheet_names) )
    
    for inv_no in inv_nos:
        current = workbook.parse(
                inv_no, 
                usecols="A:F", 
                header=0,
                names = [ 'AB','C','DE','F'],
                dtype = str,
                )
        inv_date = current.iloc[4][3]
        inv_date = inv_date.split(' ')[0]
        company = str( current.iloc[4][0] ).split('\n')[0]
        net = float( current.iloc[-1][3] )
        checksum = 0.0
        inv_date = datetime.strptime(inv_date, '%Y-%m-%d')
        
        # identify individual payments
        for index, row in current.iterrows():
            if isinstance(row.name[0],float) or isinstance(row.name[0],int):
                if math.isnan(row.name[0]) or math.isnan(row.name[1]):
                    continue
                
                # decide which VAT type to use.
                # which column has the vat value in 
                tax_amt = row['DE']
                pre_tax = float(row.name[0]) * float(row.name[1])
                vat_pct = float( tax_amt ) / pre_tax
                vat_rate = vat_pct
                
                if vat_pct == 0.175:
                    vat_rate = "17.5% (VAT on Income)"
                elif vat_pct == 0.2:
                    vat_rate = "20% (VAT on Income)"
                elif vat_pct == 0.15:
                    vat_rate = "15% (VAT on Income)"
                else:
                    vat_rate = "No VAT"
                
                # write something to calculate tax rate from net and tax
                line = pd.DataFrame({
                        "*ContactName":    [company],
                        "*InvoiceNumber" : ["{:07d}".format(int(float(inv_no)))],
                        "*InvoiceDate" :   ["{:%d/%m/%Y}".format( inv_date )],
                        "*DueDate" :       ["{:%d/%m/%Y}".format( inv_date )],
                        "*Description" :   [row['AB']], 
                        "*Quantity" :      [float(row.name[0])],
                        "*UnitAmount" :    [float(row.name[1])], 
                        "*AccountCode" :   ["200"],
                        "*TaxType" :       [vat_rate],
                        "TaxAmount" :      [tax_amt],
                        "Currency" :       ['GBP'],
                        },
                        columns = template.columns
                )
                xero = xero.append( line, ignore_index = True )

                checksum += float( row['F'])                    

        # ensure it adds up to the net!
        if net != checksum:
            print( "checksum-mismatch!! {} - {} for {} at £{}".format( inv_no, inv_date, company, net ))
            
xero.to_csv( "{}/frog.csv".format( rootdir), index = False )