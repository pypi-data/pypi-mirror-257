def avg_environment_duplicated_pipeline() -> [dict]:
    return [{'$group': {'_id': {'date': '$date', 'sensor_id': '$sensor_id'}, 'ids_duplicated': {'$addToSet': '$_id'},
                        'date': {'$first': '$date'}, 'sensor_id': {'$first': '$sensor_id'},
                        'temperature': {'$avg': '$temperature'}, 'humidity': {'$avg': '$humidity'}}}]
