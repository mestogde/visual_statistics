from flask import Flask
from flask import render_template
from flask_login import LoginManager, login_user
from werkzeug.utils import redirect

from data import db_session, users
import os


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init('users.sqlite')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


@app.route('/')  # функция обратного вызова
def route():
    return render_template('index_log.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/work')
def work():
    return render_template('work.html')


@app.route('/worktula')
def worktula():
    # добавление столбиков диаграммы
    labels = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Отябрь", "Ноябрь",
              "Декабрь"]
    # добавление соответсвующих значений
    values = [34211.1, 34214.9, 36176.2, 37376.9, 37353.2, 39478, 37666.7, 36565.8, 36668.1, 37002, 36756.7, 46503.2]
    return render_template('worktula.html', values=values, labels=labels)


@app.route('/workrussia')
def workrussia():
    labels = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Отябрь", "Ноябрь",
              "Декабрь"]
    values = [42263.2, 43062.4,	46324.2, 48029.8, 47926.2,	49347.9,	46509.4,	44961.3,	45540.9, 46549,	46284.5,	62239.2]
    return render_template('workrussia.html', values=values, labels=labels)


@app.route('/workmoscow')
def workmoscow():
    labels = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Отябрь", "Ноябрь",
              "Декабрь"]
    values = [79680.4,	85370,	95178.5,	102907.1,	89044.8,	96029.9,	91607.1,	86733.1,	86684.4,	89128.6,	88656.5,	135374.9]
    return render_template('workmoscow.html', values=values, labels=labels)


@app.route('/inv')
def inv():
    return render_template('inv.html')


@app.route('/invtula')
def invtula():
    labels = ["2005", "2006", "2007", "2008", "2009", "2010",
              "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
    values = [131.9,	105.6,	132.8,	130.1, 104.4,	112.8,	103.3,	100.7,	100.7,	100.4,	100.1,	100.2,	110.7,	112.9,	108.9]
    return render_template('invtula.html', values=values, labels=labels)


@app.route('/invmoscow')
def invmoscow():
    labels = ["2005", "2006", "2007", "2008", "2009", "2010",
              "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
    values = [110.3,	115.2,	110.9,	102.5,	76.4,	95.8,	106.6,	133.1,	107.1,	104.4,	97.4,	101.2,	114.8,	118.0,	108.9]
    return render_template('invmoscow.html', values=values, labels=labels)


@app.route('/invrussia')
def invrussia():
    labels = ["2005", "2006", "2007", "2008", "2009", "2010",
              "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
    values = [110.2,	117.8,	123.8,	109.5,	86.5,	106.3,	110.8,	106.8,	100.8,	98.5,	89.9,	99.8,	104.8,	105.4,	101.7]
    return render_template('invrussia.html', values=values, labels=labels)


@app.route('/people')
def people():
    return render_template('people.html')


@app.route('/peopletula')
def peopletula():
    labels = ["2014", "2015", "2016", "2017", "2018", "2019"]
    values = [1521.5, 1513.6, 1506.4, 1499.4, 1491.9, 1478.8]
    return render_template('peopletula.html', values=values, labels=labels)


@app.route('/peoplemoscow')
def peoplemoscow():
    labels = ["2014", "2015", "2016", "2017", "2018", "2019"]
    values = [12108.3, 12197.6, 12330.1, 12380.7, 12506.5, 12615.3]
    return render_template('peoplemoscow.html', values=values, labels=labels)


@app.route('/peoplerussia')
def peoplerussia():
    labels = ["2014", "2015", "2016", "2017", "2018", "2019"]
    values = [143.7, 146.3, 146.5, 146.8, 146.9, 146.8]
    return render_template('peoplerussia.html', values=values, labels=labels)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = users.RegisterForm()
    # проверка на выполнение всех правил регистрации
    if form.validate_on_submit():
        # проверка на совпадение паролей
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        # проверяется новый пользователь или уже существует
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = users.LoginForm()
    # проверка на правилльность авторизации
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("index")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='visual-statistics.herokuapp.com', port=port)
