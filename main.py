import os
from preprocessing import preprocess_image_for_ocr
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


def main():
    # Input for the file path (image)
    #file_path = input("Enter the path to the image file (e.g., image.png): ").strip()
    file_path = "C:/Users/Ben/Downloads/example_image.jpg"

    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    # Input for the OpenAI API key
    #api_key = input("Enter your OpenAI API key: ").strip()
    api_key = "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"

    # Output LaTeX file
    #output_file = input("Enter the name of the output LaTeX file (e.g., latex_output.txt): ").strip()
    output_file = "latex_output.txt"

    # Process the image
    process_image(file_path, output_file, api_key)


if __name__ == "__main__":
    main()
