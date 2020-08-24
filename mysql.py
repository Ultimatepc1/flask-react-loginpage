from flask import *
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token

app=Flask(__name__)
#Setting up secret key
#app.secret_key='secret123456'





#Config MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='tempusers'
app.config['MYSQL_CURSORCLASS']='DictCursor'
app.config['JWT_SECRET_KEY']='secret123456'

#init MySQL
mysql=MySQL(app)
bcrypt=Bcrypt(app)
jwt=JWTManager(app)
CORS(app)

#@app.errorhandler(404) 
  
# inbuilt function which takes error as parameter 
#def not_found(e): 
  
# defining function 
    #return render_template("errorcheck.html")

@app.route('/users/register',methods=['POST'])
def register():
    
    name=request.get_json()['name']
    email=request.get_json()['email']
    password=bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    phoneno=request.get_json()['phoneno']
    cur2=mysql.connection.cursor()
    rv=cur2.execute("SELECT * FROM users where email = '"+str(email)+"'")
    if(rv>0):
        cur2.close()
        result={"error": "Account already exists"}
    else:
        cur2.close()
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO `users`(`name`, `email`, `password`,`phoneno`) VALUES (%s,%s,%s,%s)", (str(name),str(email),str(password),str(phoneno)))
        mysql.connection.commit()
        result={"name": name,"email": email,"password": password,"phoneno": phoneno,"userrole": 'Client'}
        cur.close()
    return jsonify({"result":result})

@app.route('/users/login',methods=['POST'])
def login():
    cur=mysql.connection.cursor()
    email=request.get_json()['email']
    password=request.get_json()['password']
    result=""

    rests=cur.execute("SELECT * FROM users where email = '"+str(email)+"'")
    rv=cur.fetchone()
    if (rests>0):
        if bcrypt.check_password_hash(rv['password'],password):
            acess_token = create_access_token(identity = {"name": rv['name'],"email": rv['email'],"phoneno": rv['phoneno'],"userrole": rv['userrole'],"created_at": rv['created_at']})
            result=jsonify({"token": acess_token})
        else:
            result=jsonify({"error":"Invalid username or password"})    
    else:
        result=jsonify({"error":"Invalid username or password"})
    cur.close()
    return result

if __name__=='__main__':
    #app.run(debug=True)
    app.debug=True
    app.run(port=3000)
