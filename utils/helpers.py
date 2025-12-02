"""
VisionLingua 유틸리티 함수 모음
"""

import os
import hashlib
from datetime import datetime
from typing import List, Dict, Any
import re


# ===== 파일 처리 유틸리티 =====

def validate_image_file(file, max_size_mb=10):
    """이미지 파일 유효성 검사

    Args:
        file: 업로드된 파일 객체
        max_size_mb: 최대 파일 크기 (MB)

    Returns:
        (is_valid, error_message)
    """
    if file is None:
        return False, "파일이 선택되지 않았습니다."

    # 파일 크기 확인
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        return False, f"파일 크기가 {max_size_mb}MB를 초과합니다."

    # 파일 확장자 확인
    allowed_extensions = ['jpg', 'jpeg', 'png', 'bmp']
    file_ext = file.name.split('.')[-1].lower()

    if file_ext not in allowed_extensions:
        return False, f"지원하지 않는 파일 형식입니다. ({', '.join(allowed_extensions)})"

    return True, None


def get_file_hash(file_content):
    """파일 해시값 생성 (중복 체크용)"""
    return hashlib.md5(file_content).hexdigest()


def clean_filename(filename):
    """파일명 정리 (특수문자 제거)"""
    # 특수문자를 언더스코어로 변경
    clean_name = re.sub(r'[^\w\s.-]', '_', filename)
    return clean_name


# ===== 텍스트 처리 유틸리티 =====

def clean_text(text):
    """텍스트 정리 (공백, 특수문자 등)"""
    if not text:
        return ""

    # 연속된 공백을 하나로
    text = re.sub(r'\s+', ' ', text)

    # 앞뒤 공백 제거
    text = text.strip()

    return text


def split_sentences(text):
    """텍스트를 문장 단위로 분리"""
    # 간단한 문장 분리 (마침표, 느낌표, 물음표 기준)
    sentences = re.split(r'[.!?]\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def extract_words(text, min_length=2):
    """텍스트에서 단어 추출"""
    # 알파벳만 추출
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return [w for w in words if len(w) >= min_length]


def detect_language_simple(text):
    """간단한 언어 감지"""
    if not text:
        return 'unknown'

    # 한글 비율
    korean_chars = len(re.findall(r'[가-힣]', text))
    # 영어 비율
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    # 일본어 (히라가나, 가타카나)
    japanese_chars = len(re.findall(r'[ぁ-んァ-ン]', text))
    # 중국어 (한자)
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))

    total = korean_chars + english_chars + japanese_chars + chinese_chars

    if total == 0:
        return 'unknown'

    # 가장 많은 비율의 언어 반환
    lang_ratios = {
        'korean': korean_chars / total,
        'english': english_chars / total,
        'japanese': japanese_chars / total,
        'chinese': chinese_chars / total,
    }

    detected_lang = max(lang_ratios, key=lang_ratios.get)

    # 최소 30% 이상이어야 해당 언어로 판단
    if lang_ratios[detected_lang] > 0.3:
        return detected_lang
    else:
        return 'mixed'


# ===== 데이터 변환 유틸리티 =====

def dict_to_list(data_dict):
    """딕셔너리를 리스트로 변환"""
    return [{'key': k, 'value': v} for k, v in data_dict.items()]


def list_to_dict(data_list, key_field='key', value_field='value'):
    """리스트를 딕셔너리로 변환"""
    return {item[key_field]: item[value_field] for item in data_list}


def flatten_list(nested_list):
    """중첩 리스트를 평탄화"""
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list


# ===== 날짜/시간 유틸리티 =====

