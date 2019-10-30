import hashlib

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class File(models.Model):
    """上传的文件信息"""
    filename = models.CharField('文件名', max_length=128)
    upload_date = models.DateTimeField('上传时间', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    md5_name = models.CharField('加密名称', max_length=64)

    def __init__(self, filename, user):
        super().__init__()
        self.filename = filename
        self.user = user
        self.md5_name = self._generate_md5_name()

    def _generate_md5_name(self):
        """生成md5加密后的名称"""
        return hashlib.md5(self.filename.encode('utf-8')).hexdigest() + '.' + self.filename.split('.')[-1]
