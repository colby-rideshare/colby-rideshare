import googlemaps
from dotenv import load_dotenv
import os 
load_dotenv()

GOOGLE_API = os.environ.get('GOOGLE_API')
GAS_API = os.environ.get('GAS_API') 

gmaps = googlemaps.Client(key= GOOGLE_API)



