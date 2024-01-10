import numpy as np
import os
import pandas as pd
os.getcwd()
df = pd.read_csv("2023Q3G_topline_PNLv0621.csv")
df = pd.DataFrame(df)
df = df.rename(columns={'shipment_final':'shipments','Total':'total_cost'})

df["mode"] = df.apply(lambda x: x.transportation_mode
                        if x.shipment_destination_route == "Ocean" else ("STAR"
                        if x.shipment_destination_route == "STAR" else ("STS"
                        if x.shipment_destination_route == "STS" else ("FO"
                        if x.transportation_mode == "FASTOCEAN" else "Stan")))
                        , axis=1)
df["region"] = df.apply(lambda x: x.shipment_destination_country
                        if x.shipment_destination_country == "EU" else ("US"
                        if x.shipment_destination_country == "US" else ("JP"
                        if x.shipment_destination_country == "JP" else "EU"))
                        , axis=1)
df['sort_type'].unique()
df['region'].unique()
df.to_excel('Q3G_new_df.xlsx')
#df = pd.to_numeric(df["revenue"])

###########################################
dfpv1 = pd.pivot_table(df,values=[u"units"]
                     ,index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",u"region",u"pol", u"pod"]
                     ,columns=[u"received_month"]
                     ,aggfunc=[np.sum])
dfpv1['index'] = 'units'
dfpv1.reset_index().to_excel('Q3G_new_pv1.xlsx')

dfpv2 = pd.pivot_table(df,values=[u"volume"]
                     ,index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",u"region",u"pol", u"pod"]
                     ,columns=[u"received_month"]
                     ,aggfunc=[np.sum])
dfpv2['index'] = 'volumes'
dfpv2.reset_index().to_excel('Q3G_new_pv2.xlsx')

dfpv3 = pd.pivot_table(df,values=[u"shipments"]
                     ,index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",u"region",u"pol", u"pod"]
                     ,columns=[u"received_month"]
                     ,aggfunc=[np.sum])
dfpv3['index'] = 'shipments'
dfpv3.reset_index().to_excel('Q3G_new_pv3.xlsx')

dfpv4 = pd.pivot_table(df,values=[u"revenue"]
                       , index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv4['index'] = 'revenue'
dfpv4.reset_index().to_excel('Q3G_new_pv4.xlsx')

dfpv5 = pd.pivot_table(df,values=[u"origin"]
                       , index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv5['index'] = 'origin'
dfpv5.reset_index().to_excel('Q3G_new_pv5.xlsx')

dfpv6 = pd.pivot_table(df,values=[u"PTP"]
                       , index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv6['index'] = 'PTP'
dfpv6.reset_index().to_excel('Q3G_new_pv6.xlsx')

dfpv7 = pd.pivot_table(df, values=[u"dest"]
                       , index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv7['index'] = 'dest'
dfpv7.reset_index().to_excel('Q3G_new_pv7.xlsx')

dfpv8 = pd.pivot_table(df, values=[u"dray"]
                       , index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv8['index'] = 'dray'
dfpv8.reset_index().to_excel('Q3G_new_pv8.xlsx')

dfpv9 = pd.pivot_table(df, values=[u"origin_access"]
                       , index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv9['index'] = 'origin_access'
dfpv9.reset_index().to_excel('Q3G_new_pv9.xlsx')

dfpv10 = pd.pivot_table(df, values=[u"dest_access"]
                       , index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv10['index'] = 'dest_access'
dfpv10.reset_index().to_excel('Q3G_new_pv10.xlsx')

dfpv11 = pd.pivot_table(df, values=[u"sustainability"]
                       , index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",
                                u"region", u"pol", u"pod"]
                       , columns=[u"received_month"]
                       , aggfunc=[np.sum])
dfpv11['index'] = 'sustainability'
dfpv11.reset_index().to_excel('Q3G_new_pv11.xlsx')

dfpv12 = pd.pivot_table(df, values=[u"total_cost"]
                        , index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",
                                 u"region", u"pol", u"pod"]
                        , columns=[u"received_month"]
                        , aggfunc=[np.sum])
dfpv12['index'] = 'total_cost'
dfpv12.reset_index().to_excel('Q3G_new_pv12.xlsx')

#############################################################################################

#result_try = pd.concat([dfpv1,dfpv2,dfpv3,dfpv4,dfpv5,dfpv6],ignore_index=True)
#result_try.to_excel('Q3G_result_try.xlsx')
#############################################################################################


#
dfpv = pd.DataFrame(columns=['received_month'])
print(dfpv)
indexes = ['units','volumes','shipments','revenue','origin','PTP','dest','dray','access','total_cost']
for i in indexes:
dfpv = pd.pivot_table(df, values=[i]
                        ,index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",u"pol", u"pod"]
                        , columns=[u"received_month"])
dfpv['index'] = [i]
dfpv = dfpv.append(dfpv)
print(dfpv)
dfpv.reset_index().to_excel('test_pv.xlsx')
dfpv1['index'] = 'Units'
#



#dfpv_final=pd.concat([dfpv1,dfpv2,dfpv3,dfpv4,dfpv5,dfpv6,dfpv7,dfpv8,dfpv9,dfpv10])
#print(dfpv_final)
#dfpv_final.reset_index().to_excel('test_pv_final.xlsx')

indexes = ['units','volumes','shipments','revenue','origin','PTP','dest','dray','access','total_cost']
for i in indexes:
dfpv = pd.pivot_table(df, values=[i]
                        ,index=[u"sort_type", u"transportation_submode_adj", u"mode", u"shipment_destination_country",u"pol", u"pod"]
                        , columns=[u"received_month"])


#sort_type, transportation_submode_adj(express=air)
#mode(transportation_mode选fastocean as fo，shipment_destination_route中的MLP as STAR，MVP as STS，其他为Stan)
#region(改写country),country(shipment_destination_country),pol,pod
#                        if x.transportation_mode != "FASTOCEAN" else "FO"
#                        if x.transportation_mode != "AIR" else "Stan"
#                        if x.shipment_destination_route != "OCEAN" else "Stan"
