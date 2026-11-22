
# Piper Diagram Generation Using Python and WQChartPy

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Analysis](https://img.shields.io/badge/Analysis-Hydrochemistry-green)
![Visualization](https://img.shields.io/badge/Visualization-Piper%20Diagram-orange)
![Platform](https://img.shields.io/badge/Platform-Google%20Colab-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Overview

This project provides a reproducible Python workflow for hydrochemical data processing and Piper trilinear diagram generation using the WQChartPy library.

The workflow is designed to analyze major-ion chemistry in groundwater and surface-water samples and visualize hydrochemical composition across different rivers and sampling seasons.

The initial application focuses on three river systems:

- A River
- B River
- C River

The workflow can be adapted to other hydrochemical datasets by modifying the input data and river classification settings.

## Key Features

- CSV-based hydrochemical data import.
- Automated data cleaning and preprocessing.
- River and seasonal sample classification.
- Conversion of major ions from mg/L to meq/L.
- Calculation of cation and anion percentages.
- Charge balance error (CBE) calculation.
- Hydrochemical data quality screening.
- Piper trilinear diagram generation.
- River-specific colors and marker styles.
- High-resolution PNG and PDF figure export.
- Processed hydrochemical data export.

## Methodology

### 1. Data Preparation

Major-ion concentrations are imported from a CSV file.

### 2. Data Cleaning

Non-numeric values, missing observations and invalid negative concentrations are handled during preprocessing.

### 3. River and Seasonal Classification

Samples are classified using sample identification codes.

| River code | River |
|---|---|
A 
B
C

Seasonal classification:

- M = Monsoon
- NM = Non-Monsoon

### 4. Conversion to Milliequivalents

Major-ion concentrations are converted from mg/L to meq/L.

Cations:

Ca (meq/L) = Ca (mg/L) / 20.04

Mg (meq/L) = Mg (mg/L) / 12.15

Na (meq/L) = Na (mg/L) / 22.99

K (meq/L) = K (mg/L) / 39.10

Anions:

HCO3 (meq/L) = HCO3 (mg/L) / 61.02

SO4 (meq/L) = SO4 (mg/L) / 48.03

Cl (meq/L) = Cl (mg/L) / 35.45

Carbonate is assumed to be zero in the default workflow unless measured values are available.

### 5. Ionic Composition

Cation percentages:

Ca (%) = Ca (meq/L) / Total cations × 100

Mg (%) = Mg (meq/L) / Total cations × 100

Na (%) = Na (meq/L) / Total cations × 100

K (%) = K (meq/L) / Total cations × 100

Anion percentages are calculated similarly using total anions.

### 6. Charge Balance Error

Charge balance error is calculated as:

CBE (%) = [(Σ Cations - Σ Anions) / (Σ Cations + Σ Anions)] × 100

A value within ±5% is used as a common preliminary screening criterion. Samples outside this range are flagged rather than automatically removed.

### 7. Piper Diagram

The WQChartPy triangle_piper module generates the Piper trilinear diagram using original major-ion concentrations in mg/L.

The diagram is used to examine the relative composition of major cations and anions and identify hydrochemical facies.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/Piper-Diagram-Water-Chemistry.git
```

Navigate into the project:

```bash
cd Piper-Diagram-Water-Chemistry
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Analysis

Place your CSV input file in the project root directory.

Ensure the filename matches the configuration in `piper_diagram.py`.

Run:

```bash
python piper_diagram.py
```

## Google Colab

The workflow can also be used in Google Colab.

1. Upload the notebook.
2. Install the dependencies.
3. Upload your hydrochemical CSV file.
4. Execute the notebook cells.
5. Download the generated figures and processed datasets.

## Expected Outputs

### Figures

- Piper_Diagram.png
- Piper_Diagram.pdf

### Processed datasets

- Hydrochemical_Processed_Data.csv
- Charge_Balance_Report.csv

## River Visualization

| River | Color | Marker |
|---|---|---|
| A | Red | Triangle |
| B | Blue | Square |
| C | Green | Diamond |

## Software and Libraries

- Python
- Pandas
- NumPy
- Matplotlib
- SciPy
- Scikit-learn
- WQChartPy

## Scientific References

Piper, A. M. (1944). A Graphic Procedure in the Geochemical Interpretation of Water-Analyses. Eos, Transactions American Geophysical Union, 25, 914–928.

WQChartPy:
https://github.com/jyangfsu/WQChartPy

## Limitations

- Carbonate concentration is assumed to be zero by default.
- The accuracy of hydrochemical interpretation depends on the quality of laboratory measurements.
- Charge balance screening does not replace laboratory quality assurance.
- The calculated TDS in this workflow is the sum of the selected major-ion concentrations, not an independent laboratory TDS measurement.
- Hydrochemical facies should be interpreted with supporting geochemical and environmental evidence.

## Author

Charan Bhattarai

## License

This project is licensed under the MIT License.
