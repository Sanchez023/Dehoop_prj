from App.src.Dehoop import Dehoop
from App.src.ParamStruct import ParamOutLineWork,ParamDDLContent
from App.src.Table import replaceKeyWords,replaceKeyWords_spark
        
import tqdm 
if __name__ == '__main__':
    
    u = 'liub'
    passwd = 'hbbx@2024SxdC'

    d = Dehoop("10.1.8.17",30104)
    d.Login(u,passwd)
    # d.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkZWhvb3B1c2VyaWQiOiI2NTcyNTM5NTk3NjQ4MDM1ODQiLCJ0ZW5hbnRpZCI6IjY1NjYwOTExODM5OTc1ODMzNiIsImV4cCI6MTczOTQxMDcxNSwiaWF0IjoxNzM5MTUxNTE1fQ.OJaGWijPieXeI6j4b4a5Ap5wmsXcdpy9xeb_wEFzOWXy6KS3cunxNhTly0oVStMT0Hmxb5jFAsmwIPzCD9Y8tw"
    # d.tenantid = '656609118399758336'
    projectName = '销管域模型开发'
    
    parentid = '677525792447528960'
    workspaceId = '656613585694228480'
    
    

  
    d.DeleteWorkById(projectName,'677200708939808768')
    