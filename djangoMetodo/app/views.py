from django.shortcuts import render
from django.conf import settings
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.preprocessing import StandardScaler
import datetime
import os

EXCEL_DIR = os.path.join(settings.BASE_DIR, 'app', 'static')


def SFFS(possibleVar, y, data):
    selected_vars = {'variables': [], 'r2': None} # Diccionario para almacenar las variables seleccionadas y su MAE (usar None cuando no existe)
    maeg = [] # Lista para almacenar el MAE en cada iteración
    n = len(possibleVar)
    
    while n > 0:# while para recorrer todas las variables posibles
        lr = LinearRegression() 
        largo = len(selected_vars['variables'])
        for i in possibleVar:
            test = selected_vars['variables'] + [i]
            lr.fit(data[test], y)
            y_hat = lr.predict(data[test])
            r2 = r2_score(y, y_hat)
            
            # Comprobar de forma explícita si aún no hay MAE almacenado o si el nuevo MAE es menor
            if (selected_vars['r2'] is None) or (r2 > selected_vars['r2']):
                selected_vars['variables'] = test
                variableSelected = i
                selected_vars['r2'] = r2  
                maeg.append(selected_vars['r2'])
                print(f"Variable seleccionada: {i}")
        n -= 1 # Decrementar la iteracion
        if largo < len(selected_vars['variables']):
            possibleVar.remove(variableSelected) # Remover la variable ya seleccionada
    
    return selected_vars, maeg 



csv_path = f"{settings.BASE_DIR}/app/static/excel.csv"
tarea = pd.read_csv(csv_path)
tarea = tarea.set_index("Customer ID")
#------------------------------------------------------------------------------------------

#Value_counts de los valores categoricos
categorias = []
for i in ['Gender', 'Item Purchased', 'Category','Location', 'Size', 'Color', 'Season','Subscription Status', 'Shipping Type', 'Discount Applied','Promo Code Used', 'Payment Method','Frequency of Purchases']:
    categorias.append(tarea[i].value_counts())
#------------------------------------------------------------------------------------------

#Viendo los nulos por columna
nulos = tarea.isnull().sum()
#------------------------------------------------------------------------------------------

# funcion que traforma los yes en 0 y los no en 1
#------------------------------------------------------------------------------------------

tarea['Gender']=np.where(tarea['Gender'] == 'Male', 'Hombre',tarea['Gender'])
tarea['Gender']=np.where(tarea['Gender'] == 'Female', 'Mujer',tarea['Gender'])



# Traducción manual de valores categóricos
# Item Purchased
tarea['Item Purchased'] = tarea['Item Purchased'].replace({
    'Shirt': 'Camisa',
    'Pants': 'Pantalón',
    'Shoes': 'Zapatos',
    'Dress': 'Vestido',
    'Hat': 'Sombrero',
    'Jacket': 'Chaqueta',
    'Skirt': 'Falda',
    'Shorts': 'Shorts',
    'Sweater': 'Suéter',
    'Socks': 'Calcetines',
    'Sandals': 'Sandalias',
    'Boots': 'Botas'
})



# Category
tarea['Category'] = tarea['Category'].replace({
    'Clothing': 'Ropa',
    'Footwear': 'Calzado',
    'Accessories': 'Accesorios'
})

# Color
tarea['Color'] = tarea['Color'].replace({
    'Red': 'Rojo',
    'Blue': 'Azul',
    'Green': 'Verde',
    'Black': 'Negro',
    'White': 'Blanco',
    'Yellow': 'Amarillo',
    'Pink': 'Rosa',
    'Purple': 'Morado',
    'Brown': 'Marrón',
    'Orange': 'Naranja'
})
# Season
tarea['Season'] = tarea['Season'].replace({
    'Spring': 'Primavera',
    'Summer': 'Verano',
    'Fall': 'Otoño',
    'Winter': 'Invierno'
})
# Payment Method
tarea['Payment Method'] = tarea['Payment Method'].replace({
    'Credit Card': 'Tarjeta de Crédito',
    'Debit Card': 'Tarjeta de Débito',
    'Cash': 'Efectivo',
    'Bank Transfer': 'Transferencia Bancaria'
})
# Frequency of Purchases
tarea['Frequency of Purchases'] = tarea['Frequency of Purchases'].replace({
    'Weekly': 'Semanal',
    'Monthly': 'Mensual',
    'Bi-Weekly': 'Cada dos semanas',
    'Fortnightly': 'Quincenal',
    'Every 3 Months': 'Cada 3 Meses',
    'Quarterly': 'Trimestral',
    'Annually': 'Anual'
})


