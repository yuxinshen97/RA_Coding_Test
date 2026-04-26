# add packages
import os
import re
from pathlib import Path

import pandas as pd
import numpy as np

import pandas as pd
import numpy as np
import re
from pathlib import Path

##BEA DATA
#read data
bea_file = Path("raw_data/bea/CAINC1__ALL_AREAS_1969_2024.csv")
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)


bea_raw = pd.read_csv(bea_file, encoding="latin1")
print(bea_raw.columns.tolist())

import re

def clean_names(cols):
    cleaned = []
    for c in cols:
        c = str(c).strip().lower()
        c = re.sub(r"[^\w]+", "_", c)
        c = re.sub(r"_+", "_", c)
        c = c.strip("_")
        cleaned.append(c)
    return cleaned

bea_raw.columns = clean_names(bea_raw.columns)
print(bea_raw.columns.tolist())

#select linecode
bea_sub = bea_raw[bea_raw["linecode"].isin([1, 2, 3])].copy()
print(bea_sub.shape)

year_cols = [c for c in bea_sub.columns if re.fullmatch(r"\d{4}", c)]
print(year_cols[:5], year_cols[-5:])

bea_long = bea_sub.melt(
    id_vars=[c for c in bea_sub.columns if c not in year_cols],
    value_vars=year_cols,
    var_name="year",
    value_name="value"
)

bea_long["year"] = bea_long["year"].astype(int)
bea_long["value"] = pd.to_numeric(bea_long["value"], errors="coerce")

bea_long["variable"] = bea_long["linecode"].map({
    1: "income",
    2: "population",
    3: "income_per_capita"
})

print(bea_long.head())
print(bea_long.shape)

#Privot table
bea_panel = (
    bea_long[["geofips", "geoname", "year", "variable", "value"]]
    .pivot_table(
        index=["geofips", "geoname", "year"],
        columns="variable",
        values="value",
        aggfunc="first"
    )
    .reset_index()
)

print(bea_panel.head())
print(bea_panel.shape)
print(bea_panel.columns.tolist())

#keep county level
bea_panel["geofips"] = bea_panel["geofips"].astype(str).str.strip()
bea_panel["geofips"] = bea_panel["geofips"].str.replace('"', '', regex=False)
bea_panel["geofips"] = bea_panel["geofips"].str.replace(" ", "", regex=False)

bea_panel["state_fips"] = bea_panel["geofips"].str[:2]
bea_panel["county_fips"] = bea_panel["geofips"].str[2:5]

bea_county = bea_panel[
    (bea_panel["geofips"].str.len() == 5) &
    (bea_panel["geofips"] != "00000") &
    (bea_panel["county_fips"] != "000")
].copy()

print(bea_panel["geofips"].head())
print(bea_county.head())
print(bea_county.shape)

bea_county["county_name"] = (
    bea_county["geoname"]
    .astype(str)
    .str.split(",", n=1)
    .str[0]
    .str.strip()
)

print(bea_county[["geofips", "geoname", "county_name"]].head(10))

state_lookup = pd.DataFrame({
    "state_fips": [
        "01","02","04","05","06","08","09","10","11","12","13","15","16","17","18","19",
        "20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35",
        "36","37","38","39","40","41","42","44","45","46","47","48","49","50","51","53",
        "54","55","56"
    ],
    "state_name": [
        "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut",
        "Delaware","District of Columbia","Florida","Georgia","Hawaii","Idaho","Illinois",
        "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts",
        "Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada",
        "New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota",
        "Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
        "South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington",
        "West Virginia","Wisconsin","Wyoming"
    ],
    "state_abbr": [
        "AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA",
        "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
        "NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
        "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
    ]
})

bea_county["county_name"] = (
    bea_county["geoname"]
    .astype(str)
    .str.split(",", n=1)
    .str[0]
    .str.strip()
)

bea_clean = (
    bea_county
    .merge(state_lookup, on="state_fips", how="left")
    [[
        "state_name", "state_abbr", "county_name", "state_fips", "county_fips",
        "year", "income", "population", "income_per_capita"
    ]]
    .sort_values(["state_fips", "county_fips", "year"])
    .reset_index(drop=True)
)

print(bea_clean.head())
print(bea_clean.columns.tolist())

print(bea_clean.head())
print(bea_clean.shape)

from pathlib import Path
Path("output").mkdir(exist_ok=True)

bea_clean.to_csv("output/bea_county_panel_python.csv", index=False)

#double check
check_df = pd.read_csv("output/bea_county_panel_python.csv")
print(check_df.head())
print(check_df.shape)
print(check_df.columns.tolist())

dup_check = (
    check_df.groupby(["state_fips", "county_fips", "year"])
    .size()
    .reset_index(name="n")
)

print(dup_check[dup_check["n"] > 1].head(20))
print("number of duplicates:", (dup_check["n"] > 1).sum())

