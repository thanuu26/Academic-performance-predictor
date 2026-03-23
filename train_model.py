import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import kagglehub
import os

print("1. Downloading dataset via kagglehub...")
path = kagglehub.dataset_download("adilshamim8/student-performance-and-learning-style")
csv_file = [f for f in os.listdir(path) if f.endswith('.csv')][0]
full_path = os.path.join(path, csv_file)

print("2. Loading and preparing data...")
df = pd.read_csv(full_path)

# Clean up any hidden spaces in the column names
df.columns = df.columns.str.strip()

# 1. Define "At Risk" (1) if Exam Score is below 65, else "On Track" (0)
# USING THE EXACT COLUMN NAME: 'ExamScore'
df['is_at_risk'] = (df['ExamScore'] < 65).astype(int)

# 2. Select 4 numeric features using the EXACT COLUMN NAMES from your terminal
features = [
    'Attendance',           # Matches the frontend "Attendance Rate"
    'StudyHours',           # Matches the frontend "Study Hours"
    'OnlineCourses',        # Matches the frontend "Online Courses"
    'AssignmentCompletion'  # Matches the frontend "Assignment Completion"
]

X = df[features]
y = df['is_at_risk']

print("3. Training the Random Forest model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Check how well the model learned
accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Model Accuracy: {accuracy * 100:.2f}%")

print("4. Saving the model...")
joblib.dump(model, 'student_model.pkl')
print("Done! 'student_model.pkl' is ready.")
print("IMPORTANT: Move the new 'student_model.pkl' into your 'predictor' folder to overwrite the old one!")