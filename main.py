from src.barcode_pdf import BarcodePDF


def main():
    columns_to_replace = ["DepartmentTag", "PersonID"]  # ["DepartmentTag", "PersonID"]
    barcode_pdf = BarcodePDF("examples/example.csv")
    missing_values = barcode_pdf.generate_pdf(barcode_columns=columns_to_replace)

    if missing_values:
        print(f"Missing columns: {missing_values}")


if __name__ == "__main__":
    main()
