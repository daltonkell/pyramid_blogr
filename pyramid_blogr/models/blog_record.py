import datetime #<- will be used to set default dates on models
from pyramid_blogr.models.meta import Base  #<- we need to import our sqlalchemy metadata from which model classes will inherit
from sqlalchemy import (
    Column,
    Integer,
    Unicode,     #<- will provide Unicode field
    UnicodeText, #<- will provide Unicode text field
    DateTime,    #<- time abstraction field
)
from webhelpers2.text import urlify # will generate slugs
from webhelpers2.date import distance_of_time_in_words # human friendly dates
# the above imports work directly with the BlogRecord instance

class BlogRecord(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    # the property of an entry instance will return nice slugs for us
    # to use in URLs. E.g. pages with the title "Foo Bar Baz" will
    # have URLs of "Foo-Bar-Baz". Non-Latin characters will be
    # approximated to their closest counterparts.
    def slug(self):
        """
        Turns page titles into URLs.
        """
        return urlify(self.title)

    @property
    def created_in_words(self):
        """
        Returns information about when a specific entry was created
        in a human-friendly form, like "2 days ago".
        """
        return distance_of_time_in_words(self.created,
                                         datetime.datetime.utcnow())
