import json
import os
import cv2

# Load the existing JSON file
json_path = "question_bank.json"
if os.path.exists(json_path):
    with open(json_path, "r") as file:
        questions = json.load(file)
else:
    questions = []  # Start with an empty list if the file does not exist

directory = "question_bank_pictures"
question_index = len(questions)  # Start indexing from the current count

# Loop over the filenames in the directory
for filename in os.listdir(directory):
    # Join the directory path and filename to get the full path of the image
    filepath = os.path.join(directory, filename)

    # Read the image from the full path
    img = cv2.imread(filepath)

    # Check if the image was loaded successfully
    if img is not None:
        # Display the image
        cv2.imshow("Image", img)
        # Wait for a key press
        answer = input("Enter the number of the correct answer: ")
        cv2.waitKey(0)
        # Close the window
        cv2.destroyAllWindows()

        # Append the new question data to the list
        questions.append({"question_id": f"question_{question_index}",
                          "question_path": filepath,
                          "answer": answer})
        question_index += 1
    else:
        print(f"Failed to load image: {filepath}")

# Save the updated questions back to the JSON file
with open(json_path, "w") as file:
    json.dump(questions, file, indent=4)
