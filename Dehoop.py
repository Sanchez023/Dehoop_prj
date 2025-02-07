
from log import logger
import socket
from Module import LoginModule,PublicConfig,DataDevelopment
from ParamStruct import ParamDDLWork,ParamDDLContent
from time import sleep
class Root:
    '''网络根信息类\n
    用于维护对应的网络地址信息和端口信息，提供了一个端口测试的方法
    
    属性:
    ip:             接口对应的IP
    url:            接口对应的网络地址 
    s_url:          接口对应的SSL安全协议网络地址
    resquest_url:   接口访问地址
    resquest_s_url: 接口访问SSL协议地址
    port:           接口对应的端口  
    '''
    def __init__(self,ip:str,port:int|str):
        self.ip = ip
        self.url = f"http://{ip}"
        self.s_url = f"https://{ip}"
        self.request_url = ":".join([self.url,str(port)])
        self.request_s_url = ":".join([self.s_url,str(port)])
        self.port = int(port)
        
    def test_connect(self,)->bool:
        '''
        调用socket套接字来实现对端口的访问,返回结果为布尔型。
        ''' 
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        r = s.connect_ex(self.url,self.port)
        if r == 0:
            return True
        else:
            return False
    
class Dehoop(Root):
    '''得帆平台对象类\n
    在该类下以接口的方式实现了对得帆部分模块的基础操作
    '''
    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.token = None
        self.tenantid = None
        self.projects = None    

        self.c_workspaces = None
        self.c_prjdir =  None
        self.c_nodeMatch = None
        
        self.running_excuteId = {}
        
    def Login(self,username:str,passwd:str):
        '''执行登入'''
        result = LoginModule(self.request_url).login(username,passwd)
        if result is not None:
            self.token,self.tenantid = result
            if self.token is not None or self.tenantid is not None:
                logger.info("登入成功")
                logger.info(f'token:{self.token}')
                logger.info(f'tenantid:{self.tenantid}')
        else:
            logger.error("登入失败")
            return None
    
    def QueryProject(self):
        '''查询项目'''
       
        if self.token is not None:
            self.projects =  PublicConfig(self.request_url).QueryProject(self.token,self.tenantid)
            if self.projects is not None:
                logger.info("查询项目成功")
                
        else:
            logger.error("未获取到token,请先登入")
            return None

    def QueryWorkSpace(self,projectName:str):
        '''查询工作空间'''
       
        if self.projects is None:
            logger.warning("未获取到项目信息，正在获取项目")
            self.QueryProject()
            envid:str = self.projects[projectName][1]
            
            result =  PublicConfig(self.request_url).QueryWorkspace(self.token,envid)
            if result is not None:
                self.c_workspaces = result
            if self.c_workspaces is not None:
                logger.info("查询工作空间成功")
                logger.info(f"工作空间信息：{self.c_workspaces}")
        else:
            logger.error("查询工作空间失败")
            return None
        
    def QueryOutLineWorks(self,projectName:str):
        '''查询离线作业\n
        参数:
            projectName: 项目名称
        '''
       
        if self.projects is None:
            logger.warning("未获取到项目信息，正在获取项目")
            self.QueryProject()
            projectid:str = self.projects[projectName][0]
            envid:str = self.projects[projectName][1]
            self.c_prjdir,self.c_nodeMatch = DataDevelopment(self.request_url).QueryOutLineWork(self.token,self.tenantid,projectid,envid)
            
            if self.c_prjdir is not None:
                logger.info("查询离线作业成功")
                # logger.info(f"离线作业信息：{self.c_prjdir}")
        else:
            logger.error("查询离线作业失败")
            return None
        
    def CreateDDLWork(self,projectName:str,param:ParamDDLWork):
        '''创建DDL作业\n
        参数:
        projectName: 项目名称
        param:       DDL作业参数
        '''
       
        if self.c_prjdir is None:
            logger.warning("未获取到项目目录信息，正在获取项目目录")
            self.QueryOutLineWorks(projectName)
        projectid:str = self.projects[projectName][0]
        param.director = self.tenantid
        param.flowId = self.c_nodeMatch[param.parentId]
        id = DataDevelopment(self.request_url).CreateDDLWork(self.token,projectid,self.tenantid,param)
        if id is not None:
            logger.info("创建DDL作业成功")
            logger.info(f"DDL作业ID:{id}")
            return id
        else:
            logger.error(f"请检查当前作业名称是否重复'{param.name}'")
            return None
        
    def UpdateDDLWork(self,projectName:str,param:ParamDDLContent):
        '''保存更新DDL作业
        
        参数：
        projectName: 项目名称
        param:       DDL内容参数
        '''
       
        if self.c_prjdir is None:
            logger.warning("未获取到项目目录信息，正在获取项目目录")
            self.QueryOutLineWorks(projectName)
        projectid:str = self.projects[projectName][0]
        result = DataDevelopment(self.request_url).SaveOrUpdateDDLWork(self.token,projectid,self.tenantid,param)
        if result == None:
            raise Exception("创建失败")
    
    def DeleteWorkById(self,projectName,id):
       
        if self.c_prjdir is None:
            logger.warning("未获取到项目目录信息，正在获取项目目录")
            self.QueryOutLineWorks(projectName)
        projectid:str = self.projects[projectName][0]
        res = DataDevelopment(self.request_url).DeleteDDLWork(self.token,projectid,self.tenantid,id)
        if res:   
            logger.info(f"删除'{id}'作业成功！")
        else:
            logger.warning(f"删除'{id}'作业失败！")
            
    
    def ExuteDDLWork(self,projectName,param:ParamDDLWork):
        if self.c_prjdir is None:
            logger.warning("未获取到项目目录信息，正在获取项目目录")
            self.QueryOutLineWorks(projectName)
        projectid:str = self.projects[projectName][0]
        if DataDevelopment(self.request_url).ExcuteTestParams(self.token,projectid,self.tenantid,param):
            excuteid = DataDevelopment(self.request_url).ExcuteWork(self.token,projectid,self.tenantid,param)
            if excuteid:
                self.running_excuteId[excuteid] = ""
                logger.info(f"作业:{param.name},执行成功!")
                
        logger.warning(f"作业：'{param.name}',执行失败！")