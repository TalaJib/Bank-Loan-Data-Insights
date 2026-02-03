import pandas as pd

try:
    df = pd.read_csv('loan_data.csv')
    
    # checking for missing values in ApplicantIncome or CoapplicantIncome
    missing_income = df[df['ApplicantIncome'].isnull() | df['CoapplicantIncome'].isnull()]
    
    if not missing_income.empty:
        print("Loan_IDs with missing ApplicantIncome or CoapplicantIncome:")
        for loan_id in missing_income['Loan_ID']:
            print(loan_id)
    else:
        print("No records found with missing ApplicantIncome or CoapplicantIncome.")

except FileNotFoundError:
    print("Error: loan_data.csv not found.")
except Exception as e:
    print(f"An error occurred: {e}")

