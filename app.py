from flask import Flask, render_template, url_for, request, session, flash, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_bcrypt import Bcrypt #pip install Flask-Bcrypt
from sqlalchemy.sql import func
import random

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
bcrypt = Bcrypt()
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

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer(), nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer(), nullable=False)
    id_menu = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.Integer(), nullable=False)

    def __init__(self, id_user, id_menu, status):
        self.id_user = id_user
        self.id_menu = id_menu
        self.status = status

class all_menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer(), nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

#<----------------- user ------------------>
#< sign up >
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """sign up"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash('Please fill in all the fields.', 'danger')
            return render_template('signup.html')

        add_data = user(username=username, email=email, password=password)
        db.session.add(add_data)
        db.session.commit()

    return render_template('signup.html')

#< login >
@app.route('/', methods=['GET', 'POST'])
def login_user():
    """login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = user.query.filter_by(username=username).first()
        admin_data = Employes.query.filter_by(username=username).first()

        if user_data and user_data.password == password:
            session['user_id'] = user_data.id
            session['user_name'] = user_data.username
            
            # return render_template('page.html', username=user_data.username)
            return redirect(url_for('page'))
        if admin_data and admin_data.password == password:
            return redirect(url_for('order'))
        else:
            flash('Login failed. Check your credentials and try again.', 'danger')
        return render_template('login.html')
    
    return render_template('login.html')

@app.route('/changepass', methods=['GET', 'POST'])
def change_pass():
    """change password"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        success = False
        user_data = user.query.filter_by(username=username).first()

        if user_data and user_data.email == email:
            password = request.form['password']
            confirm = request.form['confirm-password']

            if password == confirm:
                user_data.password = password
                db.session.commit()
                success = True
                flash('Your password has been successfully changed.', 'success')
                return redirect(url_for('login_user'))
            else:
                flash('Password and confirmation do not match. Please try again.', 'danger')
        else:
            flash('Username or email is incorrect. Please check your credentials and try again.', 'danger')
        return render_template('changepass.html')

    return render_template('changepass.html')

#< home >
@app.route('/home')
def home():
    """home"""
    return render_template('home.html')

@app.route('/page')
def page():
    """page"""
    data_username = session.get('user_name')
    return render_template('page.html', username=data_username)

@app.route('/random_text', methods=['GET'])
def random_text():
    """random menu"""
    random_data = all_menu.query.order_by(func.rand()).first()
    return jsonify({'name': random_data.name, 'price': random_data.price})

#< logout >
@app.route('/logout')
def logout_user():
    """logout"""
    return redirect(url_for('login_user'))

#< menu >
@app.route('/menu')
def select_menu():
    """menu"""
    data_menu = Menu.query.all()
    return render_template('menu.html', data=data_menu)

@app.route('/list_order', methods=['GET'])
def list_order():
    """list order"""
    id_user = session.get('user_id')
    data_order = Order.query.get(id_user)
    if request.method == 'GET':
        order_list = []
        data_user = user.query.get(data_order.id_user)
        data_menu = Menu.query.get(data_order.id_menu)
        response = {
            'user_name': data_user.username,
            'user_email': data_user.email,
            'menu_name': data_menu.name,
            'menu_price': data_menu.price,
        }
    
        order_list.append(response)

        return render_template('status.html', order_list=order_list)
    return render_template('status.html')

@app.route('/status')
def status():
    """status"""
    id_user = session.get('user_id')
    data_order = Order.query.get(id_user)
    print(data_order)
    if data_order.status == 0:
        message = "รับออเดอร์"
        return render_template('status.html', message=message)

    return render_template('status.html')

#<----------------- employee ------------------>
#< log out >
@app.route('/logout_admin')
def logout_admin():
    """logout"""
    return redirect(url_for('login_user'))

#< employee list >
@app.route('/all_data')
def index():
    """employee list"""
    data_employe = Employes.query.all()
    return render_template('index.html', data=data_employe)

#< add employee >
@app.route('/input_employee', methods=['GET', 'POST'])
def input_data():
    """add employee"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']

        if not username or not email or not password or not address:
            flash('Please fill in all the fields.', 'danger')
            return render_template('input.html')

        add_data = Employes(username, email, password, address)
        
        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")
        return redirect(url_for('index'))
    
    return render_template('input.html')

