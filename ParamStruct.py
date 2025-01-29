import json
class BaseStruct:
    '''参数结构体\n
    该类用于定义接口请求的参数结构体
    '''
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

    
class ParamDDLWork(BaseStruct):
    '''DDL工作参数结构体\n
    该类用于定义DDL工作的参数结构体\n
    
    参数:
        parentId:   父作业ID
        name:       作业名称
        flowId:     流程ID
        director:   负责人
        descr:      描述
        workspaceId:工作空间ID
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id', '')
        self.parentId = kwargs.get('parentId')
        self.name = kwargs.get('name')
        self.flowId = kwargs.get('flowId')
        self.type = kwargs.get('type','DDL')
        self.director = kwargs.get('director')
        self.descr = kwargs.get('descr')
        self.workspaceId = kwargs.get('workspaceId')
    