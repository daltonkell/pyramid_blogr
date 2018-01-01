from pyramid.security import Allow, Everyone, Authenticated

class BlogRecordFactory(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, Authenticated, 'create'),
               (Allow, Authenticated, 'edit'), ]

    def __init__(self, request):
        pass

# This is an object called a context factory. It's not tied to any specific entity
# in a database, and it returns an __acl__ property which says tha everyone has a
# 'view' permission, and users that are logged in also have 'create' and 'edit'
# permissions.
