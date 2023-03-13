select *

from my_warehouse.provider

where 1
    and month(conclusion_date) = '$month'
    and year(conclusion_date) = '$year'