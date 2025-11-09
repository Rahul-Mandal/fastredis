from myapp.models.user import User


def fetch_data(db):
    print(type(db))
    print(User)

    return db.query(User).all()