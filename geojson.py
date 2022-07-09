import pandas as pd
import geopandas as gpd
import numpy as np
import folium
import os

# print(os.listdir('geojson'))

# dfgeo = gpd.read_file('./geojson/ukraine-region.json')
# df_information_csv = pd.read_csv("./csv-patern/patern-region-ukraine.csv")

dfgeo = gpd.read_file('./geojson/all_country.json')
df_information_csv = pd.read_csv("./csv-patern/patern-all-country.csv")

def region_Ukraine(df_geo,df_csv):

    dfgeo = df_geo.rename(columns = {"shapeName":"region"})
    final_df = dfgeo.merge(df_csv, on= "region")

    final_df.loc[final_df['number'] == '',"number"] = np.nan
    final_df['number'] = final_df['number'].astype(float)

    return [final_df,'region']


def all_country(df_geo,df_csv):
    final_df = dfgeo.merge(df_csv, on= "name")

    final_df.loc[final_df['number'] == '',"number"] = np.nan
    final_df['number'] = final_df['number'].astype(float)
    return [final_df,'name']


def hromada_ukraine():
    return 1


def view_map(df,legend_name):
    m = folium.Map(location=[49.17,32.89], zoom_start=5)
    # (BuGn, BuPu, GnBu, OrRd, PuBu, PuBuGn, PuRd, RdPu, YlGn, YlGnBu, YlOrBr, and YlOrRd)?

    folium.Choropleth(
    geo_data=df[0],
    data=df[0],
    columns=[str(df[1]),"number"],
    key_on=f"feature.properties.{str(df[1])}",
    fill_color='OrRd',
    fill_opacity=1,
    line_opacity=0.2,
    # ------------------ name legend
    legend_name=str(legend_name),
    Highlight= True,
    line_color = "Black",
    name = "name",
    show=True,
    overlay=True,
    nan_fill_color = "White"
    ).add_to(m)

    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}


    NIL = folium.features.GeoJson(
        data = df[0],
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=[str(df[1]),"number"],
            aliases=[str(df[1]),'Count'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
        )
    )
    m.add_child(NIL)
    m.keep_in_front(NIL)


    folium.TileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png',attr="sdf",name="dark mode").add_to(m)
    folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
                    attr="sdf",name="Esri").add_to(m)

    folium.LayerControl().add_to(m)

    return m.save(f'geojson_{df[1]}.html')


if __name__ == '__main__':
    legend_name = 'українські біженці станом на 16.06.22'
    # view_map(region_Ukraine(dfgeo,df_information_csv))
    view_map(all_country(dfgeo,df_information_csv),legend_name=legend_name)