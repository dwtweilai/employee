from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect

from user import models
from user.models import Department, UserInfo, PrettyNum


def depart_list(request):
    """ 部门列表 """
    queryset = Department.objects.all()
    return render(request, "depart_list.html", {'queryset': queryset})


def depart_add(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, "depart_add.html")
    title = request.POST.get("title")
    Department.objects.create(title=title)
    return redirect("/depart/list/")


def depart_delete(request, nid):
    """ 删除部门 """
    Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """ 修改部门 """
    if request.method == "GET":
        row_object = Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {'row_object': row_object})
    title = request.POST.get("title")
    Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')


def user_list(request):
    """ 用户管理 """
    queryset = UserInfo.objects.all()
    return render(request, 'user_list.html', {'queryset': queryset})


def user_add(request):
    """ 添加用户(原始方式) """
    if request.method == "GET":
        context = {
            'gender_choices': UserInfo.gender_choices,
            'depart_list': Department.objects.all()
        }
        return render(request, 'user_add.html', context)
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    account = request.POST.get("ac")
    ctime = request.POST.get("ctime")
    gender_id = request.POST.get("gd")
    depart_id = request.POST.get("dp")
    UserInfo.objects.create(name=user, password=pwd, age=age, account=account, create_time=ctime, gender=gender_id,
                            depart_id=depart_id)
    return redirect('/user/list/')


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']

        # 繁琐
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password': forms.TextInput(attrs={'class': 'form-control'}),
        #     'age': forms.TextInput(attrs={'class': 'form-control'}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_add(request):
    """ 添加用户(modelform) """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_edit(request, nid):
    """ 编辑用户 """
    row_object = UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def pretty_list(request):
    # PrettyNum.objects.create(mobile="13483648923",price=1500,level=3,status=1)
    queryset = PrettyNum.objects.all().order_by("-level")
    return render(request, 'pretty_list.html', {'queryset': queryset})


class PrettyModelForm(forms.ModelForm):
    # 验证1
    mobile = forms.CharField(label="手机号", validators=[RegexValidator('^13[0-9]+', '必须以13开头')])

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile','price','level','status']
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 验证2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile


def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {'form': form})


class PrettyEditModelForm(forms.ModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")
    mobile = forms.CharField(label="手机号", validators=[RegexValidator('^13[0-9]+', '必须以13开头')])

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile


def pretty_edit(request, nid):
    row_object = PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list')
    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list')
