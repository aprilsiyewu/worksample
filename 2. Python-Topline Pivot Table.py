import numpy as np
import os
import pandas as pd

os.getcwd()
planning_cycle = '2024Q3G'
df = pd.read_csv("2024Q3G_OP_Tablecsv.csv",low_memory=False)  #export PNL into csv file directly
final_output = "2024Q3G_Breakdown_Topline_PNL_v0704V2.xlsx"
df = pd.DataFrame(df)

df = df.rename(columns={'shipment':'shipments','tot_dest':'dest','tot_sus':'sustainability','Total':'total_cost'
                       ,'3P_transload':'3P Transloader','3P_linehaul':'3P Linehaul'
                        ,'IPC_Topside_NS':'IPC Topside NS','CXD_Topside_S':'CXD Topside S'})

df['total_cost'] = df['origin'] + df['PTP'] + df['dest'] + df['dray'] + df['origin_access'] + df['dest_access'] + df['sustainability'] + df['3P Transloader'] + df['3P Linehaul'] + df['IPC Topside NS'] + df['CXD Topside S']

df["speed_mode"] = df.apply(lambda x: x.transportation_mode
                        if x.shipment_destination_route == "Ocean" else ("FO"
                        if x.transportation_mode == "FASTOCEAN" else "Stan")
                        , axis=1)
df["region"] = df.apply(lambda x: x.shipment_destination_country
                        if x.shipment_destination_country == "EU" else ("US"
                        if x.shipment_destination_country == "US" else ("JP"
                        if x.shipment_destination_country == "JP" else "EU"))
                        , axis=1)
df['sort_type'].unique()
df['region'].unique()
df['revenue'] = pd.to_numeric(df["revenue"])
df['product'] = df['transportation_submode_adj']

#df.to_excel(planning_cycle + '_new_df.xlsx')

###########################################
#1 units
dfpv1 = pd.pivot_table(df,values=[u"units"]
                     ,index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",u"region",u"pol", u"pod"]
                     ,columns=[u"received_month"]
                     ,aggfunc=[np.sum])
dfpv1['index'] = 'units'

#2 volume
dfpv2 = pd.pivot_table(df,values=[u"volume"]
                     ,index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",u"region",u"pol", u"pod"]
                     ,columns=[u"received_month"]
                     ,aggfunc=[np.sum])
dfpv2['index'] = 'volumes'

#3 shipments
dfpv3 = pd.pivot_table(df,values=[u"shipments"]
                     ,index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",u"region",u"pol", u"pod"]
                     ,columns=[u"received_month"]
                     ,aggfunc=[np.sum])
dfpv3['index'] = 'shipments'

