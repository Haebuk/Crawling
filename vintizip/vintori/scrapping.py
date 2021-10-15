import time
import vintori.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class VintoriScrapping(webdriver.Chrome):
    def __init__(self, driver_path = 'C:/chromedriver', teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(VintoriScrapping, self).__init__(options=options, executable_path=driver_path)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_shop_page(self):
        return const.BASE_URL, const.BASE_URL_NO

    def land_first_page(self, url, i): # 페이지를 여는 함수
        self.get(url + f'&page={i}')

    def get_product_category(self):
        css = '#contents > div.xans-element-.xans-product.xans-product-menupackage > div.xans-element-.xans-product.xans-product-headcategory.tit-product > h2 > span'
        name = self.find_element_by_css_selector(css).text
        print(f'large category: {name}')
        return name

    def get_product_list(self): # 페이지에 존재하는 품목들을 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-normalpackage > div.xans-element-.xans-product.xans-product-listnormal.df-prl-wrap.df-prl-setup > ul'
        xpath = '//*[starts-with(@id, "anchorBoxId_")]'
        product_list = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        products = product_list.find_elements_by_xpath(xpath) # 여기에 모든 element가 담김(리스트로)
        print(f'length: {len(products)}')
        return products 
        
    def click_product(self, iter): # 품목을 클릭하는 함수
        css1 = '#contents > div.xans-element-.xans-product.xans-product-normalpackage > div.xans-element-.xans-product.xans-product-listnormal.df-prl-wrap.df-prl-setup > ul'
        xpath = '//*[starts-with(@id, "anchorBoxId_")]'
        css2 = 'div > div.df-prl-thumb > a'
        # 드라이버 재정의
        product_list = WebDriverWait(self, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, css1)))
        products = product_list.find_elements_by_xpath(xpath)
        # url
        product_link = products[iter].find_element_by_css_selector(css2).get_attribute('href')
        print(f'link:{product_link}')
        # 박스 클릭
        self.get(product_link)
        time.sleep(0.5)
        return product_link
    
    def is_product_sold_out(self): # 품절 여부 확인하는 함수
        css = '#df-product-detail > div > div.infoArea-wrap > div > div > div.scroll-wrapper.df-detail-fixed-scroll.scrollbar-macosx > div.df-detail-fixed-scroll.scrollbar-macosx.scroll-content > div.headingArea > span.icon > img'
        try:
            ele = WebDriverWait(self, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, css))).get_attribute('src')
            if ele:
                print('품절 상품') 
                return True
            else:
                print('판매중인 상품')
                return False
        except: 
            print('판매중인 상품')
            return False

    def get_product_thumbnail(self): # 썸네일 이미지를 가져오는 함수
        css = '#df-product-detail > div > div.imgArea-wrap > div > div > div.thumbnail > span > img'
        product_thumbnail = self.find_element_by_css_selector(css).get_attribute('src')
        print(f'thumbnail:{product_thumbnail}')
        return product_thumbnail

    def get_product_name(self): # 품목 이름을 가져오는 함수
        css = '#df-product-detail > div > div.infoArea-wrap > div > div > div.scroll-wrapper.df-detail-fixed-scroll.scrollbar-macosx > div.df-detail-fixed-scroll.scrollbar-macosx.scroll-content > div.headingArea > h2 > span'
        product_name = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_name = product_name.text.split('(')[0].strip()
        print(f'name:{product_name}')
        return product_name

    def get_product_brand(self): # 품목 브랜드를 가져오는 함수
        """
        상품 이름에서 공백 기준 맨 앞 substring
        우리 브랜드명에 맞춘 변환은 get_brand_list.py 함수에서 함
        """
        css = '#df-product-detail > div > div.infoArea-wrap > div > div > div.scroll-wrapper.df-detail-fixed-scroll.scrollbar-macosx > div.df-detail-fixed-scroll.scrollbar-macosx.scroll-content > div.headingArea > span.vintoribrand'
        product_brand = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css))).text.replace(' ', '')
        print(f'brand:{product_brand}')
        return product_brand

    def get_product_price(self): # 품목 가격을 가져오는 함수
        css = '#span_product_price_text'
        product_price = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_price = product_price.text
        product_price = product_price.replace(",", '').replace(" ", "").replace("원", '')
        print(f'price:{product_price}')
        return product_price

    def get_product_sale_price(self): # 할인 가격을 가져오는 함수
        css = '#span_product_price_sale'
        try:
            product_sale_price = self.find_element_by_css_selector(css).text.replace(",", '').replace(" ", "").replace("원", '')
        except:
            product_sale_price = 0
        print(f'sale_price:{product_sale_price}')
        return product_sale_price

    def get_product_gender(self): # 성별 구분하는 함수
        css = '#df-product-detail > div > div.infoArea-wrap > div > div > div.scroll-wrapper.df-detail-fixed-scroll.scrollbar-macosx > div.df-detail-fixed-scroll.scrollbar-macosx.scroll-content > div.headingArea > h2 > span'
        gender = self.find_element_by_css_selector(css).text
        gender = gender.split('(')[1].split(' ')[0]
        print(f"gender: {gender}")
        return 'women'

    def get_product_category_type(self, product_name): # 품목 카테고리 구분하는 함수
        if 'DRESS' in product_name:
            category = 'dress'
        elif 'SKIRT' in product_name:
            category = 'skirt'
        elif ('JEANS' in product_name) or ('PANTS' in product_name) or ('CHINO' in product_name) or ('SLACKS' in product_name):
            category = 'bottom'
        elif ('COAT' in product_name) or ('JACKET' in product_name) or ('CARDIGAN' in product_name) or ('BLAZER' in product_name) or ('JUMPER' in product_name) or ('PADDING' in product_name) or ('WINDBREAKER'):
            category = 'outer'
        else:
            category = 'top'
        print(f'category:{category}')
        return category

    def get_product_size(self): # 품목 사이즈를 가져오는 함수
        css = '#vintori-container > div.vintori-boards > table'
        size = self.find_element_by_css_selector(css).text
        list1 = size.split('\n')[0].split(' ')
        list2 = size.split('\n')[1].split(' ')
        if '가슴' in list1:
            type_ = '가슴'
            product_size = list2[list1.index('가슴')]
        elif '허리' in list1:
            type_ = '허리'
            product_size = list2[list1.index('허리')] 
        print(f'type: {type_}, size: {product_size}')
        return type_, product_size
            
if __name__ == '__main__':
    print(VintoriScrapping().get_shop_page())