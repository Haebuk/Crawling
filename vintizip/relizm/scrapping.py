import time
import relizm.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class RelizmScrapping(webdriver.Chrome):
    def __init__(self, driver_path = '/mnt/nas3/rjs/chromedriver', teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(RelizmScrapping, self).__init__(options=options, executable_path=driver_path)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_shop_page(self): # 쇼핑몰 URL 리스트를 받는 함수
        return const.BASE_URL

    def land_first_page(self, url, i): # 페이지를 여는 함수
        self.get(url + f'&page={i}')

    def get_product_list(self): # 페이지에 존재하는 품목들을 가져오는 함수
        css = '#contents > div > div > div.xans-element-.xans-product.xans-product-listnormal > ul'
        xpath = '//*[starts-with(@id, "anchorBoxId_")]'
        product_list = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        products = product_list.find_elements_by_xpath(xpath) # 여기에 모든 element가 담김(리스트로)
        print(f'length: {len(products)}')
        return products 

    def get_product_category(self): # 품목 카테고리 가져오는 함수
        """ex: OUTWEAR"""
        css = '#contents > div > div > div.xans-element-.xans-product.xans-product-headcategory.title > h2'
        product_category = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_category = product_category.text
        print(product_category)
        return product_category

    def click_product(self, iter): # 품목을 클릭하는 함수
        css1 = '#contents > div > div > div.xans-element-.xans-product.xans-product-listnormal > ul'
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
        time.sleep(1)
        return product_link
    
    def get_product_name(self): # 품목 이름을 가져오는 함수
        css = '#contents > div:nth-child(1) > div.xans-element-.xans-product.xans-product-detail > div > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(1) > td > span'
        product_name = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_name = product_name.text.strip().split('\n')[1]
        print(f'name:{product_name}')
        return product_name

    def get_product_brand(self): # 품목 브랜드를 가져오는 함수
        """
        명시된 브랜드명을 그대로 가져옴
        우리 브랜드명에 맞춘 변환은 get_brand_list.py 함수에서 함
        실행은 get_clothes_info() 함수에서 받아서 변환
        """
        css = '#contents > div:nth-child(1) > div.xans-element-.xans-product.xans-product-detail > div > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(1) > td > span > b'
        product_brand = WebDriverWait(self, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_brand = product_brand.text[1:-1]
        print(f'brand:{product_brand}')
        return product_brand

    def get_product_price(self): # 품목 가격을 가져오는 함수
        css = '#span_product_price_text'
        product_price = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_price = product_price.text
        product_price = product_price.replace(",", '').replace(" ", "").replace("￦", '')
        print(f'price:{product_price}')
        return product_price

    def get_product_sale_price(self): # 할인 가격을 가져오는 함수
        css = '#span_product_coupon_dc_price'
        product_sale_price = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_sale_price = product_sale_price.text.split(' ')[0] # \금액
        product_sale_price = product_sale_price.replace(",", '').replace(" ", "").replace("￦", '')
        print(f'sale_price:{product_sale_price}')
        return product_sale_price

    def get_product_size(self): # 품목 사이즈를 가져오는 함수
        id = 'prdDetail'
        product_sizes = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.ID, id))).get_attribute("innerHTML")
        product_sizes = product_sizes.strip().split('\n')

        for parse in product_sizes:
            if '가슴' in parse:
                type_ = '가슴'
                product_size = parse.split('가슴')[1].split(':')[1].strip()[:2]
                print(f'type: {type_}, size:{product_size}')
                return type_, product_size
            elif '허리' in parse:
                type_ = '허리'
                product_size = parse.split('허리')[1].split(':')[1].strip()[:2]
                print(f'type: {type_}, size:{product_size}')
                return type_, product_size
        type_ = '프리'
        product_size = '0'
        print(f'type: {type_}, size:{product_size}')
        return type_, product_size


    def get_product_thumbnail(self): # 썸네일 이미지를 가져오는 함수
        css = '#contents > div:nth-child(1) > div.xans-element-.xans-product.xans-product-detail > div > div.xans-element-.xans-product.xans-product-image.imgArea > div > div > img'
        product_thumbnail = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css))).get_attribute('src')
        print(f'thumbnail:{product_thumbnail}')
        return product_thumbnail


    def get_product_sex(self): # 성별 구분하는 함수
        css = '#contents > div:nth-child(1) > div.xans-element-.xans-product.xans-product-detail > div > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(1) > td > span'
        product_size = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_size = product_size.text.replace('[', '').replace(']','').split(' ')
        if 'MEN' in product_size: 
            sex = 'men'
        elif "WOMEN" in product_size: 
            sex = 'women'
        elif "UNISEX" in product_size:
            sex = 'unisex'
        print(f'gender:{sex}')
        return sex

    def get_product_category_type(self, product_category, name): # 품목 카테고리 구분하는 함수
        if '리버시블' in name.split(' ') or '세트' in name.split(' '):
            category = 'others'
        elif product_category == 'OUTWEAR':
            category ='outer'
        elif product_category in ['KNIT,CARDICAN', 'TOP', 'TOP(S/S)']:
            category = 'top'
        elif product_category in ['BOTTOM']:
            if '스커트' in name.split(' '):
                category = 'skirt'
            else:
                category = 'bottom'
        elif product_category == 'DRESS':
            category = 'dress'
        else:
            category = 'others'
        
        print(f'category:{category}')
        return category

    def is_product_sold_out(self): # 품절 여부 확인하는 함수
        
        css = '#contents > div:nth-child(1) > div.xans-element-.xans-product.xans-product-detail > div > div.infoArea > div.xans-element-.xans-product.xans-product-action > div.ec-base-button > a.first.displaynone'
        try:
            WebDriverWait(self, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
            print(f'품절 상품') # img src가 있으면 sold out 아이콘이 있는 거니까 품절
            return True
        except: # img src가 없으면 판매중
            print(f'판매중인 상품')
            return False

if __name__ == '__main__':
    print(RelizmScrapping().get_shop_page())