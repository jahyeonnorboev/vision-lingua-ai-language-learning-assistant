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
        conn = sqlite3.connect(self.db_path)
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
            word_id = cursor.lastrowid
            return word_id

        except Exception as e:
            print(f"단어 추가 오류: {e}")
            return None
        finally:
            conn.close()

    def get_word(self, word, language='en'):
        """단어 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM words WHERE word = ? AND language = ?
        ''', (word, language))

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
            query = 'SELECT * FROM words WHERE language = ? ORDER BY created_at DESC'
            df = pd.read_sql_query(query, conn, params=(language,))
        else:
            query = 'SELECT * FROM words ORDER BY created_at DESC'
            df = pd.read_sql_query(query, conn)

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

        cursor.execute('''
            INSERT INTO learning_history (word_id, correct)
            VALUES (?, ?)
        ''', (word_id, correct))

        conn.commit()
        conn.close()

    def get_word_stats(self, word_id):
        """단어별 학습 통계"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 
                COUNT(*) as total_attempts,
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
        """취약한 단어 조회 (정답률 낮은 순)"""
        conn = sqlite3.connect(self.db_path)

        query = '''
            SELECT 
                w.id, w.word, w.translation,
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