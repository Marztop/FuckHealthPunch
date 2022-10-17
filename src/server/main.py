from flask import Flask,render_template,request
import time
from api import HealthPunch

app = Flask(__name__)


@app.route('/fuckthehealthpunch',methods = ['POST', 'GET'])
def print_res():
    if request.method == 'POST':
        authentication=request.form.get('authentication')
        func_error,message=HealthPunch.healthFill(authentication)
        return render_template('healthpunch_res.html',healthpunch_res='%s : %s'%(func_error,message))
    return render_template('authentication_submit.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
