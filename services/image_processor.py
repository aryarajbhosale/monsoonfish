import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import io


def generate_silhouette(image_bytes: bytes, output_path: Path) -> None:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise ValueError("Could not decode image for silhouette generation")

    h, w = img.shape[:2]

    # Transparent PNG
    if len(img.shape) == 3 and img.shape[2] == 4:
        alpha = img[:, :, 3]

        _, mask = cv2.threshold(
            alpha,
            1,
            255,
            cv2.THRESH_BINARY
        )

    else:
        if len(img.shape) == 2:
            gray = img
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Generate both threshold variants
        _, mask_a = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        _, mask_b = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )

        def best_contour(mask):
            contours, _ = cv2.findContours(
                mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            best = None
            best_area = 0

            for cnt in contours:
                x, y, cw, ch = cv2.boundingRect(cnt)
                area = cv2.contourArea(cnt)

                # Skip contours that are basically the whole image
                if cw > 0.95 * w and ch > 0.95 * h:
                    continue

                if area > best_area:
                    best_area = area
                    best = cnt

            return best, best_area

        cnt_a, area_a = best_contour(mask_a)
        cnt_b, area_b = best_contour(mask_b)

        silhouette = np.zeros((h, w), dtype=np.uint8)

        if area_a >= area_b and cnt_a is not None:
            cv2.drawContours(
                silhouette,
                [cnt_a],
                -1,
                255,
                thickness=cv2.FILLED
            )
        elif cnt_b is not None:
            cv2.drawContours(
                silhouette,
                [cnt_b],
                -1,
                255,
                thickness=cv2.FILLED
            )

        cv2.imwrite(str(output_path), silhouette)
        return

    # PNG path
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (5, 5)
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    silhouette = np.zeros((h, w), dtype=np.uint8)

    cv2.drawContours(
        silhouette,
        contours,
        -1,
        255,
        thickness=cv2.FILLED
    )

    cv2.imwrite(str(output_path), silhouette)


def generate_border(image_bytes: bytes, output_path: Path) -> None:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise ValueError("Could not decode image for border generation")

    if img.ndim == 2:
        gray = img
    elif img.shape[2] == 4:
        alpha = img[:, :, 3]
        gray = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY)
        _, alpha_mask = cv2.threshold(alpha, 10, 255, cv2.THRESH_BINARY)
        gray = cv2.bitwise_and(gray, gray, mask=alpha_mask)
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    edges = cv2.dilate(edges, kernel, iterations=1)

    cv2.imwrite(str(output_path), edges)


def generate_grayscale(image_bytes: bytes, output_path: Path) -> None:
    pil_image = Image.open(io.BytesIO(image_bytes))

    if pil_image.mode == 'RGBA':
        background = Image.new('RGB', pil_image.size, (255, 255, 255))
        background.paste(pil_image, mask=pil_image.split()[3])
        pil_image = background
    elif pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')

    grayscale = pil_image.convert('L')
    grayscale.save(str(output_path), format='PNG')


def process_image(image_bytes: bytes, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)

    silhouette_path = output_dir / "silhouette.png"
    border_path = output_dir / "border.png"
    grayscale_path = output_dir / "grayscale.png"

    generate_silhouette(image_bytes, silhouette_path)
    generate_border(image_bytes, border_path)
    generate_grayscale(image_bytes, grayscale_path)

    return {
        "silhouette": str(silhouette_path),
        "border": str(border_path),
        "grayscale": str(grayscale_path),
    }
