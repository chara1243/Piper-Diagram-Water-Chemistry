
# =============================================================================
# PIPER DIAGRAM GENERATION USING WQCHARTPY
# =============================================================================
# Project: Piper Diagram - Water Chemistry Analysis
# Author: Hydrochemical Data Visualization Project
# Purpose:
#   1. Import and clean hydrochemical data.
#   2. Classify samples by river and season.
#   3. Convert major ions from mg/L to meq/L.
#   4. Calculate cation and anion percentages.
#   5. Calculate charge balance error.
#   6. Generate a Piper trilinear diagram using WQChartPy.
#   7. Export processed data and publication-quality figures.
#
# Input:
#   CSV file containing major ion concentrations in mg/L.
#
# Output:
#   - Piper_Diagram.png
#   - Piper_Diagram.pdf
#   - Hydrochemical_Processed_Data.csv
#   - Charge_Balance_Report.csv
# =============================================================================


# =============================================================================
# 1. IMPORT LIBRARIES
# =============================================================================

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from wqchartpy import triangle_piper

warnings.filterwarnings("ignore")


# =============================================================================
# 2. PROJECT CONFIGURATION
# =============================================================================

INPUT_FILE = "finaldata A2.csv"

OUTPUT_DIR = "outputs"
FIGURE_DIR = "figures"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)

FIGURE_NAME = "Piper_Diagram"

DPI = 300

# River classification
RIVER_NAMES = {
    "SK": "Sirsiya",
    "BK": "Bagmati",
    "GK": "Guang"
}

# Marker customization
RIVER_MARKERS = {
    "Sirsiya": "^",
    "Bagmati": "s",
    "Guang": "D"
}


# =============================================================================
# 3. DEFINE REQUIRED INPUT COLUMNS
# =============================================================================

REQUIRED_COLUMNS = [
    "Sample code",
    "Calcium (mg/l)",
    "Magnesium (mg/l)",
    "Na (mg/l)",
    "K (mg/l)",
    "HCO3 (mg/l)",
    "SO4 (mg/l)",
    "Chloride (mg/l)"
]


# =============================================================================
# 4. DATA IMPORT
# =============================================================================

def load_data(file_path):

    print("\n" + "=" * 70)
    print("PIPER DIAGRAM - HYDROCHEMICAL DATA ANALYSIS")
    print("=" * 70)

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    try:
        df = pd.read_csv(file_path, encoding="latin-1")
    except Exception:
        df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip()

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns:\n"
            + "\n".join(missing_columns)
        )

    print(f"\nTotal samples imported: {len(df)}")

    return df


# =============================================================================
# 5. DATA CLEANING
# =============================================================================

