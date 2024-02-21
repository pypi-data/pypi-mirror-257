import geopandas as gpd
from svgwrite.container import Group
from svgwrite import Drawing
import tempfile
import webbrowser
from svgmapper.path import Path
from svgmapper.symbol import Symbol
from svgmapper.point import Point
from svgmapper.translate import Translator
import pandas as pd

class Layer:
    def __init__(
            self,
            name: str,
            path: str = '',
            gdf: gpd.geodataframe = None,
            symbol: Symbol = None,
            crs='epsg:4326'
    ):
        self.name = name
        self.path = path
        self.gdf = gpd.read_file(path).to_crs(crs) if path else gdf.to_crs(crs)
        self.buffer_polygons()
        self.symbol = symbol
        self.group = Group(class_=name, id=name)

    def total_bounds(self):
        """Returns total bounds of geodataframe"""
        return self.gdf.total_bounds

    def get_features(self):
        """Returns features of geodataframe using iterrows method"""
        return self.gdf.to_dict('records')

    def to_crs(self, epsg: str):
        """Re-projects coordinate system with provided epgs code"""
        if epsg:
            self.gdf = self.gdf.to_crs(epsg)
        return self

    def buffer(self, factor:int):
        self.gdf.buffer(factor)
        return self

    def clip(self, mask):
        if isinstance(mask, type(self.gdf) | type(self.gdf.geometry)):
            self.gdf.set_geometry(self.buffer_polygons().clip(mask=mask).geometry, inplace=True)
        return self

    def buffer_polygons(self):
        polygons = self.gdf[self.gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])]
        points = self.gdf[self.gdf.geometry.type.isin(['Point'])]
        if not polygons.empty:
            buffered_polygons = polygons.geometry.buffer(0)
            return gpd.GeoDataFrame(
                geometry=pd.concat([points.geometry, buffered_polygons]),
                crs=self.gdf.crs
            )
        else:
            return self.gdf


    def get_layer(self):
        return self._layer

    def get_dwg(self):
        dwg = Drawing()
        dwg.add(self._layer)
        return dwg.tostring()

    def view(self):
        tmp = tempfile.NamedTemporaryFile(delete=False)
        path = tmp.name+'.svg'
        f = open(path, 'w')
        f.write(self.get_dwg())
        f.close()
        webbrowser.open_new('file://' + path)

    def write(self, translator: Translator = None):
        for feature in self.get_features():
            name = 'feature' if 'name' not in feature else feature['name']
            group = Group(id=name.replace(' ', '-'))
            # print(feature)
            geometry = feature['geometry']
            if not geometry:
                print(f'{name} had no geometry')
                continue
            if geometry.geom_type == 'Polygon':
                path = Path(
                    geometry=geometry,
                    translator=translator
                )
                group.add(path.path)
            if geometry.geom_type == 'MultiPolygon':
                for geom in geometry.geoms:
                    path = Path(
                        geometry=geom,
                        translator=translator
                    )
                    group.add(path.path)
            if geometry.geom_type == 'Point':
                point = Point(
                    geometry=geometry,
                    symbol=self.symbol,
                    translator=translator
                ).get_point()
                group.add(point)
            self.group.add(group)

        self._layer = self.group
        return self.group



