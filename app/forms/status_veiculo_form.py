from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class StatusVeiculoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=80)])
    descricao = StringField('Descrição', validators=[Optional(), Length(max=255)])
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
