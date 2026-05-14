from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import DecimalField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange


class AbastecimentoForm(FlaskForm):
    data = DateField('Data', validators=[DataRequired()])
    veiculo_id = SelectField('Veículo', coerce=int, validators=[DataRequired()])
    motorista_id = SelectField('Motorista', coerce=int, validators=[Optional()])
    km = DecimalField('KM', places=2, validators=[DataRequired(), NumberRange(min=0)])
    quantidade = DecimalField('Quantidade (L)', places=3, validators=[DataRequired(), NumberRange(min=0)])
    valor = DecimalField('Valor Total (R$)', places=2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Salvar')


class AbastecimentoAnexoForm(FlaskForm):
    tipo_arquivo_id = SelectField('Tipo de Arquivo', coerce=int, validators=[Optional()])
    arquivo = FileField('Arquivo', validators=[
        DataRequired(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Apenas PDF e imagens.'),
        FileSize(max_size=3 * 1024 * 1024, message='Tamanho máximo: 3 MB.')
    ])
    submit = SubmitField('Enviar')
