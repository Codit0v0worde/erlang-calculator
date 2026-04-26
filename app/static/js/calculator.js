document.addEventListener('DOMContentLoaded', function() {
    const modelSelect = document.getElementById('model');
    const taskSelect = document.getElementById('task');
    const inputFieldsDiv = document.getElementById('input-fields');
    const form = document.getElementById('calc-form');
    const resultDiv = document.getElementById('result');

    function updateFields() {
        const model = modelSelect.value;
        const task = taskSelect.value;
        let html = '';

        if (task === 'direct') {
            if (model === 'erlang' || model === 'engset' || model === 'erlang_c' || model === 'erlang_a' || model === 'batch' || model === 'reservation') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" placeholder="например: 5" required></div>';
                html += '<div><label>Число каналов v:</label> <input type="number" name="v" placeholder="например: 10" required></div>';
            }
            if (model === 'engset') {
                html += '<div><label>Число источников N:</label> <input type="number" name="N" placeholder="например: 20" required></div>';
            }
            if (model === 'erlang_a') {
                html += '<div><label>Интенсивность уходов θ:</label> <input type="number" step="0.01" name="theta" placeholder="например: 0.1" required></div>';
            }
            if (model === 'batch') {
                html += '<div><label>Размер группы k:</label> <input type="number" name="k" placeholder="например: 2" required></div>';
            }
            if (model === 'reservation') {
                html += '<div><label>Резервных каналов r:</label> <input type="number" name="r" placeholder="например: 2" required></div>';
            }
        } else if (task === 'inverse_p') {
            if (model === 'erlang' || model === 'erlang_c') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" placeholder="например: 5" required></div>';
                html += '<div><label>Целевая вероятность p:</label> <input type="number" step="0.0001" name="p_target" placeholder="например: 0.01" required></div>';
            } else if (model === 'engset') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" placeholder="например: 0.1" required></div>';
                html += '<div><label>Число источников N:</label> <input type="number" name="N" placeholder="например: 20" required></div>';
                html += '<div><label>Целевая вероятность p:</label> <input type="number" step="0.0001" name="p_target" placeholder="например: 0.01" required></div>';
            } else if (model === 'erlang_a') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" placeholder="например: 5" required></div>';
                html += '<div><label>Интенсивность уходов θ:</label> <input type="number" step="0.01" name="theta" placeholder="например: 0.1" required></div>';
                html += '<div><label>Целевая вероятность p:</label> <input type="number" step="0.0001" name="p_target" placeholder="например: 0.01" required></div>';
            } else if (model === 'batch') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" placeholder="например: 2" required></div>';
                html += '<div><label>Размер группы k:</label> <input type="number" name="k" placeholder="например: 2" required></div>';
                html += '<div><label>Целевая вероятность p:</label> <input type="number" step="0.0001" name="p_target" placeholder="например: 0.01" required></div>';
            } else if (model === 'reservation') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" placeholder="например: 7" required></div>';
                html += '<div><label>Целевая вероятность p:</label> <input type="number" step="0.0001" name="p_target" placeholder="например: 0.01" required></div>';
            }
        } else if (task === 'inverse_m') {
            if (model === 'erlang' || model === 'erlang_c') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" placeholder="например: 5" required></div>';
                html += '<div><label>Целевое среднее m:</label> <input type="number" step="0.1" name="m_target" placeholder="например: 4.5" required></div>';
            } else if (model === 'engset') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" placeholder="например: 0.1" required></div>';
                html += '<div><label>Число источников N:</label> <input type="number" name="N" placeholder="например: 20" required></div>';
                html += '<div><label>Целевое среднее m:</label> <input type="number" step="0.1" name="m_target" placeholder="например: 2" required></div>';
            } else if (model === 'batch') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" placeholder="например: 2" required></div>';
                html += '<div><label>Размер группы k:</label> <input type="number" name="k" placeholder="например: 2" required></div>';
                html += '<div><label>Целевое среднее m:</label> <input type="number" step="0.1" name="m_target" placeholder="например: 3" required></div>';
            }
        } else if (task === 'overload') {
            if (model === 'erlang' || model === 'erlang_c') {
                html += '<div><label>Число каналов v:</label> <input type="number" name="v" placeholder="например: 10" required></div>';
                html += '<div><label>Измеренная p*:</label> <input type="number" step="0.0001" name="p_measured" placeholder="например: 0.05" required></div>';
                html += '<div><label>Нормативная p:</label> <input type="number" step="0.0001" name="p_norm" placeholder="например: 0.01" required></div>';
            } else if (model === 'engset') {
                html += '<div><label>Число каналов v:</label> <input type="number" name="v" placeholder="например: 5" required></div>';
                html += '<div><label>Число источников N:</label> <input type="number" name="N" placeholder="например: 20" required></div>';
                html += '<div><label>Измеренная p*:</label> <input type="number" step="0.0001" name="p_measured" placeholder="например: 0.05" required></div>';
                html += '<div><label>Нормативная p:</label> <input type="number" step="0.0001" name="p_norm" placeholder="например: 0.01" required></div>';
            } else if (model === 'erlang_a') {
                html += '<div><label>Число каналов v:</label> <input type="number" name="v" placeholder="например: 10" required></div>';
                html += '<div><label>Интенсивность уходов θ:</label> <input type="number" step="0.01" name="theta" placeholder="например: 0.1" required></div>';
                html += '<div><label>Измеренная p*:</label> <input type="number" step="0.0001" name="p_measured" placeholder="например: 0.05" required></div>';
                html += '<div><label>Нормативная p:</label> <input type="number" step="0.0001" name="p_norm" placeholder="например: 0.01" required></div>';
            } else if (model === 'batch') {
                html += '<div><label>Число каналов v:</label> <input type="number" name="v" placeholder="например: 10" required></div>';
                html += '<div><label>Размер группы k:</label> <input type="number" name="k" placeholder="например: 2" required></div>';
                html += '<div><label>Измеренная p*:</label> <input type="number" step="0.0001" name="p_measured" placeholder="например: 0.05" required></div>';
                html += '<div><label>Нормативная p:</label> <input type="number" step="0.0001" name="p_norm" placeholder="например: 0.01" required></div>';
            } else if (model === 'reservation') {
                html += '<div><label>Число каналов v:</label> <input type="number" name="v" placeholder="например: 12" required></div>';
                html += '<div><label>Резервных каналов r:</label> <input type="number" name="r" placeholder="например: 2" required></div>';
                html += '<div><label>Измеренная p*:</label> <input type="number" step="0.0001" name="p_measured" placeholder="например: 0.05" required></div>';
                html += '<div><label>Нормативная p:</label> <input type="number" step="0.0001" name="p_norm" placeholder="например: 0.01" required></div>';
            }
        }
        inputFieldsDiv.innerHTML = html;
    }

    modelSelect.addEventListener('change', updateFields);
    taskSelect.addEventListener('change', updateFields);
    updateFields();

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        fetch('/', {
            method: 'POST',
            headers: {'X-Requested-With': 'XMLHttpRequest'},
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            let html = `<div class="result-header"><i class="fa fa-bar-chart"></i> Результат</div>`;
            if (data.error) {
                html += `<div class="result-error">${data.error}</div>`;
            } else {
                html += `<div class="result-big">${data.readable}</div>`;
                html += `<div class="explanation">${data.explanation.replace(/\n/g, '<br>')}</div>`;
                html += `<div style="margin-top: 20px; display: flex; gap: 10px; justify-content: center;">
                    <button type="button" class="btn-small" onclick="copyResult()">
                        <i class="fa fa-copy"></i> Копировать
                    </button>
                    <a href="/graph" target="_blank" class="btn-small">
                        <i class="fa fa-line-chart"></i> График
                    </a>
                    <a href="/compare" target="_blank" class="btn-small">
                        <i class="fa fa-bar-chart"></i> Сравнить
                    </a>
                </div>`;
            }
            resultDiv.innerHTML = html;
        })
        .catch(error => {
            resultDiv.innerHTML = `<div class="result-error">Ошибка соединения: ${error}</div>`;
        });
    });
});

