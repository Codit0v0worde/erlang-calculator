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
            if (model === 'erlang' || model === 'engset' || model === 'erlang_c' || model === 'batch') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" required></div>';
                html += '<div><label>Число каналов v:</label> <input type="number" name="v" required></div>';
            }
            if (model === 'engset') {
                html += '<div><label>Число источников N:</label> <input type="number" name="N" required></div>';
            }
            if (model === 'batch') {
                html += '<div><label>Размер группы k:</label> <input type="number" name="k" required></div>';
            }
        }
        else if (task === 'inverse_p') {
            if (model === 'erlang' || model === 'erlang_c') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" required></div>';
                html += '<div><label>Целевая вероятность p:</label> <input type="number" step="0.0001" name="p_target" required></div>';
            }
            else if (model === 'engset') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" required></div>';
                html += '<div><label>Число источников N:</label> <input type="number" name="N" required></div>';
                html += '<div><label>Целевая вероятность p:</label> <input type="number" step="0.0001" name="p_target" required></div>';
            }
            else if (model === 'batch') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" required></div>';
                html += '<div><label>Размер группы k:</label> <input type="number" name="k" required></div>';
                html += '<div><label>Целевая вероятность p:</label> <input type="number" step="0.0001" name="p_target" required></div>';
            }
        }
        else if (task === 'inverse_m') {
            if (model === 'erlang' || model === 'erlang_c') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" required></div>';
                html += '<div><label>Целевое среднее m:</label> <input type="number" step="0.1" name="m_target" required></div>';
            }
            else if (model === 'engset') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" required></div>';
                html += '<div><label>Число источников N:</label> <input type="number" name="N" required></div>';
                html += '<div><label>Целевое среднее m:</label> <input type="number" step="0.1" name="m_target" required></div>';
            }
            else if (model === 'batch') {
                html += '<div><label>Нагрузка a (Эрл):</label> <input type="number" step="0.01" name="a" required></div>';
                html += '<div><label>Размер группы k:</label> <input type="number" name="k" required></div>';
                html += '<div><label>Целевое среднее m:</label> <input type="number" step="0.1" name="m_target" required></div>';
            }
        }
        else if (task === 'overload') {
            if (model === 'erlang' || model === 'erlang_c') {
                html += '<div><label>Число каналов v:</label> <input type="number" name="v" required></div>';
                html += '<div><label>Измеренная p*:</label> <input type="number" step="0.0001" name="p_measured" required></div>';
                html += '<div><label>Нормативная p:</label> <input type="number" step="0.0001" name="p_norm" required></div>';
            }
            else if (model === 'engset') {
                html += '<div><label>Число каналов v:</label> <input type="number" name="v" required></div>';
                html += '<div><label>Число источников N:</label> <input type="number" name="N" required></div>';
                html += '<div><label>Измеренная p*:</label> <input type="number" step="0.0001" name="p_measured" required></div>';
                html += '<div><label>Нормативная p:</label> <input type="number" step="0.0001" name="p_norm" required></div>';
            }
            else if (model === 'batch') {
                html += '<div><label>Число каналов v:</label> <input type="number" name="v" required></div>';
                html += '<div><label>Размер группы k:</label> <input type="number" name="k" required></div>';
                html += '<div><label>Измеренная p*:</label> <input type="number" step="0.0001" name="p_measured" required></div>';
                html += '<div><label>Нормативная p:</label> <input type="number" step="0.0001" name="p_norm" required></div>';
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
                html += `<div class="result-readable">${data.readable}</div>`;
                html += `<div class="explanation">${data.explanation}</div>`;
            }
            resultDiv.innerHTML = html;
        })
        .catch(error => {
            resultDiv.innerHTML = `<div class="result-error">Ошибка соединения: ${error}</div>`;
        });
    });
});