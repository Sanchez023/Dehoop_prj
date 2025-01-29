from Dehoop import Dehoop
from ParamStruct import ParamDDLWork         
        

if __name__ == '__main__':
    # u = 'hbbxlb'
    # passwd = 'hbbx@2024'

    d = Dehoop("192.168.16.100",30104)
    d.token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkZWhvb3B1c2VyaWQiOiI2NDM3NDExNDYwNDgxMDI0MDAiLCJ0ZW5hbnRpZCI6IjY0MjQxNzI4MzAxMTk2OTAyNCIsImV4cCI6MTczODMzMDA5MiwiaWF0IjoxNzM4MDcwODkyfQ.Q0LPyTTZZIjlCnfTWhprfLk-OpVzLmfi4OUyxC2myaUzR77a9xPQAUrm-XQAPQlzOn0m4p5RmkM0KfgTlvq-yA'
    d.tenantid = '642417283011969024'
    
    
    p = ParamDDLWork(parentId='649607927102963712',name='生产DDL作业',descr='接口测试',workspaceId='642666109299851264')
    # d.Login('hbbxlb','hbbx@2024')
    d.CreateDDLWork('恒邦POT',p)