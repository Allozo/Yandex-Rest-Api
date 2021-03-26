from app import client, Base, engine


res = client.get('/couriers')
print(res.status_code)
print(res.get_json())

# res = client.post('/couriers',
#                   json={
#                       "data": [
#                           {
#                               "courier_id": 11,
#                               "courier_type": "foot",
#                               "regions": [1, 12, 22],
#                               "working_hours": ["11:35-14:05", "09:00-11:00"]
#                           },
#                           {
#                               "courier_id": 12,
#                               "courier_type": "bike",
#                               "regions": [22],
#                               "working_hours": ["09:00-18:00"]
#                           },
#                           {
#                               "courier_id": 13,
#                               "courier_type": "car",
#                               "regions": [12, 22, 23, 33],
#                               "working_hours": []
#                           },
#                       ]
#                   }
#                   )
# print(res.status_code)
# print(res.get_json())
#
#
# res = client.get('/couriers')
# print(res.status_code)
# print(res.get_json())

from models import *
from app import session

# c = Couriers.query.all()
# print(c)
#
# c1 = Couriers(courier_id=10,
#               courier_type=2,
#               regions=3,
#               working_hours="09:00-18:00")

# session.add(c1)
# session.commit()
# c = Couriers.query.all()
# for i in c:
#     print(i.courier_id, i.courier_type, i.regions, i.working_hours)

# Base.metadata.drop_all(engine)