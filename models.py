from DeliveryServer import Base
import sqlalchemy as db
from sqlalchemy.orm import relationship


class Couriers(Base):
    __tablename__ = 'Couriers'

    courier_id = db.Column(db.Integer,
                           primary_key=True)
    courier_type = db.Column(db.String(50),
                             nullable=False)
    rating = db.Column(db.Float,
                       nullable=False)
    earnings = db.Column(db.Integer,
                         nullable=False)

    regions = relationship("CouriersRegions",
                           cascade="all, delete, delete-orphan",
                           backref='courier')

    working_hours = relationship("CouriersWorkingTime",
                                 cascade="all, delete, delete-orphan",
                                 backref='courier')
    orders = relationship("Orders",
                          backref='courier')

    def __repr__(self):
        return f"Courier<{self.courier_id}, {self.courier_type}>"


class CouriersWorkingTime(Base):
    __tablename__ = 'CouriersWorkingTime'

    _id = db.Column(db.Integer,
                    primary_key=True)
    courier_id = db.Column(db.Integer,
                           db.ForeignKey('Couriers.courier_id'),
                           nullable=False)
    working_hours_start = db.Column(db.DateTime,
                                    nullable=False)
    working_hours_end = db.Column(db.DateTime,
                                  nullable=False)

    def __repr__(self):
        start = self.working_hours_start.strftime('%H:%M')
        end = self.working_hours_end.strftime('%H:%M')
        return f"{start}-{end}"


class CouriersRegions(Base):
    __tablename__ = "CouriersRegions"

    _id = db.Column(db.Integer,
                    primary_key=True)
    courier_id = db.Column(db.Integer,
                           db.ForeignKey('Couriers.courier_id'),
                           nullable=False)
    region = db.Column(db.Integer,
                       nullable=False)

    def __repr__(self):
        return f"{self.region}"


class Orders(Base):
    __tablename__ = 'Orders'

    order_id = db.Column(db.Integer,
                         primary_key=True)
    weight = db.Column(db.Float,
                       nullable=False)
    assign_time = db.Column(db.String(70),
                            nullable=True)
    complete_time = db.Column(db.String(70),
                              nullable=True)
    region = db.Column(db.Integer,
                       nullable=False)
    courier_id_who_complete = db.Column(db.Integer,
                                        nullable=True)
    type_courier_who_complete = db.Column(db.String(70),
                                          nullable=True)
    courier_id = db.Column(db.Integer,
                           db.ForeignKey('Couriers.courier_id'),
                           nullable=True)

    delivery_hours = relationship("OrderDeliveryTime",
                                  cascade="all, delete, delete-orphan",
                                  backref='order')

    def __repr__(self):
        return f'Order<{self.order_id}>'


class OrderDeliveryTime(Base):
    __tablename__ = 'OrderDeliveryTime'

    _id = db.Column(db.Integer,
                    primary_key=True)
    order_id = db.Column(db.Integer,
                         db.ForeignKey('Orders.order_id'),
                         nullable=False)
    delivery_hours_start = db.Column(db.DateTime,
                                     nullable=False)
    delivery_hours_end = db.Column(db.DateTime,
                                   nullable=False)

    def __repr__(self):
        start = self.delivery_hours_start.strftime('%H:%M')
        end = self.delivery_hours_end.strftime('%H:%M')
        return f"{start}-{end}"