def get_timestamp():
    """현재 타임스탬프 반환"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def format_datetime(dt, format_str="%Y-%m-%d %H:%M:%S"):
    """날짜/시간 포맷팅"""
    if isinstance(dt, str):
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    return dt.strftime(format_str)


def time_ago(dt):
    """상대적 시간 표시 (예: 3시간 전)"""
    if isinstance(dt, str):
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

    now = datetime.now()
    diff = now - dt

    seconds = diff.total_seconds()

    if seconds < 60:
        return "방금 전"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes}분 전"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours}시간 전"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days}일 전"
    else:
        weeks = int(seconds / 604800)
        return f"{weeks}주 전"


# ===== 통계 유틸리티 =====

def calculate_accuracy(correct_count, total_count):
    """정확도 계산"""
    if total_count == 0:
        return 0.0
    return (correct_count / total_count) * 100


def get_grade(score, max_score=100):
    """점수에 따른 등급 반환"""
    percentage = (score / max_score) * 100

    if percentage >= 90:
        return 'A', '🌟'
    elif percentage >= 80:
        return 'B', '⭐'
    elif percentage >= 70:
        return 'C', '👍'
    elif percentage >= 60:
        return 'D', '💪'
    else:
        return 'F', '📚'


def calculate_progress(current, total):
    """진행률 계산"""
    if total == 0:
        return 0.0
    return min((current / total) * 100, 100.0)


# ===== 문자열 유사도 계산 =====

def levenshtein_distance(s1, s2):
    """Levenshtein 거리 계산 (편집 거리)"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def similarity_ratio(s1, s2):
    """두 문자열의 유사도 비율 (0~1)"""
    s1 = s1.lower().strip()
    s2 = s2.lower().strip()

    if not s1 or not s2:
        return 0.0

    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))

    return 1 - (distance / max_len)


# ===== 데이터 검증 유틸리티 =====

def is_valid_email(email):
    """이메일 유효성 검사"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_url(url):
    """URL 유효성 검사"""
    pattern = r'^https?://[\w\-]+(\.[\w\-]+)+[/#?]?.*$'
    return re.match(pattern, url) is not None


def sanitize_input(text, max_length=1000):
    """사용자 입력 정제 (보안)"""
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)

    # 스크립트 제거
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)

    # 최대 길이 제한
    text = text[:max_length]

    return text.strip()


# ===== 포맷팅 유틸리티 =====

def format_number(num, decimal_places=2):
    """숫자 포맷팅 (천 단위 콤마)"""
    if isinstance(num, float):
        return f"{num:,.{decimal_places}f}"
    else:
        return f"{num:,}"


def format_file_size(size_bytes):
    """파일 크기 포맷팅"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def truncate_text(text, max_length=100, suffix='...'):
    """텍스트 자르기"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


# ===== 색상 유틸리티 =====

def get_difficulty_color(accuracy):
    """정확도에 따른 색상 반환"""
    if accuracy >= 80:
        return '#28A745'  # 초록색 (쉬움)
    elif accuracy >= 60:
        return '#FFC107'  # 노란색 (보통)
    else:
        return '#DC3545'  # 빨간색 (어려움)


def hex_to_rgb(hex_color):
    """HEX 색상을 RGB로 변환"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


# ===== 디버깅 유틸리티 =====

def print_debug(message, data=None):
    """디버그 메시지 출력"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[DEBUG {timestamp}] {message}")
    if data:
        print(f"  Data: {data}")


def log_error(error, context=""):
    """에러 로깅"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_msg = f"[ERROR {timestamp}] {context}: {str(error)}"
    print(error_msg)
    # 실제로는 파일에 저장하거나 로깅 시스템 사용
    return error_msg


# ===== 테스트 함수 =====

if __name__ == '__main__':
    # 유틸리티 함수 테스트
    print("=== VisionLingua 유틸리티 테스트 ===\n")

    # 텍스트 정리 테스트
    test_text = "  Hello   World!  This  is   a   test.  "
    print(f"원본: '{test_text}'")
    print(f"정리: '{clean_text(test_text)}'\n")

    # 언어 감지 테스트
    texts = [
        "Hello, how are you?",
        "안녕하세요, 반갑습니다!",
        "Hello 안녕하세요",
        "こんにちは",
    ]
    for text in texts:
        lang = detect_language_simple(text)
        print(f"'{text}' → {lang}")

    print("\n" + "=" * 40)

    # 유사도 테스트
    pairs = [
        ("apple", "apple"),
        ("apple", "aple"),
        ("apple", "banana"),
    ]
    for s1, s2 in pairs:
        ratio = similarity_ratio(s1, s2)
        print(f"'{s1}' vs '{s2}': {ratio:.2%}")

    print("\n=== 테스트 완료 ===")