from flask import Flask, render_template, request, redirect, url_for, flash, session
from threads_bot_ejecucion import ejecutar_bot
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Usuarios simulados con tokens
users = {
    'maax': {'password': '1234', 'tokens': 10}
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('panel'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            flash('Login exitoso!', 'success')
            return redirect(url_for('panel'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
    return render_template('login.html')

@app.route('/panel')
def panel():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    tokens = users[username]['tokens']
    return render_template('panel.html', tokens=tokens)

@app.route('/usar_token', methods=['POST'])
def usar_token():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user = users[username]

    if user['tokens'] > 0:
        try:
            ejecutar_bot()
            user['tokens'] -= 1
            flash('Bot ejecutado exitosamente. Token consumido.', 'success')
        except Exception as e:
            flash(f"Error al ejecutar el bot: {e}", 'error')
    else:
        flash('No tienes tokens suficientes.', 'error')

    return redirect(url_for('panel'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))  # Render asigna automáticamente el puerto
    app.run(host='0.0.0.0', port=port)
