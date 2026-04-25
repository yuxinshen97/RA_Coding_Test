
## python code for Task 2

#county-year panel
import pandas as pd
from pathlib import Path

county_2010 = pd.read_csv("raw_data/soi/county/10incyallagi.csv")
county_2011 = pd.read_csv("raw_data/soi/county/11incyallagi.csv")

print(county_2010.columns.tolist())
print(county_2011.columns.tolist())

print(county_2010.shape)
print(county_2011.shape)

county_2010["year"] = 2010
county_2011["year"] = 2011

county_panel_test = pd.concat([county_2010, county_2011], ignore_index=True)

print(county_panel_test.shape)

print(
    county_panel_test[
        ["year", "STATEFIPS", "STATE", "COUNTYFIPS", "COUNTYNAME", "agi_stub", "N1"]
    ].head(10)
)

print(county_panel_test["year"].value_counts().sort_index())

county_panel_test.columns = county_panel_test.columns.str.lower()

print(county_panel_test.columns[:10].tolist())


valid_state_fips = {
    "01","02","04","05","06","08","09","10","12","13",
    "15","16","17","18","19","20","21","22","23","24",
    "25","26","27","28","29","30","31","32","33","34",
    "35","36","37","38","39","40","41","42","44","45",
    "46","47","48","49","50","51","53","54","55","56"
}

def clean_county_soi(file, year):
    df = pd.read_csv(file)
    df.columns = df.columns.str.lower()

    df = df.rename(columns={
        "statefips": "state_fips",
        "countyfips": "county_fips",
        "countyname": "county_name"
    })

    df["year"] = year

    # clean FIPS
    df["state_fips"] = (
        pd.to_numeric(df["state_fips"], errors="coerce")
        .astype("Int64")
        .astype(str)
        .str.zfill(2)
    )

    df["county_fips"] = (
        pd.to_numeric(df["county_fips"], errors="coerce")
        .astype("Int64")
        .astype(str)
        .str.zfill(3)
    )

    # keep only 50 states
    df = df[df["state_fips"].isin(valid_state_fips)].copy()

    # remove state-level totals / non-county rows
    # usually county_fips == "000" means state total
    df = df[df["county_fips"] != "000"].copy()

    return df
  
  
years_2010_2022 = list(range(2010, 2023))

files_2010_2022 = [
    f"raw_data/soi/county/{str(year)[-2:]}incyallagi.csv"
    for year in years_2010_2022
]

county_all_new = pd.concat(
    [clean_county_soi(file, year) for file, year in zip(files_2010_2022, years_2010_2022)],
    ignore_index=True
)

print(county_all_new.shape)
print(county_all_new["year"].value_counts().sort_index())

import pandas as pd

def sum_or_na(series):
    return series.sum(skipna=True) if not series.isna().all() else pd.NA

county_fixed = (
    county_all_new
    .groupby(["year", "state_fips", "county_fips", "county_name"], as_index=False)
    .agg({
        "n1": sum_or_na,
        "n2": sum_or_na,
        "a00100": sum_or_na,
        "a00200": sum_or_na,
        "a00300": sum_or_na,
        "a00600": sum_or_na
    })
    .sort_values(["year", "state_fips", "county_fips"])
)

print(county_fixed.shape)

print(
    county_fixed.groupby("year")
    .size()
    .reset_index(name="n")
    .sort_values("year")
)

print(county_fixed.head(10))

##add state name
state_lookup = pd.DataFrame({
    "state_fips": [
        "01","02","04","05","06","08","09","10","12","13",
        "15","16","17","18","19","20","21","22","23","24",
        "25","26","27","28","29","30","31","32","33","34",
        "35","36","37","38","39","40","41","42","44","45",
        "46","47","48","49","50","51","53","54","55","56"
    ],
    "state_abbr": [
        "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
        "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
        "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
        "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
        "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
    ],
    "state_name": [
        "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia",
        "Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
        "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey",
        "New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
        "South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"
    ]
})

county_fixed = county_fixed.merge(
    state_lookup,
    on="state_fips",
    how="left"
)

county_fixed = county_fixed[
    [
        "year", "state_fips", "state_abbr", "state_name",
        "county_fips", "county_name",
        "n1", "n2", "a00100", "a00200", "a00300", "a00600"
    ]
]

pd.set_option("display.float_format", "{:.0f}".format)
print(county_fixed.head(10))

county_fixed.to_csv("output/soi_county_panel_2010_2022.csv", index=False)


#transfer data format for 2008 and 2009

def build_county_panel_for_year(folder, year):

    print("Working on:", folder)

    files = glob.glob(os.path.join(folder, "*.xls"))

    print("Number of files found:", len(files))

    dfs = []

    for f in files:
        try:
            df = pd.read_excel(f)

            df.columns = df.columns.str.lower()

            df = df.rename(columns={
                "statefips": "state_fips",
                "countyfips": "county_fips",
                "countyname": "county_name"
            })

            df["year"] = year

            df["state_fips"] = (
                pd.to_numeric(df["state_fips"], errors="coerce")
                .astype("Int64")
                .astype(str)
                .str.zfill(2)
            )

            df["county_fips"] = (
                pd.to_numeric(df["county_fips"], errors="coerce")
                .astype("Int64")
                .astype(str)
                .str.zfill(3)
            )

            dfs.append(df)

        except Exception as e:
            print("Error reading:", f)
            print(e)

    if len(dfs) == 0:
        raise ValueError("No files were successfully read.")

    return pd.concat(dfs, ignore_index=True)


import pandas as pd

test_2008 = pd.read_excel(
    "raw_data/soi/county/2008_states/2008 County income/county income 2008 AK.xls"
)

print(test_2008.columns.tolist())

##Function for 2008 and 2009
import pandas as pd
import glob
import os

valid_state_fips = {
    "01","02","04","05","06","08","09","10","12","13",
    "15","16","17","18","19","20","21","22","23","24",
    "25","26","27","28","29","30","31","32","33","34",
    "35","36","37","38","39","40","41","42","44","45",
    "46","47","48","49","50","51","53","54","55","56"
}

