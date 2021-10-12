import time
from utils.data_to_json import DataToJson
from utils.get_brand_list import get_brand_list
from utils.get_clothes_info import get_clothes_info
from refine import transform
from denia.scrapping import DeniaScrapping

with DeniaScrapping() as denia:
    soldout = False
    checked = False
    store_name = 'denia'
    file_name = f'{store_name}.json' 
    data = DataToJson(file_name)
    base_url, url_list = denia.get_shop_page()
    for n in url_list:
        for i in range(1, 200):
            if soldout:
                soldout = False
                break
            try:
                denia.land_first_page(url=base_url+str(n), i=i)
            except:
                print(e, '페이지 없음')
                break
            denia.click_box(checked)
            checked=True
            product_list = denia.get_product_list()
            product_category_name = denia.get_product_category()
            for iter in range(len(product_list)):
                total_list = data.load_json()
                print('----------------{} page, {} -----------------'.format(i, iter+1))

                try:
                    product_thumbnail = denia.get_product_thumbnail(product_list, iter)
                    product_link = denia.click_product(iter)
                    product_name = denia.get_product_name()
                    is_sold_out = denia.is_product_sold_out()
                    if is_sold_out:
                        soldout = True
                        break
                    product_brand_before = denia.get_product_brand(product_name)
                    product_price = denia.get_product_price()
                    product_sale_price = denia.get_product_sale_price()
                    product_type, product_size = denia.get_product_size()
                    product_gender = denia.get_product_gender(url)
                    product_category = denia.get_product_category_type(product_category_name, product_name)
                    product_brand_after = get_brand_list(product_brand_before)
                except Exception as e:
                    print(e)
                    time.sleep(0.5)
                    denia.land_first_page(url=base_url+str(n), i=i)
                    continue
                json_ = get_clothes_info(store_name, product_sale_price, product_name, product_category, product_gender,
        product_brand_after, product_price, product_thumbnail, product_link, is_sold_out=False, product_size=product_size, product_type=product_type)
                total_list.append(json_)
                time.sleep(0.5)
                denia.land_first_page(url=base_url+str(n), i=i)
                data.save_json(data=total_list)
                del total_list


_, exclude_soldout_list = transform(file_name)
data.save_json(data=exclude_soldout_list)
