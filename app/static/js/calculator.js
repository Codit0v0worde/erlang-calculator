document.addEventListener('DOMContentLoaded', function() {
    const modelSelect = document.getElementById('model');
    const taskSelect = document.getElementById('task');
    const inputFieldsDiv = document.getElementById('input-fields');
    const form = document.getElementById('calc-form');
    const resultDiv = document.getElementById('result');

    function updateFields() {
        const model = modelSelect.value;
        const task = taskSelect.value;
        console.log('Updating fields for model:', model, 'task:', task);
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
            if (model === 'reservation') {
                html += '<div><label>Нагрузка высокого приоритета a_high:</label> <input type="number" step="0.01" name="a_high" required></div>';
                html += '<div><label>Нагрузка низкого приоритета a_low:</label> <input type="number" step="0.01" name="a_low" required></div>';
                html += '<div><label>Число каналов v:</label> <input type="number" name="v" required></div>';
                html += '<div><label>Число резервных каналов r (если известно, иначе 0):</label> <input type="number" name="r" value="0"></div>';
            }
        } else if (task === 'inverse_p') {
            // аналогично...
        }
        // ... остальные задачи без изменений

        inputFieldsDiv.innerHTML = html;
    }

    modelSelect.addEventListener('change', updateFields);
    taskSelect.addEventListener('change', updateFields);
    updateFields();  // инициализация при загрузке

    // AJAX отправка формы
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
            if (data.result) {
                resultDiv.innerHTML = `<h2>Результат:</h2><pre>${JSON.stringify(data.result, null, 2)}</pre>`;
            } else {
                resultDiv.innerHTML = `<h2>Ошибка:</h2><pre>Нет данных</pre>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<h2>Ошибка:</h2><pre>${error}</pre>`;
        });
    });
});