CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE sports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sport TEXT NOT NULL
);

CREATE TABLE registrations (
    student_id INTEGER,
    sport_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (sport_id) REFERENCES sports(id)
);

INSERT INTO sports (sport) VALUES
('Football'), ('Basketball'), ('Tennis'), ('Swimming'),
('Volleyball'), ('Athletics'), ('Rugby'), ('Hockey');