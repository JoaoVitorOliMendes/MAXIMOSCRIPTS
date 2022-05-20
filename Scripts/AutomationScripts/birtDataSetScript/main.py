import pymssql

conn = pymssql.connect('maximocon.asuscomm.com:31433','maximo','maximocon','maxdb761EN')
cursor = conn.cursor(as_dict=True)

result = ''

query = input('Type your query: ')
arrayQ = query.lower().replace('"', '').split(' ')
if arrayQ[0] == 'select':
    arrayQ.pop(0)
    index = arrayQ.index('from')
    attributes = ''.join(arrayQ[0:index]).split(',')
    table = arrayQ[index+1]

    for i in attributes:
        i = i.replace(',','')
        i = i.replace(table + '.', '')
        executeQ = str(f"select top 1 maxtype from maxattribute where objectname = '{table}' and attributename = '{i}'")
        cursor.execute(executeQ)
        row = cursor.fetchone()
        if row:
            if row['maxtype'] in ('ALN', 'CLOB', 'GL', 'LONGALN', 'LOWER', 'UPPER'):
                result = result + str(f"\nrow['{i}'] = maximoDataSet.getString('{i}');")
            elif row['maxtype'] in ('YORN'):
                result = result + str(f"\nrow['{i}'] = maximoDataSet.getBooleanString('{i}');")
            elif row['maxtype'] in ('DATETIME', 'TIME'):
                result = result + str(f"\nrow['{i}'] = maximoDataSet.getTimestamp('{i}');")
            elif row['maxtype'] in ('DATE'):
                result = result + str(f"\nrow['{i}'] = maximoDataSet.getDate('{i}');")
            elif row['maxtype'] in ('AMOUNT', 'DECIMAL'):
                result = result + str(f"\nrow['{i}'] = maximoDataSet.getDouble('{i}');")
            elif row['maxtype'] in ('FLOAT'):
                result = result + str(f"\nrow['{i}'] = maximoDataSet.getFloat('{i}');")
            elif row['maxtype'] in ('DURATION'):
                result = result + str(f"\nrow['{i}'] = maximoDataSet.getDuration('{i}');")
            elif row['maxtype'] in ('SMALLINT', 'INTEGER'):
                result = result + str(f"\nrow['{i}'] = maximoDataSet.getInteger('{i}');")
print('\nResult: ' + result)
conn.close()
