with b AS (select g.month, g.wk,
       g.booking_id, g.pol, g.pod,
       nvl2(g.ori_fc,g.ori_fc,'N/A') as ori_fc, nvl2(g.final_fc,g.final_fc,'N/A') as final_fc, g.product,
       a.destination_country as destination,
       case when a.speed_mode = 'PREMIUM' then 'premium'
           else 'standard'
           end as premium,
       to_date(a.received_in_CS,'yyyy-mm-dd') as CS, to_date(a.AD,'yyyy-mm-dd') as AD, to_date(a.gate_in,'yyyy-mm-dd') as GD,
       case when product in ('Air','LCL') and received_in_CS is not null then to_date(received_in_CS,'yyyy-mm-dd')
           when product in ('Air','LCL') and received_in_CS is null then to_date(a.AD,'yyyy-mm-dd')
           when product in ('FCL') and gate_in is not null then to_date(a.gate_in,'yyyy-mm-dd')
           when product in ('FCL') and gate_in is null then to_date(a.AD,'yyyy-mm-dd')
           end as service_start_date,
       to_date(a.AA,'yyyy-mm-dd') as AA,
       to_date(a.cargo_delivery,'yyyy-mm-dd') as delivery_date,
       a.booking_status as status,
       case when a.received_in_CS > a.AD then 'CS>AD'
           when a.gate_in > a.AD then 'GD>AD'
           when a.AD is null then 'no_AD'
           when a.cargo_delivery is null then 'no_DD'
           when product in ('Air','LCL') and received_in_CS is not null and received_in_CS > a.cargo_delivery then 'SD>DD'
           when product in ('Air','LCL') and received_in_CS is null and a.AD > a.cargo_delivery then 'SD>DD'
           when product in ('FCL') and gate_in is not null and gate_in > a.cargo_delivery then 'SD>DD'
           when product in ('FCL') and gate_in is null and a.AD > a.cargo_delivery then 'SD>DD'
           else 'SA_Base'
           end as remark_SA,
       case when a.booking_type = 'STS' then 'STAR'
           else g.product
           end as type,
       case when a.AA < a.AD then 'AA<AD'
           when a.AA = a.cargo_delivery then 'AA=DD'
           when a.AA > a.cargo_delivery then 'AA>DD'
           when a.received_in_CS > a.AD then 'CS>AD'
           when a.gate_in > a.AD then 'GD>AD'
           when a.AA is null then 'no_AA'
           when a.AD is null then 'no_AD'
           when a.cargo_delivery is null then 'no_DD'
           when product in ('Air','LCL') and received_in_CS is not null and received_in_CS > a.cargo_delivery then 'SD>DD'
           when product in ('Air','LCL') and received_in_CS is null and a.AD > a.cargo_delivery then 'SD>DD'
           when product in ('FCL') and gate_in is not null and gate_in > a.cargo_delivery then 'SD>DD'
           when product in ('FCL') and gate_in is null and a.AD > a.cargo_delivery then 'SD>DD'
           else 'Milestone_Base'
           end as remark_Milestone,
       case when product in ('Air','LCL') and received_in_CS is not null then to_date(a.cargo_delivery,'yyyy-mm-dd')- to_date(received_in_CS,'yyyy-mm-dd')
          when product in ('Air','LCL') and received_in_CS is null then to_date(a.cargo_delivery,'yyyy-mm-dd')- to_date(a.AD,'yyyy-mm-dd')
          when product in ('FCL') and gate_in is not null then to_date(a.cargo_delivery,'yyyy-mm-dd')- to_date(a.gate_in,'yyyy-mm-dd')
          when product in ('FCL') and gate_in is null then to_date(a.cargo_delivery,'yyyy-mm-dd')- to_date(a.AD,'yyyy-mm-dd')
          end as SA

from gift_finance.gmf_report_mec g
left join agl_everest_dAA_center.agl_operation_booking_prod a
on g.booking_Id = a.booking_id
where a.booking_status != 'CANCELLED' and a.booking_status is not null and g.month in ('202203','202204','202205'))

select b.*,
       product||'_'||right(pol,3)||'_'||left(final_fc,3)||'_'||premium as SA_Key_FC,
       product||'_'||right(pol,3)||'_'||destination||'_'||premium as SA_Key_Dest
from b;
