import os
import time

from django.core import signing

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.meiduo_mall.settings.dev')
    data = 'abc'
    data = signing.dumps(data)
    print(data)
    time.sleep(6)
    data = signing.loads(data, max_age=5)
    print(data)
