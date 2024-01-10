with atd_3m_cny_table_sl as (
  select
    t.order_id
    ,t.sp_id
    ,(t.fixed + t.promo + t.adjust_to_fix) as ocean_have_tax_amount_cny
    ,sum((t.fixed + t.promo + t.adjust_to_fix)) over (partition by nvl(case when nsl.group_id = '' then null else nsl.group_id end, t.sp_id)) as ocean_have_tax_amount_cny_osid
  from
    (select
          ci.order_id
          ,ci.sp_id
          ,sum(case when ci.charge_category <> 'OTHER'
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'CNY' then cast(cast(ci.have_tax_amount as double precision)*1 as double precision)
                    when ci.charge_category <> 'OTHER'
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'EUR' then cast(cast(ci.have_tax_amount as double precision)*7.6 as double precision)
                    when ci.charge_category <> 'OTHER'
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'GBP' then cast(cast(ci.have_tax_amount as double precision)*8.7 as double precision)
                    when ci.charge_category <> 'OTHER'
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'JPY' then cast(cast(ci.have_tax_amount as double precision)*0.052 as double precision)
                    when ci.charge_category <> 'OTHER'
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'USD' then cast(cast(ci.have_tax_amount as double precision)*7 as double precision)
                else 0
                end) as fixed
            ,sum(case when ci.charge_category = 'OTHER' AND UPPER(ci.remark) LIKE '%PROMOTION%'
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'CNY' then cast(cast(ci.have_tax_amount as double precision)*1 as double precision)
                    when ci.charge_category = 'OTHER' AND UPPER(ci.remark) LIKE '%PROMOTION%'
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'EUR' then cast(cast(ci.have_tax_amount as double precision)*7.6 as double precision)
                    when ci.charge_category = 'OTHER' AND UPPER(ci.remark) LIKE '%PROMOTION%'
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'GBP' then cast(cast(ci.have_tax_amount as double precision)*8.7 as double precision)
                    when ci.charge_category = 'OTHER' AND UPPER(ci.remark) LIKE '%PROMOTION%'
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'JPY' then cast(cast(ci.have_tax_amount as double precision)*0.052 as double precision)
                    when ci.charge_category = 'OTHER' AND UPPER(ci.remark) LIKE '%PROMOTION%'
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'USD' then cast(cast(ci.have_tax_amount as double precision)*7 as double precision)
                else 0
                end) as promo
            ,sum(case when  ci.charge_category = 'OTHER' AND (
                                             ci.remark LIKE '%头程%'
                                          OR ci.remark LIKE '%二程%'
                                          OR ci.remark LIKE '%固定%'
                                          OR ci.remark LIKE '%附加操作%'
                                          OR ci.remark LIKE '%操作附加%'
                                          OR ci.remark LIKE '%抵消运费%'
                                          OR ci.remark LIKE '%快船%')
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'CNY' then cast(cast(ci.have_tax_amount as double precision)*1 as double precision)
                    when  ci.charge_category = 'OTHER' AND (
                                             ci.remark LIKE '%头程%'
                                          OR ci.remark LIKE '%二程%'
                                          OR ci.remark LIKE '%固定%'
                                          OR ci.remark LIKE '%附加操作%'
                                          OR ci.remark LIKE '%操作附加%'
                                          OR ci.remark LIKE '%抵消运费%'
                                          OR ci.remark LIKE '%快船%')
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'EUR' then cast(cast(ci.have_tax_amount as double precision)*7.6 as double precision)
                    when  ci.charge_category = 'OTHER' AND (
                                             ci.remark LIKE '%头程%'
                                          OR ci.remark LIKE '%二程%'
                                          OR ci.remark LIKE '%固定%'
                                          OR ci.remark LIKE '%附加操作%'
                                          OR ci.remark LIKE '%操作附加%'
                                          OR ci.remark LIKE '%抵消运费%'
                                          OR ci.remark LIKE '%快船%')
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'GBP' then cast(cast(ci.have_tax_amount as double precision)*8.7 as double precision)
                    when  ci.charge_category = 'OTHER' AND (
                                             ci.remark LIKE '%头程%'
                                          OR ci.remark LIKE '%二程%'
                                          OR ci.remark LIKE '%固定%'
                                          OR ci.remark LIKE '%附加操作%'
                                          OR ci.remark LIKE '%操作附加%'
                                          OR ci.remark LIKE '%抵消运费%'
                                          OR ci.remark LIKE '%快船%')
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'JPY' then cast(cast(ci.have_tax_amount as double precision)*0.052 as double precision)
                    when  ci.charge_category = 'OTHER' AND (
                                             ci.remark LIKE '%头程%'
                                          OR ci.remark LIKE '%二程%'
                                          OR ci.remark LIKE '%固定%'
                                          OR ci.remark LIKE '%附加操作%'
                                          OR ci.remark LIKE '%操作附加%'
                                          OR ci.remark LIKE '%抵消运费%'
                                          OR ci.remark LIKE '%快船%')
                             and ci.trans_mode in ('OCEAN') and ci.sp_currency_code = 'USD' then cast(cast(ci.have_tax_amount as double precision)*7 as double precision)
                else 0
                end) as adjust_to_fix
          from
            gf.charge_item ci
          where
            upper(ci.charge_category) not in ('OTHER')
            and ci.order_id in (select distinct booking_id from agl.booking
                                where convert_timezone('Asia/Shanghai',atd) between '2023-07-01' and'2023-09-30' )
            and (charge_status NOT IN ('PENDING_ELIGIBILITY_FOR_AR','INELIGIBLE_FOR_AR','MOVED') OR charge_status is null)
          group by sp_id, ci.order_id
      ) t
    left join gf.new_seller_list nsl
    on nsl.sp_id = t.sp_id
  )

