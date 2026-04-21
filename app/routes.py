from flask import Blueprint, render_template, request, jsonify
from app.forms import CalculatorForm
from app import calculator

main_bp = Blueprint('main', __name__)

def format_readable(result):
    lines = []
    for key, value in result.items():
        if key == 'p':
            lines.append(f"Вероятность блокировки: {value:.6f}")
        elif key == 'p_wait':
            lines.append(f"Вероятность ожидания: {value:.6f}")
        elif key == 'm':
            lines.append(f"Среднее число занятых каналов: {value:.4f}")
        elif key == 'v_opt':
            lines.append(f"Необходимое число каналов: {value}")
        elif key == 'reduction_percent':
            lines.append(f"Доля выгружаемой нагрузки: {value:.2f}%")
        else:
            lines.append(f"{key}: {value}")
    return "<br>".join(lines)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = CalculatorForm()
    readable = None
    explanation = ""
    if form.validate_on_submit():
        model = form.model.data
        task = form.task.data
        result = None
        try:
            if task == 'direct':
                a = float(form.a.data or 0)
                v = int(form.v.data or 0)
                if model == 'erlang':
                    p = calculator.erlang_b(v, a)
                    m = a * (1 - p)
                    result = {'p': round(p, 6), 'm': round(m, 4)}
                    explanation = "Формула Эрланга B: вероятность блокировки p = E(v,a)."
                elif model == 'engset':
                    N = int(form.N.data or 1)
                    p = calculator.engset_b(v, a, N)
                    p_states = [1.0]
                    for i in range(1, v+1):
                        p_states.append(p_states[-1] * (N - i + 1) * a / i)
                    sum_p = sum(p_states)
                    m = sum(i * p_states[i] for i in range(v+1)) / sum_p
                    result = {'p': round(p, 6), 'm': round(m, 4)}
                    explanation = "Модель Энгсета с конечным числом источников N."
                elif model == 'erlang_c':
                    p = calculator.erlang_c(v, a)
                    m = a
                    result = {'p_wait': round(p, 6), 'm': round(m, 4)}
                    explanation = "Формула Эрланга C: вероятность ожидания p_wait = C(v,a)."
                elif model == 'batch':
                    k = int(form.k.data or 1)
                    p = calculator.batch_erlang_b(v, a, k)
                    m = a * k * (1 - p)
                    result = {'p': round(p, 6), 'm': round(m, 4)}
                    explanation = "Модель с групповым поступлением (размер группы k). Эквивалентная нагрузка = a·k."
            elif task == 'inverse_p':
                a = float(form.a.data or 0)
                p_target = float(form.p_target.data or 0.01)
                if model == 'erlang':
                    v_opt = calculator.erlang_b_inv_v_p(a, p_target)
                    result = {'v_opt': v_opt}
                    explanation = f"Подбор числа каналов v методом перебора до выполнения условия p ≤ {p_target}."
                elif model == 'engset':
                    N = int(form.N.data or 1)
                    v_opt = calculator.engset_inv_v_p(a, N, p_target)
                    result = {'v_opt': v_opt}
                    explanation = f"Модель Энгсета: перебор v до достижения p ≤ {p_target}."
                elif model == 'erlang_c':
                    v_opt = calculator.erlang_c_inv_v_p(a, p_target)
                    result = {'v_opt': v_opt}
                    explanation = f"Эрланг C: перебор v до p_wait ≤ {p_target}."
                elif model == 'batch':
                    k = int(form.k.data or 1)
                    v_opt = calculator.batch_inv_v_p(a, k, p_target)
                    result = {'v_opt': v_opt}
                    explanation = f"Групповое поступление: перебор v до p ≤ {p_target}."
            elif task == 'inverse_m':
                a = float(form.a.data or 0)
                m_target = float(form.m_target.data or 0)
                if model == 'erlang':
                    v_opt = calculator.erlang_b_inv_v_m(a, m_target)
                    result = {'v_opt': v_opt}
                    explanation = f"Подбор числа каналов v методом перебора до m ≥ {m_target}."
                elif model == 'engset':
                    N = int(form.N.data or 1)
                    v_opt = calculator.engset_inv_v_m(a, N, m_target)
                    result = {'v_opt': v_opt}
                    explanation = f"Модель Энгсета: перебор v до m ≥ {m_target}."
                elif model == 'batch':
                    k = int(form.k.data or 1)
                    v_opt = calculator.batch_inv_v_m(a, k, m_target)
                    result = {'v_opt': v_opt}
                    explanation = f"Групповое поступление: перебор v до m ≥ {m_target}."
                else:
                    result = {'error': 'Для модели Эрланг C задача не имеет смысла (m всегда = a)'}
            elif task == 'overload':
                v = int(form.v.data or 0)
                p_measured = float(form.p_measured.data or 0)
                p_norm = float(form.p_norm.data or 0.01)
                if model == 'erlang':
                    reduction = calculator.erlang_b_overload(v, p_measured, p_norm)
                    result = {'reduction_percent': round(reduction, 2)}
                    explanation = f"Поиск нагрузок a* и a_норм через перебор, затем доля выгрузки = (a*-a_норм)/a*."
                elif model == 'engset':
                    N = int(form.N.data or 1)
                    reduction = calculator.engset_overload(v, N, p_measured, p_norm)
                    result = {'reduction_percent': round(reduction, 2)}
                    explanation = f"Модель Энгсета: аналогичный метод перебора нагрузок."
                elif model == 'erlang_c':
                    reduction = calculator.erlang_c_overload(v, p_measured, p_norm)
                    result = {'reduction_percent': round(reduction, 2)}
                    explanation = f"Эрланг C: перебор нагрузок для заданных вероятностей ожидания."
                elif model == 'batch':
                    k = int(form.k.data or 1)
                    reduction = calculator.batch_overload(v, k, p_measured, p_norm)
                    result = {'reduction_percent': round(reduction, 2)}
                    explanation = f"Групповое поступление: перебор нагрузок."
            if result and 'error' not in result:
                readable = format_readable(result)
        except Exception as e:
            result = {'error': str(e)}
            explanation = "Произошла ошибка при расчёте."
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(readable=readable, explanation=explanation)
    return render_template('index.html', form=form, readable=readable, explanation=explanation)