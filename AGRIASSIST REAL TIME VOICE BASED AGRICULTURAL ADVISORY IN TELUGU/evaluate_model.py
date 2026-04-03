from utils.nlp_model import IntentClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pandas as pd

# Initialize classifier
classifier = IntentClassifier()

# -------------------------------
# Test dataset (manually labelled)
# -------------------------------
test_data = [
    ("నమస్తే", "greeting"),
    ("నువ్వు నాకు ఏ విధంగా సహాయం చేయగలవు", "help"),
    ("మెదక్ వాతావరణం", "weather"),
    ("విశాఖపట్నం వాతావరణం", "weather"),
    ("మిర్చి ధర", "price"),
    ("పత్తి మార్కెట్ ధర", "price"),
    ("వరి సాగు సలహా", "advisory"),
    ("మొక్కజొన్న ఎరువు", "advisory"),
    ("రైతు బంధు పథకం", "scheme"),
    ("ప్రధానమంత్రి ఫసల్ బీమా యోజన", "scheme"),
    ("పథకాల గురించి చెప్పగలవా", "scheme"),
]

# Separate actual and predicted labels
y_true = []
y_pred = []

for text, actual_intent in test_data:
    predicted_intent, _ = classifier.predict(text)
    y_true.append(actual_intent)
    y_pred.append(predicted_intent)

# -------------------------------
# Evaluation Metrics
# -------------------------------
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average="weighted")
recall = recall_score(y_true, y_pred, average="weighted")
f1 = f1_score(y_true, y_pred, average="weighted")

# -------------------------------
# Metrics Table
# -------------------------------
metrics_table = pd.DataFrame({
    "Metric": ["Accuracy", "Precision", "Recall", "F1-Score"],
    "Value": [
        round(accuracy, 3),
        round(precision, 3),
        round(recall, 3),
        round(f1, 3)
    ]
})

print("\n📊 Evaluation Metrics:\n")
print(metrics_table.to_string(index=False))

# -------------------------------
# Confusion Matrix
# -------------------------------
labels = sorted(set(y_true))
cm = confusion_matrix(y_true, y_pred, labels=labels)

confusion_df = pd.DataFrame(
    cm,
    index=[f"Actual_{l}" for l in labels],
    columns=[f"Predicted_{l}" for l in labels]
)

print("\n📊 Confusion Matrix:\n")
print(confusion_df)
