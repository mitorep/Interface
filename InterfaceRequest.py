import pyodbc
import requests
from requests.auth import HTTPBasicAuth
server =  'Server'
database = 'Database'
username = 'login'
password = 'password'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

cursor.execute("exec Events_Procedure") 
row = cursor.fetchone()

while row: 
    if row[0] == 58:
        toExec = row
        
        row = cursor.fetchone()
    else:
        row = cursor.fetchone()

getXML = cnxn.cursor()
getXML.execute("exec XML_Procedure "+str(toExec[0]))
reqRow = getXML.fetchone()

while reqRow:
        oneRow = reqRow
        headers = {'username': oneRow[2],
                    'password': oneRow[3],
                    'languageCode': oneRow[8]}
        if oneRow[4]=='GET':
            response = requests.get(url = oneRow[5],headers = headers)
        else:
            response = requests.post(url = oneRow[5], data = oneRow[0].encode('utf-8'),headers = headers)
        print(response.content)
        reqRow = getXML.fetchone()

if response is not None:
        setRes = cnxn.cursor()
        
        sql = "EXEC Handle_Response @ID = "+str(toExec[0])+", @RESPONSE ='"+str(response.content.decode("utf-8"))+ "'"
        
        if oneRow[0] == None:
            sql = sql + ", @Request = NULL"
        else:
            sql = sql + ", @Request ='"+oneRow[0]+"'"
        
        sql = sql + ", @Code='"+oneRow[4]+"', @ID = "+str(oneRow[1])
        setRes.execute(sql)
        setRes.close()
        setRes.commit()

        
