from extensions import db


class Space(db.Model):
    __tablename__ = 'space'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    reservations = db.Column(db.ARRAY(db.String()))
    reservableTimes = db.Column(db.ARRAY(db.String()))
    is_reserved = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

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

