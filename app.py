from flask import Flask, render_template, session, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)

# Поддерживаемые языки
supported_languages = ['ru', 'en']

@app.route('/')
def index():
    global current_language
    # Получаем текущий язык из сессии или используем язык по умолчанию
    current_language = session.get('language', 'ru')
    return render_template('index.html', current_language=current_language)

@app.route('/change_language', methods=['POST'])
def change_language():
    # Получаем текущий язык из сессии или используем язык по умолчанию
    current_language = session.get('language', 'ru')

    # Проверяем поддерживаемые языки и меняем язык
    if current_language == 'ru':
        new_language = 'en'
    else:
        new_language = 'ru'
    
        # Устанавливаем новый язык в сессию
    session['language'] = new_language
    
    # Перенаправляем обратно на предыдущую страницу
    return redirect(request.referrer)



@app.route('/interactive_map')
def map():
    current_language = session.get('language', 'ru')
    return render_template('map.html', current_language=current_language)

@app.route('/contacts')
def contacts():
    current_language = session.get('language', 'ru')
    return render_template('contacts_page.html', current_language=current_language)

@app.route('/home')
def home():
    current_language = session.get('language', 'ru')
    return render_template('home.html', current_language=current_language)

@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    if request.method == 'POST':
        email = request.form['mail']
        message = request.form['text']

        item = Item(message=message, email=email)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except IntegrityError:
            db.session.rollback()
            return 'Ошибка! Дубликат записи.'
    else:
        current_language = session.get('language', 'ru')
        return render_template('feedback_page.html', current_language=current_language)


@app.route('/schedule')
def schedule():
    current_language = session.get('language', 'ru')
    return render_template('schedule_page.html', current_language=current_language)

@app.route('/my-admin-panel')
def data_table():
    current_language = session.get('language', 'ru')  # Удостоверьтесь, что у вас есть current_language
    data = Item.query.all()  # Получаем данные из базы данных
    for item in data:
        print(item.message)
    return render_template('data_table.html', current_language=current_language, data=data)

@app.route('/delete_item/<int:id>', methods=['POST'])
def delete_item(id):
    current_language = session.get('language', 'ru')

    item = Item.query.get_or_404(id)
    
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('data_table'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)