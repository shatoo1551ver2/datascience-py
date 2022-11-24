from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, get_object_or_404  # 追記
from django.http import HttpResponse
from .models import FileUpload,Post

from django.http import JsonResponse

from django_pandas.io import pd  # 追記
import csv
import io
import urllib
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CSVUploadForm, DocumentForm
from .models import Post,FileUpload

from . import graph
from . import tables

def starter(request):
    return render(request, 'app/starter.html')
def index(request):
    return render(request, 'app/index.html')

def data(request):
    return render(request, 'app/data.html')
def index2(request):
    """
    トップページ
    """
    if request.method == 'POST':
        pk = request.POST.get("pk",None)
        if pk:
            form = DocumentForm()
            documents = FileUpload.objects.all()            
            pk = request.POST.get("pk",None)
            file_value = get_object_or_404(FileUpload, id=pk)
            df = pd.read_csv(file_value.upload_dir.path, index_col=0)
            """データ型が文字列のもの集めた配列"""
            columns=df.columns.tolist()
            object={}
            for i in columns:
                a=df[i].dtype
                object[i] = a
            objectlist = [k for k, v in object.items() if v == 'object']
            """欠損値があるものもの集めた配列"""
            nulllist=df.isnull().sum().tolist()
            columnlist=df.columns.tolist()
            nulldic = {key: val for key, val in zip(columnlist, nulllist)}
            """相関関係のグラフ表示"""
            chart = graph.Plot_Graph(df)
            """相関関係のグラフ表示"""
            calc_cor_df=tables.calc_corr(df).sort_values('corr', ascending=False)
            return render(request, 'app/index2.html', {
            'form': form,
            'documents': documents,
            'file_value': file_value,
            'df': df,
            'objectlist': objectlist,
            'nulldic': nulldic,
            'calc_cor_df': calc_cor_df,
            })
        else:            
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                documents = FileUpload.objects.all()
                return render(request, 'app/index2.html', {
                'documents': documents,
                'form': form,
                })
    else:
        form = DocumentForm()
        documents = FileUpload.objects.all()
        return render(request, 'app/index2.html', {
            'form': form,
            'documents': documents
        })

def detail(request):
    pk = request.POST.get("pk",None)
    """
    詳細ページ
    """
    file_value = get_object_or_404(FileUpload, id=pk)
    df = pd.read_csv(file_value.upload_dir.path, index_col=0)
    form = DocumentForm()
    documents = FileUpload.objects.all()
    context = {
            'file_value': file_value,
            'df': df,
            'form': form,
            'documents': documents
    }
    return render(request, 'app/detail.html', context)

class List(generic.ListView):
    """
    役職テーブルの一覧表作成
    """
    model = Post
    template_name = 'app/list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_name'] = 'app'
        return ctx

class PostImport(generic.FormView):
    """
    役職テーブルの登録(csvアップロード)
    """
    template_name = 'app/import.html'
    success_url = reverse_lazy('app:list')
    form_class = CSVUploadForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_name'] = 'csvdownload'
        return ctx

    def form_valid(self, form):
        """postされたCSVファイルを読み込み、役職テーブルに登録します"""
        csvfile = io.TextIOWrapper(form.cleaned_data['file'])
        reader = csv.reader(csvfile)
        for row in reader:
            """
            役職テーブルを役職コード(primary key)で検索します
            """
            post, created = Post.objects.get_or_create(pk=row[0])
            post.name = row[1]
            post.save()
        return super().form_valid(form)

def PostExport(request):
    """
    役職テーブルを全件検索して、CSVファイルを作成してresponseに出力します。
    """
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    filename = urllib.parse.quote((u'CSVファイル.csv').encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
    writer = csv.writer(response)
    for post in Post.objects.all():
        writer.writerow([post.pk, post.name])
    return response


def modelform_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DocumentForm()
    return render(request, 'modelform_upload.html', {
        'form': form
    })