from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Optional, Email


class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=160)])
    cnpj = StringField('CNPJ', validators=[Optional(), Length(max=20)])
    email = StringField('E-mail', validators=[Optional(), Email(), Length(max=160)])
    telefone = StringField('Telefone', validators=[Optional(), Length(max=30)])
    endereco = StringField('Endereço', validators=[Optional(), Length(max=255)])
    municipio = StringField('Município', validators=[Optional(), Length(max=120)])
    responsavel = StringField('Responsável', validators=[Optional(), Length(max=160)])
    logo_esquerdo = FileField('Logo Relatório Esquerdo', validators=[Optional(), FileAllowed(['png','jpg','jpeg','svg'])])
    logo_direito = FileField('Logo Relatório Direito', validators=[Optional(), FileAllowed(['png','jpg','jpeg','svg'])])
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
