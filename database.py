import sqlite3
import time


class PersonDatabase:
    def __init__(self, database, admin=False):
        self._conn = sqlite3.connect(database)
        self._cur = self._conn.cursor()
        

        self.admin = admin

        query = """
        CREATE TABLE IF NOT EXISTS user (
            username TEXT PRIMARY KEY,
            password TEXT,
            f_name TEXT,
            l_name TEXT,
            email TEXT,
            admin TEXT
        )
        """
        

        self._cur.execute(query)

        query = """
        CREATE TABLE IF NOT EXISTS score (
            score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            correct_answers INTEGER,
            time_sec REAL,
            username TEXT,
            timestamp_creation INTEGER,
            FOREIGN KEY(username) REFERENCES user(username)
        )
        """

        self._cur.execute(query)

        query = """
        INSERT INTO user (username, password, admin) VALUES (
            'admin', 
            '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 
            'True'
            )
        """
        # Sicherstellen, dass es ein Adminkonto gibt (default Passwort admin)
        try:
            self._cur.execute(query)
        except sqlite3.IntegrityError:
            pass

        self._conn.commit()

    def new_user(self, username, password_hash, f_name, l_name, email, admin=False):
        # Check if username exists
        exists = self._cur.execute("SELECT * FROM user WHERE username = ?", (username,))

        if exists.fetchone() is None:
            query = """
            INSERT INTO user (username, password, f_name, l_name, email, admin) VALUES (
                ?, ?, ?, ?, ?, ?
            )
            """

            try:
                self._cur.execute(query, (username, password_hash, f_name, l_name, email, str(admin)))
                self._conn.commit()
                return True, ""

            except Exception as e:
                return False, e
        
        else:
            return False, "Username already exists"
    
    def check_access(self, username, hashed_password):
        query = """
        SELECT password FROM user WHERE username = ?
        """

        self._cur.execute(query, (username,))

        data = self._cur.fetchone()
        

        if data is None:
            return False

        else:
            if hashed_password == data[0]:
                return True
            else:
                return False

    def new_score(self, correct_answers, time_sec, username):
        query = """
        INSERT INTO score (correct_answers, time_sec, username, timestamp_creation) VALUES (
            ?, ?, ?, ?
        )
        """

        try:
            self._cur.execute(query, (correct_answers, time_sec, username, int(time.time())))
            self._conn.commit()
            return True, ""
        
        except Exception as e:
            return False, e

    def check_score_by_username(self, username: str, score: int, time_needed: float):
        """
        :param username: String -> Username
        :param score: Integer -> Erzielter Score
        :param time_needed: Float -> Erzielte Zeit
        :return: Integer -> Platz der eigenen Scores. 0 wird returnt, wenn es keine Übereinstimmung gibt
        """

        query = """
        SELECT correct_answers, time_sec FROM score 
            WHERE username = ?
            ORDER BY correct_answers DESC, time_sec ASC
        """

        self._cur.execute(query, (username,))
        data = self._cur.fetchall()

        index = 0

        for d in data:
            if d[0] == score and d[1] == time_needed:
                return index + 1
            index += 1
        
        return 0
    
    def check_score_by_global(self, score: int, time_needed: float):
        """
        :param score: Integer -> Erzielter Score
        :param time_needed: FLoat -> Erzielte Zeit
        :return: Integer -> Globaler Platz im Ranking
        """

        query = """
        SELECT correct_answers, time_sec FROM score
            ORDER BY correct_answers DESC, time_sec ASC
        """

        self._cur.execute(query)
        data = self._cur.fetchall()

        index = 0
        
        for d in data:
            if d[0] == score and d[1] == time_needed:
                return index + 1
            index += 1
        
        return 0

    def __del__(self):
        self._conn.close()


