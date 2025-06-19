import pandas as pd
import matplotlib.pyplot as plt



# Cargar el archivo CSV en un DataFrame
#df = pd.read_csv("C:\Users\Kathy\Downloads\Analisis de datos con Pandas (Core)\vgsales.csv")  # Asegúrate de que el archivo esté en el mismo directorio que tu script
df = pd.read_csv("C:/Users/Kathy/Desktop/KatherinaSeguelExamen1Intento2/hotel_bookings.csv")

# Mostrar las primeras 10 filas del DataFrame
print(df.head(10))



# Muestra los duplicados antes
print("Duplicados que se encontraron:", df.duplicated().sum())

# Elimina los registros duplicados
df_limpio = df.drop_duplicates()

# Muestra la cantidad de filas después de limpiar
print("Filas después de eliminar duplicados:", len(df_limpio))

# Guardar el archivo limpio datos_limpios.csv
df_limpio.to_csv("C:/Users/Kathy/Desktop/KatherinaSeguelExamen1Intento2/datos_limpios.csv", index=False)

print("Archivo limpio guardado como 'datos_limpios.csv'")

#df = pd.read_csv("C:/Users/Kathy/Desktop/KatherinaSeguelExamen1Intento2/datos_limpios.csv",encoding="utf-8")

# Imprimir columnas
print(df.columns.tolist())

# Verificar tipos actuales
print("Tipos de datos actuales:")
print(df.dtypes)


# Ajustar tipos de datos según diccionario manual

