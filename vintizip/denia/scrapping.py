import time

from numpy.core.fromnumeric import prod
import denia.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class DeniaScrapping(webdriver.Chrome):
    def __init__(self, driver_path = 'C:/Chromedriver', teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(DeniaScrapping, self).__init__(options=options, executable_path=driver_path)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_shop_page(self):
        return const.BASE_URL, const.BASE_URL_NO

    def click_box(self, checked=False):
        if not checked:
            element = self.find_element_by_css_selector('#popup_1 > iframe')
            self.switch_to.frame(element)
            box = self.find_element_by_id('popup_close_check')
            box.click()
            close = self.find_element_by_id('popup_close_btn')
            close.click()
            print('팝업 창 닫기')
            self.switch_to.default_content()
        else:
            print('팝업 창 없음')
            return

    def land_first_page(self, url, i): # 페이지를 여는 함수
        self.get(url + f'&page={i}')

    def get_product_list(self): # 페이지에 존재하는 품목들을 가져오는 함수
        css = '#contents > div > div.xans-element-.xans-product.xans-product-normalpackage > div.xans-element-.xans-product.xans-product-listnormal > ul'
        xpath = '//*[starts-with(@id, "anchorBoxId_")]'
        product_list = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        products = product_list.find_elements_by_xpath(xpath) # 여기에 모든 element가 담김(리스트로)
        print(f'length: {len(products)}')
        return products 

    def get_product_thumbnail(self, iter): # 썸네일 이미지를 가져오는 함수
        css1 = '#contents > div > div.xans-element-.xans-product.xans-product-normalpackage > div.xans-element-.xans-product.xans-product-listnormal > ul'
        xpath = '//*[starts-with(@id, "anchorBoxId_")]'
        css2 = 'div > a > img'
        # 드라이버 재정의
        product_thumbnail = self.find_element_by_css_selector(css1).find_elements_by_xpath(xpath)[iter].find_element_by_css_selector(css2).get_attribute('src')
        print(f'thumbnail:{product_thumbnail}')
        return product_thumbnail
        
    def get_product_category(self): # 품목 카테고리 가져오는 함수
        css = '#contents > div > div.xans-element-.xans-product.xans-product-headcategory.title > h2 > span'
        category = self.find_element_by_css_selector(css).text.strip()
        if category in ['아우터', '블레이저', '패딩', '스포츠/후리스']:
            product_category = 'outer'
        elif category in ['셔츠/티', '맨투맨/후드', '니트/가디건', '1/2탑', '1/2 탑']:
            product_category = 'top'
        elif category in ['팬츠', '2/1팬츠']:
            product_category = 'bottom'
        elif category == '원피스':
            product_category = 'dress'
        elif category == '스커트':
            product_category = 'skirt'
        else:
            product_category = 'others'
        print(category)
        return product_category

    def is_product_sold_out(self): # 품절 여부 확인하는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.infoArea > div.icon > img'
        try:
            WebDriverWait(self, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
            print('품절 상품') 
            return True
        except: 
            print('판매중인 상품')
            return False

    def click_product(self, iter): # 품목을 클릭하는 함수
        css1 = '#contents > div > div.xans-element-.xans-product.xans-product-normalpackage > div.xans-element-.xans-product.xans-product-listnormal > ul'
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
    
    def get_product_name(self): # 품목 이름을 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.infoArea > h3'
        product_name = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_name = product_name.text.split('\n')[0].strip()
        print(f'name:{product_name}')
        return product_name

    def get_product_brand(self, product_name): # 품목 브랜드를 가져오는 함수
        """
        상품 이름에서 공백 기준 맨 앞 substring
        우리 브랜드명에 맞춘 변환은 get_brand_list.py 함수에서 함
        """
        product_brand = product_name.split(' ')[0]
        print(f'brand:{product_brand}')
        return product_brand

    def get_product_price(self): # 품목 가격을 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(2) > td > span'
        product_price = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_price = product_price.text
        product_price = product_price.replace(",", '').replace(" ", "").replace("₩", '')
        print(f'price:{product_price}')
        return product_price

    def get_product_sale_price(self): # 할인 가격을 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(3) > td > span > span'
        try:
            product_sale_price = self.find_element_by_css_selector(css).text.replace(",", '').replace(" ", "").replace("₩", '')
        except:
            product_sale_price = 0
        print(f'sale_price:{product_sale_price}')
        return product_sale_price

    def get_product_size(self): # 품목 사이즈를 가져오는 함수
        css = '#prdDetail > div'
        product_sizes = self.find_element_by_css_selector(css).get_attribute('innerHTML')
        product_sizes = product_sizes.strip().split('실측')[1]
        print(product_sizes)
        if '가슴' in product_sizes:
            product_size = product_sizes.split('가슴')[1].split('- ')[1].split('&')[0]
            type_ = '가슴'
        else:
            product_size = product_sizes.split('허리')[1].split(' ')[1].split('&')[0]
            type_ = '허리'
        print(f'type: {type_}, size:{product_size}')
        return type_, product_size


    def get_product_gender(self, n): # 성별 구분하는 함수
        if n in const.BASE_URL_NO[:11]:
            gender = 'men'
        else:
            gender = 'women'
        print(f'gender: {gender}')
        return gender


if __name__ == '__main__':
    print(DeniaScrapping().get_shop_page())