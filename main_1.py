from flask_login import LoginManager, login_user, login_required, logout_user
from flask import Flask, render_template, request, make_response, jsonify
import datetime
from flask_wtf import FlaskForm
from requests import get
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from wtforms import BooleanField, SubmitField, PasswordField, StringField, IntegerField, TextAreaField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from data import db_session, tours_api, users_api
from data.tours import Tour
from data.users import User

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    submit = SubmitField('Войти')


class TourForm(FlaskForm):
    email = EmailField('Ваша электронная почта', validators=[DataRequired()])
    name = StringField('Название экскурсии', validators=[DataRequired()])
    about = TextAreaField('Описание экскурсии', validators=[DataRequired()])
    places = TextAreaField('Список мест для посещения, каждое с новой строки', validators=[DataRequired()])
    cost = IntegerField('Стоимость', validators=[DataRequired()])
    date = DateField('Дата экскурсии', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


def geocode(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}" \
                       f"&geocode={address}&format=json"
    response = get(geocoder_request)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
                request=geocoder_request, status=response.status_code, reason=response.reason))
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return None, None
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html', title='Главное окно')


@app.route('/tours')
@login_required
def tours_():
    db_sess = db_session.create_session()
    lst = []
    for tour in db_sess.query(Tour).all():
        user = db_sess.query(User).filter(User.id == tour.user).first()
        lst.append([tour, user, str(tour.id)])
    return render_template('tours.html', title='Список экскурсий', lst=lst)


@app.route('/tours/sort/<sort_type>')
@login_required
def tours_sort(sort_type):
    db_sess = db_session.create_session()
    lst = []
    for tour in db_sess.query(Tour).all():
        user = db_sess.query(User).filter(User.id == tour.user).first()
        lst.append([tour, user, str(tour.id), int(tour.cost), tour.date])
    if sort_type == 'max':
        lst.sort(key=lambda x: x[3])
    elif sort_type == 'min':
        lst.sort(key=lambda x: -x[3])
    else:
        lst.sort(key=lambda x: x[4])
    return render_template('tours.html', title='Список экскурсий', lst=lst)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.age = form.age.data
        user.created_date = datetime.datetime.now()
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/tours")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def make_photo(tour_id):
    db_sess = db_session.create_session()
    tour = db_sess.query(Tour).get(tour_id)
    if tour:
        lst = tour.places.split('&')
        pts = []
        x, y = [], []
        for i in range(len(lst)):
            a, b = get_coordinates(lst[i])
            x.append(a)
            y.append(b)
            coords = str(a) + ',' + str(b)
            pts.append(coords + ',pmwtm' + str(i + 1))
        ll = ','.join([str((min(x) + max(x)) / 2), str((min(y) + max(y)) / 2)])
        pts = '~'.join(pts)
        spn_x, spn_y = max(x) - min(x), max(y) - min(y)
        k = 1.2
        spn = str(spn_x * k) + ',' + str(spn_y * k)
        link = "http://static-maps.yandex.ru/1.x/?ll=" + ll + "&l=map&spn=" + spn + "&z=12&&pt=" + pts
        resp = get(link)
        filename = 'static/img/foto' + str(tour_id) + '.png'
        with open(filename, "wb") as f:
            f.write(resp.content)


@app.route('/tours/<int:tour_id>')
@login_required
def tours(tour_id):
    db_sess = db_session.create_session()
    tour = db_sess.query(Tour).get(tour_id)
    if tour:
        lst = tour.places.split('&')
        filename = 'static/img/foto' + str(tour_id) + '.png'
        return render_template("tour.html", title="Экскурсия #" + str(tour.id), tour=tour, file=filename, lst=lst)
    return """<h1 class="text-center">Ошибка!</h1>"""


@app.route('/tours/add_tour', methods=['GET', 'POST'])
@login_required
def add_tour():
    form = TourForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Tour).filter(Tour.name == form.name.data).first():
            return render_template('add_tour.html', title='Добавление работы',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        tour = Tour()
        tour.name = form.name.data
        tour.about = form.about.data
        tour.places = '&'.join(form.places.data.split('\r'))
        tour.cost = form.cost.data
        tour.date = form.date.data
        tour.user = user.id
        db_sess.add(tour)
        db_sess.commit()
        tour_id = db_sess.query(Tour).filter(Tour.name == form.name.data).first().id
        make_photo(tour_id)
        return redirect('/tours')
    return render_template('add_tour.html', title='Добавление работы', form=form)


@app.route('/tours/tours_edit/<int:tours_id>', methods=['GET', 'POST'])
@login_required
def tours_edit(tours_id):
    form = TourForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        tour = db_sess.query(Tour).filter(Tour.id == tours_id).first()
        if tour:
            user = db_sess.query(User).filter(User.id == tour.user).first()
            form.email.data = user.email
            form.name.data = tour.name
            form.about.data = tour.about
            form.places.data = '\r'.join(tour.places.split('&'))
            form.cost.data = tour.cost
            form.date.data = tour.date
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        tour = db_sess.query(Tour).filter(Tour.id == tours_id).first()
        if tour:
            tour.name = form.name.data
            tour.about = form.about.data
            tour.places = '&'.join(form.places.data.split('\r'))
            tour.cost = form.cost.data
            tour.date = form.date.data
            db_sess.commit()
            make_photo(tours_id)
            return redirect('/tours')
        else:
            abort(404)
    return render_template('edit_tour.html', title='Редактирование новости', form=form)


@app.route('/tours/tours_delete/<int:tour_id>', methods=['GET', 'POST'])
@login_required
def tours_delete(tour_id):
    db_sess = db_session.create_session()
    tour = db_sess.query(Tour).filter(Tour.id == tour_id).first()
    if tour:
        db_sess.delete(tour)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/tours')


@app.route('/favourite/<int:user_id>')
@login_required
def favourite(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    lst = []
    for tour in db_sess.query(Tour).all():
        users = db_sess.query(User).filter(User.id == tour.user).first()
        item = [tour, users, str(tour.id)]
        lst.append(item)
    return render_template("favourite.html", title='Избранное', lst=lst, user=user)


@app.route('/tours/favourite_delete/<int:user_id>/<int:tour_id>', methods=['GET'])
@login_required
def favourite_delete(user_id, tour_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    s = user.favourite.split('&')
    s = [int(i.strip('a')) for i in s]
    del s[s.index(tour_id)]
    s = list(map(str, s))
    user.favourite = '&'.join(s)
    if len(user.favourite) == 1:
        user.favourite += 'a'
    db_sess.commit()
    return redirect('/favourite/' + str(user.id))


@app.route('/favourite_delete/<int:user_id>/<int:tour_id>', methods=['GET'])
@login_required
def favourite_delete_(user_id, tour_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    s = user.favourite.split('&')
    s = [int(i.strip('a')) for i in s]
    del s[s.index(tour_id)]
    s = list(map(str, s))
    user.favourite = '&'.join(s)
    if len(user.favourite) == 1:
        user.favourite += 'a'
    db_sess.commit()
    return redirect('/tours')


@app.route('/tours/add_favourite/<int:user_id>/<int:tour_id>', methods=['GET'])
@login_required
def add_favourite(user_id, tour_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if len(user.favourite) == 0:
        user.favourite = str(tour_id) + 'a'
    else:
        user.favourite += "&" + str(tour_id)
    db_sess.commit()
    return redirect('/tours')


def main():
    db_session.global_init("db/base.db")
    app.register_blueprint(tours_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
