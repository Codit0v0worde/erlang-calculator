from flask import Blueprint, render_template, request, jsonify, session
from app.forms import CalculatorForm
from app import calculator
import json

main_bp = Blueprint('main', __name__)

def format_readable(result):
    lines = []
    for key, value in result.items():
        if key == 'p':
            lines.append(f"Вероятность блокировки: {value:.6f}")
        elif key == 'p_wait':
            lines.append(f"Вероятность ожидания: {value:.6f}")
        elif key == 'p_ab':
            lines.append(f"Вероятность ухода из очереди: {value:.6f}")
        elif key == 'm':
            lines.append(f"Среднее число занятых каналов: {value:.4f}")
        elif key == 'v_opt':
            lines.append(f"Необходимое число каналов: {value}")
        elif key == 'reduction_percent':
            lines.append(f"Доля выгружаемой нагрузки: {value:.2f}%")
        elif key == 'message':
            lines.append(f"{value}")
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
        
        params_for_graph = {
            'model': model,
            'task': task,
            'a': float(form.a.data or 5),
            'v': int(form.v.data or 15),
            'N': int(form.N.data) if form.N.data else 20,
            'k': int(form.k.data) if form.k.data else 2,
            'theta': float(form.theta.data) if form.theta.data else 0.1,
            'p_target': float(form.p_target.data) if form.p_target.data else None,
            'm_target': float(form.m_target.data) if form.m_target.data else None,
            'p_measured': float(form.p_measured.data) if form.p_measured.data else None,
            'p_norm': float(form.p_norm.data) if form.p_norm.data else None
        }
        session['graph_params'] = params_for_graph
        
        try:
            # ========== ПРЯМАЯ ЗАДАЧА ==========
            if task == 'direct':
                a = float(form.a.data or 0)
                v = int(form.v.data or 0)
                
                if model == 'erlang':
                    p = calculator.erlang_b(v, a)
                    m = a * (1 - p)
                    result = {'p': round(p, 6), 'm': round(m, 4)}
                    explanation = (
                        f"Формула Эрланга B: p = E(v,a).\n\n"
                        f"При нагрузке a = {a} Эрл и v = {v} каналах:\n"
                        f"• Вероятность блокировки p = {round(p, 6)} ({round(p*100, 2)}% вызовов получат отказ)\n"
                        f"• Среднее число занятых каналов m = a·(1-p) = {a}·(1-{round(p, 4)}) = {round(m, 4)}"
                    )
                
                elif model == 'engset':
                    N = int(form.N.data or 1)
                    p = calculator.engset_b(v, a, N)
                    p_states = [1.0]
                    for i in range(1, v+1):
                        p_states.append(p_states[-1] * (N - i + 1) * a / i)
                    sum_p = sum(p_states)
                    m = sum(i * p_states[i] for i in range(v+1)) / sum_p
                    result = {'p': round(p, 6), 'm': round(m, 4)}
                    explanation = (
                        f"Модель Энгсета (конечное число источников N = {N}).\n\n"
                        f"При нагрузке a = {a} Эрл/источник и v = {v} каналах:\n"
                        f"• Вероятность блокировки p = {round(p, 6)}\n"
                        f"• Среднее число занятых каналов m = {round(m, 4)}"
                    )
                
                elif model == 'erlang_c':
                    p = calculator.erlang_c(v, a)
                    m = a
                    result = {'p_wait': round(p, 6), 'm': round(m, 4)}
                    explanation = (
                        f"Формула Эрланга C (система с ожиданием).\n\n"
                        f"При нагрузке a = {a} Эрл и v = {v} каналах:\n"
                        f"• Вероятность ожидания p_wait = {round(p, 6)} ({round(p*100, 2)}% вызовов попадут в очередь)\n"
                        f"• Среднее число занятых каналов m = a = {a} (все вызовы будут обслужены)"
                    )
                
                elif model == 'erlang_a':
                    theta = float(form.theta.data or 0.1)
                    res = calculator.erlang_a(v, a, theta)
                    result = res
                    explanation = (
                        f"Модель Эрланга А (с уходами из очереди, θ = {theta}).\n\n"
                        f"При нагрузке a = {a} Эрл и v = {v} каналах:\n"
                        f"• Вероятность ожидания p_wait = {res['p_wait']}\n"
                        f"• Вероятность ухода из очереди p_ab = {res['p_ab']}\n"
                        f"• Среднее число занятых каналов m = {res['m']}"
                    )
                
                elif model == 'batch':
                    k = int(form.k.data or 1)
                    p = calculator.batch_erlang_b(v, a, k)
                    m = a * k * (1 - p)
                    result = {'p': round(p, 6), 'm': round(m, 4)}
                    explanation = (
                        f"Модель с групповым поступлением (размер группы k = {k}).\n"
                        f"Эквивалентная нагрузка = a·k = {a}·{k} = {a*k} Эрл.\n\n"
                        f"При v = {v} каналах:\n"
                        f"• Вероятность блокировки p = {round(p, 6)}\n"
                        f"• Среднее число занятых каналов m = {round(m, 4)}"
                    )
            
            # ========== ОБРАТНАЯ ЗАДАЧА 1 (v по p) ==========
            elif task == 'inverse_p':
                a = float(form.a.data or 0)
                p_target = float(form.p_target.data or 0.01)
                
                if model == 'erlang':
                    v_opt = calculator.erlang_b_inv_v_p(a, p_target)
                    p_actual = calculator.erlang_b(v_opt, a)
                    result = {'v_opt': v_opt}
                    explanation = (
                        f"Подбор числа каналов v для нагрузки a = {a} Эрл.\n"
                        f"Требуется p ≤ {p_target} ({p_target*100}%).\n\n"
                        f"• При v = {v_opt}: p = {round(p_actual, 6)} ≤ {p_target} ✓\n"
                        f"• При v = {v_opt-1}: p = {round(calculator.erlang_b(v_opt-1, a), 6)} > {p_target}"
                    )
                
                elif model == 'engset':
                    N = int(form.N.data or 1)
                    v_opt = calculator.engset_inv_v_p(a, N, p_target)
                    p_actual = calculator.engset_b(v_opt, a, N)
                    result = {'v_opt': v_opt}
                    explanation = (
                        f"Модель Энгсета: N = {N} источников, a = {a} Эрл/источник.\n"
                        f"Требуется p ≤ {p_target}. Подбор дал v = {v_opt} каналов.\n\n"
                        f"При этом p = {round(p_actual, 6)} ≤ {p_target} ✓"
                    )
                
                elif model == 'erlang_c':
                    v_opt = calculator.erlang_c_inv_v_p(a, p_target)
                    p_actual = calculator.erlang_c(v_opt, a)
                    result = {'v_opt': v_opt}
                    explanation = (
                        f"Эрланг C: нагрузка a = {a} Эрл.\n"
                        f"Требуется p_wait ≤ {p_target}. Подбор дал v = {v_opt} каналов.\n\n"
                        f"При этом p_wait = {round(p_actual, 6)} ≤ {p_target} ✓"
                    )
                
                elif model == 'erlang_a':
                    theta = float(form.theta.data or 0.1)
                    v_opt = calculator.erlang_a_inv_v_p(a, theta, p_target)
                    res = calculator.erlang_a(v_opt, a, theta)
                    result = {'v_opt': v_opt}
                    explanation = (
                        f"Эрланг A: a = {a} Эрл, θ = {theta}.\n"
                        f"Требуется p_wait ≤ {p_target}. Подбор дал v = {v_opt} каналов.\n\n"
                        f"При этом p_wait = {res['p_wait']} ≤ {p_target} ✓"
                    )
                
                elif model == 'batch':
                    k = int(form.k.data or 1)
                    v_opt = calculator.batch_inv_v_p(a, k, p_target)
                    p_actual = calculator.batch_erlang_b(v_opt, a, k)
                    result = {'v_opt': v_opt}
                    explanation = (
                        f"Групповое поступление: a = {a} Эрл, k = {k}.\n"
                        f"Эквивалентная нагрузка = {a*k} Эрл.\n"
                        f"Требуется p ≤ {p_target}. Подбор дал v = {v_opt} каналов.\n\n"
                        f"При этом p = {round(p_actual, 6)} ≤ {p_target} ✓"
                    )
            
            # ========== ОБРАТНАЯ ЗАДАЧА 2 (v по m) ==========
            elif task == 'inverse_m':
                a = float(form.a.data or 0)
                m_target = float(form.m_target.data or 0)
                
                if model == 'erlang':
                    v_opt = calculator.erlang_b_inv_v_m(a, m_target)
                    p = calculator.erlang_b(v_opt, a)
                    m_actual = a * (1 - p)
                    result = {'v_opt': v_opt}
                    explanation = (
                        f"Подбор v для нагрузки a = {a} Эрл.\n"
                        f"Требуется m ≥ {m_target}.\n\n"
                        f"• При v = {v_opt}: m = {a}·(1-{round(p, 4)}) = {round(m_actual, 4)} ≥ {m_target} ✓\n"
                        f"• При v = {v_opt-1}: m = {round(a * (1 - calculator.erlang_b(v_opt-1, a)), 4)} < {m_target}"
                    )
                
                elif model == 'engset':
                    N = int(form.N.data or 1)
                    v_opt = calculator.engset_inv_v_m(a, N, m_target)
                    result = {'v_opt': v_opt}
                    explanation = (
                        f"Модель Энгсета: N = {N}, a = {a} Эрл/источник.\n"
                        f"Требуется m ≥ {m_target}. Подбор дал v = {v_opt} каналов."
                    )
                
                elif model == 'erlang_c':
                    if m_target <= a:
                        min_v = int(a) + 1
                        result = {'v_opt': f'≥ {min_v}'}
                        explanation = (
                            f"В модели Эрланг C среднее число занятых каналов m всегда равно нагрузке a = {a}.\n\n"
                            f"Так как m_target = {m_target} ≤ {a}, условие m ≥ {m_target} выполняется для любого v > a.\n"
                            f"Минимальное число каналов: v = {min_v}."
                        )
                    else:
                        result = {'error': f'Невозможно достичь m = {m_target}'}
                        explanation = (
                            f"В модели Эрланг C m всегда равно a = {a}.\n"
                            f"Нельзя получить m = {m_target} > {a}."
                        )
                
                elif model == 'erlang_a':
                    theta = float(form.theta.data or 0.1)
                    v_opt = calculator.erlang_a_inv_v_m(a, theta, m_target)
                    res = calculator.erlang_a(v_opt, a, theta)
                    result = {'v_opt': v_opt}
                    explanation = (
                        f"Эрланг A: a = {a} Эрл, θ = {theta}.\n"
                        f"Требуется m ≥ {m_target}. Подбор дал v = {v_opt} каналов.\n\n"
                        f"При этом m = {res['m']} ≥ {m_target} ✓"
                    )
                
                elif model == 'batch':
                    k = int(form.k.data or 1)
                    v_opt = calculator.batch_inv_v_m(a, k, m_target)
                    p = calculator.batch_erlang_b(v_opt, a, k)
                    m_actual = a * k * (1 - p)
                    result = {'v_opt': v_opt}
                    explanation = (
                        f"Групповое поступление: a = {a} Эрл, k = {k}.\n"
                        f"Эквивалентная нагрузка = {a*k} Эрл.\n"
                        f"Требуется m ≥ {m_target}. Подбор дал v = {v_opt} каналов.\n\n"
                        f"При этом m = {round(m_actual, 4)} ≥ {m_target} ✓"
                    )
            
            # ========== ОБРАТНАЯ ЗАДАЧА 3 (доля выгрузки) ==========
            elif task == 'overload':
                v = int(form.v.data or 0)
                p_measured = float(form.p_measured.data or 0)
                p_norm = float(form.p_norm.data or 0.01)
                
                if model == 'erlang':
                    a_meas = calculator.find_a_erlang_b(v, p_measured)
                    a_norm = calculator.find_a_erlang_b(v, p_norm)
                    reduction = ((a_meas - a_norm) / a_meas * 100) if a_meas > 0 else 0
                    result = {'reduction_percent': round(reduction, 2)}
                    explanation = (
                        f"При v = {v} каналах:\n\n"
                        f"• Измеренная p* = {p_measured} соответствует нагрузке a* = {round(a_meas, 2)} Эрл\n"
                        f"• Нормативная p = {p_norm} соответствует нагрузке a_норм = {round(a_norm, 2)} Эрл\n\n"
                        f"Чтобы снизить потери с {p_measured} до {p_norm}, нужно выгрузить:\n"
                        f"({round(a_meas, 2)} - {round(a_norm, 2)}) / {round(a_meas, 2)} = {round(reduction, 2)}% трафика"
                    )
                
                elif model == 'engset':
                    N = int(form.N.data or 1)
                    a_meas = calculator.find_a_engset(v, N, p_measured)
                    a_norm = calculator.find_a_engset(v, N, p_norm)
                    reduction = ((a_meas - a_norm) / a_meas * 100) if a_meas > 0 else 0
                    result = {'reduction_percent': round(reduction, 2)}
                    explanation = (
                        f"Модель Энгсета: v = {v} каналов, N = {N} источников.\n\n"
                        f"• p* = {p_measured} → a* = {round(a_meas, 4)} Эрл/источник\n"
                        f"• p = {p_norm} → a_норм = {round(a_norm, 4)} Эрл/источник\n\n"
                        f"Доля выгрузки = {round(reduction, 2)}%"
                    )
                
                elif model == 'erlang_c':
                    a_meas = calculator.find_a_erlang_c(v, p_measured)
                    a_norm = calculator.find_a_erlang_c(v, p_norm)
                    reduction = ((a_meas - a_norm) / a_meas * 100) if a_meas > 0 else 0
                    result = {'reduction_percent': round(reduction, 2)}
                    explanation = (
                        f"Эрланг C (с очередью): v = {v} каналов.\n\n"
                        f"• p*_wait = {p_measured} → a* = {round(a_meas, 2)} Эрл\n"
                        f"• p_wait = {p_norm} → a_норм = {round(a_norm, 2)} Эрл\n\n"
                        f"Доля выгрузки = {round(reduction, 2)}%"
                    )
                
                elif model == 'erlang_a':
                    theta = float(form.theta.data or 0.1)
                    a_meas = calculator.find_a_erlang_a(v, theta, p_measured)
                    a_norm = calculator.find_a_erlang_a(v, theta, p_norm)
                    reduction = ((a_meas - a_norm) / a_meas * 100) if a_meas > 0 else 0
                    result = {'reduction_percent': round(reduction, 2)}
                    explanation = (
                        f"Эрланг A: v = {v} каналов, θ = {theta}.\n\n"
                        f"• p* = {p_measured} → a* = {round(a_meas, 2)} Эрл\n"
                        f"• p = {p_norm} → a_норм = {round(a_norm, 2)} Эрл\n\n"
                        f"Доля выгрузки = {round(reduction, 2)}%"
                    )
                
                elif model == 'batch':
                    k = int(form.k.data or 1)
                    a_meas = calculator.find_a_batch(v, k, p_measured)
                    a_norm = calculator.find_a_batch(v, k, p_norm)
                    reduction = ((a_meas - a_norm) / a_meas * 100) if a_meas > 0 else 0
                    result = {'reduction_percent': round(reduction, 2)}
                    explanation = (
                        f"Групповое поступление: v = {v} каналов, k = {k}.\n\n"
                        f"• p* = {p_measured} → a* = {round(a_meas, 2)} Эрл\n"
                        f"• p = {p_norm} → a_норм = {round(a_norm, 2)} Эрл\n\n"
                        f"Доля выгрузки = {round(reduction, 2)}%"
                    )
            
            if result and 'error' not in result:
                readable = format_readable(result)
            elif result and 'error' in result:
                readable = f"Ошибка: {result['error']}"
                
        except Exception as e:
            result = {'error': str(e)}
            explanation = f"Произошла ошибка при расчёте: {str(e)}"
            readable = f"Ошибка: {str(e)}"
            
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(readable=readable, explanation=explanation)
    
    return render_template('index.html', form=form, readable=readable, explanation=explanation)


