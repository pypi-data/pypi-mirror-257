def sum_consumption_day_duplicated_pipeline():
    return [{'$group': {'_id': {'date': '$date', 'sensor_id': '$sensor_id'}, 'ids_duplicated': {'$addToSet': '$_id'},
                        'date': {'$first': '$date'}, 'sensor_id': {'$first': '$sensor_id'},
                        'power': {'$sum': '$power'}}}]


def yearly_consumption_pipeline(sensor_id: str):
    return [{'$match': {'sensor_id': sensor_id}},
            {'$group': {'_id': {'$substr': ['$date', 0, 4]}, 'power': {'$sum': '$power'}}}, {'$sort': {'date': 1}},
            {'$project': {'year': '$_id', 'power': '$power'}}]


def monthly_consumption_pipeline(sensor_id: str, n_months: int = 120):
    return [{'$match': {'sensor_id': sensor_id}},
            {'$group': {'_id': {'$substr': ['$date', 0, 7]}, 'date': {'$first': '$date'}, 'power': {'$sum': '$power'}}},
            {'$project': {'year': {'$substr': ['$date', 0, 4]}, 'month': {'$substr': ['$date', 5, 2]},
                          'power': '$power'}}, {
                '$group': {'_id': {'$concat': ['$year', '-', '$month']}, 'year': {'$first': '$year'},
                           'month': {'$first': '$month'}, 'power': {'$sum': '$power'}}}, {"$sort": {"_id": -1}},
            {"$limit": n_months}, {"$sort": {"_id": 1}}]


def monthly_consumption_by_year_pipeline(sensor_id: str, year: str):
    return [{'$match': {'sensor_id': sensor_id}},
            {'$group': {'_id': {'$substr': ['$date', 0, 7]}, 'power': {'$sum': '$power'}}}, {
                '$project': {'year': {'$substr': ['$_id', 0, 4]}, 'month': {'$substr': ['$_id', 5, 2]},
                             'power': '$power'}}, {'$match': {'year': year}}, {'$sort': {'month': 1}}]


def daily_consumption_pipeline(sensor_id: str, n_days: int):
    return [{'$match': {'sensor_id': sensor_id}}, {
        '$group': {'_id': {'$substr': ['$date', 0, 10]}, 'date': {'$first': '$date'}, 'power': {'$sum': '$power'}}},
            {'$sort': {'date': -1}}, {'$limit': n_days}, {'$sort': {'date': 1}},
            {'$project': {'date': '$_id', 'power': '$power'}}]


def daily_consumption_details_pipeline(sensor_id: str, date: str):
    return [{'$match': {'sensor_id': sensor_id, 'date': {'$regex': date}}}, {'$sort': {'date': 1}},
            {'$project': {'power': '$power', 'date': '$date'}}]


def last_hours_consumption_pipeline(sensor_id: str, n_hours: int):
    return [{'$match': {'sensor_id': sensor_id}}, {'$sort': {'date': -1}}, {'$limit': n_hours}, {'$sort': {'date': 1}},
            {'$project': {'power': '$power', 'date': '$date'}}]


def day_and_night_consumption_pipeline(sensor_id: str, n_months: int = 12):
    return [{'$match': {'sensor_id': sensor_id}},
            {'$addFields': {'day': {'$substr': ['$date', 0, 10]}, 'hour': {'$hour': {'$toDate': '$date'}}}}, {
                '$project': {'date': '$date', 'power_day': {
                    '$cond': {'if': {'$and': [{'$gte': ['$hour', 5]}, {'$lte': ['$hour', 17]}]}, 'then': '$power',
                              'else': 0}}, 'power_night': {
                    '$cond': {'if': {'$or': [{'$gte': ['$hour', 18]}, {'$lte': ['$hour', 4]}]}, 'then': '$power',
                              'else': 0}}}}, {
                '$group': {'_id': {'$substr': ['$date', 0, 7]}, 'power_day': {'$sum': '$power_day'},
                           'power_night': {'$sum': '$power_night'}}},
            {'$project': {'month': '$_id', 'power_day': '$power_day', 'power_night': '$power_night'}},
            {'$sort': {'month': -1}}, {'$limit': n_months}, {'$sort': {'month': 1}}]
