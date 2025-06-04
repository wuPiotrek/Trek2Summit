from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Stan przycisków (początkowo wszystkie wyłączone)
button_states = {
    'dobrze': False,
    'tanio': False,
    'szybko': False
}

@app.route('/', methods=['GET', 'POST'])
def home():
    global button_states
    if request.method == 'POST':
        btn = request.form.get('button')
        # Liczba aktualnie włączonych przycisków
        active = sum(button_states.values())
        # Jeśli kliknięty przycisk jest już włączony, wyłącz go
        if button_states[btn]:
            button_states[btn] = False
        # Jeśli kliknięty przycisk jest wyłączony i włączone są mniej niż dwa, włącz go
        elif active < 2:
            button_states[btn] = True
        # W przeciwnym razie nic nie rób (nie można włączyć trzeciego)
        return redirect(url_for('home'))
    # Kolory i etykiety przycisków
    buttons = [
        {'name': 'dobrze', 'label': 'DOBRZE', 'color': 'red'},
        {'name': 'tanio', 'label': 'TANIO', 'color': 'green'},
        {'name': 'szybko', 'label': 'SZYBKO', 'color': 'gray'}
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
            .red { background: #c0392b; }
            .green { background: #27ae60; }
            .gray { background: #7f8c8d; }
        </style>
    </head>
    <body>
        <h2>Możesz wybrać tylko DWIE opcje:</h2>
        <form method="post">
            {% for btn in buttons %}
                <button name="button" value="{{btn.name}}"
                    class="btn {{btn.color}} {% if states[btn.name] %}active{% endif %}">
                    {{btn.label}}
                </button>
            {% endfor %}
        </form>
    </body>
    </html>
    ''', buttons=buttons, states=button_states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)