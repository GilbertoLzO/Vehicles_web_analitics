import pandas as pd
import plotly.express as px 
import streamlit as st

# Leer los datos
vehicles_data = pd.read_csv("vehicles_us.csv")
vehicles_data[["manufacturer","modelo"]] = vehicles_data["model"].str.split(n=1, expand= True)

st.title("Autos anunciados a venta en USA")
st.write("Se nos ha proporcionado una tabla con la informacion de autos que fueron anunciados a venta en USA ")
st.write("En esta sencilla app web te mostraremos graficos creados a partir de estos datos.")

st.header("Menu de seleccion")
st.write("Puedes dar click en cualquier casilla y se mostrara el contenido de la misma.")

# Crea una check box para mostrar el contenido de la tabla
show_table = st.checkbox("Visualizar tabla de datos")

if show_table:
    st.write("Tabla de datos")
    vehicle_table = st.dataframe(vehicles_data, use_container_width=True)
    st.write("Se muestra la informacion de los anuncios de venta de los vehiculos")


# Crea una check box que construya un histograma
hist_button = st.checkbox("Construye un histograma")

if hist_button:
    manufacturer_hist = px.histogram(vehicles_data, 
            x = "manufacturer", 
            title= "Numero de autos anunciados de cada fabricante",
            labels = {"count":"Numero","manufacturer":"Fabricante"},
            category_orders={"manufacturer": vehicles_data["manufacturer"].value_counts().index})
    st.plotly_chart(manufacturer_hist, use_container_width=True)
    st.write("En este grafico podemos observar la cantidad de vehiculos anunciados de cada fabricante. Es notable una mayor prescencia de autos cuyos fabricantes son Estado Unidenses como Ford y Chevrolet.")
    
# Crea una check box que construya una grafica de barras
bar_button = st.checkbox("Construye una grafica de barras")

if bar_button:
    group_type_veh = vehicles_data.groupby(["manufacturer","type"])["type"].count().reset_index(name = "count")

    vehicle_type = px.bar(group_type_veh, 
             x = "manufacturer",
             y = "count",
             color = "type", 
             title = "Tipos de vehiculos por fabricante", 
             labels = {"count":"Numero","manufacturer":"Fabricante"},
             category_orders={"manufacturer": vehicles_data["manufacturer"].value_counts().index}
            )
    st.plotly_chart(vehicle_type, use_container_width=True)
    st.write("Con este grafico de barras dinamico podemos filtrar por el tipo de vehiculo, de este modo tambien sabemos cuantos vehiculos de cada tipo fueron anunciados.")

# Crea una check box que construya un grafico de dispercion
scatter_button = st.checkbox("Construye un grafico de dispercion para el precio")

if scatter_button:
    st.write("Selecciona los fabricantes que deseas comparar")
    manufacturer1 = st.selectbox("Selecciona al fabricante 1", vehicles_data["manufacturer"].unique())
    manufacturer2 = st.selectbox("Selecciona al fabricante 2", vehicles_data["manufacturer"].unique())
    
    filter_df = vehicles_data[(vehicles_data["manufacturer"] == manufacturer1)|(vehicles_data["manufacturer"] == manufacturer2)]
    group_per_price = filter_df.groupby(["manufacturer","price"])["price"].count().reset_index(name = "count")
    
    price_dispersion = px.histogram(group_per_price,
            x = "price",
            y = "count",
            color = "manufacturer",
            title = f"Dispersion entre los precios de {manufacturer1} y {manufacturer2}",
            labels = {"manufacturer":"Fabricante" , "price":"Precio en dolares"}
            )
    st.plotly_chart(price_dispersion, use_container_width=True)
    st.write("Con este grafico de dispercion podemos comparar la distribucion del precio de los vehiculos anunciados de dos fabricantes.")


st.write("Con estos graficos puedes comparar, filtrar y encontrar relaciones entre los distintos fabricantes de autos.")        
st.write("Creador Gilberto Loza.")