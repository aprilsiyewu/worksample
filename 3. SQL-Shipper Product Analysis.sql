with aobp_a_amp as
(select a.shipper_id,a.placement_option, a.submission_time,
       row_number() over (partition by a.shipper_id order by a.submission_time desc) as submit_time_rank_awd
       from agl_everest_data_center.agl_operation_booking_prod a
where a.shipment_type in ('FCL','LCL')
and a.placement_option = 'GLOBAL_MILE_OPTIMIZED'
and a.booking_status not in ('CANCELLED')
and a.submission_time between '2023-01-01' and current_date
)

, aobp_a2_amp as (
select * from aobp_a_amp a
where a.submit_time_rank_awd = 1
)

, aobp_b_amp as (
select b.shipper_id,b.placement_option, b.submission_time,
       row_number() over (partition by b.shipper_id order by b.submission_time asc) as submit_time_rank_noawd
       from agl_everest_data_center.agl_operation_booking_prod b
where b.shipment_type in ('FCL','LCL')
and b.placement_option != 'GLOBAL_MILE_OPTIMIZED'
and b.booking_status not in ('CANCELLED')
and b.submission_time between '2023-01-01' and current_date
)

, aobp_b2_amp as (
select * from aobp_b_amp b
where b.submit_time_rank_noawd = 1
)

, amp_mark as (select a.shipper_id, a.placement_option as new_type, a.submission_time as max_awd_submit_time,
b.placement_option as old_type, b.submission_time as max_noawd_submit_time
from aobp_a2_amp a left join aobp_b2_amp b
on a.shipper_id = b.shipper_id
where a.submission_time > b.submission_time)

, aobp_a_awd as
(select a.shipper_id,a.booking_type, a.submission_time,
       row_number() over (partition by a.shipper_id order by a.submission_time desc) as submit_time_rank_awd
       from agl_everest_data_center.agl_operation_booking_prod a
where a.shipment_type in ('FCL','LCL')
and a.booking_type = 'STAR'
and a.booking_status not in ('CANCELLED')
and a.submission_time between '2023-01-01' and current_date

)

, aobp_a2_awd as (
select * from aobp_a_awd a
where a.submit_time_rank_awd = 1
)

, aobp_b_awd as (
select b.shipper_id,b.booking_type, b.submission_time,
       row_number() over (partition by b.shipper_id order by b.submission_time asc) as submit_time_rank_noawd
       from agl_everest_data_center.agl_operation_booking_prod b
where b.shipment_type in ('FCL','LCL')
and b.booking_type != 'STAR'
and b.booking_status not in ('CANCELLED')
and b.submission_time between '2023-01-01' and current_date
--and b.shipper_id = 'WWQ2TYCUYCZMY'
)

, aobp_b2_awd as (
select * from aobp_b_awd b
where b.submit_time_rank_noawd = 1
)

, awd_mark as (
select a.shipper_id, a.booking_type as new_type, a.submission_time as max_awd_submit_time,
b.booking_type as old_type, b.submission_time as max_noawd_submit_time
from aobp_a2_awd a left join aobp_b2_awd b
on a.shipper_id = b.shipper_id
where a.submission_time > b.submission_time)

select
b.booking_id,
b.shipper_id,
nsl.group_id,
b.atd,
b.ofa_id,
left(b.atd,7) atd_month,
b.submission_time,
left(b.submission_time,7) submit_month,
--a.shipper_currency_code,
b.shipment_type,
case when wbr.shipment_type != 'AIR' and wbr.speed_mode  =  'STANDARD' then 'OCEAN'
       when wbr.shipment_type != 'AIR' and wbr.speed_mode  =  'FastOcean' then 'FASTOCEAN'
       when wbr.shipment_type = 'AIR' then 'AIR'
else NULL end as transportation_mode,
--sum(cast(a.have_tax_amount as double precision)) as rev_amt,
--sum (case when a.shipper_currency_code = 'CNY' then cast(cast(a.have_tax_amount as double precision)*1 as double precision)
--       when a.shipper_currency_code = 'USD' then cast(cast(a.have_tax_amount as double precision)*7.23 as double precision)
--       when a.shipper_currency_code = 'EUR' then cast(cast(a.have_tax_amount as double precision)*7.85 as double precision)
--       when a.shipper_currency_code = 'GBP' then cast(cast(a.have_tax_amount as double precision)*9.15 as double precision)
--       else 0
--       end) as rev_amt_CNY,
b.source_channel,
wbr.volume_unit,
wbr.volume_value,
bw.unit as OC_unit,
case when wbr.ib_fin is not null then wbr.est_units else 0 end as ib_units,
b.origin as pol,
b.pod,
b.cargo_ready_date,
left(b.cargo_ready_date,7) as cargo_ready_month,
case when b.placement_option = 'GLOBAL_MILE_OPTIMIZED'  then 'AMP'
                        when b.placement_option = 'GLOBAL_MILE_PREMIUM' then 'MSS'
                        when b.placement_option is null then 'MSS'
                        else b.placement_option end as placement_option,
case when amp.shipper_id is not null then 'Convert_to_AMP' else ' ' end as if_convert_amp,
case when b.booking_type = 'STS' THEN 'STS'
                        when b.booking_type = 'STAR' THEN 'AWD'
                        when b.booking_type = 'FBA Inbound' THEN ' '
                        when b.booking_type is null then 'MSS'
                        else b.booking_type end as booking_type,
case when awd.shipper_id is not null then 'Convert_to_AWD' else ' ' end as if_convert_awd,
payment_method,
b.destination as destination_fc,
sysdate as last_refresh_time
from agl_everest_data_center.agl_operation_booking_prod b
--left join andes.gmp_global_shipping_prod.fba_import_gm_charge_item a on a.order_id = b.booking_id
left join gift_finance.d_gmc_fba_wbr_dd wbr on wbr.booking_id = b.booking_id
left join gift_finance.booking_weight bw on bw.booking_id = b.booking_id
left join gift_finance.new_seller_list nsl on nsl.shipper_id = b.shipper_id
left join awd_mark awd on awd.shipper_id = b.shipper_id
left join amp_mark amp on amp.shipper_id = b.shipper_id
where b.shipment_type in ('FCL','LCL')
and b.booking_status not in ('CANCELLED')
and b.submission_time between '2023-01-01' and current_date
--and (a.charge_category not in ('OTHER')
--or a.charge_category is null) --add括号improve此条件，否则null值会被miss掉
--and nsl.group_id in (1183)
group by 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25
