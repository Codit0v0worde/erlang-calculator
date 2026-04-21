from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, IntegerField, SubmitField
from wtforms.validators import Optional, NumberRange

class CalculatorForm(FlaskForm):
    model = SelectField('Модель', choices=[
        ('erlang', 'Эрланг B'),
        ('engset', 'Энгсет'),
        ('erlang_c', 'Эрланг C (ожидание)'),
        ('erlang_a', 'Эрланг A (с уходами)'),
        ('batch', 'Групповое поступление')
    ])
    task = SelectField('Задача', choices=[
        ('direct', 'Прямая (p и m)'),
        ('inverse_p', 'Обратная 1 (v по p)'),
        ('inverse_m', 'Обратная 2 (v по m)'),
        ('overload', 'Обратная 3 (доля выгрузки)')
    ])
    a = FloatField('Нагрузка a (Эрл)', validators=[Optional()], render_kw={"placeholder": "например: 5"})
    v = IntegerField('Число каналов v', validators=[Optional()], render_kw={"placeholder": "например: 10"})
    N = IntegerField('Число источников N', validators=[Optional(), NumberRange(min=1)], render_kw={"placeholder": "например: 20"})
    k = IntegerField('Размер группы k', validators=[Optional(), NumberRange(min=1)], render_kw={"placeholder": "например: 2"})
    theta = FloatField('Интенсивность уходов θ', validators=[Optional(), NumberRange(min=0)], render_kw={"placeholder": "например: 0.1"})
    p_target = FloatField('Целевая вероятность p', validators=[Optional(), NumberRange(min=0, max=1)], render_kw={"placeholder": "например: 0.01"})
    m_target = FloatField('Целевое среднее m', validators=[Optional(), NumberRange(min=0)], render_kw={"placeholder": "например: 4.5"})
    p_measured = FloatField('Измеренная вероятность p*', validators=[Optional(), NumberRange(min=0, max=1)], render_kw={"placeholder": "например: 0.05"})
    p_norm = FloatField('Нормативная вероятность p', validators=[Optional(), NumberRange(min=0, max=1)], render_kw={"placeholder": "например: 0.01"})
    submit = SubmitField('Рассчитать')