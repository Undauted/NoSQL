mongoimport --db ORG --collection Wells --file OGA_Wells_WGS84.geojson --jsonArray

mongo ORG --eval "db.Wells.ensureIndex({'geometry' : '2dsphere'})"

mongoexport -d ORG -c Wells -q "{geometry:{$near:{$geometry:{ type : 'Point', coordinates : [ 2.393602625903736,53.44106130104489 ] },$maxDistance:5000}}}" -o C:\Mongo\Mongo_export\mapa1.geojson --jsonArray --pretty

mongoexport -d ORG -c Wells -q "{geometry: { $geoWithin: { $center:  [ [ 2.1531123182033376, 52.94598756402161  ], 0.1 ] } }}" -o C:\Mongo\Mongo_export\mapa2.geojson --jsonArray --pretty

mongoexport -d ORG -c Wells -q "{geometry: {$geoWithin: { $geometry: { type : 'Polygon', coordinates: [[[ -4.399991, 60.325 ], [ -4.3080609999999995, 60.319297 ],   [ -4.30, 60.28 ], [ -4.48, 60.26], [ -4.399991, 60.325 ]    ]]}} }}" -o C:\Mongo\Mongo_export\mapa3.geojson --jsonArray --pretty

python Scripts\export.py mapa1.geojson

python Scripts\export.py mapa2.geojson

python Scripts\export_polygon.py mapa3.geojson