@main_bp.route('/graph')
def graph():
    params = session.get('graph_params', {})
    if not params:
        return "Нет данных для графика. Выполните расчёт сначала.", 400
    
    model = params.get('model', 'erlang')
    task = params.get('task', 'direct')
    a = params.get('a', 5)
    v = params.get('v', 15)
    N = params.get('N', 20)
    k = params.get('k', 2)
    theta = params.get('theta', 0.1)
    p_target = params.get('p_target')
    m_target = params.get('m_target')
    
    if task in ['inverse_p', 'inverse_m']:
        max_v = v + 20
    else:
        max_v = v + 15
    
    if model == 'engset':
        graph_data = calculator.get_graph_data(model, a, max_v, N=N, k=None, theta=None)
    elif model == 'erlang_a':
        graph_data = calculator.get_graph_data(model, a, max_v, N=None, k=None, theta=theta)
    elif model == 'batch':
        graph_data = calculator.get_graph_data(model, a, max_v, N=None, k=k, theta=None)
    else:
        graph_data = calculator.get_graph_data(model, a, max_v, N=None, k=None, theta=None)
    
    model_names = {
        'erlang': 'Эрланг B',
        'engset': f'Энгсет (N={N})',
        'erlang_c': 'Эрланг C',
        'erlang_a': f'Эрланг A (θ={theta})',
        'batch': f'Групповое поступление (k={k})'
    }
    
    task_names = {
        'direct': 'Прямая задача',
        'inverse_p': f'Обратная задача: подбор v по p = {p_target}',
        'inverse_m': f'Обратная задача: подбор v по m = {m_target}',
        'overload': 'Обратная задача: доля выгрузки'
    }
    
    return render_template('graph.html', 
                          graph_data=json.dumps(graph_data),
                          model=model_names.get(model, model),
                          task=task_names.get(task, ''),
                          a=a,
                          v=v,
                          is_inverse=(task in ['inverse_p', 'inverse_m']))


