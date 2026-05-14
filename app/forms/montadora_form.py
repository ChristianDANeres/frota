from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class MontadoraForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=120)])
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
