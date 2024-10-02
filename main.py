import os
from preprocessing import preprocess_image_for_ocr, pdf_to_images, create_temp_folder
from toLatex import toLatex


def process_image(image_path, output_file, api_key):
    """
    Preprocess the image and convert it to LaTeX.
    """
    print(f"Processing image: {image_path}")

    # Preprocess the image
    preprocessed_image = preprocess_image_for_ocr(image_path)

    # Convert the preprocessed image to LaTeX
    toLatex(preprocessed_image, output_file, api_key)

    print(f"Image processing complete. LaTeX output saved to '{output_file}'")


def process_pdf(pdf_path, output_file_base, api_key):
    """
    Convert PDF to images, preprocess each image, and convert it to LaTeX.
    Save LaTeX output for each page with page number appended to the output file name.
    """
    print(f"Processing PDF: {pdf_path}")

    # Create a temporary folder to store the PDF images
    temp_folder = create_temp_folder()

    # Convert PDF pages to images and store them in the temp folder
    pdf_images = pdf_to_images(pdf_path, temp_folder)

    # Process each image and output the LaTeX to separate files
    for page_number, image_path in enumerate(pdf_images, start=1):
        print(f"Processing page {page_number} image: {image_path}")

        # Preprocess the image for OCR
        preprocessed_image = preprocess_image_for_ocr(image_path)

        # Create the output file name for this page (e.g., output_file_base_1.txt, output_file_base_2.txt)
        page_output_file = f"{output_file_base}_{page_number}.txt"

        # Convert the preprocessed image to LaTeX
        toLatex(preprocessed_image, page_output_file, api_key)

        print(f"LaTeX output for page {page_number} saved to '{page_output_file}'")

    print("PDF processing complete.")

def main():
    #input_type = input("Enter 'pdf' to process a PDF or 'image' to process an image: ").strip().lower()
    input_type = "pdf"

    # Input for the file path (PDF or image)
    # file_path = input(f"Enter the path to the {input_type} file: ").strip()
    file_path = "C:/Users/Ben/Downloads/example_paper.pdf"

    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    # Input for the OpenAI API key
    #api_key = input("Enter your OpenAI API key: ").strip()
    api_key = "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"

    # Output LaTeX file base name
    #output_file_base = input("Enter the base name for the output LaTeX files (e.g., latex_output): ").strip()
    output_file_base = "latex_output"

    # Process the file based on the type
    if input_type == 'pdf':
        process_pdf(file_path, output_file_base, api_key)
    elif input_type == 'image':
        process_image(file_path, f"{output_file_base}_1.txt", api_key)  # Save single image as LaTeX
    else:
        print(f"Invalid input type: {input_type}. Please enter 'pdf' or 'image'.")

if __name__ == "__main__":
    main()