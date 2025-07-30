from flask import render_template, request, redirect, url_for, session, flash
from .encryption import encrypt_password, decrypt_password
from .database import init_db, add_credential, get_credentials
from .phishing_checker import is_phishing_url
from .spam_checker import is_spam_message  # newly added

def init_routes(app):
    init_db()

    @app.route('/')
    def login():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login_post():
        session['logged_in'] = True
        return redirect(url_for('home'))

    @app.route('/home')
    def home():
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return render_template('home.html')

    @app.route('/password-checker', methods=['GET', 'POST'])
    def password_checker():
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        strength = None
        if request.method == 'POST':
            password = request.form['password']
            strength = check_password_strength(password)
        return render_template('password_checker.html', strength=strength)

    @app.route('/vault', methods=['GET', 'POST'])
    def vault():
        if not session.get('logged_in'):
            return redirect(url_for('login'))

        credentials = get_credentials()
        decrypted_credentials = []

        for cred in credentials:
            decrypted_pw = decrypt_password(cred['password'])
            decrypted_credentials.append({
                'id': cred['id'],
                'website': cred['website'],
                'password': decrypted_pw
            })

        if request.method == 'POST':
            website = request.form['website']
            password = request.form['password']
            encrypted_pw = encrypt_password(password)
            add_credential(website, encrypted_pw)
            flash('Credentials saved securely!', 'success')
            return redirect(url_for('vault'))

        return render_template('vault.html', credentials=decrypted_credentials)

    @app.route('/phishing', methods=['GET', 'POST'])
    def phishing():
        if not session.get('logged_in'):
            return redirect(url_for('login'))

        result = None
        if request.method == 'POST':
            url = request.form['url']
            result = is_phishing_url(url)

        return render_template('phishing.html', result=result)

    @app.route('/spam-checker', methods=['GET', 'POST'])
    def spam_checker():
        if not session.get('logged_in'):
            return redirect(url_for('login'))

        result = None
        if request.method == 'POST':
            message = request.form['message']
            result = is_spam_message(message)

        return render_template('spam_checker.html', result=result)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        return redirect(url_for('login'))


def check_password_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if any(char.isupper() for char in password): score += 1
    if any(char.islower() for char in password): score += 1
    if any(char.isdigit() for char in password): score += 1
    if any(char in '!@#$%^&*(),.?":{}|<>' for char in password): score += 1

    if score <= 2:
        return "Weak 🔴"
    elif score == 3:
        return "Medium 🟡"
    else:
        return "Strong 🟢"
