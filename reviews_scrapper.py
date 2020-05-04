from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup, Comment
import pandas as pd

def scroll_down():
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        sleep(10)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(30)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print ("Height is same")
                break

        last_height = new_height


url = raw_input("Enter the Goggle Play store url: ") 
#driver setup
# add path to chromedriver
driver = webdriver.Chrome("/path/to/chromedriver")

link = url + "&showAllReviews=true"
#open the link in browser
k = driver.get(link)

scroll_down()

no_of_exec = 5
for i in range(1000):
    try: 
        show_more_xpath=driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div')
        show_more_xpath.click()
        scroll_down()
    except Exception as e:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        scroll_down()
        print (e)
        no_of_exec= no_of_exec -1
        if(no_of_exec<=0):
            print ("page load complete")
            break
            
Ptitle = driver.find_element_by_class_name('AHFaub').text.replace(' ','')
file_name= Ptitle+'_reviews_list.csv'
print ("File Name: "+file_name)                
xpath=driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]')
print ("Total Review : "+ str(len(xpath.find_elements_by_xpath("//div[@jscontroller='H6eOGe']"))))

reviews_df = []
try:
    for elem in xpath.find_elements_by_xpath("//div[@jscontroller='H6eOGe']"):
        #print(elem)
        content = elem.get_attribute('outerHTML')
        #print (content)
        soup = BeautifulSoup(content, "html.parser")
        #print(soup.prettify())
        date = soup.find('span',class_='p2TkOb').get_text()
        #print(date)
        rating_temp = soup.find('div',class_='pf5lIe')
        rating = rating_temp.find('div',attrs={'role':'img'})['aria-label'][6:7]
        #print(rating.find('div',attrs={'role':'img'})['aria-label'][6:7])
        full_review=soup.find('span',attrs={'jsname':'fbQN7e'}).get_text()
        if(len(full_review)>0):
            review= full_review
        else:
            review = soup.find('span',attrs={'jsname':'bN97Pc'}).get_text()
        temp = pd.DataFrame({'Date':date,'Rating':rating,'Review':review},index=[0])
        print('-'*10)
        reviews_df.append(temp)
except Exception as e:
    print(e)

reviews_df = pd.concat(reviews_df,ignore_index=True)
#print (reviews_df)
reviews_df.to_csv(file_name, encoding='utf-8')
 
driver.close()