# Análisis Univariado
def distribucion_clientes_genero(request):
    df1 = pd.read_excel(os.path.join(EXCEL_DIR, 'ED_TASAJ.xlsx')).set_index('Descripción series').drop('Reg',axis=1)
    df2 = pd.read_excel(os.path.join(EXCEL_DIR, 'EST_GEN_DEU_01.xlsx')).set_index('Descripción series').drop('Reg',axis=1)
    df3 = pd.read_excel(os.path.join(EXCEL_DIR, 'ED_VAR_REM_M_2023_EMP.xlsx')).set_index('Descripción series').drop('Reg',axis=1)
    df4 = pd.read_excel(os.path.join(EXCEL_DIR, 'EXE_EOF_1.xlsx')).set_index('Descripción series').drop('Reg',axis=1)


    df = pd.concat([df1,df2,df3,df4],join='inner').drop('\xa0\xa0\xa0Hombres',axis=0).drop('\xa0\xa0\xa0Mujeres',axis=0)
    indices = df.index.tolist()
    valores = ["TasaDesempleo", "DeudasTotal","VariacionDeSueldo","GastoDeEmpleo","Inflacion"]

    df.columns = pd.to_datetime(df.columns)

    columnasNuevas ={}
    for i in range(len(indices)):
        columnasNuevas[indices[i]]=valores[i]
    df = df.rename(index=columnasNuevas)

    df1 = df.T

    y = df1['VariacionDeSueldo']
    posibleVar = df1.columns.tolist()
    posibleVar.remove('VariacionDeSueldo')
    print(posibleVar)# lista con nuevos valores para el índice
    selected_vars, maeg = SFFS( posibleVar, y, df1)
    valores = df1[selected_vars['variables']]
    lr = LinearRegression()
    lr.fit(valores, y)
    y_hat = lr.predict(valores)
    print(selected_vars)
    r2 = r2_score(y, y_hat)
    mae = mean_absolute_error(y, y_hat)
    rmse = np.sqrt(mean_squared_error(y, y_hat))
    # Create your views here.
    x = y.values.tolist()
    y2 = y_hat.tolist()
    print(x,y2)
    return render(request, 'analisis/univariado/distribucion_genero.html', {'x': x, 'y': y2,'r2': r2, 'mae': mae, 'rmse': rmse, 'selected_vars': ', '.join(selected_vars['variables'])})

# Análisis Bivariado
def comparacion_compras_generos(request):
    # Get purchase amounts by gender
    df1 = pd.read_excel(os.path.join(EXCEL_DIR, 'ED_TASAJ.xlsx')).set_index('Descripción series').drop('Reg',axis=1)
    df2 = pd.read_excel(os.path.join(EXCEL_DIR, 'EST_GEN_DEU_01.xlsx')).set_index('Descripción series').drop('Reg',axis=1)
    df3 = pd.read_excel(os.path.join(EXCEL_DIR, 'ED_VAR_REM_M_2023_EMP.xlsx')).set_index('Descripción series').drop('Reg',axis=1)
    df4 = pd.read_excel(os.path.join(EXCEL_DIR, 'EXE_EOF_1.xlsx')).set_index('Descripción series').drop('Reg',axis=1)


    df = pd.concat([df1,df2,df3,df4],join='inner').drop('\xa0\xa0\xa0Hombres',axis=0).drop('\xa0\xa0\xa0Mujeres',axis=0)
    indices = df.index.tolist()
    valores = ["TasaDesempleo", "DeudasTotal","VariacionDeSueldo","GastoDeEmpleo","Inflacion"]

    df.columns = pd.to_datetime(df.columns)

    columnasNuevas ={}
    for i in range(len(indices)):
        columnasNuevas[indices[i]]=valores[i]
    df = df.rename(index=columnasNuevas)

    df1 = df.T




    experimentos = 1000
    mes = 12
    dias = 30

    df2 = pd.DataFrame(df1["Inflacion"])
    df2["mes"] = df1.index.month
    df2["cambio_pct"] = df2["Inflacion"].pct_change() * 100  # Calcular cambio porcentual

    # Agrupar los cambios porcentuales por mes
    meses = df2.groupby("mes").agg({"cambio_pct": list})

    inflacionInicial = df1['Inflacion'].values.tolist()[-1]
    x = []
    y = []
    for i in range(experimentos):
        inflacion = [inflacionInicial]
        for k in range(1, mes+1):
            for l in range(dias):
                # Usar cambios porcentuales históricos
                cambio = np.random.choice([x for x in meses.loc[k, "cambio_pct"] if not np.isnan(x) and not np.isinf(x)])
                nuevoValor = inflacion[-1] * (1 + cambio/100/30)  # Aplicar cambio porcentual diario
                inflacion.append(float(nuevoValor))
        x.append(list(range(0, dias*12 +1)))
        y.append(inflacion)
    print(x)
    context = {
        'x': x,
        'y': y
    }
    return render(request, 'analisis/bivariado/comparacion_generos.html', context)

