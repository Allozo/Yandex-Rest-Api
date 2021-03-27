from app import client


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
    for i in json_couriers:
        print(i)


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
                                             "19:30-23:45"]
                       })
    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "courier_id": 2,
        "courier_type": "foot",
        "regions": [11, 33, 2],
        "working_hours": ["09:00-10:15", "19:30-23:45"]
    }

    assert status_code == right_status_code, status_code
    assert answer_json == right_answer_json, answer_json


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

    assert answer_status_code == right_answer_code,  answer_status_code


def del_orders():
    res = client.delete('/orders')

    answer_status_code = res.status_code
    right_answer_code = 200

    assert answer_status_code == right_answer_code, \
        answer_status_code


def print_orders():
    res = client.get('/orders')
    json_orders = res.get_json()
    for i in json_orders:
        print(i)


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
                                                     "16:00-21:30"]
                              },
                              {
                                  "order_id": 4,
                                  "weight": 23,
                                  "region": 22,
                                  "delivery_hours": ["09:00-20:00"]
                              },
                              {
                                  "order_id": 5,
                                  "weight": 23,
                                  "region": 19,
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


def successful_assigning_order():
    res = client.post('/orders/assign',
                      json={
                          "courier_id": 1
                      }
                      )

    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "orders": [{"id": 1}, {"id": 2}, {"id": 3}],
        "assign_time": "2021-01-10T09:32:14.42Z"
    }

    # assert status_code == right_status_code, status_code
    print(answer_json)


def test_pack():
    del_orders()
    del_couriers()

    successful_post_couriers()
    successful_post_orders()

    successful_assigning_order()

    del_orders()
    del_couriers()


def testing_db():
    del_couriers()
    del_orders()

    successful_post_couriers()
    error_post_couriers()

    successful_patch_courier_regions()
    successful_patch_courier_type()
    successful_patch_courier_working_hours()
    error_patch_courier()

    successful_post_orders()
    error_post_orders()

    # print_couriers()
    # print_orders()

    del_couriers()
    del_orders()

    print_couriers()
    print_orders()


if __name__ == '__main__':
    # test_pack()
    testing_db()
