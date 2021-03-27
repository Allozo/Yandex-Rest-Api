from flask import Flask, request, jsonify
import datetime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from constants import courier_type_weight

app = Flask(__name__)
client = app.test_client()

# создадим объект, который будет использоваться для связи с БД
engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)


# Все поля курьера переводятся в json
def date_courier_in_json(courier):
    # переведем элементы списка в строки
    regions = list(courier.regions)
    regions = [int(str(x)) for x in regions]

    working_hours = list(courier.working_hours)
    working_hours = [str(x) for x in working_hours]

    orders = list(courier.orders)
    orders = [str(x) for x in orders]

    date_json = {
        "courier_id": courier.courier_id,
        "courier_type": courier.courier_type,
        "regions": regions,
        "working_hours": working_hours
    }

    return date_json


# Тестовый метод для вывода всех курьеров
@app.route('/couriers', methods=['GET'])
def get_couriers():
    all_couriers = Couriers.query.all()

    serialised = []
    for courier in all_couriers:
        date_json_courier = date_courier_in_json(courier)
        serialised.append(date_json_courier)

    return jsonify(serialised)


# Тестовый метод для удаления всех курьеров
#  (и их регионов и рабочих часов)
@app.route('/couriers', methods=['DELETE'])
def del_couriers():
    couriers = Couriers.query.all()

    for courier in couriers:
        session.delete(courier)

    session.commit()

    return '', 200


def get_bad_id_for_couriers(json_all_couriers):
    #  Тут будет список тех id, в которых есть неописанные или
    #  отсутствующие поля
    list_bad_id = []

    # Обойдем весь json в поиске отсутствующих значений
    for json_courier in json_all_couriers['data']:
        if None in [json_courier['courier_type'],
                    json_courier['regions'],
                    json_courier['working_hours']
                    ]:
            list_bad_id.append({'id': json_courier['courier_id']})

    return list_bad_id


def get_time_from_str(str_pair_date):
    pair_date = str_pair_date.split('-')
    start_time = datetime.datetime.strptime(pair_date[0], "%H:%M")
    end_time = datetime.datetime.strptime(pair_date[1], "%H:%M")

    return [start_time, end_time]


@app.route('/couriers', methods=['POST'])
def import_couriers():
    json_all_couriers = request.json

    list_bad_id = get_bad_id_for_couriers(json_all_couriers)

    # Если нашли отсутствующие значения, то вернём ошибку
    # и соответствующий json
    if len(list_bad_id) > 0:
        return {
                   "validation_error": {
                       "couriers": list_bad_id
                   }
               }, 400

    # список успешно обработанных id
    list_good_id = []

    # Добавим в базу данных новых курьеров
    for json_courier in json_all_couriers['data']:
        courier_id = json_courier['courier_id']
        courier_type = json_courier['courier_type']
        regions = json_courier['regions']
        working_hours = json_courier['working_hours']

        # Создадим нового курьера
        new_courier = Couriers(courier_id=courier_id,
                               courier_type=courier_type,
                               rating=0,
                               earnings=0)

        # Добавим регионы для курьера
        new_courier.regions = []
        for region in regions:
            new_region = CouriersRegions(courier_id=courier_id,
                                         region=region)
            new_courier.regions.append(new_region)

        # Добавим рабочие часы для курьера
        new_courier.working_hours = []
        for i in working_hours:
            pair_time = get_time_from_str(i)

            new_courier.working_hours.append(
                CouriersWorkingTime(courier_id=courier_id,
                                    working_hours_start=pair_time[0],
                                    working_hours_end=pair_time[1]))

        list_good_id.append({'id': courier_id})

        session.add(new_courier)

    # Коммитим изменения
    session.commit()

    return {
               "couriers": list_good_id
           }, 201


@app.route('/couriers/<int:courier_id>', methods=['PATCH'])
def update_courier(courier_id):
    now_courier = Couriers.query.filter(
        Couriers.courier_id == courier_id).first()

    params = request.json
    if not now_courier:
        return '', 404

    # key in ['regions', 'courier_type', 'working_hours']
    # value - новое значение
    for key, value in params.items():
        if key == '' or key is None or value == '' or value is None:
            return '', 400

        if key == 'regions':
            # обнулим существующие регионы
            now_courier.regions = []

            for new_region in value:
                new_instance_region = CouriersRegions(courier_id=courier_id,
                                                      region=new_region)
                now_courier.regions.append(new_instance_region)

        if key == 'courier_type':
            now_courier.courier_type = value

        if key == 'working_hours':
            # Обнулим существующие значения
            now_courier.working_hours = []

            for new_time in value:
                pair_time = get_time_from_str(new_time)

                new_instance_time = CouriersWorkingTime(courier_id=courier_id,
                                                        working_hours_start=
                                                        pair_time[0],
                                                        working_hours_end=
                                                        pair_time[1])

                now_courier.working_hours.append(new_instance_time)

    # for i in all_regions:
    #     session.delete(i)
    session.commit()

    date_courier_json = date_courier_in_json(now_courier)

    return jsonify(date_courier_json), 200


