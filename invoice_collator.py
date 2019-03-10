import pandas as pd

datadir="C:\Users\user\Google Drive\Invoices"
datadir="C:\Users\user\Google Drive\Invoices"
# os.listdir( datadir )
tgt = "{}\{}".format( datadir, "invoices_2017-2018 (533-567).xlsx" )
print( tgt )

foo = pd.ExcelFile( tgt )

for inv_no in foo.sheet_names:
    current = foo.parse( inv_no, usecols="A:F", header=0 )
    inv_date = current.iloc[4][3]
    company = current.iloc[4][0]
    net = current.iloc[-1][3]
    
    print( "{} - {} for {} at £{}".format( inv_no, inv_date, company, net ))