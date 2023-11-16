with h as (select g.month, g.wk, g.bk_id,
       case when a.dn_country in ('FR','IT','ES','DE','GB') then 'EU'
       else a.dn_country
       end as dn,
       g.product,
       case when a.bk_type = 'ST' then 'SR'
       else g.product
       end as type,
       cast(g.og_f as decimal(10,4)) as og, cast(g.pt_f as decimal(10,4)) as pt,
       cast(g.ds_f as decimal(10,4)) + cast(g.dy_f as decimal(10,4)) as ds,
       cast(g.ae_ori as decimal(10,4)) as og_ae,
       cast(g.ae_des as decimal(10,4)) as ds_ae,
       cast(g.ae_ori as decimal(10,4)) +cast(g.og_f as decimal(10,4)) as og_total,
       cast(g.pt_f as decimal(10,4)) as pt_total,
       cast(g.ae_des as decimal(10,4)) +cast(g.ds_f as decimal(10,4))+ cast(g.dy_f as decimal(10,4)) as ds_total,
       case when g.product = 'Air' then cast(g.og_f as decimal(10,4)) + cast(g.pt_f as decimal(10,4)) + cast(g.ds_f as decimal(10,4)) + cast(g.dy_f as decimal(10,4))
       else cast(g.og_f as decimal(10,4))+cast(g.pt_f as decimal(10,4))+cast(g.ds_f as decimal(10,4))+cast(g.ae_ori as decimal(10,4))+cast(g.ae_des as decimal(10,4))+cast(g.dy_f as decimal(10,4))
       end as Total,
       case when cast(g.og_f as decimal(10,4)) < 0 then 'check_again'
       when cast(g.pt_f as decimal(10,4)) < 0 then 'check_again'
       when cast(g.ds_f as decimal(10,4)) < 0 then 'check_again'
       when cast(g.ae_f as decimal(10,4)) < 0 then 'check_again'
       else ' ' end as check_cost
    from a.reporting g
    left join b.bk a
    on g.bk_Id = a.bk_id
    where a.bk_status != 'CANCELLED' and a.bk_status is not null and g.month in ('202307','202308','202309'))

select h.*,
       isnull(h.og_total/nullif(h.Total,0),null) as og_ratio,
       isnull(h.pt_total/nullif(h.Total,0),null) as pt_ratio,
       isnull(h.ds_total/nullif(h.Total,0),null) as ds_ratio,
       round(isnull((h.og_total+h.pt_total+h.ds_total)/nullif(h.Total,0),null),10) as total_ratio,
       case when isnull(h.og_total/nullif(h.Total,0),null)>1 then 'og_ratio>1'
       when isnull(h.pt_total/nullif(h.Total,0),null)>1 then 'pt_ratio>1'
       when isnull(h.ds_total/nullif(h.Total,0),null)>1 then 'ds_ratio>1'
       end as check_ratio
from h;
