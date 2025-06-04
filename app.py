from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Stan przycisków (początkowo wszystkie wyłączone)
button_states = {
    'dobrze': False,
    'tanio': False,
    'szybko': False
}
# Kolejność aktywacji przycisków
active_order = []

# Prosta lista TODO w pamięci
todos = []

@app.route('/', methods=['GET', 'POST'])
def home():
    global button_states, active_order, todos
    if request.method == 'POST':
        if 'button' in request.form:
            btn = request.form.get('button')
            if button_states[btn]:
                # Odkliknięcie przycisku
                button_states[btn] = False
                if btn in active_order:
                    active_order.remove(btn)
            else:
                # Kliknięcie nowego przycisku
                if sum(button_states.values()) < 2:
                    button_states[btn] = True
                    active_order.append(btn)
                else:
                    # Odkliknij najstarszy, kliknij nowy
                    oldest = active_order.pop(0)
                    button_states[oldest] = False
                    button_states[btn] = True
                    active_order.append(btn)
            return redirect(url_for('home'))
        elif 'todo_text' in request.form:
            todo_text = request.form.get('todo_text', '').strip()
            if todo_text:
                todos.append(todo_text)
            return redirect(url_for('home'))
        elif 'delete_todo' in request.form:
            idx = int(request.form.get('delete_todo'))
            if 0 <= idx < len(todos):
                todos.pop(idx)
            return redirect(url_for('home'))
    # Kolory i etykiety przycisków (wszystkie niebieskie)
    buttons = [
        {'name': 'dobrze', 'label': 'DOBRZE', 'color': 'blue'},
        {'name': 'tanio', 'label': 'TANIO', 'color': 'blue'},
        {'name': 'szybko', 'label': 'SZYBKO', 'color': 'blue'}
    ]
    # Renderowanie strony
    return render_template_string('''
    <html>
    <head>
        <title>Wybierz opcje</title>
        <style>
            .btn {
                width: 120px; height: 60px; font-size: 1.5em; margin: 10px;
                border: none; border-radius: 8px; color: white; cursor: pointer;
            }
            .active { box-shadow: 0 0 10px 2px #333; }
            .blue { background: #2980b9; }
            .todo-form { margin-top: 30px; }
            .todo-list { margin-top: 10px; }
            .todo-item { margin-bottom: 8px; }
            .del-btn { background: #c0392b; color: white; border: none; border-radius: 4px; cursor: pointer; }
        </style>
    </head>
    <body>
        <form method="post">
            {% for btn in buttons %}
                <button name="button" value="{{btn.name}}"
                    class="btn {{btn.color}} {% if states[btn.name] %}active{% endif %}">
                    {{btn.label}}
                </button>
            {% endfor %}
        </form>
        <div class="todo-form">
            <form method="post">
                <input type="text" name="todo_text" placeholder="Dodaj zadanie" required>
                <button type="submit">Dodaj</button>
            </form>
        </div>
        <div class="todo-list">
            <ul>
                {% for todo in todos %}
                <li class="todo-item">
                    {{todo}}
                    <form method="post" style="display:inline">
                        <button class="del-btn" name="delete_todo" value="{{loop.index0}}">Usuń</button>
                    </form>
                </li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    ''', buttons=buttons, states=button_states, todos=todos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)