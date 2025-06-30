from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from mdapp.models import Mdfile, Share
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from .services import converter, pdf_gerater, img_generater
from .forms import CreateMdfileForm, ShareForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse

# def index(request):
#     return render(request, 'mdapp/index.html')

img_strage_mode = "local"  # "s3" or "local"

class List(LoginRequiredMixin, ListView):
    model = Mdfile
    template_name = "mdapp/index.html"
    def get_queryset(self):
        return Mdfile.objects.filter(user=self.request.user).order_by("-created_at")
    # コンテキストを追加
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['share_form'] = ShareForm(sharer=self.request.user)
        return context

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
        if img_strage_mode == "s3":
            print("S3に保存")
            isinstance.url = img_generater.generate_image_from_pdf(pdf_bytes, isinstance.title)
        elif img_strage_mode == "local":
            print("ローカルに保存")
            isinstance.url = img_generater.generate_image_from_pdf_local(pdf_bytes, isinstance.title, self.request.user.name)
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
        if img_strage_mode == "s3":
            print("S3に保存")
            isinstance.url = img_generater.generate_image_from_pdf(pdf_bytes, isinstance.title)
        elif img_strage_mode == "local":
            print("ローカルに保存")
            isinstance.url = img_generater.generate_image_from_pdf_local(pdf_bytes, isinstance.title, self.request.user.name)
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
        if img_strage_mode == "s3":
            print("S3に保存")
            isinstance.url = img_generater.generate_image_from_pdf(pdf_bytes, isinstance.title)
        elif img_strage_mode == "local":
            print("ローカルに保存")
            isinstance.url = img_generater.generate_image_from_pdf_local(pdf_bytes, isinstance.title, self.request.user.name)
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
def get_img(request, filename):
    try:
        # 画像のパスを指定
        img_path = f"mdapp/static/mdapp/img/thumbs/{filename}"
        with open(img_path, 'rb') as img_file:
            response = HttpResponse(img_file.read(), content_type="image/jpeg")
            response['Content-Disposition'] = f'inline; filename="{filename}"'
            return response
    except FileNotFoundError:
        return HttpResponse("画像が見つかりませんでした。", status=404)

class Shared(LoginRequiredMixin, ListView):
    model = Share
    template_name = "mdapp/shared.html"
    def get_queryset(self):
        shared_files = Share.objects.filter(to_user=self.request.user).select_related("file", "file__user").order_by('created_at')
        files = []
        for f in shared_files:
            files.append({
                "shared_id": f.id,
                "file_id": f.file.id,
                "title": f.file.title,
                "base_text": f.file.base_text,
                "html_text": f.file.html_text,
                "url": f.file.url,
                "auther_user_id": f.file.user.id,
                "auther_user_name": f.file.user.name,
                "shared_at": f.created_at
            })
        return files

class CreateShared(CreateFile):
    model = Mdfile
    form_class = CreateMdfileForm
    template_name = "mdapp/create.html"
    # success_url = reverse_lazy('mdapp:index')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # ここで user を渡す
        return kwargs
    def get_initial(self):
        share_id = self.kwargs.get('pk')
        try:
            share_instance= get_object_or_404(
                Share.objects.select_related('file', 'file__user'), 
                pk=share_id,
                to_user=self.request.user
            )
            initial = super().get_initial()
            initial["title"] = f"{share_instance.file.title}_by_{share_instance.file.user.name}"
            initial["base_text"] = share_instance.file.base_text
        except Exception as e:
            print(e)
        return initial

@login_required
@require_POST
def share(request, pk):
    mdfile = Mdfile.objects.get(pk=pk)
    if mdfile.user != request.user:
        raise Http404("存在しない記事です")
    print("テストテキスト",mdfile)
    print("テストテキスト",request.POST)
    form = ShareForm(request.POST, sharer=request.user)
    status_code = 200
    if form.is_valid():
        to_user = form.cleaned_data["to_user"]
        if not Share.objects.filter(file=mdfile, to_user=to_user).exists():
            Share.objects.create(
                file=mdfile,
                to_user=to_user
            )
            res_data = {"status": "success", "message": f"{to_user.name}にファイル[{mdfile.title}]を共有しました"}
        else:
            res_data = {"status": "info", "message": f"ファイル[{mdfile.title}]は{to_user.name}に既に共有済みです"}
    else:
        status_code = 400
        res_data = {"status": "error", "message": f"データが間違っています"}
        return HttpResponse(f"formエラー:", status=500)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(res_data, status=status_code)
    
    