def relacion_categoria_monto(request):
    # Calculate total purchase amount by category
    category_totals = tarea.groupby('Category')['Purchase Amount (USD)'].sum().to_dict()
    
    # Get category names and values
    categories = list(category_totals.keys())
    values = list(category_totals.values())
    
    # Calculate percentages
    total = sum(values)
    percentages = [(v/total)*100 for v in values]
    context = {
        'categories': categories,
        'values': values,
        'percentages': percentages,
        'total': total
    }
    return render(request, 'analisis/bivariado/categoria_monto.html', context)

def cantidad_ventas_categoria(request):
    y=tarea['Category'].value_counts()
    x =  y.index.tolist()
    y = y.values.tolist()

    return render(request, 'analisis/bivariado/ventas_categoria.html', {'y': y, 'x': x})



# Diccionario para mapear nombres de estados a códigos (para Plotly)
STATE_CODE_MAP = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Análisis de Ubicación
def relacion_ubicacion_monto(request):
    # Agrupar por ubicación y calcular el total de ventas
    ventas_por_estado = tarea.groupby('Location')['Purchase Amount (USD)'].sum().reset_index()
    ventas_por_estado.columns = ['Estado', 'Total_Ventas']
    
    # Mapear nombres de estados a códigos
    ventas_por_estado['Codigo'] = ventas_por_estado['Estado'].map(STATE_CODE_MAP)
    
    # Ordenar por total de ventas descendente
    ventas_por_estado = ventas_por_estado.sort_values('Total_Ventas', ascending=False)
    
    # Preparar datos para el template
    estados = ventas_por_estado['Estado'].tolist()
    codigos = ventas_por_estado['Codigo'].tolist()
    totales = [int(x) for x in ventas_por_estado['Total_Ventas'].tolist()]
    
    # Top 10 estados
    top_10_estados = estados[:10]
    top_10_totales = totales[:10]
    
    context = {
        'estados': estados,
        'codigos': codigos,
        'totales': totales,
        'top_10_estados': top_10_estados,
        'top_10_totales': top_10_totales
    }
    
    return render(request, 'analisis/ubicacion/ubicacion_monto.html', context)

def presencia_geografica(request):
    # Calcular cantidad de ventas por estado
    ventas_por_estado = tarea.groupby('Location').size().reset_index(name='Cantidad_Ventas')
    ventas_por_estado.columns = ['Estado', 'Cantidad_Ventas']
    
    # Mapear nombres de estados a códigos
    ventas_por_estado['Codigo'] = ventas_por_estado['Estado'].map(STATE_CODE_MAP)
    
    # Crear copia ordenada para la tabla (bottom 10)
    ventas_ordenadas = ventas_por_estado.sort_values('Cantidad_Ventas', ascending=True)
    estados_baja_presencia = ventas_ordenadas.head(10)
    
    # Bottom 10 para la tabla - crear lista de diccionarios
    bottom_10_data = [
        {'estado': estado, 'cantidad': int(cantidad)}
        for estado, cantidad in zip(
            estados_baja_presencia['Estado'].tolist(),
            estados_baja_presencia['Cantidad_Ventas'].tolist()
        )
    ]
    
    # Preparar datos para el mapa (todos los estados)
    todos_estados = ventas_por_estado['Estado'].tolist()
    todos_codigos = ventas_por_estado['Codigo'].tolist()
    todas_cantidades = [int(x) for x in ventas_por_estado['Cantidad_Ventas'].tolist()]
    
    context = {
        'todos_estados': todos_estados,
        'todos_codigos': todos_codigos,
        'todas_cantidades': todas_cantidades,
        'bottom_10_data': bottom_10_data
    }
    
    return render(request, 'analisis/ubicacion/presencia_geografica.html', context)



