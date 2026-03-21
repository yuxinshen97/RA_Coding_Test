## Data Summary

### Combined County-Year Panel

The revised combined county-year panel contains **180,894 observations** covering **3,279 counties** across **56 years**, from **1969 to 2024**. Each observation represents one county in one year.

The panel combines the cleaned BEA county panel and the cleaned BLS county panel using harmonized state and county identifiers. The BEA data provide `income`, `population`, and `income_per_capita`, while the BLS data provide `unemployment_rate`.

For the four key variables, availability differs across sources. The earliest available year for `income`, `population`, and `income_per_capita` is **1969**, and the latest available year is **2024**. For `unemployment_rate`, the earliest available year is **1990** and the latest available year is **2024**. The number of non-missing observations is **112,569** for `unemployment_rate`, **174,148** for `income`, **174,148** for `population`, and **174,148** for `income_per_capita`.

The panel is generally well structured at the county-year level after harmonization. Year-by-year counts are stable within source coverage periods. In the earlier years from **1969 to 1989**, the panel contains **3,149 counties** per year. Starting in **1990**, the number increases to **3,279 counties** per year, which likely reflects broader coverage in the merged source files rather than a coding issue.

A notable feature of the merged panel is that the time coverage of unemployment data is shorter than that of the BEA variables. As a result, the final combined panel is balanced for identifiers within years, but not all variables are observed over the full 1969–2024 period.

### Combined County-Year Panel Summary Statistics

| Variable | Mean | Median | Standard Deviation | Min | Max | Observations |
|---|---:|---:|---:|---:|---:|---:|
| `unemployment_rate` | 6.03 | 5.3 | 3.15 | 0.4 | 40.6 | 112,569 |
| `income` | 2,753,689.17 | 414,231.0 | 12,741,751.51 | 183.0 | 818,509,319.0 | 174,148 |
| `population` | 87,176.83 | 23,434.0 | 285,627.46 | 43.0 | 10,125,014.0 | 174,148 |
| `income_per_capita` | 23,599.89 | 19,824.0 | 17,573.64 | 1,166.0 | 532,903.0 | 174,148 |

### Final Output Files

- `output/bea_county_panel_revised.csv`
- `output/bls_county_panel_revised.csv`
- `output/county_year_panel_revised.csv`