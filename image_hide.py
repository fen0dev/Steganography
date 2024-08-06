from PIL import Image
from bitarray import bitarray
import os
import argparse

def encode_image(input_image_path, output_image_path, script_path):
    # Check if the input image and script files exist
    if not os.path.isfile(input_image_path):
        raise FileNotFoundError(f"Input image file not found: {input_image_path}")
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"Script file not found: {script_path}")
    
    # Open the input image
    try:
        image = Image.open(input_image_path)
    except IOError:
        raise IOError(f"Failed to open image file: {input_image_path}")
    
    pixels = image.load()

    # Read the script file and convert its contents to binary format
    try:
        with open(script_path, 'rb') as file:
            script_data = file.read()
    except IOError:
        raise IOError(f"Failed to read script file: {script_path}")
    
    script_bits = bitarray()
    script_bits.frombytes(script_data)

    # Add a delimiter to indicate the end of the script
    script_bits.extend('00000000')
    # Get image dimension
    width, height = image.size

    # Ensure the image is large enough to hold the script
    if len(script_bits) > width * height * 3:
        raise ValueError("Script is too large to fit in the image.")

    # Embed the script bits into the least significant bits of the image pixels
    bit_index = 0
    for y in range(height):
        for x in range(width):
            if bit_index >=len(script_bits):
                break

            r, g, b = pixels[x, y]
            r = (r & ~1) | int(script_bits[bit_index])
            bit_index += 1
            
            if bit_index < len(script_bits):
                g = (g & ~1) | int(script_bits[bit_index])
                bit_index += 1

            if bit_index < len(script_bits):
                b = (b & ~1) | int(script_bits[bit_index])
                bit_index +=1
            
            pixels[x, y] = (r, g, b)

            if bit_index >= len(script_bits):
                break

    # Save the output image
    try:
        image.save(output_image_path)
    except IOError:
        raise IOError(f"Failed to save image file: {output_image_path}")
    
def decode_image(image_path, output_script_path):
    # Check if image file exists
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Open image
    try:
        image = Image.open(image_path)
    except IOError:
        raise IOError(f"Failed to open image file: {image_path}")
    
    pixels = image.load()

    # Get image dimension
    width, height = image.size

    # Extract the script bits from the least significant bits of the image pixels
    script_bits = bitarray()
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            script_bits.append(r & 1)
            script_bits.append(g & 1)
            script_bits.append(b & 1)

    # Convert the bits back to bytes and write the script to a file
    script_bytes = script_bits.tobytes()
    delimiter_index = script_bytes.find(b'\x00')
    if delimiter_index != -1:
        script_bytes = script_bytes[:delimiter_index]

    try:
        with open(output_script_path, 'wb') as file:
            file.write(script_bytes)
    except IOError:
        raise IOError(f"Failed to write script file: {output_script_path}")
    
def main():
    parser = argparse.ArgumentParser(description="Hide and extract scripts in images.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    encode_parser = subparsers.add_parser('encode', help='Encode a script into an image')
    encode_parser.add_argument('input_image', type=str, help='Path to the input image')
    encode_parser.add_argument('output_image', type=str, help='Path to the output image')
    encode_parser.add_argument('script', type=str, help='Path to the script to hide')

    decode_parser = subparsers.add_parser('decode', help='Decode a script from an image')
    decode_parser.add_argument('input_image', type=str, help='Path to the input image with hidden script')
    decode_parser.add_argument('output_script', type=str, help='Path to save the extracted script')

    args = parser.parse_args()

    if args.command == 'encode':
        try:
            encode_image(args.input_image, args.output_image, args.script)
            print(f'Script hidden in {args.output_image}')
        except Exception as e:
            print(f"An error occurred during encoding: {e}")
    elif args.command == 'decode':
        try:
            decode_image(args.input_image, args.output_script)
            print(f'Script extracted to {args.output_script}')
        except Exception as e:
            print(f"An error occurred during decoding: {e}")

if __name__ == '__main__':
    main()

# Usage for encoding
# Command --> python3 hide.py encode input.png output.png script.py
# where input.png = path to the input image
# where output.png = path where the output image with the hidden script will be saved
# script.py = path to the script file to hide

# Usage for decoding
# Command: python3 hide.py decode output.png extracted_script.py
# where output.png = path to the image that contains the hidden script
# where extracted_script.py = path where the extracted script will be saved


