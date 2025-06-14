from django.shortcuts import render
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from mdapp.models import Mdfile
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CreateMdfileForm
from . import converter, pdf_gerater


def index(request):
    return render(request, 'mdapp/index.html')

class List(ListView):
    model = Mdfile
    template_name = "mdapp/index.html"

class Detail(DeleteView):
    model = Mdfile
    template_name = "mdapp/detail.html"

class CreateFile(CreateView):
    model = Mdfile
    form_class = CreateMdfileForm
    template_name = "mdapp/create.html"
    # success_url = reverse_lazy('mdapp:index')
    def form_valid(self, form):
        self.object = form.save(commit=False)  # 明示的にobjectを更新
        isinstance = form.instance
        isinstance.html_text = converter.markdown_to_html(isinstance.base_text)
        self.object.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('mdapp:ditail', kwargs={'pk': self.object.id})

class UpdateFile(UpdateView):
    model = Mdfile
    form_class = CreateMdfileForm
    template_name = "mdapp/create.html"
    # success_url = reverse_lazy('mdapp:index')
    def form_valid(self, form):
        self.object = form.save()  # 明示的にobjectを更新
        isinstance = form.instance
        isinstance.html_text = converter.markdown_to_html(isinstance.base_text)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('mdapp:ditail', kwargs={'pk': self.object.id})

class Delet(DeleteView):
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

def get_pdf_bytedeta(request, pk):
    try:
        mdfile_instance = Mdfile.objects.get(pk=pk) 
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