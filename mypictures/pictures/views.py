import os

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, FileResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import File
from .config import ALLOW_EXTENSIONS, UPLOAD_DIR


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

    def get_queryset(self):
        return super(IndexView, self).get_queryset().filter(user=self.request.user, removed=0).order_by('-id')


class FileSearch(IndexView):
    """文件搜索结果视图"""
    def get_queryset(self):
        return super(FileSearch, self).get_queryset().filter(filename__contains=self.kwargs.get('keyword'))


def search(request):
    """搜索"""
    return HttpResponseRedirect(reverse('pictures:search_result', kwargs={'keyword': request.POST.get('q')}))


def get_file(request, filename):
    """返回图片"""
    filepath = os.path.join(UPLOAD_DIR, filename)
    try:
        response = FileResponse(open(filepath, 'rb'))
        return response
    except Exception:
        return Http404


@login_required
def upload(request):
    """上传文件"""
    file = request.FILES['file']
    extension = file.name.split('.')[-1]

    if extension not in ALLOW_EXTENSIONS:
        messages.add_message(request, messages.ERROR, '不支持的文件格式！', extra_tags='danger')
    else:
        myfile = File.create(filename=file.name, user=request.user)
        with open(os.path.join(UPLOAD_DIR, myfile.md5_name), 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        myfile.save()

    ori_page = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(ori_page)


@login_required
def remove(request, pk):
    """删除已上传文件"""
    # 修改状态
    file = get_object_or_404(File, pk=pk)
    file.removed = 1
    file.save()

    # 移除文件
    filepath = os.path.join(UPLOAD_DIR, file.md5_name)
    try:
        os.remove(filepath)
    except Exception:
        pass

    # 返回
    messages.add_message(request, messages.SUCCESS, '文件已删除！', extra_tags='success')
    ori_page = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(ori_page)
