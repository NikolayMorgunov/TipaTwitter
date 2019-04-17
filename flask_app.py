from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired
from flask import redirect, render_template
from users_db import *
from news_db import *
from auth_check import *
from news_create_check import *
from flask import session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twit_twit'
#User.create_table()
#News.create_table()


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    rep_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Создать пользователя')


class NewsCreateForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    text = TextAreaField('Текст новости')
    submit = SubmitField('Создать новость')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/main_page')
    form = LoginForm()
    username = form.data['username']
    password = form.data['password']
    normal_auth = True
    if form.validate_on_submit():
        if auth_check(username, password):
            session['username'] = username
            return redirect('/main_page')
        else:
            normal_auth = False
    return render_template('login.html', title='Вход', form=form, normal_auth=normal_auth)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    exists = False
    diff_pass = False
    username = form.data['username']
    password = form.data['password']
    rep_password = form.data['rep_password']
    if form.validate_on_submit():
        if User.select().where(User.username == username):
            diff_pass = True
        if diff_pass:
            exists = True
        elif password != rep_password:
            diff_pass = True
        else:
            user = User.create(username=username, password=password)
            return redirect("/success_register")
    return render_template('register.html', title='Регистрация', form=form, exists=exists, diff_pass=diff_pass)


@app.route('/success_register')
def success_register():
    return render_template('success_register.html')


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    if 'username' in session:
        return render_template('main_page.html', title='Главная страница', current_username=session['username'],
                               news=News.select())
    return redirect('/login')


@app.route('/my_page', methods=['GET', 'POST'])
def my_page():
    if 'username' in session:
        return render_template('my_page.html', title='Моя страница', current_username=session['username'],
                               news=News.select().where(News.username == session['username']))
    return redirect('/login')


@app.route('/logout', methods=['GET', 'POST'])
def log_out():
    session.pop('username', 0)
    return redirect('/login')


@app.route('/create_news', methods=['GET', 'POST'])
def create_news():
    form = NewsCreateForm()
    title = form.data['title']
    text = form.data['text']
    norm_create = True
    if form.validate_on_submit():
        if news_create_check(title):
            news = News.create(title=title, text=text, username=session['username'])
            return redirect('/my_page')
        else:
            norm_create = False
    return render_template("create_news.html", title='Создание новости', form=form, norm_create=norm_create)


@app.route('/delete_news/<title>')
def delete_news(title):
    news_to_delete = News.select().where(News.title == title).get()
    news_to_delete.delete_instance()
    return redirect('/my_page')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
