from postgresql_python.types import Column

WEATHER_DB_NAME = 'weather'
WEATHER_TABLE_NAME = 'measurements'
WEATHER_TABLE_STRUCTURE: list[Column] = {
    'columns': [
        {
            'name': 'id',
            'data_type': 'INT',
            'constrains': [
                'GENERATED ALWAYS',
                'AS IDENTITY'
            ]
        },
        {
            'name': 'timestamp',
            'data_type': 'TIMESTAMP',
            'constrains': [
                'NOT NULL'
            ]
        },
        {
            'name': 'temperature',
            'data_type': 'FLOAT'
        },
        {
            'name': 'humidity',
            'data_type': 'FLOAT'
        }
    ]
}
