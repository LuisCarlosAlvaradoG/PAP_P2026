import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

df = pd.read_csv('Data/Ingresos Alimentadoras limpio.csv')

df['Ingreso Total'] = df[['Efectivo', 'Tarifa Incompleta', 'Monto Tarjeta Gral', 'Monto Tarjeta Per', 'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error']].sum(axis=1)

x = df[['Efectivo', 'Tarifa Incompleta', 'Monto Tarjeta Gral', 'Monto Tarjeta Per', 'Monto Tarjeta Bpd', 'Recargas', 'Recargas Error']]
y = df['Ingreso Total']

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