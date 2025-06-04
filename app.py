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
        # Jeśli kliknięty przycisk jest już włączony, wyłącz go
        if button_states[btn]:
            button_states[btn] = False
        else:
            # Wyłącz wszystkie, włącz tylko kliknięty
            for k in button_states:
                button_states[k] = False
            button_states[btn] = True
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
    </body>
    </html>
    ''', buttons=buttons, states=button_states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)