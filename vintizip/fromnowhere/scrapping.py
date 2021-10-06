import time
import fromnowhere.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class FromNoWhereScrapping(webdriver.Chrome):
    def __init__(self, driver_path = '/mnt/nas3/rjs/chromedriver', teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(FromNoWhereScrapping, self).__init__(options=options, executable_path=driver_path)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_shop_page(self): # 쇼핑몰 URL 리스트를 받는 함수
        return const.BASE_URL

    def land_first_page(self, url, i): # 페이지를 여는 함수
        self.get(url + f'&page={i}')

    def get_product_list(self): # 페이지에 존재하는 품목들을 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-normalpackage > div.xans-element-.xans-product.xans-product-listnormal > ul'
        xpath = '//*[starts-with(@id, "anchorBoxId_")]'
        product_list = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        products = product_list.find_elements_by_xpath(xpath) # 여기에 모든 element가 담김(리스트로)
        print(f'length: {len(products)}')
        return products 

    def get_product_category(self): # 품목 카테고리 가져오는 함수
        """ex: 니트 · 가디건"""
        css = '#contents > div.xans-element-.xans-product.xans-product-menupackage > div > h2'
        product_category = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_category = product_category.text
        print(product_category)
        return product_category

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
    
    def get_product_name(self): # 품목 이름을 가져오는 함수
        class_name = 'ndc_name'
        product_name = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        product_name = product_name.text
        print(f'name:{product_name}')
        return product_name

    def get_product_brand(self): # 품목 브랜드를 가져오는 함수
        """
        명시된 브랜드명을 그대로 가져옴
        우리 브랜드명에 맞춘 변환은 get_brand_list.py 함수에서 함
        실행은 get_clothes_info() 함수에서 받아서 변환
        """
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(2) > td'
        product_brand = WebDriverWait(self, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_brand = product_brand.text
        print(f'brand:{product_brand}')
        return product_brand

    def get_product_price(self): # 품목 가격을 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(5) > td > span'
        product_price = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_price = product_price.text
        product_price = product_price.replace(",", '').replace(" ", "").replace("KRW", '')
        print(f'price:{product_price}')
        return product_price

    def get_product_sale_price(self): # 할인 가격을 가져오는 함수
            return 0

    def get_product_size(self): # 품목 사이즈를 가져오는 함수
        id = 'prdDetail'
        product_sizes = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.ID, id))).get_attribute("innerHTML")
        product_sizes = product_sizes.strip().split('\n')
        try: # 가슴 사이즈가 있으면 가슴 사이즈만 추출
            product_size = [x for x in product_sizes if '가슴' in x][0].split('가슴')[1].split('cm')[0].strip()
            type_ = '가슴'
        except: # 가슴 사이즈 없고 허리 사이즈 있으면 허리 사이즈 추출
            product_size = [x for x in product_sizes if '허리' in x][0].split('허리')[1].split('cm')[0].strip()
            type_ = '허리'
        print(f'type: {type_}, size:{product_size}')
        return type_, product_size

    def get_product_thumbnail(self): # 썸네일 이미지를 가져오는 함수
        xpath = '//*[@id="contents"]/div[1]/div[1]/div[2]/div/img'
        product_thumbnail = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute('src')
        print(f'thumbnail:{product_thumbnail}')
        return product_thumbnail

    def get_product_sex(self): # 성별 구분하는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(3) > td'
        product_size = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_size = product_size.text
        if product_size[0] == 'W': # 사이즈에 WL, WM 이런 식으로 되어 있으면 여자꺼
            sex = 'women'
        else: # M, L, 이런식이면 남자꺼
            sex = 'men'
        print(f'product size:{product_size}, {sex}')
        return sex

    def get_product_category_type(self, product_category, sizing_name): # 품목 카테고리 구분하는 함수
        if product_category == '반팔 · 반바지':
            if sizing_name == '가슴':
                category = 'top'
            elif sizing_name == '허리':
                category = 'bottom'
        elif product_category == '치마 · 원피스':
            if sizing_name == '가슴':
                category = 'dress'
            elif sizing_name == '허리':
                category = 'skirt'
        elif product_category in ['후디 · 맨투맨', '셔츠 · 긴팔티', '니트 · 가디건']:
            category = 'top'
        elif product_category in ['코트 · 아우터', '점퍼 · 스포츠', '자켓 · 블루종']:
            category = 'outer'
        else: # 가끔 품목에 기타 카테고리가 있음
            category = 'others'
        print(f'category:{category}')
        return category

    def is_product_sold_out(self): # 품절 여부 확인하는 함수
        """sold out 아이콘이 있는지 체킹해서 품절 여부를 판단한다."""
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.headingArea > span.icon > img'
        try:
            product_sold_out = WebDriverWait(self, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
            product_sold_out.get_attribute('src')
            print(f'품절 상품') # img src가 있으면 sold out 아이콘이 있는 거니까 품절
            return True
        except: # img src가 없으면 판매중
            print(f'판매중인 상품')
            return False

if __name__ == '__main__':
    print(RelizmScrapping().get_shop_page())