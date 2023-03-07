-- CS3810 - Principles of Database Systems - Spring 2021
-- Instructor: Thyago Mota
-- Description: enrollments database
-- Student(s) Name(s): Evan Birt & Nicole Weickert & Naji Shamus

DROP DATABASE IF EXISTS enrollments;
CREATE DATABASE enrollments;
USE enrollments;

CREATE TABLE courses (
    code       VARCHAR(7)  NOT NULL PRIMARY KEY,
    title      VARCHAR(35) NOT NULL,
    instructor VARCHAR(15) NOT NULL,
    `max`      INT         NOT NULL,
    actual     INT         DEFAULT 0,
    CHECK (actual >= 0 AND actual <= `max`)
);

INSERT INTO courses (code, title, instructor, `max`)
VALUES	('CS1030', 'Computer Science Principles',    'Jody Paul',     5),
	('CS1050', 'Computer Science 1',             'David Kramer',  3),
	('CS2050', 'Computer Science 2',             'Steve Geinitz', 3),
	('CS3810', 'Principles of Database Systems', 'Thyago Mota',   2);

CREATE TABLE students (
    id   INT         NOT NULL PRIMARY KEY,
    name VARCHAR(15) NOT NULL
);

INSERT INTO students
VALUES	(1, 'Perry Rhodan'),
	(2, 'Icho Tolot'),
	(3, 'Deshan Apian');

CREATE TABLE enrollments (
    code VARCHAR(10) NOT NULL,
    id   INT         NOT NULL,
    PRIMARY KEY (code, id),
    FOREIGN KEY (code) REFERENCES courses(code),
    FOREIGN KEY (id)   REFERENCES students(id)
);

CREATE USER 'enrollments' IDENTIFIED BY '135791';
GRANT ALL ON enrollments.* TO 'enrollments';

-- TODO: create a trigger name enroll_student that automatically increments the actual field in courses whenever a student enrolls in a course
DELIMITER |
DROP TRIGGER IF EXISTS enroll_student |
CREATE TRIGGER enroll_student
    AFTER INSERT ON enrollments
    FOR EACH ROW
    BEGIN
    UPDATE courses
	    SET actual = actual + 1
	    WHERE code = NEW.code;
    END
|
DELIMITER ;

-- TODO: create a trigger name drop_student that automatically decrements the actual field in courses whenever a student drops from a course
DELIMITER |
DROP TRIGGER IF EXISTS drop_student |
CREATE TRIGGER drop_student
    AFTER DELETE ON enrollments
    FOR EACH ROW
    BEGIN
    UPDATE courses
	    SET actual = actual - 1
	    WHERE code = OLD.code;
    END
|
DELIMITER ;

-- TODO: create a stored procedure name list_students that returns a list of ids and names of all students currently enrolled in a given course 
DELIMITER |
DROP PROCEDURE IF EXISTS list_students |
CREATE PROCEDURE list_students(courseCode VARCHAR(7))
	SELECT students.id, students.name
	FROM Enrollments
	NATURAL JOIN students
	WHERE code = courseCode;
|
DELIMITER ;