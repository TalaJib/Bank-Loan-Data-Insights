import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
from sklearn.preprocessing import LabelEncoder


df = pd.read_csv('loan_data.csv')
#print(df.head())

#analyse des val maquantes
print(df.isnull().sum())


print(median := df['ApplicantIncome'].median())


df['ApplicantIncome_Was_Missing'] = df['ApplicantIncome'].isnull().astype(int) #on repere les null
df['ApplicantIncome'] = df['ApplicantIncome'].fillna(df['ApplicantIncome'].median()) #on remplie


df['CoapplicantIncome_Was_Missing'] = df['CoapplicantIncome'].isnull().astype(int) #on repere les null
df['CoapplicantIncome'] = df['CoapplicantIncome'].fillna(0) #generalement s'il n'y a pas de coapplicant c'est 0, eviter de mettre la mediane 



df['LoanAmount_Was_Missing'] = df['LoanAmount'].isnull().astype(int) #on repere les null
df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].median()) #on remplie

# On remplace par la durée la plus fréquente (le MODE) (souvent 360.0)
df['LoanAmount_Term_Was_Missing'] = df['Loan_Amount_Term'].isnull().astype(int)
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mode()[0])


# Au lieu du mode, on crée une valeur distincte pour l'absence d'info
# On utilise 2.0 pour dire "Information non disponible"
df['Credit_History_Was_Missing'] = df['Credit_History'].isnull().astype(int)
df['Credit_History'] = df['Credit_History'].fillna(-1.0)


df['Dependents_Was_Missing'] = df['Dependents'].isnull().astype(int)
df['Dependents'] = df['Dependents'].fillna(-1.0)




#null into Unknown for non numerical columns
cat_cols = ['Gender', 'Married', 'Self_Employed']
for col in cat_cols:
    df[col] = df[col].fillna('Unknown')
#print(df.head())
#print("Gender", df['Gender'].value_counts())


#renvenu total
df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']

# remplissage rapide (ex: la médiane pour le montant du prêt)
#moyenne peut varier selon le revenu des personnes pauvres/riches
#df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].median())
#df['Credit_History'] = df['Credit_History'].fillna(1) # On suppose 1 par défaut

#print(df.head(60))




# if 'Loan_Status' in df.columns:
#     plt.figure(figsize=(10, 6))
#     sns.boxplot(x='Loan_Status', y='Total_Income', data=df)
#     plt.title('Comparaison du Revenu Total par Statut du Prêt')
#     plt.ylim(0, 20000) 
#     plt.show()



# transformer les textes en nb
le = LabelEncoder()

df_encoded = df.copy()

# colonnes à transformer 
mapping_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area', 'Dependents']

for col in mapping_cols:
    df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))

# si Loan_Status existe on le transforme en 1/0
if 'Loan_Status' in df_encoded.columns:
    df_encoded['Loan_Status'] = le.fit_transform(df_encoded['Loan_Status'])

if 'Loan_ID' in df_encoded.columns:
    df_encoded = df_encoded.drop(columns=['Loan_ID'])

#heatmap
plt.figure(figsize=(15, 10))
# On calcule la corrélation entre toutes les colonnes
correlation_matrix = df_encoded.corr()

# affichage avec Seaborn
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Matrice de Corrélation : Quels facteurs influencent le dossier ?")
plt.show()



# export pour Power BI etExcel
df.to_csv('credit_data_visualisation.csv', index=False)

# export pour le Machine Learning (Tout en numérique)
# df_encoded créeé pour la Heatmap
df_encoded.to_csv('credit_data_machine_learning.csv', index=False)

print("\n--- ÉTAPE TERMINÉE ---")
print("1. 'credit_data_visualisation.csv' créé pour Power BI.")
print("2. 'credit_data_machine_learning.csv' créé pour l'IA.")