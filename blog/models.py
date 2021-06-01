from datetime import datetime
from blog import db, login_manager, app
from flask_login import UserMixin

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


### Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    img_profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    # tasks = db.relationship('Task', backref='owner', lazy=True)

    def __repr__(self):
        return f'User(" {self.id}: {self.username} - {self.email} - {self.img_profile}")'

    
    def getResetToken(self, expires=1800):
        s = Serializer(app.config['SECRET_KEY'], expires)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verifyResetToken(token):
        s=Serializer(app.config['SECRET_KEY'])
        try:
            user_id= s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    def __repr__(self):
        return f'User(" {self.id}: {self.title} - {self.date_posted} by User #{self.author_id}")'
    
    



###
# class Task(db.Model):
#     id =
#     title =
#     subtitle =
#     content = 
#     assigned_tab =
#     status =
#     # dates
#     date_created =
#     due_date_original =
#     due_date_edited =
#     # users
#     creator=
#     owner =
#     assigned_user =
#     assinged_team =

#     def __repr__(self) -> str:
#         return f'Task("{self.id}: {self.title} - {self.date_created} by")'

# class Subtask(db.Model):
#     id = 
#     title =
#     subtitle =
#     date_created =
#     due_date_original =
#     due_date_edited =
