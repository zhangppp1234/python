#coding:utf-8
import urllib.request
from bs4 import BeautifulSoup
from openpyxl import Workbook
import bs4
def spider_book_url():
    page_num = 1
    book_url_list = []
    time = 0
    hds = [
        {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    ]
    while time<100:
        #url = https://www.huxiu.com/member/1405886/article/1.html
        url = 'https://www.huxiu.com/member/1405886/article/'+str(page_num)+'.html'
        try:
            brrow = urllib.request.Request(url,headers=hds[page_num%len(hds)])
            code = urllib.request.urlopen(brrow).read()
        except Exception as e:
            print(e)
            continue
        soup = BeautifulSoup(code, 'html.parser')
        soup_booklist = soup.find('div', {'class': 'message-box'})
        if soup_booklist == None:
            break
        time += 1
        soup_class = soup_booklist.find_all('div',{'class':'mod-b mod-art'})
        for soup_book in soup_class:
            book_url = soup_book.find('a', {'class': 'transition'}).get('href')
            try:
                book_url = book_url
            except:
                book_url = 'None'
            book_url_list.append(book_url)
        page_num += 1
    return book_url_list

def spider_book(url_list):
    url_num = 0
    book_list = []
    hds = [
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, \
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}, \
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    ]
    while (url_num<len(urllist)):
        # url = 'https://www.huxiu.com/'
        book = []
        url = 'https://www.huxiu.com' + url_list[url_num]
        brrow = urllib.request.Request(url, headers=hds[url_num % len(hds)])
        code = urllib.request.urlopen(brrow).read()
        soup = BeautifulSoup(code, 'html.parser')
        if soup == None:
            break


        book.append(url_num+1)
        try:
            title = soup.find('h1', {'class': 'article__title'}).text
            book.append(title)
        except:
            book.append(('无'))
        try:
            time = soup.find('span', {'class': 'article__time'}).text
            book.append(time)
        except:
            book.append(('无'))
        try:
            pl_num = soup.find('div', {'class': "icons-wrap"}).find('i', {'data-v-95b1c8f2': '', 'class': 'num'}).text
            book.append(pl_num)
        except:
            book.append(('无'))
        try:
            dz_num = soup.find('div',{'class':"detail-icons icon-hasNum grey-icon"}).find('i', {'data-v-588ede25': '', 'class': 'num'}).text
            book.append(dz_num)

        except:
            book.append(('无'))
        try:
            text_list = soup.find_all('p', {'label': '正文'})
            if len(text_list) < 10:
                text_list = soup.find('div', {'id': "article-content", 'class': "article__content"}).find_all('p')
            pure_text = ''
            for text in text_list:
                text = str(text.text).strip()
                pure_text = pure_text + text
            book.append(pure_text)
        except:
            book.append(('无'))
        book_list.append(book)
        url_num += 1
        print('Downloading Information %d' % url_num)
    return book_list

def store(booklists):
    wb = Workbook()
    ws = wb.create_sheet(title = 'QianDeHu')
    ws.append(['序号', '标题', '发布时间', '评论人数','点赞人数', '正文'])
    for j in booklists:
        ws.append([j[0],j[1],j[2],j[3],j[4],j[5]])
    save_path = 'huxiu.xlsx'
    wb.save(save_path)




if __name__ == '__main__':
    urllist = spider_book_url()
    booklist = spider_book(urllist)
    store(booklist)