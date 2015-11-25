from intro_to_flask import app
from flask import Flask, render_template, json, request,jsonify
from flask.ext.mysql import MySQL
from flask import render_template, request, flash, session, url_for, redirect
from forms import ContactForm, SignupForm, SigninForm
from flask.ext.mail import Message, Mail
from models import db, User

mail = Mail()
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'gen'
app.config['MYSQL_DATABASE_PASSWORD'] = 'gen'
app.config['MYSQL_DATABASE_DB'] = 'genlysis_1'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

choose = ""

@app.route('/insertdb',methods=['POST','GET'])
def insertdb():
  global choose
  if 'email' not in session:
    return redirect(url_for('signin'))

  tuples = request.form.getlist('tupleval')
  header = choose
  print header
  valstr = ""
  for a in tuples:     
    valstr += "'"+ str(a) +"'" +","
  valstr = valstr[:-1]
  print valstr
  print type(valstr)
  conn = mysql.connect()
  cursor = conn.cursor() 
  try:
    query = "INSERT INTO "+str(choose)+" VALUES ( "+valstr+" );"
    #query = "INSERT INTO bacteria VALUES ('123','qwerty');"

    cursor.execute(query)
    conn.commit()
  except:
    conn.rollback()
    return redirect(url_for('error'))

  conn.close() 
  return redirect(url_for('fill'))




@app.route('/fill',methods=['POST','GET'])
def fill():
  global choose
  if 'email' not in session:
    return redirect(url_for('signin'))

  conn = mysql.connect()
  cursor = conn.cursor() 
  
  if request.method == 'POST':
      try:
          choose = request.form['option']
          print "fsfsdfs"
          print type(choose) 
          query = "select DISTINCT(COLUMN_NAME) from information_schema.columns where table_name = '"+ str(choose) +"' ;"
          cursor.execute(query)
          data = cursor.fetchall()
          valstr = []
          for a in data:     
            valstr += a     
          attributes = valstr  
          print data
          conn.close() 
          return render_template('fillafter.html',attributes = attributes, choose = choose)
      except:
        return redirect(url_for('error'))

  
  elif request.method == 'GET':
    try:
      query = "SHOW TABLES;"
      cursor.execute(query)
      data = cursor.fetchall()
      valstr = []
      for a in data:     
        valstr += a     
      activities = valstr
      conn.close()   
      return render_template('fillin.html',activities = activities)
    except:
      return redirect(url_for('error'))
        
  

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/error')
def error():
  return render_template('error.html')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/results',methods=['POST','GET'])
def results():
   
    name = request.form['text1']
    name = '"' +name+'"'
    option = request.form['item']
    #checks = request.form['check' ]
    value = request.form.getlist('check')
    printf = request.form.getlist('print')
    printstr = ""
    for a in printf:     
      printstr += a 
    print printstr   
    print value
    print type(printf)
    valstr = ""
    for a in value:     
      valstr += a + ","
    
    valstr = valstr[:-1]
    print valstr
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            #batch statement
           
            if option == "Disease":
              print 1
              query = "SELECT "+valstr+" FROM pathogenecity, specie_det, taxonomy, sequences, morphology, bacteria, meta_char, genome WHERE Specie_Det_Id = Pid AND Species = Species_name AND Seq_Id = Pid AND Specieid = Pid AND Id = Pid AND Meta_Specie_id = Id and Id = Genome_id AND Disease = "+name+";"
            elif option == "Species":
              print 2
              query = "SELECT "+valstr+" FROM pathogenecity, specie_det, taxonomy, sequences, morphology, bacteria, meta_char, genome WHERE Specie_Det_Id = Pid AND Species = Species_name AND Seq_Id = Pid AND Specieid = Pid AND Id = Pid AND Meta_Specie_id = Id and Id = Genome_id AND Species_name = "+name+";"
            elif option == "Id":
              print 3
              query = "SELECT "+valstr+" FROM pathogenecity, specie_det, taxonomy, sequences, morphology, bacteria, meta_char, genome WHERE Specie_Det_Id = Pid AND Species = Species_name AND Seq_Id = Pid AND Specieid = Pid AND Id = Pid AND Meta_Specie_id = Id and Id = Genome_id AND Id = "+name+";"
            elif option == "Location":
              print 3
              query = "SELECT "+valstr+" FROM pathogenecity, specie_det, taxonomy, sequences, morphology, bacteria, meta_char, genome WHERE Specie_Det_Id = Pid AND Species = Species_name AND Seq_Id = Pid AND Specieid = Pid AND Id = Pid AND Meta_Specie_id = Id and Id = Genome_id AND Location = "+name+";"
            else:
              print 4
              query = "SELECT * FROM pathogenecity, specie_det, taxonomy, sequences, morphology, bacteria, meta_char, genome WHERE Specie_Det_Id = Pid AND Species = Species_name AND Seq_Id = Pid AND Specieid = Pid AND Id = Pid AND Meta_Specie_id = Id and Id = Genome_id;"
            #query = "SELECT Id,Location FROM bacteria"

            cursor.execute(query)
            data = cursor.fetchall()
            #print type(data)
            #print len(data)   
            conn.close() 
            json_output = json.dumps(data)

    except:
                          print "Inavlid Entry"
                          return redirect(url_for('error'))


    print query                 
    #print type(json_output) 
    if printstr == "print":
      return render_template('printresult.html', datas=data, titles= value)

    #print type(json_output)
    return render_template('results.html', datas=data, titles= value)
    