def read_one_old_county_file(file, year):
    df = pd.read_excel(file, header=None, engine="xlrd")

    df = df.iloc[7:, 0:9].copy()

    df.columns = [
        "state_fips",
        "county_fips",
        "county_name",
        "n1",
        "n2",
        "a00100",
        "a00200",
        "a00600",
        "a00300"
    ]

    df = df[df["state_fips"].notna()].copy()

    df["state_fips"] = df["state_fips"].astype(str).str.strip()
    df["county_fips"] = df["county_fips"].astype(str).str.strip()
    df["county_name"] = df["county_name"].astype(str).str.strip()

    df = df[df["state_fips"].str.fullmatch(r"\d+(\.0+)?")].copy()
    df = df[df["county_fips"].str.fullmatch(r"\d+(\.0+)?")].copy()

    df["state_fips"] = (
        df["state_fips"]
        .str.replace(r"\.0+$", "", regex=True)
        .str.zfill(2)
    )

    df["county_fips"] = (
        df["county_fips"]
        .str.replace(r"\.0+$", "", regex=True)
        .str.zfill(3)
    )

    df = df[df["county_fips"] != "000"].copy()
    df = df[df["state_fips"].isin(valid_state_fips)].copy()

    numeric_cols = ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["year"] = year

    return df[
        [
            "year", "state_fips", "county_fips", "county_name",
            "n1", "n2", "a00100", "a00200", "a00300", "a00600"
        ]
    ]


panel_2008 = build_county_panel_for_year(
    "raw_data/soi/county/2008_states/2008 County income",
    2008
)

panel_2009 = build_county_panel_for_year(
    "raw_data/soi/county/2009_states/2009 County Income",
    2009
)

print(panel_2008.shape)
print(panel_2009.shape)
print(panel_2008.head(10).to_string())
print(panel_2009.head(10).to_string())



county_fixed = pd.read_csv(
    "output/soi_county_panel_2010_2022.csv",
    dtype={"state_fips": str, "county_fips": str},
    encoding="latin1"
)


county_fixed["state_fips"] = (
    county_fixed["state_fips"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(2)
)

county_fixed["county_fips"] = (
    county_fixed["county_fips"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(3)
)

county_fixed["county_name"] = county_fixed["county_name"].astype(str).str.strip()

county_fixed = county_fixed[county_fixed["county_fips"] != "000"].copy()

# combined by county-year
county_fixed_clean = (
    county_fixed.groupby(
        ["year", "state_fips", "county_fips", "county_name"],
        as_index=False
    )[["n1", "n2", "a00100", "a00200", "a00300", "a00600"]]
    .sum()
)

print(county_fixed_clean.shape)
print(county_fixed_clean.groupby("year").size().reset_index(name="n"))
print(
    "duplicated county-year in county_fixed_clean:",
    county_fixed_clean.duplicated(subset=["year", "state_fips", "county_fips"]).sum()
)
print("county_fips == 000:", (county_fixed_clean["county_fips"] == "000").sum())
print(county_fixed_clean.head(10).to_string())

county_2008_2022 = pd.concat(
    [panel_2008, panel_2009, county_fixed_clean],
    ignore_index=True
).sort_values(["year", "state_fips", "county_fips"]).reset_index(drop=True)

abbr_map = dict(zip(state_lookup_fresh["state_fips"], state_lookup_fresh["state_abbr"]))
name_map = dict(zip(state_lookup_fresh["state_fips"], state_lookup_fresh["state_name"]))

county_2008_2022["state_abbr"] = county_2008_2022["state_fips"].map(abbr_map)
county_2008_2022["state_name"] = county_2008_2022["state_fips"].map(name_map)

df_2008_2022_clean = county_2008_2022[
    [
        "year", "state_fips", "state_abbr", "state_name",
        "county_fips", "county_name",
        "n1", "n2", "a00100", "a00200", "a00300", "a00600"
    ]
].copy()

print(df_2008_2022_clean.shape)
print("missing state_abbr:", df_2008_2022_clean["state_abbr"].isna().sum())
print("missing state_name:", df_2008_2022_clean["state_name"].isna().sum())
print(df_2008_2022_clean.groupby("year").size().reset_index(name="n"))

df_2008_2022_clean = df_2008_2022_clean[
    df_2008_2022_clean["state_fips"] != "11"
].copy()

#clean for 2007
import pandas as pd
import numpy as np
import glob
import os
import re

state_lookup = pd.DataFrame({
    "state_fips": [
        "01","02","04","05","06","08","09","10","12","13",
        "15","16","17","18","19","20","21","22","23","24",
        "25","26","27","28","29","30","31","32","33","34",
        "35","36","37","38","39","40","41","42","44","45",
        "46","47","48","49","50","51","53","54","55","56"
    ],
    "state_abbr": [
        "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
        "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
        "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
        "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
        "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
    ],
    "state_name": [
        "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia",
        "Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
        "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey",
        "New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
        "South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"
    ]
})

VALID_STATE_FIPS = set(state_lookup["state_fips"].tolist())

state_lookup_2007 = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "NewHampshire": "NH", "NewJersey": "NJ", "NewMexico": "NM", "NewYork": "NY",
    "NorthCarolina": "NC", "NorthDakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "RhodeIsland": "RI", "SouthCarolina": "SC",
    "SouthDakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "WestVirginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY"
}

def parse_number_col(series):
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False).str.strip(),
        errors="coerce"
    )

