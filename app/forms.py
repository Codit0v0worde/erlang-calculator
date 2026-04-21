from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, IntegerField, SubmitField
from wtforms.validators import Optional, NumberRange

class CalculatorForm(FlaskForm):
    model = SelectField('Модель', choices=[
        ('erlang', 'Эрланг B'),
        ('engset', 'Энгсет'),
        ('erlang_c', 'Эрланг C (ожидание)'),
        ('batch', 'Групповое поступление')
    ])
    task = SelectField('Задача', choices=[
        ('direct', 'Прямая (p и m)'),
        ('inverse_p', 'Обратная 1 (v по p)'),
        ('inverse_m', 'Обратная 2 (v по m)'),
        ('overload', 'Обратная 3 (доля выгрузки)')
    ])
    a = FloatField('Нагрузка a (Эрл)', validators=[Optional()])
    v = IntegerField('Число каналов v', validators=[Optional()])
    N = IntegerField('Число источников N', validators=[Optional(), NumberRange(min=1)])
    k = IntegerField('Размер группы k', validators=[Optional(), NumberRange(min=1)])
    p_target = FloatField('Целевая вероятность p', validators=[Optional(), NumberRange(min=0, max=1)])
    m_target = FloatField('Целевое среднее число занятых каналов m', validators=[Optional(), NumberRange(min=0)])
    p_measured = FloatField('Измеренная вероятность p*', validators=[Optional(), NumberRange(min=0, max=1)])
    p_norm = FloatField('Нормативная вероятность p', validators=[Optional(), NumberRange(min=0, max=1)])
    submit = SubmitField('Рассчитать')