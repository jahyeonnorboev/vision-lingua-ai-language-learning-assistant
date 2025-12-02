"""
VisionLingua 프로젝트 설정 파일
"""

import os
from pathlib import Path

# ===== 프로젝트 경로 설정 =====
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
TEMP_DIR = DATA_DIR / 'temp'
MODELS_DIR = BASE_DIR / 'models'

# 디렉토리 생성
for directory in [DATA_DIR, TEMP_DIR, MODELS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ===== 데이터베이스 설정 =====
DATABASE_PATH = DATA_DIR / 'vocabulary.db'

# ===== OCR 설정 =====
OCR_CONFIG = {
    'languages': {
        'eng': '영어',
        'kor': '한국어',
        'eng+kor': '영어+한국어',
        'jpn': '일본어',
        'chi_sim': '중국어 (간체)',
    },
    'default_lang': 'eng',
    'psm_mode': 6,  # Page Segmentation Mode (1-13)
    'oem_mode': 3,  # OCR Engine Mode (0-3)
}

# Tesseract 경로 (Windows 사용자를 위한 일반적인 경로)
TESSERACT_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    '/usr/bin/tesseract',  # Linux
    '/usr/local/bin/tesseract',  # Mac
]

# ===== 번역 설정 =====
TRANSLATION_CONFIG = {
    'default_method': 'google',  # 'google' or 'marian'
    'language_codes': {
        'korean': {'google': 'ko', 'marian': 'ko'},
        'english': {'google': 'en', 'marian': 'en'},
        'japanese': {'google': 'ja', 'marian': 'ja'},
        'chinese': {'google': 'zh-CN', 'marian': 'zh'},
    },
    'marian_models': {
        'en-ko': 'Helsinki-NLP/opus-mt-en-ko',
        'ko-en': 'Helsinki-NLP/opus-mt-ko-en',
        'en-ja': 'Helsinki-NLP/opus-mt-en-jap',
        'en-zh': 'Helsinki-NLP/opus-mt-en-zh',
    }
}

# ===== NLP 설정 =====
NLP_CONFIG = {
    'spacy_models': {
        'en': 'en_core_web_sm',
        'ko': None,  # KoNLPy 사용
    },
    'pos_tags_korean': {
        'Noun': '명사',
        'Verb': '동사',
        'Adjective': '형용사',
        'Adverb': '부사',
        'Josa': '조사',
        'Eomi': '어미',
    }
}

# ===== 사전 API 설정 =====
DICTIONARY_CONFIG = {
    'free_dict_api': 'https://api.dictionaryapi.dev/api/v2/entries/en/',
    'timeout': 30,  # seconds
    'max_definitions': 3,  # 표시할 최대 정의 개수
}

# ===== TTS/STT 설정 =====
SPEECH_CONFIG = {
    'tts_languages': {
        'en': 'en',
        'ko': 'ko',
        'ja': 'ja',
        'zh-CN': 'zh-CN',
        'es': 'es',
        'fr': 'fr',
        'de': 'de',
    },
    'stt_languages': {
        'en': 'en-US',
        'ko': 'ko-KR',
        'ja': 'ja-JP',
        'zh': 'zh-CN',
    },
    'default_tts_lang': 'en',
    'default_stt_lang': 'en-US',
    'tts_slow_speed': False,
    'audio_format': 'mp3',
}

# ===== 퀴즈 설정 =====
QUIZ_CONFIG = {
    'types': {
        'multiple_choice': '객관식',
        'fill_blank': '빈칸 채우기',
        'translation': '번역',
        'matching': '매칭',
    },
    'default_quiz_count': 10,
    'min_words_for_quiz': 4,
    'distractor_count': 3,  # 객관식 오답 개수
    'similarity_threshold': 0.8,  # 정답 인정 유사도
}

# ===== UI 설정 =====
UI_CONFIG = {
    'page_title': 'VisionLingua - AI 번역 학습',
    'page_icon': '📸',
    'layout': 'wide',
    'max_image_size': 10 * 1024 * 1024,  # 10MB
    'allowed_image_types': ['jpg', 'jpeg', 'png', 'bmp'],
    'items_per_page': 20,
}

# ===== 색상 테마 =====
THEME = {
    'primary_color': '#FF6B6B',
    'background_color': '#FFFFFF',
    'secondary_background': '#F0F2F6',
    'text_color': '#262730',
}

# ===== 로깅 설정 =====
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': DATA_DIR / 'visionlingua.log',
}

# ===== 성능 설정 =====
PERFORMANCE_CONFIG = {
    'enable_caching': True,
    'cache_ttl': 3600,  # 1시간
    'max_workers': 4,  # 멀티스레딩 워커 수
    'batch_size': 10,  # 배치 처리 크기
}

# ===== 에러 메시지 =====
ERROR_MESSAGES = {
    'ocr_failed': '텍스트 추출에 실패했습니다. 이미지를 확인해주세요.',
    'translation_failed': '번역에 실패했습니다. 네트워크 연결을 확인해주세요.',
    'no_text_found': '이미지에서 텍스트를 찾을 수 없습니다.',
    'file_too_large': f'파일 크기가 너무 큽니다. (최대: {UI_CONFIG["max_image_size"] // (1024 * 1024)}MB)',
    'invalid_file_type': f'지원하지 않는 파일 형식입니다. ({", ".join(UI_CONFIG["allowed_image_types"])}만 가능)',
    'db_error': '데이터베이스 오류가 발생했습니다.',
    'model_load_error': '모델 로딩에 실패했습니다.',
}

# ===== 성공 메시지 =====
SUCCESS_MESSAGES = {
    'ocr_success': '✅ 텍스트 추출 완료!',
    'translation_success': '✅ 번역 완료!',
    'word_saved': '✅ 단어장에 저장되었습니다!',
    'quiz_completed': '🎉 퀴즈 완료!',
    'export_success': '✅ CSV 내보내기 완료!',
}

# ===== 개발자 설정 =====
DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'
VERSION = '1.0.0'
AUTHOR = 'VisionLingua Team'

# ===== 환경 변수 =====
# .env 파일에서 로드 가능한 설정들
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
GOOGLE_TRANSLATE_API_KEY = os.getenv('GOOGLE_TRANSLATE_API_KEY', '')


# ===== 설정 검증 함수 =====
def validate_config():
    """설정 유효성 검사"""
    errors = []

    # 필수 디렉토리 확인
    if not DATA_DIR.exists():
        errors.append(f"Data directory not found: {DATA_DIR}")

    # Tesseract 경로 확인
    tesseract_found = False
    for path in TESSERACT_PATHS:
        if os.path.exists(path):
            tesseract_found = True
            break

    if not tesseract_found and not DEBUG_MODE:
        errors.append("Tesseract-OCR not found. Please install it.")

    return errors


# ===== 설정 정보 출력 =====
def print_config_info():
    """설정 정보 출력 (디버깅용)"""
    print("=" * 50)
    print(f"VisionLingua v{VERSION}")
    print("=" * 50)
    print(f"Base Directory: {BASE_DIR}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Database Path: {DATABASE_PATH}")
    print(f"Debug Mode: {DEBUG_MODE}")
    print("=" * 50)

    # 설정 검증
    errors = validate_config()
    if errors:
        print("⚠️ Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ All configurations are valid!")
    print("=" * 50)


if __name__ == '__main__':
    print_config_info()