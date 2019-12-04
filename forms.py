from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField)
from wtforms.validators import DataRequired, Length, Email, EqualTo

class CadastroUsuario(FlaskForm):
    usuario = StringField('Usuário', validators = [DataRequired(), Length(min = 2, max = 80)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    senha = PasswordField('Senha', validators = [DataRequired(), EqualTo('repita_senha')])
    repita_senha = PasswordField('Repita sua senha', validators = [DataRequired()])
    submit = SubmitField('Cadastrar')

class LoginUsuario(FlaskForm):
    usuario = StringField('Usuário', validators = [DataRequired()])
    senha = PasswordField('Senha', validators = [DataRequired()])
    remember_me = BooleanField('Remember_me')
    submit = SubmitField('Entrar')