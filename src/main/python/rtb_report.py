from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
import arena_config
from mail import Mailer
from util import Util



# CONNECT TO PHANTOMJS Driver
driver = webdriver.PhantomJS()


# ESTABLISH URL WE WANT TO ACCESS
driver.get(arena_config.url)




# SET WINDOW SIZE
driver.set_window_size(1500, 1500)
# driver.maximize_window()
# print driver.get_window_size()


# LOGGING INTO ARENA
email = arena_config.email
passw = arena_config.passw

username = driver.find_element_by_id("login-email")
password = driver.find_element_by_id("login-pass")

username.send_keys(email)
password.send_keys(passw)


try:
	login_attempt = driver.find_element_by_xpath("//*[@type='submit']").click()
except:
	print "Login Failed"
else:
	print "Login Succeeded"


# SLEEP TO ALLOW PAGE TO LOAD
time.sleep(10)



# DOUBLE CLICK TO SORT GROSS REVENUE DATA IN DESCENDING ORDER
rev_attempt = driver.find_element_by_xpath("//span [@class='slick-column-name' and text()='Gross Revenue']")

actionchains = ActionChains(driver)
actionchains.double_click(rev_attempt).perform()


# ESTABLISH WHICH TABLE TO PULL FROM 
table = driver.find_element_by_xpath("//*[@id='campaigns-container']")
# table = driver.find_element_by_xpath("//*[@id='j-campaignTableDiv']")     


# MAKE A SCREENSHOT TO SEE WHAT IS BEING DISPLAYED
driver.save_screenshot('alt_screen.png')


# GET HTML
table_html = table.get_attribute('innerHTML')


# PARSE HTML
table_soup = BeautifulSoup(table_html, 'lxml')


# PULL ROWS BY CERTAIN PARAMETERS
table_data = table_soup.find_all("div", {"class": "slick-row"})




filename = '/tmp/arena_rev_test.csv'

with open(filename, 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	header = ['Campaign Name', 'Impressions', 'Gross Revenue']
	writer.writerow(header)
	for item in table_data:
		writer.writerow([item.contents[0].text, item.contents[7].text, item.contents[8].text])
csvfile.close()


#Mail message to recipients
message = Util().get_arena_rtb()
mail_user = arena_config.mail_user
mail_pwd = arena_config.mail_pwd
mail_recipients = list()
mail_recipients.append(arena_config.email)

mail_subject = 'RTB Dashboard Report - ' + arena_config.yesterday_date
Util().send_mail(mail_user, mail_pwd, mail_subject, mail_recipients, message, filename)

