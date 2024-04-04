
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def check_about_page(url):
    ''' Takes the url to the homepage of a website as input
        Returns either a valid URL to the brand's about page or returns None '''
    
    # Check the homepage URL is working and available
    try:
        if requests.get(url).status_code != 200:
            print(f'Domain {url} unavailable')
            return None
    except:
        print(f'Domain {url} unavailable')
        return None
    
    # Possible extensions for the about page
    about_urls = ['about', 'about-us', 'our-story', 'pages/about', 'pages/about-us', 'pages/our-story', 'p/about', 'p/about-us', 'p/our-story']  
    for ext in about_urls:
        # Checks if the proposed URL is valid and available
        try:
            response = requests.get(url + ext) 
        except:
            continue
        if response.status_code == 200:
            return url + ext
    
    print('About page for ', url, ' not found')
    return None


def check_product_page(url):
    ''' Takes the url to the homepage of a website as input
        Returns either a valid URL to the brand's about page or returns None '''      
    # Check the homepage URL is working and available
    try:
        if requests.get(url).status_code != 200:
            print(f'Domain {url} unavailable')
            return None
    except:
        print(f'Domain {url} unavailable')
        return None
    
    # Possible extensions for the about page 
    product_urls = ['collections', 'all-products', 'products', 'services', 'shop', 'shop-all', 'pages/collections', 'pages/all-products', 'pages/products', 'pages/services', 'pages/shop', 'pages/shop-all', 'p/collections', 'p/all-products', 'p/products', 'p/services', 'p/shop', 'p/shop-all']  
    for ext in product_urls:
        # Checks if the proposed URL is valid
        try:
            response = requests.get(url + ext) 
        except:
            continue
        if response.status_code == 200:
            return url + ext
            
    return None


def find_about_page(url):
    '''Find the link to the about page by searching hyperlinks on the homepage'''
    # Check that the homepage URL is valid
    try:
        response = requests.get(url)
    except:
        print('Homepage unavailable for ' + url)
        return None

    if response.status_code != 200:
        print('Homepage URL failed for ' + url)
        return None
    
    # Parse HTML content of homepage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Search for each possible link text on the homepage
    about_text = ['About', 'About Us', 'The Brand', 'Our Story', 'History', 'Mission', 'Our Mission', 'Who We Are']
    for text in about_text:
        about_page_link = soup.find('a', text=text)
        if about_page_link:
            try: about_page_url = urljoin(url, about_page_link['href'])
            except: continue
            return about_page_url
            
    # Check for any other link text starting with "About ..."
    about_page_link = soup.find('a', text=lambda x: x and x.startswith('About'))
    if about_page_link:
        try: about_page_url = urljoin(url, about_page_link['href'])
        except: return None
        return about_page_url

    # If no match is found, return None
    return None


def find_product_page(url):
    '''Find the link to the product page by searching hyperlinks on the homepage'''
    # Check that the homepage URL is valid
    try:
        response = requests.get(url)
    except:
        print('Homepage unavailable for ' + url)
        return None
        
    if response.status_code != 200:
        print('Homepage URL failed for ' + url)
        return None
    
    # Parse HTML content of homepage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Search for each possible link text on the homepage
    product_text = ['Shop', 'Shop All', 'Services', 'Collections', 'Products']
    for text in product_text:
        product_page_link = soup.find('a', text=text)
        if product_page_link:
            try: product_page_url = urljoin(url, product_page_link['href'])
            except: continue
            return product_page_url

    # If no match is found, return None
    return None


def remove_tags(text):
    '''Remove all opening and closing tag pairs from an htlm page formated as a string'''
    temp = text
    while temp.find('<') > -1:
        temp = temp[:temp.find('<')] + temp[temp.find('>')+1:]

    temp = ' '.join(temp.split())
    return temp.strip()

def clean_website_text(text, min_len, search_tags):
    paragraphs = [remove_tags(t.prettify()) for t in text.find_all(search_tags)]
    return '\n'.join([p for p in paragraphs if len(p) > min_len])

def get_text_from_url(url, clean=True, min_para_len=100, search_tags=['p', 'h1', 'h2']):
    '''Extract text without html tags from a website'''
    # Fetch HTML content of the about page
    try:
        response = requests.get(url)
    except:
        return None
    
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        return None
        
    # Parse and return HTML content of the about page
    soup = BeautifulSoup(response.text, 'html.parser')
    if clean:
        return clean_website_text(soup, min_len=min_para_len, search_tags=search_tags)
    else:
        return soup



def get_home_page(homepage_url):
    '''Returns the text without html tags of a website's about page'''
    return get_text_from_url(homepage_url, min_para_len=20)

def get_about_page(homepage_url):
    '''Returns the text without html tags of a website's about page'''
    about_url = check_about_page(homepage_url)
    if about_url == None:
        about_url = find_about_page(homepage_url)
        if about_url == None:
            return None
    
    return get_text_from_url(about_url)

def get_product_page(homepage_url):
    '''Returns the text without html tags of a website's product or services page'''
    product_url = check_product_page(homepage_url)
    if product_url == None:
        product_url = find_product_page(homepage_url)
        if product_url == None:
            return None
    
    return get_text_from_url(product_url)