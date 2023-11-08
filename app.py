from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

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
login_manager = LoginManager()
login_manager.init_app(app)
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
class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

#<----------------- user ------------------>
#< login >
@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('page'))
        else:
            flash('Login failed. Check your credentials and try again.', 'danger')
    return render_template('login.html')

#< home >
@app.route('/page')
@login_required
def page():
    return 'Welcome to your dashboard, {}'.format(current_user.username)

#< logout >
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#< sign up >
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']


        add_data = user(username, email, password)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

    return render_template('signup.html')

#<----------------- employee ------------------>
#< employee list >
@app.route('/all_data')
def index():
    data_employe = Employes.query.all()
    return render_template('index.html', data=data_employe)

#< login employee >
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
    db.create_all()
    app.run(debug=True)