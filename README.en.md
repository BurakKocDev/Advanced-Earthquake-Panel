<div align="center">

# Advanced Earthquake Panel

### An interactive Streamlit dashboard for global earthquake records from 1900 to 2025

[Türkçe](README.md) · English

![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-Data%20Analysis-3776AB?logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-DBSCAN-F7931E?logo=scikitlearn&logoColor=white)
![USGS Data](https://img.shields.io/badge/Data-USGS%20Earthquakes-2E7D32)

</div>

---

## Overview

**Advanced Earthquake Panel** is a Streamlit application that filters large-scale global earthquake records by date and magnitude and presents their geographic distribution, density, annual frequency, and cumulative seismic-energy indicator through interactive visualizations.

The project was designed around the **Earthquakes Around the World from 1900–2025** dataset, described as containing approximately 4.3 million records. Earthquake locations are displayed together with tectonic-plate boundaries, while an optional DBSCAN view provides an exploratory analysis of dense seismic-location clusters.

---

## Key Features

### Interactive Filtering

- Start and end date selection
- Minimum and maximum magnitude filtering
- Filtered-record count
- Sampling of up to 50,000 map points to protect browser performance on large result sets

### Geographic Visualization

- Global scatter map with marker size and color based on magnitude
- Earthquake-density map
- Tectonic-plate boundaries loaded from GeoJSON
- Interactive hover information for location, depth, time, and magnitude

### Exploratory Clustering

- DBSCAN with the Haversine distance metric
- Geographic coordinates transformed to radians
- Dense seismic regions visualized with cluster labels
- Outlying observations marked as noise

### Statistical and Temporal Analysis

- Annual earthquake frequency
- Cumulative seismic-energy indicator over time
- Charts that update according to the selected date and magnitude filters

---

## Analysis Approach

### DBSCAN Clustering

The application runs DBSCAN on the earthquake coordinates selected for map display using:

```text
metric      = haversine
eps         = 0.03 radians
min_samples = 25
```

This approach groups geographically close and dense earthquake observations. The output is an exploratory view of spatial-density patterns, not a scientific confirmation of geological fault lines.

### Cumulative Energy Indicator

The application calculates a relative energy value using:

```text
relative_energy = 10^(1.5 × magnitude)
```

Records are sorted by time and the cumulative sum is plotted. The chart helps compare the relative influence of large events within the selected interval; it is not a calibrated physical-energy measurement or a direct Benioff-strain calculation.

---

## Data Sources

### Earthquake Dataset

The project was designed for the following Kaggle dataset:

```text
Earthquakes Around the World from 1900–2025
```

The approximately 2 GB `Earthquakes_USGS.csv` file is not included in the repository because of GitHub file-size limits.

Expected core columns:

```text
time
latitude
longitude
mag
depth
place
```

During loading, the application renames:

- `latitude` to `lat`
- `longitude` to `lon`
- `mag` to `magnitude`

It then removes records with invalid time, location, magnitude, or depth values.

### Tectonic Plate Data

Plate boundaries are downloaded at runtime from this public GeoJSON resource:

```text
https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json
```

An internet connection is therefore required for the tectonic-plate layer.

---

## Technology Stack

- **Python**
- **Streamlit**
- **Pandas**
- **NumPy**
- **Plotly**
- **Plotly Express**
- **scikit-learn**
- **GeoJSON**
- **USGS-based earthquake data**

---

## Project Structure

```text
Advanced-Earthquake-Panel/
├── app.py
├── requirements.txt
└── README.md
```

Add the dataset locally as follows:

```text
Advanced-Earthquake-Panel/
├── Earthquakes_USGS.csv
├── app.py
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/BurakKocDev/Advanced-Earthquake-Panel.git
cd Advanced-Earthquake-Panel
```

### 2. Add the dataset

Locate the `Earthquakes Around the World from 1900–2025` dataset on Kaggle and place `Earthquakes_USGS.csv` in the same directory as `app.py`.

### 3. Update the CSV path

Replace the old machine-specific path in `app.py`:

```python
FILE_PATH = r"C:\Users\ASUS\Desktop\TezCalismalar\Earthquakes\Earthquakes_USGS.csv"
```

with a relative path:

```python
FILE_PATH = "Earthquakes_USGS.csv"
```

### 4. Install dependencies

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

---

## Performance Notes

- Loading the entire dataset may require substantial memory.
- Date parsing and cleaning may take several minutes during the first run.
- Map rendering is limited to 50,000 points, while statistical charts use the full filtered dataset.
- DBSCAN runs on the sampled dataset selected for visualization.
- Repeated data and GeoJSON loads benefit from Streamlit caching.

---

## Limitations

- The earthquake dataset is not included and must be downloaded separately.
- The default CSV path in the source code is machine-specific.
- The tectonic-plate layer depends on an external internet resource.
- Random sampling means the exact map points may differ between runs.
- DBSCAN clusters must not be interpreted as direct validation of geological faults or tectonic structures.
- The relative-energy formula is not a calibrated physical-energy calculation.
- The application is not a real-time earthquake alert, risk-prediction, or early-warning system.
- This project was developed for learning, data analysis, and portfolio purposes.

---

## Goal

Advanced Earthquake Panel combines large-scale geospatial data cleaning, filtering, interactive visualization, and exploratory machine-learning analysis in a single web dashboard.
