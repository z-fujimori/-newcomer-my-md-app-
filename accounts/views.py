from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import BudgetSetting
from .forms import CustomUserCreationForm, CustomAuthenticationForm, SettingForm

# Create your views here.
def index(request):
    return render(request, "accounts/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'アカウントを作成しました！')
            BudgetSetting.objects.create(user=user)
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'ログインしました！')
            return redirect('accounts:index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'ログアウトしました。')
    return redirect('accounts:login')

@login_required
def settingStore(request):
    if request.method == "POST":
        # 既存の設定を取得
        budget_setting = BudgetSetting.objects.filter(user=request.user).first()
        if budget_setting:
            # 更新の場合
            form = SettingForm(request.POST, instance=budget_setting)
        else:
            # 新規作成の場合
            form = SettingForm(request.POST)
            
        if form.is_valid():
            budget_setting = form.save(commit=False)
            budget_setting.user = request.user
            budget_setting.save()
            messages.success(request, '予算設定を更新しました！')
            return redirect('expenses:index')
        else:
            userData = BudgetSetting.objects.filter(user=request.user).first()
            return render(request, 'accounts/setting.html', {
                'max_weekly_limit': userData.max_weekly_limit if userData else 0,
                'monthly_buffer': userData.monthly_buffer if userData else 0
            })
    else:
        userData = BudgetSetting.objects.filter(user=request.user).first()
        return render(request, 'accounts/setting.html', {
                'max_weekly_limit': userData.max_weekly_limit if userData else 0,
                'monthly_buffer': userData.monthly_buffer if userData else 0
            })
