# ===== modules/__init__.py =====
"""
VisionLingua 핵심 모듈
"""

from .ocr_engine import OCREngine
from .translator import TranslationEngine
from .word_analyzer import WordAnalyzer
from .vocabulary_db import VocabularyDB
from .speech_engine import SpeechEngine
from .quiz_generator import QuizGenerator

__version__ = '1.0.0'
__all__ = [
    'OCREngine',
    'TranslationEngine',
    'WordAnalyzer',
    'VocabularyDB',
    'SpeechEngine',
    'QuizGenerator',
]


# ===== utils/__init__.py =====
"""
VisionLingua 유틸리티 함수
"""

from .helpers import (
    validate_image_file,
    clean_text,
    split_sentences,
    extract_words,
    detect_language_simple,
    levenshtein_distance,
    similarity_ratio,
    calculate_accuracy,
    get_grade,
    format_datetime,
    time_ago,
    truncate_text,
    sanitize_input,
)

__all__ = [
    'validate_image_file',
    'clean_text',
    'split_sentences',
    'extract_words',
    'detect_language_simple',
    'levenshtein_distance',
    'similarity_ratio',
    'calculate_accuracy',
    'get_grade',
    'format_datetime',
    'time_ago',
    'truncate_text',
    'sanitize_input',
]