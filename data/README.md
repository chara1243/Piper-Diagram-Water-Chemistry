
# Input Data

This directory is reserved for hydrochemical input datasets.

## Required parameters

The CSV input file should contain:

| Parameter | Required column |
|---|---|
| Sample identification | Sample code |
| Calcium | Calcium (mg/l) |
| Magnesium | Magnesium (mg/l) |
| Sodium | Na (mg/l) |
| Potassium | K (mg/l) |
| Bicarbonate | HCO3 (mg/l) |
| Sulfate | SO4 (mg/l) |
| Chloride | Chloride (mg/l) |

## Data format

- Concentrations must be provided in mg/L.
- Missing values should be represented as blank or NaN.
- Negative concentrations are invalid.
- Each sample should have a unique sample code.

## Example sample codes

SK01(M)
SK02(NM)
BK01(M)
GK01(NM)

The workflow uses sample codes to identify rivers and seasons.

M = Monsoon

NM = Non-Monsoon

## Privacy

Do not upload confidential, unpublished, or restricted datasets.
