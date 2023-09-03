from app import db
from flask_login import UserMixin
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(32))
    fullname = db.Column(db.String(100))
    image = db.Column(db.String(100))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(14))
    email_verification = db.Column(db.String(32))
    otp = db.Column(db.String(6))
    is_active = db.Column(db.Integer(),default=1)
    is_email_verified = db.Column(db.Integer())
    is_phone_verified = db.Column(db.Integer())
    t_app = db.relationship('TApp')
    files = db.relationship('UserFile')
    user_category_id = db.Column(db.Integer, db.ForeignKey('user_category.id'))
    category = db.relationship('UserCategory', uselist=False)
    def __repr__(self):
        return '<User: {}>'.format(self.id)

    def check_password(self,verify):
        return verify == self.password
class UserCategory(db.Model):
    __tablename__ = 'user_category'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user = db.relationship('User',back_populates='category')
    def __repr__(self):
        return '<UserCategory: {}>'.format(self.id)
class AppCategory(db.Model):
    __tablename__ = 'app_category'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    t_app = db.relationship('TApp',back_populates='category')
    def __repr__(self):
        return '<AppCategory: {}>'.format(self.id)
class FinalModel(db.Model):
    __tablename__ = 'final_model'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    model_name = db.Column(db.String(100))
    desc = db.Column(db.String(500))
    lang = db.Column(db.String(40))
    app_id = db.Column(db.Integer, db.ForeignKey('t_app.id'))
    t_app = db.relationship('TApp', uselist=False)
    def __repr__(self):
        return '<FinalModel: {}>'.format(self.id)
class TApp(db.Model):
    __tablename__ = 't_app'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String(255),default='-')
    data_folder = db.Column(db.String(100))
    created_date = db.Column(db.Date)
    status = db.Column(db.String(20),default=0) #1=idle , 2=training , 3=ready to deploy
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, back_populates='t_app')
    category_id = db.Column(db.Integer, db.ForeignKey('app_category.id'))
    category = db.relationship('AppCategory', uselist=False)
    files = db.relationship('UserFile')
    models = db.relationship('FinalModel',back_populates='t_app')
    def __repr__(self):
        return '<TApp: {}>'.format(self.id)
class UserFile(db.Model):
    __tablename__ = 'user_file'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    uid = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    app_id = db.Column(db.Integer, db.ForeignKey('t_app.id'))
    user = db.relationship('User', uselist=False,back_populates='files')
    app = db.relationship('TApp', uselist=False,back_populates='files')
    def __repr__(self):
        return '<UserFile: {}>'.format(self.id)
class CoreFunction(db.Model):
    __tablename__ = 'core_function'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    class_name = db.Column(db.String(100))
    function_name = db.Column(db.String(100))
    params = db.Column(db.String(400))
    requirements = db.Column(db.String(1000))
    lang = db.Column(db.String(40))
    def __repr__(self):
        return '<CoreFunction: {}>'.format(self.id)

################### OAUTH 2 ##############################
class Client(db.Model):

    # human readable name, not required
    name = db.Column(db.String(40))

    # human readable description, not required
    description = db.Column(db.String(400))

    # creator of the client, not required
    user_id = db.Column(db.ForeignKey('user.id'))
    # required if you need to support client credential
    user = db.relationship('User')

    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              nullable=False)

    # public or confidential
    is_confidential = db.Column(db.Boolean)

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []

class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
