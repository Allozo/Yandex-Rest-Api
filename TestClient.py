from app import app
import json

client = app.test_client()


def successful_post_couriers():
    res = client.post('/couriers',
                      json={
                          "data": [
                              {
                                  "courier_id": 1,
                                  "courier_type": "foot",
                                  "regions": [1, 12, 22],
                                  "working_hours": ["11:35-14:05",
                                                    "09:00-11:00"]
                              },
                              {
                                  "courier_id": 2,
                                  "courier_type": "bike",
                                  "regions": [22],
                                  "working_hours": ["09:00-18:00"]
                              },
                              {
                                  "courier_id": 3,
                                  "courier_type": "car",
                                  "regions": [12, 22, 23, 33],
                                  "working_hours": ["09:00-15:00"]
                              },

                          ]
                      }
                      )
    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 201
    right_answer_json = {'couriers': [{'id': 1},
                                      {'id': 2},
                                      {'id': 3}
                                      ]
                         }

    assert status_code == right_status_code, status_code
    assert answer_json == right_answer_json, answer_json


# Отправляем в полях None
def error_post_couriers():
    res = client.post('/couriers',
                      json={
                          "data": [
                              {
                                  "courier_id": 1,
                                  "courier_type": "foot",
                                  "regions": [1, 12, 22],
                                  "working_hours": ["11:35-14:05",
                                                    "09:00-11:00"]
                              },
                              {
                                  "courier_id": 2,
                                  "courier_type": "bike",
                                  "regions": None,
                                  "working_hours": ["09:00-18:00"]
                              },
                              {
                                  "courier_id": 3,
                                  "courier_type": "car",
                                  "regions": [12, 22, 23, 33],
                                  "working_hours": None
                              },
                          ]
                      }
                      )
    status_code = res.status_code
    answer_json = res.get_json()

    expected_error_json = {'validation_error': {'couriers': [{'id': 2},
                                                             {'id': 3}
                                                             ]
                                                }
                           }

    assert status_code == 400, status_code
    assert answer_json == expected_error_json, answer_json


def print_couriers():
    res = client.get('/couriers')
    json_couriers = res.get_json()
    print(json.dumps(json_couriers, sort_keys=True, indent=4))
    # for i in json_couriers:
    #     print(i)


def successful_patch_courier_regions():
    # пример из ТЗ
    res = client.patch('/couriers/2',
                       json={
                           "regions": [11, 33, 2]
                       })
    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "courier_id": 2,
        "courier_type": "bike",
        "regions": [11, 33, 2],
        "working_hours": ["09:00-18:00"]
    }

    assert status_code == right_status_code, status_code
    assert answer_json == right_answer_json, answer_json


def successful_patch_courier_type():
    # Пример не из ТЗ

    res = client.patch('/couriers/2',
                       json={
                           "courier_type": "foot"
                       })
    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "courier_id": 2,
        "courier_type": "foot",
        "regions": [11, 33, 2],
        "working_hours": ["09:00-18:00"]
    }

    assert status_code == right_status_code, status_code
    assert answer_json == right_answer_json, answer_json


def successful_patch_courier_working_hours():
    # Пример не из ТЗ

    res = client.patch('/couriers/2',
                       json={
                           "working_hours": ["09:00-10:15",
                                             "14:30-23:45"]
                       })
    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "courier_id": 2,
        "courier_type": "foot",
        "regions": [11, 33, 2],
        "working_hours": ["09:00-10:15", "14:30-23:45"]
    }

    assert status_code == right_status_code, status_code
    assert answer_json == right_answer_json, answer_json


# Отправляем id, которого нет
def error_patch_courier():
    res = client.patch('/couriers/12',
                       json={
                           "working_hours": ["09:00-09:15",
                                             "09:30-09:45"]
                       })
    status_code = res.status_code

    right_status_code = 404

    assert status_code == right_status_code, status_code


def del_couriers():
    res = client.delete('/couriers')

    answer_status_code = res.status_code
    right_answer_code = 200

    assert answer_status_code == right_answer_code, answer_status_code


def del_orders():
    res = client.delete('/orders')

    answer_status_code = res.status_code
    right_answer_code = 200

    assert answer_status_code == right_answer_code, \
        answer_status_code


