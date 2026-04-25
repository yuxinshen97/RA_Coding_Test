# Task 2 Data Summary

**Author:** Yuxin Shen

## Overview

Task 2 constructs revised IRS SOI county-year and ZIP-year panels using a harmonized set of variables that can be identified consistently across years. The final outputs include one county-year panel and one ZIP-year panel.

A common-variable harmonization strategy was used because the raw IRS SOI files were not fully uniform across years and geographic levels. Rather than attempting to preserve all year-specific fields, I retained a core set of variables that were clearly comparable across files and could be harmonized consistently.

The main variables retained in the revised panels are:

- `n1` — number of returns
- `n2` — number of exemptions / individuals
- `a00100` — adjusted gross income
- `a00200` — wages and salaries
- `a00300` — interest
- `a00600` — dividends

The identifier variables include year, state identifiers, and county or ZIP identifiers, depending on the panel.

## County-Year SOI Panel

The revised county-year SOI panel is organized so that each observation represents one county in one year. The final county panel is restricted to the 50 U.S. states and excludes state total rows.

The final county panel includes the following variables:

- `year`
- `state_fips`
- `state_abbr`
- `state_name`
- `county_fips`
- `county_name`
- `county_id`
- `n1`
- `n2`
- `a00100`
- `a00200`
- `a00300`
- `a00600`

The revised county panel contains **106,759 observations**, covering county-level SOI records across **34 years** from **1989 to 2022**.

### Data Sources Used

The county panel was constructed from IRS county income files released in multiple formats across years. These files were not always structured in the same way. Depending on the year, the raw county files appeared as:

- county-year files with one observation per county-year
- county-by-AGI-group files with multiple observations per county-year
- spreadsheets or flat files with different layouts and naming conventions

### Data Processing and Harmonization

To build a consistent county-year panel, I reviewed the raw files year by year and identified a common set of identifiers and income variables that could be retained across periods. I then standardized variable names, state identifiers, county identifiers, and year fields before combining the files.

State information was harmonized to include all of the following in the revised output:

- `state_fips`
- `state_abbr`
- `state_name`

County identifiers were standardized so that the final panel consistently includes `county_fips`, `county_name`, and `county_id`. Variable names were renamed into a common format across years to ensure comparability.

### How Inconsistencies Across Years Were Handled

The main challenge in constructing the county panel was that the raw IRS county files changed structure over time.

For earlier years, the files were closer to a county-year format, but some still required cleaning of non-data rows, state total rows, inconsistent capitalization, special state coding, and suppressed entries. For example, the 1989 file required standardizing state identifiers using state abbreviations because some raw state FIPS entries were not consistent with standard FIPS codes.

Beginning in 2010, the raw county files were often organized at the county-by-AGI-group level, so that the same county appeared multiple times within a year across different AGI categories.

To make the panel consistent across years, I collapsed these records back to one observation per county-year. The collapsing was performed at the county-year level. For the core count and dollar variables (`n1`, `n2`, `a00100`, `a00200`, `a00300`, and `a00600`), I summed values across AGI groups within each county-year. I did not take averages because these variables represent totals rather than mean values. Summing across AGI groups is the appropriate way to reconstruct county-level totals when the groups are mutually exclusive components of the same county-year observation.

This step was necessary to ensure that the final county panel used a consistent unit of observation across the full time span.

### Treatment of Suppressed and Invalid Values

Several county files contained suppression codes rather than true numeric values. These values were not treated as zeros. Instead, they were recoded as missing values (`NA`) in the revised panel.

State total rows were removed so that the final file contains only county-level observations. Other non-data rows, such as title or header rows carried into spreadsheets, were also dropped during cleaning.

### Data Summary

For the main count and income variables, the earliest available year in the county panel is **1989** and the latest available year is **2022**.

The number of non-missing observations is:

- **106,753** for `n1`
- **106,753** for `n2`
- **106,741** for `a00100`
- **106,737** for `a00200`
- **53,389** for `a00300`
- **53,389** for `a00600`

The smaller number of non-missing observations for `a00300` and `a00600` reflects the more limited availability of interest and dividend variables in the source files for earlier years.

After revision, the county panel is consistently organized at the county-year level. A few anomalies remain worth noting. Some variables contain rare negative values, including `a00100` and values of `-1` in several variables. These appear to reflect source-file coding or adjustment entries and should be checked before downstream regression analysis.

### County SOI Panel Summary Statistics

| Variable | Mean | Median | Standard Deviation | Min | Max | Observations |
|---|---:|---:|---:|---:|---:|---:|
| `n1` | 39,971.35 | 9,758 | 130,685.80 | -1 | 5,028,630 | 106,753 |
| `n2` | 81,835.77 | 20,990 | 263,769.37 | -1 | 9,293,169 | 106,753 |
| `a00100` | 2,296,875.96 | 381,143 | 9,288,754.21 | -198,783 | 480,343,326 | 106,741 |
| `a00200` | 1,638,330.31 | 276,520 | 6,375,909.40 | -1 | 305,958,865 | 106,737 |
| `a00300` | 44,408.35 | 6,077 | 323,013.52 | -1 | 52,646,635 | 53,389 |
| `a00600` | 74,768.39 | 6,703 | 394,100.88 | -1 | 14,222,363 | 53,389 |

