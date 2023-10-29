from flask import Flask, render_template, session, redirect, url_for, request
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Clave secreta para manejar la sesión

# Ruta raíz
@app.route('/', methods=['GET', 'POST'])
def guess_number():
    message = ""  # Inicializamos la variable 'message'
    color = ""     # Inicializamos la variable 'color'

    if 'number' not in session:
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0

    if request.method == 'POST':
        guessed_number = int(request.form['guessed_number'])
        session['attempts'] += 1

        if guessed_number < session['number']:
            message = "Muy bajo, intenta de nuevo."
            color = "blue"
        elif guessed_number > session['number']:
            message = "Muy alto, intenta de nuevo."
            color = "red"
        else:
            message = "¡Correcto! El número era {}".format(session['number'])
            color = "green"
            if 'winners' not in session:
                session['winners'] = []
            session['winners'].append({'attempts': session['attempts']})
            session.pop('number')

    if 'number' in session and session['attempts'] == 5:
        message = "¡Lo siento! Agotaste tus intentos. El número era {}".format(session['number'])
        color = "black"
        session.pop('number')

    return render_template('index.html', message=message, color=color)

# Ruta para mostrar los ganadores
@app.route('/winners')
def winners():
    if 'winners' in session:
        return render_template('winners.html', winners=session['winners'])
    else:
        return "No hay ganadores todavía."

if __name__ == '__main__':
    app.run(debug=True)
