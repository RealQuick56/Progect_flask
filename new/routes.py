from flask import render_template, session, flash, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user

from new import db, app
from new.models import Item, User


@app.route('/home')
def index():
    items = Item.query.order_by(Item.id).all()
    try:
        return render_template('index.html', data=items, user=session['login'])
    except:
        return render_template('index.html', data=items, user='')


@app.route('/about')
def about():
    try:
        return render_template('about.html', text='Чтобы не было тут пусто...', user=session['login'])
    except:
        return render_template('about.html', text='Чтобы не было тут пусто...', user='')


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == "POST":
        __tablename__ = 'item'

        title = request.form['title']
        price = request.form['price']
        text = request.form['text']
        item = Item(title=title, price=price, text=text)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/home')
        except:
            return "Получилась ошибка"
    else:
        try:
            return render_template('create.html', user=session['login'])
        except:
            return render_template('create.html', user='')


@app.route('/login', methods=['GET', "POST"])
def logins():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            session['login'] = user.login
            if next_page is None:
                return redirect('/profile')
            else:
                return redirect(next_page)
        else:
            flash("Неверный логин и пароль")
    else:
        flash("Неверный логин и пароль")
    try:
        return render_template('login.html', user=session['login'])
    except:
        return render_template('login.html', user='')


@app.route('/registration', methods=['GET', "POST"])
def register():
    if request.method == 'POST':
        __tablename__ = 'user'

        login = request.form['login']
        nick = request.form['nick']
        text_about = request.form['about_me']
        password = request.form['password']
        repassword = request.form['repassword']
        photo = request.form['photo']

        try:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd, nick=nick, text_about=text_about, photo=photo)
            db.session.add(new_user)
            db.session.commit()

            session['login'] = new_user.login
            return redirect('/home')
        except:
            return 'Получилась ошибка!'
    else:
        try:
            return render_template('register.html', user=session['login'])
        except:
            return render_template('register.html', user='')


@app.route('/logout', methods=['GET', "POST"])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect('/home')


@app.route('/profile')
@login_required
def profile():
    users = User.query.order_by(User.id).all()
    return render_template('profile.html', user=session['login'], users=users)


@app.route('/buy/<path:title>')
@login_required
def buy(title):
    items = Item.query.order_by(Item.id).all()
    try:
        return render_template('buy.html', title=title, data=items, user=session['login'])
    except:
        return render_template('register.html', user='')




@app.after_request
def redirect_to_singing(response):
    if response.status_code == 401:
        return redirect(url_for('logins') + '?next=' + request.url)
    else:
        return response
