import overpass
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

def get_overpass_api():
    api = overpass.API(endpoint="https://maps.mail.ru/osm/tools/overpass/api/interpreter")
    return api

def prepare_filter(key, type="nwr", area="area"):
    result = "%s[%s](%s);" % (type, key, area)
    return result

def prepare_around(lat, lon, radius):
    result = "around:%s, %s, %s" % (radius, lat, lon)
    return result

def prepare_overpass_infrastructure(around, array):
    filter = ''
    type = 'nwr'
    for k in array:
        filter += prepare_filter(k,type,around)
                 
    result = "(%s);" % (filter)
    return result

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Timeweb Cloud + FastAPI = ❤️"

@app.get("/api/around/{lat}/{lon}/{radius}")
def get_entity_list(lat: float, lon: float, radius: float):
    around = prepare_around(lat, lon, radius)
    array = [
        "amenity=school",
        "amenity=college",
        "amenity=music_school",
        "amenity=university",
        "amenity=hospital",
        "amenity=clinic",
        "amenity=bus_station",
        "highway=bus_stop",
    ]
    request = prepare_overpass_infrastructure(around, array)
    api = get_overpass_api()
    result = api.get(request)
    return result
