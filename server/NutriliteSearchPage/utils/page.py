class Pagination(object):

  def __init__(self,current_page_num,all_count,request,per_page_num=10,pager_count=11):
    """
    封裝分頁相關資料
    :param current_page_num: 當前訪問頁的數字
    :param all_count:  分頁資料中的資料總條數
    :param per_page_num: 每頁顯示的資料條數
    :param pager_count: 最多顯示的頁碼個數
    """
    try:
      current_page_num = int(current_page_num)
    except Exception as e:
      current_page_num = 1

    if current_page_num < 1:
      current_page_num = 1

    self.current_page_num = current_page_num

    self.all_count = all_count
    self.per_page_num = per_page_num

    # 實際總頁碼
    all_pager,tmp = divmod(all_count,per_page_num)
    if tmp:
      all_pager += 1
    self.all_pager = all_pager

    self.pager_count = pager_count
    self.pager_count_half = int((pager_count - 1) / 2) # 5

    # 儲存搜尋條件
    import copy
    self.params = copy.deepcopy(request.GET) # {"a":"1","b":"2"}

  # 開始
  @property
  def start(self):
    return (self.current_page_num - 1) * self.per_page_num

  # 結束
  @property
  def end(self):
    return self.current_page_num * self.per_page_num

  # 實現
  def page_html(self):
    # 如果總頁碼 < 11個：
    if self.all_pager <= self.pager_count:
      pager_start = 1
      pager_end = self.all_pager + 1
    # 總頁碼 > 11
    else:
      # 當前頁如果<=頁面上最多顯示11/2個頁碼
      if self.current_page_num <= self.pager_count_half:
        pager_start = 1
        pager_end = self.pager_count + 1
      # 當前頁大於5
      else:
        # 頁碼翻到最後
        if (self.current_page_num + self.pager_count_half) > self.all_pager:

          pager_start = self.all_pager - self.pager_count + 1
          pager_end = self.all_pager + 1

        else:
          pager_start = self.current_page_num - self.pager_count_half
          pager_end = self.current_page_num + self.pager_count_half + 1

    page_html_list = []

    # first_page = '<li><a href="?page=%s" rel="external nofollow" rel="external nofollow" rel="external nofollow" rel="external nofollow" class="button small">首頁</a></li>' % (1,)
    # page_html_list.append(first_page)

    if self.current_page_num <= 1:
      prev_page = '<li class="disabled"><a href="#" rel="external nofollow" rel="external nofollow" class="button small">上一頁</a></li>'
    else:
      prev_page = '<li><a href="?page=%s" rel="external nofollow" rel="external nofollow" rel="external nofollow" rel="external nofollow" class="button small">上一頁</a></li>' % (self.current_page_num - 1,)

    page_html_list.append(prev_page)

    # self.params=copy.deepcopy(request.GET) # {"a":"1","b":"2"}
    page_html_list.append("&nbsp &nbsp")
    for i in range(pager_start,pager_end):

      self.params["page"] = i

      if i == self.current_page_num:
        temp = '<li class="active"><a href="?%s" rel="external nofollow" rel="external nofollow" class="page active" >%s</a></li>' % (self.params.urlencode(),i)
      else:
        temp = '<li><a href="?%s" rel="external nofollow" rel="external nofollow" class="page">%s</a></li>' % (self.params.urlencode(),i,)
      page_html_list.append(temp)
    page_html_list.append("&nbsp &nbsp")
    if self.current_page_num >= self.all_pager:
      next_page = '<li class="disabled"><a href="#" rel="external nofollow" rel="external nofollow" class="button small">下一頁</a></li>'
    else:
      next_page = '<li><a href="?page=%s" rel="external nofollow" rel="external nofollow" rel="external nofollow" rel="external nofollow" class="button small">下一頁</a></li>' % (self.current_page_num + 1,)
    page_html_list.append(next_page)
    # last_page = '<li><a href="?page=%s" rel="external nofollow" rel="external nofollow" rel="external nofollow" rel="external nofollow" class="button small">尾頁</a></li>' % (self.all_pager,)
    # page_html_list.append(last_page)

    return ''.join(page_html_list)