## ZIP-Year SOI Panel

The revised ZIP-year SOI panel is organized so that each observation represents one ZIP code in one year.

The final ZIP panel includes the following variables:

- `year`
- `state_fips`
- `state_abbr`
- `state_name`
- `zipcode`
- `n1`
- `n2`
- `a00100`
- `a00200`
- `a00300`
- `a00600`

The final ZIP panel contains **569,836 observations**, covering **50 U.S. states** across **19 years** from **2004 to 2022**.

### Data Sources Used

The ZIP panel was constructed from IRS ZIP code income files distributed in multiple formats across years. Although the ZIP files are more uniform than the county files overall, naming conventions and raw layouts were not fully consistent across all years, so harmonization was required before the yearly files could be combined into a single panel.

### Handling ZIP-by-AGI-Group Structure

The raw ZIP files are organized at the **ZIP-by-AGI-group** level rather than directly at the ZIP-year level. Each ZIP code can therefore appear multiple times within a year across different AGI groups.

To construct the final ZIP-year panel, I collapsed the data to **one observation per ZIP-year**. The collapsing was performed at the `year × state_fips × state × zipcode` level. For the core count and dollar variables (`n1`, `n2`, `a00100`, `a00200`, `a00300`, and `a00600`), I summed values across AGI groups within each ZIP-year.


### Data Adjustments

Two additional adjustments were applied to ensure consistency.

First, the monetary variables `a00100`, `a00200`, `a00300`, and `a00600` were harmonized to a common unit of **thousand dollars**. The 2007 and 2008 raw ZIP files were reported in dollars, so those years were divided by 1,000 to make them comparable with the rest of the panel.

Second, the sample was restricted to the **50 U.S. states**. Washington, D.C. was excluded, and ZIP records equal to `00000` were removed because they represent state-level aggregate records rather than actual ZIP areas.

### Data Summary

For all six key variables in the ZIP panel, the earliest available year is **2004** and the latest available year is **2022**. In the final ZIP panel, all six variables are fully observed across the retained records, with **569,836** non-missing observations for each of `n1`, `n2`, `a00100`, `a00200`, `a00300`, and `a00600`.

The ZIP-year counts are relatively stable over time after harmonization, although the early years contain more ZIP records than later years. The panel contains roughly **38,000 observations** per year in 2006–2007 and roughly **27,000 to 30,000 observations** per year from 2008 onward. The number of distinct ZIP units per year follows a similar pattern.

Compared with the county panel, the revised ZIP panel does not show the same post-2010 aggregation inconsistency and appears to be consistently organized at the ZIP-year level after harmonization. Duplicate checks indicated no repeated observations at the ZIP-year level in the final output.

The main notable pattern in the ZIP panel is that `a00100` includes some negative values, which is acceptable given the variable definition. Otherwise, the key variables are nonnegative in the final output, and no major anomalies remain after standardizing identifiers, harmonizing variable names, rescaling monetary units, and aggregating ZIP-by-AGI-group records into ZIP-year observations.

### ZIP SOI Panel Summary Statistics

| Variable | Mean | Median | Standard Deviation | Min | Max | Observations |
|---|---:|---:|---:|---:|---:|---:|
| `n1` | 4,787.91 | 1,530.00 | 7,122.74 | 0 | 438,630 | 569,836 |
| `n2` | 9,336.47 | 3,052.00 | 13,896.03 | 0 | 823,578 | 569,836 |
| `a00100` | 28,924,344.61 | 120,932.00 | 174,221,591.99 | -57,969 | 16,765,584,053 | 569,836 |
| `a00200` | 20,188,720.77 | 84,041.50 | 114,813,585.86 | 0 | 6,252,241,013 | 569,836 |
| `a00300` | 765,904.35 | 907.00 | 6,926,703.64 | 0 | 1,287,790,267 | 569,836 |
| `a00600` | 700,767.53 | 1,119.00 | 7,692,406.53 | 0 | 1,082,440,596 | 569,836 |

**Note:** Monetary variables are measured in thousand dollars. The sample is a ZIP-year panel covering the 50 U.S. states from 2004 to 2022. Washington, D.C. and state aggregate ZIP records coded as `00000` are excluded.

## Final Output Files

- `output/soi_county_panel_1989_2022_R.csv`
- `output/soi_county_panel_1989_2022_python.csv`
- `output/soi_zip_panel_2004_2022_R.csv`
- `output/soi_zip_panel_2004_2022_python.csv`
``
## Data Comparison with Other Sources

I compare the SOI county panel with a BEA-based county-year panel using matched observations by `year`, `state_fips`, and `county_fips`. The comparison focuses on SOI `n2` versus BEA `population`, and SOI `a00100` versus BEA `income`.

The two sources show a strong cross-sectional relationship. The correlation between SOI `n2` and BEA `population` is **0.9956**, and the correlation between SOI `a00100` and BEA `income` is **0.9923**. On average, `n2 / population` is about **0.864**, and `a00100 / income` is about **0.580**.

The level differences reflect definition differences: SOI `n2` is based on tax filers rather than the full resident population, and SOI `a00100` (adjusted gross income) is narrower than BEA income.

These results indicate that while the levels differ, the two datasets are highly consistent in cross-county variation.