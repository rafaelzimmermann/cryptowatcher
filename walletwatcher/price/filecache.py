import base64
import os
import time
from model.price import Price

class Serializer:

    def serialize(self, value) -> str:
        raise NotImplementedError()

    def deserialize(self, value: str):
        raise NotImplementedError()


class PriceSerializer(Serializer):

    def serialize(self, value: Price) -> str:
        return value.to_csv()

    def deserialize(self, value: str):
        return Price.from_csv(value)


class FileCache:

    def __init__(self, path, serializer: Serializer = PriceSerializer()):
        self.path = path
        self.serializer = serializer

    def get_item(self, key: str):
        try:
            with open(f'{self.path}{key}', 'r') as _f:
                cache_data = _f.read()
                ttl, value = cache_data.split(',')
                if time.time() < int(ttl):
                    return self.serializer.deserialize(base64.b64decode(value).decode('utf-8'))
        except Exception as e:
            print('Failed to deserialize', e)
        return None

    def set_item(self, key: str, value, ttl: int = 60):
        file_path = f'{self.path}{key}'
        if os.path.exists(file_path):
            try:
                with open(f'{self.path}{key}', 'w') as _f:
                    now = int(time.time() + ttl)
                    b64str = base64.b64encode(bytes(self.serializer.serialize(value), 'utf-8'))
                    
                    _f.write(str(now) + ',' + b64str.decode('utf-8'))
            except Exception as e:
                print('Failed to serialize', e)
        return None

