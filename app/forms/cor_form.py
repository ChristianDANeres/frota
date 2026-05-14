from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class CorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=80)])
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
