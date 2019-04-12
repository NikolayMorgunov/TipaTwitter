from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask import redirect, render_template
from users_db import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twit_twit'
User.create_table()

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    rep_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    photo = FileField('Выберите аватар')
    submit = SubmitField('Создать пользователя')

@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Вход', form=form)


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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
