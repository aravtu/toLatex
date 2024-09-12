import cv2
import os
api_key = "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"

def is_image_blurry(image_path: str, threshold: float = 100.0) -> bool:
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Compute the Laplacian of the image and then the variance
    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()

    # Return True if the variance is below the threshold (blurry), otherwise False
    return laplacian_var < threshold


def preprocess_image_for_ocr(input_image_path: str, output_image_path: str = None,
                             blur_threshold: float = 100.0) -> str:
    # Read the image
    image = cv2.imread(input_image_path)

    # Check if the image is blurry
    gray_for_blur_check = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray_for_blur_check, cv2.CV_64F).var()

    # Convert the image to grayscale for preprocessing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Otsu's thresholding after Gaussian filtering (binarization)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply dilation and erosion to remove small noise and smooth text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    # If output_image_path is not provided, generate a default path
    if not output_image_path:
        base_name, ext = os.path.splitext(input_image_path)
        output_image_path = f"{base_name}_preprocessed{ext}"

    # Save the preprocessed image
    cv2.imwrite(output_image_path, eroded)

    return output_image_path


input_path = "raw.png"
output_path = preprocess_image_for_ocr(input_path, blur_threshold=100.0)  # Adjust the blur threshold as needed
print(f"Preprocessed image saved to: {output_path}")