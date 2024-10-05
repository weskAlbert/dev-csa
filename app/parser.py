def parse_schedule(filename):
    schedule = {}
    
    with open(filename, 'r', encoding='utf-8') as file:
        current_day = ""
        for line in file:
            line = line.strip()
            # Detect days of the week
            if line.endswith(":"):
                current_day = line[:-1].strip()  # Get the day without the colon
                schedule[current_day] = []
                #print(f"Detected day: {current_day}")  # Debugging output
            # Detect class name and initialize entry
            elif line and not line.startswith("Instructor") and not line.startswith("Weeks") and not line.startswith("Time") and not line.startswith("Location"):
                class_info = {"name": line}
                schedule[current_day].append(class_info)
                #print(f"Added class: {class_info}")  # Debugging output
            # Populate class details
            elif "Instructor" in line:
                if schedule[current_day]:  # Ensure there is a class to add instructor to
                    schedule[current_day][-1]["instructor"] = line.split(": ", 1)[1].strip()
                    #print(f"Set instructor for {schedule[current_day][-1]['name']}: {schedule[current_day][-1]['instructor']}")  # Debugging output
                else:
                    print(f"Warning: No class found for instructor assignment on {current_day}.")  # Debugging output
            elif "Weeks" in line:
                if schedule[current_day]:
                    schedule[current_day][-1]["weeks"] = line.split(": ", 1)[1].strip()
                    #print(f"Set weeks for {schedule[current_day][-1]['name']}: {schedule[current_day][-1]['weeks']}")  # Debugging output
                else:
                    print(f"Warning: No class found for weeks assignment on {current_day}.")  # Debugging output
            elif "Time" in line:
                if schedule[current_day]:
                    schedule[current_day][-1]["time"] = line.split(": ", 1)[1].strip()
                    #print(f"Set time for {schedule[current_day][-1]['name']}: {schedule[current_day][-1]['time']}")  # Debugging output
                else:
                    print(f"Warning: No class found for time assignment on {current_day}.")  # Debugging output
            elif "Location" in line:
                if schedule[current_day]:
                    schedule[current_day][-1]["location"] = line.split(": ", 1)[1].strip()
                    #print(f"Set location for {schedule[current_day][-1]['name']}: {schedule[current_day][-1]['location']}")  # Debugging output
                else:
                    print(f"Warning: No class found for location assignment on {current_day}.")  # Debugging output
    return schedule
