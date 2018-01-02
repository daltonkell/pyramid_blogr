from ..models.user import User


class UserService(object):

    @classmethod
    def by_name(cls, name, request):
        return request.dbsession.query(User).filter(User.name == name).first()

    @classmethod
    def all(cls, request):
        _query = request.dbsession.query(User).all()
        return _query

        # names = []
        # passwords = []
        # logged = []
        # for _row in _query:
        #     names.append(_row.name)
        #     passwords.append(_row.password)
        #     logged.append(_row.last_logged)
        # return (names, passwords, logged)
