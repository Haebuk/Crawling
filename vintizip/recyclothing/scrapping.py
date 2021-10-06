import re
import recyclothing.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class RecyclothingScrapping(webdriver.Chrome):
    def __init__(self, driver_path = 'C:/Chromedriver', teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(RecyclothingScrapping, self).__init__(options=options, executable_path=driver_path)
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
        product_list = WebDriverWait(self, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        products = product_list.find_elements_by_xpath(xpath) # 여기에 모든 element가 담김(리스트로)
        print(f'product 개수: {len(products)}')
        return products 

    def get_product_category(self, url): # 품목 카테고리 가져오는 함수
        if url.split('=')[-1] in ['46', '47']:
            product_category = 'outer'
        elif url.split('=')[-1] in ['48', '49']:
            product_category = 'top'
        else:
            product_category = 'bottom'
        print(product_category)
        return product_category

        """sold out 아이콘이 있는지 체킹해서 품절 여부를 판단한다."""
    def is_product_sold_out(self): # 품절 여부 확인하는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.headingArea > span.icon > img'
        try:
            WebDriverWait(self, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
            print('품절 상품') 
            return True
        except: 
            print('판매중인 상품')
            return False

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
        return product_link

    def get_product_name(self): # 품목 이름을 가져오는 함수
        class_name = 'ndc_name'
        product_name = WebDriverWait(self, 3).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        product_name = product_name.text
        print(f'name:{product_name}')
        return product_name


    def get_product_brand(self, product_name): # 품목 브랜드를 가져오는 함수
        """
        이름을 공백 구분 리스트로 변환한 후, 대문자가 있는 인덱스를 추출해서 브랜드 명을 뽑는다.
        우리 브랜드명에 맞춘 변환은 get_brand_list.py 함수에서 함
        실행은 get_clothes_info() 함수에서 받아서 변환
        """
        name_to_list = product_name.split(' ')
        return name_to_list[0]


    def get_product_price(self): # 품목 가격을 가져오는 함수
        id = 'span_product_price_text'
        product_price = WebDriverWait(self, 3).until(EC.presence_of_element_located((By.ID, id)))
        product_price = product_price.text
        product_price = product_price.replace(",", '').replace(" ", "").replace("원", '')
        print(f'price:{product_price}')
        return product_price

    def get_product_sale_price(self): # 할인 가격을 가져오는 함수
        try:
            id = 'span_product_price_sale'
            product_sale_price = WebDriverWait(self, 3).until(EC.presence_of_element_located((By.ID, id)))
            product_sale_price = product_sale_price.text.split('원')[0].replace(',', '')
            print(f'sale price:{product_sale_price}')
            return product_sale_price
        except:
            print('할인 없음')
            return 0

    def get_product_size(self): # 품목 사이즈를 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(3)'
        product_sizes = WebDriverWait(self, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, css))).get_attribute("innerHTML")
        product_sizes = product_sizes.strip().split('\n')
        try: # 가슴 사이즈가 있으면 가슴 사이즈만 추출
            product_size = [x for x in product_sizes if '가슴' in x][0].split('가슴')[1].strip()
            product_size = re.sub('[^0-9]', '', product_size) # 숫자만 추출
            type_ = '가슴'
        except: # 가슴 사이즈 없고 허리 사이즈 있으면 허리 사이즈 추출
            product_size = [x for x in product_sizes if '허리' in x][0].split('허리')[1].strip()
            product_size = re.sub('[^0-9]', '', product_size) # 숫자만 추출
            type_ = '허리'
        print(f'type: {type_}, size:{product_size}')
        return type_, product_size

    def get_product_thumbnail(self): # 썸네일 이미지를 가져오는 함수
        css = '#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.xans-element-.xans-product.xans-product-image.imgArea > div > img'
        product_thumbnail = WebDriverWait(self, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, css))).get_attribute('src')
        print(f'thumbnail:{product_thumbnail}')
        return product_thumbnail

    def get_product_gender(self, url): # 성별 구분하는 함수
        if url.split('=')[-1] in ['46', '48', '50']:
            return 'men'
        else:
            return 'women'

    def get_product_category_type(self, product_category, name): # 품목 카테고리 구분하는 함수
        if product_category == 'bottom':
            if 'skirt' in name:
                return 'skirt'
        return product_category


if __name__ == '__main__':
    print(RelizmScrapping().get_shop_page())