@app.route('/report')
def report():
   
    #_name = request.form['inputCat']
    #db = MySQLdb.connect("localhost", "root", "","test")
    #print "iuhfuiewhiwehriwehriowjeriewiorewioruewio"
    try:
      conn = mysql.connect()
      cursor = conn.cursor()
      #batch statement
      query = "SELECT * FROM `pathogenecity`, specie_det, taxonomy, sequences, morphology, bacteria, meta_char, genome WHERE Specie_Det_Id = Pid AND Species = Species_name AND Seq_Id = Pid AND Specieid = Pid AND Id = Pid AND Meta_Specie_id = Id and Id = Genome_id;"
      #query = "SELECT Id,Location FROM bacteria"

      cursor.execute(query)
      data = cursor.fetchall()
      print type(data)
      print len(data)
      #dictdata = dict(data)
      #dictdata = dict((i,j) for i,j in data)
      query = "select DISTINCT(COLUMN_NAME) from information_schema.columns "
      cursor.execute(query)
      titles = cursor.fetchall()
      valstr = []
      for a in titles:     
        valstr += a     
      titles = valstr
      print titles
      
      json_output = json.dumps(data)
      print type(json_output)
      #with open('templates/data.json', 'w') as outfile:
                  # json.dump(data, outfile)
      
      #ht = json2html.convert(json = jsonify(data))
      #print ht
      # return jsonify(lolmax=data)
      #return json_output
      
      #return jsonify(datas = data)

      print type(json_output)
      return render_template('report.html', datas=data)
      # template = env.get_template( 'results.html')
      # return template.render( title="Country list", json_output=json_output)
      #return  render_template('index.html')
    except:
      return redirect(url_for('error'))

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='jeevu.g1@gmail.com', recipients=['jeevu.art@gmail.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)

      return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if 'email' in session:
    return redirect(url_for('profile')) 
  
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      
      session['email'] = newuser.email
      return redirect(url_for('profile'))
  
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/profile')
def profile():

  if 'email' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(email = session['email']).first()

  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if 'email' in session:
    return redirect(url_for('profile')) 
      
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))
                
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():

  if 'email' not in session:
    return redirect(url_for('signin'))
    
  session.pop('email', None)
  return redirect(url_for('home'))


@app.route('/printresult',methods=['POST','GET'])
def printresult():
   
    name = request.form['text1']
    name = '"' +name+'"'
    option = request.form['item']
    #checks = request.form['check' ]
    value = request.form.getlist('check')
    
    print value
    print type(value)
    valstr = ""
    for a in value:     
      valstr += a + ","
    
    valstr = valstr[:-1]
    print valstr
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            #batch statement
           
            if option == "Disease":
              print 1
              query = "SELECT "+valstr+" FROM pathogenecity, specie_det, taxonomy, sequences, morphology, bacteria, meta_char, genome WHERE Specie_Det_Id = Pid AND Species = Species_name AND Seq_Id = Pid AND Specieid = Pid AND Id = Pid AND Meta_Specie_id = Id and Id = Genome_id AND Disease = "+name+";"
            elif option == "Species":
              print 2
              query = "SELECT "+valstr+" FROM pathogenecity, specie_det, taxonomy, sequences, morphology, bacteria, meta_char, genome WHERE Specie_Det_Id = Pid AND Species = Species_name AND Seq_Id = Pid AND Specieid = Pid AND Id = Pid AND Meta_Specie_id = Id and Id = Genome_id AND Species_name = "+name+";"
            elif option == "Id":
              print 3
              query = "SELECT "+valstr+" FROM pathogenecity, specie_det, taxonomy, sequences, morphology, bacteria, meta_char, genome WHERE Specie_Det_Id = Pid AND Species = Species_name AND Seq_Id = Pid AND Specieid = Pid AND Id = Pid AND Meta_Specie_id = Id and Id = Genome_id AND Id = "+name+";"
            elif option == "Location":
              print 3
              query = "SELECT "+valstr+" FROM pathogenecity, specie_det, taxonomy, sequences, morphology, bacteria, meta_char, genome WHERE Specie_Det_Id = Pid AND Species = Species_name AND Seq_Id = Pid AND Specieid = Pid AND Id = Pid AND Meta_Specie_id = Id and Id = Genome_id AND Location = "+name+";"
            else:
              print 4
              query = "SELECT * FROM pathogenecity, specie_det, taxonomy, sequences, morphology, bacteria, meta_char, genome WHERE Specie_Det_Id = Pid AND Species = Species_name AND Seq_Id = Pid AND Specieid = Pid AND Id = Pid AND Meta_Specie_id = Id and Id = Genome_id;"
            #query = "SELECT Id,Location FROM bacteria"

            cursor.execute(query)
            data = cursor.fetchall()
            #print type(data)
            #print len(data)   
            conn.close() 
            json_output = json.dumps(data)

    except:
                          print "Inavlid Entry"
                          return redirect(url_for('error'))


    print query                 
    #print type(json_output)    
    #print type(json_output)
    return render_template('printresult.html', datas=data, titles= value)