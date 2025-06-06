import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np

#Loading data
file_path = "JPMC Tasks/Customer_Loan_Data.csv"
df = pd.read_csv(file_path)
df = df.dropna() #remove rows with missing values

# Define features and target
features = [
    'credit_lines_outstanding',
    'loan_amt_outstanding',
    'total_debt_outstanding',
    'income',
    'years_employed',
    'fico_score'
]

X = df[features]
y = df['default']

# Split into training/testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

def expected_loss(customer_data, loan_amount, recovery_rate=0.10):
    """
    customer_data: dict of borrower features (same keys as in `features`)
    loan_amount: the dollar amount of the loan
    recovery_rate: assumed percentage recovered on default
    """
    input_df = pd.DataFrame([customer_data])
    prob_default = model.predict_proba(input_df)[0,1]
    lgd = 1-recovery_rate
    loss = prob_default *lgd +loan_amount
    return loss

sample_customer = {
    'credit_lines_outstanding': 5,
    'loan_amt_outstanding': 12000,
    'total_debt_outstanding': 20000,
    'income': 45000,
    'years_employed': 3,
    'fico_score': 680
}

loan_amount = 10000
print(f"Expected Loss: ${expected_loss(sample_customer, loan_amount):.2f}")

