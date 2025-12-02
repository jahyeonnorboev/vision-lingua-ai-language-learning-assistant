import os
import spacy
import requests
from collections import Counter
from dotenv import load_dotenv

# .env 파일에서 환경 변수 불러오기
load_dotenv()
OXFORD_API_ID = os.getenv("OXFORD_API_ID", "")
OXFORD_API_KEY = os.getenv("OXFORD_API_KEY", "")


class WordAnalyzer:
    def __init__(self):
        """단어 분석기 초기화"""
        try:
            self.nlp_en = spacy.load("en_core_web_sm")
        except Exception:
            print("❌ 영어 spaCy 모델이 설치되어 있지 않습니다.")
            self.nlp_en = None

        # 한국어 처리를 위한 KoNLPy (선택사항)
        try:
            from konlpy.tag import Okt
            self.okt = Okt()
        except Exception:
            print("⚠️ KoNLPy가 설치되어 있지 않아 한국어 분석 기능이 비활성화됩니다.")
            self.okt = None

    def analyze_english_text(self, text):
        """영어 텍스트 형태소 분석"""
        if not self.nlp_en:
            return []

        doc = self.nlp_en(text)
        words_info = []
        for token in doc:
            if token.is_alpha and not token.is_stop:
                words_info.append({
                    'word': token.text,
                    'lemma': token.lemma_,
                    'pos': token.pos_,
                    'pos_detail': token.tag_,
                    'dependency': token.dep_
                })
        return words_info

    def analyze_korean_text(self, text):
        """한국어 텍스트 형태소 분석"""
        if not self.okt:
            return []

        morphs = self.okt.pos(text)
        words_info = []
        for word, pos in morphs:
            if pos in ['Noun', 'Verb', 'Adjective']:
                words_info.append({
                    'word': word,
                    'pos': pos,
                    'pos_korean': self._convert_pos_korean(pos)
                })
        return words_info

    def _convert_pos_korean(self, pos):
        """품사 태그를 한국어로 변환"""
        pos_map = {
            'Noun': '명사',
            'Verb': '동사',
            'Adjective': '형용사',
            'Adverb': '부사',
            'Josa': '조사'
        }
        return pos_map.get(pos, pos)

    def get_word_frequency(self, text):
        """단어 빈도 분석"""
        if self.nlp_en:
            doc = self.nlp_en(text.lower())
            words = [token.text for token in doc if token.is_alpha and not token.is_stop]
        else:
            words = text.lower().split()

        return Counter(words).most_common(20)

    def extract_key_phrases(self, text):
        """핵심 구문(명사구) 추출"""
        if not self.nlp_en:
            return []

        doc = self.nlp_en(text)
        phrases = []
        for chunk in doc.noun_chunks:
            phrases.append({
                'text': chunk.text,
                'root': chunk.root.text,
                'type': 'noun_phrase'
            })
        return phrases

    def analyze_sentence_structure(self, text):
        """문장 구조 분석"""
        if not self.nlp_en:
            return None

        doc = self.nlp_en(text)
        structure = {
            'num_sentences': len(list(doc.sents)),        # 문장 수
            'num_tokens': len(doc),                       # 토큰 수
            'num_words': len([t for t in doc if t.is_alpha]),  # 단어 수
            'entities': [(ent.text, ent.label_) for ent in doc.ents]  # 개체명 인식 결과
        }
        return structure


def get_word_definition(word, api='dictionaryapi'):
    """단어 정의 가져오기 (Oxford 또는 DictionaryAPI 사용)"""
    try:
        if api == 'oxford':
            if not OXFORD_API_ID or not OXFORD_API_KEY:
                print("⚠️ Oxford API 키가 설정되어 있지 않습니다. .env 파일을 확인하세요.")
                return None

            url = f"https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/{word.lower()}"
            headers = {
                "app_id": OXFORD_API_ID,
                "app_key": OXFORD_API_KEY
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            meanings = []
            lexical_entries = data.get('results', [])[0].get('lexicalEntries', [])
            for lex in lexical_entries:
                pos = lex.get('lexicalCategory', {}).get('text', '')
                entries = lex.get('entries', [])
                for entry in entries:
                    senses = entry.get('senses', [])
                    for sense in senses[:2]:  # 상위 2개 정의만 사용
                        definitions = sense.get('definitions', [])
                        examples = sense.get('examples', [])
                        meanings.append({
                            'pos': pos,
                            'definition': definitions[0] if definitions else '',
                            'example': examples[0]['text'] if examples else ''
                        })

            return {
                'word': word,
                'phonetic': '',
                'meanings': meanings
            }

        elif api == 'dictionaryapi':
            # 무료 Dictionary API (키 필요 없음)
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()

    except Exception as e:
        print(f"❌ 단어 정의 가져오기 실패: {e}")
        return None
