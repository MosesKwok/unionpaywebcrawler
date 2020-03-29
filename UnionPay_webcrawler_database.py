#!apt install chromium-chromedriver
#!pip install selenium
#!pip install pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pymysql
import time
import datetime

host = "127.0.0.1"
port = 3306
user = "database_username"
password = "database_pw"
database = "database_name"

db = pymysql.connect(host = host,port = port,user = user,password = password,db = database)
cur = db.cursor()

url = 'https://www.unionpayintl.com/cardholderServ/serviceCenter/rate?language=hk'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=options)
driver.get(url)

driver.find_element(By.CSS_SELECTOR, ".fixed:nth-child(2) > .select").click()
driver.find_element(By.LINK_TEXT, "HKD, Hong Kong Dollar").click()

driver.find_element(By.CSS_SELECTOR, ".fixed:nth-child(3) > .select").click()
driver.find_element(By.LINK_TEXT, "TWD, New Taiwan Dollar").click()

oneday = datetime.timedelta(days = 1)
begindate = datetime.date(2018,1,1)
enddate = datetime.date(2018,12,31)

resultdate = begindate
while(1):
	print("%s start webcrawler" % (resultdate))
	driver.find_element(By.ID, "d4311").click()
	for i in range(15):
		driver.find_element(By.ID, "d4311").send_keys(Keys.BACK_SPACE)
	datestring = resultdate.strftime("%Y-%m-%d")
	driver.find_element(By.ID, "d4311").send_keys(datestring)
	driver.find_element(By.LINK_TEXT, "査詢").click()
	time.sleep(3)
	resultstr = driver.find_element(By.ID, "resultDiv").text

	resultstr = resultstr.replace('您查詢的匯率結果為：1TWD = ','')
	resultstr = resultstr.replace(' HKD','')

	try:
		sql = "INSERT INTO RecordTable(Date, ExchangeRate) VALUES ('%s', '%s');" % (resultdate,resultstr)

		try:
			cur.execute(sql)
			db.commit()
			print('%s: %s' % (resultdate,resultstr))
		except:
			db.rollback()
			print("Error: %s" % (resultdate))

	except:
		print('%s暫無相關資料' % (resultdate))

	resultdate += oneday
	if(resultdate>enddate):
		break

db.close()