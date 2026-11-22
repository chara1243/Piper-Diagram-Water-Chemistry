
# Piper Diagram Generation Using Python and WQChartPy

## Overview

This repository provides a reproducible Python workflow for generating Piper trilinear diagrams from hydrochemical water-quality data using the WQChartPy library.

The workflow is designed for groundwater and surface-water hydrochemical characterization and supports the visualization of major cations and anions across different rivers, sampling locations, and seasons.

## Objectives

- Process and clean water chemistry datasets.
- Convert major ion concentrations from mg/L to meq/L.
- Calculate cation and anion composition percentages.
- Visualize hydrochemical characteristics using Piper diagrams.
- Compare hydrochemical composition across rivers and seasons.

## Methodology

The workflow consists of the following steps:

1. Import hydrochemical data from CSV.
2. Clean missing and non-numeric observations.
3. Identify river and seasonal sampling categories.
4. Convert major ions into milliequivalents per liter (meq/L).
5. Calculate cation and anion percentages.
6. Prepare the required input format for WQChartPy.
7. Generate Piper trilinear diagrams.
8. Export figures in high-resolution PNG format.

## Chemical Parameters

### Major Cations

- Calcium (Ca2+)
- Magnesium (Mg2+)
- Sodium (Na+)
- Potassium (K+)

### Major Anions

- Bicarbonate (HCO3-)
- Carbonate (CO3 2-)
- Chloride (Cl-)
- Sulfate (SO4 2-)

## Installation

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Usage

1. Download or clone this repository.
2. Open `Piper_Diagram_WQChartPy.ipynb` in Google Colab.
3. Upload your hydrochemical CSV dataset.
4. Check that the column names match the expected format.
5. Run all notebook cells.
6. Find the generated Piper diagram in the output directory.

## Input Data

The input dataset must contain major ion concentrations in mg/L.

A sample CSV template will be provided in the data directory.

## Output

The workflow generates high-resolution Piper diagrams in PNG format.

## Software and Libraries

- Python
- Pandas
- NumPy
- Matplotlib
- WQChartPy
- Google Colab

## Scientific Reference

Piper, A. M. (1944). A Graphic Procedure in the Geochemical Interpretation of Water-Analyses. Eos, Transactions American Geophysical Union, 25, 914–928.

WQChartPy:
https://github.com/jyangfsu/WQChartPy

## Author

Hydrochemical Data Visualization and Piper Diagram Workflow.

## License

This project is distributed under the MIT License.
