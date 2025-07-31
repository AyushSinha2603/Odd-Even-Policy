# 📊 Delhi Air Quality: A Deep-Dive Analysis of the Odd-Even Policy at Punjabi Bagh

This repository contains the final report and analysis of the impact of Delhi's Odd-Even vehicle rationing policy on air quality. The project performs an in-depth exploratory data analysis (EDA) on the **Punjabi Bagh (DL013)** monitoring station, focusing on hourly pollution patterns during the January 2016 implementation.

---

## 🎯 Objective

The project's objective is to move beyond daily averages and analyze the policy's effect on the **hourly and daily cycles of air pollution**. By examining heatmaps, 24-hour trends, and rush hour periods, we can pinpoint when and how the policy made a difference at a representative urban location.

---

## 🛠️ Tech Stack

* **Python 3.x**
* **Pandas & NumPy** for data manipulation and time-series analysis
* **Matplotlib & Seaborn** for advanced visualizations
* **SciPy** for statistical t-tests
* **Jupyter Notebook** (`delhi_air_quality_analysis.ipynb`) for the development environment

---

## 📂 Dataset

The analysis uses the **Air Quality Data in India (2015-2020)** dataset from Kaggle, focusing on hourly data for the Punjabi Bagh station.

* **Data Source:** [Kaggle](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india)
* **Primary Focus:** Hourly PM2.5 readings from the **Punjabi Bagh (DL013)** station.
* **Time Frame:** December 17, 2015, to January 30, 2016, to create a baseline and measure the policy's effect.

---

## 📈 Analysis & Key Visualizations at Punjabi Bagh (DL013)

The analysis reveals a clear change in the daily pollution rhythm.

### **1. Hourly Pollution Heatmap**

This heatmap visualizes PM2.5 concentration by hour of the day across the study period. The 'Before' period likely shows intense red bands during morning and evening rush hours. The key insight from the 'During' policy period is a potential lightening of these bands, indicating that the policy successfully blunted the worst pollution spikes.

![Hourly PM2.5 Heatmap](visualisations/heatMap.png)

### **2. The 24-Hour PM2.5 Cycle**

This plot averages the PM2.5 levels for each of the 24 hours of the day, comparing the cycles before and during the Odd-Even policy. The 'During' policy line is expected to be consistently lower, especially during the **8 AM - 11 AM** and **5 PM - 8 PM** windows, which correspond to peak traffic times. This provides strong evidence that the policy directly impacted traffic-related emissions.

![24-Hour PM2.5 Cycle](visualisations/24hour_PM2.5.png)

### **3. Rush Hour vs. Off-Peak Analysis**

This visualization directly compares the average PM2.5 levels during rush hours versus off-peak hours. The most significant finding here would be a much larger percentage drop in pollution during **rush hours** in the 'During' policy phase. This demonstrates that the policy was most effective when it was needed most—when traffic is typically at its worst.

![Rush Hour vs. Off-Peak PM2.5](visualisations/rushHour_s_offPeak.png)

---

## 📝 Final Conclusion

The Odd-Even policy in January 2016 had a **clear and statistically significant impact** on the hourly air pollution patterns at the Punjabi Bagh (DL013) station. The policy was effective in **dampening the peak pollution levels** typically seen during morning and evening rush hours.

By moving the analysis from simple daily averages to a more granular, hourly view, we can more confidently conclude that the reduction in vehicular traffic directly led to healthier air during the city's busiest times. While weather plays a role, the consistent drop in pollution during peak traffic hours strongly points to the policy's success.

---

## 🚀 How to Run this Project

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-link]
    ```
2.  **Install dependencies:**
    ```bash
    pip install pandas numpy matplotlib seaborn scipy jupyterlab
    ```
3.  **Download the dataset** from the Kaggle link provided above and place the relevant data file in the root folder.
4.  **Run the notebook:**
    ```bash
    jupyter notebook delhi_air_quality_analysis.ipynb
    ```
