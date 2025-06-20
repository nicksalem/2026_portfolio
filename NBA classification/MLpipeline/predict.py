import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def model_predictions(model, X_test,y_test,le, save_dir=None):

    y_proba = model.predict_proba(X_test)
    y_pred = model.predict(X_test)

    class_labels = le.classes_
    if le:
        y_pred_labels = le.inverse_transform(y_pred)
        y_test_labels = le.inverse_transform(y_test)
        class_labels = le.classes_
    else:
        class_labels = [f"class_{i}" for i in range(y_proba.shape[1])]

    # Create a dictionary for class probability columns
    proba_df = pd.DataFrame(y_proba, columns=[f"proba_{label}" for label in class_labels])

    # Build the final DataFrame
    predictions_df = pd.DataFrame({
        'actual': y_test_labels, #type:ignore
        'predicted': y_pred_labels, #type:ignore
        'timestamp': datetime.now().isoformat() #type:ignore
    }).reset_index(drop=True)

    predictions_df['correct'] = np.where(predictions_df['actual'] == predictions_df['predicted'],1,0)

    predictions_df = pd.concat([predictions_df, proba_df], axis=1)
 
    if save_dir:
        save_path = os.path.join(save_dir,"predictions.csv")
        predictions_df.to_csv(save_path, index=False)
        print(f"Predictions saved to: {save_path}")

    # Use 'macro', 'weighted', or 'micro' depending on your goal
    print("Precision (macro):", precision_score(y_test, y_pred, average='macro'))
    print("Recall (macro):", recall_score(y_test, y_pred, average='macro'))
    print("F1 Score (macro):", f1_score(y_test, y_pred, average='macro'))

    # Optional: 'weighted' is often good if classes are imbalanced
    print("Precision (weighted):", precision_score(y_test, y_pred, average='weighted'))

    # Classification report handles all classes
    print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))

    # Custom class order
    custom_order = ['C', 'PF', 'SF', 'SG', 'PG']

    # Convert custom label order to integer label indices
    custom_indices = le.transform(custom_order)

    # Compute confusion matrix in desired label order
    cm = confusion_matrix(y_test, y_pred, labels=custom_indices)

    # Display with custom labels
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=custom_order)
    disp.plot(cmap='Blues', xticks_rotation=45)
    plt.title("Confusion Matrix: Position Ordered")
    plt.grid(False)
    plt.show()

    return y_proba, predictions_df