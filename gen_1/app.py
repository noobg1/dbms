from flask import Flask, render_template, json, request,jsonify
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from json2html import *


mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'gen'
app.config['MYSQL_DATABASE_PASSWORD'] = 'gen'
app.config['MYSQL_DATABASE_DB'] = 'genlysis_1'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/php')
def php():
    return render_template('php.php')


@app.route('/')
def main():
   
    #_name = request.form['inputCat']
    #db = MySQLdb.connect("localhost", "root", "","test")
    #print "iuhfuiewhiwehriwehriowjeriewiorewioruewio"
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT *  FROM Taxonomy"
   
    cursor.execute(query)
    data = cursor.fetchall()
    print data
    
    json_output = json.dumps(data)
    with open('templates/data.json', 'w') as outfile:
#                 json.dump(data, outfile)
    

    
   # return jsonify(lolmax=data)
    #return json_output
    #return jsonify(data=cursor.fetchall())
    return  render_template('index.html')






@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
 
@app.route('/render')    
def render():
    print "checked"
    return render_template('data.json')







@app.route('/signUp',methods=['POST','GET'])
def signUp():	
    try:
        _name = request.form['inputCat']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                #return json.dumps({'message':'User created successfully !'})
                with open('data.json', 'w') as outfile:
    				json.dump({'message':'User created successfully !'}, outfile)
                #return jsonify({'message':'User created successfully !'})
                #json2html.convert(json = {'name':'softvar','age':'22'})
                #jsondata = {'message':'User created successfully !'}
                #return render_template('data.html',data=data, jsondata=jsondata)
                #jsondata = request.form['inputName']
                # Convert the JSON data into a Python structure
                #data = json.loads({'message':'User created successfully !'})
                #return render_template('data.json', data=data, jsondata={'message':'User created successfully !'})
                render()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

if __name__ == "__main__":
    app.debug = True
    app.run(port=5002)
    #app.run()