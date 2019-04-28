import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
sns.set(style="white", palette="muted", color_codes=True)
sns.set_context("poster")
os.chdir("data/")

NAICS_col_name = ["cns01", "cns02", "cns04",
                  "cns05", "cns06", "cns07", "cns08"]

result_df_dict = {
    "Original Route": pd.read_csv("OriginRoute.csv"),
    "Designated Route 1": pd.read_csv("DesignRoute1.csv"),
    "MDOT Route": pd.read_csv("MDOTRoute.csv"),
    "Designated Route 2": pd.read_csv("DesignRoute2.csv")
}

otm = pd.read_csv("otm.txt")
otm["trkEmp"] = otm[NAICS_col_name].sum(axis=1)
# TODO: keep columns needed
col_to_keep = ["FID", "id", "trkEmp", "POINT_X", "POINT_Y"]
otm = otm[col_to_keep]

result = {}
for key, df in result_df_dict.items():
    result_df_dict[key]["TrkOrigName"] = df.apply(
        lambda x: x["Name"].split("-")[0].strip(), axis=1)
    result_df_dict[key]["TrkDestName"] = df.apply(
        lambda x: x["Name"].split("-")[1].strip(), axis=1)
    result_df_dict[key]["trkEmp"] = result_df_dict[key]["TrkDestName"].apply(
        lambda x: otm["trkEmp"][otm["FID"] == int(x)].values[0])
    df_time_for_each_orig = {}
    for name_of_orig in df["TrkOrigName"].unique():
        selected_orig_df = df[df["TrkOrigName"] == name_of_orig]
        df_time_for_each_orig[name_of_orig] = (selected_orig_df["Total_time"]*selected_orig_df['trkEmp']
                                               ).sum()/(selected_orig_df['trkEmp'].sum())
    result[key] = df_time_for_each_orig

with open("TrkRtTimeresult.json", "w") as fp:
    json.dump(result, fp, sort_keys=True, indent=4)

pd.DataFrame(result).to_csv("result.csv")
otm.to_csv("otm_withWeight.csv")
