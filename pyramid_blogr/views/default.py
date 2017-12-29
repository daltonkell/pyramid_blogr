# from pyramid.view import view_config
# from pyramid.httpexceptions import HTTPFound
# from pyramid.security import remember, forget
# from ..services.user import UserService
# from ..services.blog_record import BlogRecordService
# from ..forms import RegistrationForm
# from ..models.user import User
#
#
# @view_config(route_name='auth', match_param='action=in', renderer='string',
#              request_method='POST')
# @view_config(route_name='auth', match_param='action=out', renderer='string')
# def sign_in_out(request):
#     username = request.POST.get('username')
#     if username:
#         user = UserService.by_name(username, request=request)
#         if user and user.verify_password(request.POST.get('password')):
#             headers = remember(request, user.name)
#         else:
#             headers = forget(request)
#     else:
#         headers = forget(request)
#     return HTTPFound(location=request.route_url('home'), headers=headers)
#
#
# @view_config(route_name='register',
#              renderer='pyramid_blogr:templates/register.jinja2')
# def register(request):
#     form = RegistrationForm(request.POST)
#     if request.method == 'POST' and form.validate():
#         new_user = User(name=form.username.data)
#         new_user.set_password(form.password.data.encode('utf8'))
#         request.dbsession.add(new_user)
#         return HTTPFound(location=request.route_url('home'))
#     return {'form': form}


from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from ..services.blog_record import BlogRecordService # import from /services
from ..models.user import User


# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def my_view(request):
#     try:
#         query = request.dbsession.query(User)
#         one = query.filter(User.name == 'admin').first()
#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
#     return {'one': one, 'project': 'pyramid_blogr'}

# replaces the above
@view_config(route_name='home',
             renderer='pyramid_blogr:templates/index.jinja2')
             # Here, view_config takes two params that will reguster our
             # index_page callable in Pyramid's registry, specifying the route
             # that should be used to match this view. We also specify renderer.
             # See templates/index.jinja2 for the template itself.
# implement our actual index view
def index_page(request):
    """
    First retrieves from the URL's request object the page number that we want
    to present to the user. If the page number is not present, it defaults to 1.

    The paginator object returned by BlogRecordService.get_paginator will then
    be used in the template to build a nice list of entries.
    """
    page = int(request.params.get('page', 1))
    paginator = BlogRecordService.get_paginator(request, page)
    return {'paginator': paginator}
    # return {}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramid_blogr_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    return {}

# these routes will hander user authentication and logout. They do not use a
# template because they will just perform HTTP redirects, and no one will see
# them.
# Note that this view is decorated more than once. It also introduces a new
# parameter, request_method, which restricts view resolution to a specific
# request method (in this example, just POST requests). It will not be reachable
# with GET requests. Views can be decorated unlimited times with different
# params passed into @view_config.

# Everything we return from our views in dictionaries will be available in
# templates as variables. So, if we return {'foo': 1, 'bar': 2}, then we will
# be able to access the variables inside the template directly as foo and bar.
