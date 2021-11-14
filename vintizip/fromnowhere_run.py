import time
from utils.data_to_json import DataToJson
from utils.get_brand_list import get_brand_list
from utils.get_clothes_info import get_clothes_info
from refine import transform
from fromnowhere.scrapping import FromNoWhereScrapping
from utils.time_check import time_check

start = time.time()
with FromNoWhereScrapping() as fromnowhere:
    soldout = False
    store_name = 'fromnowhere'
    file_name = f'{store_name}.json' 
    data = DataToJson(file_name)
    url_list = fromnowhere.get_shop_page()
    for url in url_list:
        for i in range(1, 200):
            if soldout:
                soldout = False
                break
            try:
                fromnowhere.land_first_page(url=url, i=i)
            except:
                print(e, '페이지 없음')
                break
            
            product_list = fromnowhere.get_product_list()
            for iter in range(len(product_list)):
                total_list = data.load_json()
                print('----------------{} page, {} -----------------'.format(i, iter+1))

                try:
                    product_category_name = fromnowhere.get_product_category()
                    product_link = fromnowhere.click_product(iter)
                    product_name = fromnowhere.get_product_name()
                    product_brand_before = fromnowhere.get_product_brand()
                    product_price = fromnowhere.get_product_price()
                    product_sale_price = fromnowhere.get_product_sale_price()
                    product_type, product_size = fromnowhere.get_product_size()
                    product_thumbnail = fromnowhere.get_product_thumbnail()
                    product_gender = fromnowhere.get_product_sex()
                    product_category = fromnowhere.get_product_category_type(product_category_name, product_type)
                    is_sold_out = fromnowhere.is_product_sold_out()
                    if is_sold_out:
                        soldout = True
                        break
                    product_brand_after = get_brand_list(product_brand_before)
                except Exception as e:
                    print(e)
                    time.sleep(0.5)
                    fromnowhere.land_first_page(url=url, i=i)
                    continue
                json_ = get_clothes_info(store_name, product_sale_price, product_name, product_category, product_gender,
        product_brand_after, product_price, product_thumbnail, product_link, is_sold_out, product_size, product_type)
                total_list.append(json_)
                time.sleep(0.5)
                fromnowhere.land_first_page(url=url, i=i)
                data.save_json(data=total_list)
                del total_list


_, exclude_soldout_list = transform(file_name)
data.save_json(data=exclude_soldout_list)

end = time.time()
time_check(store_name, start, end)