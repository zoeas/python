from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from openpyxl import Workbook
from collections import OrderedDict
from datetime import datetime
import re
import time

urllist = []
urllist.append('http://www.dgkoaa.or.kr/sub01-08.jsp?common_sel=10&syear_option=2019&smonth_option=4&syear_option=&smonth_option=&common_code=30') # 중구
urllist.append('http://www.dgkoaa.or.kr/sub01-08.jsp?common_sel=20&syear_option=2019&smonth_option=4&syear_option=&smonth_option=&common_code=30') # 동구
urllist.append('http://www.dgkoaa.or.kr/sub01-08.jsp?common_sel=30&syear_option=2019&smonth_option=4&syear_option=&smonth_option=&common_code=30') # 서구
urllist.append('http://www.dgkoaa.or.kr/sub01-08.jsp?common_sel=40&syear_option=2019&smonth_option=4&syear_option=&smonth_option=&common_code=30') # 남구
urllist.append('http://www.dgkoaa.or.kr/sub01-08.jsp?common_sel=50&syear_option=2019&smonth_option=4&syear_option=&smonth_option=&common_code=30') # 북구
urllist.append('http://www.dgkoaa.or.kr/sub01-08.jsp?common_sel=60&syear_option=2019&smonth_option=4&syear_option=&smonth_option=&common_code=30') # 수성구

write_wb = Workbook()

# 엑셀쓰기
write_ws = write_wb.active
write_ws['A1'] = '시작'

html = ''

for url in urllist:
    req = Request(url)
    res = urlopen(req)
    html += res.read().decode('cp949')

bs = BeautifulSoup(html, 'html.parser')
'''
tag_table = bs.find('table', attrs={'class': 'tb03'})
tags_tbody = tag_table.findAll('tbody')
'''

# 모든 td를 찾음
tags_td = bs.findAll('td')

regex = re.compile(r"<td>(\D+.+) (\d+.+) <br\/>")

title_list = []
num_list = []
for tag_td in tags_td:
    rm = tag_td.find('font')
    if not rm :                 # font 태그가 없는 td만
        m = regex.search(str(tag_td))
        if m != None:
            title_list.append(m.group(1).replace(' ',''))
            num_list.append(m.group(2))

title_dic = list(OrderedDict.fromkeys(title_list))
num_dic = list(OrderedDict.fromkeys(num_list))

i = 1
for tdic,ndic in zip(title_dic, num_dic):
    write_ws.cell(i, 1, tdic)
    write_ws.cell(i, 2, ndic)
    i = i + 3

now = datetime.now()
write_wb.save('%s-%s-%s 옥외광고협회 전화번호.xlsx' % (now.year, now.month, now.day))



# tabel 클래스 'tb03' tbody th 패스, 첫번째 tr 패스 tr 3개 연속 첫번째 td 패스, 남은 두개 td br 이전의 택스트만



