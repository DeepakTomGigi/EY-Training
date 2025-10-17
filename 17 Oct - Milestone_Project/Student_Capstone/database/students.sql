CREATE DATABASE Student_DB;
USE Student_DB;


-- Create students table
CREATE TABLE students (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    Course VARCHAR(100)
);


select * from students;

