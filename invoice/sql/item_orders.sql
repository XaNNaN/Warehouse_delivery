select  id_product_info,
        name,
        category,
        material,
        unit_of_measurment

from my_warehouse.product_info

where 1
    and id_product_info= '$id_product_info'