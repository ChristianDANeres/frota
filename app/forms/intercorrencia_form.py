from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, DateField,
                     TimeField, SelectField, BooleanField, SubmitField)
from wtforms.validators import DataRequired, Optional, NumberRange, Length


STATUS_CHOICES = [
    ('EM_ABERTO',  'Em Aberto'),
    ('EM_ANALISE', 'Em Análise'),
    ('FINALIZADO', 'Finalizado'),
]

DESTINO_CHOICES = [
    ('',          'Selecione...'),
    ('DOMICILIO', 'Domicílio'),
    ('UPA',       'UPA'),
    ('HOSPITAL',  'Hospital'),
]


class IntercorrenciaForm(FlaskForm):
    # Vínculo com viagem e paciente
    viagem_id          = SelectField('Viagem', coerce=int, validators=[DataRequired()])
    viagem_paciente_id = SelectField('Paciente da Viagem', coerce=int,
                                     validators=[Optional()])

    # Cabeçalho
    local_origem       = StringField('Local de Origem',
                                     validators=[DataRequired(), Length(max=255)])
    local_destino      = StringField('Local de Destino',
                                     validators=[Optional(), Length(max=255)])
    data_transporte    = DateField('Data do Transporte',
                                   format='%Y-%m-%d', validators=[DataRequired()])
    horario_ocorrencia = TimeField('Horário da Ocorrência',
                                   format='%H:%M', validators=[DataRequired()])

    # Dados do paciente
    paciente_nome          = StringField('Nome do Paciente',
                                          validators=[DataRequired(), Length(max=160)])
    paciente_idade         = IntegerField('Idade',
                                          validators=[Optional(), NumberRange(min=0, max=150)])
    paciente_telefone      = StringField('Telefone',
                                          validators=[Optional(), Length(max=20)])
    paciente_acompanhante  = StringField('Acompanhante',
                                          validators=[Optional(), Length(max=160)])

    # Condição física
    cond_deambula                 = BooleanField('Deambula')
    cond_nao_deambula             = BooleanField('Não Deambula')
    cond_acamado                  = BooleanField('Acamado')
    cond_cadeirante               = BooleanField('Cadeirante')
    cond_dispositivo_mobil        = BooleanField('Uso de Dispositivos de Mobilidade')
    cond_traqueostomizado         = BooleanField('Traqueostomizado')
    cond_oxigenio_continuo        = BooleanField('Uso de Oxigênio Contínuo')
    cond_portador_ostomias        = BooleanField('Portador de Ostomias')
    cond_drenos_dispositivos      = BooleanField('Em uso de drenos/dispositivos externos')
    cond_acesso_venoso_periferico = BooleanField('Com acesso venoso periférico')
    cond_acesso_venoso_central    = BooleanField('Com acesso venoso central e/ou catéter duplo-lúmen')

    # Ocorrência
    descricao_ocorrencia  = TextAreaField('Descrição da Ocorrência/Intercorrência',
                                           validators=[Optional()])
    endereco_ocorrencia   = StringField('Endereço da Ocorrência/Intercorrência',
                                         validators=[Optional(), Length(max=500)])
    socorristas           = StringField('Socorrista(s)',
                                        validators=[Optional(), Length(max=500)])
    destino_usuario       = SelectField('Destino do Usuário', choices=DESTINO_CHOICES,
                                        validators=[Optional()])
    data_atendimento      = DateField('Data do Atendimento',
                                       format='%Y-%m-%d', validators=[Optional()])
    local_atendimento     = StringField('Local do Atendimento',
                                         validators=[Optional(), Length(max=255)])
    observacoes           = TextAreaField('Observações', validators=[Optional()])

    # Status
    status = SelectField('Status', choices=STATUS_CHOICES, default='EM_ABERTO')

    submit = SubmitField('Salvar')
