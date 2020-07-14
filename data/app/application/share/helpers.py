from math import ceil

class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = int(page)
        self.per_page = int(per_page)
        self.total_count = int(total_count)
        self.first_of_next_ten = ceil(self.page/10)*10+1

    @property
    def pages(self):
        i = float(self.total_count) / float(self.per_page)
        return ceil(i)

    @property
    def has_prev(self):
        return self.page > 1
        
    @property
    def prev_num(self):
        if self.has_prev:
            return self.page-1

    @property
    def has_next(self):
        return self.page < self.pages
    @property
    def next_num(self):
        if self.has_next:
            return self.page+1

    @property
    def has_prev_jump(self):
        return self.page >10
        
    @property
    def prev_jump_num(self):
        if self.has_prev_jump:
            return self.page-10

    @property
    def has_next_jump(self):        
        return self.first_of_next_ten <= self.pages
    @property
    def next_jump_num(self):
        if self.has_next_jump:
            return self.first_of_next_ten if self.page+10>=self.pages else self.page+10
           
    @property
    def jump_page(self):
        i = float(self.page) / float(10)
        return ceil(i)       

    def iter_pages(self):
        first = ((self.page-1) // 10) * 10 
        for num in range(1,11):
            #yield first
            if first+num <= self.pages:
                yield first+num
    """
    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
    """            