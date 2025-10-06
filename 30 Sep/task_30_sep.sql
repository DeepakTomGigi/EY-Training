CREATE DATABASE UniversityDB;
USE UniversityDB;
-- Students Table
CREATE TABLE Students (
student_id INT PRIMARY KEY,
name VARCHAR(50),
city VARCHAR(50)
);
-- Courses Table
CREATE TABLE Courses (
course_id INT PRIMARY KEY,
course_name VARCHAR(50),
credits INT
);
-- Enrollments Table
CREATE TABLE Enrollments (
enroll_id INT PRIMARY KEY,
student_id INT,
course_id INT,
grade CHAR(2),
FOREIGN KEY (student_id) REFERENCES Students(student_id),
FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
-- Insert Students
INSERT INTO Students VALUES
(1, 'Rahul', 'Mumbai'),
(2, 'Priya', 'Delhi'),
(3, 'Arjun', 'Bengaluru'),
(4, 'Neha', 'Hyderabad'),
(5, 'Vikram', 'Chennai');
-- Insert Courses
INSERT INTO Courses VALUES
(101, 'Mathematics', 4),
(102, 'Computer Science', 3),
(103, 'Economics', 2),
(104, 'History', 3);
-- Insert Enrollments
INSERT INTO Enrollments VALUES
(1, 1, 101, 'A'),
(2, 1, 102, 'B'),
(3, 2, 103, 'A'),
(4, 3, 101, 'C'),
(5, 4, 102, 'B'),
(6, 5, 104, 'A');

-- TASK:1 Single Table
-- 1
DELIMITER $$

CREATE PROCEDURE GetAllStudents()
BEGIN
	SELECT student_id, name
    FROM Students; 
END $$

DELIMITER ;
CALL GetAllStudents();

-- 2
DELIMITER $$

CREATE PROCEDURE GetAllCourses()
BEGIN
	SELECT course_id, course_name
    FROM Courses; 
END $$

DELIMITER ;
CALL GetAllCourses();

-- 3 
DELIMITER $$

CREATE PROCEDURE GetAllCityStudents(IN city_name VARCHAR(50))
BEGIN
	SELECT student_id, name
    FROM Students
    WHERE city = city_name; 
END $$

DELIMITER ;
CALL GetAllCityStudents('Mumbai');

-- TASK:2 Two-table Joins
-- 4
DELIMITER $$

CREATE PROCEDURE GetStudentsWithCourses()
BEGIN
	SELECT e.enroll_id, s.name, c.course_name
    FROM  Enrollments e
    JOIN Students s ON e.student_id = s.student_id
    JOIN Courses c ON e.course_id = c.course_id;
    
END $$

DELIMITER ;
CALL GetStudentsWithCourses();

-- 5
DELIMITER $$

CREATE PROCEDURE GetStudentsInCourses(IN courseId INT)
BEGIN
	SELECT e.enroll_id, s.name, c.course_name
    FROM  Enrollments e
    JOIN Students s ON e.student_id = s.student_id
    JOIN Courses c ON e.course_id = c.course_id
    WHERE c.course_id = courseId;
    
END $$

DELIMITER ;

CALL GetStudentsInCourses(101);

-- 6

DELIMITER $$

CREATE PROCEDURE GetCountStudentsPerCourse()
BEGIN
    SELECT c.course_id, c.course_name, COUNT(e.student_id) AS student_count
    FROM Courses c
    LEFT JOIN Enrollments e ON c.course_id = e.course_id
    GROUP BY c.course_id, c.course_name;
END $$

DELIMITER ;

CALL GetCountStudentsPerCourse();

-- 7

DELIMITER $$
CREATE PROCEDURE GetListStudentsCoursesGrades()
BEGIN
    SELECT s.student_id, s.name, c.course_name, e.grade
    FROM Students s
    JOIN Enrollments e ON s.student_id = e.student_id
    JOIN Courses c ON e.course_id = c.course_id;
END $$
DELIMITER ;

CALL GetListStudentsCoursesGrades();

-- 8 

DELIMITER $$
CREATE PROCEDURE GetCoursesByStudent(IN sid INT)
BEGIN
    SELECT c.course_id, c.course_name, c.credits, e.grade
    FROM Courses c
    JOIN Enrollments e ON c.course_id = e.course_id
    WHERE e.student_id = sid;
END $$
DELIMITER ;

CALL GetCoursesByStudent(1);

-- 9 

DELIMITER $$
CREATE PROCEDURE AverageGradePerCourse()
BEGIN
    SELECT 
        c.course_id,
        c.course_name,
        ROUND(AVG(
            CASE e.grade
                WHEN 'A' THEN 4
                WHEN 'B' THEN 3
                WHEN 'C' THEN 2
                WHEN 'D' THEN 1
                ELSE 0
            END
        ), 2) AS average_grade_numeric
    FROM Courses c
    JOIN Enrollments e ON c.course_id = e.course_id
    GROUP BY c.course_id, c.course_name;
END $$
DELIMITER ;

CALL AverageGradePerCourse();