from django.conf.urls import url
from django.forms import ModelForm
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

class ModelConfig(object):
    """
    默认执行的类方法
    """
    list_display = []
    show_add_btn=True
    model_form_class=None
    def __init__(self,model_class,site):
        self.model_class=model_class
        self.site=site
    def get_list_display(self):
        data=[]
        data.extend(self.list_display)
        data.append(ModelConfig.edit)
        data.append(ModelConfig.delete)
        data.insert(0,ModelConfig.checkbox)
        return data
    def get_add_btn(self):
        return self.show_add_btn
    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return "选择"
        return mark_safe("<input type='checkbox' name='choice' value='%s'>" %(obj.id,))
    def edit(self,obj=None,is_header=False):
        if is_header:
            return "编辑"
        return mark_safe("<a href='%s'>编辑</a>" %(self.get_edit_url(obj.id),))
    def delete(self,obj=None,is_header=False):
        if is_header:
            return "删除"
        return mark_safe("<a href='%s'>删除</a>" %(self.get_delete_url(obj.id),))
    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class
        meta=type("Meta",(object,),{"model":self.model_class,"fields":"__all__"})
        AddForm=type("AddForm",(ModelForm,),{"Meta":meta})
        return AddForm
    def get_urls(self):
        app_name=self.model_class._meta.app_label
        model_name=self.model_class._meta.model_name
        url_patterns=[
            url(r'^$', self.list_view,name="%s_%s_list" %(app_name,model_name)),
            url(r'^add/$', self.add_view,name="%s_%s_add" %(app_name,model_name)),
            url(r'^edit/(\d+)/$', self.edit_view,name="%s_%s_edit" %(app_name,model_name)),
            url(r'^delete/(\d+)/$', self.delete_view,name="%s_%s_delete" %(app_name,model_name)),
        ]
        return url_patterns
    @property
    def urls(self):
        return self.get_urls()
    def get_edit_url(self,nid):
        name = "stark:%s_%s_edit" % (self.model_class._meta.app_label, self.model_class._meta.model_name)
        edit_url = reverse(name,args=(nid,))
        return edit_url
    def get_delete_url(self,nid):
        name = "stark:%s_%s_delete" % (self.model_class._meta.app_label, self.model_class._meta.model_name)
        delete_url = reverse(name,args=(nid,))
        return delete_url
    def get_add_url(self):
        name = "stark:%s_%s_add" % (self.model_class._meta.app_label, self.model_class._meta.model_name)
        add_url = reverse(name)
        return add_url
    def get_list_url(self):
        name = "stark:%s_%s_list" % (self.model_class._meta.app_label, self.model_class._meta.model_name)
        list_url = reverse(name)
        return list_url
    def list_view(self,request,*args,**kwargs):
        head_list=[]
        for field_name in self.get_list_display():
            if isinstance(field_name,str):
                verbose_name=self.model_class._meta.get_field(field_name).verbose_name
            else:
                verbose_name=field_name(self,is_header=True)
            head_list.append(verbose_name)
        data_list=self.model_class.objects.all()
        new_list=[]
        for row in data_list:
            rank_list=[]
            for rank in self.get_list_display():
                if isinstance(rank,str):
                    word=getattr(row,rank)
                else:
                    word=rank(self,obj=row)
                rank_list.append(word)
            new_list.append(rank_list)
        return render(request,"list.html",{"data_list":new_list,"head_list":head_list,"show_add_btn":self.get_add_btn(),"add_url":self.get_add_url()})
    def add_view(self,request,*args,**kwargs):
        model_form_class=self.get_model_form_class()
        if request.method=="GET":
            forms=model_form_class()
            return render(request,"add.html",{"forms":forms})
        else:
            forms=model_form_class(data=request.POST)
            if forms.is_valid():
                forms.save()
                return redirect(self.get_list_url())
            else:
                return render(request, "add.html", {"forms": forms})

    def edit_view(self,request,nid,*args,**kwargs):
        model_form_class=self.get_model_form_class()
        obj=self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return render(request,"list.html")
        if request.method=="GET":
            forms=model_form_class(instance=obj)
            return render(request,"add.html",{"forms":forms})
        else:
            forms=model_form_class(instance=obj,data=request.POST)
            if forms.is_valid():
                forms.save()
                return redirect(self.get_list_url())
            else:
                return render(request, "add.html", {"forms": forms})

    def delete_view(self,request,nid,*args,**kwargs):
        self.model_class.objects.filter(pk=nid).delete()
        return redirect(self.get_list_url())


class StartApp(object):
    def __init__(self):
        self._registry={}
    def register(self,model_class,default_class=None):
        if not default_class:
            default_class=ModelConfig
        self._registry[model_class]=default_class(model_class,self)

    def get_urls(self):
        url_patterns=[]
        for modle_class,model_obj in self._registry.items():
            app_name=modle_class._meta.app_label
            model_name=modle_class._meta.model_name
            curd_url=url(r'^%s/%s/' %(app_name,model_name),(model_obj.urls,None,None))
            url_patterns.append(curd_url)
        return url_patterns

    @property
    def urls(self):
        return (self.get_urls(),None,"stark")
site=StartApp()
