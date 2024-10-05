$(document).ready(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const searchTerm = urlParams.get('searchTerm');
    const className = urlParams.get('class_name');

    // Fetch schedule data based on the class name
    fetch(`/api/schedule?class_name=${className}`)
        .then(response => response.json())
        .then(data => {
            displayClassDetails(data, searchTerm);
        })
        .catch(error => console.error("Error fetching schedule:", error));
});

function displayClassDetails(data, searchTerm) {
    const classInfoContainer = $("#class-info");
    classInfoContainer.empty(); // Clear previous content

    let foundClasses = [];

    // Filter classes based on search term
    for (const [day, classes] of Object.entries(data)) {
        classes.forEach(classInfo => {
            if (classInfo.name?.toLowerCase().includes(searchTerm.toLowerCase())) {
                foundClasses.push({ ...classInfo, day });
            }
        });
    }

    // Render the class details
    if (foundClasses.length > 0) {
        foundClasses.forEach(classInfo => {
            const classDetails = $(`
                <div class="mb-4 p-3 border border-gray-300 rounded-lg bg-gray-50">
                    <h4 class="font-semibold text-xl text-blue-600">${classInfo.name}</h4>
                    <p class="text-m"><strong>Instructor:</strong> ${classInfo.instructor}</p>
                    <p class="text-m"><strong>Weeks:</strong> ${classInfo.weeks}</p>
                    <p class="text-m"><strong>Time:</strong> ${classInfo.time}</p>
                    <p class="text-m"><strong>Location:</strong> ${classInfo.location}</p>
                    <p class="text-m"><strong>Day:</strong> ${classInfo.day}</p>
                </div>
            `);
            classInfoContainer.append(classDetails);
        });
    } else {
        classInfoContainer.append(`<p>No classes found matching "${searchTerm}".</p>`);
    }
}
