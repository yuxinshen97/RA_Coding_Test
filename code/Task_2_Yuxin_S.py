
## python code for Task 2

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
    df = pd.read_excel(file, header=None)

    df = df.iloc[5:, :9].copy()

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

    df = df[df["state_fips"].str.fullmatch(r"\d+")]
    df = df[df["county_fips"].str.fullmatch(r"\d+")]

    df["state_fips"] = df["state_fips"].str.zfill(2)
    df["county_fips"] = df["county_fips"].str.zfill(3)

    df = df[df["county_fips"] != "000"].copy()

    df = df[df["state_fips"].isin(valid_state_fips)].copy()

    numeric_cols = ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["year"] = year

    return df


def build_county_panel_for_year(folder, year):
    print("Working on:", folder)

    files = glob.glob(os.path.join(folder, "*.xls"))
    print("Number of files found:", len(files))

    dfs = []

    for f in files:
        try:
            df = read_one_old_county_file(f, year)
            dfs.append(df)
        except Exception as e:
            print("Error reading:", f)
            print(e)

    if len(dfs) == 0:
        raise ValueError("No files were successfully read.")

    return pd.concat(dfs, ignore_index=True)
  
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

print(panel_2008.head(10))
print(panel_2009.head(10))

county_fixed = pd.read_csv("output/soi_county_panel_2010_2022.csv")
county_2008_2022 = pd.concat(
    [panel_2008, panel_2009, county_fixed],
    ignore_index=True
).sort_values(["year", "state_fips", "county_fips"]).reset_index(drop=True)

print(
    county_2008_2022.groupby("year")
    .size()
    .reset_index(name="n")
    .sort_values("year")
)

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
county_2008_2022 = county_2008_2022.merge(
    state_lookup,
    on="state_fips",
    how="left"
)

print(county_2008_2022.head(10))

county_2008_2022.to_csv(
    "output/soi_county_panel_2008_2022.csv",
    index=False
)

import os
import re
import glob
import pandas as pd


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
    "Wisconsin": "WI", "Wyoming": "WY", "DofC": "DC"
}

VALID_STATE_FIPS = {
    "01","02","04","05","06","08","09","10","12","13",
    "15","16","17","18","19","20","21","22","23","24",
    "25","26","27","28","29","30","31","32","33","34",
    "35","36","37","38","39","40","41","42","44","45",
    "46","47","48","49","50","51","53","54","55","56"
}


def parse_number_col(series):
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False).str.strip(),
        errors="coerce"
    )


def parse_num(series):
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False).str.strip(),
        errors="coerce"
    )


def clean_county_soi_2007(file, year, state_abbr):
    df = pd.read_excel(
        file,
        skiprows=7,
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
        dtype=str
    )

    df = df[df["state_fips"] != "CODES"].copy()

    df["state_abbr"] = state_abbr
    df["year"] = year

    df["state_fips"] = df["state_fips"].astype(str).str.strip().str.zfill(2)
    df["county_fips"] = df["county_fips"].astype(str).str.strip().str.zfill(3)
    df["county_name"] = df["county_name"].astype(str).str.strip()

    for col in ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]:
        df[col] = parse_number_col(df[col])

    return df[
        ["year", "state_fips", "state_abbr", "county_fips", "county_name",
         "n1", "n2", "a00100", "a00200", "a00300", "a00600"]
    ]


files_2007 = glob.glob("raw_data/soi/county/2007_states/2007 County income/*.xls")

county_2007_all = []

for f in files_2007:
    fname = os.path.basename(f)
    state_name = re.sub(r"07ci\.xls$", "", fname)
    state_abbr = state_lookup_2007.get(state_name)

    if state_abbr is None:
        print("Unmatched 2007 file:", fname)
        continue

    df = clean_county_soi_2007(f, 2007, state_abbr)
    county_2007_all.append(df)

county_2007_all = pd.concat(county_2007_all, ignore_index=True)

print(county_2007_all.shape)
print(county_2007_all.groupby("state_abbr").size().reset_index(name="n"))
print(county_2007_all.head(20))


def clean_soi_1990_2006_file(file_path, year_value):
    file_name = os.path.basename(file_path)
    file_name_lower = file_name.lower()

    skip_value = 6 if file_name_lower == "kentucky01ci.xls" else 7

    df = pd.read_excel(file_path, skiprows=skip_value, header=None)

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
    df["county_name"] = df["county_name"].str.replace(r"\s+COUNTY$", "", regex=True)

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


