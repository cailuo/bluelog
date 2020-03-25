import random

from bluelog.models import Admin, Category, Post, Comment, Link
from bluelog.extensions import db
from sqlalchemy.exc import IntegrityError

from faker import Faker
fake = Faker()


def fake_admin():
    admin = Admin(
        username='admin',
        # password_hash=None,
        blog_title='Bluelog',
        blog_sub_title='I am the sub_title',
        name='cailuo',
        about='keep moving, keep study'
    )
    admin.set_password('12345678')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            timestamp=fake.date_time_this_year(),
            # category_id=None,
            category=Category.query.get(random.randint(1, Category.query.count()))
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            from_admin=False,
            reviewed=True,
            timestamp=fake.date_time_this_year(),
            # post_id=None,
            post=Post.query.get(random.randint(1, Post.query.count())),
            # replied_id=None,
            # replied=None,
            # replies=None
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # reviewed is False
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            from_admin=False,
            reviewed=False,
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count())),
            # replied_id=None,
            # replied=None,
            # replies=None
        )
        db.session.add(comment)

        # author is admin, and reviewed is True
        comment = Comment(
            author='admin',
            email='admin@example.com',
            site='example.com',
            body=fake.sentence(),
            from_admin=True,
            reviewed=True,
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count())),
            # replied_id=None,
            # replied=None,
            # replies=None
        )
        db.session.add(comment)

        # replies to comments, and reviewed is True
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            from_admin=False,
            reviewed=True,
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count())),
            # replied_id=None,
            replied=Comment.query.get(random.randint(1, Comment.query.count()))
            # replies=None
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    twitter = Link(name='Twitter', url='#')
    facebook = Link(name='Facebook', url='#')
    linkedin = Link(name='LinkedIn', url='#')
    google = Link(name='Google+', url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()
