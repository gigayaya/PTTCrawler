#Copyright © 2015 by Gigayaya

# -*- coding: utf-8-*-
#!/usr/bin/python

import requests
import time
import httplib
from BeautifulSoup import BeautifulSoup
import MySQLdb
import sys
import random
reload(sys)
sys.setdefaultencoding('utf-8')

#===========Settings==============
MySQLHost = "localhost"
MySQLUser = "root"
MySQLPassword = "12345678"
MySQLdb = "PTT"
#=================================

#get the time of content
def PTTtime(html):
	Time = html.findAll(attrs={'class' :'article-meta-value'})
	TimeTemp = Time[3].string
	Month = ""
	Month += TimeTemp[4] + TimeTemp[5] + TimeTemp[6]
	Month = MonthChack(Month)
	Day = ""
	if(TimeTemp[8] == " "):
		Day += "0"
		Day += TimeTemp[9]
	else:
		Day += TimeTemp[8] + TimeTemp[9]
	Year = ""
	Year += TimeTemp[20] + TimeTemp[21] + TimeTemp[22] + TimeTemp[23]
	Result = ""
	Result += Year + "-" + Month + "-" + Day
	return Result

#translation English to Integer
def MonthChack(Month):
	MonthReturn = ""
	if(Month == "Jan"):
		MonthReturn = "1"
	if(Month == "Feb"):
		MonthReturn = "2"
	if(Month == "Mar"):
		MonthReturn = "3"
	if(Month == "Apr"):
		MonthReturn = "4"
	if(Month == "May"):
		MonthReturn = "5"
	if(Month == "Jun"):
		MonthReturn = "6"
	if(Month == "Jul"):
		MonthReturn = "7"
	if(Month == "Aug"):
		MonthReturn = "8"
	if(Month == "Sep"):
		MonthReturn = "9"
	if(Month == "Oct"):
		MonthReturn = "10"
	if(Month == "Nov"):
		MonthReturn = "11"
	if(Month == "Dec"):
		MonthReturn = "12"
	return MonthReturn

#get commit of content
def ContentCrawler(PTTurl):
	#log in MySQL
	db = MySQLdb.connect(host=MySQLHost, user=MySQLUser, passwd=MySQLPassword, db=MySQLdb)
	db.set_character_set('utf8')
	cursor = db.cursor()

	#parser settings
	cookies = dict(over18='1')
	res = requests.get(str(PTTurl), verify=False, cookies=cookies)
	content = res.content
	soup = BeautifulSoup(content.decode('utf-8','ignore')) 

	#get the title name
	try:
		Title = soup.find("meta", {"property":"og:title"})['content']
	except:
		Title = "unknown"

	#get commit of content
	commit = soup.findAll(attrs={'class' :'push'})

	#analysis the raw data of commit
	for rawdata in commit:
		SQLname = ""
		SQLpush = ""
		SQLnopush = ""
		SQLcommit = ""
		#find all id
		name = rawdata.findAll(attrs={'class' :'f3 hl push-userid'})
		for idd in name:
			SQLname = idd.string
		#find all push
		push = rawdata.findAll(attrs={'class' :'hl push-tag'})
		for showpush in push:
			SQLpush = showpush.string
		#find all no push
		nopush = rawdata.findAll(attrs={'class' :'f1 hl push-tag'})
		for shownopush in nopush:
			SQLnopush = shownopush.string
		if(SQLpush == ""):
			SQLcommit = SQLnopush
		else:
			SQLcommit = SQLpush
		#SQL command insert the data
		date = PTTtime(soup)
		sqlcommand = "INSERT INTO `PTT`.`test1` (`title`, `url`, `id`, `commit`, `date`) VALUES ('%s', '%s', '%s', '%s', '%s')" %(Title,PTTurl,SQLname,SQLcommit,date)
		cursor.execute(sqlcommand)
		db.commit()

#get the previous page link
def PreviousPage(url):
	ReturnUrl = ""
	PTTurl = str(url)
	cookies = dict(over18='1')
	res = requests.get(PTTurl, verify=False, cookies=cookies)
	content = res.content
	soup = BeautifulSoup(content.decode('utf-8','ignore')) 
	PreviousPageButton = soup.findAll(attrs={'class' :'btn-group pull-right'})
	for FindButton in PreviousPageButton:
		FindUrl = FindButton.findAll(attrs={'class' :'btn wide'})
		ReturnUrl = FindUrl[1].get('href')
		ReturnUrl = "https://www.ptt.cc" + ReturnUrl
	return str(ReturnUrl)

#find all links on page
def AllLinkOnPage(PTTurl):
	print "Start search links on: " + PTTurl
	CheckIsDelete = False
	cookies = dict(over18='1')
	res = requests.get(PTTurl, verify=False, cookies=cookies)
	content = res.content
	soup = BeautifulSoup(content.decode('utf-8','ignore')) 
	AllTittle = soup.findAll(attrs={'class' :'r-ent'})
	#if a post is deleted, the authos is "-" and skip the post
	for Content in AllTittle:
		CheckIsDelete = False
		CheckDeleteDiv = Content.findAll(attrs={'class' :'meta'})
		for DeleteResult in CheckDeleteDiv:
			FindAuthor = DeleteResult.findAll(attrs={'class' :'author'})
			for CheckAuthor in FindAuthor:
				if(CheckAuthor.string == "-"):
					CheckIsDelete = True
					break 
		if(CheckIsDelete == True):
			continue
		#if author is not "-",parser the post	
		ContentTittle = Content.findAll(attrs={'class' :'title'})	
		for TittleUrl in ContentTittle:
			ContentUrl =  "https://www.ptt.cc" + TittleUrl.find('a').get('href')
			print ContentUrl
			#call function parser the post and add to MySQL
			ContentCrawler(ContentUrl)

#main function, type board name and how many page you want to parser
def Main(loop,board):
	url = "https://www.ptt.cc/bbs/" + str(board) + "/index.html"
	for times in range(0,loop):
		global url
		print "Start Parser page" + url
		AllLinkOnPage(url)
		url = PreviousPage(url)
		print "Done Parser page"

#example, parser all commit in "Soft_job" of 3 pages
Main(3,"Soft_job")


