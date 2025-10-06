use SchoolDB;

insert into Students (name, age, course, marks)
values ('Rahul', 21, 'AI', 85);

insert into Students (name, age, course, marks)
values 
('Priya', 22, 'ML', 90),
('Arjun', 20, 'Data Science', 78);

select * from Students;

select name, marks from Students;

select * from Students where marks > 80;

update Students
SET marks = 95, course = 'Advanced AI'
WHERE id = 4;

-- UPDATE Students SET course = 'AI'; 

DELETE FROM Students WHERE id = 3;

CREATE TABLE Employees (
	id INT auto_increment primary key,
    name varchar(50) not null,
    age INT,
    department varchar(50),
    salary decimal(10,2)
);

