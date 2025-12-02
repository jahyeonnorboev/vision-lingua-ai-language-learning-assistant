import streamlit as st
from PIL import Image
import sys
import os

# 모듈 임포트
sys.path.append(os.path.dirname(__file__))
from modules.ocr_engine import OCREngine
from modules.translator import TranslationEngine
from modules.word_analyzer import WordAnalyzer
from modules.vocabulary_db import VocabularyDB
from modules.speech_engine import SpeechEngine
from modules.quiz_generator import QuizGenerator

# 페이지 설정
st.set_page_config(
    page_title="VisionLingua - AI 번역 ㄴㅔ학습",
    page_icon="📸",
    layout="wide"
)

# 세션 상태 초기화
if 'ocr_engine' not in st.session_state:
    st.session_state.ocr_engine = OCREngine()
if 'translator' not in st.session_state:
    st.session_state.translator = TranslationEngine()
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = WordAnalyzer()
if 'vocab_db' not in st.session_state:
    st.session_state.vocab_db = VocabularyDB()
if 'speech_engine' not in st.session_state:
    st.session_state.speech_engine = SpeechEngine()
if 'quiz_gen' not in st.session_state:
    st.session_state.quiz_gen = QuizGenerator()

# 사이드바 메뉴
st.sidebar.title("📚 VisionLingua")
st.sidebar.markdown("**카메라로 배우는 AI 번역기**")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "메뉴 선택",
    ["📸 이미지 번역", "📖 단어장", "🎯 퀴즈", "📊 학습 통계", "⚙️ 설정"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **사용법**\n\n"
    "1. 이미지를 업로드하세요\n"
    "2. OCR로 텍스트 추출\n"
    "3. 번역 및 단어 분석\n"
    "4. 단어장에 저장\n"
    "5. 퀴즈로 복습"
)

