from extensions import db

space_list = []


def get_last_id():
    if space_list:
        last_space = space_list[-1]
    else:
        return 1
    return last_space.id + 1


class Space(db.Model):
    __tablename__ = 'space'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    reservations = db.Column(db.ARRAY(db.String()), nullable=True)
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
