from app import Confessions, db

for x in range(50):
    newPost = Confessions(title='Sample Title', description='Sample Description')
    db.session.add(newPost)
    db.session.commit()