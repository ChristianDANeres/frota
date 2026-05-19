from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, TextAreaField, DecimalField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, Length


class DiarioForm(FlaskForm):
    codigo       = StringField('Código', validators=[DataRequired(), Length(max=30)])
    veiculo_id   = SelectField('Veículo (Placa)', coerce=int, validators=[DataRequired()])
    motorista_id = SelectField('Motorista', coerce=int, validators=[Optional()])
    data         = DateField('Data', validators=[DataRequired()])
    km           = DecimalField('KM', places=2, validators=[DataRequired(), NumberRange(min=0)])
    texto        = TextAreaField('Texto', validators=[Optional(), Length(max=10000)])
    submit       = SubmitField('Salvar')


class DiarioAnexoForm(FlaskForm):
    tipo_arquivo_id = SelectField('Tipo de Arquivo', coerce=int, validators=[Optional()])
    arquivo = FileField('Arquivo', validators=[
        DataRequired(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx'],
                    'Apenas PDF, imagens e documentos Office.'),
        FileSize(max_size=3 * 1024 * 1024, message='Tamanho máximo: 3 MB.'),
    ])
    submit = SubmitField('Enviar')
