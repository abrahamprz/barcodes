from barcode_pdf import BarcodePDF


def main():
    columns_to_replace = ["DepartmentTag", "PersonID"]
    barcode_pdf = BarcodePDF("example.csv")
    barcode_pdf.generate_pdf(barcode_columns=columns_to_replace)


if __name__ == "__main__":
    main()
