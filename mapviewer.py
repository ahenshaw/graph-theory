import shapefile
import geopandas as gpd
import pandas as pd
import osr
import matplotlib.pyplot as plt
from shapely.geometry import shape 

base = 'c:/temp/tl_2017_13_prisecroads'
r = shapefile.Reader(base)
prj = base+'.prj'

attributes, geometry = [], []
field_names = [field[0] for field in r.fields[1:]]  
for row in r.shapeRecords():  
    geometry.append(shape(row.shape.__geo_interface__))  
    attributes.append(dict(zip(field_names, row.record)))  
    
proj4 = osr.SpatialReference(open(prj).read()).ExportToProj4()
gdf = gpd.GeoDataFrame(data = attributes, geometry = geometry, crs=proj4)
print(gdf['MTFCC'].unique())
print(gdf['RTTYP'].unique())
#print(gdf[gdf.RTTYP=='I'])

interstates = gdf[gdf.RTTYP=='I'].to_crs(epsg = 3424)
ax = interstates.plot(color = 'blue', figsize=(10,10))
ax.set(xticks=[], yticks=[])
plt.show()
#plt.savefig("NJ_Counties.png", bbox_inches='tight')


