import dash
from dash import dcc, html, callback, Input, Output
import pandas as pd
import plotly.express as px

# Cargar los datos
df = pd.read_csv('carpetasFGJ_2023.csv')  # Asegúrate de que el nombre del archivo sea correcto

# Filtrar para asegurar que todas las filas tengan coordenadas
df = df.dropna(subset=['latitud', 'longitud'])

# Crear la figura del mapa de calor
fig = px.density_mapbox(df, lat='latitud', lon='longitud',
                        radius=10,
                        center={"lat": 19.36, "lon": -99.133209},  # Centro en la Ciudad de México
                        zoom=10,
                        mapbox_style="mapbox://styles/mapbox/light-v10")  # Puedes cambiar el estilo del mapa aquí

# Lee la clave API desde el archivo
with open('api_key.txt', 'r') as file:
    key = file.read().strip()
fig.update_layout(mapbox_accesstoken=key)

# Iniciar la aplicación Dash
app = dash.Dash(__name__)

# Definir las opciones para el menú desplegable
categorias_delito = df['delito'].unique()
opciones_delito = [{'label': categoria, 'value': categoria} for categoria in categorias_delito]

# Definir el layout de la aplicación
app.layout = html.Div([
    html.H1("Mapa de Calor de Criminalidad en la Ciudad de México", className='h1'),
    
    # Menú desplegable para seleccionar la categoría del delito
    dcc.Dropdown(
        id='dropdown-delito',
        options=opciones_delito,
        value=categorias_delito[0],  # Valor predeterminado
        multi=False,
        style={'width': '50%'}
    ),
    
    dcc.Graph(id='mapa-delito', className='graph')
], className='body')

# Callback para actualizar el mapa cuando se selecciona una categoría de delito
@app.callback(
    Output('mapa-delito', 'figure'),
    [Input('dropdown-delito', 'value')]
)
def actualizar_mapa(categoria_delito):
    # Filtrar el DataFrame para mostrar solo la categoría de delito seleccionada
    df_filtrado = df[df['delito'] == categoria_delito]

    # Crear la figura del mapa de calor actualizada
    fig_actualizada = px.density_mapbox(df_filtrado, lat='latitud', lon='longitud',
                                        radius=10,
                                        center={"lat": 19.36, "lon": -99.133209},  # Centro en la Ciudad de México
                                        zoom=10,
                                        mapbox_style="mapbox://styles/mapbox/light-v10")

    # Actualizar la clave API del mapa
    fig_actualizada.update_layout(mapbox_accesstoken=key)

    return fig_actualizada

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
