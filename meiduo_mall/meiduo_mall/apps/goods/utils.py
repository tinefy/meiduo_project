def get_breadcrumb(category):
    """获取面包屑导航"""
    breadcrumb = {}
    if category.parent is None:
        # 当前类别为一级类别
        breadcrumb['category_level_1'] = category
    elif category.parent is not None and category.goodscategory_set.count() != 0:
        # 当前类别为二级
        breadcrumb['category_level_1'] = category.parent
        breadcrumb['category_level_2'] = category
    elif category.goodscategory_set.count() == 0:
        # 当前类别为三级
        breadcrumb['category_level_1'] = category.parent.parent
        breadcrumb['category_level_2'] = category.parent
        breadcrumb['category_level_3'] = category
    return breadcrumb
