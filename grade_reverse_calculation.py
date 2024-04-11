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

def subjectGradeCalculation(subject, gpa):
    # Filter graded subjects
    graded_subjects = {subject: data for subject, data in grade_dict.items() if data['grade']}
    
    # Calculate the numerator (sum of credits of graded subjects)
    total_credits = sum(subject_data['credit'] for subject_data in graded_subjects.values())+ grade_dict[selected_subject]['credit']
    print(f"Total Credits: {total_credits:.2f}")
    # Calculate the denominator (sum of products of credit and grade for graded subjects)
    total_weighted_grade = sum(grade_translation[subject_data['grade']] * subject_data['credit'] for subject_data in graded_subjects.values())
    print(f"Total Weighted of Graded subjects: {total_weighted_grade:.2f}")
    print(f"credit of {subject}: {grade_dict[subject]['credit']}")
    # Calculate the selected_subject_grade
    selected_subject_grade = ((gpa * total_credits) - total_weighted_grade)/grade_dict[subject]['credit']
    # print mapped selected subject grade
    print(f"Selected Subject[{subject}] Grade: {list(grade_translation.keys())[list(grade_translation.values()).index(selected_subject_grade)]}, {selected_subject_grade:.2f}")
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
                raise ValueError("Invalid selection. Please enter a number between 1 and", len(grade_dict)+1)
            
            selected_subject = list(grade_dict.keys())[selection - 1]
            if grade_dict[selected_subject]['grade']:
                raise ValueError("This subject has already been graded. Please select another subject.")
            
            break
        except ValueError as e:
            print_error(str(e))

    print("Selected Subject:", selected_subject)

    while True:
        try:
            grade_input = float(input("Enter the current GPS: "))
            if grade_input <= 4.00:
                break
            else:
                raise ValueError("The GPA cannot be more than 4.00. Please try again.")
        except ValueError as e:
            print_error(str(e))

    subjectGradeCalculation(selected_subject, grade_input)
    # Convert grade_dict to JSON with readability
    grade_dict_json = json.dumps(grade_dict, indent=4)

    # Write grade_dict_json to a separate JSON file
    with open('grade_dict.json', 'w') as json_file:
        json_file.write(grade_dict_json)

    print("Grade dictionary saved to grade_dict.json")





