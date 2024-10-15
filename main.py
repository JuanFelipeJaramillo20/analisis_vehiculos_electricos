# Importamos las librerías necesarias
import requests
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Definimos la URL de la API del conjunto de datos
api_url = "https://www.datos.gov.co/resource/7qfh-tkr3.json"

# Definimos el límite de registros por solicitud y el total estimado de registros
limit = 1000  # La API permite un máximo de 1000 registros por solicitud
total_records = 56545  # Número total estimado de registros en el dataset
all_data = []  # Lista para almacenar todos los registros
valid_offsets = []
invalid_offsets = []
# Hacemos solicitudes paginadas en bloques de 'limit' hasta obtener todos los registros
for offset in range(0, total_records, limit):
    params = {
        "$limit": limit,
        "$offset": offset,
    }

    # Realizamos la solicitud GET a la API
    response = requests.get(api_url, params=params)

    # Verificamos el estado de la respuesta
    if response.status_code == 200:
        valid_offsets.append(offset)
        data = response.json()  # Obtenemos los datos en formato JSON
        all_data.extend(data)  # Añadimos los registros obtenidos a la lista total
        print(f"Obtenidos {len(data)} registros desde el offset {offset}.")
    else:
        invalid_offsets.append(offset)
        print(f"Error al acceder a la API en el offset {offset}: {response.status_code}")
        break  # Detenemos el bucle en caso de error

    # Esperamos un pequeño intervalo de tiempo para evitar sobrecargar el servidor
    time.sleep(1)

# Convertimos la lista de registros en un DataFrame de pandas
df = pd.DataFrame(all_data)

# Mostramos el número total de registros obtenidos
print(f"Total de registros obtenidos: {len(df)}")
df.head()

# Guardar el análisis de valores nulos en un archivo de texto
with open("analisis_nulos.txt", "w") as f:
    f.write("Valores Nulos por Columna:\n")
    f.write(df.isnull().sum().to_string())

# Guardar los tipos de datos en un archivo de texto
with open("tipos_de_datos.txt", "w") as f:
    f.write("Tipos de Datos por Columna:\n")
    f.write(df.dtypes.to_string())

# Contamos el número de vehículos por departamento
departamento_counts = df['departamento'].value_counts()

# Guardar el gráfico de la distribución por departamento como imagen
plt.figure(figsize=(10, 6))
sns.barplot(x=departamento_counts.index, y=departamento_counts.values, hue=departamento_counts.index, palette="viridis", legend=False)
plt.title('Distribución de Vehículos por Departamento')
plt.xticks(rotation=90)
plt.ylabel('Cantidad de Vehículos')
plt.savefig("distribucion_vehiculos_departamento.png")
plt.close()

# Contamos el número de vehículos por tipo de combustible
combustible_counts = df['combustible'].value_counts()

# Guardar el gráfico de la distribución por tipo de combustible como imagen
plt.figure(figsize=(8, 5))
sns.barplot(x=combustible_counts.index, y=combustible_counts.values, hue=combustible_counts.index, palette="magma", legend=False)
plt.title('Distribución de Vehículos por Tipo de Combustible')
plt.ylabel('Cantidad de Vehículos')
plt.savefig("distribucion_vehiculos_combustible.png")
plt.close()

# Graficamos la distribución por clasificación de vehículos
clasificacion_counts = df['clasificacion'].value_counts()

# Guardar el gráfico de la distribución por clasificación como imagen
plt.figure(figsize=(8, 5))
sns.barplot(x=clasificacion_counts.index, y=clasificacion_counts.values, hue=clasificacion_counts.index, palette="coolwarm", legend=False)
plt.title('Distribución de Vehículos por Clasificación')
plt.ylabel('Cantidad de Vehículos')
plt.savefig("distribucion_vehiculos_clasificacion.png")
plt.close()

# Graficamos la distribución por tipo de servicio
servicio_counts = df['servicio'].value_counts()

# Guardar el gráfico de la distribución por tipo de servicio como imagen
plt.figure(figsize=(8, 5))
sns.barplot(x=servicio_counts.index, y=servicio_counts.values, hue=servicio_counts.index, palette="rocket", legend=False)
plt.title('Distribución de Vehículos por Tipo de Servicio')
plt.ylabel('Cantidad de Vehículos')
plt.savefig("distribucion_vehiculos_servicio.png")
plt.close()

# Guardar el gráfico de outliers en cilindraje
plt.figure(figsize=(10, 6))
sns.boxplot(x='cilindraje', data=df)
plt.title('Distribución de Cilindraje - Detección de Outliers')
plt.savefig("outliers_cilindraje.png")
plt.close()

# Guardar el gráfico de outliers en potencia
plt.figure(figsize=(10, 6))
sns.boxplot(x='potencia', data=df)
plt.title('Distribución de Potencia - Detección de Outliers')
plt.savefig("outliers_potencia.png")
plt.close()

# Filtramos los registros de vehículos eléctricos
df_electricos = df[df['combustible'].str.contains('Eléctrico', case=False, na=False)]

# Contamos el número de vehículos eléctricos registrados por año
electricos_por_anio = df_electricos.groupby('anio_registro').size()

# Guardamos los resultados en un archivo CSV
electricos_por_anio.to_csv('tendencia_vehiculos_electricos.csv')

# Contamos el número de vehículos por tipo de combustible
combustible_comparativa = df['combustible'].value_counts()

# Guardamos los resultados en un archivo CSV
combustible_comparativa.to_csv('comparativa_combustible.csv')

# Graficamos la comparativa entre vehículos eléctricos y de combustión interna
plt.figure(figsize=(10,6))
combustible_comparativa.plot(kind='bar', color=['green', 'red', 'blue', 'orange'])
plt.title('Comparativa de Vehículos Eléctricos vs. Combustión Interna')
plt.xlabel('Tipo de Combustible')
plt.ylabel('Cantidad de Vehículos Registrados')
plt.grid(True)
plt.savefig("comparativa_vehiculos_combustible.png")
plt.close()


# Convertir la columna 'anio_registro' a tipo numérico
df['anio_registro'] = pd.to_numeric(df['anio_registro'], errors='coerce')

# Convertir las columnas numéricas relevantes (cilindraje, potencia, etc.)
df['cilindraje'] = pd.to_numeric(df['cilindraje'], errors='coerce')
df['potencia'] = pd.to_numeric(df['potencia'], errors='coerce')
df['capacidad_carga'] = pd.to_numeric(df['capacidad_carga'], errors='coerce')
df['peso'] = pd.to_numeric(df['peso'], errors='coerce')

# Filtramos los registros de vehículos eléctricos
df_electricos = df[df['combustible'].str.contains('Eléctrico', case=False, na=False)]

# Contamos el número de vehículos por tipo de combustible
combustible_comparativa = df['combustible'].value_counts()

# Guardamos los resultados en un archivo CSV
combustible_comparativa.to_csv('comparativa_combustible.csv')

# Graficamos la comparativa entre vehículos eléctricos y de combustión interna
if not combustible_comparativa.empty:
    plt.figure(figsize=(10, 10))
    combustible_comparativa.plot(kind='bar', color=['green', 'red', 'blue', 'orange'])
    plt.title('Comparativa de Vehículos Eléctricos vs. Combustión Interna')
    plt.xlabel('Tipo de Combustible')
    plt.ylabel('Cantidad de Vehículos Registrados')
    plt.grid(True)
    plt.savefig("comparativa_vehiculos_combustible.png")
    plt.close()
else:
    print("No hay datos suficientes para la comparativa de combustibles.")
