import platform
from gtts import gTTS
import speech_recognition as sr
import os
from io import BytesIO
import tempfile
import time

class SpeechEngine:
    def __init__(self):
        self.system = platform.system()
        self.temp_dir = tempfile.gettempdir()
        self.recognizer = sr.Recognizer()

    def speak(self, text, lang='en'):
        """텍스트를 음성으로 변환 및 재생"""
        try:
            tts = gTTS(text=text, lang=lang)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_file_path = temp_file.name
            temp_file.close()
            tts.save(temp_file_path)

            if self.system == "Darwin":  # Mac
                os.system(f"afplay {temp_file_path}")
            elif self.system == "Windows":
                os.system(f"start {temp_file_path}")
            else:  # Linux
                os.system(f"mpg123 {temp_file_path}")

            time.sleep(1)
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        except Exception as e:
            print(f"TTS 오류: {e}")

    def text_to_speech(self, text, lang='en', slow=False, save_as_file=True, filename="output.mp3"):
        """텍스트를 파일로 저장하거나 BytesIO로 반환"""
        try:
            tts = gTTS(text=text, lang=lang, slow=slow)

            if save_as_file:
                filepath = os.path.join(self.temp_dir, filename)
                tts.save(filepath)
                return filepath
            else:
                audio_fp = BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                return audio_fp

        except Exception as e:
            print(f"TTS 오류: {e}")
            return None

    def speech_to_text(self, audio_source=None, language='en-US'):
        """마이크 또는 오디오 소스에서 음성을 텍스트로 변환"""
        try:
            if audio_source is None:
                with sr.Microphone() as source:
                    print("음성을 입력하세요...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = self.recognizer.listen(source, timeout=5)
            else:
                audio = audio_source

            text = self.recognizer.recognize_google(audio, language=language)
            return text

        except sr.WaitTimeoutError:
            return "시간 초과: 음성이 감지되지 않았습니다."
        except sr.UnknownValueError:
            return "음성을 인식할 수 없습니다."
        except sr.RequestError as e:
            return f"서비스 오류: {e}"
        except Exception as e:
            return f"STT 오류: {e}"

    def speech_to_text_from_file(self, audio_file, language='en-US'):
        """오디오 파일에서 텍스트 추출"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language=language)
                return text
        except Exception as e:
            return f"파일 STT 오류: {e}"

    def compare_pronunciation(self, original_text, spoken_text):
        """발음 비교 및 피드백"""
        original = original_text.lower().strip()
        spoken = spoken_text.lower().strip()

        if original == spoken:
            accuracy = 100
            feedback = "완벽합니다! 🎉"
        else:
            similarity = self._calculate_similarity(original, spoken)
            accuracy = similarity * 100
            if accuracy >= 80:
                feedback = "매우 좋습니다! 👍"
            elif accuracy >= 60:
                feedback = "좋아요! 조금 더 연습해보세요."
            else:
                feedback = "다시 한번 시도해보세요."

        return {
            'accuracy': round(accuracy, 2),
            'feedback': feedback,
            'original': original,
            'spoken': spoken
        }

    def _calculate_similarity(self, s1, s2):
        if len(s1) == 0:
            return 0.0 if len(s2) > 0 else 1.0
        if len(s2) == 0:
            return 0.0
        distance = self._levenshtein_distance(s1, s2)
        max_len = max(len(s1), len(s2))
        similarity = 1 - (distance / max_len)
        return max(0, similarity)

    def _levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
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

    def get_supported_languages(self):
        """지원 언어 목록"""
        return {
            'en': 'English',
            'ko': 'Korean',
            'ja': 'Japanese',
            'zh-CN': 'Chinese (Simplified)',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German'
        }
