# Health Data Analysis and Visualization Using Python

## 📌 Project Overview

This project is a Python-based data analysis application designed to
clean, process, analyze, and visualize patient health records using
NumPy, Matplotlib, and CSV file handling.

The application processes health-related data such as patient age,
gender, systolic blood pressure, and cholesterol levels. It removes
invalid records, generates statistical insights, calculates correlations
between numerical attributes, and creates visual representations of the
cleaned data.

The project can work with either a user-provided CSV file or
automatically generated synthetic demo data.

**Note:** This project is developed for educational and data-analysis
demonstration purposes only. It does not provide medical advice or
perform medical diagnosis.

## ✨ Key Features

-   Synthetic Data Generation using NumPy.
-   CSV file import and export.
-   Automatic data cleaning and validation.
-   Removal of invalid or missing records.
-   Correlation analysis using NumPy.
-   Six data visualizations using Matplotlib.
-   Command-line support with Argparse.

## 🛠️ Technologies Used

  Technology   Purpose
  ------------ ------------------------
  Python       Programming Language
  NumPy        Data Processing
  Matplotlib   Visualization
  CSV          File Handling
  Argparse     Command-Line Interface
  Pathlib      File Management

## 📂 Project Structure

``` text
Health-Data-Analysis/
│
├── health_analysis.py
├── cleaned_health_data.csv
├── health_analysis.png
├── README.md
└── requirements.txt
```

## ⚙️ Installation

Clone the repository:

``` bash
git clone https://github.com/your-username/Health-Data-Analysis.git
cd Health-Data-Analysis
```

Install dependencies:

``` bash
pip install numpy matplotlib
```

Or use a `requirements.txt` file:

``` text
numpy
matplotlib
```

Then run:

``` bash
pip install -r requirements.txt
```

## ▶️ Usage

Run with demo data:

``` bash
python health_analysis.py
```

Run with your own CSV:

``` bash
python health_analysis.py --input patients.csv
```

Custom output files:

``` bash
python health_analysis.py --input patients.csv --output cleaned_data.csv --plot analysis.png
```

Run without opening the chart:

``` bash
python health_analysis.py --no-show
```

## 📊 Required CSV Format

  Column        Required
  ------------- ----------
  patient_id    Yes
  age           Yes
  gender        Yes
  systolic_bp   Yes
  cholesterol   Yes
  test_result   Optional

Example:

``` csv
patient_id,age,gender,systolic_bp,cholesterol,test_result
P001,25,Male,120,180,Normal
P002,35,Female,130,210,Abnormal
```

## 📈 Generated Visualizations

The program creates six charts:

1.  Patient Age Distribution
2.  Gender Distribution
3.  Age vs Systolic Blood Pressure
4.  Age vs Cholesterol
5.  Blood Pressure vs Cholesterol
6.  Test Result Distribution

## 🧹 Data Cleaning

The application:

-   Removes invalid or missing numeric values.
-   Validates age (0--120).
-   Validates systolic blood pressure (60--300).
-   Validates cholesterol (50--600).
-   Replaces missing gender and test result values with `"Unknown"`.

## 📉 Correlation Analysis

The application calculates Pearson correlations for:

-   Age vs Systolic Blood Pressure
-   Age vs Cholesterol
-   Systolic Blood Pressure vs Cholesterol

## 📁 Output Files

After execution, the following files are generated:

-   `cleaned_health_data.csv`
-   `health_analysis.png`

The terminal also displays:

-   Records read
-   Valid records
-   Removed records
-   Correlation values

## 🎯 Learning Outcomes

-   CSV file handling in Python
-   Data cleaning with NumPy
-   Data visualization with Matplotlib
-   Statistical correlation analysis
-   Command-line argument handling
-   Working with synthetic datasets

## 🔮 Future Improvements

-   Streamlit dashboard
-   Interactive charts
-   Additional file format support
-   Advanced analytics
-   Educational machine learning integration

## ⚠️ Disclaimer

This project is intended for educational purposes only. It uses
synthetic demo data by default and does not provide medical advice.

## 👨‍💻 Author

**Akshit Katoch**

MCA (Artificial Intelligence & Machine Learning)

Chandigarh University

------------------------------------------------------------------------

⭐ If you find this project useful, consider giving the repository a
star.
