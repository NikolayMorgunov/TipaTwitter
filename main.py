from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask import redirect, render_template
import users_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twit_twit'
db = users_db.DB()
users_db.UsersModel(db.get_connection()).init_table()

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
    if form.validate_on_submit():
        user_db = users_db.UsersModel(db.get_connection())
        if not user_db.exists(form.data['username']) and form.data['password'] == form.data['rep_password']:
            return redirect('/success_register')
        elif db.exists(form['username']):
            exists = True
        elif form.data['password'] != form.data['rep_password']:
            diff_pass = True
    return render_template('register.html', title='Регистрация', form=form, exists=exists, diff_pass=diff_pass)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
