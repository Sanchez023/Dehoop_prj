from App.src.Dehoop import Dehoop
from App.src.ParamStruct import ParamDDLWork,ParamDDLContent
from App.src.Table import replaceKeyWords
        
import tqdm 
if __name__ == '__main__':
    # u = 'hbbxlb'
    # passwd = 'hbbx@2024'

    # d = Dehoop("192.168.16.100",30104)
    # d.token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkZWhvb3B1c2VyaWQiOiI2NDM3NDExNDYwNDgxMDI0MDAiLCJ0ZW5hbnRpZCI6IjY0MjQxNzI4MzAxMTk2OTAyNCIsImV4cCI6MTczOTAwNDI2MCwiaWF0IjoxNzM4NzQ1MDYwfQ.uJoSDqweut1CqzPRdUBSvULqjrCjcr3XY7L9PtFhmaZhW19G9m0Uvm7JZgx_76JNmBiC73u1zArzcQsBZ5x7gw'
    # d.tenantid = '642417283011969024'
    
    # projectName = '恒邦POT'
    # p = ParamDDLWork(parentId='649607927102963712',name='ods_hbcore_gupolicymain',descr='接口测试',workspaceId='642666109299851264')
    # # Script = 'DROP TABLE IF EXISTS POLICYMAIN'
    
    # # with open("./DDL.sql","r",encoding="utf-8") as f:
    # #     Script = f.read()

    # d.Login('hbbxlb','hbbx@2024')
    
    # script = d.GenerateDDLScript('恒邦POT',"643763299611049984","643766294172139520",'GGPRODUCTATTR')
   
    # id = d.CreateDDLWork(projectName,p)
    # script = replaceKeyWords(p.name,script,'接口测试')
    
    # if id is not None:
    #     try:
    #         p2 = ParamDDLContent(id= id ,workScript=script)
    #         d.UpdateDDLWork(projectName,p2)
    #         d.ExuteDDLWork(projectName,p2)
    #     except:
    #         d.DeleteWorkById(projectName,id)
    
    u = 'liub'
    passwd = 'hbbx@2024SxdC'

    d = Dehoop("10.1.8.17",30104)
    d.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkZWhvb3B1c2VyaWQiOiI2NTcyNTM5NTk3NjQ4MDM1ODQiLCJ0ZW5hbnRpZCI6IjY1NjYwOTExODM5OTc1ODMzNiIsImV4cCI6MTczOTA4NTQ2NCwiaWF0IjoxNzM4ODI2MjY0fQ.mGxpr7t0oj-TltddIZiJ8o4b-rA2zcO5jrpTyd-T6yhlWtsLb5sVkjFZYt4CF617o0j9HmDvDS7u0pUTlBBxTg"
    d.tenantid = '656609118399758336'
    projectName = '保单域模型开发'
    
    parentid = '660506747688976384'
    workspaceId = '656613585694228480'
    
    
    import pandas as pd 

    df= pd.read_excel("C:/Xiaomi Cloud/Desktop/1.xlsx").fillna('')

    for i in tqdm.tqdm(range(len(df)),desc="建表中...",total=len(df)):
        name = df.iloc[i, 0]
        descr = df.iloc[i,1]

    
        
        
        
        TABLENAME = name
        DESCR = descr
        script = d.GenerateDDLScript(projectName,"661617050451443712","660489358226227200","HBCORE."+TABLENAME)
        # stg 切换为STG_HBCORE_
        INPARAM = 'STG_HBCORE_' + TABLENAME
        p = ParamDDLWork(parentId=parentid,name=INPARAM,descr=DESCR,workspaceId=workspaceId)
        id = d.CreateDDLWork(projectName,p)
        
        # stg 切换为False
        script = replaceKeyWords(p.name,script,DESCR,False)
        
        if id is not None:
            try:
                p2 = ParamDDLContent(id= id ,workScript=script)
                d.UpdateDDLWork(projectName,p2)
                d.ExuteDDLWork(projectName,p2)
            except:
                d.DeleteWorkById(projectName,id)