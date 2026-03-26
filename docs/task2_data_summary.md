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

The revised county-year SOI panel is organized so that each observation represents one county (or county-equivalent unit) in one year.

The final county panel includes the following variables:

- `year`
- `state_fips`
- `state_abbr`
- `state_name`
- `county_fips`
- `county_name`
- `n1`
- `n2`
- `a00100`
- `a00200`
- `a00300`
- `a00600`

The revised county panel contains **53,410 observations**, covering **3,220 county-equivalent units** across **17 years** between **1989 and 2022**. The panel is not fully consecutive by year, but it includes the available county-level IRS SOI files retained in the harmonized output.

### Data Sources Used

The county panel was constructed from IRS county income files released in multiple formats across years. These files were not always structured in the same way. Depending on the year, the raw county files appeared as:

- county-year files with one observation per county-year
- county-by-AGI-group files with multiple observations per county-year
- spreadsheets or flat files with different layouts and naming conventions

### Data Processing and Harmonization

To build a consistent county-year panel, I first reviewed the raw files year by year and identified a common set of identifiers and income variables that could be retained across periods. I then standardized variable names, state identifiers, county identifiers, and year fields before combining the files.

State information was harmonized to include all of the following in the revised output:

- `state_fips`
- `state_abbr`
- `state_name`

County identifiers were also standardized so that the final panel consistently includes both `county_fips` and `county_name`. Variable names were renamed into a common format across years to ensure comparability.

### How Inconsistencies Across Years Were Handled

The main challenge in constructing the county panel was that the raw IRS county files changed structure over time.

For earlier years, the files were generally closer to the county-year format used in the final panel, but some still required cleaning of non-data rows, state total rows, inconsistent capitalization, and suppressed entries recorded using special symbols.

Beginning in **2010**, the raw county files were no longer consistently structured as one observation per county-year. Instead, many files were organized at the **county-by-AGI-group** level, so that the same county appeared multiple times within a year across different AGI categories.

To make the panel consistent across years, I collapsed these records back to **one observation per county-year**. The collapsing was performed at the **county-year** level. For the core count and dollar variables (`n1`, `n2`, `a00100`, `a00200`, `a00300`, and `a00600`), I summed values across AGI groups within each county-year. I did not take averages, because these variables represent totals rather than mean values. Summing across AGI groups is the appropriate way to reconstruct county-level totals when the groups are mutually exclusive components of the same county-year observation.

This step was necessary to ensure that the final county panel used a consistent unit of observation across the full time span.

### Treatment of Suppressed and Invalid Values

Several county files contained suppression codes rather than true numeric values. In particular, some entries were marked as `(1)` in the raw files, indicating suppression for disclosure protection. These values were not treated as zeros. Instead, they were recoded as missing values (`NA`) in the revised panel.

State total rows were removed so that the final file contains only county-level observations. Other non-data rows, such as title or header rows carried into spreadsheets, were also dropped during cleaning.

### Data Summary

For all six key variables (`n1`, `n2`, `a00100`, `a00200`, `a00300`, and `a00600`), the earliest available year in the county panel is **1989** and the latest available year is **2022**.

Missingness is limited. The number of non-missing observations is:

- **53,407** for `n1`
- **53,407** for `n2`
- **53,408** for `a00100`
- **53,406** for `a00200`
- **53,405** for `a00300`
- **53,397** for `a00600`

After revision, the county panel is consistently organized at the county-year level. Year-by-year row counts are stable, generally around **3,140–3,143 observations per year**. This pattern suggests that the revised county panel is internally consistent after harmonization.

A few anomalies remain worth noting. Negative values remain mainly in `a00100`, which is consistent with the definition of adjusted gross income. The minimum of `a00300` is `-1`, which appears to be a rare edge case. Relative to the original output, the revised county panel is substantially more internally consistent after recoding suppressed values as missing, removing state total rows, and collapsing post-2010 county-by-AGI-group files to the county-year level.

### County SOI Panel Summary Statistics

| Variable | Mean | Median | Standard Deviation | Min | Max | Observations |
|---|---:|---:|---:|---:|---:|---:|
| `n1` | 45,888.90 | 10,830 | 148,588.7 | 0 | 5,028,630 | 53,407 |
| `n2` | 89,641.18 | 22,108 | 288,359.8 | 0 | 9,293,169 | 53,407 |
| `a00100` | 3,080,333.58 | 502,365 | 11,910,760.6 | -198,783 | 480,343,326 | 53,408 |
| `a00200` | 2,133,164.52 | 353,061 | 7,999,809.6 | 0 | 305,958,865 | 53,406 |
| `a00300` | 44,502.06 | 6,082 | 323,016.2 | -1 | 52,646,635 | 53,405 |
| `a00600` | 75,031.76 | 6,712 | 394,368.7 | 0 | 14,222,363 | 53,397 |

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

The revised ZIP panel contains **571,112 observations**, covering **39,059 ZIP units** across **19 years** from **2004 to 2022**.

### Data Sources Used

The ZIP panel was constructed from IRS ZIP code income files distributed in multiple formats across years. As with the county files, naming conventions and raw layouts were not fully uniform across periods, so harmonization was required before the yearly files could be combined into a single panel.

### Data Processing and Harmonization

