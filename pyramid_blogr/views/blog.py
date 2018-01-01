from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from ..models.blog_record import BlogRecord
from ..services.blog_record import BlogRecordService
# The above HTTP exceptions will be used to perform redirects inside our apps.
from ..forms import BlogCreateForm, BlogUpdateForm
# the above is needed for writing our blog views for creating and updating


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


# now that our simple form definition is ready (see forms.py), we can actually
# write our view code.

@view_config(route_name='blog_action', match_param='action=create',
             renderer='pyramid_blogr:templates/edit_blog.jinja2',
             permission='create')
def blog_create(request):
    """
    We implement a view callable that will handle new entries for us.
    - create a new entry row and form object from BlogCreateForm
    - the form will be populated by POST, if present
    - if the request method is POST, the form gets validated
    - If the form is validated, our form sets it values to the model instance
    and adds it to the database session
    - redirects to the index page
    """
    entry = BlogRecord()
    form = BlogCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        request.dbsession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='pyramid_blogr:templates/edit_blog.jinja2',
             permission='create')
def blog_update(request):
    """
    The following view will handle updates to existing blog entries.
    - Fetch the blog entry from the DB
    - show a 404 Not Found page if the record requested is not present
    - Create the form object, populating it from the POST params or from the
    actual blog entry, if we haven't POSTed any values yet.
    This approach ensures our form is always populated with the latest data from
    the DB, or if the submission is not valid, then the values we POSTed in our
    last requuest will poulate the form fields.
    """
    blog_id = int(request.params.get('id', -1))
    entry = BlogRecordService.by_id(blog_id, request)
    if not entry:
        return HTTPNotFound()
    form = BlogUpdateForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        del form.id  # SECURITY: prevent overwriting of primary key
        form.populate_obj(entry)
        return HTTPFound(
            location=request.route_url('blog', id=entry.id,slug=entry.slug))
    return {'form': form, 'action': request.matchdict.get('action')}