# ===== 메인 화면 =====
if menu == "📸 이미지 번역":
    st.title("📸 이미지에서 텍스트 추출 & 번역")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1️⃣ 이미지 업로드 또는 텍스트 입력")

        # 이미지 업로드
        uploaded_file = st.file_uploader(
            "이미지를 선택하세요 (JPG, PNG)",
            type=['jpg', 'jpeg', 'png']
        )

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지",use_container_width=True)

            # OCR 언어 선택
            ocr_lang = st.selectbox(
                "OCR 언어",
                options=['eng', 'kor', 'eng+kor'],
                format_func=lambda x: {
                    'eng': '영어',
                    'kor': '한국어',
                    'eng+kor': '영어+한국어'
                }[x]
            )

            # OCR 실행 버튼
            if st.button("🔍 텍스트 추출", type="primary"):
                with st.spinner("텍스트를 추출하는 중..."):
                    try:
                        extracted_text = st.session_state.ocr_engine.extract_text(
                            image, lang=ocr_lang
                        )
                        if extracted_text and not extracted_text.startswith("OCR 오류"):
                            st.session_state.extracted_text = extracted_text
                            st.success("✅ 텍스트 추출 완료!")
                        else:
                            st.error("❌ 텍스트를 찾을 수 없습니다.")
                    except Exception as e:
                        st.error(f"OCR 오류: {str(e)}")

        st.markdown("---")
        st.subheader("또는 직접 텍스트 입력")

        # 직접 텍스트 입력
        user_text = st.text_area(
            "번역할 텍스트를 입력하세요:",
            height=100,
            placeholder="여기에 텍스트를 입력하거나 붙여넣으세요..."
        )

    with col2:
        st.subheader("2️⃣ 추출된 텍스트 및 번역")

        # OCR 결과 또는 사용자 입력 텍스트 표시
        final_text = ""

        if 'extracted_text' in st.session_state and st.session_state.extracted_text:
            final_text = st.session_state.extracted_text

        if user_text.strip():
            final_text = user_text

        if final_text:
            # 텍스트 표시 및 편집
            edited_text = st.text_area(
                "텍스트 (수정 가능)",
                value=final_text,
                height=150
            )

            # 번역 옵션
            col_a, col_b = st.columns(2)
            with col_a:
                src_lang = st.selectbox(
                    "원본 언어",
                    options=['auto', 'en', 'ko', 'ja', 'zh-CN'],
                    format_func=lambda x: {
                        'auto': '자동 감지',
                        'en': '영어',
                        'ko': '한국어',
                        'ja': '일본어',
                        'zh-CN': '중국어'
                    }[x]
                )

            with col_b:
                tgt_lang = st.selectbox(
                    "번역 언어",
                    options=['ko', 'en', 'ja', 'zh-CN'],
                    format_func=lambda x: {
                        'ko': '한국어',
                        'en': '영어',
                        'ja': '일본어',
                        'zh-CN': '중국어'
                    }[x]
                )

            # 번역 실행
            if st.button("🌍 번역하기", type="primary"):
                with st.spinner("번역 중..."):
                    try:
                        translated = st.session_state.translator.translate(
                            edited_text,
                            src_lang=src_lang,
                            tgt_lang=tgt_lang
                        )
                        if translated:
                            st.session_state.translated_text = translated
                            st.session_state.source_text = edited_text
                            st.session_state.src_lang = src_lang
                            st.session_state.tgt_lang = tgt_lang
                        else:
                            st.error("❌ 번역에 실패했습니다.")
                    except Exception as e:
                        st.error(f"번역 오류: {str(e)}")

            # 번역 결과
            if 'translated_text' in st.session_state:
                st.success("✅ 번역 완료!")
                st.text_area(
                    "번역 결과",
                    value=st.session_state.translated_text,
                    height=150
                )

                # 음성 재생
                st.markdown("### 🔊 음성 듣기")
                col_x, col_y = st.columns(2)
                with col_x:
                    if st.button("🎵 원문 읽기"):
                        try:
                            # 언어 코드 변환
                            audio_lang = 'en' if st.session_state.src_lang in ['auto',
                                                                               'en'] else st.session_state.src_lang
                            if audio_lang == 'zh-CN':
                                audio_lang = 'zh-cn'

                            audio_file = st.session_state.speech_engine.text_to_speech(
                                st.session_state.source_text,
                                lang=audio_lang,
                                save_as_file=True,
                                filename="original.mp3"
                            )
                            if audio_file and os.path.exists(audio_file):
                                with open(audio_file, 'rb') as f:
                                    st.audio(f.read(), format='audio/mp3')
                        except Exception as e:
                            st.error(f"TTS 오류: {str(e)}")

                with col_y:
                    if st.button("🎵 번역 읽기"):
                        try:
                            audio_lang = st.session_state.tgt_lang
                            if audio_lang == 'zh-CN':
                                audio_lang = 'zh-cn'

                            audio_file = st.session_state.speech_engine.text_to_speech(
                                st.session_state.translated_text,
                                lang=audio_lang,
                                save_as_file=True,
                                filename="translation.mp3"
                            )
                            if audio_file and os.path.exists(audio_file):
                                with open(audio_file, 'rb') as f:
                                    st.audio(f.read(), format='audio/mp3')
                        except Exception as e:
                            st.error(f"TTS 오류: {str(e)}")
        else:
            st.info("👆 이미지를 업로드하거나 텍스트를 입력하세요.")

    # 단어 분석 섹션
    if final_text:
        st.markdown("---")
        st.subheader("📚 단어 분석 및 저장")

        if st.button("🔬 단어 분석 시작"):
            with st.spinner("단어를 분석하는 중..."):
                try:
                    words_info = st.session_state.analyzer.analyze_english_text(final_text)
                    if words_info:
                        st.session_state.analyzed_words = words_info
                        st.success(f"✅ {len(words_info)}개의 단어를 발견했습니다!")
                    else:
                        st.warning("⚠️ 분석할 수 있는 단어를 찾지 못했습니다.")
                except Exception as e:
                    st.error(f"단어 분석 오류: {str(e)}")

        if 'analyzed_words' in st.session_state and st.session_state.analyzed_words:
            st.write(f"**발견된 단어: {len(st.session_state.analyzed_words)}개**")

            # 단어 테이블
            for idx, word_info in enumerate(st.session_state.analyzed_words[:10]):
                with st.expander(f"📖 {word_info['word']} ({word_info['pos']})"):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        # 단어 정의 가져오기
                        try:
                            definition = st.session_state.analyzer.get_word_definition(
                                word_info['word']
                            )

                            if definition and definition.get('meanings'):
                                for meaning in definition['meanings'][:2]:
                                    st.write(f"**{meaning['pos']}:** {meaning['definition']}")
                                    if meaning.get('example'):
                                        st.write(f"*예: {meaning['example']}*")
                            else:
                                st.write("사전 정의를 찾을 수 없습니다.")
                        except Exception as e:
                            st.write(f"정의 로드 실패: {str(e)}")

                    with col2:
                        # 번역
                        try:
                            translation = st.session_state.translator.translate(
                                word_info['word'], 'en', 'ko'
                            )
                            st.write(f"**번역:** {translation}")

                            # 단어장에 저장
                            if st.button(f"💾 저장", key=f"save_{idx}"):
                                st.session_state.vocab_db.add_word(
                                    word=word_info['word'],
                                    translation=translation,
                                    language='en',
                                    pos=word_info['pos']
                                )
                                st.success("✅ 단어장에 저장되었습니다!")
                        except Exception as e:
                            st.error(f"번역 실패: {str(e)}")

