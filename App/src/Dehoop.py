from App.src.log import logger
import socket
from App.src.Module import LoginModule, PublicConfig, DataDevelopment
from App.src.ParamStruct import (
    ParamOutLineWork,
    ParamDDLContent,
    ParamFlink,
    ParamDBInfo,
    ParamColumnGet,
    ParamSyncJob,
)
from App.src.Table import DDLStruct, GetColumns, replaceKeyWords_spark, replaceKeyWords
from typing import Literal
import json


class Root:
    """网络根信息类\n
    用于维护对应的网络地址信息和端口信息，提供了一个端口测试的方法

    属性:
    ip:             接口对应的IP
    url:            接口对应的网络地址
    s_url:          接口对应的SSL安全协议网络地址
    resquest_url:   接口访问地址
    resquest_s_url: 接口访问SSL协议地址
    port:           接口对应的端口
    """

    def __init__(self, ip: str, port: int | str):
        self.ip = ip
        self.url = f"http://{ip}"
        self.s_url = f"https://{ip}"
        self.request_url = ":".join([self.url, str(port)])
        self.request_s_url = ":".join([self.s_url, str(port)])
        self.port = int(port)

    def test_connect(
        self,
    ) -> bool:
        """
        调用socket套接字来实现对端口的访问,返回结果为布尔型。
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:

            r = s.connect_ex((self.ip, self.port))
            s.close()
        except:
            s.close()
            return False
        if r == 0:
            return True
        else:
            return False


class Dehoop(Root):
    """得帆平台对象类\n
    在该类下以接口的方式实现了对得帆部分模块的基础操作
    """

    def __init__(self, ip, port) -> bool:
        super().__init__(ip, port)
        self.token = None
        self.tenantid = None
        self.userId = None
        self.projects = None

        self.c_workspaces = None
        self.c_prjdir = None
        self.c_nodeMatch = None
        self.c_dbsType = None
        self.c_dbids = None

        self.running_executeId = {}

    def Login(self, username: str, passwd: str):
        """执行登入"""
        result = LoginModule(self.request_url).login(username, passwd)
        if result is not None:
            self.token, self.tenantid, self.userId = result
            if self.token is not None or self.tenantid is not None:
                logger.info("登入成功")
                logger.info(f"token:{self.token}")
                logger.info(f"tenantid:{self.tenantid}")
            return True
        else:
            logger.error("登入失败")
            return False

    def QueryProject(self):
        """查询项目\n
        返回参数：
        项目ID和环境ID的字典"""

        if self.token is not None:
            self.projects = PublicConfig(self.request_url).QueryProject(
                self.token, self.tenantid
            )
            if self.projects is not None:
                logger.info("查询项目成功")
                return self.projects

        else:
            logger.error("未获取到token,请先登入")
            return None

    def QueryWorkSpace(self, projectName: str):
        """查询工作空间"""

        if self.projects is None:
            logger.warning("未获取到项目信息，正在获取项目")
            self.QueryProject()
            envid: str = self.projects[projectName][1]

            result = PublicConfig(self.request_url).QueryWorkspace(self.token, envid)
            if result is not None:
                self.c_workspaces = result
                logger.info("查询工作空间成功")
                logger.info(f"工作空间信息：{self.c_workspaces}")
                return result
        else:
            logger.error("查询工作空间失败")
            return None

    def QueryOutLineWorks(self, projectName: str):
        """查询离线作业\n
        参数:
            projectName: 项目名称
        """

        if self.projects is None:
            logger.warning("未获取到项目信息，正在获取项目")
            self.QueryProject()
            projectid: str = self.projects[projectName][0]
            envid: str = self.projects[projectName][1]
            self.c_prjdir, self.c_nodeMatch = DataDevelopment(
                self.request_url
            ).QueryOutLineWork(self.token, self.tenantid, projectid, envid)

            if self.c_prjdir is not None:
                logger.info("查询离线作业成功")
                # logger.info(f"离线作业信息：{self.c_prjdir}")
        else:
            logger.error("查询离线作业失败")
            return None

    def CreateDDLWork(self, projectName: str, param: ParamOutLineWork):
        """创建DDL作业\n
        参数:
        projectName: 项目名称
        param:       DDL作业参数
        """

        if self.c_prjdir is None:
            logger.warning("未获取到项目目录信息，正在获取项目目录")
            self.QueryOutLineWorks(projectName)
        projectid: str = self.projects[projectName][0]
        param.director = self.tenantid
        param.flowId = self.c_nodeMatch[param.parentId]
        id = DataDevelopment(self.request_url).CreateDDLWork(
            self.token, projectid, self.tenantid, param
        )
        if id is not None:
            logger.info("创建DDL作业成功")
            logger.info(f"DDL作业ID:{id}")
            return id
        else:
            logger.error(f"请检查当前作业名称是否重复'{param.name}'")
            return None

    def UpdateDDLWork(self, projectName: str, param: ParamDDLContent):
        """保存更新DDL作业

        参数：
        projectName: 项目名称
        param:       DDL内容参数
        """

        if self.c_prjdir is None:
            logger.warning("未获取到项目目录信息，正在获取项目目录")
            self.QueryOutLineWorks(projectName)
        projectid: str = self.projects[projectName][0]
        result = DataDevelopment(self.request_url).SaveOrUpdateDDLWork(
            self.token, projectid, self.tenantid, param
        )
        if result == None:
            raise Exception("创建失败")

    def DeleteWorkById(self, projectName, id):

        if self.c_prjdir is None:
            logger.warning("未获取到项目目录信息，正在获取项目目录")
            self.QueryOutLineWorks(projectName)
        projectid: str = self.projects[projectName][0]
        res = DataDevelopment(self.request_url).DeleteDDLWork(
            self.token, projectid, self.tenantid, id
        )
        if res:
            logger.info(f"删除'{id}'作业成功！")
        else:
            logger.warning(f"删除'{id}'作业失败！")

    def ExuteDDLWork(self, projectName, param: ParamOutLineWork):
        """执行DDL作业\n

        参数：
        projectName: 项目名称
        para:         DDL作业参数
        """
        if self.c_prjdir is None:
            logger.warning("未获取到项目目录信息，正在获取项目目录")
            self.QueryOutLineWorks(projectName)
        projectid: str = self.projects[projectName][0]
        if DataDevelopment(self.request_url).ExecuteTestParams(
            self.token, projectid, self.tenantid, param
        ):
            executeid = DataDevelopment(self.request_url).ExecuteWork(
                self.token, projectid, self.tenantid, param
            )
            if executeid:
                self.running_executeId[executeid] = ""
                logger.info(f"作业:{param.id},执行成功!")
            else:
                logger.warning(f"作业：'{param.id}',执行失败！")

    def CreateDDLWorkBatch(
        self, projectName: str, params: list[ParamOutLineWork], ddls: list[DDLStruct]
    ):
        for p, d in zip(params, ddls):
            id = self.CreateDDLWork(projectName, p)
            script = d.ToScript()
            if id is not None:
                try:
                    p2 = ParamDDLContent(id=id, workScript=script)
                    self.UpdateDDLWork(projectName, p2)
                    self.ExecuteDDLWork(projectName, p2)
                except:
                    self.DeleteWorkById(projectName, id)
                    continue

    def CreateOutlineWorkBatch(
        self,
        projectName: str,
        parentid: str,
        workspaceId,
        df: list,
        type: Literal["ODS", "STG", "SPARK", "DDL"],
        fromdb: str,
        todb: str = None,
    ):
        "批量创建作业"

        for i in range(len(df)):
            name = df.iloc[i, 0]
            descr = df.iloc[i, 1]

            TABLENAME = name
            DESCR = descr
            script = self.GenerateDDLScript(
                projectName, fromdb, todb, "HBCORE." + TABLENAME
            )
            if script is None:
                continue

            match type:
                case "SPARK":
                    INPARAM = TABLENAME
                    p = ParamOutLineWork(
                        parentId=parentid,
                        name="ODS_HBCORE_" + INPARAM + "_ONYARN",
                        descr=DESCR,
                        workspaceId=workspaceId,
                        type="SparkSQL",
                        director=self.tenantid,
                    )
                case "ODS":
                    INPARAM = "ODS_HBCORE_" + TABLENAME
                    p = ParamOutLineWork(
                        parentId=parentid,
                        name=INPARAM,
                        descr=DESCR,
                        workspaceId=workspaceId,
                        director=self.tenantid,
                    )
                case "STG":
                    INPARAM = "STG_HBCORE_" + TABLENAME
                    p = ParamOutLineWork(
                        parentId=parentid,
                        name=INPARAM,
                        descr=DESCR,
                        workspaceId=workspaceId,
                        director=self.tenantid,
                    )

            id = self.CreateDDLWork(projectName, p)

            if type == "spark":
                script = replaceKeyWords_spark(INPARAM)
            elif type == "STG":
                script = replaceKeyWords(INPARAM, script, DESCR, False)
            else:
                script = replaceKeyWords(INPARAM, script, DESCR, True)

            if id is not None:

                with open("./log_id.txt", "a", encoding="utf-8") as f:
                    f.write(id + "\n")

                try:
                    p2 = ParamDDLContent(id=id, workScript=script)
                    self.UpdateDDLWork(projectName, p2)
                    if type != "spark":
                        self.ExecuteDDLWork(projectName, p2)
                except:
                    self.DeleteWorkById(projectName, id)

    def GenerateDDLScript(
        self, projectName: str, fromdb: str, todb: str, tableName: str
    ) -> str:
        if self.c_prjdir is None:
            logger.warning("未获取到项目目录信息，正在获取项目目录")
            self.QueryOutLineWorks(projectName)
        projectid: str = self.projects[projectName][0]
        param = ParamFlink(fromDbId=fromdb, toDbId=todb, tableName=tableName)
        res = DataDevelopment(self.request_url).GenerateDDL(
            self.token, projectid, self.tenantid, param
        )
        if res is None:
            return None
        return GetColumns(res)

    def GetResourceType(self, projectName):
        """获取数据库类型"""
        if self.c_prjdir is None:
            logger.warning("未获取到项目目录信息，正在获取项目目录")
            self.QueryOutLineWorks(projectName)
        projectid: str = self.projects[projectName][0]
        res = PublicConfig(self.request_url).GetResourceType(
            self.token, projectid, self.tenantid
        )
        if res is not None:
            self.c_dbsType = res
            return res
        else:
            return None

    def GetDBResourceId(self, projectName, type: str, isInnertype: bool = False):
        """获取数据来源ID"""
        if self.c_prjdir is None:
            logger.warning("未获取到项目目录信息，正在获取项目目录")
            self.QueryOutLineWorks(projectName)
        projectid: str = self.projects[projectName][0]
        envId = self.projects[projectName][1]

        param = ParamDBInfo(envId=envId, type=type, isInnerType=isInnertype)
        res = PublicConfig(self.request_url).GetDBResourceId(
            self.token, projectid, self.tenantid, param
        )
        if res is not None:
            self.c_dbids = res
            return res
        else:
            return None

    def GetColumnInfos(
        self,
        projectName: str,
        resourceId: str,
        tableName: str,
        type: Literal["src", "dist"],
    ) -> list:
        """获字段信息"""
        if self.projects is None:
            logger.warning("未获取到项目信息，正在获取项目")
            self.QueryProject()

        projectid: str = self.projects[projectName][0]
        param = ParamColumnGet(dbSourceId=resourceId, tableName=tableName, type=type)

        res = DataDevelopment(self.request_url).GetColumnInfo(
            self.token, projectid, self.tenantid, param
        )
        if res is not None:
            return res
        else:
            return None

    def SaveOrUpdateSyncWork(
        self,
        projectName: str,
        id: str,
        fromDbId: str,
        fromTableName: str,
        toDbId: str,
        toTableName: str,
        mappingList: list,
        addColumn: list,
        maxConCurrentNum: int=1,
        maxTransSpeed: int=10
    ):
        """保存更新离线同步作业"""
        
        if self.projects is None:
            logger.warning("未获取到项目信息，正在获取项目")
            self.QueryProject()

        projectid: str = self.projects[projectName][0]
        param = ParamSyncJob(
            id=id,
            fromDbId=fromDbId,
            fromTableName=fromTableName,
            toDbId=toDbId,
            toTableName=toTableName,
            addColumn=addColumn,
            mappingList=mappingList,
            maxConCurrentNum=maxConCurrentNum,
            maxTransSpeed=maxTransSpeed,
        )

        res = DataDevelopment(self.request_url).SaveOrUpdateSyncWork(
            self.token, projectid, self.tenantid, param
        )
        if res is not None:
            return res
        else:
            return None
