## Task 1 Data Summary

### Overview

Task 1 constructs a U.S. county-year panel dataset by combining county-level data from the BEA and BLS. The final panel uses harmonized state and county identifiers and includes the following variables:

- `state_name`
- `state_abbr`
- `county_name`
- `state_fips`
- `county_fips`
- `year`
- `unemployment_rate`
- `income`
- `population`
- `income_per_capita`

In addition to the original workflow, the full data-cleaning and panel-construction process was also replicated in **Python**, and the Python-generated output files are included for reproducibility.

### Dataset Coverage

The final combined county-year panel contains **179,025 observations** covering **3,200 counties** across **56 years**, from **1969 to 2024**. Each observation represents one county in one year.

The panel combines the cleaned BEA county panel and the cleaned BLS county panel using harmonized state and county identifiers. The BEA data provide `income`, `population`, and `income_per_capita`, while the BLS data provide `unemployment_rate`.

For the four key variables, availability differs across sources. The earliest available year for `income`, `population`, and `income_per_capita` is **1969**, and the latest available year is **2024**. For `unemployment_rate`, the earliest available year is **1990** and the latest available year is **2024**.

The final panel keeps only the **50 U.S. states**. State-level summary rows and non-state territories were excluded. County FIPS and state FIPS codes were treated as character variables throughout construction in order to preserve leading zeros and ensure accurate merges.

### Data Sources Used

#### BEA

BEA county personal income data were used to construct:

- `income`
- `population`
- `income_per_capita`

#### BLS

BLS Local Area Unemployment Statistics were used to construct:

- `unemployment_rate`

The BLS unemployment data begin in **1990**, which is why `unemployment_rate` is missing for earlier years in the merged panel.

### Construction Steps

1. Downloaded the BEA and BLS county-level raw files.
2. Cleaned each source separately.
3. Standardized state and county identifiers.
4. Preserved leading zeros in FIPS codes by storing them as character variables.
5. Harmonized variable names across the two sources.
6. Removed state summary rows.
7. Restricted the final merged panel to the 50 U.S. states.
8. Merged the cleaned BEA and BLS panels into a final county-year panel.
9. Replicated the full workflow in Python and exported parallel Python output files.

### How Inconsistencies Were Handled

Several inconsistencies had to be addressed during construction:

- BEA and BLS use different raw file layouts and naming conventions.
- County and state identifiers had to be standardized before merging.
- County naming conventions sometimes differed across raw sources, so the merge relied primarily on standardized FIPS identifiers rather than names.
- The BEA series cover a longer historical period than the BLS unemployment series.
- State summary rows and non-state territorial records were excluded from the final 50-state panel.

### Assumptions

- State and county FIPS codes were treated as the primary identifiers.
- The final merged panel was constructed at the county-year level.
- Variable definitions were taken directly from the underlying BEA and BLS sources.
- `unemployment_rate` is only expected to be observed beginning in **1990**.

### Notable Observations

- The merged panel is balanced in identifiers within years after harmonization, but not all variables are observed over the full time span.
- The BEA variables begin in **1969**, while the BLS unemployment series begin in **1990**.
- Preserving standardized county identifiers was essential for reproducibility and accurate merging.
- The Python replication reproduced the full BEA cleaning, BLS cleaning, and final county-year merge workflow.

### Combined County-Year Panel Summary

The revised combined county-year panel contains **179,025 observations** across **3,200 counties** from **1969 to 2024**.

The number of non-missing observations is:

- **109,882** for `unemployment_rate`
- **174,092** for `income`
- **174,092** for `population`
- **174,092** for `income_per_capita`

In the earlier years from **1969 to 1989**, the panel contains fewer counties because unemployment data are not yet available from BLS. Starting in **1990**, `unemployment_rate` enters the merged panel.

### Combined County-Year Panel Summary Statistics

| Variable | Mean | Median | Standard Deviation | Min | Max | Observations |
|---|---:|---:|---:|---:|---:|---:|
| `unemployment_rate` | 5.83 | 5.2 | 2.81 | 0.4 | 40.6 | 109,882 |
| `income` | 2,745,999.71 | 414,021.0 | 12,731,555.11 | 183.0 | 818,509,319.0 | 174,092 |
| `population` | 86,999.50 | 23,422.0 | 285,500.43 | 43.0 | 10,125,014.0 | 174,092 |
| `income_per_capita` | 23,593.96 | 19,821.5 | 17,565.34 | 1,166.0 | 532,903.0 | 174,092 |
### Final Output Files

#### R-based output files

- `output/bea_county_panel_R.csv`
- `output/bls_county_panel_R.csv`
- `output/county_year_panel_R.csv`

#### Python replication output files

- `output/bea_county_panel_python.csv`
- `output/bls_county_panel_python.csv`
- `output/county_year_panel_python.csv`

#### R script

- `code/Task_1_Yuxin_S.Rmd`

#### Python script

- `code/Task_1_Yuxin_S.py`

