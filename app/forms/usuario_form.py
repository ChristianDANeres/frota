from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo, Regexp


class UsuarioForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired(), Length(max=80)])
    nome = StringField('Nome completo', validators=[DataRequired(), Length(max=160)])
    email = StringField('E-mail', validators=[Optional(), Email(), Length(max=160)])
    cpf = StringField('CPF', validators=[Optional(), Regexp(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$", message='Formato de CPF inválido'), Length(max=20)])
    telefone = StringField('Telefone', validators=[Optional(), Length(max=30)])
    senha = PasswordField('Senha', validators=[Optional(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar senha', validators=[EqualTo('senha', message='Senhas não conferem')])
    is_admin = BooleanField('Administrador')
    ativo = BooleanField('Ativo', default=True)
    clientes = SelectMultipleField('Municípios Vinculados', coerce=int)
    perfis = SelectMultipleField('Perfis de Acesso', coerce=int)
    submit = SubmitField('Salvar')
