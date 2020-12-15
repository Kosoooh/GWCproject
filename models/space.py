from extensions import db


class Space(db.Model):
    __tablename__ = 'space'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), unique=True)
    reservableTimes = db.Column(db.ARRAY(db.String()), default=["16", "17", "18", "19", "20"])
    is_publish = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    reservations = db.relationship("Reservation", backref="space")

    @classmethod
    def get_all_published(cls):
        return cls.query.filter_by(is_publish=True).all()

    @classmethod
    def get_by_id(cls, space_id):
        return cls.query.filter_by(id=space_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def get_all_by_user(cls, user_id, visibility='public'):
        if visibility == 'public':
            return cls.query.filter_by(user_id=user_id, is_publish=True).all()

        elif visibility == 'private':
            return cls.query.filter_by(user_id=user_id, is_publish=False).all()

        else:
            return cls.query.filter_by(user_id=user_id).all()

