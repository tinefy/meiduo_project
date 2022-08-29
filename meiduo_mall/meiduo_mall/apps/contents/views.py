from collections import OrderedDict

from django.shortcuts import render
from django.views import View

# Create your views here.
from goods.models import GoodsChannel


class IndexView(View):
    def get(self, request):
        # categories = OrderedDict()
        categories = dict()
        channels = GoodsChannel.objects.order_by('group_id', 'sequence')
        for channel in channels:
            group_id = channel.group_id
            if group_id not in categories:
                categories[group_id] = {
                    'channels': [],
                    'sub_cats': [],
                }
            category_in_level_1 = channel.category
            categories[group_id]['channels'].append(
                {
                    'id': category_in_level_1.id,
                    'name': category_in_level_1.name,
                    'url': channel.url,
                }
            )
            # for category_in_level_2 in category_in_level_1.subs.all():
            for category_in_level_2 in category_in_level_1.goodscategory_set.all():
                category_in_level_2_sub_cats = []
                for category_in_level_3 in category_in_level_2.goodscategory_set.all():
                    category_in_level_2_sub_cats.append(
                        {
                            'id': category_in_level_3.id,
                            'name': category_in_level_3.name
                        }
                    )
                categories[group_id]['sub_cats'].append(
                    {
                        "id": category_in_level_2.id,
                        "name": category_in_level_2.name,
                        "sub_cats": category_in_level_2_sub_cats
                    }
                )
        print(categories)
        return render(request, 'index.html')