,login_table as (
    select login
    ,name
    ,case when team = 'SALES_MASS1' then 'SALES_MASS'
    when team = 'SALES_MASS2' then 'SALES_MASS'
    else team
    end as match_team
    from finance.staff sl
)

select distinct
  ac_sl.order_id
  ,oos.sp_id
  --,oos.program_type
  --,oc_oos.company
  ,case when nsl.group_id is not null then nsl.group_id
  else ncgl.group_id
  end as group_id
  ,oos.ocean_discount_item_first_leg as ocean_discount_AGL_SC_EU
  ,case when upper(oos.discount_size) = 'S' then 100
        when upper(oos.discount_size) = 'M' then 96
        when upper(oos.discount_size) = 'L' then 94
        when upper(oos.discount_size) = 'XL' then 92
        end as ocean_discount_sc_us
  ,case when sl.login is not null then sl.login
    else oos.sales_contact end as login
  ,case when nsl.final_sales is not null then nsl.final_sales
    else sl.name end as sales_names
  ,nsl.propsed_team
  ,cast(ac_sl.ocean_have_tax_amount_cny as double precision) as spid_revenue_rmb
  ,cast(ac_sl.ocean_have_tax_amount_cny_osid as double precision) as group_revenue_rmb
  ,oos.discount_effective_time
  ,oos.discount_expire_time
  ,gss.expire_date as gss_expire_date
  --,case when oos.ocean_discount_item_first_leg <> '92' then 'N'
  --    when oos.ocean_discount_item_first_leg = '92' and max(gss.expire_date) is null then oos.discount_expire_date
  --    else gss.expire_date end as discount_expire_date
  ,case -- when max(gss.expire_date) <= getdate() then 'N'
      when gss.expire_date > current_date then 'Y'  -- ocean_discount_item has value more then 92
      else 'N' end as is_gss
    -- expire date after 05.04 is gss Y
  ,oos.ocean_discount_item_first_leg as current_pricing_level
from
  g.o_oc_sp oos
  left join atd_3m_cny_table_sl ac_sl
      on oos.sp_id = ac_sl.sp_id
  left join gf.ocean_gss_discount_list gss
      on oos.sp_id = gss.seller_id
  --left join glstransdb1.g.o_oc_sp oc_oos
      --on oos.sp_id =oc_oos.sp_id
  left join gf.new_seller_list nsl
      on oos.sp_id = nsl.sp_id
  left join login_table sl
      on oos.sales_contact = sl.login
  left join gf.non_cn_grouplist ncgl
      on oos.sp_id = ncgl.sp_id
where --oc_oos.company not like '%测试%' and
      ac_sl.ocean_have_tax_amount_cny is not null
and oos.discount_size is not null
--and oos.program_type = 'FREIGHT'
group by ac_sl.order_id
  ,oos.sp_id
  --,oos.program_type
  --,oc_oos.company
  ,oos.ocean_discount_item_first_leg
  ,oos.discount_size
  ,ac_sl.ocean_have_tax_amount_cny
  ,ac_sl.ocean_have_tax_amount_cny_osid
  ,oos.discount_effective_time
  ,nsl.group_id
  ,nsl.final_sales
  ,nsl.propsed_team
  ,sl.login
  ,oos.discount_expire_time
  ,gss.expire_date
  ,oos.sales_contact
  ,sl.name
  ,ncgl.group_id