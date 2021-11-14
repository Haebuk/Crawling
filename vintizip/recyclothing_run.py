import time
from utils.data_to_json import DataToJson
from utils.get_brand_list import get_brand_list
from utils.get_clothes_info import get_clothes_info
from refine import transform
from recyclothing.scrapping import RecyclothingScrapping
from utils.time_check import time_check

start = time.time()
with RecyclothingScrapping() as recyclothing:
    soldout = False
    store_name = 'recyclothing'
    file_name = f'{store_name}.json' 
    data = DataToJson(file_name)
    url_list = recyclothing.get_shop_page()
    for url in url_list:
        for i in range(1, 200):
            if soldout:
                soldout = False
                break
            try:
                recyclothing.land_first_page(url=url, i=i)
            except:
                print(e, '페이지 없음')
                break
            
            product_list = recyclothing.get_product_list()
            product_category_name = recyclothing.get_product_category(url)
            for iter in range(len(product_list)):
                total_list = data.load_json()
                print('----------------{} page, {} -----------------'.format(i, iter+1))

                try:
                    product_link = recyclothing.click_product(iter)
                    product_name = recyclothing.get_product_name()
                    is_sold_out = recyclothing.is_product_sold_out()
                    if is_sold_out:
                        soldout = True
                        break
                    product_brand_before = recyclothing.get_product_brand(product_name)
                    product_price = recyclothing.get_product_price()
                    product_sale_price = recyclothing.get_product_sale_price()
                    product_type, product_size = recyclothing.get_product_size()
                    product_thumbnail = recyclothing.get_product_thumbnail()
                    product_gender = recyclothing.get_product_gender(url)
                    product_category = recyclothing.get_product_category_type(product_category_name, product_name)
                    product_brand_after = get_brand_list(product_brand_before)
                except Exception as e:
                    print(e)
                    time.sleep(0.5)
                    recyclothing.land_first_page(url=url, i=i)
                    continue
                json_ = get_clothes_info(store_name, product_sale_price, product_name, product_category, product_gender,
        product_brand_after, product_price, product_thumbnail, product_link, is_sold_out=False, product_size=product_size, product_type=product_type)
                total_list.append(json_)
                time.sleep(0.5)
                recyclothing.land_first_page(url=url, i=i)
                data.save_json(data=total_list)
                del total_list


_, exclude_soldout_list = transform(file_name)
data.save_json(data=exclude_soldout_list)

end = time.time()
time_check(store_name, start, end)