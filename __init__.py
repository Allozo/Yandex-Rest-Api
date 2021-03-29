from flask import Flask, request, jsonify
import datetime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from constants import courier_type_weight, cost_courier_type

_is_Test = False

application = Flask(__name__)

# создадим объект, который будет использоваться для связи с БД
engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)

'''
    Ниже будут методы необходимые для работы сервера
'''


@application.route("/")
def test():
    return jsonify({"message": "Welcome!"})


# Поля курьера переводятся в json
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
        "working_hours": working_hours,
    }

    return date_json


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
        "assign_time": order.assign_time,
        "complete_time": order.complete_time,
        "courier_id_who_complete": order.courier_id_who_complete
    }

    return date_json


def get_bad_id_for_orders(json_all_orders):
    list_bad_id = []

    for json_order in json_all_orders['data']:
        if None in [json_order['weight'],
                    json_order['region'],
                    json_order['delivery_hours']
                    ] or not (0.01 <= json_order['weight'] <= 50):
            list_bad_id.append({'id': json_order['order_id']})

    return list_bad_id


# Для тестирования раскомментировать вторую строчку с now_time
def time_intersects(courier, order):
    for courier_time in courier.working_hours:
        for order_time in order.delivery_hours:
            start_1 = courier_time.working_hours_start
            end_1 = courier_time.working_hours_end
            start_2 = order_time.delivery_hours_start
            end_2 = order_time.delivery_hours_end

            # Условие пересечения времени
            if start_1 < end_2 and start_2 < end_1:
                str_now_time = datetime.datetime.now().strftime('%H:%M')
                now_time = datetime.datetime.strptime(str_now_time, "%H:%M")
                if _is_Test:
                    now_time = datetime.datetime.strptime("14:01", "%H:%M")
                if start_1 < now_time < end_1 and start_2 < now_time < end_2:
                    return True
    return False


