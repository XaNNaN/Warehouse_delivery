select  p.name,
        p.telephone,
        d.id_del as del_id,
        d.del_date as del_date

from provider as p

join delivery as d using (id_prov)

where 1
      and p.name = '$name'