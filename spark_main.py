from App.src.Dehoop import Dehoop
from App.src.ParamStruct import ParamOutLineWork,ParamDDLContent
from App.src.Table import replaceKeyWords,replaceKeyWords_spark
        
import tqdm 
if __name__ == '__main__':
    
    u = 'liub'
    passwd = 'hbbx@2024SxdC'

    d = Dehoop("10.1.8.17",30104)
    # d.Login(u,passwd)
    d.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkZWhvb3B1c2VyaWQiOiI2NTcyNTM5NTk3NjQ4MDM1ODQiLCJ0ZW5hbnRpZCI6IjY1NjYwOTExODM5OTc1ODMzNiIsImV4cCI6MTc0MDM4NDcwNywiaWF0IjoxNzQwMTI1NTA3fQ.JzmbO1bMUZfOGCNapJQBQO3kmSk90pSXUY5r4SqipZYK2Q6M_yIOKLlG_v3W7ddj80e2ZVM3yB5NMRQEP4gAFg"
    d.tenantid = '656609118399758336'
    projectName = '财务域模型开发'
    
    parentid = '681794474774364160'
    workspaceId = '656613585694228480'
    
    
    import pandas as pd 

    df= pd.read_excel("C:/Xiaomi Cloud/Desktop/FV-1.xlsx").fillna('')
    type = 'STG'
    system = 'HBCORE'
    for i in tqdm.tqdm(range(len(df)),desc="建表中...",total=len(df),colour="green"):
        name = df.iloc[i, 0]
        descr = df.iloc[i, 1]

        TABLENAME = name
        DESCR = descr
        
        script = d.GenerateDDLScript(projectName,"661617050451443712","660489358226227200",system+"."+TABLENAME)
    
        
        match type:
            case 'spark':
                INPARAM = TABLENAME
                p = ParamOutLineWork(parentId=parentid,name="ODS_"+system+"_"+INPARAM+"_ONYARN",descr=DESCR,workspaceId=workspaceId,type="SparkSQL",director = d.tenantid)
            case 'ODS':
                INPARAM = 'ODS_'+system+'_' + TABLENAME
                p = ParamOutLineWork(parentId=parentid,name = INPARAM,descr=DESCR,workspaceId=workspaceId,director = d.tenantid)
            case 'STG':
                INPARAM = 'STG_'+system+'_' + TABLENAME
                p = ParamOutLineWork(parentId=parentid,name = INPARAM,descr=DESCR,workspaceId=workspaceId,director = d.tenantid)
        
        id = d.CreateDDLWork(projectName,p)
  
        if type == 'spark':
            script = replaceKeyWords_spark(INPARAM)
        elif type == 'STG':
            script = replaceKeyWords(INPARAM,script,DESCR,False)
        else:
            script = replaceKeyWords(INPARAM,script,DESCR,True)
        
        if id is not None:
            
            with open("./log_id.txt","a",encoding="utf-8") as f:
                f.write(id+"\n")
                
            try:
                p2 = ParamDDLContent(id= id ,workScript=script)
                d.UpdateDDLWork(projectName,p2)
                if type != 'spark':
                    d.ExuteDDLWork(projectName,p2)
            except:
                d.DeleteWorkById(projectName,id)
    