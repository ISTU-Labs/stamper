from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import User


class View:
    def __init__(self):
        self.title = "Home!"


class ImageUploadView(View):
    def __init__(self):
        self.title = "Загрузка изображений"
        self.subtitle = ''


@view_config(route_name='home', renderer='../templates/home.pt')
def my_view(request):
    try:
        query = request.dbsession.query(User)
        one = query.filter(User.nick == 'admin').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'Stamper Server', 'view': View()}


@view_config(route_name='add-image', renderer='json')
def add_image(request):
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
    return {"result": 1, "message": "Изображение сохранено", "alert": alert}


@view_config(route_name='image-upload', renderer='../templates/upload.pt')
def image_upload(request):
    return {'view': ImageUploadView}


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
