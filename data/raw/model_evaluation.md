# Machine Learning Model Evaluation

## Classification Metrics
Accuracy is the proportion of correct predictions. Precision measures how many predicted positives are truly positive. Recall measures how many actual positives are detected. The F1 score is the harmonic mean of precision and recall.

## Confusion Matrix
A confusion matrix counts true positives, true negatives, false positives, and false negatives. The relative cost of these errors depends on the application.

## ROC-AUC
ROC-AUC measures how well a classifier ranks positive examples above negative examples across thresholds. A score near 0.5 generally indicates ranking performance similar to random guessing; a score near 1 indicates strong ranking performance.

## Regression Metrics
Mean absolute error measures average absolute prediction error. Root mean squared error penalizes larger errors more strongly. R-squared compares model performance with a baseline that predicts the target mean, though it can be negative on test data.

## Reliable Evaluation
Use a suitable validation strategy, check class imbalance, compare against a simple baseline, and evaluate on held-out data. Report the metric that best reflects the real problem.
