from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


COMBUSTIVEIS = [('', 'Selecione...'), ('Gasolina', 'Gasolina'), ('Etanol', 'Etanol'),
                ('Flex', 'Flex'), ('Diesel', 'Diesel'), ('GNV', 'GNV'), ('Elétrico', 'Elétrico')]


class VeiculoForm(FlaskForm):
    placa = StringField('Placa', validators=[DataRequired(), Length(max=10)])
    montadora_id = SelectField('Montadora', coerce=int, validators=[Optional()])
    modelo = StringField('Modelo', validators=[Optional(), Length(max=120)])
    cor_id = SelectField('Cor', coerce=int, validators=[Optional()])
    ano_fabricacao = IntegerField('Ano de Fabricação', validators=[Optional()])
    tipo_combustivel = SelectField('Combustível', choices=COMBUSTIVEIS, validators=[Optional()])
    status_veiculo_id = SelectField('Status', coerce=int, validators=[Optional()])
    ativo = BooleanField('Ativo', default=True)
    submit = SubmitField('Salvar')
