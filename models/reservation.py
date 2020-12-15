from extensions import db


class Reservation(db.Model):

    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True)

    reservationTime = db.Column(db.String(64))
    is_published = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    @classmethod
    def get_all_published(cls):
        return cls.query.filter_by(is_published=True).all()

    @classmethod
    def get_by_id(cls, reservation_id):
        return cls.query.filter_by(id=reservation_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def get_all_by_user(cls, user_id, visibility='public'):

        return cls.query.filter_by(user_id=user_id).all()