To construct the revised ZIP-year panel, I retained the same core variables used in the county panel whenever they could be identified consistently in the raw ZIP files. Variable names were standardized across years, and ZIP identifiers were stored as five-character strings to preserve leading zeros. State identifiers were harmonized to include `state_fips`, `state_abbr`, and `state_name` in the final output.

The raw ZIP files were more uniform than the county files overall, but they still required harmonization of variable names and identifier formats before yearly data could be combined.

### Handling ZIP-by-AGI-Group Structure

The raw ZIP files are organized at the **ZIP-by-AGI-group** level rather than directly at the ZIP-year level. Each ZIP code can therefore appear multiple times within a year across different AGI groups.

To construct the final ZIP-year panel, I collapsed the data to **one observation per ZIP-year**. The collapsing was performed at the `year × state_fips × state × zipcode` level. For the core count and dollar variables (`n1`, `n2`, `a00100`, `a00200`, `a00300`, and `a00600`), I summed values across AGI groups within each ZIP-year.

I did not take averages for these variables. These fields represent totals, so summing across mutually exclusive AGI categories is the appropriate way to reconstruct ZIP-level totals.

### Data Summary

For all six key variables in the ZIP panel, the earliest available year is **2004** and the latest available year is **2022**. In the revised ZIP panel, all six variables are fully observed across the retained records, with **571,112** non-missing observations for each of `n1`, `n2`, `a00100`, `a00200`, `a00300`, and `a00600`.

The ZIP-year counts are relatively stable over time. The panel contains **35,701 observations** in 2004, roughly **38,500 observations** in 2005–2007, and roughly **27,600 to 29,900 observations** per year from 2008 onward. The number of distinct ZIP units per year follows a similar pattern.

Compared with the county panel, the revised ZIP panel does not show the same post-2010 aggregation inconsistency and appears to be consistently organized at the ZIP-year level after harmonization. Duplicate checks also indicated no repeated observations at the ZIP-year level in the revised output.

The main notable pattern in the ZIP panel is that `a00100` includes some negative values, which is acceptable given the variable definition. Otherwise, the key variables are nonnegative in the revised output, and no major anomalies remain after standardizing identifiers, harmonizing variable names, and aggregating ZIP-by-AGI-group records into ZIP-year observations.

### ZIP SOI Panel Summary Statistics

| Variable | Mean | Median | Standard Deviation | Min | Max | Observations |
|---|---:|---:|---:|---:|---:|---:|
| `n1` | 8,400.39 | 1,540.0 | 153,536.4 | 0 | 18,878,390 | 571,112 |
| `n2` | 16,312.21 | 3,069.0 | 299,503.3 | 0 | 35,759,770 | 571,112 |
| `a00100` | 29,201,656.74 | 121,688.0 | 174,768,496.3 | -57,969 | 16,765,584,053 | 571,112 |
| `a00200` | 20,373,135.42 | 84,603.5 | 115,145,808.4 | 0 | 6,252,241,013 | 571,112 |
| `a00300` | 768,449.67 | 913.0 | 6,928,752.4 | 0 | 1,287,790,267 | 571,112 |
| `a00600` | 707,844.97 | 1,127.0 | 7,710,274.7 | 0 | 1,082,440,596 | 571,112 |

## Final Output Files

- `output/soi_county_panel_1989_2022_revised.csv`
- `output/soi_county_panel_1989_2022_python.csv`
- `output/soi_zip_panel_2004_2022_revised.csv`
- `output/soi_zip_panel_2004_2022_python.csv`
``
## Data Comparison with Other Sources

To validate the revised SOI county panel, I compare it with the revised BEA-based county-year panel using matched observations by `year`, `state_fips`, and `county_fips`. The comparison focuses on SOI `n2` versus BEA `population`, and SOI `a00100` versus BEA `income`.

These measures are not expected to be identical in levels. SOI `n2` is a tax-based count rather than a full resident-population measure, and SOI `a00100` is adjusted gross income (AGI), which is narrower than the broader BEA income concept. Therefore, the purpose of this comparison is to assess consistency in county-level patterns and time trends rather than exact equality.

The matched comparison contains 53,269 county-year observations. The cross-sectional relationship is extremely strong: the correlation between SOI `n2` and BEA `population` is 0.9986, and the correlation between SOI `a00100` and BEA `income` is 0.9930. The average `n2 / population` ratio is about 0.875, while the average `a00100 / income` ratio is about 0.569. These results indicate that SOI and BEA differ systematically in level, but remain highly consistent in county-level ordering.

The scatterplots and log-scale plots support this conclusion. In both the population and income comparisons, counties that are larger in one source also tend to be larger in the other. The log-scale relationships are especially close to linear, showing that this consistency holds across both smaller and larger counties.

The time-series comparison shows broadly similar long-run movement, but the SOI series is less smooth around 2008–2009. In those years, both `n2 / population` and `a00100 / income` decline and then recover in 2010, while matched county coverage remains stable. This suggests that the 2008–2009 pattern is unlikely to be caused by merge failure alone. Instead, it more likely reflects the fact that SOI is a tax-based source and may behave differently from BEA aggregates during the financial crisis, possibly because of reporting behavior, coverage differences, or year-specific comparability issues.

Overall, the revised SOI county panel appears highly consistent with the BEA-based panel in cross-county variation and broadly similar in long-run time trends. The main differences reflect definition differences and some caution is warranted for the 2008–2009 SOI observations in raw time-series comparisons.
