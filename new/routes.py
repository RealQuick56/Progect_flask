from flask import render_template, flash, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user

from new import db, app
from new.models import Item, User


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html', text='Чтобы не было тут пусто...')


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']
        item = Item(title=title, price=price, text=text)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка"
    else:
        return render_template('create.html')


@app.route('/login', methods=['GET', "POST"])
def logins():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')

            redirect(next_page)
        else:
            flash("Неверный логин и пароль")
    else:
        flash("Неверный логин и пароль")
    return render_template('login.html')


@app.route('/registration', methods=['GET', "POST"])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    repassword = request.form.get('repassword')

    if request.method == 'POST':
        if not(login or password or repassword):
            flash('Неправильный логин или пароль')
        elif password != repassword:
            flash('Пароли не совпадают')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('logins'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', "POST"])
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.after_request
def redirect_to_singin(response):
    if response.status_code == 401:
        return redirect(url_for('logins') + '?next=' + request.url)
    else:
        return response
