import json

with open("./json.json",'r',encoding='utf-8') as f:
    dict_json = json.load(f)

dict_works = {}
dict_child = {}
dict_parent = {}
def FindChild(child_work:list,parent:str):
    for work in child_work:
        if work['type'] == 'DIR':
            
            dict_child[work['id']] = []
            dict_works[work['id']] = work['name']
            
            dict_child[parent].append(work['id'])

        if work['child']:
            FindChild(work['child'],work['id'])

def FindChildV2(child_work:list,parent:str,topid:str):
    for work in child_work:
        if work['type'] == 'DIR':
            dict_works[work['id']] = "/".join([dict_works[parent],work['name']])
            dict_parent[work['id']] = topid
        if work['child']:
            FindChildV2(work['child'],work['id'],topid)
    
# for work in dict_json['data']:
#     dict_works[work['id']] = work['name']
    
#     if work['child']:
        
#         dict_child[work['id']] = []
#         dict_works[work['id']] = work['name']
#         print(work['child'],work['id'])
#         FindChild(work['child'],work['id'])
    
    
for work in dict_json['data']:
    dict_works[work['id']] = work['name']
    
    if work['child']:

        dict_child[work['id']] = []
        dict_works[work['id']] = work['name']
        dict_parent[work['id']] = work['id']
        FindChildV2(work['child'],work['id'],work['id'])
            
print("-"*50)        
print(dict_works)
print(dict_works.__len__())
print(dict_parent.__len__())
print(dict_parent)
# print(dict_child)
# print(dict_work)