# 2007
def clean_county_soi_2007(file, year, state_abbr):
    df = pd.read_excel(
        file,
        skiprows=7,
        usecols="B:J",
        header=None,
        names=[
            "state_fips",
            "county_fips",
            "county_name",
            "n1",
            "n2",
            "a00100",
            "a00200",
            "a00600",
            "a00300"
        ],
        dtype=str,
        engine="xlrd"
    )

    df = df[
        df["state_fips"].notna() &
        (df["state_fips"].astype(str).str.strip() != "CODES")
    ].copy()

    df["year"] = year
    df["state_abbr"] = state_abbr
    df["state_fips"] = df["state_fips"].astype(str).str.strip().str.zfill(2)
    df["county_fips"] = df["county_fips"].astype(str).str.strip().str.zfill(3)
    df["county_name"] = df["county_name"].astype(str).str.strip()

    for col in ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]:
        df[col] = parse_number_col(df[col])

    df = df[
        df["state_fips"].isin(VALID_STATE_FIPS) &
        (df["county_fips"] != "000")
    ].copy()

    df = (
        df.groupby(
            ["year", "state_fips", "state_abbr", "county_fips", "county_name"],
            as_index=False
        )[["n1", "n2", "a00100", "a00200", "a00300", "a00600"]]
        .sum()
    )

    return df

files_2007 = glob.glob("raw_data/soi/county/2007_states/2007 County income/*.xls")

county_2007_all = []
for f in files_2007:
    fname = os.path.basename(f)
    state_name = re.sub(r"07ci\.xls$", "", fname)
    state_abbr = state_lookup_2007.get(state_name)

    if state_abbr is None:
        print("Unmatched 2007 file:", fname)
        continue

    county_2007_all.append(clean_county_soi_2007(f, 2007, state_abbr))

county_2007_all = pd.concat(county_2007_all, ignore_index=True)

county_2007_all = county_2007_all.merge(
    state_lookup[["state_fips", "state_abbr", "state_name"]],
    on=["state_fips", "state_abbr"],
    how="left"
)

county_2007_all = county_2007_all[
    [
        "year", "state_fips", "state_abbr", "state_name",
        "county_fips", "county_name",
        "n1", "n2", "a00100", "a00200", "a00300", "a00600"
    ]
].sort_values(["year", "state_fips", "county_fips"]).reset_index(drop=True)

print("2007:", county_2007_all.shape)
print(county_2007_all.groupby("year").size())
print("2007 dup county-year:",
      county_2007_all.duplicated(subset=["year", "state_fips", "county_fips"]).sum())

#clean data for 1990-2006
def clean_soi_1990_2006_file(file_path, year_value):
    file_name = os.path.basename(file_path)
    file_name_lower = file_name.lower()

    skip_value = 6 if file_name_lower == "kentucky01ci.xls" else 7

    df = pd.read_excel(
        file_path,
        skiprows=skip_value,
        header=None,
        engine="xlrd"
    )

    df = df.iloc[:, 1:8].copy()
    df.columns = [
        "state_fips",
        "county_code",
        "county_name",
        "n_returns",
        "n_exemptions",
        "agi",
        "wages"
    ]

    df = df[df["state_fips"].astype(str).str.upper() != "CODES"].copy()

    df["state_fips"] = pd.to_numeric(df["state_fips"], errors="coerce")
    df["county_code"] = pd.to_numeric(df["county_code"], errors="coerce")

    df = df[df["state_fips"].notna() & df["county_code"].notna()].copy()

    df["state_fips"] = df["state_fips"].astype(int).astype(str).str.zfill(2)
    df["county_code"] = df["county_code"].astype(int).astype(str).str.zfill(3)
    df["county_fips"] = df["state_fips"] + df["county_code"]

    df["county_name"] = df["county_name"].astype(str).str.strip()

    for col in ["n_returns", "n_exemptions", "agi", "wages"]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "", regex=False).str.strip(),
            errors="coerce"
        )

    df["year"] = year_value
    df["source_file"] = file_name

    df = df[
        df["state_fips"].isin(VALID_STATE_FIPS) &
        (df["county_code"] != "000")
    ].copy()

    return df[
        [
            "state_fips", "county_code", "county_fips", "county_name",
            "year", "n_returns", "n_exemptions", "agi", "wages", "source_file"
        ]
    ]

def clean_soi_old_year(year_value, base_dir):
    year_dirs = [
        os.path.join(base_dir, d)
        for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d))
    ]

    year_folder = [
        d for d in year_dirs
        if str(year_value) in os.path.basename(d)
    ]

    if len(year_folder) == 0:
        print(f"Year {year_value} | folder not found")
        return {"data": pd.DataFrame(), "failed": pd.DataFrame()}

    files = glob.glob(os.path.join(year_folder[0], "**", "*.xls"), recursive=True)

    print(f"Year {year_value} | files: {len(files)}")

    data_list = []
    failed_list = []

    for f in files:
        try:
            data_list.append(clean_soi_1990_2006_file(f, year_value))
        except Exception as e:
            failed_list.append({
                "year": year_value,
                "file": os.path.basename(f),
                "error": str(e)
            })

    return {
        "data": pd.concat(data_list, ignore_index=True) if data_list else pd.DataFrame(),
        "failed": pd.DataFrame(failed_list)
    }

base_dir = "raw_data/soi/county"
years_old = list(range(1990, 2007))
all_results = [clean_soi_old_year(y, base_dir) for y in years_old]

soi_1990_2006 = pd.concat(
    [x["data"] for x in all_results if not x["data"].empty],
    ignore_index=True
) if any(not x["data"].empty for x in all_results) else pd.DataFrame()

failed_files_1990_2006 = pd.concat(
    [x["failed"] for x in all_results if not x["failed"].empty],
    ignore_index=True
) if any(not x["failed"].empty for x in all_results) else pd.DataFrame()

print("1990-2006 raw:", soi_1990_2006.shape)
print(failed_files_1990_2006.head())

soi_1990_2006_std = soi_1990_2006.copy()
soi_1990_2006_std = soi_1990_2006_std.rename(columns={
    "county_code": "county_fips_3",
    "n_returns": "n1",
    "n_exemptions": "n2",
    "agi": "a00100",
    "wages": "a00200"
})

soi_1990_2006_std["a00300"] = np.nan
soi_1990_2006_std["a00600"] = np.nan

