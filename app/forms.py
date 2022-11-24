from django import forms
from app.models import FileUpload

class CSVUploadForm(forms.Form):
    file = forms.FileField(label='CSVファイル')


class DocumentForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('title', 'upload_dir', )