#< edit >
@app.route('/edit/<int:id>')
def edit_data(id):
    """edit1"""
    data_employes = Employes.query.get(id)
    return render_template('edit.html', data=data_employes)

@app.route('/proses_edit', methods=['POST', 'GET'])
def proses_edit():
    """edit2"""
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
    """delete"""
    data_employe = Employes.query.get(id)
    db.session.delete(data_employe)
    db.session.commit()

    flash('Delete Data Success')
    return redirect(url_for('index'))

#< home_admin >
@app.route('/home_admin')
def home_admin():
    """home"""
    return render_template('page_admin.html')

#< add orders to table >
@app.route('/receive', methods=['POST', 'GET'])
def receive():
    """add orders to table"""
    if request.method == "POST":
        # data = request.json
        id_user = session.get('user_id')
        id_menu = request.form['id_menu']
        status = 0

        if id_user is not None and id_menu is not None:
            add_data = Order(id_user=id_user, id_menu=id_menu, status=status)
            db.session.add(add_data)
            db.session.commit()

            return redirect(url_for('page'))
    return render_template('order.html')

#< all order >
#< start status => 0 order >
@app.route('/order', methods=['GET'])
def order():
    """all order"""
    if request.method == 'GET':
        status = 0
        all_order = Order.query.filter_by(status=status).all()
        order_list = []
        for order in all_order:
            data_user = user.query.get(order.id_user)
            data_menu = Menu.query.get(order.id_menu)
            data_order = Order.query.get(order.id)
            response = {
                'user_name': data_user.username,
                'user_email': data_user.email,
                'menu_name': data_menu.name,
                'menu_price': data_menu.price,
                'id': data_order.id,
            }
            order_list.append(response)
        print(order_list)
        return render_template('order.html', order_list=order_list)
    return render_template('order.html')

#< change status => 3 cancel order >
@app.route('/cancel/<int:id>')
def cancel(id):
    """cancel"""
    cancel_order = Order.query.get(id)
    db.session.delete(cancel_order)
    db.session.commit()

    return redirect(url_for('order'))

#< change status => 1 continue >
@app.route('/continue/<int:id>')
def id_order(id):
    """order(id)"""
    data_order = Order.query.get(id)
    new_status = request.form.get('status', 1)
    data_order.status = new_status
    db.session.commit()
    return redirect(url_for('id_order2', id=id))
        
@app.route('/continue2/<int:id>')
def id_order2(id):
    """order(id)"""
    data_order = Order.query.get(id)
    if request.method == 'GET':
        data_user = user.query.get(data_order.id_user)
        data_menu = Menu.query.get(data_order.id_menu)
        response = [{
            'user_name': data_user.username,
            'user_email': data_user.email,
            'menu_name': data_menu.name,
            'menu_price': data_menu.price,
            'id': data_order.id
        }]

        return render_template('continue.html', order_list=response)
    return render_template('continue.html')

#< change status => 2 sucess >
@app.route('/success/<int:id>')
def finish(id):
    """success"""
    data_order = Order.query.get(id)
    new_status = request.form.get('status', 2)
    data_order.status = new_status
    db.session.commit()
    return redirect(url_for('finish2', id=id))
    
@app.route('/success2/<int:id>')
def finish2(id):
    """success"""
    data_order = Order.query.get(id)
    if request.method == 'GET':
        data_user = user.query.get(data_order.id_user)
        data_menu = Menu.query.get(data_order.id_menu)
        response = [{
            'user_name': data_user.username,
            'user_email': data_user.email,
            'menu_name': data_menu.name,
            'menu_price': data_menu.price,
            'id': data_order.id
        }]

        return render_template('order_success.html', order_list=response)
    return render_template('order_success.html')


if __name__ == "__main__":
    app.run(debug=True)