soi_1990_2006_std = soi_1990_2006_std.merge(
    state_lookup,
    on="state_fips",
    how="left"
)

soi_1990_2006_std["county_fips"] = soi_1990_2006_std["county_fips_3"]

soi_1990_2006_std = soi_1990_2006_std[
    [
        "year", "state_fips", "state_abbr", "state_name",
        "county_fips", "county_name",
        "n1", "n2", "a00100", "a00200", "a00300", "a00600"
    ]
].copy()

print("1990-2006 std:", soi_1990_2006_std.shape)

#combined
county_panel_1990_2022 = county_panel_1990_2022.drop_duplicates(
    subset=["year", "state_fips", "county_fips"],
    keep="first"
).copy()

county_panel_1990_2022 = county_panel_1990_2022.sort_values(
    ["year", "state_fips", "county_fips"]
).reset_index(drop=True)

print(county_panel_1990_2022.shape)
print(county_panel_1990_2022.groupby("year").size().reset_index(name="n").to_string())

print(
    "duplicated county-year rows:",
    county_panel_1990_2022.duplicated(
        subset=["year", "state_fips", "county_fips"]
    ).sum()
)

print("missing state_name:", county_panel_1990_2022["state_name"].isna().sum())
print("county_fips == 000:", (county_panel_1990_2022["county_fips"] == "000").sum())

county_panel_1990_2022["county_id"] = (
    county_panel_1990_2022["state_fips"] + county_panel_1990_2022["county_fips"]
)

print("unique county_id:", county_panel_1990_2022["county_id"].nunique())

county_panel_1990_2022.to_csv(
    "output/soi_county_panel_1990_2022_FINAL.csv",
    index=False
)

#add 1989
import glob, os
import pandas as pd

county_1989 = pd.read_csv(
    "raw_data/soi/county/1989countyincome/89incyallnoagi.csv"
)

print(county_1989.shape)
print(county_1989.columns.tolist())
print(county_1989.head())


county_1989_clean = county_1989.rename(columns={
    "STATE": "state",
    "STATEFIPS": "state_fips",
    "COUNTYFIPS": "county_fips",
    "COUNTYNAME": "county_name",
    "N1": "n1",
    "N2": "n2",
    "AGI": "a00100",
    "WAGES_SAL": "a00200",
    "DIVIDENDS": "a00600",
    "INTEREST": "a00300"
}).copy()

county_1989_clean["year"] = 1989

county_1989_clean["state_fips"] = (
    county_1989_clean["state_fips"].astype(str)
    .str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(2)
)

county_1989_clean["county_fips"] = (
    county_1989_clean["county_fips"].astype(str)
    .str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(3)
)

county_1989_clean["county_name"] = county_1989_clean["county_name"].astype(str).str.strip()

county_1989_clean = county_1989_clean[
    county_1989_clean["state_fips"].isin(VALID_STATE_FIPS) &
    (county_1989_clean["county_fips"] != "000")
].copy()

county_1989_clean = county_1989_clean.merge(
    state_lookup[["state_fips", "state_abbr", "state_name"]],
    on="state_fips",
    how="left"
)

county_1989_common = county_1989_clean[
    [
        "year", "state_fips", "state_abbr", "state_name",
        "county_fips", "county_name",
        "n1", "n2", "a00100", "a00200", "a00300", "a00600"
    ]
].copy()

print(county_1989_common.shape)
print("1989 dup:", county_1989_common.duplicated(subset=["year", "state_fips", "county_fips"]).sum())
print("1989 missing state_name:", county_1989_common["state_name"].isna().sum())

county_panel_1989_2022 = pd.concat(
    [county_1989_common, county_panel_1990_2022],
    ignore_index=True
).sort_values(["year", "state_fips", "county_fips"]).reset_index(drop=True)

county_panel_1989_2022["county_id"] = (
    county_panel_1989_2022["state_fips"] + county_panel_1989_2022["county_fips"]
)

print(county_panel_1989_2022.groupby("year").size().reset_index(name="n").to_string())
print("final shape:", county_panel_1989_2022.shape)
print("final dup:", county_panel_1989_2022.duplicated(subset=["year", "state_fips", "county_fips"]).sum())
print("final missing state_name:", county_panel_1989_2022["state_name"].isna().sum())
print("final county_fips == 000:", (county_panel_1989_2022["county_fips"] == "000").sum())

county_panel_1989_2022.to_csv(
    "output/soi_county_panel_1989_2022_Py.csv",
    index=False
)

#check both
df_py_test.to_csv(
    "output/soi_county_panel_1989_2022_Python.csv",
    index=False
)

df_r_test.to_csv(
    "output/soi_county_panel_1989_2022_R.csv",
    index=False
)


    
## Zip code panel data
## 2006-2022 ZIP SOI cleaning

import pandas as pd
from pathlib import Path

