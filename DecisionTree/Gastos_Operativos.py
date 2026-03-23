import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

df = pd.read_csv('Data/Gastos.csv')

df['Gastos Operativos'] = df[['Costo de Venta (Refacciones)', 'Gastos de Operación', 'Gastos de Mantenimiento']].sum(axis=1)    
x = df[['Costo de Venta (Refacciones)', 'Gastos de Operación', 'Gastos de Mantenimiento']]
y = df['Gastos Operativos']

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