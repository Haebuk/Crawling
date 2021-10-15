import time
from utils.data_to_json import DataToJson
from utils.get_brand_list import get_brand_list
from utils.get_clothes_info import get_clothes_info
from refine import transform
from vintori.scrapping import VintoriScrapping

with VintoriScrapping() as vintori:
    soldout = False
    store_name = 'vintori'
    file_name = f'{store_name}.json'
    data = DataToJson(file_name)
    base_url, url_list = vintori.get_shop_page()
    for n in url_list:
        for i in range(2, 200):
            if soldout:
                soldout = False
                break
            try:
                vintori.land_first_page(url=base_url+str(n), i=i)
            except:
                print(e, '페이지 없음')
                break
            product_list = vintori.get_product_list()
            product_category_name = vintori.get_product_category()
            for iter in range(len(product_list)):
                total_list = data.load_json()
                print('----------------{} page, {} -----------------'.format(i, iter+1))

                try:
                    product_link = vintori.click_product(iter)
                    is_sold_out = vintori.is_product_sold_out()
                    if is_sold_out:
                        soldout = True
                        break
                    product_thumbnail = vintori.get_product_thumbnail()
                    product_name = vintori.get_product_name()
                    product_brand_before = vintori.get_product_brand()
                    product_gender = vintori.get_product_gender()
                    product_price = vintori.get_product_price()
                    product_sale_price = vintori.get_product_sale_price()
                    product_category = vintori.get_product_category_type( product_name)
                    product_type, product_size = vintori.get_product_size()
                    product_brand_after = get_brand_list(product_brand_before)
                except Exception as e:
                    print(e)
                    time.sleep(0.5)
                    vintori.land_first_page(url=base_url+str(n), i=i)
                    continue
                json_ = get_clothes_info(store_name, product_sale_price, product_name, product_category, product_gender,
        product_brand_after, product_price, product_thumbnail, product_link, is_sold_out=False, product_size=product_size, product_type=product_type)
                total_list.append(json_)
                time.sleep(0.5)
                vintori.land_first_page(url=base_url+str(n), i=i)
                data.save_json(data=total_list)
                del total_list


_, exclude_soldout_list = transform(file_name)
data.save_json(data=exclude_soldout_list)
