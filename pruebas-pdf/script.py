import pdfplumber
import os

def extract_text_from_pdf(pdf_path, **kwargs):
    """
    Function to extract text from a PDF and return it as plain text.

    Parameters:
    - pdf_path: str, path to the input PDF file (required)
    - **kwargs: additional optional arguments for pdfplumber's extract_text method, such as:
        - layout: bool, whether to preserve the layout (default: True)
        - line_dir_render: str, direction of line rendering (default: 'ttb')
        - char_dir_render: str, direction of character rendering (default: 'ltr')
        - x_tolerance: int, horizontal tolerance for grouping elements (default: 1)
        - y_tolerance: int, vertical tolerance for grouping elements (default: 1)

    Returns:
    - text: str, the extracted text from the PDF.
    """

    options = {
        "layout": True,
        "line_dir_render": "ttb",
        "char_dir_render": "ltr",
        "x_tolerance": 1,
        "y_tolerance": 1,
    }

    # Update options with any additional keyword arguments passed
    options.update(kwargs)

    # Extract text from the PDF
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text(
                layout=options["layout"],
                line_dir_render=options["line_dir_render"],
                char_dir_render=options["char_dir_render"],
                x_tolerance=options["x_tolerance"],
                y_tolerance=options["y_tolerance"],
            )
            text += "\n"

    return text

if __name__ == "__main__":
    # Example usage
    pdf_path = "../pdfs/noche.pdf"  # Replace with the actual PDF file path
    extracted_text = extract_text_from_pdf(pdf_path)
    print(extracted_text)  # Outputs the plain text directly to the console