test = clean_soi_1990_2006_file(
    "raw_data/soi/county/2005countyincome/Alabama05ci.xls",
    2005
)

print(test.shape)
print(test.head())

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

print(soi_1990_2006.shape)
print(soi_1990_2006.groupby("year").size().reset_index(name="n"))
print(failed_files_1990_2006.head(20))

soi_1990_2006_std = soi_1990_2006.copy()

soi_1990_2006_std = soi_1990_2006_std.rename(columns={
    "county_code": "county_fips_3",
    "n_returns": "n1",
    "n_exemptions": "n2",
    "agi": "a00100",
    "wages": "a00200"
})

soi_1990_2006_std["a00300"] = pd.NA
soi_1990_2006_std["a00600"] = pd.NA

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
]

county_2007_std = county_2007_all.copy()

county_2007_std = county_2007_std.merge(
    state_lookup,
    on=["state_fips", "state_abbr"],
    how="left"
)

county_2007_std = county_2007_std[
    [
        "year", "state_fips", "state_abbr", "state_name",
        "county_fips", "county_name",
        "n1", "n2", "a00100", "a00200", "a00300", "a00600"
    ]
]

county_2008_2022_clean = county_2008_2022.copy()

if "state_abbr_x" in county_2008_2022_clean.columns and "state_abbr_y" in county_2008_2022_clean.columns:
    county_2008_2022_clean["state_abbr"] = county_2008_2022_clean["state_abbr_x"].combine_first(
        county_2008_2022_clean["state_abbr_y"]
    )
    county_2008_2022_clean["state_name"] = county_2008_2022_clean["state_name_x"].combine_first(
        county_2008_2022_clean["state_name_y"]
    )

county_2008_2022_clean = county_2008_2022_clean[
    [
        "year", "state_fips", "state_abbr", "state_name",
        "county_fips", "county_name",
        "n1", "n2", "a00100", "a00200", "a00300", "a00600"
    ]
].copy()

county_panel_1990_2022 = pd.concat(
    [soi_1990_2006_std, county_2007_std, county_2008_2022_clean],
    ignore_index=True
).sort_values(["year", "state_fips", "county_fips"]).reset_index(drop=True)

print(county_panel_1990_2022.shape)
print(county_panel_1990_2022.groupby("year").size().reset_index(name="n"))
print(county_panel_1990_2022.head(20))
print(county_panel_1990_2022.isna().sum())

county_panel_1990_2022.to_csv(
    "output/soi_county_panel_1990_2022.csv",
    index=False
)

county_1989 = pd.read_csv(
    "raw_data/soi/county/1989countyincome/89incyallnoagi.csv"
)

print(county_1989.columns.tolist())
print(county_1989.shape)
print(county_1989.head(10))

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
county_1989_clean["state_fips"] = county_1989_clean["state_fips"].astype(str).str.zfill(2)
county_1989_clean["county_fips"] = county_1989_clean["county_fips"].astype(str).str.zfill(3)

print(
    county_1989_clean[
        ["year", "state_fips", "state", "county_fips", "county_name",
         "n1", "n2", "a00100", "a00200", "a00600", "a00300"]
    ].head(20)
)

