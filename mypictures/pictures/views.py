# from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import File


class IndexView(LoginRequiredMixin, ListView):
    """文件列表视图"""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = File
    template_name = 'pictures/index.html'
    context_object_name = 'files'
    # 分页
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        """分页数据"""
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)
        return context

    @staticmethod
    def pagination_data(paginator, page, is_paginated):
        """分页详细数据"""
        if not is_paginated:
            return {}

        left, right = [], []
        left_has_more, right_has_more = False, False
        first, last = False, False

        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number != total_pages:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        if page_number != 1:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class FileSearch(IndexView):
    """文件搜索结果视图"""
    def get_queryset(self):
        pass


@login_required
def upload(request):
    """上传文件"""
    pass


@login_required
def remove_file(request):
    """删除已上传文件"""
    pass
