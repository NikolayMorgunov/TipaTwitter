from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask import redirect, render_template
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'twit_twit'


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
    to_register = SubmitField('Зарегестрироваться')


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
    return render_template('login.html', title='Авторизация', form=form)




if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