def print_orders():
    res = client.get('/orders')
    json_orders = res.get_json()
    print(json.dumps(json_orders, sort_keys=True, indent=4))
    # for i in json_orders:
    #     print(i)


def successful_post_orders():
    res = client.post('/orders',
                      json={
                          "data": [
                              {
                                  "order_id": 1,
                                  "weight": 0.23,
                                  "region": 12,
                                  "delivery_hours": ["09:00-18:00"]
                              },
                              {
                                  "order_id": 2,
                                  "weight": 15,
                                  "region": 1,
                                  "delivery_hours": ["09:00-18:00"]
                              },
                              {
                                  "order_id": 3,
                                  "weight": 0.1,
                                  "region": 22,
                                  "delivery_hours": ["11:00-12:00",
                                                     "14:00-21:30"]
                              },
                              {
                                  "order_id": 4,
                                  "weight": 20,
                                  "region": 22,
                                  "delivery_hours": ["14:00-20:00"]
                              },
                              {
                                  "order_id": 5,
                                  "weight": 30,
                                  "region": 33,
                                  "delivery_hours": ["09:00-20:00"]
                              }
                          ]
                      }

                      )
    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 201
    right_answer_json = {'orders': [{'id': 1},
                                    {'id': 2},
                                    {'id': 3},
                                    {'id': 4},
                                    {'id': 5}
                                    ]
                         }

    assert status_code == right_status_code, status_code
    assert answer_json == right_answer_json, answer_json


# Отправляем поля с None
def error_post_orders():
    res = client.post('/orders',
                      json={
                          "data": [
                              {
                                  "order_id": 1,
                                  "weight": 0.23,
                                  "region": 12,
                                  "delivery_hours": ["09:00-18:00"]
                              },
                              {
                                  "order_id": 2,
                                  "weight": None,
                                  "region": 1,
                                  "delivery_hours": ["09:00-18:00"]
                              },
                              {
                                  "order_id": 3,
                                  "weight": 0.01,
                                  "region": 22,
                                  "delivery_hours": None
                              }
                          ]
                      }
                      )
    status_code = res.status_code
    answer_json = res.get_json()

    expected_error_json = {'validation_error': {'orders': [{'id': 2},
                                                           {'id': 3}
                                                           ]
                                                }
                           }

    assert status_code == 400, status_code
    assert answer_json == expected_error_json, answer_json


def successful_assigning_order_courier_1():
    res = client.post('/orders/assign',
                      json={
                          "courier_id": 1
                      }
                      )

    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    '''
        Если падает тут, то стоит обратить внимаение на порядок id
    '''
    right_answer_json = {
        "orders": [{"id": 3}, {"id": 1}],
        "assign_time": "2021-01-10T09:32:14.42Z"
    }

    assert status_code == right_status_code, status_code
    assert answer_json['orders'] == right_answer_json['orders'], answer_json


def successful_assigning_order_courier_2():
    res = client.post('/orders/assign',
                      json={
                          "courier_id": 2
                      }
                      )

    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "orders": [],
    }

    assert status_code == right_status_code, status_code
    assert answer_json['orders'] == right_answer_json['orders'], answer_json


def successful_assigning_order_courier_3():
    res = client.post('/orders/assign',
                      json={
                          "courier_id": 3
                      }
                      )

    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "orders": [{'id': 4}, {'id': 5}]
    }

    assert status_code == right_status_code, status_code
    assert answer_json['orders'] == right_answer_json['orders'], answer_json


def successful_assigning_order_courier_1_after_complete():
    res = client.post('/orders/assign',
                      json={
                          "courier_id": 1
                      }
                      )

    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "orders": [{"id": 3}],
        "assign_time": "2021-01-10T09:32:14.42Z"
    }

    assert status_code == right_status_code, status_code
    assert answer_json['orders'] == right_answer_json['orders'], answer_json


# Отправляем несуществующий id
def error_assigning_order():
    res = client.post('/orders/assign',
                      json={
                          "courier_id": 30
                      }
                      )

    status_code = res.status_code

    right_status_code = 400

    assert status_code == right_status_code, status_code


def successful_complete_order_1():
    res = client.post('/orders/complete',
                      json={
                          "courier_id": 1,
                          "order_id": 1,
                          "complete_time": "2021-01-10T10:33:01.42Z"
                      })

    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "order_id": 1
    }

    assert status_code == right_status_code, status_code
    assert answer_json == right_answer_json, answer_json


