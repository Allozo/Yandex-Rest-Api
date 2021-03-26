from app import Base
import sqlalchemy as db
from sqlalchemy.orm import relationship


class Couriers(Base):
    __tablename__ = 'Couriers'

    courier_id = db.Column(db.Integer, primary_key=True)
    courier_type = db.Column(db.String(50), nullable=False)

    regions = relationship("CouriersRegions",
                           cascade="all, delete, delete-orphan",
                           backref='courier')

    working_hours = relationship("CouriersWorkingTime",
                                 cascade="all, delete, delete-orphan",
                                 backref='courier')

    def __repr__(self):
        return f"{self.courier_id}, {self.courier_type}"


class CouriersWorkingTime(Base):
    __tablename__ = 'CouriersWorkingTime'

    _id = db.Column(db.Integer, primary_key=True)
    courier_id = db.Column(db.Integer, db.ForeignKey('Couriers.courier_id'),
                           nullable=False)
    working_hours_start = db.Column(db.DateTime, nullable=False)
    working_hours_end = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        start = self.working_hours_start.strftime('%H:%M')
        end = self.working_hours_end.strftime('%H:%M')
        return f"{start}-{end}"


class CouriersRegions(Base):
    __tablename__ = "CouriersRegions"

    _id = db.Column(db.Integer, primary_key=True)
    courier_id = db.Column(db.Integer, db.ForeignKey('Couriers.courier_id'),
                           nullable=False)
    region = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.region}"


class Orders(Base):
    __tablename__ = 'Orders'

    order_id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    time_accept = db.Column(db.DateTime, nullable=True)
    complete_time = db.Column(db.DateTime, nullable=True)

    regions = relationship("OrderRegions",
                           cascade="all, delete, delete-orphan",
                           backref='order')

    delivery_hours = relationship("OrderDeliveryTime",
                                  cascade="all, delete, delete-orphan",
                                  backref='order')


class OrderRegions(Base):
    __tablename__ = 'OrderRegions'

    _id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,
                         db.ForeignKey('Orders.order_id'),
                         nullable=False)
    region = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.region}"


class OrderDeliveryTime(Base):
    __tablename__ = 'OrderDeliveryTime'

    _id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,
                         db.ForeignKey('Orders.order_id'),
                         nullable=False)
    delivery_hours_start = db.Column(db.DateTime, nullable=False)
    delivery_hours_end = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        start = self.delivery_hours_start.strftime('%H:%M')
        end = self.delivery_hours_end.strftime('%H:%M')
        return f"{start}-{end}"
