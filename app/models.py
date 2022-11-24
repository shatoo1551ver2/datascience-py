from django.db import models
from django.core.validators import FileExtensionValidator
import os
# Create your models here.


class FileUpload(models.Model):
    """
    ファイルのアップロード
    """
    title = models.CharField(default='CSVファイル', max_length=50)
    upload_dir = models.FileField(upload_to='csv', validators=[FileExtensionValidator(['csv',])])
    created_at = models.DateField(auto_now_add=True)



    def __str__(self):
        return self.title

    def file_name(self):
        """
        相対パスからファイル名のみを取得するカスタムメソッド
        """
        path = os.path.basename(self.upload_dir.name)
        return path


class Post(models.Model):
    """役職マスタ"""
    name = models.CharField('役職名', max_length=50)

    def __str__(self):
        return self.name