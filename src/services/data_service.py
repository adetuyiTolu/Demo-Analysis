import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import os


class DataService:
    def __init__(self):
        self.input_file = "../data/raw/raw.csv"
        self.output_file = "../data/interim/output.csv"
        self.data = None
        self.report = None

    def load_data(self):
        self.data = pd.read_csv(self.input_file)

    def process_data(self):
        self.data["total"] = self.data["quantity"] * self.data["price"]

    def export_data(self):
        self.data.to_csv(self.output_file, index=False)

    def generate_report(self):
        report = (
            self.data.groupby("product")
            .agg({"quantity": "sum", "total": "sum"})
            .reset_index()
        )
        report["avg_price"] = report["total"] / report["quantity"]
        self.report = report
        report.to_csv("../data/processed/report.csv")
        print("Sales report generated: data/report.csv")

    def config_plot_style(self):
        """mpl.style.use("seaborn")"""
        mpl.rcParams["figure.dpi"] = 200

    def generate_chart(self):
        self.config_plot_style()
        report = pd.read_csv("../data/processed/report.csv")
        products = report["product"]
        total_sales = report["total"]

        plt.figure(figsize=(8, 6))
        plt.bar(products, total_sales)
        plt.xlabel("Product")
        plt.ylabel("Total Sales")
        plt.title("Sales by Product")
        plt.tight_layout()
        plt.savefig("../reports/figures/sales_chart.png")
        print("Sales chart generated: figures/sales_chart.png")

    def run(self):
        """print(os.getcwd())"""
        self.load_data()
        self.process_data()
        self.export_data()
        self.generate_report()
        self.generate_chart()
        print(f"Data successfuly processed and exported to{self.output_file}")
