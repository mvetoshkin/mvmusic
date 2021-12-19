import enum
import json
from datetime import date, datetime, timezone
from uuid import UUID


class RequestMethod(enum.Enum):
    GET = 'get'


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, enum.Enum):
            return o.value
        if isinstance(o, datetime):
            return o.replace(tzinfo=timezone.utc).isoformat()
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, UUID):
            return str(o)
        super(JSONEncoder, self).default(o)
