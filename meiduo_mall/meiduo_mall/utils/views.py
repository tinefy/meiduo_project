# LoginRequiredJSONMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from meiduo_mall.utils.response_code import RETCODE

# FastDFSView
from django.views import View
from django.http import HttpResponse
from fdfs_client.client import Fdfs_client, get_tracker_conf

# FileView
from django.http import StreamingHttpResponse


class LoginRequiredJSONMixin(LoginRequiredMixin):
    # def handle_no_permission(self):
    #     return JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})
        return super().dispatch(request, *args, **kwargs)


class FastDFSView(View):
    def get(self, request, fastdfs):
        config_ = get_tracker_conf(r'meiduo_mall/meiduo_mall/utils/fastdfs/client.conf')
        client = Fdfs_client(config_)
        ret = client.download_to_buffer(fastdfs.encode())
        content_type = ''
        if fastdfs.endswith('.jpg') or fastdfs.endswith('.jpeg'):
            content_type = 'image/jpeg'
        elif fastdfs.endswith('.png'):
            content_type = 'image/png'
        return HttpResponse(ret['Content'], content_type=content_type)


class FileView(View):
    def get(self, request, url):
        chunk_size = 1024 * 1024
        file_path = '~/'
        file_name = url.split('/')[-1]
        file = file_path + file_name

        def file_iter(file_, chunk_size_):
            with open(file_, 'rb') as fd:
                while True:
                    c = fd.read(chunk_size_)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iter(file, chunk_size))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)  # 下载文件名
        return response
