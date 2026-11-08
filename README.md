# Evaluating Low-Cost PM2.5 Sensors: Calibration Accuracy, Generalization, and Reliability

## Project Overview

This research project evaluates the performance of low-cost PurpleAir PM2.5 sensors against reference monitoring measurements. It examines the accuracy of raw sensor measurements, the improvement achieved through calibration adjustments, and whether calibration performance remains consistent across different environmental and monitoring conditions.

The project uses two datasets:

- **Dataset A — 24-hour collocation:** Daily PurpleAir measurements collocated with reference monitors.
- **Dataset B — Hourly wildfire-smoke:** Hourly PurpleAir and reference monitor measurements, including different calibration and withholding configurations.

The analysis focuses on measurement agreement, calibration performance, temporal coverage, sensor-level variation, and generalization.

## Research Question

How much does calibration improve agreement between low-cost PurpleAir sensors and reference monitors, and does that improvement hold under wildfire-smoke conditions?

## Research Objectives

1. Characterize the distributions and data quality of low-cost PurpleAir measurements.
2. Evaluate agreement between raw PurpleAir measurements and reference monitor measurements.
3. Compare available calibration adjustments using appropriate error metrics.
4. Examine calibration performance across PM2.5 concentrations, relative humidity, time periods, and individual sensors.
5. Assess the limitations of available withholding configurations and their implications for generalization.
6. Develop an evaluation framework for further calibration and validation analysis.

## Repository Structure

```text
low-cost-pm25-calibration/
│
├── data/
│   ├── raw/                  # Downloaded datasets (not tracked by Git)
│   └── processed/            # Locally generated data (not tracked by Git)
│
├── notebooks/
│   ├── 01_data_profile.ipynb
│   ├── 02_analytical_decisions.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   └── 04_calibration_and_evaluation.ipynb  # Planned
│
├── reports/
│   └── figures/              # Generated research figures
│
├── src/
│   └── download_data.py      # Dataset download and preparation
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Datasets and Sources

All raw datasets are excluded from this GitHub repository because of their size and to maintain consistent data preparation.

The download script retrieves the required datasets from their original sources.

### Dataset A — 24-hour Collocation

**Main file:** `Full24hrdataset.csv`

**Source:** EPA Pasteur Repository

Original archive:

https://pasteur.epa.gov/uploads/10.23719/1522388/Data_DevelopmentUSPAcorrection_210408.zip

Expected local location:

```text
data/raw/24hr_collocation/Full24hrdataset.csv
```

### Dataset B — Hourly Wildfire-Smoke

**Main file:** `Finaldataset_correcteddatasetwholding_10_26_22.csv`

**Source:** EPA Pasteur Repository

Original archive:

https://pasteur.epa.gov/uploads/10.23719/1528138/Dataset_PurpleAirSmoke_Barkjohn_3_15_23.zip

Expected local location:

```text
data/raw/hourly_smoke/Finaldataset_correcteddatasetwholding_10_26_22.csv
```

### Dataset C — EPA AQS Monitor Listing

**Main file:** `aqs_monitors.csv`

**Source:** EPA AirData

Download source:

https://aqs.epa.gov/aqsweb/airdata/aqs_monitors.zip

Expected local location:

```text
data/raw/aqs_monitors.csv
```

The download script extracts the required CSV from the EPA ZIP archive.

### Dataset D — EPA Daily PM2.5 Measurements

**Parameter:** PM2.5 (Parameter Code 88101)

**Source:** EPA AirData

Required annual ZIP files:

| Year | Download |
|---|---|
| 2018 | https://aqs.epa.gov/aqsweb/airdata/daily_88101_2018.zip |
| 2019 | https://aqs.epa.gov/aqsweb/airdata/daily_88101_2019.zip |
| 2020 | https://aqs.epa.gov/aqsweb/airdata/daily_88101_2020.zip |

Expected local locations:

```text
data/raw/
├── daily_88101_2018.zip
├── daily_88101_2019.zip
└── daily_88101_2020.zip
```

These ZIP archives are retained without extraction by the download script. Notebook 02 handles archive inspection and extraction as required by the analysis.

## Installation and Environment Setup

### 1. Install Python

Install Python 3.12.x.

Download:

https://www.python.org/downloads/

Verify your installation:

```bash
python --version
```

### 2. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/low-cost-pm25-calibration.git
```

