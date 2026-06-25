"""
Common JSON schemas for RPC API response validation.
"""

# Schema for get_by_code response (used in v2 and v3)
GET_BY_CODE_RESPONSE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "altText": {"oneOf": [{"type": "null"}, {"type": "string"}]},
        "card_type": {"type": "string"},
        "code": {"type": "string"},
        "donate": {
            "type": "object",
            "properties": {
                "show_button": {"type": "boolean"},
                "title": {"type": "string"},
                "url": {"type": "string"},
            },
            "required": ["show_button", "title", "url"],
        },
        "name": {"type": "string"},
        "plCapital": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
        "plCapital_notes": {"oneOf": [{"type": "null"}, {"type": "string"}]},
        "plNotGlobEnt": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
        "plNotGlobEnt_notes": {"oneOf": [{"type": "null"}, {"type": "string"}]},
        "plRegistered": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
        "plRegistered_notes": {"oneOf": [{"type": "null"}, {"type": "string"}]},
        "plRnD": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
        "plRnD_notes": {"oneOf": [{"type": "null"}, {"type": "string"}]},
        "plScore": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
        "plWorkers": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
        "plWorkers_notes": {"oneOf": [{"type": "null"}, {"type": "string"}]},
        "product_id": {"oneOf": [{"type": "null"}, {"type": "integer"}]},
        "report_button_text": {"type": "string"},
        "report_button_type": {"type": "string"},
        "report_text": {"type": "string"},
    },
    "required": [
        "altText",
        "card_type",
        "code",
        "donate",
        "name",
        "plCapital",
        "plCapital_notes",
        "plNotGlobEnt",
        "plNotGlobEnt_notes",
        "plRegistered",
        "plRegistered_notes",
        "plRnD",
        "plRnD_notes",
        "plScore",
        "plWorkers",
        "plWorkers_notes",
        "product_id",
        "report_button_text",
        "report_button_type",
        "report_text",
    ],
}

# Schema for create_report response (v2 with id and signed_requests)
CREATE_REPORT_V2_RESPONSE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "signed_requests": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["id", "signed_requests"],
}

# Schema for create_report response (v3 - includes id in response but only signed_requests is required)
CREATE_REPORT_V3_RESPONSE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "signed_requests": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["signed_requests"],
}

# Schema for update_report response
UPDATE_REPORT_RESPONSE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {"id": {"type": "integer"}},
    "required": ["id"],
}

# Schema for attach_file response (v2 - uses signed_request)
ATTACH_FILE_V2_RESPONSE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {"signed_request": {"type": "array", "items": {"type": "string"}}},
    "required": ["signed_request"],
}

# Schema for add_ai_pics response (v3 - uses signed_requests)
ADD_AI_PICS_RESPONSE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {"signed_requests": {"type": "array", "items": {"type": "string"}}},
    "required": ["signed_requests"],
}
