import json
import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            encoded_object = str(obj)
        else:
            encoded_object =json.JSONEncoder.default(self, obj)
        return encoded_object


