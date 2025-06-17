from django.shortcuts import render
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from mdapp.models import Mdfile, Share
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse

from .services import converter, pdf_gerater, img_generater
from .forms import CreateMdfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

def index(request):
    return render(request, 'mdapp/index.html')

class List(LoginRequiredMixin, ListView):
    model = Mdfile
    template_name = "mdapp/index.html"
    def get_queryset(self):
        return Mdfile.objects.filter(user=self.request.user)

class Detail(LoginRequiredMixin, DeleteView):
    model = Mdfile
    template_name = "mdapp/detail.html"
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("存在しない記事です")
        return obj

class CreateFile(LoginRequiredMixin, CreateView):
    model = Mdfile
    form_class = CreateMdfileForm
    template_name = "mdapp/create.html"
    # success_url = reverse_lazy('mdapp:index')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # ここで user を渡す
        return kwargs
    def form_valid(self, form):
        self.object = form.save(commit=False)  # 明示的にobjectを更新
        self.object.user = self.request.user
        isinstance = form.instance
        isinstance.html_text = converter.markdown_to_html(isinstance.base_text)
        pdf_bytes = pdf_gerater.generater(isinstance.html_text)
        isinstance.url = img_generater.generate_image_from_pdf(pdf_bytes, isinstance.title)
        self.object.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('mdapp:ditail', kwargs={'pk': self.object.id})

class UpdateFile(LoginRequiredMixin, UpdateView):
    model = Mdfile
    form_class = CreateMdfileForm
    template_name = "mdapp/create.html"
    # success_url = reverse_lazy('mdapp:index')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # ここで user を渡す
        return kwargs
    def form_valid(self, form):
        self.object = form.save()  # 明示的にobjectを更新
        self.object.user = self.request.user
        isinstance = form.instance
        isinstance.html_text = converter.markdown_to_html(isinstance.base_text)
        # imgを作成してS3に保存
        pdf_bytes = pdf_gerater.generater(isinstance.html_text)
        isinstance.url = img_generater.generate_image_from_pdf(pdf_bytes, isinstance.title)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('mdapp:ditail', kwargs={'pk': self.object.id})
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("存在しない記事です")
        return obj

class Delet(LoginRequiredMixin, DeleteView):
    model = Mdfile
    template_name = "mdapp/detail.html"  # Getの際は詳細へ
    success_url = reverse_lazy('mdapp:index')
    def get_success_url(self):
        return reverse_lazy('mdapp:index')
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        referrer_url = self.request.META.get('HTTP_REFERER')
        if referrer_url:
            return HttpResponseRedirect(referrer_url)  # リクエストしてきたページ
        return HttpResponseRedirect(reverse_lazy('mdapp:ditail', kwargs={'pk': id}))  # 分からなければ詳細
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)  
        if obj.user != self.request.user:
            raise Http404("存在しない記事です")
        return obj

@login_required
def get_pdf_bytedeta(request, pk):
    try:
        mdfile_instance = Mdfile.objects.get(pk=pk) 

        if mdfile_instance.user != request.user:
            raise Http404("存在しない記事です")

        html_text = mdfile_instance.html_text
        title = mdfile_instance.title
        pdf_bytes = pdf_gerater.generater(html_text)
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        # Content-Disposition ヘッダーを設定して、ダウンロード時のファイル名を指定
        # 'inline' にするとブラウザで直接開かれ、'attachment' にするとダウンロードダイアログが表示される
        # response['Content-Disposition'] = 'inline; filename="generated_report.pdf"'
        # ダウンロードさせる場合
        response['Content-Disposition'] = f"""attachment; filename="{title}.pdf" """
        return response
    except Mdfile.DoesNotExist:
        # 指定された pk の Mdfile が見つからない場合の処理
        return HttpResponse("指定された記事が見つかりませんでした。", status=404)
    except Exception as e:
        # その他の予期せぬエラー
        print(f"ビュー関数内でエラーが発生しました: {e}")
        return HttpResponse(f"エラーが発生しました: {e}", status=500)
    
@login_required
def generate_thumbnail(request, pk):
    try:
        mdfile_instance = Mdfile.objects.get(pk=pk)
        if mdfile_instance.user != request.user:
            raise Http404("存在しない記事です")
        html_text = mdfile_instance.html_text
        title = mdfile_instance.title
        pdf_bytes = pdf_gerater.generater(html_text)
        img_url = img_generater.generate_image_from_pdf(pdf_bytes, title)
        json_data = {
            'status': 'success',
            'message': 'サムネイル画像の生成に成功しました。',
            'img_url': img_url
        }
        return HttpResponse(json_data, content_type='application/json')
    except Mdfile.DoesNotExist:
        # 指定された pk の Mdfile が見つからない場合の処理
        return HttpResponse("指定された記事が見つかりませんでした。", status=404)
    except Exception as e:
        # その他の予期せぬエラー
        print(f"ビュー関数内でエラーが発生しました: {e}")
        return HttpResponse(f"エラーが発生しました: {e}", status=500)
    
@login_required
@require_POST
def share(request, pk):
    if request.method == "GET":
        return HttpResponse("getリクエストはありません", status=404)
        