# Все поля заказа переводятся в json
def date_order_in_json(order):
    # переведем элементы списка в строки

    delivery_hours = list(order.delivery_hours)
    delivery_hours = [str(x) for x in delivery_hours]

    date_json = {
        "order_id": order.order_id,
        "weight": order.weight,
        "region": order.region,
        "delivery_hours": delivery_hours,
        "courier_id": order.courier_id,
        "time_accept": order.time_accept,
        "complete_time": order.complete_time
    }

    return date_json


# Тестовый метод для вывода всех заказов
@app.route('/orders', methods=['GET'])
def get_orders():
    all_orders = Orders.query.all()

    serialised = []
    for order in all_orders:
        date_json_order = date_order_in_json(order)
        serialised.append(date_json_order)

    return jsonify(serialised)


# Тестовый метод для удаления всех заказов
@app.route('/orders', methods=['DELETE'])
def del_orders():
    orders = Orders.query.all()

    for order in orders:
        session.delete(order)

    session.commit()

    return '', 200


def get_bad_id_for_orders(json_all_orders):
    list_bad_id = []

    for json_order in json_all_orders['data']:
        if None in [json_order['weight'],
                    json_order['region'],
                    json_order['delivery_hours']
                    ]:
            list_bad_id.append({'id': json_order['order_id']})

    return list_bad_id


@app.route('/orders', methods=['POST'])
def import_orders():
    json_all_orders = request.json

    list_bad_id = get_bad_id_for_orders(json_all_orders)

    if len(list_bad_id) > 0:
        return {
                   "validation_error": {
                       "orders": list_bad_id
                   }
               }, 400

    list_good_id = []

    for json_order in json_all_orders['data']:
        order_id = json_order['order_id']
        weight = json_order['weight']
        region = json_order['region']
        delivery_hours = json_order['delivery_hours']

        new_order = Orders(order_id=order_id,
                           weight=weight,
                           region=region,
                           courier_id=None)

        # Добавим время доставки для курьера
        new_order.delivery_hours = []
        for i in delivery_hours:
            pair_time = get_time_from_str(i)

            new_order.delivery_hours.append(
                OrderDeliveryTime(order_id=order_id,
                                  delivery_hours_start=pair_time[0],
                                  delivery_hours_end=pair_time[1]))

        list_good_id.append({'id': order_id})

        session.add(new_order)

    # Коммитим изменения
    session.commit()

    return {
               "orders": list_good_id
           }, 201


def time_intersects(courier, order):
    for courier_time in courier.working_hours:
        for order_time in order.delivery_hours:
            start_1 = courier_time.working_hours_start
            end_1 = courier_time.working_hours_end
            start_2 = order_time.delivery_hours_start
            end_2 = order_time.delivery_hours_end

            # Условие пересечения времени
            if start_1 <= end_2 and start_2 <= end_1:
                return True

    return False


@app.route('/orders/assign', methods=['POST'])
def assigning_order():
    params = request.json

    # key = "courier_id"
    # value - сам id
    courier_id = params['courier_id']
    courier = Couriers.query.filter_by(courier_id=courier_id).first()

    if not courier:
        return '', 400

    # Получим все регионы у заданного курьера
    couriers_region = Couriers.query.filter_by(
        courier_id=courier_id
    ).first().regions
    couriers_region = [int(str(i)) for i in couriers_region]

    s = Orders.query.all()

    # Получим все свободные заказы, подходящие по региону
    orders_with_right_regions = Orders.query.filter(
        Orders.region.in_(couriers_region)
        & Orders.courier_id.is_(None)
    ).all()

    # Получим заказы, подходящие по времени
    right_orders = []
    for order in orders_with_right_regions:
        if time_intersects(courier, order):
            right_orders.append(order)

    # Добавим для курьера заказ
    courier.orders = []
    weight_orders = 0
    max_courier_weight = courier_type_weight[courier.courier_type]
    good_order_id = []  # Список order_id, которые добавили курьеру
    for order in right_orders:
        if order.weight + weight_orders <= max_courier_weight:
            courier.orders.append(order)
            weight_orders += order.weight
            order.courier_id = courier.courier_id
            good_order_id.append({"id": order.order_id})

    session.commit()

    # Если подходящих заказов нет, то вернем сообщение
    if len(good_order_id) == 0:
        return {
                   "orders": []
               }, 200

    return {
               "orders": good_order_id,
               "assign_time": datetime.datetime.utcnow().isoformat() + "Z"
           }, 200


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()
