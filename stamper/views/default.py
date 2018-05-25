from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
import pyramid.httpexceptions as exc

from ..models import User
from ..hashes import (
    check_password
)


class View:
    def __init__(self):
        self.title = "Home!"


class ImageUploadView(View):
    def __init__(self):
        self.title = "Загрузка изображений"
        self.subtitle = ''


class LoginView(View):
    def __init__(self):
        self.title = "Регистрация пользователя"
        self.subtitle = 'Вам необходимо войти или зарегистрироваться как новый пользователь'


class UnknownUser:
    def __init__(self):
        self.isvalid = False


unknownUser = UnknownUser()


def get_user(request):
    session = request.session
    if "user" in session:
        return session["user"]
    return unknownUser


def go(request, route, message=None):
    if "message" in request.session:
        del request.session["message"]

    if message is not None:
        request.session["message"] = message

    raise exc.HTTPFound(request.route_url(route))


def relogin(request, message=None):
    return go(request, route="login", message=message)


def go_work(request, message=None):
    return go(request, route="image-upload", message=message)


@view_config(route_name='home', renderer='../templates/home.pt')
def my_view(request):
    try:
        query = request.dbsession.query(User)
        one = query.filter(User.nick == 'admin').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    session = request.session

    return {'one': one,
            'project': 'Stamper Server',
            'view': View(),
            'user': get_user(request)
            }


@view_config(route_name='add-image', renderer='json')
def add_image(request):

    user = get_user(request)

    form = request.POST
    fileFS = form.get("file", None)
    alert = "error"
    print(fileFS)
    filename = fileFS.filename
    input_file = fileFS.file
    content = fileFS.file.read()
    print(len(content))
    imgstore = request.imgstore
    imgstore.start()
    id = imgstore.save(content)
    print(id)
    if fileFS is None:
        return {"result": 0, "message": "Изображение не получено", "alert": alert}

    alert = "success"

    imgstore.commit()
    return {"result": 1, "message": "Изображение сохранено", "alert": alert,
            "id": id}


@view_config(route_name='image-upload', renderer='../templates/upload.pt')
def image_upload(request):
    user = get_user(request)
    if user.isvalid:
        return {'view': ImageUploadView,
                'user': user
                }
    else:
        relogin(request)


@view_config(route_name='login', renderer='../templates/login.pt',
             request_method="GET")
def login_GET(request):
    user = get_user(request)
    if user.isvalid:
        raise exc.HTTPBadRequest()

    else:
        return {'view': LoginView,
                'user': user
                }


@view_config(route_name='login', renderer='json', request_method="POST")
def login_POST(request):
    post = request.POST
    user = unknownUser
    try:
        query = request.dbsession.query(User)
        user = query.filter(User.nick == post["user"]).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

    register = post.get("register", None)
    register = register is not None

    session = request.session

    if "usage" in session:
        del session["user"]

    session["user"] = unknownUser

    if user is None:
        if register:
            # регистрация
            pass
        else:
            relogin(request, "Пользователь не найден")
    else:
        if register:
            relogin(request, "Такой ник уже использован")
        else:
            if check_password(post["password"], user.passwd):
                session["user"] = user
                return go_work(request, "Вы вошли в систему")
            else:
                return relogin(request, "Пароль неверный")

    return {
        'user': user.nick
    }


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_stamper_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
