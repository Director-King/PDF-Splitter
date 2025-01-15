import PyPDF2
import pandas as pd

def split_pdf_by_csv(pdf_path, csv_path, encoding='latin-1'):
    """
    Splits a PDF document into multiple files based on instructions in a CSV.

    Args:
        pdf_path (str): Path to the input PDF file.
        csv_path (str): Path to the CSV file with instructions.
        The CSV file should have two columns:
            - "No.": Starting page number (inclusive).
            - "Names": Desired name for the new PDF file.
        encoding (str, optional): Encoding to use when reading the CSV file. Defaults to 'latin-1'.

    Returns:
        None
    """

    pdf_reader = PyPDF2.PdfReader(pdf_path)
    try:
        # Try reading the CSV with the specified encoding
        df = pd.read_csv(csv_path, encoding=encoding)
    except UnicodeDecodeError:
        # If decoding with 'latin-1' fails, try 'utf-8' as a fallback
        print("Error: Unable to decode CSV using latin-1. Trying utf-8...")
        df = pd.read_csv(csv_path, encoding='utf-8')

    # Check if the required columns exist in the DataFrame
    required_columns = ['No.', 'Names']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Required column '{col}' not found in CSV file.")

    for index, row in df.iterrows():
        start_page = row['No.'] - 1  # Adjust for 0-based indexing
        end_page = row['No.']

        pdf_writer = PyPDF2.PdfWriter()
        for page_num in range(start_page, end_page):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        output_path = f"{row['Names']}.pdf"
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

# Example usage:
pdf_path = "SVG Certificates.pdf"
csv_path = "names.csv"
split_pdf_by_csv(pdf_path, csv_path)