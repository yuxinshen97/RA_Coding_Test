# Task 2 Data Summary

## Overview

Task 2 constructs harmonized IRS SOI county-year and ZIP-year panels. The final outputs are:

- a county-year SOI panel for 1989–2022
- a ZIP-year SOI panel for 2004–2022

Both panels retain a common set of variables that can be consistently identified across years and geographic levels:

- `n1`: number of returns
- `n2`: number of exemptions / individuals
- `a00100`: adjusted gross income
- `a00200`: wages and salaries
- `a00300`: taxable interest
- `a00600`: ordinary dividends

The sample is restricted to the **50 U.S. states**. Washington, D.C., state aggregate records, and non-geographic total rows are excluded. Monetary variables are reported in **thousand dollars** after harmonization.

## County-Year SOI Panel

The county-year SOI panel is organized at the county-year level. Each observation corresponds to one county in one year.

The final county panel contains **106,759 observations** across **34 years**, from **1989 to 2022**.

The final variables are:

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

### Harmonization Procedure

The IRS county files are not fully uniform across years. Earlier files are closer to county-year files, while later files often report county-by-AGI-group records. To construct a consistent panel, I standardized state identifiers, county identifiers, year fields, and variable names before appending files across years.

Beginning in 2010, several county files report multiple rows per county-year across AGI categories. These records were collapsed to the county-year level by summing `n1`, `n2`, `a00100`, `a00200`, `a00300`, and `a00600` across AGI groups. Summation is appropriate because these variables are totals, not averages.

State total rows, non-data header rows, and non-county records were removed. Suppression codes and invalid entries were recoded as missing values rather than zeros.

### County-Year Panel Coverage

The number of non-missing observations is:

- **106,753** for `n1`
- **106,753** for `n2`
- **106,741** for `a00100`
- **106,737** for `a00200`
- **53,389** for `a00300`
- **53,389** for `a00600`

The lower coverage for `a00300` and `a00600` reflects limited availability of interest and dividend variables in earlier source files.

A few rare negative or `-1` values remain in the source-derived monetary and count variables. These likely reflect IRS source-file coding, suppression, or adjustment entries and should be checked before regression analysis.

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

The ZIP-year SOI panel is organized at the ZIP-year level. Each observation corresponds to one ZIP code in one year.

The final ZIP panel contains **569,836 observations** across **19 years**, from **2004 to 2022**.

The final variables are:

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

### Harmonization Procedure

The raw ZIP files are reported at the ZIP-by-AGI-group level. I collapsed them to one observation per ZIP-year by summing `n1`, `n2`, `a00100`, `a00200`, `a00300`, and `a00600` across AGI groups within each `year × state_fips × state_abbr × zipcode` cell.

Two additional adjustments were applied. First, monetary variables were harmonized to **thousand dollars**. The 2007 and 2008 raw ZIP files were reported in dollars, so those years were divided by 1,000. Second, the sample was restricted to the **50 U.S. states**. Washington, D.C. and ZIP records coded as `00000` were removed because they represent state-level aggregate records rather than actual ZIP areas.

Duplicate checks confirm that the final ZIP panel has no repeated observations at the ZIP-year level.

### ZIP-Year Panel Coverage

All six key variables are fully observed in the retained ZIP panel:

- **569,836** observations for `n1`
- **569,836** observations for `n2`
- **569,836** observations for `a00100`
- **569,836** observations for `a00200`
- **569,836** observations for `a00300`
- **569,836** observations for `a00600`

The number of ZIP records is higher in 2006–2007 and stabilizes at roughly 27,000–30,000 ZIP-year observations per year from 2008 onward.

The main remaining feature is that `a00100` includes some negative values, which is consistent with adjusted gross income definitions. Other key variables are nonnegative after harmonization.

### ZIP SOI Panel Summary Statistics

| Variable | Mean | Median | Standard Deviation | Min | Max | Observations |
|---|---:|---:|---:|---:|---:|---:|
| `n1` | 4,787.91 | 1,530.00 | 7,122.74 | 0 | 438,630 | 569,836 |
| `n2` | 9,336.47 | 3,052.00 | 13,896.03 | 0 | 823,578 | 569,836 |
| `a00100` | 28,924,344.61 | 120,932.00 | 174,221,591.99 | -57,969 | 16,765,584,053 | 569,836 |
| `a00200` | 20,188,720.77 | 84,041.50 | 114,813,585.86 | 0 | 6,252,241,013 | 569,836 |
| `a00300` | 765,904.35 | 907.00 | 6,926,703.64 | 0 | 1,287,790,267 | 569,836 |
| `a00600` | 700,767.53 | 1,119.00 | 7,692,406.53 | 0 | 1,082,440,596 | 569,836 |

**Note:** Monetary variables are measured in thousand dollars. The sample covers the 50 U.S. states only. Washington, D.C. and aggregate ZIP records coded as `00000` are excluded.

## Final Output Files

- `output/soi_county_panel_1989_2022_R.csv`
- `output/soi_county_panel_1989_2022_python.csv`
- `output/soi_zip_panel_2004_2022_R.csv`
- `output/soi_zip_panel_2004_2022_python.csv`

## Validation Against BEA Data

I validate the SOI county panel against a BEA county-year panel matched by `year`, `state_fips`, and `county_fips`. The comparison focuses on SOI `n2` versus BEA `population`, and SOI `a00100` versus BEA `income`.

The two sources are highly correlated in cross-county variation. The correlation between SOI `n2` and BEA `population` is **0.9956**. The correlation between SOI `a00100` and BEA `income` is **0.9923**.

The level ratios are below one, as expected. On average, `n2 / population` is **0.864**, and `a00100 / income` is **0.580**. These gaps reflect definitional differences: SOI `n2` is based on tax-filing units and exemptions rather than the full resident population, while SOI adjusted gross income is narrower than BEA income.

Overall, the validation indicates that the SOI panels capture county-level cross-sectional variation very closely, despite expected level differences across data sources.
