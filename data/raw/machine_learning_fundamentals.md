# Machine Learning Fundamentals

## Supervised Learning
Supervised learning trains a model using examples with known target labels. Classification predicts categories, such as whether a customer will churn. Regression predicts numeric values, such as house prices.

## Unsupervised Learning
Unsupervised learning discovers patterns in data without a target label. Clustering groups similar observations, while dimensionality reduction represents data using fewer features.

## Overfitting and Underfitting
Overfitting occurs when a model learns training data too closely and performs poorly on unseen examples. Underfitting occurs when a model is too simple to capture important patterns. Compare training and validation performance to diagnose both problems.

## Data Leakage
Data leakage occurs when training uses information that would not legitimately be available at prediction time. Split data before fitting preprocessing steps, and fit transformations only on the training data.

## Train and Test Sets
The training set fits the model. The validation set supports model selection and hyperparameter tuning. The test set estimates final performance and should not be repeatedly used to make modeling decisions.