#4 revenue
dfpv4 = pd.pivot_table(df,values=[u"revenue"]
                       , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv4['index'] = 'revenue'

#5 origin
dfpv5 = pd.pivot_table(df,values=[u"origin"]
                       , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv5['index'] = 'origin'

#6 PTP
dfpv6 = pd.pivot_table(df,values=[u"PTP"]
                       , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv6['index'] = 'PTP'

#7 dest
dfpv7 = pd.pivot_table(df, values=[u"dest"]
                       , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv7['index'] = 'dest'

#8 dray
dfpv8 = pd.pivot_table(df, values=[u"dray"]
                       , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv8['index'] = 'dray'

#9 orgin_access
dfpv9 = pd.pivot_table(df, values=[u"origin_access"]
                       , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv9['index'] = 'origin_access'

#10 dest_access
dfpv10 = pd.pivot_table(df, values=[u"dest_access"]
                       , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv10['index'] = 'dest_access'

#11 sustainability
dfpv11 = pd.pivot_table(df, values=[u"sustainability"]
                       , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv11['index'] = 'sustainability'

#12 total cost
dfpv12 = pd.pivot_table(df, values=[u"total_cost"]
                        , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                 u"region", u"pol", u"pod"]
                        , columns=[u"received_month"]
                        , aggfunc=[np.sum])
dfpv12['index'] = 'total_cost'

#13 3P Transloader
dfpv13 = pd.pivot_table(df, values=[u"3P Transloader"]
                        , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                 u"region", u"pol", u"pod"]
                        , columns=[u"received_month"]
                        , aggfunc=[np.sum])
dfpv13['index'] = '3P Transloader'

#14 3P Linehaul
dfpv14 = pd.pivot_table(df, values=[u"3P Linehaul"]
                        , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                 u"region", u"pol", u"pod"]
                        , columns=[u"received_month"]
                        , aggfunc=[np.sum])
dfpv14['index'] = '3P Linehaul'


#15 IPC Topside NS
dfpv15 = pd.pivot_table(df, values=[u"IPC Topside NS"]
                        , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                 u"region", u"pol", u"pod"]
                        , columns=[u"received_month"]
                        , aggfunc=[np.sum])
dfpv15['index'] = 'IPC Topside NS'

#16 CXD Topside S
dfpv16 = pd.pivot_table(df, values=[u"CXD Topside S"]
                        , index=[u"shipment_destination_route", u"sort_type", u"product", u"speed_mode", u"shipment_destination_country",
                                 u"region", u"pol", u"pod"]
                        , columns=[u"received_month"]
                        , aggfunc=[np.sum])
dfpv16['index'] = 'CXD Topside S'


#combine all pivot tables together
dfpv1.reset_index(inplace = True)
dfpv1.columns = dfpv1.columns.droplevel(1)
dfpv1.columns = dfpv1.columns.droplevel(1)

dfpv2.reset_index(inplace = True)
dfpv2.columns = dfpv2.columns.droplevel(1)
dfpv2.columns = dfpv2.columns.droplevel(1)

dfpv3.reset_index(inplace = True)
dfpv3.columns = dfpv3.columns.droplevel(1)
dfpv3.columns = dfpv3.columns.droplevel(1)

dfpv4.reset_index(inplace = True)
dfpv4.columns = dfpv4.columns.droplevel(1)
dfpv4.columns = dfpv4.columns.droplevel(1)

dfpv5.reset_index(inplace = True)
dfpv5.columns = dfpv5.columns.droplevel(1)
dfpv5.columns = dfpv5.columns.droplevel(1)

dfpv6.reset_index(inplace = True)
dfpv6.columns = dfpv6.columns.droplevel(1)
dfpv6.columns = dfpv6.columns.droplevel(1)

dfpv7.reset_index(inplace = True)
dfpv7.columns = dfpv7.columns.droplevel(1)
dfpv7.columns = dfpv7.columns.droplevel(1)

dfpv8.reset_index(inplace = True)
dfpv8.columns = dfpv8.columns.droplevel(1)
dfpv8.columns = dfpv8.columns.droplevel(1)

dfpv9.reset_index(inplace = True)
dfpv9.columns = dfpv9.columns.droplevel(1)
dfpv9.columns = dfpv9.columns.droplevel(1)

dfpv10.reset_index(inplace = True)
dfpv10.columns = dfpv10.columns.droplevel(1)
dfpv10.columns = dfpv10.columns.droplevel(1)

dfpv11.reset_index(inplace = True)
dfpv11.columns = dfpv11.columns.droplevel(1)
dfpv11.columns = dfpv11.columns.droplevel(1)

dfpv12.reset_index(inplace = True)
dfpv12.columns = dfpv12.columns.droplevel(1)
dfpv12.columns = dfpv12.columns.droplevel(1)

dfpv13.reset_index(inplace = True)
dfpv13.columns = dfpv13.columns.droplevel(1)
dfpv13.columns = dfpv13.columns.droplevel(1)

dfpv14.reset_index(inplace = True)
dfpv14.columns = dfpv14.columns.droplevel(1)
dfpv14.columns = dfpv14.columns.droplevel(1)

dfpv15.reset_index(inplace = True)
dfpv15.columns = dfpv15.columns.droplevel(1)
dfpv15.columns = dfpv15.columns.droplevel(1)

dfpv16.reset_index(inplace = True)
dfpv16.columns = dfpv16.columns.droplevel(1)
dfpv16.columns = dfpv16.columns.droplevel(1)

df_final = pd.concat([dfpv1, dfpv2, dfpv3, dfpv4, dfpv5, dfpv6, dfpv7, dfpv8,
                     dfpv9, dfpv10, dfpv11, dfpv12, dfpv13, dfpv14, dfpv15, dfpv16], axis=0, join='outer',ignore_index=True)

df_final.to_excel(final_output,index=False)

print(df_final.shape[0])
print('All done')
