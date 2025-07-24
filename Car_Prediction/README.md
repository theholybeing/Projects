# Car Price Prediction using Simple Linear Regression

## 📌 Overview
This project demonstrates Simple Linear Regression in Python to predict car prices based on engine size using a real-world dataset.

The objective of this project is to:
- Learn how to implement Simple Linear Regression
- Visualize the relationship between engine size and car price
- Evaluate the model using R² Score

---

## 📂 Dataset
The dataset contains multiple car attributes such as:
- Car name
- Engine size
- Horsepower
- Price

For this project, we use:
- Feature: `enginesize`
- Target: `price`

---

## 🔍 Project Steps
1. **Import Libraries**
   - pandas, matplotlib, scikit-learn
2. **Load Dataset**
   - Read CSV file, clean missing values
3. **Feature Selection**
   - X = enginesize
   - y = price
4. **Train-Test Split**
   - 80% training, 20% testing
5. **Train the Model**
   - LinearRegression() from scikit-learn
6. **Make Predictions**
   - Predict car prices for the test set
7. **Visualize Results**
   - Scatter plot of actual values vs predicted regression line
8. **Evaluate Performance**
   - Print slope, intercept, and R² Score

---

## 📈 Visualization
The regression line shows the predicted car prices based on engine size, while blue dots represent actual prices.

---

## 🛠️ Technologies Used
- Python
- pandas
- scikit-learn
- matplotlib

---

## ✅ Output
Example Output:
- Slope (Coefficient): `value`
- Intercept: `value`
- R² Score: `value`

---

## ▶️ How to Run
1. Install dependencies:
   ```bash
   pip install pandas scikit-learn matplotlib
