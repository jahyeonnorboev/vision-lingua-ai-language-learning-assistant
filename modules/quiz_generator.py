import random
from transformers import pipeline
import re


class QuizGenerator:
    def __init__(self):
        """퀴즈 생성기 초기화"""
        self.quiz_types = ['multiple_choice', 'fill_blank', 'translation', 'matching']

        # Question Generation 모델 (선택사항 - 필요시 로드)
        self.qg_model = None

    def load_qg_model(self):
        """Question Generation 모델 로드"""
        try:
            self.qg_model = pipeline(
                "text2text-generation",
                model="valhalla/t5-small-qg-hl"
            )
            print("Question Generation 모델 로드 완료")
        except Exception as e:
            print(f"QG 모델 로드 실패: {e}")

    def generate_multiple_choice(self, word, translation, distractors=None):
        """객관식 퀴즈 생성

        Args:
            word: 영어 단어
            translation: 한국어 번역
            distractors: 오답 선택지 (없으면 자동 생성)

        Returns:
            퀴즈 딕셔너리
        """
        if not distractors:
            # 간단한 오답 생성 (실제로는 더 정교한 방법 필요)
            distractors = self._generate_distractors(translation, count=3)

        options = [translation] + distractors[:3]
        random.shuffle(options)

        return {
            'type': 'multiple_choice',
            'question': f'"{word}"의 뜻은?',
            'options': options,
            'correct_answer': translation,
            'correct_index': options.index(translation)
        }

    def generate_fill_blank(self, sentence, target_word):
        """빈칸 채우기 퀴즈 생성

        Args:
            sentence: 예문
            target_word: 빈칸으로 만들 단어

        Returns:
            퀴즈 딕셔너리
        """
        # 대소문자 구분 없이 단어 찾기
        pattern = re.compile(re.escape(target_word), re.IGNORECASE)
        blank_sentence = pattern.sub('_____', sentence, count=1)

        return {
            'type': 'fill_blank',
            'question': '빈칸에 알맞은 단어를 입력하세요:',
            'sentence': blank_sentence,
            'correct_answer': target_word.lower(),
            'original_sentence': sentence
        }

    def generate_translation_quiz(self, word, translation, direction='en_to_ko'):
        """번역 퀴즈 생성

        Args:
            word: 영어 단어
            translation: 한국어 번역
            direction: 'en_to_ko' 또는 'ko_to_en'

        Returns:
            퀴즈 딕셔너리
        """
        if direction == 'en_to_ko':
            question = f'"{word}"를 한국어로 번역하세요:'
            correct_answer = translation
        else:
            question = f'"{translation}"를 영어로 번역하세요:'
            correct_answer = word

        return {
            'type': 'translation',
            'question': question,
            'correct_answer': correct_answer.lower(),
            'direction': direction
        }

    def generate_matching_quiz(self, word_pairs):
        """매칭 퀴즈 생성

        Args:
            word_pairs: [(word1, translation1), (word2, translation2), ...]

        Returns:
            퀴즈 딕셔너리
        """
        if len(word_pairs) < 4:
            return None

        selected_pairs = random.sample(word_pairs, min(5, len(word_pairs)))
        words = [pair[0] for pair in selected_pairs]
        translations = [pair[1] for pair in selected_pairs]

        # 번역 순서 섞기
        shuffled_translations = translations.copy()
        random.shuffle(shuffled_translations)

        return {
            'type': 'matching',
            'question': '영어 단어와 한국어 뜻을 연결하세요:',
            'words': words,
            'translations': shuffled_translations,
            'correct_pairs': dict(zip(words, translations))
        }

    def generate_context_question(self, sentence):
        """문맥 기반 질문 생성 (T5 모델 사용)"""
        if not self.qg_model:
            return None

        try:
            # 문장에 하이라이트 추가 (QG 모델 입력 형식)
            # 예: "The <hl> cat <hl> is sleeping."
            result = self.qg_model(f"generate question: {sentence}")
            question = result[0]['generated_text']

            return {
                'type': 'context_question',
                'question': question,
                'context': sentence
            }
        except Exception as e:
            print(f"문맥 질문 생성 오류: {e}")
            return None

    def _generate_distractors(self, correct_answer, count=3):
        """오답 선택지 생성 (간단한 버전)"""
        # 실제로는 의미적으로 비슷하지만 틀린 답을 생성해야 함
        # 여기서는 예시로 간단한 단어 목록 사용
        common_words = [
            '사과', '바나나', '고양이', '강아지', '집', '학교',
            '책', '컴퓨터', '차', '비행기', '음식', '물',
            '하늘', '바다', '산', '나무', '꽃', '새'
        ]

        distractors = []
        for word in common_words:
            if word != correct_answer and len(distractors) < count:
                distractors.append(word)

        # 충분하지 않으면 랜덤 문자열 추가
        while len(distractors) < count:
            distractors.append(f"오답{len(distractors) + 1}")

        return distractors[:count]

    def create_quiz_set(self, vocabulary_list, quiz_count=10, quiz_type='mixed'):
        """퀴즈 세트 생성

        Args:
            vocabulary_list: [(word, translation, example), ...]
            quiz_count: 생성할 퀴즈 개수
            quiz_type: 'mixed', 'multiple_choice', 'fill_blank', 'translation'

        Returns:
            퀴즈 리스트
        """
        if not vocabulary_list:
            return []

        quizzes = []
        selected_words = random.sample(
            vocabulary_list,
            min(quiz_count, len(vocabulary_list))
        )

        for word_data in selected_words:
            word = word_data[0]
            translation = word_data[1]
            example = word_data[2] if len(word_data) > 2 else None

            # 퀴즈 타입 결정
            if quiz_type == 'mixed':
                q_type = random.choice(['multiple_choice', 'translation', 'fill_blank'])
            else:
                q_type = quiz_type

            # 퀴즈 생성
            if q_type == 'multiple_choice':
                quiz = self.generate_multiple_choice(word, translation)
            elif q_type == 'translation':
                direction = random.choice(['en_to_ko', 'ko_to_en'])
                quiz = self.generate_translation_quiz(word, translation, direction)
            elif q_type == 'fill_blank' and example:
                quiz = self.generate_fill_blank(example, word)
            else:
                # fill_blank이지만 예문이 없으면 multiple_choice로
                quiz = self.generate_multiple_choice(word, translation)

            quizzes.append(quiz)

        return quizzes

    def check_answer(self, quiz, user_answer):
        """답안 확인

        Returns:
            (정답여부, 피드백)
        """
        if quiz['type'] == 'multiple_choice':
            correct = user_answer.lower().strip() == quiz['correct_answer'].lower().strip()
            feedback = "정답입니다! 🎉" if correct else f"틀렸습니다. 정답: {quiz['correct_answer']}"

        elif quiz['type'] in ['translation', 'fill_blank']:
            user_ans = user_answer.lower().strip()
            correct_ans = quiz['correct_answer'].lower().strip()

            # 유사도 체크 (오타 허용)
            similarity = self._calculate_similarity(user_ans, correct_ans)
            correct = similarity > 0.8

            if correct:
                feedback = "정답입니다! 🎉"
            else:
                feedback = f"틀렸습니다. 정답: {quiz['correct_answer']}"

        else:
            correct = False
            feedback = "알 수 없는 퀴즈 타입입니다."

        return correct, feedback

    def _calculate_similarity(self, s1, s2):
        """문자열 유사도 계산"""
        if len(s1) == 0 or len(s2) == 0:
            return 0.0

        # 간단한 Jaccard 유사도
        set1 = set(s1.lower())
        set2 = set(s2.lower())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union if union > 0 else 0.0