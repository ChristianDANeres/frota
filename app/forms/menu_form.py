from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from wtforms_sqlalchemy.fields import QuerySelectField


class MenuForm(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired(), Length(max=60)])
    nome = StringField('Nome', validators=[DataRequired(), Length(max=120)])
    icone = StringField('Ícone (Bootstrap Icons)', validators=[Optional(), Length(max=60)])
    endpoint = StringField('Endpoint Flask', validators=[Optional(), Length(max=120)])
    ordem = IntegerField('Ordem', default=0)
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
