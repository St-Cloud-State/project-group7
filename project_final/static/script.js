function addStudent() {
    const studentID = document.getElementById('studentID').value;
    const studentName = document.getElementById('studentName').value;
    const studentAddress = document.getElementById('studentAddress').value;

    const studentData = {
        StudentID: studentID,
        Name: studentName,
        Address: studentAddress
    };

    fetch('/api/add_student', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(studentData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        document.getElementById('studentID').value = '';
        document.getElementById('studentName').value = '';
        document.getElementById('studentAddress').value = '';
        showStudents();  // update the list of students
    })
    .catch(error => console.error('Error adding student:', error));
}

function addCourse() {
    const courseID = document.getElementById('courseID').value;
    const courseName = document.getElementById('courseName').value;
    const courseCredits = document.getElementById('courseCredits').value;

    const courseData = {
        CourseID: courseID,
        Name: courseName,
        Credits: courseCredits
    };

    fetch('/api/add_course', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(courseData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        document.getElementById('courseID').value = '';
        document.getElementById('courseName').value = '';
        document.getElementById('courseCredits').value = '';
        showCourses();  // update the list of courses
    })
    .catch(error => console.error('Error adding course:', error));
}

function addSection() {
    const sectionID = document.getElementById('sectionID').value;
    const sectionCourseID = document.getElementById('sectionCourseID').value;
    const sectionSemester = document.getElementById('sectionSemester').value;
    const sectionYear = document.getElementById('sectionYear').value;

    const sectionData = {
        SectionID: sectionID,
        CourseID: sectionCourseID,
        Semester: sectionSemester,
        Year: sectionYear
    };

    fetch('/api/add_section', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sectionData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        document.getElementById('sectionID').value = '';
        document.getElementById('sectionCourseID').value = '';
        document.getElementById('sectionSemester').value = '';
        document.getElementById('sectionYear').value = '';
        showSections();  // update the list of sections
    })
    .catch(error => console.error('Error adding section:', error));
}



function showStudents() {
    fetch('/api/students')
    .then(response => response.json())
    .then(data => {
        const studentsDiv = document.getElementById('studentsList');
        studentsDiv.innerHTML = '';
        data.students.forEach(student => {
            const div = document.createElement('div');
            div.innerHTML = `<strong>${student.StudentID}</strong> - ${student.Name} (${student.Address})`;
            studentsDiv.appendChild(div);
        });
    })
    .catch(error => console.error('Error fetching students:', error));
}

function showCourses() {
    const rubric = document.getElementById('filterRubric').value;
    let url = '/api/courses';
    if (rubric) {
        url += '?rubric=' + encodeURIComponent(rubric);
    }
    fetch(url)
    .then(response => response.json())
    .then(data => {
        const coursesDiv = document.getElementById('coursesList');
        coursesDiv.innerHTML = '';
        data.courses.forEach(course => {
            const div = document.createElement('div');
            div.innerHTML = `<strong>${course.CourseID}</strong> - ${course.Name} (Credits: ${course.Credits})`;
            coursesDiv.appendChild(div);
        });
    })
    .catch(error => console.error('Error fetching courses:', error));
}

function showSections() {
    const courseID = document.getElementById('filterCourseID').value;
    let url = '/api/sections';
    if (courseID) {
        url += '?courseid=' + encodeURIComponent(courseID);
    }
    fetch(url)
    .then(response => response.json())
    .then(data => {
        const sectionsDiv = document.getElementById('sectionsList');
        sectionsDiv.innerHTML = '';
        data.sections.forEach(section => {
            const div = document.createElement('div');
            div.innerHTML = `<strong>${section.SectionID}</strong> - Course: ${section.CourseID}, Semester: ${section.Semester}, Year: ${section.Year}`;
            sectionsDiv.appendChild(div);
        });
    })
    .catch(error => console.error('Error fetching sections:', error));
}

function registerStudent() {
    const studentID = document.getElementById('regStudentID').value;
    const sectionID = document.getElementById('regSectionID').value;

    fetch('/api/register_student', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ StudentID: studentID, SectionID: sectionID })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error registering student:', error));
}

function getSectionStudents() {
    const sectionID = document.getElementById('lookupSectionID').value;

    fetch('/api/section_students?sectionid=' + encodeURIComponent(sectionID))
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('sectionStudentsList');
        container.innerHTML = '';
        data.students.forEach(s => {
            container.innerHTML += `<div>${s.StudentID} - ${s.Name} (${s.Address})</div>`;
        });
    });
}

function getStudentCourses() {
    const studentID = document.getElementById('lookupStudentID').value;

    fetch('/api/student_courses?studentid=' + encodeURIComponent(studentID))
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('studentCoursesList');
        container.innerHTML = '';
        data.courses.forEach(c => {
            container.innerHTML += `<div>${c.CourseID} - ${c.Name} (${c.Credits} credits)</div>`;
        });
    });
}
