Use SchoolDB;

Create table Teachers (
	teache_id INT AUTO_INCREMENT PRIMARY KEY,
    name varchar(50),
    subject_id INT
);

CREATE TABLE Subjects (
	subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(50)
);

INSERT INTO Subjects (subject_name) VALUES
('Mathematics'),   -- id = 1
('Science'),       -- id = 2
('English'),       -- id = 3
('History'),       -- id = 4
('Geography');     -- id = 5 (no teacher yet)

INSERT INTO Teachers (name, subject_id) VALUES
('Rahul Sir', 1),   -- Mathematics
('Priya Madam', 2), -- Science
('Arjun Sir', NULL),-- No subject assigned
('Neha Madam', 3);  -- English

-- INNER Join

select t.name, t.subject_id, s.subject_name
from Teachers t
INNER JOIN Subjects s
ON t.subject_id = s.subject_id;

-- LEFT JOIN

select t.name, t.subject_id, s.subject_name
from Teachers t
LEFT JOIN Subjects s
ON t.subject_id = s.subject_id;

-- RIGHT JOIN

select t.name, t.subject_id, s.subject_name
from Teachers t
RIGHT JOIN Subjects s
ON t.subject_id = s.subject_id;

-- FULL JOIN

select t.name, t.subject_id, s.subject_name
from Teachers t
LEFT JOIN Subjects s
ON t.subject_id = s.subject_id

UNION

select t.name, t.subject_id, s.subject_name
from Teachers t
RIGHT JOIN Subjects s
ON t.subject_id = s.subject_id;