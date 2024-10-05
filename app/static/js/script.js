$(document).ready(() => {
    fetchSchedule();
});

function fetchSchedule() {
    const className = window.location.pathname.split("/").pop(); // Get the last part of the path
    console.log("Fetching schedule for class:", className); // Log the class name for debugging

    $.getJSON(`/api/schedule?class_name=${className}`, function(data) {
        console.log("Schedule Data:", data); // Log the response data
        window.scheduleData = data;
        renderSchedule(window.scheduleData);
    }).fail((jqXHR, textStatus, errorThrown) => {
        console.error("Error:", textStatus, errorThrown); // Log detailed error info
        alert("Failed to load schedule data.");
    });
}

function renderSchedule(data) {
    const scheduleContainer = $("#schedule");
    scheduleContainer.empty();  // Clear previous content

    const daysOrder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

    daysOrder.forEach(day => {
        if (data[day]) {
            const dayCard = $(`
                <div class="bg-white rounded-lg shadow-lg p-4 border border-gray-300 mb-4">
                    <h2 class="font-bold text-3xl text-blue-600 mb-4">${day}</h2>
                    <div class="space-y-3">
                        ${data[day].map(classInfo => `
                            <div class="class-item p-3 border border-gray-300 rounded-lg bg-gray-50 hover:bg-gray-100 transition duration-300">
                                <h4 class="font-semibold text-lg">${classInfo.name}</h4>
                                <p><strong>Instructor:</strong> ${classInfo.instructor}</p>
                                <p><strong>Weeks:</strong> ${classInfo.weeks}</p>
                                <p><strong>Time:</strong> ${classInfo.time}</p>
                                <p><strong>Location:</strong> ${classInfo.location}</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `);
            scheduleContainer.append(dayCard);
        }
    });
}

function showSuggestions() {
    const searchTerm = $("#search-input").val().toLowerCase();
    const suggestionsContainer = $("#suggestions");
    suggestionsContainer.empty();  // Clear previous suggestions

    // Filter classes for suggestions from the correct class data
    const suggestions = [];

    for (const day of Object.keys(window.scheduleData)) {
        for (const classInfo of window.scheduleData[day]) {
            if (classInfo.name.toLowerCase().includes(searchTerm) && !suggestions.includes(classInfo.name)) {
                suggestions.push(classInfo.name);
            }
        }
    }

    if (suggestions.length > 0) {
        suggestions.forEach(suggestion => {
            suggestionsContainer.append(`
                <div class="py-2 px-4 hover:bg-gray-200 cursor-pointer" onclick="selectSuggestion('${suggestion}')">
                    ${suggestion}
                </div>
            `);
        });
        suggestionsContainer.removeClass("hidden"); // Show suggestions
    } else {
        suggestionsContainer.addClass("hidden"); // Hide if no suggestions
    }
}

function selectSuggestion(suggestion) {
    $("#search-input").val(suggestion); // Set input to selected suggestion
    $("#suggestions").addClass("hidden"); // Hide suggestions
    searchClasses(); // Trigger the search
}

function searchClasses() {
    const searchTerm = $("#search-input").val().toLowerCase();
    const filteredData = {};

    for (const [day, classes] of Object.entries(window.scheduleData)) {
        const filteredClasses = classes.filter(classInfo => 
            classInfo.name?.toLowerCase().includes(searchTerm)
        );

        if (filteredClasses.length > 0) {
            filteredData[day] = filteredClasses;
        }
    }

    if (Object.keys(filteredData).length > 0) {
        // Redirect to the class details page with the search term and class name
        window.location.href = `/class_details?searchTerm=${encodeURIComponent(searchTerm)}&class_name=${window.location.pathname.split("/").pop()}`;
    } else {
        alert("No classes found matching your search.");
    }
}


// Show today's schedule
function showTodaySchedule() {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const today = days[new Date().getDay()];

    if (window.scheduleData && window.scheduleData[today]) {
        const todaysClasses = { [today]: window.scheduleData[today] };
        renderSchedule(todaysClasses);
    } else {
        alert("No classes scheduled for today.");
    }
}
function clearSearch(){
    window.location.reload()
}
// Show weekly schedule
function showWeeklySchedule() {
    if (window.scheduleData) {
        renderSchedule(window.scheduleData);
    } else {
        alert("No schedule data found.");
    }
}
