def yearly_generation_pipeline():
    return [{'$group': {'_id': {'$substr': ['$date', 0, 4]}, 'year': {'$first': {'$substr': ['$date', 0, 4]}},
                        'power': {'$sum': '$power'}}}, {'$sort': {'_id': 1}}]


def monthly_generation_pipeline(year: str, limit: int):
    if year:
        return [
            {'$group': {'_id': {'$substr': ['$date', 0, 7]}, 'year': {'$first': {'$substr': ['$date', 0, 4]}},
                        'month': {'$first': {'$substr': ['$date', 5, 2]}}, 'power': {'$sum': '$power'}}},
            {'$match': {'year': '2023'}}, {'$sort': {'_id': 1}}, {'$project': {'month': '$month', 'power': '$power'}}
        ]
    else:
        return [{'$group': {'_id': {'$substr': ['$date', 0, 7]}, 'year': {'$first': {'$substr': ['$date', 0, 4]}},
                            'month': {'$first': {'$substr': ['$date', 5, 2]}}, 'power': {'$sum': '$power'}}},
                {'$sort': {'_id': -1}}, {'$limit': limit}, {'$sort': {'_id': 1}},
                {'$project': {'month': '$_id', 'power': '$power'}}]
