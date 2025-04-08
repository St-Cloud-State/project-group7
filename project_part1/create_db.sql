-- from our project plan from the questions for 2nf design, just run sqlite3 university.db < create_db.sql to create the university db
CREATE TABLE IF NOT EXISTS Student (
  StudentID VARCHAR(10) PRIMARY KEY,
  Name VARCHAR(100),
  Address VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Course (
  CourseID VARCHAR(10) PRIMARY KEY,
  Name VARCHAR(100),
  Credits INT
);

CREATE TABLE IF NOT EXISTS Section (
  SectionID VARCHAR(10) PRIMARY KEY,
  CourseID VARCHAR(10),
  Semester TEXT CHECK(Semester IN ('Fall', 'Spring', 'Summer')),
  Year INT,
  FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);

CREATE TABLE IF NOT EXISTS Registration (
  StudentID VARCHAR(10),
  SectionID VARCHAR(10),
  Grade CHAR(1),
  PRIMARY KEY (StudentID, SectionID),
  FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
  FOREIGN KEY (SectionID) REFERENCES Section(SectionID)
);
