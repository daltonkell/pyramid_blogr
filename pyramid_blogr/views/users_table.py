from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
# The above HTTP exceptions will be used to perform redirects inside our apps.
from ..services.user import UserService

# what I want to do: create a view that pulls all users from the database
# session and returns all their associated information

@view_config(route_name='users',
     renderer='pyramid_blogr:templates/view_users.jinja2', request_method='GET')
def users_table(request):
    """
    This method returns a view of the entire database of registered users and
    their associated information.
    """
    data = UserService.all(request)
    print(data)
    return {'data': data}