RAW_DIR = Path("raw_data/soi/zip")
OUT_DIR = Path("output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# State map

state_map = pd.DataFrame({
    "state": [
        "AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME",
        "MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI",
        "SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
    ],
    "state_fips": [
        "01","02","04","05","06","08","09","10","11","12","13","15","16","17","18","19","20","21","22","23",
        "24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","44",
        "45","46","47","48","49","50","51","53","54","55","56"
    ]
})

# Helper functions

def standardize_columns(df):
    df = df.copy()
    df.columns = [c.lower().strip() for c in df.columns]
    return df


def safe_numeric(x):
    return pd.to_numeric(x, errors="coerce")


def pad_code(x, width):
    return (
        x.astype("string")
        .str.replace(r"\.0$", "", regex=True)
        .str.strip()
        .str.zfill(width)
    )

# Unified cleaner

def clean_zip_soi(file_path, year):
    df = pd.read_csv(file_path, low_memory=False)
    df = standardize_columns(df)

    rename_map = {
        "zip_code": "zipcode",
        "agi_class": "agi_stub",
        "agi_classs": "agi_stub",
        "state_fips": "statefips",
    }

    df = df.rename(
        columns={k: v for k, v in rename_map.items() if k in df.columns and v not in df.columns}
    )

    # If statefips missing, recover from state abbreviation
    if "statefips" not in df.columns:
        if "state" not in df.columns:
            raise ValueError(
                f"{year}: neither statefips nor state exists in {file_path.name}"
            )

        df["state"] = df["state"].astype("string").str.upper().str.strip()
        df = df.merge(state_map, on="state", how="left")
        df = df.rename(columns={"state_fips": "statefips"})

    required = [
        "statefips", "state", "zipcode", "agi_stub",
        "n1", "n2", "a00100", "a00200", "a00600", "a00300"
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"{year}: missing columns {missing} in {file_path.name}. "
            f"Existing columns: {df.columns.tolist()}"
        )

    core = pd.DataFrame({
        "year": year,
        "state_fips": pad_code(df["statefips"], 2),
        "state": df["state"].astype("string").str.upper().str.strip(),
        "zipcode": pad_code(df["zipcode"], 5),
        "agi_stub": safe_numeric(df["agi_stub"]),
        "n1": safe_numeric(df["n1"]),
        "n2": safe_numeric(df["n2"]),
        "a00100": safe_numeric(df["a00100"]),
        "a00200": safe_numeric(df["a00200"]),
        "a00600": safe_numeric(df["a00600"]),
        "a00300": safe_numeric(df["a00300"]),
    })

    return core

# Collapse AGI bins to ZIP-year panel

def make_zip_panel(df_core):
    value_cols = ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]

    panel = (
        df_core
        .groupby(["year", "state_fips", "state", "zipcode"], as_index=False)[value_cols]
        .sum(min_count=1)
    )

    for c in value_cols:
        panel[c] = panel[c].round()

    return panel

# Check all raw files

years = list(range(2006, 2023))

for y in years:
    yy = str(y)[2:4]
    file_path = RAW_DIR / f"{yy}zpallagi.csv"

    print("\n", y, file_path.name, "exists =", file_path.exists())

    if file_path.exists():
        tmp = pd.read_csv(file_path, nrows=2, low_memory=False)
        tmp = standardize_columns(tmp)
        print(tmp.columns.tolist())
    else:
        raise FileNotFoundError(f"Missing file: {file_path}")

# Build full 2006-2022 panel

core_list = []
panel_list = []

for y in years:
    yy = str(y)[2:4]
    file_path = RAW_DIR / f"{yy}zpallagi.csv"

    print(f"Processing {y}...")

    core = clean_zip_soi(file_path, y)
    panel = make_zip_panel(core)

    print("   core shape:", core.shape)
    print("   panel shape:", panel.shape)

    core_list.append(core)
    panel_list.append(panel)

soi_zip_core_2006_2022 = (
    pd.concat(core_list, ignore_index=True)
    .sort_values(["year", "state_fips", "zipcode", "agi_stub"])
)

soi_zip_panel_2006_2022 = (
    pd.concat(panel_list, ignore_index=True)
    .sort_values(["year", "state_fips", "zipcode"])
)

# Diagnostics

summary = (
    soi_zip_panel_2006_2022
    .groupby("year")
    .agg(
        n_rows=("zipcode", "size"),
        n_zipcodes=("zipcode", "nunique"),
        n_states=("state_fips", "nunique"),
        total_n1=("n1", "sum"),
        total_n2=("n2", "sum"),
        total_agi=("a00100", "sum"),
        total_wages=("a00200", "sum"),
        total_dividends=("a00600", "sum"),
        total_interest=("a00300", "sum"),
    )
    .reset_index()
)

print("\nYear-level summary:")
print(summary)

dups = (
    soi_zip_panel_2006_2022
    .groupby(["year", "state_fips", "zipcode"])
    .size()
    .reset_index(name="n")
    .query("n > 1")
)

print("\nDuplicated ZIP-year rows:", len(dups))
print(dups.head())

# Save

soi_zip_core_2006_2022.to_csv(
    OUT_DIR / "soi_zip_core_2006_2022.csv",
    index=False
)

soi_zip_panel_2006_2022.to_csv(
    OUT_DIR / "soi_zip_panel_2006_2022.csv",
    index=False
)

summary.to_csv(
    OUT_DIR / "soi_zip_summary_2006_2022.csv",
    index=False
)

print("\nSaved:")
print(OUT_DIR / "soi_zip_core_2006_2022.csv")
print(OUT_DIR / "soi_zip_panel_2006_2022.csv")
print(OUT_DIR / "soi_zip_summary_2006_2022.csv")

print(summary)


# Fix money units for 2007-2008
# 2007-2008 appear to be in dollars; convert to thousand dollars

money_cols = ["a00100", "a00200", "a00600", "a00300"]

for col in money_cols:
    soi_zip_core_2006_2022.loc[
        soi_zip_core_2006_2022["year"].isin([2007, 2008]), col
    ] = soi_zip_core_2006_2022.loc[
        soi_zip_core_2006_2022["year"].isin([2007, 2008]), col
    ] / 1000

    soi_zip_panel_2006_2022.loc[
        soi_zip_panel_2006_2022["year"].isin([2007, 2008]), col
    ] = soi_zip_panel_2006_2022.loc[
        soi_zip_panel_2006_2022["year"].isin([2007, 2008]), col
    ] / 1000


# Rebuild summary after correction

summary_fixed = (
    soi_zip_panel_2006_2022
    .groupby("year")
    .agg(
        n_rows=("zipcode", "size"),
        n_zipcodes=("zipcode", "nunique"),
        n_states=("state_fips", "nunique"),
        total_n1=("n1", "sum"),
        total_n2=("n2", "sum"),
        total_agi=("a00100", "sum"),
        total_wages=("a00200", "sum"),
        total_dividends=("a00600", "sum"),
        total_interest=("a00300", "sum"),
    )
    .reset_index()
)

print(summary_fixed)