@main_bp.route('/compare')
def compare():
    params = session.get('graph_params', {})
    a = params.get('a', 5)
    v = params.get('v', 15)
    N = params.get('N', 20)
    k = params.get('k', 2)
    theta = params.get('theta', 0.1)
    
    models = ['erlang', 'engset', 'erlang_c', 'erlang_a', 'batch']
    model_names = {
        'erlang': 'Эрланг B (блокировка)',
        'engset': f'Энгсет (N={N})',
        'erlang_c': 'Эрланг C (ожидание)',
        'erlang_a': f'Эрланг A (θ={theta})',
        'batch': f'Групповое (k={k})'
    }
    
    compare_data = {}
    max_v = v + 20
    
    for model in models:
        if model == 'engset':
            data = calculator.get_graph_data(model, a, max_v, N=N, k=None, theta=None)
        elif model == 'erlang_a':
            data = calculator.get_graph_data(model, a, max_v, N=None, k=None, theta=theta)
        elif model == 'batch':
            data = calculator.get_graph_data(model, a, max_v, N=None, k=k, theta=None)
        else:
            data = calculator.get_graph_data(model, a, max_v, N=None, k=None, theta=None)
        
        compare_data[model] = {
            'name': model_names[model],
            'v': data['v'],
            'p': data['p']
        }
    
    return render_template('compare.html', 
                          compare_data=json.dumps(compare_data),
                          a=a, N=N, k=k, theta=theta)