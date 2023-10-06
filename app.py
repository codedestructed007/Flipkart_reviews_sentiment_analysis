import time

from flask import Flask, redirect, render_template, request
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen
from datetime import datetime
from urllib.parse import urljoin

from urllib3 import response

app = Flask(__name__)

home_flipkart = "https://www.flipkart.com/"
product = 'smallphones'
flipkart_url = 'https://www.flipkart.com/search?q=' + product
flipkart_html = requests.get(flipkart_url)
# flipkart_open = urlopen(flipkart_url)
# flipkart_html = flipkart_open.read()
product_html_access = bs(flipkart_html.text, 'html.parser')



# home function
@app.route('/')
def home():
    return render_template('home.html')




@app.route('/product')
def product() :
    time.sleep(1.5830810070037842)
    start_time  =time.time()
    home_flipkart = "https://www.flipkart.com/"
    phone_name = request.args.get( 'phones' )
    flipkart_url = 'https://www.flipkart.com/search?q=' + str(phone_name)
    flipkart_open = urlopen( flipkart_url )
    flipkart_html = flipkart_open.read()
    product_html_access = bs( flipkart_html, 'html.parser' )
    iphone_product_name_list = product_html_access.find_all('div', {'class' : '_4rR01T'})
    iphone_html_image_list = product_html_access.find_all('div', {'class' : '_2QcLo-'})
    number_of_products = len(iphone_html_image_list)

    product_name = []
    images_link = []
    cost = []
    ratings = []
    product_link = []

    for i in range(number_of_products) :
        images_link.append(iphone_html_image_list[i]('img')[0]['src'])

        # Product name
        product_name.append(iphone_product_name_list[i].text)

        # cost
        cost.append(product_html_access.find_all('div', {'class' : "_30jeq3 _1_WHN1"})[i].text)

        # ratings
        ratings.append(product_html_access.find_all('div', {'class' : "_3LWZlK"})[i].text)

        #product link

        product_link_list = product_html_access.find_all( 'div', {'class' : '_2kHMtA'} )
        product_link.append(product_link_list[i]('a')[0]['href'])
    print(product_link)
    end_time = time.time()
    response_time=  end_time - start_time
    print('{} thi is the response time of the server'.format(response_time))
    return render_template('product.html', images=images_link, product_name=product_name, cost=cost, ratings=ratings, product_link = product_link)


@app.route('/reviews/<path:product_link>')
def Reviews(product_link) :
    reviews = []
    specific_product_path = urljoin(home_flipkart , product_link)
    print(specific_product_path)
    print(product_link)
    try :
        specific_product_url = urlopen( specific_product_path )
        specific_product_html = bs( specific_product_url.read(), 'html.parser' )

        # Check if the expected elements exist on the page before scraping
        if specific_product_html.find_all( 'div', {'class' : 't-ZTKy'} ) :
            print(specific_product_html)
            total_reviews = len( specific_product_html.find_all( 'div', {'class' : 't-ZTKy'} ) )
            for i in range( total_reviews ) :
                reviews.append( specific_product_html.find_all( 'div', {'class' : 't-ZTKy'} )[i].text )
            print(reviews)
            return render_template( 'reviews.html', reviews=reviews )
        else :
            # Handle the case where expected elements are not found on the page
            print(reviews)
            error_message = "Product page structure has changed. Unable to fetch reviews."
            return render_template( 'error.html', error_message=error_message )

    except Exception as e :
        # Handle any exceptions that may occur during scraping
        print( f"Error: {str( e )}" )
        error_message = "An error occurred while fetching product reviews."
        return render_template( 'error.html', error_message=error_message )


if __name__ == '__main__' :
    app.run( host='0.0.0.0',port=5000, debug=True)