##BLS Data
state_lookup = pd.DataFrame({
    "state_fips": [
        "01","02","04","05","06","08","09","10","11","12","13","15","16","17","18","19",
        "20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35",
        "36","37","38","39","40","41","42","44","45","46","47","48","49","50","51","53",
        "54","55","56"
    ],
    "state_name": [
        "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut",
        "Delaware","District of Columbia","Florida","Georgia","Hawaii","Idaho","Illinois",
        "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts",
        "Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada",
        "New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota",
        "Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
        "South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington",
        "West Virginia","Wisconsin","Wyoming"
    ],
    "state_abbr": [
        "AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA",
        "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
        "NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
        "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
    ]
})

bls_dir = Path("raw_data/bls")

bls_files = []
for f in bls_dir.iterdir():
    if f.is_file():
        name = f.name
        if (not name.startswith("~$")) and re.match(r"^laucnty\d{2}\.xlsx$|^laucnty\d{2}\.xls$", name):
            bls_files.append(f)

bls_files = sorted(bls_files)
print(bls_files)
print("number of files:", len(bls_files))


# clean bls panel
import pandas as pd
import numpy as np
import re
from pathlib import Path

def clean_names(cols):
    cleaned = []
    for c in cols:
        c = str(c).strip().lower()
        c = re.sub(r"[^\w]+", "_", c)
        c = re.sub(r"_+", "_", c)
        c = c.strip("_")
        cleaned.append(c)
    return cleaned


def clean_county_name(x):
    if pd.isna(x):
        return x
    x = str(x)
    x = re.sub(r",\s*[A-Z]{2}$", "", x)
    x = re.sub(r"\s+County$", "", x)
    x = re.sub(r"\s+Parish$", "", x)
    x = re.sub(r"\s+Borough$", "", x)
    x = re.sub(r"\s+Census Area$", "", x)
    x = re.sub(r"\s+Municipality$", "", x)
    x = re.sub(r"\s+City and Borough$", "", x)
    x = re.sub(r"\s+city and borough$", "", x)
    return x.strip()


