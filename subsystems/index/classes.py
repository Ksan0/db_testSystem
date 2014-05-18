import json
import datetime
import decimal
import bson

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                encoded_object = str(obj)
            elif isinstance(obj, decimal.Decimal):
                encoded_object = str(obj)
            elif isinstance(obj, bson.objectid.ObjectId):
                encoded_object = str(obj)
            else:
                encoded_object =json.JSONEncoder.default(self, obj)
        except:
            encoded_object = None
        return encoded_object