elif menu == "📖 단어장":
    st.title("📖 나의 단어장")

    # 단어장 조회
    vocab_df = st.session_state.vocab_db.get_all_words()

    if not vocab_df.empty:
        st.write(f"**총 {len(vocab_df)}개의 단어**")

        # 필터
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("🔍 단어 검색")
        with col2:
            lang_filter = st.selectbox("언어", options=['전체', 'en', 'ko'])

        # 필터링
        filtered_df = vocab_df.copy()
        if search:
            filtered_df = filtered_df[
                filtered_df['word'].str.contains(search, case=False, na=False)
            ]
        if lang_filter != '전체':
            filtered_df = filtered_df[filtered_df['language'] == lang_filter]

        # 테이블 표시
        st.dataframe(
            filtered_df[['word', 'translation', 'pos', 'created_at']],
            use_container_width=True
        )

        # CSV 내보내기
        if st.button("📥 CSV로 내보내기"):
            try:
                filename = st.session_state.vocab_db.export_to_csv()
                st.success(f"✅ {filename}으로 내보내기 완료!")
            except Exception as e:
                st.error(f"내보내기 실패: {str(e)}")

    else:
        st.info("📭 단어장이 비어있습니다. 이미지에서 단어를 추가해보세요!")

elif menu == "🎯 퀴즈":
    st.title("🎯 단어 퀴즈")

    vocab_df = st.session_state.vocab_db.get_all_words()

    if not vocab_df.empty and len(vocab_df) >= 4:
        # 퀴즈 설정
        col1, col2 = st.columns(2)
        with col1:
            quiz_count = st.slider("퀴즈 개수", 5, min(20, len(vocab_df)), 10)
        with col2:
            quiz_type = st.selectbox(
                "퀴즈 유형",
                options=['mixed', 'multiple_choice', 'translation'],
                format_func=lambda x: {
                    'mixed': '혼합',
                    'multiple_choice': '객관식',
                    'translation': '번역'
                }[x]
            )

        if st.button("🎮 퀴즈 시작", type="primary"):
            # 퀴즈 생성
            vocab_list = [
                (row['word'], row['translation'], row.get('example', ''))
                for _, row in vocab_df.iterrows()
            ]

            quizzes = st.session_state.quiz_gen.create_quiz_set(
                vocab_list, quiz_count, quiz_type
            )
            st.session_state.current_quizzes = quizzes
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0

        # 퀴즈 진행
        if 'current_quizzes' in st.session_state:
            quizzes = st.session_state.current_quizzes
            idx = st.session_state.quiz_index

            if idx < len(quizzes):
                quiz = quizzes[idx]

                st.progress((idx + 1) / len(quizzes))
                st.write(f"**문제 {idx + 1}/{len(quizzes)}**")
                st.write(f"### {quiz['question']}")

                if quiz['type'] == 'multiple_choice':
                    answer = st.radio("답을 선택하세요:", quiz['options'], key=f"q_{idx}")
                else:
                    answer = st.text_input("답을 입력하세요:", key=f"q_{idx}")

                if st.button("제출", key=f"submit_{idx}"):
                    correct, feedback = st.session_state.quiz_gen.check_answer(quiz, answer)

                    if correct:
                        st.success(feedback)
                        st.session_state.quiz_score += 1
                    else:
                        st.error(feedback)

                    st.session_state.quiz_index += 1
                    st.rerun()

            else:
                # 퀴즈 종료
                st.balloons()
                score = st.session_state.quiz_score
                total = len(quizzes)
                percentage = (score / total) * 100

                st.success(f"## 🎉 퀴즈 완료!")
                st.write(f"### 점수: {score}/{total} ({percentage:.1f}%)")

                if st.button("다시 시작"):
                    del st.session_state.current_quizzes
                    del st.session_state.quiz_index
                    del st.session_state.quiz_score
                    st.rerun()

    else:
        st.warning("⚠️ 퀴즈를 생성하려면 최소 4개 이상의 단어가 필요합니다.")

