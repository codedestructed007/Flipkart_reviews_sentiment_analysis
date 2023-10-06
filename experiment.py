pip install selenium
from selenium import webdriver

# Set up the web driver (e.g., Chrome)
driver = webdriver.Chrome('path/to/chromedriver')

product_url = 'https://www.flipkart.com/apple-iphone-13-midnight-128-gb/p/itmca361aab1c5b0'
driver.get(product_url)


read_more_button = driver.find_element_by_css_selector("/html/body/div[1]/div/div[3]/div[1]/div[2]/div[9]/div[7]/div/div[4]/div[1]/div/div/div[2]/div/div/span")
read_more_button.click()


complete_reviews = driver.find_elements_by_css_selector('your-selector-for-complete-reviews')
for review in complete_reviews:
    print(review.text)


driver.quit()