def successful_complete_order_4():
    res = client.post('/orders/complete',
                      json={
                          "courier_id": 3,
                          "order_id": 4,
                          "complete_time": "2021-01-20T20:33:01.42Z"
                      })

    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "order_id": 4
    }

    assert status_code == right_status_code, status_code
    assert answer_json == right_answer_json, answer_json


def successful_complete_order_3():
    res = client.post('/orders/complete',
                      json={
                          "courier_id": 1,
                          "order_id": 3,
                          "complete_time": "2018-01-20T20:33:01.42Z"
                      })

    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "order_id": 3
    }

    assert status_code == right_status_code, status_code
    assert answer_json == right_answer_json, answer_json


# Для заказа неправильно указан курьер
def error_complete_order():
    res = client.post('/orders/complete',
                      json={
                          "courier_id": 12,
                          "order_id": 4,
                          "complete_time": "2021-01-20T20:33:01.42Z"
                      })

    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 400

    assert status_code == right_status_code, status_code


def successful_assigning_order_1_finally():
    res = client.post('/orders/assign',
                      json={
                          "courier_id": 1
                      }
                      )

    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "orders": [],
        "assign_time": "2021-01-10T09:32:14.42Z"
    }

    assert status_code == right_status_code, status_code
    assert answer_json['orders'] == right_answer_json['orders'], answer_json


def successful_patch_courier_3_regions():
    # пример из ТЗ
    res = client.patch('/couriers/3',
                       json={
                           "regions": [12, 21, 22]
                       })
    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "courier_id": 3,
        "courier_type": "car",
        "regions": [12, 21, 22],
        "working_hours": ["09:00-15:00"]
    }

    assert status_code == right_status_code, status_code
    assert answer_json == right_answer_json, answer_json


def print_count_orders():
    res = client.get('/orders/count')
    json_orders = res.get_json()
    print(json_orders)


def print_inf_for_courier_1():
    res = client.get('/courier/1')

    answer_status_code = res.status_code
    answer_json = res.get_json()

    # print(json.dumps(answer_json, sort_keys=True, indent=4))

    right_status_code = 200
    right_json = {
        "courier_id": 1,
        "courier_type": "foot",
        "earnings": 1000,
        "rating": 0.0,
        "regions": [
            1,
            12,
            22
        ],
        "working_hours": [
            "11:35-14:05",
            "09:00-11:00"
        ]
    }

    assert answer_status_code == right_status_code, answer_status_code
    assert answer_json == right_json, answer_json


def print_inf_for_courier_2():
    res = client.get('/courier/2')

    answer_status_code = res.status_code
    answer_json = res.get_json()

    # print(json.dumps(answer_json, sort_keys=True, indent=4))

    right_status_code = 200
    right_json = {
        "courier_id": 2,
        "courier_type": "bike",
        "earnings": 0,
        "regions": [
            22
        ],
        "working_hours": [
            "09:00-18:00"
        ]
    }

    assert answer_status_code == right_status_code, answer_status_code
    assert answer_json == right_json, answer_json


def print_inf_for_courier_3():
    res = client.get('/courier/3')

    answer_status_code = res.status_code
    answer_json = res.get_json()

    # print(json.dumps(answer_json, sort_keys=True, indent=4))

    right_status_code = 200
    right_json = {
        "courier_id": 3,
        "courier_type": "car",
        "earnings": 4500,
        "rating": 0.0,
        "regions": [
            12,
            21,
            22
        ],
        "working_hours": [
            "09:00-15:00"
        ]
    }

    assert answer_status_code == right_status_code, answer_status_code
    assert answer_json == right_json, answer_json


def test_pack():
    del_orders()
    del_couriers()

    successful_post_couriers()
    successful_post_orders()

    successful_assigning_order_courier_1()
    successful_assigning_order_courier_2()
    successful_assigning_order_courier_3()

    successful_complete_order_1()
    error_complete_order()
    successful_complete_order_4()

    successful_assigning_order_courier_1_after_complete()
    successful_complete_order_3()

    successful_assigning_order_1_finally()

    successful_patch_courier_3_regions()

    print_inf_for_courier_1()
    print_inf_for_courier_2()
    print_inf_for_courier_3()

    del_orders()
    del_couriers()


if __name__ == '__main__':
    test_pack()
