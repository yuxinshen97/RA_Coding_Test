## ZIP-Year SOI Panel

The ZIP-year SOI panel is organized so that each observation represents one ZIP code in one year.

Because the raw IRS ZIP files were not fully standardized across years, I used the same common-variable harmonization strategy as in the county panel. I retained a core set of variables that could be identified consistently across the ZIP-level files from 2004 onward.

The harmonized ZIP-year panel currently includes the following variables:

- `year`
- `state_fips`
- `state`
- `zipcode`
- `n1` — number of returns
- `n2` — number of exemptions
- `a00100` — adjusted gross income
- `a00200` — wages and salaries
- `a00600` — dividends
- `a00300` — interest

## Data Sources Used

The ZIP-level SOI panel was constructed from IRS ZIP code income files distributed in multiple formats across years.

For the completed portion of the ZIP panel, I used ZIP-level files for 2004–2022. These files were not released in a uniform format. Depending on the year, they appeared as:

- state-level Excel files
- all-state CSV files
- ZIP-by-AGI grouped files with different naming conventions

## Construction Steps

1. Downloaded ZIP-level IRS SOI files for available years used in the final panel.
2. Reviewed file layouts and documentation for different ZIP-file periods.
3. Identified a common set of identifier and income variables that could be retained across years.
4. Standardized ZIP codes as 5-character strings to preserve leading zeros.
5. Standardized state abbreviations and state FIPS codes.
6. Renamed variables into a common format across years.
7. Added year identifiers to each cleaned file.
8. Cleaned ZIP-by-AGI-group records and aggregated them into ZIP-year observations.
9. Combined cleaned yearly files into a unified ZIP-year SOI panel.

## How Inconsistencies Across Years Were Handled

The main challenge in the ZIP panel was that variable names, file layouts, and release formats changed across time.

### 2004

The 2004 ZIP files were distributed as separate state-level Excel files. Within each file, ZIP codes and AGI classes appeared in a stacked layout rather than a flat rectangular table. ZIP code rows and AGI-class rows had to be separated and linked during cleaning.

To harmonize these files, I:

- skipped non-data title and header rows
- identified rows containing ZIP codes
- filled ZIP identifiers downward to the associated AGI rows
- mapped AGI class labels into a common `agi_stub` field
- retained only the common variables used in the final ZIP panel
- aggregated ZIP-by-AGI records into ZIP-year observations

### 2005–2008

The 2005–2008 ZIP files used older all-state CSV layouts. In these files:

- some identifier variables appeared in a different order
- the AGI grouping variable appeared as `agi_class` in some years
- ZIP code variable capitalization differed across files
- some files did not directly include `statefips`

To harmonize these years, I:

- converted all column names to lowercase
- mapped older AGI-group variables such as `agi_class` into a common `agi_stub` field
- standardized `zipcode` as a 5-character string
- converted state abbreviations to uppercase
- generated `state_fips` from state abbreviations when it was not explicitly provided

### 2009–2010

The 2009–2010 ZIP files were closer to the later standardized format. These files already included variables such as `STATEFIPS`, `STATE`, `zipcode`, and `agi_stub`, though capitalization still differed from later years.

To harmonize these years, I:

- standardized all column names
- preserved leading zeros in ZIP codes and state FIPS codes
- retained only the common variables used in the final ZIP panel

### 2011–2022

The 2011–2022 ZIP files were more standardized and included a consistent set of variables across years. These files used a common structure with variables such as `STATEFIPS`, `STATE`, `ZIPCODE`, `agi_stub`, `N1`, `N2`, `A00100`, `A00200`, `A00300`, and `A00600`.

These files were harmonized by:

- converting variable names to lowercase
- standardizing ZIP and state FIPS identifiers
- retaining the common core variables
- aggregating across AGI groups to create one ZIP-year observation per ZIP code per year

## Aggregation Logic

The raw ZIP files were initially read at the ZIP-by-AGI-group level. In other words, each ZIP code appeared multiple times within a year, once for each AGI group.

To construct the final ZIP-year panel, I aggregated these records across AGI groups within each year, state, and ZIP code. This produced a single observation per ZIP code per year in the final dataset.

During this step, I also rounded aggregated values where needed to remove small decimal artifacts introduced by IRS disclosure-related coding conventions in the source files.

## Assumptions

- A common-variable strategy was used rather than attempting to retain all year-specific ZIP variables.
- ZIP codes were stored as 5-character strings to preserve leading zeros.
- When `state_fips` was not explicitly available in older ZIP files, it was reconstructed from the state abbreviation.
- The final ZIP-year panel was created by aggregating across AGI groups within a year and ZIP code.
- Only variables with clearly comparable meanings across years were retained in the final ZIP panel.
- For some older ZIP releases, variables available in later years were not consistently reported. In such cases, unavailable variables were set to missing rather than imputed.

## Notable Observations

- The ZIP-level files are less uniform than they initially appear, especially in the 2004–2010 period.
- The main inconsistencies involve identifier names, AGI-group variable names, file layout, and the presence or absence of `statefips`.
- The 2004 state-level files required the most manual restructuring because ZIP codes and AGI categories were embedded in a stacked format.
- Later ZIP files are much easier to standardize than earlier ones.
- Constructing a clean ZIP-year panel requires first cleaning ZIP-by-AGI records and then aggregating them to the ZIP-year level.

## Final Output Files

- `output/soi_county_panel_1989_2022.csv`
- `output/soi_zip_panel_2004_2022.csv`