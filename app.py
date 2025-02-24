from flask import Flask,render_template,request,jsonify,session

from App.src.Dehoop import Dehoop
HOST = "127.0.0.1"
PORT = "3020"


app = Flask(__name__,template_folder='./App/templates')
app.secret_key = 'your_secret_key' 

@app.route("/",)
def index():
    return render_template("func.html")

@app.route("/back")
def back():
    return render_template("func.html",isinner=True)
@app.route("/outLineWork")
def outLineWork():
    return render_template("func.html",isinner=False)


# 登入
@app.route("/login",methods=['POST'])
def login():
    address = request.args.get("address",type=str)
    port = request.args.get("port",type=int)
    username = request.args.get('username',type=str,default=None)
    passwd = request.args.get('passwd',type=str,default=None)
    
    if username is None or passwd is None:
        return jsonify({'code':200,'message':'username or password is null!'})
    current_dehoop = Dehoop(address,port)
    if current_dehoop.Login(username,passwd):
        session['token'] = current_dehoop.token
        session['tenantid'] = current_dehoop.tenantid
        session['port'] = current_dehoop.port
        session['ip'] = current_dehoop.ip
        return jsonify({'code':200,'message':'success','token':current_dehoop.token,'tenantid':current_dehoop.tenantid})
    return jsonify({'code':401,'message':'error'})

# 获取项目ID
@app.route("/PublicConfig/GetProjects",methods=['GET'])
def GetProjects():
    d = GetDehoopFromSession()
    projects = d.QueryProject()
    if projects:
        return jsonify({'code':200,'message':'success','data':projects})
    return jsonify({'code':400,'message':'error'})

# 获取工作组ID
@app.route("/PublicConfig/GetWorkspaceId",methods=['GET'])
def GetWorkspaceIds():
    projectName = request.args.get("projectName")
    d = GetDehoopFromSession()
    data = d.QueryWorkSpace(projectName)
    if data:
        return jsonify({'code':200,'message':'success','data':data})
    return jsonify({'code':400,'message':'error'})

# 批量创建离线作业
@app.route("/Datadevlopment/Outlinework/createOutLineWorkInBatch",methods=['POST'])
def CreateoutlineWorkInBatch():
    import pandas as pd
    try:
        projectName = request.form.get('projectName')
    
        parentid = request.form.get("parentId")
        workspaceId= request.form.get("workspaceId")
        file = request.files.get("file")
        
        df= pd.read_excel(file.stream).fillna('')
        dtype= request.form.get('type')
        fromdb = request.form.get("fromdb")
        todb = request.form.get("todb")
        
        d = GetDehoopFromSession()
        d.CreateOutlineWorkBatch(projectName,parentid,workspaceId,df,dtype,fromdb,todb)
        return jsonify({'code':200,'message':'success','data':{"status":"finish"}}) 
    except Exception as e:
        return jsonify({'code':400,'message':str(e)})

# 获取数据库类型
@app.route("/PublicConfig/GetDbType",methods=['GET'])
def GetDbType():
    projectName = request.args.get('projectName',type=str)
    d = GetDehoopFromSession()
    types = d.GetResourceType(projectName)

    if types:
        return jsonify({'code':200,'message':'success','data':types})
    return jsonify({'code':400,'message':'error'})


# 获取资源ID
@app.route("/PublicConfig/GetResourceId",methods=['GET'])
def GetResourceId():
    projectName = request.args.get('projectName',type=str)
    type = request.args.get('type',type=str)
    isInner = request.args.get('isInnerType',type=int)
    bool_inner = True if isInner == 1 else False

    d = GetDehoopFromSession()
    res = d.GetDBResourceId(projectName,type,bool_inner)

    if res:
        return jsonify({'code':200,'message':'success','data':res})
    return jsonify({'code':400,'message':'error'})

def GetDehoopFromSession()->Dehoop:
    ip = session.get('ip')
    port = session.get('port')
    token = session.get('token')
    tenantid = session.get('tenantid')
    d = Dehoop(ip,port)
    d.token = token
    d.tenantid = tenantid
    return d



if __name__ == "__main__":
    app.run(HOST,PORT,debug=True)