def clean_data(df):

    df = df.copy()

    numeric_columns = [
        "Calcium (mg/l)",
        "Magnesium (mg/l)",
        "Na (mg/l)",
        "K (mg/l)",
        "HCO3 (mg/l)",
        "SO4 (mg/l)",
        "Chloride (mg/l)"
    ]

    # Additional optional columns
    optional_columns = [
        "Total Hardness (mg/l)",
        "Calcium Hardness (mg/l)",
        "Magnesium Hardness(mg/l )",
        "Total iron (mg/l)",
        "Ammonia( mg/l)*"
    ]

    for col in optional_columns:
        if col in df.columns:
            numeric_columns.append(col)

    for col in numeric_columns:

        df[col] = (
            df[col]
            .replace(
                {
                    "ND": np.nan,
                    "0:02": "0.02",
                    "1.9 0.3": "1.9"
                }
            )
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Remove invalid or negative major-ion concentrations
    ion_columns = [
        "Calcium (mg/l)",
        "Magnesium (mg/l)",
        "Na (mg/l)",
        "K (mg/l)",
        "HCO3 (mg/l)",
        "SO4 (mg/l)",
        "Chloride (mg/l)"
    ]

    for col in ion_columns:
        df.loc[df[col] < 0, col] = np.nan

    # Identify river
    df["Sample code"] = df["Sample code"].astype(str).str.strip()

    df["River_Code"] = (
        df["Sample code"]
        .str.extract(r"([A-Z]+)", expand=False)
    )

    df["River"] = df["River_Code"].map(RIVER_NAMES)

    # Identify season
    df["Season"] = np.where(
        df["Sample code"].str.contains(
            r"\(M\)",
            case=False,
            regex=True,
            na=False
        ),
        "Monsoon",
        "Non-Monsoon"
    )

    print("\nRiver classification:")
    print(df["River"].value_counts(dropna=False))

    print("\nSeason classification:")
    print(df["Season"].value_counts(dropna=False))

    return df


# =============================================================================
# 6. CONVERT MG/L TO MEQ/L
# =============================================================================

def prepare_piper_data(df):

    df = df.copy()

    # Cation conversion factors
    df["Ca_meq"] = df["Calcium (mg/l)"] / 20.04

    df["Mg_meq"] = df["Magnesium (mg/l)"] / 12.15

    df["Na_meq"] = df["Na (mg/l)"] / 22.99

    df["K_meq"] = df["K (mg/l)"] / 39.10

    # Anion conversion factors
    df["HCO3_meq"] = df["HCO3 (mg/l)"] / 61.02

    # Carbonate assumed zero unless measured data are available.
    df["CO3_meq"] = 0.0

    df["SO4_meq"] = df["SO4 (mg/l)"] / 48.03

    df["Cl_meq"] = df["Chloride (mg/l)"] / 35.45

    # Total cations
    df["Total_cations"] = (
        df["Ca_meq"]
        + df["Mg_meq"]
        + df["Na_meq"]
        + df["K_meq"]
    )

    # Total anions
    df["Total_anions"] = (
        df["HCO3_meq"]
        + df["CO3_meq"]
        + df["SO4_meq"]
        + df["Cl_meq"]
    )

    # Calculate cation percentages
    for ion in ["Ca", "Mg", "Na", "K"]:

        df[f"{ion}_pct"] = (
            df[f"{ion}_meq"]
            / df["Total_cations"]
        ) * 100

    # Calculate anion percentages
    for ion in ["HCO3", "CO3", "SO4", "Cl"]:

        df[f"{ion}_pct"] = (
            df[f"{ion}_meq"]
            / df["Total_anions"]
        ) * 100

    # Calculate TDS from major ion concentrations
    df["TDS_calc"] = (
        df["Calcium (mg/l)"]
        + df["Magnesium (mg/l)"]
        + df["Na (mg/l)"]
        + df["K (mg/l)"]
        + df["HCO3 (mg/l)"]
        + df["SO4 (mg/l)"]
        + df["Chloride (mg/l)"]
    )

    # Charge balance error (%)
    denominator = df["Total_cations"] + df["Total_anions"]

    df["CBE_percent"] = np.where(
        denominator > 0,
        (
            (df["Total_cations"] - df["Total_anions"])
            / denominator
        ) * 100,
        np.nan
    )

    return df


# =============================================================================
# 7. QUALITY CONTROL
# =============================================================================

def quality_control(df):

    df = df.copy()

    essential_columns = [
        "Ca_pct",
        "Mg_pct",
        "Na_pct",
        "K_pct",
        "HCO3_pct",
        "CO3_pct",
        "SO4_pct",
        "Cl_pct"
    ]

    valid_mask = (
        df[essential_columns].notna().all(axis=1)
        & (df["Total_cations"] > 0)
        & (df["Total_anions"] > 0)
    )

    valid_df = df.loc[valid_mask].copy()

    print("\n" + "=" * 70)
    print("QUALITY CONTROL REPORT")
    print("=" * 70)

    print(f"Original samples: {len(df)}")
    print(f"Valid samples: {len(valid_df)}")
    print(f"Excluded samples: {len(df) - len(valid_df)}")

    print("\nCharge Balance Error:")
    print(valid_df["CBE_percent"].describe())

    # Common screening criterion; retain the actual values
    # so users can choose their own scientifically justified threshold.
    valid_df["CBE_acceptable_5pct"] = (
        valid_df["CBE_percent"].abs() <= 5
    )

    print(
        "\nSamples within ±5% charge balance error:",
        valid_df["CBE_acceptable_5pct"].sum()
    )

    print(
        "Samples outside ±5% charge balance error:",
        (~valid_df["CBE_acceptable_5pct"]).sum()
    )

    return valid_df


# =============================================================================
# 8. PREPARE WQCHARTPY INPUT
# =============================================================================

def create_wqchartpy_dataframe(df):

    piper_data = pd.DataFrame({

        "Label": df["Sample code"],

        # Original concentrations in mg/L
        "Ca": df["Calcium (mg/l)"],
        "Mg": df["Magnesium (mg/l)"],
        "Na": df["Na (mg/l)"],
        "K": df["K (mg/l)"],

        "HCO3": df["HCO3 (mg/l)"],

        # Carbonate assumption
        "CO3": 0.0,

        "SO4": df["SO4 (mg/l)"],
        "Cl": df["Chloride (mg/l)"],

        "TDS": df["TDS_calc"]

    })

    # WQChartPy category grouping
    piper_data["Category"] = df["River"].values

    # Preserve seasonal metadata
    piper_data["Season"] = df["Season"].values

    # River-specific marker styles
    piper_data["Marker"] = (
        piper_data["Category"]
        .map(RIVER_MARKERS)
    )

    piper_data["Size"] = 80

    piper_data["Alpha"] = 0.8

    # Reset index
    piper_data = piper_data.reset_index(drop=True)

    return piper_data


# =============================================================================
# 9. GENERATE PIPER DIAGRAM
# =============================================================================

def generate_piper_diagram(piper_data):

    print("\nGenerating Piper diagram...")

    # Create a copy
    plot_data = piper_data.copy()

    # Prevent individual sample labels from cluttering the plot
    plot_data["Label"] = ""

    output_file = os.path.join(
        FIGURE_DIR,
        FIGURE_NAME
    )

    # Pass original concentrations in mg/L.
    # WQChartPy performs the ionic conversion internally.
    triangle_piper.plot(
        plot_data,
        unit="mg/L",
        figname=output_file,
        figformat="png"
    )

    print("\nPiper diagram generated successfully.")

    print(f"Output: {output_file}.png")


# =============================================================================
# 10. EXPORT RESULTS
# =============================================================================

def export_results(df):

    processed_file = os.path.join(
        OUTPUT_DIR,
        "Hydrochemical_Processed_Data.csv"
    )

    cbe_file = os.path.join(
        OUTPUT_DIR,
        "Charge_Balance_Report.csv"
    )

    df.to_csv(
        processed_file,
        index=False
    )

    df[
        [
            "Sample code",
            "River",
            "Season",
            "Total_cations",
            "Total_anions",
            "CBE_percent",
            "CBE_acceptable_5pct"
        ]
    ].to_csv(
        cbe_file,
        index=False
    )

    print("\nExport completed:")
    print(processed_file)
    print(cbe_file)


# =============================================================================
# 11. MAIN EXECUTION
# =============================================================================

def main():

    # Import data
    df = load_data(INPUT_FILE)

    # Clean data
    df = clean_data(df)

    # Convert concentrations and calculate percentages
    df = prepare_piper_data(df)

    # Quality control
    df_piper = quality_control(df)

    if len(df_piper) == 0:
        raise ValueError(
            "No valid samples available for Piper diagram."
        )

    # Prepare plotting data
    piper_data = create_wqchartpy_dataframe(df_piper)

    # Generate Piper diagram
    generate_piper_diagram(piper_data)

    # Export processed data
    export_results(df_piper)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()
