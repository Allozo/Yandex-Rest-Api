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
                                  "working_hours": ["10:00-11:00"]
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


def successful_put_courier_regions():
    # пример из ТЗ
    res = client.put('/couriers/2',
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


def successful_put_courier_type():
    # Пример не из ТЗ

    res = client.put('/couriers/2',
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


def successful_put_courier_working_hours():
    # Пример не из ТЗ

    res = client.put('/couriers/2',
                     json={
                         "working_hours": ["09:00-09:15", "09:30-09:45"]
                     })
    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 200
    right_answer_json = {
        "courier_id": 2,
        "courier_type": "foot",
        "regions": [11, 33, 2],
        "working_hours": ["09:00-09:15", "09:30-09:45"]
    }

    assert status_code == right_status_code, status_code
    assert answer_json == right_answer_json, answer_json


def error_put_courier():
    res = client.put('/couriers/12',
                     json={
                         "working_hours": ["09:00-09:15", "09:30-09:45"]
                     })
    status_code = res.status_code
    answer_json = res.get_json()

    right_status_code = 404
    right_answer_json = ''

    assert status_code == right_status_code, status_code


def del_couriers():
    res = client.delete('/couriers')

    answer_status_code = res.status_code
    right_answer_code = 200

    assert answer_status_code == right_answer_code, answer_status_code


def test_pack():
    print('-----------------------')
    del_couriers()
    successful_post_couriers()
    print_couriers()
    print('-----------------------')

    print_couriers()

    successful_put_courier_regions()
    successful_put_courier_type()
    successful_put_courier_working_hours()

    error_put_courier()

    print_couriers()

    print('-----------------------')
    del_couriers()
    print_couriers()


def testing_db():
    del_couriers()
    successful_post_couriers()
    error_post_couriers()
    successful_put_courier_regions()
    successful_put_courier_type()
    successful_put_courier_working_hours()
    error_put_courier()
    del_couriers()
    print_couriers()


if __name__ == '__main__':
    # test_pack()
    testing_db()
