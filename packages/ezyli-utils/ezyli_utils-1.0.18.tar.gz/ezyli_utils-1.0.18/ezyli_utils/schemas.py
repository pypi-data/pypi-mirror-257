COMMON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "data": {"type": "object"},
        "routing_id": {"type": "string"},
        "user_id": {"type": "integer"},
        "app": {"type": "string"},
        "event": {"type": "string"},
        "meta": {"type": "object"},
    },
    "required": ["data", "routing_id", "user_id", "app", "event", "meta"],
}

UPDATE_ROUTE_DATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "args": {
                    "type": "object",
                    "properties": {
                        "current_position": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 2,
                            "maxItems": 2,


                        },
                        "initial_route_geometry": {
                            "type": "object",
                            "properties": {
                                "type": {"const": "MultiLineString"},
                                "coordinates": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 2,
                                            "maxItems": 2,
                                        },
                                    },
                                },
                            },
                            "required": ["type", "coordinates"],
                        },
                        "break_points": {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "items": {"type": "number"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                        },
                        "optmize_first_path": {"type": "boolean"},
                    },
                    "required": [
                        "current_position",
                        "initial_route_geometry",
                        "break_points",
                        "optmize_first_path",
                    ],
                },
                "receiver": {
                    "type": "object",
                    "properties": {"queue_name": {"type": "string"}},
                    "required": ["queue_name"],
                },
            },
            "required": ["args", "receiver"],
        },
    },
    "required": ["data"],
}


BUILD_ROUTE_DATA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "args": {
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 2,
                            "maxItems": 2,
                        },
                        "destination": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 2,
                            "maxItems": 2,
                        },
                        "waypoints": {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "items": {"type": "number"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                        },
                        "lat_first": {"type": "boolean"},
                    },
                    "required": ["origin", "destination", "waypoints"],
                },
                "receiver": {
                    "type": "object",
                    "properties": {"queue_name": {"type": "string"}},
                    "required": ["queue_name"],
                },
            },
            "required": ["args", "receiver"],
        },
    },
    "required": ["data"],
}


MULTI_TABLE_SERVICE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "args": {
                    "type": "object",
                    "properties": {
                        "coord_params": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "origins": {
                                        "type": "array",
                                        "items": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 2,
                                            "maxItems": 2,
                                        },
                                    },
                                    "destinations": {
                                        "type": "array",
                                        "items": {
                                            "type": "array",
                                            "items": {"type": "number"},
                                            "minItems": 2,
                                            "maxItems": 2,
                                        },
                                    },
                                    # id can be either integer or string
                                    "id": {"type": ["integer", "string"]},
                                },
                                "required": ["origins", "destinations", "id"],
                            },
                        },
                        "mode": {"type": "string"},
                        "matrix_types": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "lat_first": {"type": "boolean"},
                    },
                    "required": ["coord_params", "mode", "matrix_types"],
                },
                "receiver": {
                    "type": "object",
                    "properties": {"queue_name": {"type": "string"}},
                    "required": ["queue_name"],
                },
            },
            "required": ["args", "receiver"],
        },
    },
    "required": ["data"],
}