from flask import Flask,render_template,request

from App.src.Dehoop import Root
HOST = "127.0.0.1"
PORT = "3020"

app = Flask(__name__,template_folder='templates')

@app.route("/",)

def index():
    return render_template("content.html")


@app.route("/login",methods=['POST'])
def login():
    pass 

@app.route("/ping",methods=['GET'])
def ping():
    ip = request.args.get("ip")
    port = request.args.get("port")
    
    root = Root(ip,port).test_connect()
    return render_template('content.html',ping =root)
if __name__ == "__main__":
    app.run(HOST,PORT,debug=True)