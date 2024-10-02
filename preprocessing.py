import cv2
import os

def is_image_blurry(image_path: str, threshold: float = 100.0) -> bool:
    """
    Check if the image is blurry based on the Laplacian variance.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Ensure the image was loaded successfully
    if image is None:
        raise ValueError(f"Error: Could not read the image file '{image_path}'. Please check the path.")

    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
    return laplacian_var < threshold

def preprocess_image_for_ocr(input_image_path: str, output_image_path: str = None, blur_threshold: float = 100.0) -> str:
    """
    Preprocess the image for OCR by converting it to grayscale, blurring, and thresholding.
    Returns the path to the preprocessed image.
    """
    if not os.path.exists(input_image_path):
        raise FileNotFoundError(f"Error: The file '{input_image_path}' does not exist.")

    # Read the image
    image = cv2.imread(input_image_path)

    if image is None:
        raise ValueError(f"Error: Could not read the image file '{input_image_path}'. Please check the file format.")

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Otsu's thresholding (binarization)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply dilation and erosion to remove small noise and smooth text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    # If no output path is specified, save the preprocessed image with '_preprocessed' appended
    if not output_image_path:
        base_name, ext = os.path.splitext(input_image_path)
        output_image_path = f"{base_name}_preprocessed{ext}"

    # Save the preprocessed image
    cv2.imwrite(output_image_path, eroded)
    return output_image_path
