## Data Summary

### County SOI Panel

The revised county SOI panel contains **53,410 observations** covering **3,220 county-equivalent units** across **17 years**, from **1989 to 2022**. The panel is not a fully consecutive annual panel, but it covers the available county-level IRS SOI releases retained in the final harmonized dataset.

For all six key variables (`n1`, `n2`, `a00100`, `a00200`, `a00300`, and `a00600`), the earliest available year is **1989** and the latest available year is **2022**. Missingness is limited. The number of non-missing observations is **53,407** for `n1`, **53,407** for `n2`, **53,408** for `a00100`, **53,406** for `a00200`, **53,405** for `a00300`, and **53,397** for `a00600`.

After revision, the county panel is consistently organized at the county-year level. Year-by-year row counts are stable, generally around **3,140–3,143 observations per year**. The number of county-equivalent units is **321** in 1989, **324** in most years from 2007 to 2018, **325** in 2019 and 2020, and **329** in 2021 and 2022. This modest increase in recent years likely reflects source coverage differences rather than a coding error.

A few notable anomalies remain. Negative values remain mainly in `a00100`, which is consistent with the definition of adjusted gross income. The minimum of `a00300` is `-1`, which appears to be a rare edge case. Relative to the original output, the revised county panel is much more internally consistent after recoding suppressed values as missing, removing state total rows, and collapsing post-2010 county-by-AGI-group files to the county-year level.

### County SOI Panel Summary Statistics

| Variable | Mean | Median | Standard Deviation | Min | Max | Observations |
|---|---:|---:|---:|---:|---:|---:|
| `n1` | 45,888.90 | 10,830 | 148,588.7 | 0 | 5,028,630 | 53,407 |
| `n2` | 89,641.18 | 22,108 | 288,359.8 | 0 | 9,293,169 | 53,407 |
| `a00100` | 3,080,333.58 | 502,365 | 11,910,760.6 | -198,783 | 480,343,326 | 53,408 |
| `a00200` | 2,133,164.52 | 353,061 | 7,999,809.6 | 0 | 305,958,865 | 53,406 |
| `a00300` | 44,502.06 | 6,082 | 323,016.2 | -1 | 52,646,635 | 53,405 |
| `a00600` | 75,031.76 | 6,712 | 394,368.7 | 0 | 14,222,363 | 53,397 |

### ZIP SOI Panel

The revised ZIP SOI panel contains **571,112 observations** covering **39,059 ZIP units** across **19 years**, from **2004 to 2022**. Each observation represents one ZIP code in one year.

For all six key variables in the ZIP panel, the earliest available year is **2004** and the latest available year is **2022**. In the revised ZIP panel, all six variables are fully observed across the retained records, with **571,112** non-missing observations for each of `n1`, `n2`, `a00100`, `a00200`, `a00300`, and `a00600`.

The ZIP-year counts are relatively stable over time. The panel contains **35,701 observations** in 2004, roughly **38,500 observations** in 2005–2007, and roughly **27,600 to 29,900 observations** per year from 2008 onward. The number of distinct ZIP units per year follows a similar pattern. Compared with the county panel, the revised ZIP panel does not show the same aggregation inconsistency problem and appears to be consistently organized at the ZIP-year level after harmonization.

The main notable pattern in the ZIP panel is that `a00100` includes some negative values, which is acceptable given the variable definition. Otherwise, the key variables are nonnegative in the revised output, and no major anomalies remain after standardizing identifiers, harmonizing variable names, and aggregating ZIP-by-AGI-group records into ZIP-year observations.

### ZIP SOI Panel Summary Statistics

| Variable | Mean | Median | Standard Deviation | Min | Max | Observations |
|---|---:|---:|---:|---:|---:|---:|
| `n1` | 8,400.388 | 1,540.0 | 153,536.4 | 0 | 18,878,390 | 571,112 |
| `n2` | 16,312.205 | 3,069.0 | 299,503.3 | 0 | 35,759,770 | 571,112 |
| `a00100` | 29,201,656.739 | 121,688.0 | 174,768,496.3 | -57,969 | 16,765,584,053 | 571,112 |
| `a00200` | 20,373,135.418 | 84,603.5 | 115,145,808.4 | 0 | 6,252,241,013 | 571,112 |
| `a00300` | 768,449.665 | 913.0 | 6,928,752.4 | 0 | 1,287,790,267 | 571,112 |
| `a00600` | 707,844.970 | 1,127.0 | 7,710,274.7 | 0 | 1,082,440,596 | 571,112 |