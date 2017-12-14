from django.conf.urls import url
from django.shortcuts import render,HttpResponse
class ModelConfig(object):
    """
    默认执行的类方法
    """
    list_display = []
    def __init__(self,model_class,site):
        self.model_class=model_class
        self.site=site

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

    def list_view(self,request,*args,**kwargs):
        head_list=[]
        print(self.list_display)
        for field_name in self.list_display:
            if isinstance(field_name,str):
                verbose_name=self.model_class._meta.get_field(field_name).verbose_name
            else:
                verbose_name=field_name(self,is_header=True)
            head_list.append(verbose_name)
        data_list=self.model_class.objects.all()
        new_list=[]
        for row in data_list:
            rank_list=[]
            for rank in self.list_display:
                if isinstance(rank,str):
                    word=getattr(row,rank)
                else:
                    word=rank(self,obj=row)
                rank_list.append(word)
            new_list.append(rank_list)
        return render(request,"list.html",{"data_list":new_list,"head_list":head_list})
    def add_view(self,request,*args,**kwargs):
        return HttpResponse("添加")
    def edit_view(self,request,nid,*args,**kwargs):
        return HttpResponse("编辑")
    def delete_view(self,request,nid,*args,**kwargs):
        return HttpResponse("删除")


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
