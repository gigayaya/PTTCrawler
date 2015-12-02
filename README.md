# PTTCrawler

##This is a Crawler for PTT.

這是小弟無聊寫來練習的PTT推文爬蟲(不一定要用來爬推文XD)


輸入：想爬的版名，想從最新文章往回爬的頁數


輸出：把目標範圍內文章中的所有推文，每個推文Insert一次到MySQL


##需要環境:

####Python 2.7


1. requests套件 [http://docs.python-requests.org/en/latest/](http://docs.python-requests.org/en/latest/)


2. BeautifulSoup套件 [http://www.crummy.com/software/BeautifulSoup/](http://www.crummy.com/software/BeautifulSoup/)


3. MySQLdb套件 [https://pypi.python.org/pypi/MySQL-python](https://pypi.python.org/pypi/MySQL-python)

####MySQL Server

##使用方法：

1. 修改開頭settings中的MySQL登入訊息部分


2. 使用Main，給參數(頁數,版名)


3. 執行.py，會把你指定的版，從最新往回數你輸入的頁數，其中所有文章的推文都insrt到你的MySQL


4. 會在MySQL Insert(每筆推文): 文章名稱,網址,推文者,推文種類,時間(年月日)


然後你的MySQL裡面就會有一堆raw data啦～想怎麼玩這些資料就怎麼玩A_A


如果有想要的功能或有bug歡迎留言～
