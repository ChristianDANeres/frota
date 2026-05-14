from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, DateTimeLocalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange


STATUS_CHOICES = [('EM_ABERTO', 'Em Aberto'), ('INICIADA', 'Iniciada'), ('FINALIZADA', 'Finalizada')]


class ViagemForm(FlaskForm):
    veiculo_id = SelectField('Veículo', coerce=int, validators=[DataRequired()])
    motorista_id = SelectField('Motorista', coerce=int, validators=[DataRequired()])
    tipo_viagem_id = SelectField('Tipo de Viagem', coerce=int, validators=[Optional()])
    destino = StringField('Destino', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[Optional()])
    km_inicial = DecimalField('KM Inicial', places=2, validators=[DataRequired(), NumberRange(min=0)])
    km_final = DecimalField('KM Final', places=2, validators=[Optional(), NumberRange(min=0)])
    status = SelectField('Status', choices=STATUS_CHOICES, default='EM_ABERTO')
    data_inicial = DateTimeLocalField('Data/Hora Inicial', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    data_final = DateTimeLocalField('Data/Hora Final', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    submit = SubmitField('Salvar')


class ViagemPacienteForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    nome_mae = StringField('Nome da Mãe', validators=[DataRequired()])
    data_nascimento = StringField('Data de Nascimento', validators=[DataRequired()])
    submit = SubmitField('Adicionar Paciente')
