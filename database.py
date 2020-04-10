import sqlite3


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
            admin BOOL
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
        self._conn.commit()

    def new_user(self, username, password_hash, f_name, l_name, email, admin=False):
        # Check if username exists
        exists = self._cur.execute("SELECT * FROM user WHERE username = ?", (username,))

        if exists is None:
            query = """
            INSERT INTO user (username, password, f_name, l_name, email, admin) VALUES (
                ?, ?, ?, ?, ?, ?
            )
            """

            try:
                self._cur.execute(query, (username, password_hash, f_name, l_name, admin))
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
        if self.permission:
            query = f"""
            DELETE FROM quiz WHERE quiz_id = ?
            """

            try:
                self._cur.execute(query, (primarykey))
                self._conn.commit()
                return True, ""
            
            except Exception as e:
                return False, e
    
        self._conn.close()        

    def __del__(self):
        self._conn.close()