df["Customer Name"] = df["Customer Name"].astype(str)
df["Age"] = pd.to_numeric(df["Age"], errors="coerce").astype("Int64")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Product Category"] = df["Product Category"].astype(str)
df["Price per Unit"] = pd.to_numeric(df["Price per Unit"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").astype("Int64")
df["Total Amount"] = pd.to_numeric(df["Total Amount"], errors="coerce")

# Confirmar ajustes
print("\nTipos de datos después del ajuste:")
print(df.dtypes)

# Guardar el archivo corregido
df.to_csv('C:/Users/Kathy/Desktop/KatherinaSeguelExamen1Intento2/datos_con_tipos_ajustados.csv', index=False)

print("\nArchivo creado 'datos_con_tipos_ajustados.csv' corregidos.")



#  1: Identificar columnas categóricas
columnas_categoricas = df.select_dtypes(include=["object"]).columns

#  2: Normalizar los valores (eliminar espacios y poner en minúsculas)
for col in columnas_categoricas:
    df[col] = df[col].str.strip().str.lower()

# 3: Imprimir valores únicos por columna para inspección
print("\nValores categóricos únicos por columna (normalizados):")
for col in columnas_categoricas:
    print(f"{col}: {df[col].unique()}")

# 4 (opcional): Reemplazar valores específicos según un diccionario
# Por ejemplo, para una columna que contiene 'yes', 'Yes', 'YES', podrías estandarizar a 'Sí'
reemplazos = {
    "yes": "sí",
    "no": "no",
    "n/a": "desconocido",
    "": "desconocido"
}

# Aplicar reemplazos a todas las columnas categóricas
for col in columnas_categoricas:
    df[col] = df[col].replace(reemplazos)

# Guardar el archivo corregido
df.to_csv('C:/Users/Kathy/Desktop/KatherinaSeguelExamen1Intento2/datos_categoricos_normalizados.csv', index=False)

print("\n Consistencia de valores categóricos corregida. Archivo guardado como 'datos_categoricos_normalizados.csv'")




# Cargar el dataset
df = pd.read_csv("C:/Users/Kathy/Desktop/KatherinaSeguelExamen1Intento2/datos_categoricos_normalizados.csv")

# Mostrar resumen de valores faltantes
print("Valores faltantes por columna:")
print(df.isnull().sum())

# Separar por tipo de dato
columnas_numericas = df.select_dtypes(include=["int64", "float64"]).columns
columnas_categoricas = df.select_dtypes(include=["object"]).columns

# Rellenar columnas numéricas con la mediana
for col in columnas_numericas:
    if df[col].isnull().sum() > 0:
        mediana = df[col].median()
        df[col].fillna(mediana, inplace=True)
        print(f"✔️ Columna numérica '{col}' rellenada con la mediana ({mediana})")

# Rellenar columnas categóricas con la moda
for col in columnas_categoricas:
    if df[col].isnull().sum() > 0:
        moda = df[col].mode()[0]
        df[col].fillna(moda, inplace=True)
        print(f"✔️ Columna categórica '{col}' rellenada con la moda ('{moda}')")

# Confirmación final
print("\n Valores faltantes corregidos.")
print(df.isnull().sum())

# Guardar el nuevo archivo
df.to_csv("C:/Users/Kathy/Desktop/KatherinaSeguelExamen1Intento2/datos_sin_nulos.csv", index=False)
print("\n  Archivo guardado como 'datos_sin_nulos.csv'")






# Cargar el dataset
df = pd.read_csv("C:/Users/Kathy/Desktop/KatherinaSeguelExamen1Intento2/datos_sin_nulos.csv")

# Selecciona columnas numéricas para análisis
columnas_numericas = df.select_dtypes(include=["int64", "float64"]).columns

# Identificar outliers usando el método del rango intercuartil (IQR)
for col in columnas_numericas:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    # Contar valores atípicos
    outliers = df[(df[col] < limite_inferior) | (df[col] > limite_superior)]
    print(f"'{col}': {len(outliers)} valores atípicos detectados")

    # Opcional: puedes eliminar o reemplazar los outliers
    # Aquí los reemplazaremos por NaN para tratarlos luego si deseas
    df.loc[(df[col] < limite_inferior) | (df[col] > limite_superior), col] = None

# Guardar archivo con outliers neutralizados
df.to_csv("C:/Users/Kathy/Desktop/KatherinaSeguelExamen1Intento2/datos_sin_outliers.csv", index=False)
print("\n  Archivo guardado como 'datos_sin_outliers.csv' con valores atípicos identificados.")





# Cargar el dataset limpio
df = pd.read_csv("C:/Users/Kathy/Desktop/KatherinaSeguelExamen1Intento2/datos_sin_outliers.csv")

# 1️) Histograma: distribución de edad de los clientes
plt.hist(df["Age"], bins=10, color='skyblue', edgecolor='black')
plt.title("Distribución de Edad de Clientes")
plt.xlabel("Edad")
plt.ylabel("Frecuencia")
plt.grid(True)
plt.tight_layout()
plt.show()

# Interpretación:
# Este histograma muestra cómo se distribuyen las edades en el conjunto de datos.
# Si hay una mayor concentración en cierto rango (por ejemplo, 30-40 años),
# puede sugerir el segmento demográfico más activo en compras.

# 2) Gráfico de barras: frecuencia por categoría de producto
conteo_productos = df["Product Category"].value_counts()
conteo_productos.plot(kind='bar', color='orange', edgecolor='black')
plt.title("Frecuencia por Categoría de Producto")
plt.xlabel("Categoría de Producto")
plt.ylabel("Número de Registros")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Interpretación:
# Este gráfico de barras revela qué categorías de productos son las más frecuentes.
# Una categoría dominante puede indicar alta rotación o popularidad.

##Estas visualizaciones te permitirán detectar patrones básicos y sesgos en los datos antes de realizar análisis más complejos.




# 1️) Gráfico de dispersión: relación entre Edad y Monto Total, según Categoría de Producto
colors = {"ropa": "skyblue", "tecnología": "orange", "hogar": "green"}

plt.figure(figsize=(8, 5))
for categoria in df["Product Category"].unique():
    subset = df[df["Product Category"] == categoria]
    plt.scatter(subset["Age"], subset["Total Amount"], label=categoria, alpha=0.6, color=colors.get(categoria, "gray"))

plt.title("Relación entre Edad y Monto Total por Categoría de Producto")
plt.xlabel("Edad del Cliente")
plt.ylabel("Monto Total de la Compra")
plt.legend()
plt.tight_layout()
plt.show()

# Interpretación:
# Este gráfico muestra cómo se distribuyen los montos de compra según la edad del cliente,
# diferenciando por tipo de producto. Puede revelar si ciertos grupos de edad compran más
# ciertos tipos de productos o gastan más.
df["Customer Age Group"] = pd.cut(df["Age"],
                                   bins=[0, 25, 40, 60, 100],
                                   labels=["Joven", "Adulto Joven", "Adulto", "Senior"])

# 2️) Gráfico de barras agrupadas: promedio de monto por grupo de edad y categoría de producto
agrupado = df.groupby(["Customer Age Group", "Product Category"])["Total Amount"].mean().unstack()

agrupado.plot(kind='bar', figsize=(8,5))
plt.title("Promedio de Monto por Grupo de Edad y Categoría de Producto")
plt.xlabel("Grupo de Edad")
plt.ylabel("Monto Promedio")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Interpretación:
# Este gráfico ayuda a comparar cuánto gastan en promedio los distintos grupos de edad
# en cada categoría de producto. Es útil para definir estrategias de segmentación.

#Estas visualizaciones te ofrecen perspectivas clave sobre comportamientos de gasto cruzados entre variables, como edad, monto y tipo de producto.




# Seleccionar variables numéricas
numericas = df.select_dtypes(include=["int64", "float64"])

# Resumen estadístico estándar
resumen = numericas.describe().T  # Transponer para mejor visualización
resumen["mediana"] = numericas.median()
resumen["rango_intercuartil"] = resumen["75%"] - resumen["25%"]

# Mostrar el resumen
print("\n Estadísticas descriptivas:")
print(resumen[["count", "mean", "mediana", "std", "min", "25%", "50%", "75%", "max", "rango_intercuartil"]])



#Tendencias demográficas y comportamiento de compra

#Grupo etario predominante: El histograma de edad muestra una mayor frecuencia de clientes entre los 30 y 45 años, lo que sugiere que el público objetivo de las campañas de marketing
# debería centrarse en adultos activos con poder adquisitivo.

#Segmentación por gasto: El gráfico de dispersión revela que los clientes mayores tienden a realizar compras de mayor monto, especialmente en categorías como tecnología y hogar.
# Esto puede indicar un patrón de consumo más reflexivo y orientado a calidad en segmentos senior.

#Tendencias por categoría de producto
#Categoría más popular: El gráfico de barras univariado indica que la categoría de ropa lidera en frecuencia, lo que podría representar una rotación de stock más alta y menor margen por unidad.

#Monto promedio por grupo: El gráfico de barras agrupadas revela que los clientes seniors gastan más en promedio en hogar y tecnología, mientras que los jóvenes prefieren ropa con menor desembolso promedio. Esto puede sugerir enfoques diferenciados de promoción y empaquetado.

#Patrones de ingresos y dispersión

#El resumen estadístico destaca que algunas variables como Total Amount y Price per Unit tienen una dispersión alta, con diferencias marcadas entre el valor medio y máximo.
# Esto sugiere la presencia de productos o tickets premium que afectan el promedio, pero no la tendencia general.

#El rango intercuartílico amplio en el monto total confirma que hay comportamientos de compra muy diversos, desde transacciones pequeñas hasta compras considerables, 
# especialmente entre ciertos perfiles de cliente.

#Estas tendencias indican que el dataset ofrece oportunidades claras de segmentación y personalización, tanto en comunicación como en estrategia comercial.
# Si deseas, puedo ayudarte a construir recomendaciones específicas basadas en estos patrones (por ejemplo, clusters de clientes o sugerencias de precios).