elif menu == "📊 학습 통계":
    st.title("📊 학습 통계")

    vocab_df = st.session_state.vocab_db.get_all_words()

    if not vocab_df.empty:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("총 단어 수", len(vocab_df))
        with col2:
            eng_count = len(vocab_df[vocab_df['language'] == 'en'])
            st.metric("영어 단어", eng_count)
        with col3:
            kor_count = len(vocab_df[vocab_df['language'] == 'ko'])
            st.metric("한국어 단어", kor_count)

        # 취약한 단어
        st.subheader("💪 복습이 필요한 단어")
        weak_words = st.session_state.vocab_db.get_weak_words(limit=10)

        if not weak_words.empty:
            st.dataframe(weak_words, use_container_width=True)
        else:
            st.info("아직 퀴즈 기록이 없습니다.")

    else:
        st.info("📭 학습 데이터가 없습니다.")

elif menu == "⚙️ 설정":
    st.title("⚙️ 설정")

    st.subheader("OCR 설정")
    tesseract_path = st.text_input(
        "Tesseract 경로 (선택사항)",
        help="Windows: C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    )

    if tesseract_path and st.button("경로 적용"):
        try:
            st.session_state.ocr_engine = OCREngine(tesseract_path=tesseract_path)
            st.success("✅ Tesseract 경로가 설정되었습니다!")
        except Exception as e:
            st.error(f"❌ 경로 설정 실패: {str(e)}")

    st.subheader("번역 엔진")
    st.info("현재 **Google Translate (deep-translator)** 사용 중")

    st.subheader("정보")
    st.write(f"**버전:** 1.0.1")
    st.write(f"**Streamlit 버전:** {st.__version__}")
    st.write(f"**Python 버전:** {sys.version.split()[0]}")

# 푸터
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='text-align: center'>
        <p>Made with ❤️ by JN as VisionLingua Team</p>
        <p style='font-size: 0.8em'>v1.0.1</p>
    </div>
    """,
    unsafe_allow_html=True
)