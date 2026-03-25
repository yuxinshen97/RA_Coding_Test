# Task 1 Data Summary

**Author:** Yuxin Shen

## Overview

Task 1 constructs a U.S. county-year panel dataset by combining county-level data from BEA and BLS. The final panel includes harmonized county identifiers and the following variables:

- State name
- County name
- State FIPS code
- County FIPS code
- Unemployment rate
- Income
- Population
- Income per capita

## Dataset Coverage

The Task 1 dataset is organized as a county-year panel. Each observation represents one county in one year.

The cleaned BEA county panel covers county-level income, population, and income per capita.  
The cleaned BLS county panel covers county-level unemployment rates.  
The final merged county-year panel combines these two sources using standardized county identifiers.

Because the two sources have different raw formats and different year coverage, the final merged panel reflects the years and county identifiers that can be consistently matched across both datasets.

## Data Sources Used

### BEA
BEA county personal income data were used to construct the income-related variables:
- personal income
- population
- per capita personal income

### BLS
BLS Local Area Unemployment Statistics were used to construct:
- unemployment rate

## Construction Steps

1. Downloaded the BEA and BLS county-level raw files.
2. Cleaned each source separately.
3. Standardized state and county identifiers.
4. Preserved leading zeros in FIPS codes.
5. Harmonized variable names across the two sources.
6. Merged the two datasets into a final county-year panel.

## How Inconsistencies Were Handled

Several inconsistencies had to be addressed during construction:

- BEA and BLS use different raw file layouts.
- County and state identifiers had to be standardized before merging.
- FIPS codes were stored as character variables to preserve leading zeros.
- County naming conventions sometimes differed across raw sources, so the merge relied primarily on standardized identifiers.

## Assumptions

- State and county FIPS codes were treated as the primary identifiers.
- The final merged panel was constructed at the county-year level.
- Variable definitions were taken directly from the underlying BEA and BLS sources.

## Notable Observations

- BEA provides a longer historical time span than BLS.
- The merged Task 1 panel is constrained by the overlap between the two sources.
- Preserving standardized county identifiers was essential for reproducibility and accurate merging.

## Final Output Files

- `output/task1_bea_county_panel.csv`
- `output/task1_bls_county_panel.csv`
- `output/task1_county_year_panel.csv`