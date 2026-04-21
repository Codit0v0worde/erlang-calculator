from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, IntegerField, SubmitField
from wtforms.validators import Optional, NumberRange

class CalculatorForm(FlaskForm):
    model = SelectField('Модель', choices=[
        ('erlang', 'Эрланг B'),
        ('engset', 'Энгсет'),
        ('erlang_c', 'Эрланг C (ожидание)'),
        ('batch', 'Групповое поступление'),
        ('reservation', 'С резервированием')
    ])
    task = SelectField('Задача', choices=[
        ('direct', 'Прямая (p и m)'),
        ('inverse_p', 'Обратная 1 (v по p)'),
        ('inverse_m', 'Обратная 2 (v по m)'),
        ('overload', 'Обратная 3 (доля выгрузки)'),
        ('reservation', 'Подбор v и r')   # для модели с резервированием
    ])
    # Общие поля
    a = FloatField('Нагрузка a (Эрл)', validators=[Optional()])
    v = IntegerField('Число каналов v', validators=[Optional()])
    # Для Энгсета
    N = IntegerField('Число источников N', validators=[Optional(), NumberRange(min=1)])
    # Для группового поступления
    k = IntegerField('Размер группы k', validators=[Optional(), NumberRange(min=1)])
    # Целевые значения
    p_target = FloatField('Целевая вероятность p', validators=[Optional(), NumberRange(min=0, max=1)])
    m_target = FloatField('Целевое среднее число занятых каналов m', validators=[Optional(), NumberRange(min=0)])
    p_measured = FloatField('Измеренная вероятность p*', validators=[Optional(), NumberRange(min=0, max=1)])
    p_norm = FloatField('Нормативная вероятность p', validators=[Optional(), NumberRange(min=0, max=1)])
    # Для резервирования
    a_high = FloatField('Нагрузка высокого приоритета a_high', validators=[Optional()])
    a_low = FloatField('Нагрузка низкого приоритета a_low', validators=[Optional()])
    p_high_target = FloatField('Целевая P потерь высокого приоритета', validators=[Optional(), NumberRange(min=0, max=1)])
    p_low_target = FloatField('Целевая P потерь низкого приоритета', validators=[Optional(), NumberRange(min=0, max=1)])
    submit = SubmitField('Рассчитать')