import time
import regarment.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class RegarmentScrapping(webdriver.Chrome):
    def __init__(self, driver_path = 'C:/chromedriver', teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(RegarmentScrapping, self).__init__(options=options, executable_path=driver_path)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_shop_page(self):
        return const.BASE_URL, const.BASE_URL_NO

    def land_first_page(self, url, i): # 페이지를 여는 함수
        self.get(url + f'&page={i}')

    def get_product_list(self): # 페이지에 존재하는 품목들을 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-listnormal.ec-base-product.prdlist_default > ul'
        xpath = '//*[starts-with(@id, "anchorBoxId_")]'
        product_list = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        products = product_list.find_elements_by_xpath(xpath) # 여기에 모든 element가 담김(리스트로)
        print(f'length: {len(products)}')
        return products 
        
    def get_product_category(self): # 품목 카테고리 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-menupackage > div.xans-element-.xans-product.xans-product-headcategory.title > h2 > span'
        category = self.find_element_by_css_selector(css).text.strip()
        print(category)
        return category

    def click_product(self, iter): # 품목을 클릭하는 함수
        css1 = '#contents > div.xans-element-.xans-product.xans-product-listnormal.ec-base-product.prdlist_default > ul'
        xpath = '//*[starts-with(@id, "anchorBoxId_")]'
        css2 = 'div > div.prdImg > a'
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
        css = '#detail_info_wrap > div.detailArea > div.infoArea > div.headingArea > h2 > span.icon > img'
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
        css = '#detail_info_wrap > div.detailArea > div.xans-element-.xans-product.xans-product-image.imgArea > div.keyImg > div.thumbnail > a > img'
        product_thumbnail = self.find_element_by_css_selector(css).get_attribute('src')
        print(f'thumbnail:{product_thumbnail}')
        return product_thumbnail

    def get_product_name(self): # 품목 이름을 가져오는 함수
        css = '#detail_info_wrap > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(2) > td > span'
        product_name = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_name = product_name.text.strip()
        print(f'name:{product_name}')
        return product_name

    def get_product_brand(self): # 품목 브랜드를 가져오는 함수
        """
        상품 이름에서 공백 기준 맨 앞 substring
        우리 브랜드명에 맞춘 변환은 get_brand_list.py 함수에서 함
        """
        css = '#detail_info_wrap > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(1) > td > span'
        product_brand = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css))).text.strip()
        print(f'brand:{product_brand}')
        return product_brand

    def get_product_price(self): # 품목 가격을 가져오는 함수
        css = '#span_product_price_text'
        product_price = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_price = product_price.text
        product_price = product_price.replace(",", '').replace(" ", "").replace("₩", '').split('(')[0]
        print(f'price:{product_price}')
        return product_price

    def get_product_sale_price(self): # 할인 가격을 가져오는 함수
        css = '#span_product_price_sale'
        try:
            product_sale_price = self.find_element_by_css_selector(css).text.replace(",", '').replace(" ", "").replace("₩", '').split('(')[0]
        except:
            product_sale_price = 0
        print(f'sale_price:{product_sale_price}')
        return product_sale_price



    def get_product_gender(self): # 성별 구분하는 함수
        return 'women'

    def get_product_category_type(self, product_category, product_name): # 품목 카테고리 구분하는 함수
        if product_category == 'OUTERWEAR':
            category = 'outer'
        elif product_category in ['T&SHIRTS', 'KNIT & CARDIGAN']:
            category = 'top'
        elif product_category == 'DRESS & BOTTOM':
            if '원피스' in product_name:
                category = 'dress'
            elif ('스커트' in product_name) or ('치마' in product_name):
                category = 'skirt'
            else:
                category = 'bottom'
        elif product_category in ['1%', 'LEATHER & FUR']:
            if '원피스' in product_name:
                category = 'dress'
            elif ('스커트' in product_name) or ('치마' in product_name):
                category = 'skirt'
            elif ('코트' in product_name) or ('자켓' in product_name) or ('블루종' in product_name):
                category = 'outer'
            elif ('바지' in product_name) or ('팬츠' in product_name):
                category = 'bottom'
            else:
                category = 'top'
        print(f'category:{category}')
        return category

    def get_product_size(self): # 품목 사이즈를 가져오는 함수
        css = '#detail_info_wrap > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(7) > td > span'
        size = self.find_element_by_css_selector(css).text
        if ('가슴' in size) and ('허리' in size):
            type_ = '가슴'
        elif '가슴' in size:
            type_ = '가슴'
        elif '허리' in size:
            type_ = '허리'
        else:
            css = '#detail_info_wrap > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(6) > td > span'
            size = self.find_element_by_css_selector(css).text
            if ('가슴' in size) and ('허리' in size):
                type_ = '가슴'
            elif '가슴' in size:
                type_ = '가슴'
            elif '허리' in size:
                type_ = '허리'
            else:
                css = '#detail_info_wrap > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(5) > td > span'
                size = self.find_element_by_css_selector(css).text
                if ('가슴' in size) and ('허리' in size):
                    type_ = '가슴'
                elif '가슴' in size:
                    type_ = '가슴'
                elif '허리' in size:
                    type_ = '허리'
                else:
                    raise Exception('사이즈 타입을 찾을 수 없습니다.')
        product_size = size.split(type_)[1].strip().split(' ')[0].strip()
        print(f'type: {type_}, size: {product_size}')
        return type_, product_size
            
if __name__ == '__main__':
    print(RegarmentScrapping().get_shop_page())