def clean_bls_file(file_path):
    df_raw = pd.read_excel(file_path, header=None)

    # row 2 contains the actual headers
    new_names = df_raw.iloc[1].astype(str).tolist()

    df = df_raw.iloc[2:].copy()
    df.columns = clean_names(new_names)

    # extract year from file name
    yy = int(re.search(r"(\d{2})", file_path.name).group(1))
    file_year = 2000 + yy if yy <= 24 else 1900 + yy

    # standardize FIPS
    df["state_fips_code"] = (
        df["state_fips_code"]
        .astype(str)
        .str.extract(r"(\d+)")[0]
        .str.zfill(2)
    )

    df["county_fips_code"] = (
        df["county_fips_code"]
        .astype(str)
        .str.extract(r"(\d+)")[0]
        .str.zfill(3)
    )

    # numeric conversions
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    for col in ["labor_force", "employed", "unemployed", "unemployment_rate"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.extract(r"([-+]?\d*\.?\d+)")[0]
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["year_from_file"] = file_year

    # drop missing FIPS
    df = df[
        df["state_fips_code"].notna() &
        df["county_fips_code"].notna()
    ].copy()

    return df
  

state_lookup = pd.DataFrame({
    "state_fips": [
        "01","02","04","05","06","08","09","10","11","12","13","15","16","17","18","19",
        "20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35",
        "36","37","38","39","40","41","42","44","45","46","47","48","49","50","51","53",
        "54","55","56"
    ],
    "state_name": [
        "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut",
        "Delaware","District of Columbia","Florida","Georgia","Hawaii","Idaho","Illinois",
        "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts",
        "Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada",
        "New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota",
        "Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
        "South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington",
        "West Virginia","Wisconsin","Wyoming"
    ],
    "state_abbr": [
        "AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA",
        "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
        "NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
        "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
    ]
})

bls_dir = Path("raw_data/bls")

bls_files = []
for f in bls_dir.iterdir():
    if f.is_file():
        name = f.name
        if (not name.startswith("~$")) and re.match(r"^laucnty\d{2}\.xlsx$|^laucnty\d{2}\.xls$", name):
            bls_files.append(f)

bls_files = sorted(bls_files)

print(bls_files)
print("number of files:", len(bls_files))

test_df = clean_bls_file(bls_files[0])
print(test_df.head())
print(test_df.columns.tolist())
print(test_df.shape)

bls_all = pd.concat([clean_bls_file(f) for f in bls_files], ignore_index=True)

year_match_check = (bls_all["year"] == bls_all["year_from_file"]).all()
print("all years match file year:", year_match_check)

bls_clean = pd.DataFrame({
    "state_fips": bls_all["state_fips_code"],
    "county_fips": bls_all["county_fips_code"],
    "county_name": bls_all["county_name_state_abbreviation"].apply(clean_county_name),
    "year": bls_all["year"],
    "unemployment_rate": bls_all["unemployment_rate"]
})

bls_clean = bls_clean[bls_clean["county_fips"] != "000"].copy()
bls_clean["county_name"] = bls_clean["county_name"].astype(str).str.strip()

bls_clean = (
    bls_clean
    .merge(state_lookup, on="state_fips", how="left")
    [[
        "state_name", "state_abbr", "county_name",
        "state_fips", "county_fips", "year", "unemployment_rate"
    ]]
    .sort_values(["state_fips", "county_fips", "year"])
    .reset_index(drop=True)
)

print(bls_clean.head(10))
print(bls_clean.shape)

Path("output").mkdir(exist_ok=True)
bls_clean.to_csv("output/bls_county_panel_python.csv", index=False)

test_df = clean_bls_file(bls_files[0])
print(test_df.columns.tolist())
print(test_df.head())

#combine BEA and BLS
import pandas as pd
from pathlib import Path

bea = pd.read_csv(
    "output/bea_county_panel_python.csv",
    dtype={"state_fips": str, "county_fips": str}
)

bls = pd.read_csv(
    "output/bls_county_panel_python.csv",
    dtype={"state_fips": str, "county_fips": str}
)

print(bea.columns.tolist())
print(bls.columns.tolist())
print(bea.head())
print(bls.head())

#combine two
final_panel = bea.merge(
    bls,
    on=["state_fips", "county_fips", "year"],
    how="outer",
    suffixes=("_bea", "_bls")
)

final_panel["state_name"] = final_panel["state_name_bea"].combine_first(final_panel["state_name_bls"])
final_panel["state_abbr"] = final_panel["state_abbr_bea"].combine_first(final_panel["state_abbr_bls"])
final_panel["county_name"] = final_panel["county_name_bea"].combine_first(final_panel["county_name_bls"])

final_panel = final_panel[[
    "state_name",
    "state_abbr",
    "county_name",
    "state_fips",
    "county_fips",
    "year",
    "unemployment_rate",
    "income",
    "population",
    "income_per_capita"
]].sort_values(["state_fips", "county_fips", "year"]).reset_index(drop=True)

print(final_panel.head(10))
print(final_panel.shape)
print(final_panel.columns.tolist())


#double check
dup_check_final = (
    final_panel.groupby(["state_fips", "county_fips", "year"])
    .size()
    .reset_index(name="n")
)

print(dup_check_final[dup_check_final["n"] > 1].head(20))
print("number of duplicates:", (dup_check_final["n"] > 1).sum())

print("min year:", final_panel["year"].min())
print("max year:", final_panel["year"].max())

n_counties_final = final_panel[["state_fips", "county_fips"]].drop_duplicates().shape[0]
print("number of counties:", n_counties_final)

print(final_panel.isna().sum())

final_panel.loc[final_panel["state_name"].isna(), ["state_fips", "county_fips", "county_name", "year"]].head(20)

final_panel = final_panel[
    (final_panel["state_fips"] != "72") &
    (final_panel["county_fips"] != "000")
].copy()

valid_states_50 = [
    "01","02","04","05","06","08","09","10","12","13","15","16","17","18","19",
    "20","21","22","23","24","25","26","27","28","29","30","31","32","33","34",
    "35","36","37","38","39","40","41","42","44","45","46","47","48","49","50",
    "51","53","54","55","56"
]

final_panel = final_panel[
    final_panel["state_fips"].isin(valid_states_50) &
    (final_panel["county_fips"] != "000")
].copy()

print(final_panel.isna().sum())

dup_check_final = (
    final_panel.groupby(["state_fips", "county_fips", "year"])
    .size()
    .reset_index(name="n")
)

print("number of duplicates:", (dup_check_final["n"] > 1).sum())
print("min year:", final_panel["year"].min())
print("max year:", final_panel["year"].max())
print("number of counties:", final_panel[["state_fips", "county_fips"]].drop_duplicates().shape[0])

final_panel.to_csv("output/county_year_panel_python.csv", index=False)

key_cols = ["year", "state_fips", "state_abbr", "state_name", "zipcode"]

print("R duplicated keys:", df_r.duplicated(key_cols).sum())
print("Python duplicated keys:", df_py.duplicated(key_cols).sum())

tmp = df_r.merge(
    df_py,
    on=key_cols,
    suffixes=("_R", "_Python"),
    how="inner"
)

diff_a00200 = tmp[
    tmp["a00200_R"].fillna(-999999999).round(6)
    != tmp["a00200_Python"].fillna(-999999999).round(6)
]

print(diff_a00200[[*key_cols, "a00200_R", "a00200_Python"]].head(100))
print("a00200 real differences:", len(diff_a00200))

