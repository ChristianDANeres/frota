from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Email


class OficinaForm(FlaskForm):
    cnpj = StringField('CNPJ', validators=[Optional(), Length(max=20)])
    nome = StringField('Nome', validators=[DataRequired(), Length(max=200)])
    logradouro = StringField('Logradouro', validators=[Optional(), Length(max=255)])
    numero = StringField('Número', validators=[Optional(), Length(max=50)])
    municipio = StringField('Município', validators=[Optional(), Length(max=120)])
    estado = StringField('Estado (Sigla)', validators=[Optional(), Length(max=2)])
    email = StringField('E-mail', validators=[Optional(), Email(), Length(max=200)])
    telefone = StringField('Telefone', validators=[Optional(), Length(max=50)])
    responsavel = StringField('Responsável', validators=[Optional(), Length(max=160)])
    submit = SubmitField('Salvar')
