# Overview

ImageScriptHider is a Python-based project that demonstrates how to hide and extract scripts within image files using steganography techniques. This project provides a practical example of encoding binary data (in this case, a script) into the least significant bits of an image and then decoding it back. This can be useful for educational purposes in the field of cybersecurity and data hiding.

# Features

    Encoding Scripts: Hide any script file within an image by embedding its binary data into the image's pixels.
    Decoding Scripts: Extract the hidden script from an image and save it as a file.
    Error Handling: Includes error checks to ensure files exist, images are large enough to hold the script, and more.
    Command-Line Interface: Easy-to-use command-line interface for encoding and decoding operations.

# Technologies Used

    Python: The main programming language used for the implementation.
    Pillow (PIL): Python Imaging Library used for image processing.
    bitarray: Library used for efficient manipulation of binary data.
    argparse: Python module for parsing command-line arguments.

# Prerequisites

- Python 3.x
- Pillow (pip install pillow)
- bitarray (pip install bitarray)

# Usage
  - Encoding a Script into an Image

        python3 image_hide.py encode input_image.png output_image.png script_to_hide.py

    input_image.png: Path to the input image file.
    output_image.png: Path where the output image with the hidden script will be saved.
    script_to_hide.py: Path to the script file that you want to hide.

  - Decoding a Script from an Image


        python3 image_hide.py decode input_image.png output_script.py

    input_image.png: Path to the image file that contains the hidden script.
    output_script.py: Path where the extracted script will be saved.

- Example
  Encoding Example

        python3 image_hide.py encode my_image.png encoded_image.png my_script.py

    This command hides the content of my_script.py inside my_image.png and saves the result as encoded_image.png.

- Decoding Example

        python3 image_hide.py decode encoded_image.png extracted_script.py

    This command extracts the hidden script from encoded_image.png and saves it as extracted_script.py.

# Project Structure

image_hide.py: Main script containing both encoding and decoding functionality.
pdf_hide.py: Other main script containing both encoding and decoding functionality.

# Error Handling

Checks if the input files exist.
Verifies if the image has sufficient space to embed the script.
Handles I/O errors during file operations.

# Contributions

Contributions are welcome! Feel free to open issues or submit pull requests with improvements and bug fixes.
