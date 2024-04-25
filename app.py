import os
import numpy as np
from keras.models import load_model
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for,session


app = Flask(__name__)
# MySQL configuration
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'flask_users'
app.secret_key='water'

mysql= MySQL(app)
 

model = load_model('model/mymodel.keras', compile=False)
model.compile(
    optimizer = 'adam',
    loss      = 'categorical_crossentropy',
    metrics   = ['accuracy']
)

@app.route('/', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        email = request.form['emailaddress']
        pwd = request.form['password']
        cur= mysql.connection.cursor()
        cur.execute(f"select email,password from tbl_users where email ='{email}'" )
        user = cur.fetchone()
        cur.close()
        if user and pwd == user[1]:
            session['email'] = user[0]
            return redirect(url_for('index'))
        else:
            return render_template('invalid.html')

    return render_template('login.html')

    
    

        

        # if username == 'sneha@gmail.com' and password == 'sneha789':
        #     # Redirect to the home page or any other page upon successful login
        #     return redirect('/index')
        # elif username =='sital@gmail.com' and password == 'sital789':
        #     return redirect('/index')
        # elif username =='nischal@gmail.com' and password == 'nischal789':
        #     return redirect('/index')
        # elif username =='test@gmail.com' and password == 'nischal789':
        #     return redirect('/index')
        # else:
        #     return redirect('/invalid')
        # username = request.form['username']
        # password = request.form['password']
        
        # # Here you can add your authentication logic
        # # For demonstration purposes, let's say username is 'admin' and password is 'password'
       
    
    # Render the login page template
        # return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        pwd = request.form['password']
        cur= mysql.connection.cursor()
        cur.execute(f"insert into tbl_users (name,email,password) values ('{name}','{email}','{pwd}') " )
        mysql.connection.commit()
        user = cur.fetchone()
        cur.close()
        return redirect(url_for('loginPage'))
    
    return render_template('register.html')

@app.route('/index')
def index():
    name = session.get('email')
    return render_template('index.html', name=name)

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/invalid')
def invalid():
    return render_template('invalid.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    features = [float(x) for x in request.form.values()]
    final_features = np.array([features])

    prediction = np.argmax(model.predict(final_features))

    return render_template('predict.html', result=prediction)


@app.route('/logout')
def logout():
    return redirect(url_for('loginPage'))

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
