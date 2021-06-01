from blog import db
from blog.models import User, Post

def clear_db():
    db.drop_all()

def make_db():
    db.create_all()

def make_dummy_data():
    user1 = User(username='Kilian', email='kilianetter@web.de', password='herbert')
    user2 = User(username='Alfons', email='alfons@demo.com', password='herbert')

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    user = User.query.get(1)


    post1 = Post(title='Title 1', content='fürst pöst cöntent!', author_id=user.id)
    post2 = Post(title='Title 2', content='secönd pöst cöntent!', author_id=user.id)
    db.session.add(post1)
    db.session.add(post2)
    db.session.commit()

    post = Post.query.get(1) 


if __name__ == '__main__':

    print(User.query.all())
    print(Post.query.all())

