from django.conf import settings
import os

from django.core.signing import Signer, TimestampSigner


class SignData(object):
    def sign(self, data, key=None, sep=':', salt=None, time=False):
        # settings.SECRET_KEY
        if not time:
            singer = Signer(key=key, sep=sep, salt=salt)
            data_signed = singer.sign(data)
        else:
            singer = TimestampSigner(key=key, sep=sep, salt=salt)
            data_signed = singer.sign(data)
        return data_signed

    def unsign(self, data, key=None, sep=':', salt=None, time=None):
        if not time:
            singer = Signer(key=key, sep=sep, salt=salt)
            data_unsigned = singer.unsign(data)
        else:
            singer = TimestampSigner(key=key, sep=sep, salt=salt)
            data_unsigned = singer.unsign(data, time)
        return data_unsigned


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.meiduo_mall.settings.dev')
    singer = SignData()
    data = singer.sign('abc', key=settings.SECRET_KEY,salt='1')
    print(data)
    data = singer.sign('abc', key=settings.SECRET_KEY,salt='1')
    print(data)
    # data=data.split(':')[1]
    # print(data)
    # data=singer.unsign(data)
    # print(data)

