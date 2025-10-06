CREATE DATABASE HospitalDB;
USE HospitalDB;

CREATE TABLE Patients (
	patient_id INT PRIMARY KEY,
	name VARCHAR(50),
	age INT,
	gender CHAR(1),
	city VARCHAR(50)
);

-- Patients Table
CREATE TABLE Patients (
	patient_id INT PRIMARY KEY,
	name VARCHAR(50),
	age INT,
	gender CHAR(1),
	city VARCHAR(50)
);

-- Doctors Table
CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(50),
    specialization VARCHAR(50),
    experience INT
);

-- Appointments Table
CREATE TABLE Appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

-- MedicalRecords Table
CREATE TABLE MedicalRecords (
    record_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    diagnosis VARCHAR(100),
    treatment VARCHAR(100),
    date DATE,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

-- Billing Table
CREATE TABLE Billing (
    bill_id INT PRIMARY KEY,
    patient_id INT,
    amount DECIMAL(10,2),
    bill_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);

-- Insert Patients (10)
INSERT INTO Patients VALUES
(1, 'Seethal', 22, 'F', 'Kochi'),
(2, 'Paul', 32, 'M', 'Mumbai'),
(3, 'Rajesh', 28, 'M', 'Kolkata'),
(4, 'Pooja', 40, 'F', 'Bengaluru'),
(5, 'Swathy', 23, 'F', 'Hyderabad'),
(6, 'Joshi', 27, 'M', 'Pune'),
(7, 'Vyshnav', 36, 'M', 'Chennai'),
(8, 'Neha', 28, 'F', 'Ahmedabad'),
(9, 'Karan', 45, 'M', 'Jaipur'),
(10, 'Sanjay', 30, 'M', 'Lucknow');

-- Insert Doctors (5)
INSERT INTO Doctors VALUES
(1, 'Dr. Raj Malhotra', 'Cardiology', 15),
(2, 'Dr. Meena Iyer', 'Orthopedics', 12),
(3, 'Dr. Sunil Deshmukh', 'Pediatrics', 10),
(4, 'Dr. Aarti Singh', 'Neurology', 8),
(5, 'Dr. Mohan Reddy', 'Dermatology', 20);

-- Insert Appointments
INSERT INTO Appointments VALUES
(1, 1, 1, '2025-10-01', 'Completed'),
(2, 2, 3, '2025-10-02', 'Scheduled'),
(3, 3, 2, '2025-10-03', 'Cancelled'),
(4, 4, 1, '2025-10-04', 'Completed'),
(5, 5, 4, '2025-10-05', 'Scheduled'),
(6, 6, 5, '2025-10-06', 'Completed'),
(7, 7, 1, '2025-10-07', 'Scheduled'),
(8, 8, 3, '2025-10-08', 'Completed'),
(9, 9, 2, '2025-10-09', 'Completed'),
(10, 10, 4, '2025-10-10', 'Scheduled');

-- Insert Medical Records
INSERT INTO MedicalRecords VALUES
(1, 1, 1, 'Hypertension', 'Medication', '2025-10-01'),
(2, 4, 1, 'Chest Pain', 'ECG & Medication', '2025-10-04'),
(3, 6, 5, 'Skin Allergy', 'Ointment', '2025-10-06'),
(4, 8, 3, 'Flu', 'Rest & Medication', '2025-10-08'),
(5, 9, 2, 'Back Pain', 'Physiotherapy', '2025-10-09');

-- Insert Bills
INSERT INTO Billing VALUES
(1, 1, 5000.00, '2025-10-02', 'Paid'),
(2, 2, 2000.00, '2025-10-03', 'Unpaid'),
(3, 3, 1500.00, '2025-10-04', 'Paid'),
(4, 4, 3000.00, '2025-10-05', 'Unpaid'),
(5, 5, 2500.00, '2025-10-06', 'Paid'),
(6, 6, 1800.00, '2025-10-07', 'Unpaid'),
(7, 7, 4000.00, '2025-10-08', 'Paid'),
(8, 8, 2200.00, '2025-10-09', 'Unpaid'),
(9, 9, 3500.00, '2025-10-10', 'Paid'),
(10, 10, 2700.00, '2025-10-11', 'Unpaid');

-- Basic Queries

-- 1
SELECT p.name
FROM Patients p
JOIN Appointments a ON p.patient_id = a.patient_id
JOIN Doctors d ON d.doctor_id = a.doctor_id
WHERE d.specialization = 'cardiology';

-- 2
SELECT * FROM Appointments WHERE doctor_id = 1;

-- 3
SELECT b.bill_id, p.name, b.amount, b.bill_date, b.status
FROM Billing b
JOIN Patients p ON b.patient_id = p.patient_id
WHERE b.status = 'Unpaid';

-- Stored Procedures

-- 4
DELIMITER $$
CREATE PROCEDURE GetPatientHistory(IN pid INT)
BEGIN
    SELECT mr.record_id, mr.date, d.name AS doctor_name, mr.diagnosis, mr.treatment
    FROM MedicalRecords mr
    JOIN Doctors d ON mr.doctor_id = d.doctor_id
    WHERE mr.patient_id = pid
    ORDER BY mr.date DESC;
END $$
DELIMITER ;

CALL GetPatientHistory(1);

-- 5
DELIMITER $$
CREATE PROCEDURE GetDoctorAppointments(IN did INT)
BEGIN
    SELECT a.appointment_id, a.appointment_date, a.status, p.name AS patient_name, p.age, p.gender, p.city
    FROM Appointments a
    JOIN Patients p ON a.patient_id = p.patient_id
    WHERE a.doctor_id = did
    ORDER BY a.appointment_date DESC;
END $$
DELIMITER ;

CALL GetDoctorAppointments(1);