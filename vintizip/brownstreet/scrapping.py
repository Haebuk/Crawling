import time
import brownstreet.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class BrownstreetScrapping(webdriver.Chrome):
    def __init__(self, driver_path = 'C:/chromedriver', teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(BrownstreetScrapping, self).__init__(options=options, executable_path=driver_path)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_shop_page(self):
        return const.BASE_URL, const.BASE_URL_NO

    def land_first_page(self, url, i): # 페이지를 여는 함수
        self.get(url + f'&page={i}')

    def get_product_category(self):
        css = '#catetitle > h2'
        name = self.find_element_by_css_selector(css).text
        print(f'large category: {name}')
        return name

    def get_product_list(self): # 페이지에 존재하는 품목들을 가져오는 함수
        css = '#contents > div:nth-child(6) > div.xans-element-.xans-product.xans-product-listnormal.ga09list > ul'
        xpath = '//*[starts-with(@id, "anchorBoxId_")]'
        product_list = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        products = product_list.find_elements_by_xpath(xpath) # 여기에 모든 element가 담김(리스트로)
        print(f'length: {len(products)}')
        return products 

    def get_product_price(self, iter): # 품목 가격을 가져오는 함수
        css = '#contents > div:nth-child(6) > div.xans-element-.xans-product.xans-product-listnormal.ga09list > ul'
        xpath1 = '//*[starts-with(@id, "anchorBoxId_")]'
        xpath2 = 'div/div[3]/p[1]'
        # 드라이버 재정의
        product_list = WebDriverWait(self, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        products = product_list.find_elements_by_xpath(xpath1)
        product_price = products[iter].find_element_by_xpath(xpath2).get_attribute('innerHTML').split('KRW ')[1].split('<')[0].replace(',', '')
        print(f'price:{product_price}')
        return product_price
        
    def click_product(self, iter): # 품목을 클릭하는 함수
        css1 = '#contents > div:nth-child(6) > div.xans-element-.xans-product.xans-product-listnormal.ga09list > ul'
        xpath = '//*[starts-with(@id, "anchorBoxId_")]'
        css2 = 'div > div.prdline > a'
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
        css = '#prdbox > div:nth-child(2) > div > div.icon > img'
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
        css = '#contents > div:nth-child(6) > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.xans-element-.xans-product.xans-product-image.imgArea > div.keyImg > div > img'
        product_thumbnail = self.find_element_by_css_selector(css).get_attribute('src')
        print(f'thumbnail:{product_thumbnail}')
        return product_thumbnail

    def get_product_name(self): # 품목 이름을 가져오는 함수
        css = '#prdbox > div:nth-child(2) > div'
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

    def get_product_sale_price(self): # 할인 가격을 가져오는 함수
        css = '#span_product_price_text'
        product_price = WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        product_price = product_price.text
        product_price = product_price.replace(",", '').replace(" ", "").replace("KRW", '')
        print(f'sale price:{product_price}')
        return product_price

    def get_product_gender(self, product_name): # 성별 구분하는 함수
        for g in ['men', 'MEN', 'MAN', 'man']:
            if g in product_name.split(' ')[-1]:
                print('gender:', g)
                return 'men'
        for g in ['women', 'WOMEN', 'woman', 'WOMAN']:
            if g in product_name.split(' ')[-1]:
                print('gender:', g)
                return 'women'

        print('gender:', 'unisex')
        return 'unisex'

    def get_product_category_type(self, product_name, product_category): # 품목 카테고리 구분하는 함수
        for c in ['OUTERS', '코트', '아우터', '사파리', '패딩', '데님자켓', '블레이저', '후드집업/후리스', '가디건']:
            if c in product_name:
                if '세트' in product_name:
                    category = 'others'
                    print(f'category:{category}')
                    return category
                else:
                    category = 'outer'
                    print(f'category:{category}')
                    return category

        for c in ['팬츠', '1/2 팬츠', '데님팬츠']:
            if c in product_category:
                category = 'bottom'
                print(f'category:{category}')
                return category 
        if product_category == 'PANT':
            if '스커트' in product_name:
                category = 'skirt'
                print(f'category:{category}')
                return category 
            else:
                category = 'bottom'
                print(f'category:{category}')
                return category 
        elif product_category == '드레스':
            category = 'dress'
        if product_category == '스포츠':
            if '팬츠' in product_name:
                category = 'bottom'
                print(f'category:{category}')
                return category 
            else:
                category = 'top'
                print(f'category:{category}')
                return category 
        else:
            category = 'top'
            print(f'category:{category}')
            return category

    def get_product_size(self): # 품목 사이즈를 가져오는 함수
        css = '#prddetailimg'
        size = self.find_element_by_css_selector(css).text.split('\n')[0]
        print(size)
        # list1 = size.split('\n')[0].split(' ')
        # list2 = size.split('\n')[1].split(' ')
        if '가슴' in size:
            type_ = '가슴'
            product_size = size.split('가슴: ')[1].split(' ')[0]
        elif '허리' in size:
            type_ = '허리'
            product_size = size.split('허리: ')[1].split(' ')[0]
        print(f'type: {type_}, size: {product_size}')
        return type_, product_size
            
if __name__ == '__main__':
    print(BrownstreetScrapping().get_shop_page())