county_1989_clean = county_1989_clean.merge(
    state_lookup,
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
print(county_1989_common.head(20))

county_panel_1989_2022 = pd.concat(
    [county_1989_common, county_panel_1990_2022],
    ignore_index=True
).sort_values(["year", "state_fips", "county_fips"]).reset_index(drop=True)

print(county_panel_1989_2022.groupby("year").size().reset_index(name="n"))
print(county_panel_1989_2022.shape)
print(county_panel_1989_2022.isna().sum())
print(county_panel_1989_2022.head(20))

county_panel_1989_2022.to_csv(
    "output/soi_county_panel_1989_2022.csv",
    index=False
)

## Zip code panel data

import pandas as pd
from pathlib import Path

RAW_DIR = Path("../raw_data/soi/zip")
OUT_DIR = Path("../output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

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


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase all column names."""
    df = df.copy()
    df.columns = [c.lower() for c in df.columns]
    return df


def safe_numeric(series):
    """Convert to numeric safely."""
    return pd.to_numeric(series, errors="coerce")


def pad_fips(series, width):
    """Convert to string and pad with leading zero."""
    return (
        series.astype("string")
        .str.replace(r"\.0$", "", regex=True)
        .str.zfill(width)
    )



def clean_zip_soi(file_path, year):
    df = pd.read_csv(file_path)
    df = standardize_columns(df)

    core = pd.DataFrame({
        "year": year,
        "state_fips": pad_fips(df["statefips"], 2),
        "state": df["state"],
        "zipcode": pad_fips(df["zipcode"], 5),
        "agi_stub": safe_numeric(df["agi_stub"]),
        "n1": safe_numeric(df["n1"]),
        "n2": safe_numeric(df["n2"]),
        "a00100": safe_numeric(df["a00100"]),
        "a00200": safe_numeric(df["a00200"]),
        "a00600": safe_numeric(df["a00600"]),
        "a00300": safe_numeric(df["a00300"]),
    })

    return core



def clean_zip_soi_2005_2010(file_path, year):
    df = pd.read_csv(file_path)
    df = standardize_columns(df)

    # rename possible alternative column names
    rename_map = {}
    if "zip_code" in df.columns and "zipcode" not in df.columns:
        rename_map["zip_code"] = "zipcode"
    if "agi_class" in df.columns and "agi_stub" not in df.columns:
        rename_map["agi_class"] = "agi_stub"
    if "agi_classs" in df.columns and "agi_stub" not in df.columns:
        rename_map["agi_classs"] = "agi_stub"
    if "state_fips" in df.columns and "statefips" not in df.columns:
        rename_map["state_fips"] = "statefips"

    if rename_map:
        df = df.rename(columns=rename_map)

    # if statefips missing, merge from state abbreviation
    if "statefips" not in df.columns:
        df["state"] = df["state"].astype("string").str.upper()
        df = df.merge(state_map, on="state", how="left")
        df = df.rename(columns={"state_fips": "statefips"})

    core = pd.DataFrame({
        "year": year,
        "state_fips": pad_fips(df["statefips"], 2),
        "state": df["state"].astype("string").str.upper(),
        "zipcode": pad_fips(df["zipcode"], 5),
        "agi_stub": safe_numeric(df["agi_stub"]),
        "n1": safe_numeric(df["n1"]),
        "n2": safe_numeric(df["n2"]),
        "a00100": safe_numeric(df["a00100"]),
        "a00200": safe_numeric(df["a00200"]),
        "a00600": safe_numeric(df["a00600"]),
        "a00300": safe_numeric(df["a00300"]),
    })

    return core


def make_zip_panel(df_core):
    panel = (
        df_core
        .groupby(["year", "state_fips", "state", "zipcode"], as_index=False)[
            ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]
        ]
        .sum(min_count=1)
    )

    for col in ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]:
        panel[col] = panel[col].round()

    return panel

from pathlib import Path

RAW_DIR = Path("raw_data/soi/zip")
OUT_DIR = Path("output")

print("RAW_DIR =", RAW_DIR)
print("Full path =", RAW_DIR / "11zpallagi.csv")
print("Exists?", (RAW_DIR / "11zpallagi.csv").exists())

test = pd.read_csv(RAW_DIR / "11zpallagi.csv")
print(test.head())
print(test.columns)

zip_2011_core = clean_zip_soi(RAW_DIR / "11zpallagi.csv", 2011)
zip_2011_panel = make_zip_panel(zip_2011_core)

print(zip_2011_core.head())
print(zip_2011_panel.head())
print(zip_2011_panel.info())


years_new = list(range(2011, 2023))

zip_core_list_new = []
zip_panel_list_new = []

for y in years_new:
    yy = str(y)[2:4]
    file_path = RAW_DIR / f"{yy}zpallagi.csv"
    
    core = clean_zip_soi(file_path, y)
    panel = make_zip_panel(core)
    
    zip_core_list_new.append(core)
    zip_panel_list_new.append(panel)

soi_zip_core_2011_2022 = (
    pd.concat(zip_core_list_new, ignore_index=True)
    .sort_values(["year", "state_fips", "zipcode", "agi_stub"])
)

soi_zip_panel_2011_2022 = (
    pd.concat(zip_panel_list_new, ignore_index=True)
    .sort_values(["year", "state_fips", "zipcode"])
)

print(soi_zip_panel_2011_2022.groupby("year").size().reset_index(name="n"))

duplicates_new = (
    soi_zip_panel_2011_2022
    .groupby(["year", "state_fips", "zipcode"])
    .size()
    .reset_index(name="n")
)

print(duplicates_new[duplicates_new["n"] > 1])

soi_zip_core_2011_2022.to_csv(OUT_DIR / "soi_zip_core_2011_2022.csv", index=False)
soi_zip_panel_2011_2022.to_csv(OUT_DIR / "soi_zip_panel_2011_2022.csv", index=False)

years_old = list(range(2005, 2011))

for y in years_old:
    yy = str(y)[2:4]
    file_path = RAW_DIR / f"{yy}zpallagi.csv"
    df_tmp = pd.read_csv(file_path, nrows=5)
    print(f"\n===== {y} =====")
    print(df_tmp.columns.tolist())
    
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

def clean_zip_soi_2005_2010(file_path, year):
    df = pd.read_csv(file_path)
    df.columns = [c.lower() for c in df.columns]

    if "zip_code" in df.columns and "zipcode" not in df.columns:
        df = df.rename(columns={"zip_code": "zipcode"})
    if "agi_class" in df.columns and "agi_stub" not in df.columns:
        df = df.rename(columns={"agi_class": "agi_stub"})
    if "agi_classs" in df.columns and "agi_stub" not in df.columns:
        df = df.rename(columns={"agi_classs": "agi_stub"})
    if "state_fips" in df.columns and "statefips" not in df.columns:
        df = df.rename(columns={"state_fips": "statefips"})

    if "statefips" not in df.columns:
        df["state"] = df["state"].astype("string").str.upper()
        df = df.merge(state_map, on="state", how="left")
        df = df.rename(columns={"state_fips": "statefips"})

    core = pd.DataFrame({
        "year": year,
        "state_fips": df["statefips"].astype("string").str.replace(r"\.0$", "", regex=True).str.zfill(2),
        "state": df["state"].astype("string").str.upper(),
        "zipcode": df["zipcode"].astype("string").str.replace(r"\.0$", "", regex=True).str.zfill(5),
        "agi_stub": pd.to_numeric(df["agi_stub"], errors="coerce"),
        "n1": pd.to_numeric(df["n1"], errors="coerce"),
        "n2": pd.to_numeric(df["n2"], errors="coerce"),
        "a00100": pd.to_numeric(df["a00100"], errors="coerce"),
        "a00200": pd.to_numeric(df["a00200"], errors="coerce"),
        "a00600": pd.to_numeric(df["a00600"], errors="coerce"),
        "a00300": pd.to_numeric(df["a00300"], errors="coerce"),
    })

    return core
  
def make_zip_panel(df_core):
    panel = (
        df_core
        .groupby(["year", "state_fips", "state", "zipcode"], as_index=False)[
            ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]
        ]
        .sum(min_count=1)
    )

    for col in ["n1", "n2", "a00100", "a00200", "a00600", "a00300"]:
        panel[col] = panel[col].round()

    return panel
  
zip_2005_core = clean_zip_soi_2005_2010(RAW_DIR / "05zpallagi.csv", 2005)
zip_2005_panel = make_zip_panel(zip_2005_core)

print(zip_2005_core.head())
print(zip_2005_panel.head())
print(zip_2005_panel.info())

years_old = list(range(2005, 2011))

zip_core_list_old = []
zip_panel_list_old = []

for y in years_old:
    yy = str(y)[2:4]
    file_path = RAW_DIR / f"{yy}zpallagi.csv"

    core = clean_zip_soi_2005_2010(file_path, y)
    panel = make_zip_panel(core)

    zip_core_list_old.append(core)
    zip_panel_list_old.append(panel)

soi_zip_core_2005_2010 = (
    pd.concat(zip_core_list_old, ignore_index=True)
    .sort_values(["year", "state_fips", "zipcode", "agi_stub"])
)

soi_zip_panel_2005_2010 = (
    pd.concat(zip_panel_list_old, ignore_index=True)
    .sort_values(["year", "state_fips", "zipcode"])
)

print(soi_zip_panel_2005_2010.groupby("year").size().reset_index(name="n"))

dup_old = (
    soi_zip_panel_2005_2010
    .groupby(["year", "state_fips", "zipcode"])
    .size()
    .reset_index(name="n")
)

print(dup_old[dup_old["n"] > 1])

soi_zip_panel_2005_2022 = (
    pd.concat([soi_zip_panel_2005_2010, soi_zip_panel_2011_2022], ignore_index=True)
    .sort_values(["year", "state_fips", "zipcode"])
)

print(soi_zip_panel_2005_2022.groupby("year").size().reset_index(name="n"))

dup_all = (
    soi_zip_panel_2005_2022
    .groupby(["year", "state_fips", "zipcode"])
    .size()
    .reset_index(name="n")
)

print(dup_all[dup_all["n"] > 1])

soi_zip_panel_2005_2022.to_csv(OUT_DIR / "soi_zip_panel_2004_2022_revised.csv", index=False)

import pandas as pd
from pathlib import Path

OUT_DIR = Path("output")


