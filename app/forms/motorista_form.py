from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, BooleanField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class MotoristaForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired(), Length(max=14)])
    nome = StringField('Nome', validators=[DataRequired(), Length(max=160)])
    data_nascimento = DateField('Data de Nascimento', validators=[Optional()])
    cnh = StringField('CNH', validators=[DataRequired(), Length(max=20)])
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')


class MotoristaAnexoForm(FlaskForm):
    tipo_arquivo_id = SelectField('Tipo de Arquivo', coerce=int, validators=[Optional()])
    arquivo = FileField('Arquivo', validators=[
        DataRequired(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Apenas PDF e imagens.'),
        FileSize(max_size=3 * 1024 * 1024, message='Tamanho máximo: 3 MB.')
    ])
    submit = SubmitField('Enviar')
