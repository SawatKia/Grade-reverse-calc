import json
import sys
def print_error(message):
    # ANSI escape code for red color
    print("\033[91m" + message + "\033[0m", file=sys.stderr)

def load_grade_dict_from_json(file_path):
    try:
        with open(file_path, 'r') as json_file:
            grade_dict = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        grade_dict = {}
    return grade_dict

def subjectGradeCalculation(subject, gps):
    # Filter graded subjects
    graded_subjects = {}
    for subject_name, subject_data in grade_dict.items():
        if subject_data['grade']:
            graded_subjects[subject_name] = subject_data
    
    # Calculate the numerator (sum of credits of graded subjects)
    total_credits = 0
    for subject_data in graded_subjects.values():
        total_credits += subject_data['credit']
    total_credits += grade_dict[subject]['credit']
    print(f"Total Credits: {total_credits:.2f}")
    # Calculate the denominator (sum of products of credit and grade for graded subjects)
    total_weighted_grade = 0
    for subject_data in graded_subjects.values():
        grade_value = grade_translation[subject_data['grade']]
        total_weighted_grade += grade_value * subject_data['credit']
    print(f"Total Weighted of Graded subjects: {total_weighted_grade:.2f}")
    subject_credit = grade_dict[subject]['credit']
    print(f"credit of {subject}: {subject_credit}")
    # Calculate the selected_subject_grade
    selected_subject_grade = ((gps * total_credits) - total_weighted_grade) / subject_credit
    selected_subject_grade = round(selected_subject_grade)
    # map selected subject grade to letter
    selected_subject_letter_grade = list(grade_translation.keys())[list(grade_translation.values()).index(selected_subject_grade)]
    print(f"Selected Subject[{subject}] Grade: {selected_subject_letter_grade}, {selected_subject_grade:.2f}")
    # add the grade to certain subject in  the grade_dict
    grade_dict[subject]['grade'] = list(grade_translation.keys())[list(grade_translation.values()).index(selected_subject_grade)]


if __name__ == '__main__':
    # Load grade_dict from JSON file
    grade_dict = load_grade_dict_from_json('grade_dict.json')
    grade_translation = {
        'A': 4.0,
        'B+': 3.5,
        'B': 3.0,
        'C+': 2.5,
        'C': 2.0,
        'D+': 1.5,
        'D': 1.0,
        'F': 0.0
    }

    # If there are no subjects in the dictionary, prompt the user to create new data
    if not grade_dict:
        print("No data found. Let's create new data.")
        while True:
            subject_name = input("Enter subject name: ")
            credit = int(input("Enter credit for the subject: "))
            grade = input("Enter grade for the subject (enter in letter grade, leave blank if not graded yet): ")
            
            grade_dict[subject_name] = {'credit': credit, 'grade': grade}
            
            choice = input("Do you want to add another subject? (yes/no): ")
            if choice.lower() != 'yes':
                break

    # Print available subjects for grading
    print("Available Subjects:")
    for i, subject in enumerate(grade_dict.keys()):
        if not grade_dict[subject]['grade']:
            print(f"{i+1}. {subject}")

    # Select the subject that has recently been graded
    while True:
        try:
            selection = int(input("select the number of the subject that has been graded recently: "))
            if selection < 1 or selection > len(grade_dict):
                raise ValueError(f"Invalid selection. Please enter a number between 0 to {len(grade_dict)+1}")
            
            selected_subject = list(grade_dict.keys())[selection - 1]
            if grade_dict[selected_subject]['grade']:
                raise ValueError("This subject has already been graded. Please select another subject.")
            
            break
        except ValueError as e:
            print_error(str(e))

    print("Selected Subject: " + "\033[1;36m" + selected_subject + "\033[0m")

    while True:
        try:
            grade_input = float(input("Enter the current GPS: "))
            if grade_input <= 4.00:
                break
            else:
                raise ValueError("The GPS cannot be more than 4.00. Please try again.")
        except ValueError as e:
            print_error(str(e))

    subjectGradeCalculation(selected_subject, grade_input)
    # Convert grade_dict to JSON with readability
    grade_dict_json = json.dumps(grade_dict, indent=4)

    # Write grade_dict_json to a separate JSON file
    with open('grade_dict.json', 'w') as json_file:
        json_file.write(grade_dict_json)

    print("\033[1;42m" + "Grade dictionary saved to grade_dict.json" + "\033[0m")





