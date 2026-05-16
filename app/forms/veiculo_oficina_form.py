from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import DateField, DecimalField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, NumberRange, Length


class VeiculoOficinaForm(FlaskForm):
    data_entrada = DateField('Data de Entrada', validators=[DataRequired()])
    data_saida = DateField('Data de Saída', validators=[Optional()])
    km_entrada = DecimalField('KM Entrada', places=2, validators=[Optional(), NumberRange(min=0)])
    km_saida = DecimalField('KM Saída', places=2, validators=[Optional(), NumberRange(min=0)])
    motorista_entrada_id = SelectField('Motorista', coerce=int, validators=[Optional()])
    oficina_id = SelectField('Oficina', coerce=int, validators=[DataRequired()])
    veiculo_id = SelectField('Veículo', coerce=int, validators=[DataRequired()])
    motivo = TextAreaField('Motivo', validators=[Optional(), Length(max=4000)])
    submit = SubmitField('Salvar')


class VeiculoOficinaAnexoForm(FlaskForm):
    tipo_arquivo_id = SelectField('Tipo de Arquivo', coerce=int, validators=[Optional()])
    arquivo = FileField('Arquivo', validators=[
        DataRequired(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Apenas PDF e imagens.'),
        FileSize(max_size=3 * 1024 * 1024, message='Tamanho máximo: 3 MB.')
    ])
    submit = SubmitField('Enviar')