# Save corrected files

soi_zip_core_2006_2022.to_csv(
    OUT_DIR / "soi_zip_core_2006_2022_corrected.csv",
    index=False
)

soi_zip_panel_2006_2022.to_csv(
    OUT_DIR / "soi_zip_panel_2006_2022_corrected.csv",
    index=False
)

summary_fixed.to_csv(
    OUT_DIR / "soi_zip_summary_2006_2022_corrected.csv",
    index=False
)

print("Saved corrected files:")
print(OUT_DIR / "soi_zip_core_2006_2022_corrected.csv")
print(OUT_DIR / "soi_zip_panel_2006_2022_corrected.csv")
print(OUT_DIR / "soi_zip_summary_2006_2022_corrected.csv")

# Keep 50 states only and drop aggregate ZIP rows

# DC = 11, remove it
keep_state_fips = [
    "01","02","04","05","06","08","09","10","12","13",
    "15","16","17","18","19","20","21","22","23","24",
    "25","26","27","28","29","30","31","32","33","34",
    "35","36","37","38","39","40","41","42","44","45",
    "46","47","48","49","50","51","53","54","55","56"
]

# core: keep 50 states, drop aggregate ZIP rows
soi_zip_core_2006_2022_50states = (
    soi_zip_core_2006_2022
    .loc[
        soi_zip_core_2006_2022["state_fips"].isin(keep_state_fips)
        & (soi_zip_core_2006_2022["zipcode"] != "00000")
    ]
    .copy()
)

# panel: keep 50 states, drop aggregate ZIP rows
soi_zip_panel_2006_2022_50states = (
    soi_zip_panel_2006_2022
    .loc[
        soi_zip_panel_2006_2022["state_fips"].isin(keep_state_fips)
        & (soi_zip_panel_2006_2022["zipcode"] != "00000")
    ]
    .copy()
)

# Check again

summary_50states = (
    soi_zip_panel_2006_2022_50states
    .groupby("year")
    .agg(
        n_rows=("zipcode", "size"),
        n_zipcodes=("zipcode", "nunique"),
        n_states=("state_fips", "nunique"),
        total_n1=("n1", "sum"),
        total_n2=("n2", "sum"),
        total_agi=("a00100", "sum"),
        total_wages=("a00200", "sum"),
        total_dividends=("a00600", "sum"),
        total_interest=("a00300", "sum"),
    )
    .reset_index()
)

print(summary_50states)

bad_zip_50states = soi_zip_panel_2006_2022_50states[
    (soi_zip_panel_2006_2022_50states["zipcode"].isna()) |
    (soi_zip_panel_2006_2022_50states["zipcode"].str.len() != 5) |
    (soi_zip_panel_2006_2022_50states["zipcode"] == "00000")
]

print("bad zip rows after cleaning:", len(bad_zip_50states))

print(
    soi_zip_panel_2006_2022_50states
    .groupby("year")["state_fips"]
    .nunique()
    .reset_index(name="n_states")
)

# Save 50-state files

soi_zip_core_2006_2022_50states.to_csv(
    OUT_DIR / "soi_zip_core_2006_2022_50states.csv",
    index=False
)

soi_zip_panel_2006_2022_50states.to_csv(
    OUT_DIR / "soi_zip_panel_2006_2022_50states.csv",
    index=False
)

summary_50states.to_csv(
    OUT_DIR / "soi_zip_summary_2006_2022_50states.csv",
    index=False
)

print("Saved 50-state files.")

# Add 2004-2005 from R revised file into Python 2006-2022 panel
import pandas as pd
from pathlib import Path

OUT_DIR = Path("output")

# Python cleaned 2006-2022 file
py_file = OUT_DIR / "soi_zip_panel_2006_2022_50states.csv"

# R revised 2004-2022 file
r_file = OUT_DIR / "soi_zip_panel_2004_2022_revised.csv"

py_0622 = pd.read_csv(
    py_file,
    dtype={"state_fips": "string", "zipcode": "string"}
)

r_all = pd.read_csv(
    r_file,
    dtype={"state_fips": "string", "zipcode": "string"}
)

# standardize column names
py_0622.columns = [c.lower().strip() for c in py_0622.columns]
r_all.columns = [c.lower().strip() for c in r_all.columns]

# standardize keys
for df in [py_0622, r_all]:
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["state_fips"] = df["state_fips"].astype("string").str.replace(r"\.0$", "", regex=True).str.zfill(2)
    df["zipcode"] = df["zipcode"].astype("string").str.replace(r"\.0$", "", regex=True).str.zfill(5)

    if "state" in df.columns:
        df["state"] = df["state"].astype("string").str.upper().str.strip()

# keep 50 states only
keep_state_fips = [
    "01","02","04","05","06","08","09","10","12","13",
    "15","16","17","18","19","20","21","22","23","24",
    "25","26","27","28","29","30","31","32","33","34",
    "35","36","37","38","39","40","41","42","44","45",
    "46","47","48","49","50","51","53","54","55","56"
]

# extract 2004-2005 from R revised
r_0405 = (
    r_all
    .loc[
        r_all["year"].isin([2004, 2005])
        & r_all["state_fips"].isin(keep_state_fips)
        & (r_all["zipcode"] != "00000")
    ]
    .copy()
)

# keep same columns as Python 2006-2022
common_cols = [c for c in py_0622.columns if c in r_0405.columns]

r_0405 = r_0405[common_cols].copy()
py_0622 = py_0622[common_cols].copy()

# make numeric columns numeric
num_cols = ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]

for df in [r_0405, py_0622]:
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

# combine
soi_zip_panel_2004_2022_final = (
    pd.concat([r_0405, py_0622], ignore_index=True)
    .sort_values(["year", "state_fips", "zipcode"])
    .reset_index(drop=True)
)

# Diagnostics

