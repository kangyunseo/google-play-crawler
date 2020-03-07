import time
from bs4 import BeautifulSoup
import sys, io
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import *

# @author Ranjeet Singh <ranjeetsingh867@gmail.com>
# Modified my yunseo kang <kangyunseo@icloud.com>
# Modify it according to your requirements

no_of_reviews = 1000

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
driver = webdriver.Chrome('/Users/kangyunseo/Downloads/chromedriver') #your web driver

wait = WebDriverWait( driver, 10 )


# Append your app store urls here
urls = ["https://play.google.com/store/apps/details?id=com.flipkart.android&hl=en"] #your play store link (support string list type)

"""
ref from HUX at dev.to
https://dev.to/hellomrspaceman/python-selenium-infinite-scrolling-3o12

abstract
This function do scrolling & click button to load all play store reviews

requirement
driver : webdriver object
timeout : sleep time (sec) for loading one scrolled page
max_scrolling : number of try scrolling
"""
def scroll(driver, timeout, max_scrolling):
    scroll_pause_time = timeout
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    loopcounter = 0
    while True:
        loopcounter += 1
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            driver.find_element_by_xpath( #click for next reviews
                '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/span/span').click()
        except:
            pass
        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or loopcounter > max_scrolling:
            # If heights are the same it will exit the function
            # If scrolling number increase enough then exit the function
            break
        last_height = new_height


for url in urls:

    driver.get(url)

    page = driver.page_source

    soup_expatistan = BeautifulSoup(page, "html.parser")

    expatistan_table = soup_expatistan.find("h1", class_="AHFaub")

    print("App name: ", expatistan_table.string)

    expatistan_table = soup_expatistan.findAll("span", class_="htlgb")[4]

    print("Installs Range: ", expatistan_table.string)

    # Becausec play sotre web page get changed, need to change find option

    expatistan_table = soup_expatistan.find("div", class_="BHMmbe").get('aria-label')
    print("Rating Value: ", expatistan_table)

    expatistan_table = soup_expatistan.find("span", class_="EymY4b")
    expatistan_table = expatistan_table.find_all("span")[1].get('aria-label')
    print("Reviews Count: ", expatistan_table)

    soup_histogram = soup_expatistan.find("div", class_="VEF2C")

    rating_bars = soup_histogram.find_all('div', class_="mMF0fd")

    for rating_bar in rating_bars:
        print("Rating: ", rating_bar.find("span").text)
        print("Rating count: ", rating_bar.find("span", class_="L2o20d").get('style'))

    # open all reviews
    url = url + '&showAllReviews=true'
    driver.get(url)
    time.sleep(5)  # wait dom ready
    scroll(driver, 3, 50)
    time.sleep(5)  # wait dom ready
    page = driver.page_source

    soup_expatistan = BeautifulSoup(page, "html.parser")
    expand_pages = soup_expatistan.findAll("div", class_="d15Mdf")
    counter = 1
    for expand_page in expand_pages:
        try:
            print("\n===========\n")
            print("review：" + str(counter))
            print("Author Name: ", str(expand_page.find("span", class_="X43Kjb").text))
            print("Review Date: ", expand_page.find("span", class_="p2TkOb").text)
            '''
            //didn't find reviewer link
            print("Reviewer Link: ", expand_page.find("a", class_="reviews-permalink")['href'])
            '''
            reviewer_ratings = expand_page.find("div", class_="pf5lIe").find_next()['aria-label'];
            reviewer_ratings = reviewer_ratings.split('(')[0]
            reviewer_ratings = ''.join(x for x in reviewer_ratings if x.isdigit())
            print("Reviewer Ratings: ", reviewer_ratings)
            '''
            //didn't find review title
            print("Review Title: ", str(expand_page.find("span", class_="review-title").string))
            '''
            print("Review Body: ", str(expand_page.find("div", class_="UD7Dzf").text))
            developer_reply = expand_page.find_parent().find("div", class_="LVQB0b")
            if hasattr(developer_reply, "text"):
                print("Developer Reply: " + "\n", str(developer_reply.text))
            else:
                print("Developer Reply: ", "")
            counter += 1
        except:
            pass
driver.quit()

