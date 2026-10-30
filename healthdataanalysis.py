"""
CSV files must contain patient_id, age, gender, systolic_bp, and cholesterol.
The optional test_result column is retained when present. This project is for
data-analysis demonstration only and does not provide medical advice.
"""

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


REQUIRED_COLUMNS = (
    "patient_id",
    "age",
    "gender",
    "systolic_bp",
    "cholesterol",
)
NUMERIC_COLUMNS = ("age", "systolic_bp", "cholesterol")


def generate_demo_records(count=200, seed=42):
    """Create reproducible synthetic records; no real patient data is used."""
    rng = np.random.default_rng(seed)
    ages = np.clip(rng.normal(48, 17, count), 18, 90).round()
    systolic_bp = (108 + 0.48 * ages + rng.normal(0, 13, count)).round()
    cholesterol = (
        155 + 0.55 * ages + 0.18 * (systolic_bp - 120) + rng.normal(0, 25, count)
    ).round()
    genders = rng.choice(("Female", "Male", "Other"), count, p=(0.49, 0.48, 0.03))
    test_results = rng.choice(
        ("Normal", "Abnormal", "Inconclusive"), count, p=(0.72, 0.2, 0.08)
    )

    return [
        {
            "patient_id": f"DEMO-{index + 1:04d}",
            "age": age,
            "gender": gender,
            "systolic_bp": bp,
            "cholesterol": chol,
            "test_result": result,
        }
        for index, (age, gender, bp, chol, result) in enumerate(
            zip(ages, genders, systolic_bp, cholesterol, test_results)
        )
    ]


def load_csv(path):
    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames or []
        missing_columns = [name for name in REQUIRED_COLUMNS if name not in fieldnames]
        if missing_columns:
            raise ValueError(
                f"CSV is missing required columns: {', '.join(missing_columns)}"
            )
        return list(reader)


def clean_records(records):
    """Drop rows with missing, non-numeric, or out-of-range measurements."""
    numeric = {
        name: np.array(
            [
                _to_float(record.get(name))
                for record in records
            ],
            dtype=float,
        )
        for name in NUMERIC_COLUMNS
    }
    valid = np.ones(len(records), dtype=bool)
    for values in numeric.values():
        valid &= np.isfinite(values)

    valid &= (numeric["age"] >= 0) & (numeric["age"] <= 120)
    valid &= (numeric["systolic_bp"] >= 60) & (numeric["systolic_bp"] <= 300)
    valid &= (numeric["cholesterol"] >= 50) & (numeric["cholesterol"] <= 600)

    cleaned = []
    for index, record in enumerate(records):
        if not valid[index]:
            continue
        cleaned.append(
            {
                "patient_id": str(record.get("patient_id", "")).strip(),
                "age": float(numeric["age"][index]),
                "gender": str(record.get("gender", "")).strip() or "Unknown",
                "systolic_bp": float(numeric["systolic_bp"][index]),
                "cholesterol": float(numeric["cholesterol"][index]),
                "test_result": str(record.get("test_result", "")).strip() or "Unknown",
            }
        )
    return cleaned


def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return np.nan


def save_cleaned_csv(records, path):
    columns = (*REQUIRED_COLUMNS, "test_result")
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(records)


def create_visualizations(records, output_path, show=True):
    ages = np.array([record["age"] for record in records])
    systolic_bp = np.array([record["systolic_bp"] for record in records])
    cholesterol = np.array([record["cholesterol"] for record in records])
    genders, gender_counts = np.unique(
        [record["gender"] for record in records], return_counts=True
    )
    test_results, test_counts = np.unique(
        [record["test_result"] for record in records], return_counts=True
    )

    figure, axes = plt.subplots(3, 2, figsize=(12, 14))
    figure.suptitle("Health Data Analysis (de-identified/demo data)", fontsize=16)

    axes[0, 0].hist(ages, bins=12, color="steelblue", edgecolor="white")
    axes[0, 0].set(title="Patient age distribution", xlabel="Age (years)", ylabel="Patients")

    axes[0, 1].bar(genders, gender_counts, color="cadetblue")
    axes[0, 1].set(title="Patient demographics by gender", xlabel="Gender", ylabel="Patients")

    axes[1, 0].scatter(ages, systolic_bp, alpha=0.7, color="darkorange")
    axes[1, 0].set(
        title="Age vs. systolic blood pressure",
        xlabel="Age (years)",
        ylabel="Systolic blood pressure (mmHg)",
    )

    axes[1, 1].scatter(ages, cholesterol, alpha=0.7, color="seagreen")
    axes[1, 1].set(
        title="Age vs. cholesterol",
        xlabel="Age (years)",
        ylabel="Cholesterol (mg/dL)",
    )

    axes[2, 0].scatter(systolic_bp, cholesterol, alpha=0.7, color="mediumpurple")
    axes[2, 0].set(
        title="Systolic blood pressure vs. cholesterol",
        xlabel="Systolic blood pressure (mmHg)",
        ylabel="Cholesterol (mg/dL)",
    )

    axes[2, 1].bar(test_results, test_counts, color="slategray")
    axes[2, 1].set(title="Test result categories", xlabel="Test result", ylabel="Patients")
    axes[2, 1].tick_params(axis="x", rotation=20)

    for axis in axes.flat:
        axis.grid(axis="y", alpha=0.2)
    figure.tight_layout(rect=(0, 0, 1, 0.97))
    figure.savefig(output_path, dpi=150)
    if show:
        plt.show()
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser(
        description="Clean health records with NumPy and plot patient demographics."
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="CSV input (otherwise reproducible synthetic demo data is used)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("cleaned_health_data.csv"),
        help="path for the cleaned CSV (default: cleaned_health_data.csv)",
    )
    parser.add_argument(
        "--plot",
        type=Path,
        default=Path("health_analysis.png"),
        help="path for the analysis chart (default: health_analysis.png)",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="save the chart without opening a window",
    )
    args = parser.parse_args()

    records = load_csv(args.input) if args.input else generate_demo_records()
    cleaned = clean_records(records)
    if not cleaned:
        raise ValueError("No valid records remain after cleaning.")

    save_cleaned_csv(cleaned, args.output)
    create_visualizations(cleaned, args.plot, show=not args.no_show)

    print(f"Records read: {len(records)}")
    print(f"Valid records: {len(cleaned)}")
    print(f"Records removed: {len(records) - len(cleaned)}")
    print(f"Cleaned data saved to: {args.output.resolve()}")
    print(f"Visualizations saved to: {args.plot.resolve()}")
    for left, right in (
        ("age", "systolic_bp"),
        ("age", "cholesterol"),
        ("systolic_bp", "cholesterol"),
    ):
        left_values = np.array([record[left] for record in cleaned])
        right_values = np.array([record[right] for record in cleaned])
        if (
            len(cleaned) < 2
            or np.std(left_values) == 0
            or np.std(right_values) == 0
        ):
            print(f"Correlation ({left}, {right}): not defined")
        else:
            correlation = np.corrcoef(left_values, right_values)[0, 1]
            print(f"Correlation ({left}, {right}): {correlation:.2f}")


if __name__ == "__main__":
    main()
