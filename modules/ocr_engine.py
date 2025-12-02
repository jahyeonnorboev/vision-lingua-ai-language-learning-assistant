import pytesseract
from PIL import Image
import cv2
import numpy as np


class OCREngine:
    def __init__(self, tesseract_path=None):
        """OCR 엔진 초기화"""
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def preprocess_image(self, image):
        """이미지 전처리로 OCR 정확도 향상"""
        # PIL Image → NumPy array
        img_array = np.array(image)

        # 🛠️ Kanal sonini tekshirib, mos konvertatsiya qilish
        # 이미지 타입에 따라 자동 처리
        if len(img_array.shape) == 2:
            gray = img_array  # 이미 grayscale
        elif img_array.shape[2] == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        elif img_array.shape[2] == 4:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGBA2GRAY)
        else:
            raise ValueError(f"Unexpected channels: {img_array.shape}")
        # 🧹 Noiseni olib tashlash
        denoised = cv2.fastNlMeansDenoising(gray)

        # 🌓 Adaptive Thresholding bilan binarizatsiya
        binary = cv2.adaptiveThreshold(
            denoised, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        return binary

    def extract_text(self, image, lang='eng', preprocess=True):
        """이미지에서 텍스트 추출"""
        try:
            if isinstance(image, str):
                image = Image.open(image)

            if preprocess:
                processed_img = self.preprocess_image(image)
            else:
                processed_img = np.array(image)

            text = pytesseract.image_to_string(
                processed_img,
                lang=lang,
                config='--psm 6'
            )

            return text.strip()

        except Exception as e:
            return f"OCR 오류: {str(e)}"

    def extract_text_with_boxes(self, image, lang='eng'):
        """텍스트와 위치 정보 함께 추출"""
        try:
            if isinstance(image, str):
                image = Image.open(image)

            data = pytesseract.image_to_data(
                image,
                lang=lang,
                output_type=pytesseract.Output.DICT
            )

            results = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 60:
                    results.append({
                        'text': data['text'][i],
                        'confidence': data['conf'][i],
                        'x': data['left'][i],
                        'y': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i]
                    })

            return results

        except Exception:
            return []

    def detect_language(self, text):
        """텍스트 언어 감지 (간단한 버전)"""
        korean_chars = sum(1 for c in text if '가' <= c <= '힣')
        english_chars = sum(1 for c in text if c.isalpha() and c.isascii())

        total = korean_chars + english_chars
        if total == 0:
            return 'unknown'

        if korean_chars / total > 0.3:
            return 'korean'
        elif english_chars / total > 0.3:
            return 'english'
        else:
            return 'mixed'
