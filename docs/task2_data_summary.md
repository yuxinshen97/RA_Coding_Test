# Task 2 Data Summary

**Author:** Yuxin Shen

## Overview

Task 2 focuses on downloading, cleaning, and harmonizing IRS Statistics of Income (SOI) data across years. The required outputs are:

- a county-year SOI panel
- a ZIP-year SOI panel

The county-year panel was constructed by harmonizing IRS county files released in different formats across time. The ZIP-year panel follows the same overall logic, with harmonization based on the structure of the available ZIP-level files.

## County-Year SOI Panel

The county-year SOI panel is organized so that each observation represents one county in one year.

To ensure comparability across years, I retained a common set of variables that could be consistently matched across formats:

- `year`
- `state_fips`
- `state`
- `county_fips`
- `county_name`
- `n1` — number of returns
- `n2` — number of exemptions
- `a00100` — adjusted gross income
- `a00200` — wages and salaries
- `a00600` — dividends
- `a00300` — interest

## Data Sources Used

The county-level SOI panel was constructed from IRS county income files distributed in different release formats over time.

These included:
- national CSV files for some years
- state-level Excel files for some years
- all-state CSV files for later years

## Construction Steps

1. Downloaded county-level IRS SOI files for available years.
2. Reviewed the documentation and file layouts for different periods.
3. Identified a common set of variables that could be consistently retained across release formats.
4. Standardized identifier variables and preserved leading zeros in FIPS codes.
5. Renamed variables into a common format.
6. Added year identifiers to each cleaned file.
7. Combined cleaned files into a unified county-year SOI panel.

## How Inconsistencies Across Years Were Handled

The main challenge in Task 2 was that IRS county files were released in different formats across periods.

### 1989
The 1989 county file was available as a national CSV file. It contained a compact set of county identifiers and income variables. These variables were renamed into the common format used in the final panel.

### 2007–2009
The 2007–2009 files were distributed as state-level Excel files. These files required:
- skipping title and header rows
- manually assigning column names
- adding `state` and `year`
- preserving leading zeros in FIPS codes
- converting suppression markers such as `d` into missing values

### 2010–2022
The 2010–2022 files were available as all-state CSV files and were more standardized. These files were harmonized by:
- standardizing column names
- renaming identifier variables
- adding year values
- preserving leading zeros in FIPS codes

## Assumptions

- A common-variable strategy was used rather than retaining all year-specific fields.
- County identifiers were standardized using FIPS codes and harmonized county names.
- Suppressed non-numeric values in older files were treated as missing values.
- Only variables with comparable meanings across periods were retained in the final county panel.

## Notable Observations

- IRS county files become much more standardized in the later period.
- Older files require much more manual cleaning and documentation review.
- Suppression markers appear in older releases and must be handled explicitly.
- A common-variable approach is necessary to maintain comparability across years.

## ZIP-Year SOI Panel

The ZIP-year SOI panel is intended to be constructed using the same general approach:

1. download ZIP-level SOI files for available years  
2. identify common identifier and income variables  
3. standardize ZIP identifiers and year fields  
4. harmonize variable names and definitions  
5. combine cleaned files into a ZIP-year panel dataset

## Final Output Files

- `output/task2_soi_county_year_panel.csv`
- `output/task2_soi_zip_year_panel.csv`