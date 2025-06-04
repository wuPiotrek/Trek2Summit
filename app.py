from flask import Flask, render_template_string, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Stan przycisków (początkowo wszystkie wyłączone)
button_states = {
    'dobrze': False,
    'tanio': False,
    'szybko': False
}
# Kolejność aktywacji przycisków
active_order = []

# Konfiguracja połączenia z MSSQL (zgodnie z main.tf)
MSSQL_SERVER = 'piotrw-webapp-t2s-workshop-db.database.windows.net'
MSSQL_DATABASE = 'piotrw-db'
MSSQL_USERNAME = '4dm1n157r470r'
MSSQL_PASSWORD = '4-v3ry-53cr37-p455w0rd'
MSSQL_DRIVER = '{ODBC Driver 17 for SQL Server}'

def get_db_conn():
    return pyodbc.connect(
        f'DRIVER={MSSQL_DRIVER};SERVER={MSSQL_SERVER};DATABASE={MSSQL_DATABASE};UID={MSSQL_USERNAME};PWD={MSSQL_PASSWORD}'
    )

def init_db():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='todo' AND xtype='U')
        CREATE TABLE todo (
            id INT IDENTITY(1,1) PRIMARY KEY,
            text NVARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_todos():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM todo ORDER BY id DESC")
    todos = cursor.fetchall()
    conn.close()
    return todos

def add_todo(text):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todo (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

def delete_todo(todo_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()

@app.before_first_request
def setup():
    init_db()

@app.route('/', methods=['GET', 'POST'])
def home():
    global button_states, active_order
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
                add_todo(todo_text)
            return redirect(url_for('home'))
        elif 'delete_todo' in request.form:
            todo_id = int(request.form.get('delete_todo'))
            delete_todo(todo_id)
            return redirect(url_for('home'))
    # Kolory i etykiety przycisków (wszystkie niebieskie)
    buttons = [
        {'name': 'dobrze', 'label': 'DOBRZE', 'color': 'blue'},
        {'name': 'tanio', 'label': 'TANIO', 'color': 'blue'},
        {'name': 'szybko', 'label': 'SZYBKO', 'color': 'blue'}
    ]
    todos = get_todos()
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
                    {{todo[1]}}
                    <form method="post" style="display:inline">
                        <button class="del-btn" name="delete_todo" value="{{todo[0]}}">Usuń</button>
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