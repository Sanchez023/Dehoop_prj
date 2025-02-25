from App.src.Dehoop import Dehoop
from App.src.ParamStruct import ParamOutLineWork,ParamDDLContent
from App.src.Table import ReplaceKeyWords,ReplaceKeyWords_spark
from App.src.TransFormer import Transerfrom_addColumn,Transerfrom_mappingList,ExtraColumn,ReMappingList

import tqdm 
if __name__ == '__main__':
    
    u = ''
    passwd = ''

    d = Dehoop("10.1.8.17",30104)
    # d.Login(u,passwd)
    d.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkZWhvb3B1c2VyaWQiOiI2NTcyNTM5NTk3NjQ4MDM1ODQiLCJ0ZW5hbnRpZCI6IjY1NjYwOTExODM5OTc1ODMzNiIsImV4cCI6MTc0MDM4NDcwNywiaWF0IjoxNzQwMTI1NTA3fQ.JzmbO1bMUZfOGCNapJQBQO3kmSk90pSXUY5r4SqipZYK2Q6M_yIOKLlG_v3W7ddj80e2ZVM3yB5NMRQEP4gAFg"
    d.userId = '657253959764803584'
    d.tenantid = '656609118399758336'
    projectName = '业务流程域模型开发'
    
    parentid = '681804602156253184'
    workspaceId = '656613585694228480'
    fromDbId = "661617050451443712"
    toDbId = "660489358226227200"
    
    
    import pandas as pd

    df= pd.read_excel("C:/Xiaomi Cloud/Desktop/BFO-2.xlsx").fillna('')
    type = 'ODS'
    system = 'HBCORE'
    for i in tqdm.tqdm(range(len(df)),desc="建表中...",total=len(df),colour="green"):
        name = df.iloc[i, 0]
        descr = df.iloc[i, 1]

        TABLENAME = name
        DESCR = descr
        
        script = d.GenerateDDLScript(projectName,fromDbId,toDbId,system+"."+TABLENAME)
    
        
        match type:
            case 'spark':
                INPARAM = TABLENAME
                p = ParamOutLineWork(parentId=parentid,name="ODS_"+system+"_"+INPARAM+"_ONYARN",descr=DESCR,workspaceId=workspaceId,type="SparkSQL",director = d.userId)
            case 'ODS':
                INPARAM = 'ODS_'+system+'_' + TABLENAME
                p = ParamOutLineWork(parentId=parentid,name = INPARAM,descr=DESCR,workspaceId=workspaceId,director = d.userId)
            case 'STG':
                INPARAM = 'STG_'+system+'_' + TABLENAME
                p = ParamOutLineWork(parentId=parentid,name = INPARAM,descr=DESCR,workspaceId=workspaceId,director = d.userId)
            case 'SYNC':
                INPARAM = 'STG_'+system+'.' + TABLENAME+"_F_1_10"
                p = ParamOutLineWork(parentId=parentid,name = INPARAM,descr=DESCR,workspaceId=workspaceId,director = d.userId,type = "SYNC")
                
        id = d.CreateDDLWork(projectName,p)
  
        if type == 'spark':
            script = ReplaceKeyWords_spark(INPARAM)
        elif type == 'STG':
            script = ReplaceKeyWords(INPARAM,script,DESCR,False)
        elif type == "ODS":
            script = ReplaceKeyWords(INPARAM,script,DESCR,True)
        # elif type == "SYNC":
            
        
        if id is not None:
            try:  
                with open("./log_id.txt","a",encoding="utf-8") as f:
                    f.write(id+"\n")
                
          
                # 同步作业保存
                if type == "SYNC":
            
                    toTableName = TABLENAME
                    fromTableName = system+"."+TABLENAME
                
                    column_list:list[dict]= d.GetColumnInfos(projectName,toDbId,toTableName,"dist")
                    column_list_src:list[dict] = d.GetColumnInfos(projectName,fromDbId,fromTableName,"src")
                    mappingList = Transerfrom_mappingList(column_list,fromTableName,toTableName)

                    field,uuid,new_column = ExtraColumn("etl_timestamp",fromTableName,"localtimestamp")
                    mappingList = ReMappingList(mappingList,field,uuid)

                    addColumnList = Transerfrom_addColumn(column_list_src,fromTableName)
                    addColumnList.append(new_column)

                    d.SaveOrUpdateSyncWork(projectName,id,fromDbId,fromTableName,toDbId,toTableName,mappingList,addColumnList)

                    continue
        
                
            
                p2 = ParamDDLContent(id= id ,workScript=script)
                d.UpdateDDLWork(projectName,p2)
                if type == 'ODS' or type == "STG":
                    d.ExuteDDLWork(projectName,p2)
            except:
                d.DeleteWorkById(projectName,id)
    
    
