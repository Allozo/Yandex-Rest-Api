from flask import Flask, request, jsonify
import datetime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

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


def get_bad_id(json_all_couriers):
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

    list_bad_id = get_bad_id(json_all_couriers)

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

        # Добавим регионы для курьеры
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
    regions = list(order.regions)
    regions = [int(str(x)) for x in regions]

    delivery_hours = list(order.delivery_hours)
    delivery_hours = [str(x) for x in delivery_hours]

    date_json = {
        "order_id": order.order_id,
        "weight": order.weight,
        "regions": regions,
        "delivery_hours": delivery_hours
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


@app.route('/orders', methods=['POST'])
def import_orders():
    pass


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()
