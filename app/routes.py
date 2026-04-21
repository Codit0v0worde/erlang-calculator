from flask import Blueprint, render_template, request, jsonify
from app.forms import CalculatorForm
from app import calculator

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = CalculatorForm()
    result = None
    if form.validate_on_submit():
        model = form.model.data
        task = form.task.data
        try:
            # Прямая задача
            if task == 'direct':
                a = float(form.a.data or 0)
                v = int(form.v.data or 0)
                if model == 'erlang':
                    p = calculator.erlang_b(v, a)
                    m = a * (1 - p)
                    result = {'p': round(p, 6), 'm': round(m, 4)}
                elif model == 'engset':
                    N = int(form.N.data or 1)
                    p = calculator.engset_b(v, a, N)
                    # Вычисляем точное m
                    p_states = [1.0]
                    for i in range(1, v + 1):
                        p_states.append(p_states[-1] * (N - i + 1) * a / i)
                    sum_p = sum(p_states)
                    m = sum(i * p_states[i] for i in range(v + 1)) / sum_p
                    result = {'p': round(p, 6), 'm': round(m, 4)}
                elif model == 'erlang_c':
                    p = calculator.erlang_c(v, a)
                    m = a  # нет потерь
                    result = {'p_wait': round(p, 6), 'm': round(m, 4)}
                elif model == 'batch':
                    k = int(form.k.data or 1)
                    p = calculator.batch_erlang_b(v, a, k)
                    m = a * k * (1 - p)
                    result = {'p': round(p, 6), 'm': round(m, 4)}
                elif model == 'reservation':
                    # Прямая задача для резервирования: вычисляем вероятности при заданных v и r
                    a_high = float(form.a_high.data or 0)
                    a_low = float(form.a_low.data or 0)
                    # r не вводится в прямой задаче, но можно добавить поле или считать r=0
                    r = 0
                    p_high = calculator.erlang_b(v - r, a_high) if (v - r) > 0 else 1.0
                    p_low = calculator.erlang_b(v, a_high + a_low)
                    result = {'p_high': round(p_high, 6), 'p_low': round(p_low, 6)}
            # Обратная задача 1 (v по p)
            elif task == 'inverse_p':
                a = float(form.a.data or 0)
                p_target = float(form.p_target.data or 0.01)
                if model == 'erlang':
                    v_opt = calculator.erlang_b_inv_v_p(a, p_target)
                    result = {'v_opt': v_opt}
                elif model == 'engset':
                    N = int(form.N.data or 1)
                    v_opt = calculator.engset_inv_v_p(a, N, p_target)
                    result = {'v_opt': v_opt}
                elif model == 'erlang_c':
                    v_opt = calculator.erlang_c_inv_v_p(a, p_target)
                    result = {'v_opt': v_opt}
                elif model == 'batch':
                    k = int(form.k.data or 1)
                    v_opt = calculator.batch_inv_v_p(a, k, p_target)
                    result = {'v_opt': v_opt}
                else:
                    result = {'error': 'Для выбранной модели задача не реализована'}
            # Обратная задача 2 (v по m)
            elif task == 'inverse_m':
                a = float(form.a.data or 0)
                m_target = float(form.m_target.data or 0)
                if model == 'erlang':
                    v_opt = calculator.erlang_b_inv_v_m(a, m_target)
                    result = {'v_opt': v_opt}
                elif model == 'engset':
                    N = int(form.N.data or 1)
                    v_opt = calculator.engset_inv_v_m(a, N, m_target)
                    result = {'v_opt': v_opt}
                elif model == 'batch':
                    k = int(form.k.data or 1)
                    v_opt = calculator.batch_inv_v_m(a, k, m_target)
                    result = {'v_opt': v_opt}
                else:
                    result = {'error': 'Для выбранной модели задача не реализована'}
            # Обратная задача 3 (доля выгрузки)
            elif task == 'overload':
                v = int(form.v.data or 0)
                p_measured = float(form.p_measured.data or 0)
                p_norm = float(form.p_norm.data or 0.01)
                if model == 'erlang':
                    reduction = calculator.erlang_b_overload(v, p_measured, p_norm)
                    result = {'reduction_percent': round(reduction, 2)}
                elif model == 'engset':
                    N = int(form.N.data or 1)
                    reduction = calculator.engset_overload(v, N, p_measured, p_norm)
                    result = {'reduction_percent': round(reduction, 2)}
                elif model == 'erlang_c':
                    reduction = calculator.erlang_c_overload(v, p_measured, p_norm)
                    result = {'reduction_percent': round(reduction, 2)}
                elif model == 'batch':
                    k = int(form.k.data or 1)
                    reduction = calculator.batch_overload(v, k, p_measured, p_norm)
                    result = {'reduction_percent': round(reduction, 2)}
                else:
                    result = {'error': 'Для выбранной модели задача не реализована'}
            # Задача для резервирования
            elif task == 'reservation':
                a_high = float(form.a_high.data or 0)
                a_low = float(form.a_low.data or 0)
                p_high_target = float(form.p_high_target.data or 0.01)
                p_low_target = float(form.p_low_target.data or 0.01)
                v_opt, r_opt = calculator.reservation_find_v_r(a_high, a_low, p_high_target, p_low_target)
                if v_opt is not None:
                    result = {'v': v_opt, 'r': r_opt}
                else:
                    result = {'error': 'Решение не найдено в пределах max_v=100'}
        except Exception as e:
            result = {'error': str(e)}

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(result=result)

    return render_template('index.html', form=form, result=result)