import csv
from code128 import Code128
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.platypus import Image as PlatypusImage
from reportlab.lib.styles import getSampleStyleSheet


class BarcodePDF:
    """
    This class is used to generate a PDF from a CSV file, replacing certain columns with barcodes.
    """

    def __init__(self, filename: str) -> None:
        """
        Initialize the BarcodePDF instance.

        Args:
            filename (str): The path to the CSV file.
        """
        self.filename = filename

        # Register the Arial font
        pdfmetrics.registerFont(TTFont("Arial", "fonts/ARIAL.TTF"))
        pdfmetrics.registerFont(TTFont("Arial-Bold", "fonts/ARIALBD.TTF"))

        # Get a sample style sheet
        self.styles = getSampleStyleSheet()

        # Select the 'BodyText' style and reduce the font size
        self.normal_style = self.styles["BodyText"]
        self.normal_style.fontSize = 6  # Change to your desired size

    def generate_pdf(self, barcode_columns: list) -> list:
        """
        Generate a PDF from the CSV file, replacing the specified columns with barcodes.

        Args:
            barcode_columns (list): The columns to replace with barcodes.

        Returns:
            list: A list of missing columns, or an empty list if all columns were found.
        """
        # Create a list to store the table data
        data = []

        # Create a Code128 instance
        code128 = Code128()

        # Open the CSV file
        with open(self.filename, "r") as f:
            reader = csv.reader(f)
            headers = next(reader)  # Assume the first row is headers

            # Check if all specified columns exist in the CSV header
            missing_columns = [
                column for column in barcode_columns if column not in headers
            ]
            if missing_columns:
                return missing_columns

            for row in reader:
                # Replace the specified columns with barcode images, unless they contain '#N/A'
                row = [
                    PlatypusImage(code128.code128_image(data=cell))
                    if header in barcode_columns and "#N/A" not in cell
                    else Paragraph(cell, self.normal_style)
                    for header, cell in zip(headers, row)
                ]
                # Append each row to the table data
                data.append(row)

        # Create a document template
        doc = SimpleDocTemplate(
            f"{self.filename.split('.')[0]}_barcodes.pdf", pagesize=landscape(letter)
        )

        # Create a table with the data and add it to the document
        table = Table(data)
        elements = []
        elements.append(table)
        doc.build(elements)

        return []


# Usage:
# barcode_pdf = BarcodePDF("migrant.csv")
# barcode_pdf.generate_pdf()