class QuizDatabase:
    def __init__(self, database, username):
        self.username = username

        # Initialize SQLite3-Connection and create cursor
        self._conn = sqlite3.connect(database)
        self._cur = self._conn.cursor()

        # Create Table if not exist
        query = """
        CREATE TABLE IF NOT EXISTS quiz (
            quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            wrong_answer_1 TEXT,
            wrong_answer_2 TEXT,
            wrong_answer_3 TEXT,
            correct_answer TEXT,
            category TEXT,
            author TEXT,
            editor TEXT,
            timestamp_creation INTEGER,
            timestamp_lastchange INTEGER
        )
        """

        self._cur.execute(query)

        query = """
        CREATE TABLE IF NOT EXISTS deleted_quiz (
            deleted_quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            wrong_answer_1 TEXT,
            wrong_answer_2 TEXT,
            wrong_answer_3 TEXT,
            correct_answer TEXT,
            category TEXT,
            author TEXT,
            editor TEXT,
            timestamp_creation INTEGER,
            timestamp_lastchange INTEGER,
            old_primarykey INTEGER
        )
        """

        self._cur.execute(query)

        query = """
        CREATE TABLE IF NOT EXISTS complained_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER,
            comment TEXT,
            suggested_answer TEXT,
            username TEXT,
            timestamp INTEGER,
            FOREIGN KEY(quiz_id) REFERENCES quiz(quiz_id)
        )
        """

        self._cur.execute(query)

        self._conn.commit()

    def new_question(self, question, wrong_answer_1, wrong_answer_2, wrong_answer_3, correct_answer, category):
        query = """
        INSERT INTO quiz (
            question,
            wrong_answer_1,
            wrong_answer_2,
            wrong_answer_3,
            correct_answer,
            category,
            author,
            editor,
            timestamp_creation,
            timestamp_lastchange
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            self._cur.execute(query, (question, wrong_answer_1, wrong_answer_2, wrong_answer_3, correct_answer, category, self.username, self.username, int(time.time()), int(time.time())))
            self._conn.commit()
            
            return True, ""

        except Exception as e:
            return False, e
    
    def change_question(self, *args):
        query = f"""
        UPDATE quiz 
        SET 
            timestamp_lastchange = ?,
            question = ?,
            wrong_answer_1 = ?,
            wrong_answer_2 = ?,
            wrong_answer_3 = ?,
            correct_answer = ?,
            category = ?,
            editor = ?                
        WHERE quiz_id = ?
        """

        try:
            self._cur.execute(query, (int(time.time()), *args))
            self._conn.commit()
            return True, ""

        except Exception as e:
            return False, e

    def delete_question(self, primarykey):
        query = """
        SELECT * FROM quiz WHERE quiz_id = ?
        """
        try:
            self._cur.execute(query, (primarykey,))

            data = self._cur.fetchone()
            
            if data is None:
                raise Exception("Zu löschendes Quiz existiert nicht")
        
        except Exception as e:
            return False, e

        query = """
        INSERT INTO deleted_quiz (
            old_primarykey,
            question,
            wrong_answer_1,
            wrong_answer_2,
            wrong_answer_3,
            correct_answer,
            category,
            author,
            editor,
            timestamp_creation,
            timestamp_lastchange            
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            self._cur.execute(query, (*data, ))
        
        except Exception as e:
            return False, e


        query = """
        DELETE FROM quiz WHERE quiz_id = ?
        """

        try:
            self._cur.execute(query, (primarykey,))
            self._conn.commit()
            return True, ""
        
        except Exception as e:
            return False, e  

    def new_complain(self, quiz_id, comment, suggested_answer, username):
        query = """
        INSERT INTO complained_questions (
            quiz_id,
            comment,
            suggested_answer,
            username,
            timestamp
        ) VALUES (?, ?, ?, ?, ?)
        """

        try:
            self._cur.execute(query, (quiz_id, comment, suggested_answer, username, int(time.time())))
            self._conn.commit()

            return True, ""
        
        except Exception as e:
            return False, e


    def __del__(self):
        self._conn.close()


if __name__ == "__main__":
    quiz = QuizDatabase("Database/quiz.db", "admin")
    a = quiz.delete_question(28)
    print(a)


