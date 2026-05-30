import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("dataset.csv")
X = df[
    [
        "Attendance",
        "StudyHours",
        "Assignments",
        "PreviousMarks"
    ]
]

y = df["FinalMarks"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Model Trained Successfully")