summary_final = (
    soi_zip_panel_2004_2022_final
    .groupby("year")
    .agg(
        n_rows=("zipcode", "size"),
        n_zipcodes=("zipcode", "nunique"),
        n_states=("state_fips", "nunique"),
        total_n1=("n1", "sum"),
        total_n2=("n2", "sum"),
        total_agi=("a00100", "sum"),
        total_wages=("a00200", "sum"),
        total_dividends=("a00600", "sum"),
        total_interest=("a00300", "sum"),
    )
    .reset_index()
)

print(summary_final)

dups_final = (
    soi_zip_panel_2004_2022_final
    .groupby(["year", "state_fips", "zipcode"])
    .size()
    .reset_index(name="n")
    .query("n > 1")
)

print("duplicated ZIP-year rows:", len(dups_final))
print(dups_final.head())

bad_zip_final = soi_zip_panel_2004_2022_final[
    (soi_zip_panel_2004_2022_final["zipcode"].isna()) |
    (soi_zip_panel_2004_2022_final["zipcode"].str.len() != 5) |
    (soi_zip_panel_2004_2022_final["zipcode"] == "00000")
]

print("bad ZIP rows:", len(bad_zip_final))

# Save

soi_zip_panel_2004_2022_final.to_csv(
    OUT_DIR / "soi_zip_panel_2004_2022_final.csv",
    index=False
)

summary_final.to_csv(
    OUT_DIR / "soi_zip_summary_2004_2022_final.csv",
    index=False
)

print("Saved final file:")
print(OUT_DIR / "soi_zip_panel_2004_2022_final.csv")

# Compare final Python file with R revised file

OUT_DIR = Path("output")

py_final_file = OUT_DIR / "soi_zip_panel_2004_2022_final.csv"
r_file = OUT_DIR / "soi_zip_panel_2004_2022_revised.csv"

py = pd.read_csv(py_final_file, dtype={"state_fips": "string", "zipcode": "string"})
r = pd.read_csv(r_file, dtype={"state_fips": "string", "zipcode": "string"})

py.columns = [c.lower().strip() for c in py.columns]
r.columns = [c.lower().strip() for c in r.columns]

keep_state_fips = [
    "01","02","04","05","06","08","09","10","12","13",
    "15","16","17","18","19","20","21","22","23","24",
    "25","26","27","28","29","30","31","32","33","34",
    "35","36","37","38","39","40","41","42","44","45",
    "46","47","48","49","50","51","53","54","55","56"
]

for df in [py, r]:
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["state_fips"] = df["state_fips"].astype("string").str.replace(r"\.0$", "", regex=True).str.zfill(2)
    df["zipcode"] = df["zipcode"].astype("string").str.replace(r"\.0$", "", regex=True).str.zfill(5)

    if "state" in df.columns:
        df["state"] = df["state"].astype("string").str.upper().str.strip()

# make R same sample: 2004-2022, 50 states, no state aggregate ZIP
r_clean = (
    r.loc[
        r["year"].between(2004, 2022)
        & r["state_fips"].isin(keep_state_fips)
        & (r["zipcode"] != "00000")
    ]
    .copy()
)

py_clean = (
    py.loc[
        py["year"].between(2004, 2022)
        & py["state_fips"].isin(keep_state_fips)
        & (py["zipcode"] != "00000")
    ]
    .copy()
)

print("Python final shape:", py_clean.shape)
print("R revised cleaned shape:", r_clean.shape)

key_cols = ["year", "state_fips", "zipcode"]

only_py = py_clean[key_cols].merge(
    r_clean[key_cols],
    on=key_cols,
    how="left",
    indicator=True
).query("_merge == 'left_only'")

only_r = r_clean[key_cols].merge(
    py_clean[key_cols],
    on=key_cols,
    how="left",
    indicator=True
).query("_merge == 'left_only'")

print("only_py:", only_py.shape)
print("only_r:", only_r.shape)

value_cols = ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]
key_cols = ["year", "state_fips", "zipcode"]

for df in [py_clean, r_clean]:
    for c in value_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

merged_check = py_clean[key_cols + value_cols].merge(
    r_clean[key_cols + value_cols],
    on=key_cols,
    how="inner",
    suffixes=("_py", "_r")
)

for c in value_cols:
    merged_check[f"diff_{c}"] = merged_check[f"{c}_py"] - merged_check[f"{c}_r"]

diff_cols = [f"diff_{c}" for c in value_cols]

print(merged_check[diff_cols].abs().sum())
print(merged_check[diff_cols].agg(["min", "max"]))

# Add state_abbr and state_name to Python final file

state_name_map = pd.DataFrame({
    "state_fips": [
        "01","02","04","05","06","08","09","10","12","13",
        "15","16","17","18","19","20","21","22","23","24",
        "25","26","27","28","29","30","31","32","33","34",
        "35","36","37","38","39","40","41","42","44","45",
        "46","47","48","49","50","51","53","54","55","56"
    ],
    "state_abbr": [
        "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
        "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
        "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
        "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
        "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
    ],
    "state_name": [
        "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia",
        "Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
        "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey",
        "New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
        "South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"
    ]
})

soi_zip_panel_2004_2022_final_with_state = (
    soi_zip_panel_2004_2022_final
    .drop(columns=["state_abbr", "state_name"], errors="ignore")
    .merge(state_name_map, on="state_fips", how="left")
)

# reorder columns to match R style
cols_order = [
    "year", "state_fips", "state_abbr", "state_name", "zipcode",
    "n1", "n2", "a00100", "a00200", "a00600", "a00300"
]

soi_zip_panel_2004_2022_final_with_state = soi_zip_panel_2004_2022_final_with_state[cols_order]

print(soi_zip_panel_2004_2022_final_with_state.head())
print(soi_zip_panel_2004_2022_final_with_state.shape)

# save
soi_zip_panel_2004_2022_final_with_state.to_csv(
    OUT_DIR / "soi_zip_panel_2004_2022_final_with_state.csv",
    index=False
)

print("Saved:")
print(OUT_DIR / "soi_zip_panel_2004_2022_final_with_state.csv")

