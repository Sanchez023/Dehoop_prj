from datetime import datetime
from App.src.Db import MySQLConnector
from App.src.Table import replaceKeyWords_sparkv2

import re

priority_level = {8:"createtime",7:"startdate",6:"starttime",5:"createdate",4:"QUOTATIONNO",3:"policyno",2:"proposalno",1:"endorno",0:""}


conn = MySQLConnector("root","leo130","localhost",'hbbx')
script_tables = "select tableName from tablesparkscript where status = 0;"
res_tables = conn.execute_sql(script_tables)
for table in res_tables:
    tableName = table[0]
    # tableName = "GUPOLICYMAIN"
    script_join = f"SELECT columnName from odstableinfo where tableName = '{tableName}' and pk_constraint is not null;"
    res_join = conn.execute_sql(script_join)
    script_partition = f'''select columnName from odstableinfo o where tableName  = '{tableName}' and columnName in ('Startdate','starttime','createtime','createDate') 
    union select columnName from odstableinfo where pk_constraint is not null and tableName = '{tableName}';'''
    res_parition = conn.execute_sql(script_partition)

    ds = ""
    temp = 0
    for p in res_parition:
        parition = str(p[0]).lower()
        
        for key,value in priority_level.items():
              
            if parition == value:
                temp =  max(key,temp)
                
        
    ds = priority_level[temp]
    if ds == "":
        continue

    if bool(re.search(r"policyno",ds)) or bool(re.search(r'endorno',ds)) or bool(re.search(r'proposalno',ds)):
        ds = f"substring({ds},12,4)"
        
    if bool(re.search(r'time',ds)) or bool(re.search(r'date',ds)):
        ds = f'substring({ds},1,7)'
    
    


    print(ds)
    join_condition = []
    linkColumn = ""
    for i in res_join:
        str_ods  = "ODS."+str(i[0])
        str_stg = "STG."+str(i[0])
        
        join_condition.append("=".join([str_ods,str_stg]))
        linkColumn = " AND ".join(join_condition)
    script = replaceKeyWords_sparkv2(tableName,ds,linkColumn)
    conn.execute_sql_WithouReturn(f"update tablesparkscript  set script = '{script}',status = 1,updatetime = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' where tableName = '{tableName}';")



