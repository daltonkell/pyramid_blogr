from wtforms import Form, StringField, TextAreaField, validators
from wtforms import IntegerField, PasswordField
from wtforms.widgets import HiddenInput

# For form validation and creation, we will use a very friendly and easy to use
# form called WTForms. First we need to define our form schems that will be used
# to generate form HTML and valdiate values of form fields. We'll do this here.

strip_filter = lambda x: x.strip() if x else None

class BlogCreateForm(Form):
    """
    Enables the creation of a blog entry.
    """
    title = StringField('Title', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    body = TextAreaField('Contents', [validators.Length(min=1)],
                         filters=[strip_filter])

class BlogUpdateForm(BlogCreateForm):
    """
    Enables the editing of blogs. Inherits all properties from BlogCreateForm,
    but introduces a new attr 'id' which will be used to determine which entry
    we want to update.
    """
    id = IntegerField(widget=HiddenInput())


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=255)],
                           filters=[strip_filter])
    password = PasswordField('Password', [validators.Length(min=3)])
