import sqlite3
from datetime import datetime
import pandas as pd


class VocabularyDB:
    def __init__(self, db_path='data/vocabulary.db'):
        """단어장 데이터베이스 초기화"""
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        """데이터베이스 테이블 생성"""
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        cursor = conn.cursor()

        # 단어 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                translation TEXT,
                language TEXT,
                pos TEXT,
                definition TEXT,
                example TEXT,
                phonetic TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(word, language)
            )
        ''')

        # 학습 기록 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word_id INTEGER,
                correct BOOLEAN,
                learning_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (word_id) REFERENCES words (id)
            )
        ''')

        # 퀴즈 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word_id INTEGER,
                question TEXT,
                correct_answer TEXT,
                wrong_answers TEXT,
                quiz_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (word_id) REFERENCES words (id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_word(self, word, translation='', language='en', pos='',
                 definition='', example='', phonetic=''):
        """단어 추가"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO words 
                (word, translation, language, pos, definition, example, phonetic)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (word, translation, language, pos, definition, example, phonetic))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"단어 추가 오류: {e}")
            return None
        finally:
            conn.close()

    def update_word(self, word_id, word=None, translation=None, language=None,
                    pos=None, definition=None, example=None, phonetic=None):
        """단어 수정"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            # 기존 단어 정보 가져오기
            cursor.execute('SELECT * FROM words WHERE id = ?', (word_id,))
            row = cursor.fetchone()
            if not row:
                return False

            updated_word = word if word is not None else row[1]
            updated_translation = translation if translation is not None else row[2]
            updated_language = language if language is not None else row[3]
            updated_pos = pos if pos is not None else row[4]
            updated_definition = definition if definition is not None else row[5]
            updated_example = example if example is not None else row[6]
            updated_phonetic = phonetic if phonetic is not None else row[7]

            cursor.execute('''
                UPDATE words
                SET word = ?, translation = ?, language = ?, pos = ?, definition = ?, example = ?, phonetic = ?
                WHERE id = ?
            ''', (updated_word, updated_translation, updated_language,
                  updated_pos, updated_definition, updated_example, updated_phonetic, word_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"단어 수정 오류: {e}")
            return False
        finally:
            conn.close()

    def get_word(self, word, language='en'):
        """단어 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM words WHERE word = ? AND language = ?', (word, language))
        result = cursor.fetchone()
        conn.close()
        if result:
            return {
                'id': result[0],
                'word': result[1],
                'translation': result[2],
                'language': result[3],
                'pos': result[4],
                'definition': result[5],
                'example': result[6],
                'phonetic': result[7],
                'created_at': result[8]
            }
        return None

    def get_all_words(self, language=None):
        """모든 단어 조회"""
        conn = sqlite3.connect(self.db_path)
        if language:
            df = pd.read_sql_query('SELECT * FROM words WHERE language = ? ORDER BY created_at DESC', conn, params=(language,))
        else:
            df = pd.read_sql_query('SELECT * FROM words ORDER BY created_at DESC', conn)
        conn.close()
        return df

    def delete_word(self, word_id):
        """단어 삭제"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM words WHERE id = ?', (word_id,))
        conn.commit()
        conn.close()

    def add_learning_record(self, word_id, correct):
        """학습 기록 추가"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO learning_history (word_id, correct) VALUES (?, ?)', (word_id, correct))
        conn.commit()
        conn.close()

    def get_word_stats(self, word_id):
        """단어별 학습 통계"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) as total_attempts,
                   SUM(CASE WHEN correct = 1 THEN 1 ELSE 0 END) as correct_count
            FROM learning_history
            WHERE word_id = ?
        ''', (word_id,))
        result = cursor.fetchone()
        conn.close()
        if result and result[0] > 0:
            return {
                'total_attempts': result[0],
                'correct_count': result[1],
                'accuracy': (result[1] / result[0]) * 100
            }
        return None

    def get_weak_words(self, limit=10):
        """취약한 단어 조회"""
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT w.id, w.word, w.translation,
                   COUNT(lh.id) as attempts,
                   SUM(CASE WHEN lh.correct = 1 THEN 1 ELSE 0 END) as correct,
                   CAST(SUM(CASE WHEN lh.correct = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(lh.id) as accuracy
            FROM words w
            LEFT JOIN learning_history lh ON w.id = lh.word_id
            GROUP BY w.id
            HAVING attempts > 0
            ORDER BY accuracy ASC, attempts DESC
            LIMIT ?
        '''
        df = pd.read_sql_query(query, conn, params=(limit,))
        conn.close()
        return df

    def export_to_csv(self, filename='vocabulary_export.csv'):
        """단어장을 CSV로 내보내기"""
        df = self.get_all_words()
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        return filename