Navigate into the project directory:

```bash
cd low-cost-pm25-calibration
```

### 3. Create a virtual environment

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 4. Install dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install all required project dependencies:

```bash
python -m pip install -r requirements.txt
```

The requirements file includes the scientific computing, visualization, document processing, and Jupyter packages needed by the project.

### 5. Download and prepare datasets

From the project root, execute:

```bash
python src/download_data.py
```

The script:

- Downloads missing datasets from their configured sources.
- Reuses existing nonempty local datasets.
- Validates downloaded ZIP archives.
- Extracts the required PurpleAir CSV files.
- Extracts the AQS monitor listing.
- Downloads and validates the three EPA daily PM2.5 ZIP archives without extracting them.

All downloaded datasets remain under `data/raw/` and are excluded from Git.

## Running the Notebooks

Execute the notebooks in the following order:

| Order | Notebook | Purpose |
|---|---|---|
| 1 | `01_data_profile.ipynb` | Dataset profiling and initial data inspection |
| 2 | `02_analytical_decisions.ipynb` | Analytical decisions, data interpretation, and supporting checks |
| 3 | `03_exploratory_data_analysis.ipynb` | Exploratory analysis of both research datasets |
| 4 | `04_calibration_and_evaluation.ipynb` | Planned calibration and evaluation analysis |

Open the project in VS Code or JupyterLab and run the notebooks in sequence.

For relative paths used by the notebooks, ensure the notebook working directory is the `notebooks/` directory.

To launch JupyterLab from the project root:

```bash
cd notebooks
jupyter lab
```

## Reproducibility

The project is organized to support reproducible analysis.

- Python dependencies are documented in `requirements.txt`.
- Raw datasets are downloaded through `src/download_data.py`.
- Original downloaded datasets are kept separate from analysis outputs.
- Raw and processed data are excluded from Git.
- Analysis notebooks are maintained in execution order.
- Generated research figures are stored under `reports/figures/`.

The download script skips existing nonempty files. If an existing local dataset is incomplete or corrupted, remove that file before rerunning the script.

For reproducibility, use the documented Python version and dependency file, preserve the original downloaded datasets, and execute notebooks in the specified order.

## Research Scope and Limitations

The exploratory analysis is descriptive and does not, by itself, establish that a calibration method will generalize to all sensors, locations, or wildfire-smoke events.

The interpretation of calibration performance must account for:

- Differences in PM2.5 concentration ranges.
- Relative humidity and environmental conditions.
- Temporal coverage and missing observations.
- Repeated observations from individual sensors.
- Differences between withholding configurations.
- The distinction between published calibration outputs and independently trained models.

Further calibration, validation, and generalization analysis will be documented in the subsequent modeling notebook.

## Project Status

| Component | Status |
|---|---|
| Dataset profiling | Completed |
| Analytical decisions | Completed |
| Exploratory data analysis | Completed |
| Download automation | Implemented |
| Dependency documentation | Implemented and tested in a clean environment |
| Calibration and evaluation | Upcoming |

## Acknowledgments and Data Attribution

This project uses publicly available PurpleAir and U.S. Environmental Protection Agency (EPA) datasets.

Original dataset sources and download locations are documented above. Please consult the original data providers' documentation and applicable terms when using or redistributing the data.

---

**Research Project:** Evaluating Low-Cost PM2.5 Sensors: Calibration Accuracy, Generalization, and Reliability

**Repository:** `low-cost-pm25-calibration`