function copyResult() {
    const resultText = document.querySelector('.result-big')?.innerText || '';
    const explanationText = document.querySelector('.explanation')?.innerText || '';
    const fullText = resultText + '\n\n' + explanationText;
    navigator.clipboard.writeText(fullText).then(() => {
        alert('Результат скопирован в буфер обмена!');
    }).catch(err => {
        alert('Не удалось скопировать');
    });
}

function loadExample(type) {
    const modelSelect = document.getElementById('model');
    const taskSelect = document.getElementById('task');
    const form = document.getElementById('calc-form');
    const resultDiv = document.getElementById('result');

    const examples = {
        'erlang-direct':        { model: 'erlang', task: 'direct', a: 5, v: 10 },
        'erlang-inverse-p':    { model: 'erlang', task: 'inverse_p', a: 10, p_target: 0.01 },
        'erlang-overload':     { model: 'erlang', task: 'overload', v: 10, p_measured: 0.05, p_norm: 0.01 },
        'erlang-overload-noloss': { model: 'erlang', task: 'overload', v: 10, p_measured: 0.008, p_norm: 0.01 },
        'engset-direct':       { model: 'engset', task: 'direct', a: 0.1, v: 5, N: 20 },
        'erlang-c-direct':     { model: 'erlang_c', task: 'direct', a: 8, v: 10 },
        'erlang-a-direct':     { model: 'erlang_a', task: 'direct', a: 5, v: 10, theta: 0.1 },
        'batch-direct':        { model: 'batch', task: 'direct', a: 2, v: 5, k: 2 },
        'reservation-inverse-p': { model: 'reservation', task: 'inverse_p', a: 7, p_target: 0.01 }
    };

    const ex = examples[type];
    if (!ex) return;

    modelSelect.value = ex.model;
    modelSelect.dispatchEvent(new Event('change'));
    taskSelect.value = ex.task;
    taskSelect.dispatchEvent(new Event('change'));

    setTimeout(() => {
        for (const [key, value] of Object.entries(ex)) {
            if (key === 'model' || key === 'task') continue;
            const field = document.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = value;
            }
        }

        const formData = new FormData(form);
        fetch('/', {
            method: 'POST',
            headers: {'X-Requested-With': 'XMLHttpRequest'},
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            let html = `<div class="result-header"><i class="fa fa-bar-chart"></i> Результат</div>`;
            if (data.error) {
                html += `<div class="result-error">${data.error}</div>`;
            } else {
                html += `<div class="result-big">${data.readable}</div>`;
                html += `<div class="explanation">${data.explanation.replace(/\n/g, '<br>')}</div>`;
                html += `<div style="margin-top: 20px; display: flex; gap: 10px; justify-content: center;">
                    <button type="button" class="btn-small" onclick="copyResult()">
                        <i class="fa fa-copy"></i> Копировать
                    </button>
                    <a href="/graph" target="_blank" class="btn-small">
                        <i class="fa fa-line-chart"></i> График
                    </a>
                    <a href="/compare" target="_blank" class="btn-small">
                        <i class="fa fa-bar-chart"></i> Сравнить
                    </a>
                </div>`;
            }
            resultDiv.innerHTML = html;
        })
        .catch(error => {
            resultDiv.innerHTML = `<div class="result-error">Ошибка соединения: ${error}</div>`;
        });
    }, 100);
}

function clearForm() {
    const modelSelect = document.getElementById('model');
    const taskSelect = document.getElementById('task');
    const examplesSelect = document.getElementById('examples');
    const resultDiv = document.getElementById('result');

    // Сброс выпадающих списков
    modelSelect.value = 'erlang';
    modelSelect.dispatchEvent(new Event('change'));
    taskSelect.value = 'direct';
    taskSelect.dispatchEvent(new Event('change'));
    examplesSelect.value = '';

    // Очистка результата
    resultDiv.innerHTML = `<div class="result-placeholder">
        <i class="fa fa-arrow-up"></i> Выберите модель и задачу, введите параметры
    </div>`;
}