from geopy.geocoders import Nominatim

# Defina um user_agent personalizado
geolocator = Nominatim(user_agent="my_geocoder_app")

# Tente novamente
location = geolocator.geocode("Palmas, Brasil")

if location:
    print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
else:
    print("Localização não encontrada.")