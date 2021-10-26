import time
import oldgoods.constants as const
from utils.category_filter import category_filter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class OldgoodsScrapping(webdriver.Chrome):
    def __init__(self, driver_path = 'C:/chromedriver', teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(OldgoodsScrapping, self).__init__(options=options, executable_path=driver_path)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_shop_page(self):
        return const.BASE_URL, const.BASE_URL_NO

    def land_first_page(self, url, i): # 페이지를 여는 함수
        self.get(url + f'&page={i}')

    def get_product_category(self):
        css = '#contents > div.xans-element-.xans-product.xans-product-menupackage > div.xans-element-.xans-product.xans-product-headcategory.title > h2 > span'
        name = self.find_element_by_css_selector(css).text
        print(f'large category: {name}')
        return name

    def get_product_list(self): # 페이지에 존재하는 품목들을 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-normalpackage > div.xans-element-.xans-product.xans-product-listnormal > ul'
        xpath = '//*[starts-with(@id, "anchorBoxId_")]'
        product_list = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        products = product_list.find_elements_by_xpath(xpath) # 여기에 모든 element가 담김(리스트로)
        print(f'length: {len(products)}')
        return products 

    def click_product(self, iter): # 품목을 클릭하는 함수
        css1 = '#contents > div.xans-element-.xans-product.xans-product-normalpackage > div.xans-element-.xans-product.xans-product-listnormal > ul'
        xpath = '//*[starts-with(@id, "anchorBoxId_")]'
        css2 = 'div > a'
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
    
    def get_product_sale_price(self): # 할인 가격을 가져오는 함수
        css = '#totalProducts > table > tfoot > tr > td > span > strong > em'
        product_price = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_price = product_price.text
        product_price = product_price.replace(",", '').replace(" ", "").replace("원", '')
        print(f'sale price:{product_price}')
        return product_price

    def is_product_sold_out(self, product_price): # 품절 여부 확인하는 함수
        # price=0이면 품절
        return True if product_price == '0' else False


    def get_product_price(self): # 품목 가격을 가져오는 함수
        css = '#span_product_price_text'
        # 드라이버 재정의
        product_price = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_price = product_price.text
        product_price = product_price.replace(",", '').replace(" ", "").replace("원", '')
        print(f'price:{product_price}')
        return product_price


    def get_product_thumbnail(self): # 썸네일 이미지를 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.xans-element-.xans-product.xans-product-image.imgArea > div.keyImg > div > a > img'
        product_thumbnail = self.find_element_by_css_selector(css).get_attribute('src')
        print(f'thumbnail:{product_thumbnail}')
        return product_thumbnail

    def get_product_name(self): # 품목 이름을 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(1) > td > span'
        product_name = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_name = product_name.text.strip()
        print(f'name:{product_name}')
        return product_name


    def get_product_brand(self, product_name): # 품목 브랜드를 가져오는 함수
        """
        상품 이름에서 공백 기준 맨 앞 substring
        우리 브랜드명에 맞춘 변환은 get_brand_list.py 함수에서 함
        """
        product_brand = ''
        for word in product_name.split(' '):
            if word.encode().isalpha():
                product_brand += word
            else:
                break
        print(f'brand:{product_brand}')
        return product_brand


    def get_product_gender(self, product_name): # 성별 구분하는 함수
        for g in ['women', 'WOMEN', 'woman', 'WOMAN']:
            if g in product_name.split(' ')[-1]:
                print('gender:', g)
                return 'women'

        for g in ['men', 'MEN', 'MAN', 'man']:
            if g in product_name.split(' ')[-1]:
                print('gender:', g)
                return 'men'

        print('gender:', 'unisex')
        return 'unisex'

    def get_product_category_type(self, product_name, product_category): # 품목 카테고리 구분하는 함수
        return category_filter(category_name=product_category, product_name=product_name)

    def get_product_size(self): # 품목 사이즈를 가져오는 함수
        css = '#prdDetail > div > strong'
        size = self.find_element_by_css_selector(css).text
        if '반품' in size:
            type_ = '가슴'
            product_size = size.split('반품')[1].split(':')[1].strip()
            print(product_size)
            product_size = ''.join(s for s in product_size if s.isdigit())
        elif '허리' in size:
            type_ = '허리'
            product_size = size.split('허리')[1].split(':')[1].strip()
            print(product_size)
            product_size = ''.join(s for s in product_size if s.isdigit())
        print(f'type: {type_}, size: {product_size}')
        return type_, product_size
            
if __name__ == '__main__':
    print(OldgoodsScrapping().get_shop_page())