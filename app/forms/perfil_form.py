from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class PerfilForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    descricao = StringField('Descrição', validators=[Optional(), Length(max=255)])
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