# Check which years create money differences
year_diff = (
    merged_check
    .groupby("year")[diff_cols]
    .sum()
    .reset_index()
)

print(year_diff)

# Fix R revised 2007-2008 money units

r_clean_fixed = r_clean.copy()

money_cols = ["a00100", "a00200", "a00600", "a00300"]
value_cols = ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]
key_cols = ["year", "state_fips", "zipcode"]

r_clean_fixed["year"] = pd.to_numeric(r_clean_fixed["year"], errors="coerce").astype("Int64")
py_clean["year"] = pd.to_numeric(py_clean["year"], errors="coerce").astype("Int64")

# convert value columns
for c in value_cols:
    r_clean_fixed[c] = pd.to_numeric(r_clean_fixed[c], errors="coerce")
    py_clean[c] = pd.to_numeric(py_clean[c], errors="coerce")

# force money columns to float first
for c in money_cols:
    r_clean_fixed[c] = r_clean_fixed[c].astype(float)
    py_clean[c] = py_clean[c].astype(float)

mask = r_clean_fixed["year"].isin([2007, 2008])
print("Rows to fix:", mask.sum())

r_clean_fixed.loc[mask, money_cols] = r_clean_fixed.loc[mask, money_cols] / 1000.0

print("R fixed totals:")
print(
    r_clean_fixed
    .loc[r_clean_fixed["year"].isin([2007, 2008])]
    .groupby("year")[money_cols]
    .sum()
)

merged_check_fixed = py_clean[key_cols + value_cols].merge(
    r_clean_fixed[key_cols + value_cols],
    on=key_cols,
    how="inner",
    suffixes=("_py", "_r")
)

for c in value_cols:
    merged_check_fixed[f"diff_{c}"] = (
        merged_check_fixed[f"{c}_py"] - merged_check_fixed[f"{c}_r"]
    )

diff_cols_fixed = [f"diff_{c}" for c in value_cols]

print(merged_check_fixed[diff_cols_fixed].abs().sum())
print(merged_check_fixed[diff_cols_fixed].agg(["min", "max"]))

# ==================================================
# Add state_abbr/state_name to Python final, then save both
# ==================================================

py_final_save = py_clean.copy()
r_final_save = r_clean_fixed.copy()

# state crosswalk from R version
state_crosswalk = (
    r_final_save[["state_fips", "state_abbr", "state_name"]]
    .drop_duplicates()
    .copy()
)

py_final_save = (
    py_final_save
    .drop(columns=["state_abbr", "state_name"], errors="ignore")
    .merge(state_crosswalk, on="state_fips", how="left")
)

# Match R column order
py_final_save = py_final_save[r_final_save.columns.tolist()]

# Save
py_final_save.to_csv(
    OUT_DIR / "soi_zip_panel_2004_2022_python.csv",
    index=False
)

r_final_save.to_csv(
    OUT_DIR / "soi_zip_panel_2004_2022_R.csv",
    index=False
)

print(py_final_save.shape)
print(r_final_save.shape)

print("Saved:")
print(OUT_DIR / "soi_zip_panel_2004_2022_python.csv")
print(OUT_DIR / "soi_zip_panel_2004_2022_R.csv")

import pandas as pd
from pathlib import Path

OUT_DIR = Path("output")

df = pd.read_csv(
    OUT_DIR / "soi_zip_panel_2004_2022_python_final.csv",
    dtype={
        "state_fips": "string",
        "zipcode": "string",
        "state_abbr": "string",
        "state_name": "string"
    }
)

num_cols = ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]

for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

desc_stats = df[num_cols].describe().T

desc_stats.columns = [
    "count", "mean", "std", "min", "25%", "50%", "75%", "max"
]

desc_stats.to_csv(
    OUT_DIR / "soi_zip_descriptive_stats.csv"
)

print(desc_stats)
print("Saved:", OUT_DIR / "soi_zip_descriptive_stats.csv")

# compare with BEA panel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT_DIR = Path("output")

soi_file = OUT_DIR / "soi_county_panel_1989_2022_Python.csv"
bea_file = OUT_DIR / "bea_county_panel_revised.csv"

soi = pd.read_csv(soi_file, dtype=str, encoding="latin1", low_memory=False)
bea = pd.read_csv(bea_file, dtype=str, encoding="latin1", low_memory=False)

soi.columns = [c.lower().strip() for c in soi.columns]
bea.columns = [c.lower().strip() for c in bea.columns]

print("SOI shape:", soi.shape)
print("BEA shape:", bea.shape)
print("SOI columns:", soi.columns.tolist())
print("BEA columns:", bea.columns.tolist())

for df in [soi, bea]:
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["state_fips"] = df["state_fips"].astype("string").str.zfill(2)
    df["county_fips"] = df["county_fips"].astype("string").str.zfill(3)

soi_keep = soi[["year", "state_fips", "county_fips", "n2", "a00100"]].copy()
bea_keep = bea[["year", "state_fips", "county_fips", "population", "income"]].copy()

for c in ["n2", "a00100"]:
    soi_keep[c] = pd.to_numeric(soi_keep[c], errors="coerce")

for c in ["population", "income"]:
    bea_keep[c] = pd.to_numeric(bea_keep[c], errors="coerce")

merged = soi_keep.merge(
    bea_keep,
    on=["year", "state_fips", "county_fips"],
    how="inner"
)

print("Merged shape:", merged.shape)

corr_n2_pop = merged[["n2", "population"]].corr().iloc[0, 1]
corr_agi_income = merged[["a00100", "income"]].corr().iloc[0, 1]

merged["n2_population_ratio"] = merged["n2"] / merged["population"]
merged["agi_income_ratio"] = merged["a00100"] / merged["income"]

print("corr n2 vs population:", corr_n2_pop)
print("corr AGI vs income:", corr_agi_income)
print("mean n2/population:", merged["n2_population_ratio"].mean())
print("mean AGI/income:", merged["agi_income_ratio"].mean())
