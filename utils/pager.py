import copy
class Pagination(object):
    def __init__(self,current_page,total_count,base_url,params,per_page_num=10,max_per_page_code=11):
        self.current_page=current_page
        self.total_count=total_count
        self.base_url=base_url
        # self.params=params
        self.max_per_page_code=max_per_page_code
        self.per_page_num=per_page_num
        self.half_page_code=(self.max_per_page_code-1)/2

        max_code,remainder=divmod(total_count,per_page_num)
        if remainder:
            max_code=max_code+1
        self.max_code=max_code
        params=copy.deepcopy(params)
        params._mutable=True
        self.params=params

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page*self.per_page_num

    def page_code(self):
        code_list=[]
        if self.max_code<self.max_per_page_code:
            code_start=1
            code_end=self.max_code
        else:
            if self.current_page<self.half_page_code:
                code_start=1
                code_end=self.current_page+self.per_page_num
            elif (self.current_page+self.half_page_code)>self.max_code:
                code_end=self.max_code
                code_start=self.max_code-self.max_per_page_code+1
            else:
                code_start=self.current_page-self.half_page_code
                code_end=self.current_page+self.half_page_code



