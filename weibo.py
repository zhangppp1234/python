#coding:utf-8
import re
import pymongo
import time
from selenium import webdriver
from selenium.webdriver.support import ui
browser = webdriver.Chrome(executable_path=r"D:\aboutpython\chromedriver.exe")
def login(host):
    wait = ui.WebDriverWait(browser, 2)
    browser.get(host)
    time.sleep(5)
    wait.until(lambda browser: browser.find_element_by_id("loginName"))
    u = browser.find_element_by_id("loginName")
    u.send_keys('%d' % 17680945853)
    wait.until(lambda browser: browser.find_element_by_id('loginPassword'))
    p = browser.find_element_by_id('loginPassword')
    p.send_keys('%s' % 'xc0684111')
    wait.until(lambda browser: browser.find_element_by_id('loginAction'))
    login = browser.find_element_by_id('loginAction')
    time.sleep(2)
    login.click()
    time.sleep(10)

def get_blog(host):
    pagenum = 1 #页数
    blog_num = 1 #微博数
    browser.get(host)
    page = browser.find_element_by_xpath("//div[@class='pa']").text
    pageList_num = re.findall(r'\d+',page)[1]
    message_list = []
    while (pagenum <= int(pageList_num)):
        time.sleep(5)
        browser.get(host + '?page=' + str(pagenum))
        content_list = browser.find_elements_by_xpath("//div[@class='c']")
        for content in content_list:
            try:
                cc_url = content.find_element_by_class_name('cc').get_attribute('href') #评论url
                content = content.text.replace('\n', '').replace('\r', '').replace(' ', '')
                report = re.findall(u'.*?\u8d5e\[', content)
                like = re.findall(u'\u8d5e\[(\d+)\]', content)  # 点赞数
                transfer = re.findall(u'\u8f6c\u53d1\[(\d+)\]', content)  # 转载数
                comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', content)  # 评论数
                other = re.findall(u'\u6536\u85cf(.*)', content)  # 时间 位置
                message = {}
                if len(report) > 0:
                    message['_id'] = blog_num
                    if report:
                        message['简报'] = report[0]
                    if like:
                        message['点赞'] = like[0]
                    if transfer:
                        message['转载'] = transfer[0]
                    if comment:
                        message['评论'] = comment[0]
                    if other:
                        ot = other[0].split(u'\u6765\u81ea')
                        message['来自'] = ot[1]
                        message['时间'] = ot[0]
                    if cc_url:
                        message['URL'] = cc_url
                    blog_num += 1
                    message_list.append(message)
            except:
                continue
        print('第{}页已抓取'.format(pagenum))
        pagenum += 1
        try:
            if time.strptime(message_list[blog_num-2]['时间'], '%Y-%m-%d%H:%M:%S') < time.strptime('2019-12-2000:00:00', '%Y-%m-%d%H:%M:%S'):
                break
        except:
            continue


    return message_list


def get_comment(url):
    time.sleep(2)
    browser.get(url)
    comment_list = browser.find_elements_by_xpath("//div[@class='c']")
    comments = []
    c_num = 1
    for comment_ in comment_list[3:]:
        try:
            c_message = {}
            comment_text = comment_.text.replace('\n', '').replace('\r', '').replace(' ', '')
            c_message['编号'] = c_num
            c_message['内容'] = comment_text
            c_num += 1
            comments.append(c_message)
        except:
            c_message['编号'] = c_num
            c_message['内容'] = '无内容'
            c_num += 1
            comments.append(c_message)
    return comments

def store_message(message):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['pymongo']
    mycol = mydb['t_weibo']
    mycol.insert_many(message)


if __name__ == '__main__':
    host = 'https://weibo.cn/u/1642720480'
    login(host)
    message = get_blog(host)
    for m in message:
        text = get_comment(m['URL'])
        m['评论内容'] = (text)
    store_message(message)