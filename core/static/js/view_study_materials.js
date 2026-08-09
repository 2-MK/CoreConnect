// =====================================
// Subjects for Each Semester
// =====================================

const subjects = {

    "Semester 1": [
        "20MCA101- Mathematical Foundations for Computing ",
        "20MCA103- Digital Fundamentals & Computer Architecture",
        "20MCA105- Advanced Data Structures",
        "20MCA107- Advanced Software Engineering",
        "20MCA131- Programming Lab",
        "20MCA133- Web Programming Lab",
        "20MCA135- Data Structures Lab"
    ],

    "Semester 2": [
        "20MCA102- Avanced Database Management System",
        "20MCA104- Advanced Computer Networks",
        "20MCA162- Applied Statistics",
        "20MCA164- Organisational Behaviour",
        "20MCA188- Artificial Intelligence",
        "20MCA192- IPR and Cyber Laws",
        "20MCA132- Object Oriented Programming",
        "20MCA134- Advanced DBMS Lab",
        "20MCA136- Networking & System Administration Lab"
    ],

    "Semester 3": [
        "20MCA201- Data Science & Machine Learning",
        "20MCA203- Design & Analysis of Algorithms",
        "20MCA263- Cyber Security & Cryptography",
        "20MCA283- Deep Learning",
        "S20MCA287- Bioinformatics",
        "20MCA241- Data Science Lab",
        "20MCA243- Mobile Application Develpoment Lab",
        "20MCA245- Mini Project"
    ],

    "Semester 4": [
        "20MCA242- Comprehensive Viva",
        "20MCA244- Seminar",
        "20MCA246- Main Project"
    ]

};

// =====================================
// Elements
// =====================================

const semester = document.getElementById("semester");
const subject = document.getElementById("subject");

// =====================================
// Load Subjects
// =====================================

function loadSubjects(selectedSemester, selectedSubject = "") {

    subject.innerHTML = "";

    // Default option
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "All Subjects";
    subject.appendChild(defaultOption);

    if (!selectedSemester || !subjects[selectedSemester]) {
        return;
    }

    subjects[selectedSemester].forEach(function (item) {

        const option = document.createElement("option");

        option.value = item;
        option.textContent = item;

        if (item === selectedSubject) {
            option.selected = true;
        }

        subject.appendChild(option);

    });

}

// =====================================
// Semester Change Event
// =====================================

semester.addEventListener("change", function () {

    loadSubjects(this.value);

});

// =====================================
// Page Load
// =====================================

// These variables are defined in the HTML:
//
// const selectedSemester = "...";
// const selectedSubject = "...";

if (typeof selectedSemester !== "undefined") {

    semester.value = selectedSemester;

    loadSubjects(selectedSemester, selectedSubject);

}

// =====================================
// Reset Subject if Semester Cleared
// =====================================

semester.addEventListener("change", function () {

    if (this.value === "") {

        subject.innerHTML = "";

        const option = document.createElement("option");

        option.value = "";
        option.textContent = "All Subjects";

        subject.appendChild(option);

    }

});