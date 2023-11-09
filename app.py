from flask import Flask, render_template, url_for, request, session, flash, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "djfljdfljfnkjsfhjfshjkfjfjfhjdhfdjhdfu"

user = "root"
password = ""
host = "localhost"
dbname = "foodbooked"

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{user}:{password}@{host}/{dbname}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
class Employes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def __init__(self, username, email, password, address):
        self.username = username
        self.email = email
        self.password = password
        self.address = address
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f'<user: {self.username}>'

#<----------------- user ------------------>
#< sign up >
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        password_hash = generate_password_hash(password)
        add_data = user(username=username, email=email, password=password_hash)
        #add_data = user(username, email, password)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Registration successful!")

    return render_template('signup.html')

#< login >
@app.route('/')
def login_user():
    passwordhash = generate_password_hash('test2')
    print(passwordhash)
    return render_template('login.html')

# @app.route('/submit', methods=['GET', 'POST'])
# def login_user_submit():
#     _username = request.form['username']
#     _password = request.form['password']
#     if _username and _password:
#         row = user.query.filter_by(username=_username).first()
#         if row:
#             print(f"User found: {row.username}, {row.password}")
#             if check_password_hash(row.password, _password):
#                 session['username'] = row.username
#                 return redirect(url_for('page'))
#             else:
#                 flash('Invalid Password!')
#                 return redirect(url_for('login_user'))
#         else:
#             flash('Invalid username or password!')
#             return redirect(url_for('login_user'))
#     else:
#         flash('Invalid usernamd or password')
#         return redirect(url_for('login_user'))
#< home >
@app.route('/page')
def page():
    return render_template('page.html')

#     if 'username' in session:
#         username_session = session['username']
#         user_rs = user.query.filter_by(username=username_session).first()
#         return render_template('page.html', user_rs=user_rs)
#     else:
#         return redirect(url_for('login_user'))

#< logout >
# @app.route('/logout')
# def logout_user():
#     if 'username' in session:
#         session.pop('username', None)
#     return redirect('/home')


#<----------------- employee ------------------>
#< employee list >
@app.route('/all_data')
def index():
    data_employe = Employes.query.all()
    return render_template('index.html', data=data_employe)

#< register employee >
@app.route('/input_employee', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']


        add_data = Employes(username, email, password, address)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('index'))

    return render_template('input.html')

#< edit >
@app.route('/edit/<int:id>')
def edit_data(id):
    data_employes = Employes.query.get(id)
    return render_template('edit.html', data=data_employes)

@app.route('/proses_edit', methods=['POST', 'GET'])
def proses_edit():
    data_employes = Employes.query.get(request.form.get('id'))

    data_employes.username = request.form['username']
    data_employes.email = request.form['email']
    data_employes.password = request.form['password']
    data_employes.address = request.form['address']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('index'))

#< delete >
@app.route('/delete/<int:id>')
def delete(id):
    data_employe = Employes.query.get(id)
    db.session.delete(data_employe)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)