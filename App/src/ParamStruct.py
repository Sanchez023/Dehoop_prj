import json
from uuid import uuid4

class BaseStruct:
    """参数结构体\n
    该类用于定义接口请求的参数结构体
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.__dict__)


class ParamOutLineWork(BaseStruct):
    """DDL工作参数结构体\n
    该类用于定义DDL工作的参数结构体\n

    参数:
        parentId:   父作业ID
        name:       作业名称
        type:       作业类型
        flowId:     流程ID
        director:   负责人
        descr:      描述
        workspaceId:工作空间ID
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id", "")
        self.workId = kwargs.get("workId", "")
        self.parentId = kwargs.get("parentId")
        self.name = kwargs.get("name")
        self.flowId = kwargs.get("flowId")
        self.type = kwargs.get("type", "DDL")
        self.director = kwargs.get("director")
        self.descr = kwargs.get("descr")
        self.workspaceId = kwargs.get("workspaceId")


class ParamDDLContent(BaseStruct):
    """DDl内容参数结构体\n
    该类用于存放DDL语句等内容

    参数:
    id:         作业id,
    excuteId:   执行id
    workScript: SQL语句
    keyWords:   传入SQL的关键字,
    remain:     false
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        default_keywords = [
            "DROP",
            "TABLE",
            "IF",
            "CREATE",
            "LANGUAGE",
            "TIMESTAMP",
            "ROW",
            "BY",
            "AS",
        ]
        self.id = kwargs.get("id")
        self.workId = kwargs.get("workId",self.id)
        self.executeId = kwargs.get("executeId",uuid4().hex)
        self.workScript = kwargs.get("workScript")
        self.keywords = kwargs.get("keyWords", default_keywords)
        self.remain = kwargs.get("remain", False)
        self.script = self.workScript


class paramFlink(BaseStruct):
    '''
    {
    "fromDbId": "643763299611049984",
    "toDbId": "643766294172139520",
    "schema": null,
    "tableName": "GCMAXDEALERCODE"
}'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.fromDbId = kwargs.get("fromDbId")
        self.toDbId = kwargs.get("toDbId", False)
        self.tableName = kwargs.get("tableName", False)
        self.schema = None   


class paramDBInfo(BaseStruct):
       def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.envId = kwargs.get("envId")
        self.type = kwargs.get("type", False)
        self.isInnerType = kwargs.get("isInnerType",False)