def get_courier_rating(courier_id):
    orders_completing_courier = Orders.query.filter_by(
        courier_id_who_complete=courier_id).all()

    if len(orders_completing_courier) == 0:
        return None

    # Получим словарь регионов - списков order
    dict_list_order_by_region = {}
    for order in orders_completing_courier:
        if order.region not in dict_list_order_by_region:
            dict_list_order_by_region[order.region] = list()
        dict_list_order_by_region[order.region].append(order)

    # Получим словарь регионов - словарей assign_time - списков order
    dict_region_assign_time = {}
    for region, list_order in dict_list_order_by_region.items():
        dict_region_assign_time[region] = {}

        for order in list_order:
            if order.assign_time not in dict_region_assign_time[region]:
                dict_region_assign_time[region][order.assign_time] = []
            dict_region_assign_time[region][order.assign_time].append(order)

    dict_region_time_delivery = {}
    for region, assign_time_list_orders in dict_region_assign_time.items():
        dict_region_time_delivery[region] = []
        for assign_time, list_orders in assign_time_list_orders.items():
            list_delivery_time = []
            datetime_assign_time = datetime.datetime.strptime(
                assign_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            for order in list_orders:
                order_complete_time = order.complete_time
                order_complete_time = datetime.datetime.strptime(
                    order_complete_time, "%Y-%m-%dT%H:%M:%S.%fZ")

                list_delivery_time.append(order_complete_time)

            list_delivery_time.sort()
            list_delivery_time.insert(0, datetime_assign_time)

            # Получили список времен заказов, отсортированых в порядке
            #   их выполнения (в начале стоит assign_time)

            for i in range(len(list_delivery_time) - 1):
                difference_time = abs(
                    (list_delivery_time[i] - list_delivery_time[i + 1]
                     ).total_seconds())
                dict_region_time_delivery[region].append(difference_time)

    # Получим td[i] - среднее время доставки заказы в районе i
    td = {}
    for region, list_time in dict_region_time_delivery.items():
        td[region] = sum(list_time) / len(list_time)
    t = min(td.values())
    rating = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5
    return rating


def get_order_type_assign(orders):
    dict_type_assign_orders = {}
    for order in orders:
        order_type = order.type_courier_who_complete

        if order_type not in dict_type_assign_orders:
            dict_type_assign_orders[order_type] = {}

        if order.assign_time not in dict_type_assign_orders[order_type]:
            dict_type_assign_orders[order_type][order.assign_time] = []

        dict_type_assign_orders[order_type][order.assign_time].append(order)

    return dict_type_assign_orders


def get_courier_earnings(courier_id):
    complete_orders = Orders.query.filter(
        (Orders.courier_id_who_complete == courier_id)
    ).all()

    orders_not_complete = Orders.query.filter(
        (Orders.complete_time.is_(None))
        &
        (Orders.courier_id == courier_id)
    ).all()

    complete_orders_type_assign = get_order_type_assign(complete_orders)
    not_complete_orders_type_assign = get_order_type_assign(orders_not_complete)

    earnings = 0

    for type_order, assign_list_order in complete_orders_type_assign.items():
        for assign_time, list_orders in assign_list_order.items():
            if type_order in not_complete_orders_type_assign:
                if assign_time in not_complete_orders_type_assign[type_order]:
                    continue
            earnings += 500 * cost_courier_type[type_order]

    return earnings


'''
    Ниже методы для сервера, которые нужны для его тестировки
'''


# Тестовый метод для вывода всех курьеров
@application.route('/couriers', methods=['GET'])
def get_couriers():
    all_couriers = Couriers.query.all()

    serialised = []
    for courier in all_couriers:
        date_json_courier = date_courier_in_json(courier)
        date_json_courier['orders'] = str(courier.orders)
        serialised.append(date_json_courier)

    return jsonify(serialised)


# Тестовый метод для удаления всех курьеров
@application.route('/couriers', methods=['DELETE'])
def del_couriers():
    couriers = Couriers.query.all()

    for courier in couriers:
        session.delete(courier)

    session.commit()

    return '', 200


# Тестовый метод для вывода всех заказов
@application.route('/orders', methods=['GET'])
def get_orders():
    all_orders = Orders.query.all()

    serialised = []
    for order in all_orders:
        date_json_order = date_order_in_json(order)
        serialised.append(date_json_order)

    return jsonify(serialised)


# Тестовый метод для удаления всех заказов
@application.route('/orders', methods=['DELETE'])
def del_orders():
    orders = Orders.query.all()

    for order in orders:
        session.delete(order)

    session.commit()

    return '', 200


# Тестовый метод для получения количества заказов всего
@application.route('/orders/count', methods=['GET'])
def get_count_orders():
    return jsonify(len(Orders.query.all())), 200


'''
    Ниже основные методы для сервера
'''


@application.route('/couriers', methods=['POST'])
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


@application.route('/couriers/<int:courier_id>', methods=['PATCH'])
def update_courier(courier_id):
    courier = Couriers.query.filter(
        Couriers.courier_id == courier_id
    ).first()

    params = request.json
    if not courier:
        return '', 404

    # key in ['regions', 'courier_type', 'working_hours']
    # value - новое значение
    for key, value in params.items():
        if key == '' or key is None or value == '' or value is None:
            return '', 400

        if key == 'regions':
            # обнулим существующие регионы
            courier.regions = []

            for new_region in value:
                new_instance_region = CouriersRegions(courier_id=courier_id,
                                                      region=new_region)
                courier.regions.append(new_instance_region)

        if key == 'courier_type':
            courier.courier_type = value

        if key == 'working_hours':
            # Обнулим существующие значения
            courier.working_hours = []

            for new_time in value:
                pair_time = get_time_from_str(new_time)

                new_instance_time = CouriersWorkingTime(
                    courier_id=courier_id,
                    working_hours_start=pair_time[0],
                    working_hours_end=pair_time[1]
                )

                courier.working_hours.append(new_instance_time)

    # Делаем проверку на то, нужно ли убрать какие-то заказы у курьера
    if len(courier.orders) > 0:
        orders = courier.orders
        courier_regions = courier.regions
        courier_regions = [int(str(x)) for x in courier_regions]

        new_orders_list = []

        for order in orders:
            if order.complete_time:
                continue

            if time_intersects(courier, order) and (
                    order.region in courier_regions):
                new_orders_list.append(order)
            else:
                order.assign_time = None
                order.type_courier_who_complete = None
                order.courier = None

        courier.orders = new_orders_list

    session.commit()

    date_courier_json = date_courier_in_json(courier)

    return jsonify(date_courier_json), 200


@application.route('/orders', methods=['POST'])
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


@application.route('/orders/assign', methods=['POST'])
def assigning_order():
    params = request.json

    courier_id = params['courier_id']
    courier = Couriers.query.filter_by(courier_id=courier_id).first()

    if not courier:
        return '', 400

    # Проверим, есть ли у курьера незаконченные заказы
    if len(courier.orders) > 0:
        all_courier_orders = courier.orders
        new_list_order = []
        new_list_order_id = []
        for order in all_courier_orders:
            if order.complete_time is None:
                new_list_order.append(order)
                new_list_order_id.append({'id': order.order_id})

        # Если список не пустой, то ещё есть неразвезённые заказы.
        #   Если список пустой, то занулим список и наберем новые заказы
        #   в основном теле функции
        courier.orders = new_list_order

        if len(new_list_order) > 0:
            session.commit()

            return {
                       "orders": new_list_order_id,
                       "assign_time": new_list_order[0].assign_time
                   }, 200

    # Получим все регионы у заданного курьера
    couriers_region = Couriers.query.filter_by(
        courier_id=courier_id
    ).first().regions
    couriers_region = [int(str(i)) for i in couriers_region]

    # Получим все свободные заказы, подходящие по региону
    orders_with_right_regions = Orders.query.filter(
        Orders.region.in_(couriers_region)
        & Orders.courier_id_who_complete.is_(None)
        & Orders.courier_id.is_(None)
    ).order_by(db.asc(Orders.weight)).all()

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
    assign_time = datetime.datetime.utcnow().isoformat() + "Z"
    for order in right_orders:
        if order.weight + weight_orders <= max_courier_weight:
            weight_orders += order.weight
            order.courier_id = courier.courier_id
            order.assign_time = assign_time
            order.type_courier_who_complete = courier.courier_type
            courier.orders.append(order)
            good_order_id.append({"id": order.order_id})

    session.commit()

    # Если подходящих заказов нет, то вернем сообщение
    if len(good_order_id) == 0:
        return {
                   "orders": []
               }, 200

    return {
               "orders": good_order_id,
               "assign_time": assign_time
           }, 200


@application.route('/orders/complete', methods=['POST'])
def complete_order():
    params = request.json
    courier_id = params['courier_id']
    order_id = params['order_id']
    complete_time = params['complete_time']

    # Проверим, что заказ существует
    order = Orders.query.filter_by(order_id=order_id).first()
    if not order:
        return '', 400

    # Проверим, что курьер существует
    courier = Couriers.query.filter_by(courier_id=courier_id).first()
    if not courier:
        return '', 400

    # Проверим, что у заказа стоит тот курьер
    if order.courier_id != courier_id:
        return '', 400

    order.complete_time = complete_time
    order.courier_id_who_complete = order.courier_id
    order.type_courier_who_complete = courier.courier_type

    session.commit()

    return {
               'order_id': order_id
           }, 200


@application.route('/courier/<int:courier_id>', methods=['GET'])
def get_inf_for_courier(courier_id):
    courier = Couriers.query.filter(
        Couriers.courier_id == courier_id
    ).first()

    if not courier:
        return '', 404

    courier.rating = get_courier_rating(courier_id)
    courier.earnings = get_courier_earnings(courier_id)

    courier_inf_json = date_courier_in_json(courier)
    courier_inf_json["earnings"] = courier.earnings
    if courier.rating is not None:
        courier_inf_json["rating"] = courier.rating
    return courier_inf_json, 200


@application.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    application.run()
