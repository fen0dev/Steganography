import fitz
import os
import argparse

def embed_script_in_PDF(input_pdf_path, output_pdf_path, script_path):
    # Check if input pdf file exists
    if not os.path.isfile(input_pdf_path):
        raise FileNotFoundError(f"Input PDF file not found: {input_pdf_path}")
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"Script file not found: {script_path}")
    
    # Open PDF
    try:
        doc = fitz.open(input_pdf_path)
    except Exception as e:
        raise IOError(f"Failed to open PDF file: {input_pdf_path}. Error: {e}")
    
    # Read script file
    try:
        with open(script_path, 'r') as file:
            script_data = file.read()
    except Exception as e:
        raise IOError(f"Failed to read script file: {script_path}. Error: {e}")
    
    # Embed script data in metadata file
    for page in doc:
        page.set_text('script_data', script_data)

    # Save the modified PDF
    try:
        doc.save(output_pdf_path)
    except Exception as e:
        raise IOError(f"Failed to save PDF file: {output_pdf_path}. Error: {e}")
    
def extract_script_from_PDF(pdf_path, output_script_path):
    # Check if PDF file still exists
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Open PDF
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise IOError(f"Failed to open PDF file: {pdf_path}. Error: {e}")

    # Extract script data from metadata
    script_data = None
    for page in doc:
        script_data = page.set_text('script_data')
        if script_data:
            break
    
    if script_data is None:
        raise ValueError("No script data found in the PDF")
    
    # Write extracted script to a file
    try:
        with open(output_script_path, 'w') as file:
            file.write(script_data)
    except Exception as e:
        raise IOError(f"Failed to write script file: {output_script_path}. Error: {e}")
    
def main():
    parser = argparse.ArgumentParser(description="Embed and extract scripts in PDF files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    embed_parser = subparsers.add_parser('embed', help='Embed a script into a PDF')
    embed_parser.add_argument('input_pdf', type=str, help='Path to the input PDF')
    embed_parser.add_argument('output_pdf', type=str, help='Path to the output PDF with embedded script')
    embed_parser.add_argument('script', type=str, help='Path to the script to embed')

    extract_parser = subparsers.add_parser('extract', help='Extract a script from a PDF')
    extract_parser.add_argument('input_pdf', type=str, help='Path to the input PDF with embedded script')
    extract_parser.add_argument('output_script', type=str, help='Path to save the extracted script')

    args = parser.parse_args()

    if args.command == 'embed':
        try:
            embed_script_in_PDF(args.input_pdf, args.output_pdf, args.script)
            print(f'Script embedded in {args.output_pdf}')
        except Exception as e:
            print(f"An error occurred during embedding: {e}")
    elif args.command == 'extract':
        try:
            extract_script_from_PDF(args.input_pdf, args.output_script)
            print(f'Script extracted to {args.output_script}')
        except Exception as e:
            print(f"An error occurred during extraction: {e}")

if __name__ == '__main__':
    main()

# Usage for embedding
# Command --> python3 pdf_hide.py embed input.pdf output.pdf script.py
# where input.pdf = path to the input PDF
# where output.pdf = path where the output PDF with the embedded script will be saved
# where script.py = path to the script file to embed
    
# Usage for extracting
# Command --> python pdf_hide.py extract output.pdf extracted_script.py
# where output.pdf = path to the PDF that contains the embedded script
# where extracted_script.py = path where the extracted script will be saved
