from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from ..models.blog_record import BlogRecord
from ..services.blog_record import BlogRecordService
# The above HTTP exceptions will be used to perform redirects inside our apps.
# from ..forms import BlogCreateForm, BlogUpdateForm


# register blog_view with a rotue named 'blog' using the view_blog template as
# the response
@view_config(route_name='blog',
             renderer='pyramid_blogr:templates/view_blog.jinja2')
def blog_view(request):
    """
    First we get the id variable from our route. It will be present in the
    matchdict property of the request object (recall that the request object
    is created ------ ????). All of our defined route args will end up there.

    After we get the entry id, it will be passed to BlogRecordService class
    method by_id() to fetch a specific blog entry. If it's found, we return the
    database row for the template to use, otherwise we present the user with a
    standard 404 response.
    """
    blog_id = int(request.matchdict.get('id', -1))
    entry = BlogRecordService.by_id(blog_id, request)
    if not entry:
        return HTTPNotFound
    return {'entry': entry}

@view_config(route_name='blog_action', match_param='action=create',
             renderer='pyramid_blogr:templates/edit_blog.jinja2')
             # notice the new match_param kw. Its purpose is to tell pyramid
             # which view callable to use when the dynamic part of the
             # route{action} is matched. E.g. the above will be launched for
             # the URL /blog/create
def blog_create(request):
    return {}


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='pyramid_blogr:templates/edit_blog.jinja2')
             # this one launches for _______
def blog_update(request):
    return {}

# @view_config(route_name='blog',
#              renderer='pyramid_blogr:templates/view_blog.jinja2')
# def blog_view(request):
#     blog_id = int(request.matchdict.get('id', -1))
#     entry = BlogRecordService.by_id(blog_id, request)
#     if not entry:
#         return HTTPNotFound()
#     return {'entry': entry}
#
#
# @view_config(route_name='blog_action', match_param='action=create',
#              renderer='pyramid_blogr:templates/edit_blog.jinja2',
#              permission='create')
# def blog_create(request):
#     entry = BlogRecord()
#     form = BlogCreateForm(request.POST)
#     if request.method == 'POST' and form.validate():
#         form.populate_obj(entry)
#         request.dbsession.add(entry)
#         return HTTPFound(location=request.route_url('home'))
#     return {'form': form, 'action': request.matchdict.get('action')}
#
#
# @view_config(route_name='blog_action', match_param='action=edit',
#              renderer='pyramid_blogr:templates/edit_blog.jinja2',
#              permission='create')
# def blog_update(request):
#     blog_id = int(request.params.get('id', -1))
#     entry = BlogRecordService.by_id(blog_id, request)
#     if not entry:
#         return HTTPNotFound()
#     form = BlogUpdateForm(request.POST, entry)
#     if request.method == 'POST' and form.validate():
#         del form.id  # SECURITY: prevent overwriting of primary key
#         form.populate_obj(entry)
#         return HTTPFound(
#             location=request.route_url('blog', id=entry.id,slug=entry.slug))
#     return {'form': form, 'action': request.matchdict.get('action')}
