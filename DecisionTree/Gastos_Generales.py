import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

df = pd.read_csv('Data/Gastos.csv')

df['Gastos Generales'] = df[['Gastos Administrativos', 'Gastos Financieros', 'Gastos no fiscales', 'ISR  Ejercicio', 'ISR Facilidades Administrativas', 'Costo de lo Vendido']].sum(axis=1)

x = df[['Gastos Administrativos', 'Gastos Financieros', 'Gastos no fiscales', 'ISR  Ejercicio', 'ISR Facilidades Administrativas', 'Costo de lo Vendido']]
y = df['Gastos Generales']

model = DecisionTreeRegressor()
model.fit(x, y)
importances = model.feature_importances_
feature_importance = pd.DataFrame({'Feature': x.columns, 'Importance': importances})
feature_importance = feature_importance.sort_values(by='Importance', ascending=False)   

print(feature_importance)
plt.figure(figsize=(10, 6))
plt.bar(feature_importance['Feature'], feature_importance['Importance'], color='skyblue')   
plt.xlabel('Features')
plt.ylabel('Importance')
plt.title('Feature Importance in Decision Tree Regressor')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