# Análisis Multivariado
def compras_categoria_talla(request):

    category_size_counts = pd.crosstab(tarea['Category'], tarea['Size'])
    

    categories = category_size_counts.index.tolist()
    sizes = category_size_counts.columns.tolist()

    size_data = {}
    for size in sizes:
        size_data[size] = category_size_counts[size].tolist()
    
    context = {
        'categories': categories,
        'sizes': sizes,
        'size_data': size_data
    }
    return render(request, 'analisis/multivariado/categoria_talla.html', context)

# Problemas
def problemas(request):
    return render(request, 'problemas/base_problemas.html')

def problema1(request):

    x = tarea['Gender'].value_counts().index.tolist()
    y = tarea["Gender"].value_counts().tolist()
    

    male_purchases = tarea[tarea['Gender'] == 'Hombre']['Purchase Amount (USD)'].tolist()
    female_purchases = tarea[tarea['Gender'] == 'Mujer']['Purchase Amount (USD)'].tolist()
    
    context = {
        'gender_labels': x,
        'gender_counts': y,
        'male_purchases': male_purchases,
        'female_purchases': female_purchases
    }
    return render(request, 'problemas/problema1.html', context)

def problema2(request):

    category_size_counts = pd.crosstab(tarea['Category'], tarea['Size'])
    categories = category_size_counts.index.tolist()
    sizes = category_size_counts.columns.tolist()
    size_data = {}
    for size in sizes:
        size_data[size] = category_size_counts[size].tolist()

    y = tarea['Category'].value_counts()
    x_ventas = y.index.tolist()
    y_ventas = y.values.tolist()
    
    # Bivariado 2: Monto total por categoría
    category_totals_dict = tarea.groupby('Category')['Purchase Amount (USD)'].sum().to_dict()
    cat_names = list(category_totals_dict.keys())
    cat_values = list(category_totals_dict.values())
    total_monto = sum(cat_values)
    cat_percentages = [(v/total_monto)*100 for v in cat_values]
    
    context = {
        'categories': categories,
        'sizes': sizes,
        'size_data': size_data,
        'x_ventas': x_ventas,
        'y_ventas': y_ventas,
        'cat_names': cat_names,
        'cat_values': cat_values,
        'cat_percentages': cat_percentages,
        'total_monto': total_monto
    }
    return render(request, 'problemas/problema2.html', context)

def problema3(request):

    ventas_por_estado = tarea.groupby('Location')['Purchase Amount (USD)'].sum().reset_index()
    ventas_por_estado.columns = ['Estado', 'Total_Ventas']
    ventas_por_estado['Codigo'] = ventas_por_estado['Estado'].map(STATE_CODE_MAP)
    ventas_por_estado = ventas_por_estado.sort_values('Total_Ventas', ascending=False)
    

    cantidad_por_estado = tarea.groupby('Location').size().reset_index(name='Cantidad_Ventas')
    cantidad_por_estado.columns = ['Estado', 'Cantidad_Ventas']
    cantidad_por_estado['Codigo'] = cantidad_por_estado['Estado'].map(STATE_CODE_MAP)
    cantidad_ordenada = cantidad_por_estado.sort_values('Cantidad_Ventas', ascending=True)
    

    todos_estados = ventas_por_estado['Estado'].tolist()
    todos_codigos = ventas_por_estado['Codigo'].tolist()
    todos_montos = [int(x) for x in ventas_por_estado['Total_Ventas'].tolist()]
    
    todas_cantidades = []
    for estado in todos_estados:
        cantidad = cantidad_por_estado[cantidad_por_estado['Estado'] == estado]['Cantidad_Ventas'].values[0]
        todas_cantidades.append(int(cantidad))
    

    bottom_10 = cantidad_ordenada.head(10)
    bottom_10_data = []
    for i in range(len(bottom_10)):
        estado = bottom_10.iloc[i]['Estado']
        cantidad = int(bottom_10.iloc[i]['Cantidad_Ventas'])
        bottom_10_data.append({'estado': estado, 'cantidad': cantidad})
    
    context = {
        'estados': todos_estados,
        'codigos': todos_codigos,
        'montos': todos_montos,
        'cantidades': todas_cantidades,
        'bottom_10': bottom_10_data
    }
    return render(request, 'problemas/problema3.html', context)

# Alcance
def alcance(request):
    return render(request, 'alcance.html')

def home(request):
    return render(request, 'home.html')

