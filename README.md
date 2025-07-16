# 🐦 Mini-Project-2
**Project Title**: *Bird Species Observation Analysis*

---

**Domain:** Environmental Studies, Biodiversity Conservation, Ecology
**Tools Used:** Streamlit, Pandas, Plotly, SQL, Jupyter Notebook

---

## 🚀 Project Description

This project focuses on analyzing the distribution, diversity, and environmental behavior of bird species across two ecosystems: **forests** and **grasslands**. Using observational data and environmental metrics, the dashboard aims to uncover ecological insights that can support conservation strategies and biodiversity studies.

---

## 🎯 Problem Statement

To analyze bird species observations across forest and grassland ecosystems and identify:
- Habitat-specific trends in species behavior and diversity
- The impact of environmental conditions on sightings
- Conservation patterns through watchlist and stewardship data

---

## 🧭 Approach

### 1. Data Cleaning & Preprocessing
- Handle missing values
- Standardize data columns (species, time, weather)
- Merge forest and grassland data into a unified structure

### 2. Exploratory Data Analysis (EDA)
- **Temporal Trends:** Year, Month, Season, Hour
- **Spatial Analysis:** Location Type, Plot Name
- **Species Patterns:** Common Names, ID Method, Sex Ratio

### 3. 📊 Data Visualization
- Build an interactive dashboard using **Streamlit & Plotly** to explore:
  - 📅 Heatmaps for month-wise and hour-wise sightings  
  - 🕊️ Top 10 observed species  
  - 🌡️ Bird sightings vs. temperature/humidity correlation  
  - 🧍‍♂️ Observer vs. Location heatmaps  
  - 📌 Distance-based species behavior analysis  
  - 🛑 Pie charts for Watchlist/Stewardship overlap  
  - 🗂️ Interactive filters (species, month, gender, location, etc.)

---

## 📊 Types of Analysis

| Type              | Description |
|-------------------|-------------|
| **Temporal**       | Bird activity over months, seasons, and hours |
| **Spatial**        | Location Type, Plot-level observation density |
| **Behavioral**     | Distance, Flyovers, Activity methods |
| **Environmental**  | Effects of weather: temperature, humidity, sky, wind |
| **Conservation**   | Focus on Watchlist & Regional species |
| **Observer Trends**| Biases and contribution patterns |

---

## 📂 Project Structure

- `db_config.py` — Database connection setup (MySQL)
- `streamlit_app.py` — Main Streamlit app for visualization
- `Bird_data_grassland_and_forest.ipynb` — Jupyter Notebook for preprocessing & MySQL data insertion
- `data/` — Folder containing `.xlsx` and `.csv` files used
- `requirements.txt` — Python dependencies

---

## 🚀 How to Run
1. Clone the repo
2. Activate virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run app: `streamlit run streamlit_app.py`





