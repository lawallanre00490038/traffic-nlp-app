# def get_location(df, traffic_category, traffic_class_column="traffic_class", place_column="place"):
#     from geopy.geocoders import GoogleV3
#     from geopy.exc import GeocoderTimedOut

#     # Create a geocoder object with the API key
#     api_key = "AIzaSyDxTCeIB_-YadQbWqDbCSBKtfttEWbF_8w"
    
#     geolocator = GoogleV3(api_key=api_key, domain="maps.google.com.ng")
#     geolocator.timeout = 10

#     data = df[df[traffic_class_column] == traffic_category].dropna()

#     def get_location_coordinates(place):
#         try:
#             location = geolocator.geocode(place)
#             if location is not None:
#                 return f"{location.latitude}, {location.longitude}"
#             else:
#                 return None
#         except GeocoderTimedOut:
#             return None

#     data["location"] = data[place_column].apply(get_location_coordinates)
#     data.dropna(subset=["location"], inplace=True)
#     data[["lat", "lng"]] = data["location"].str.split(",", expand=True).astype(float)
#     data.drop(columns=["location"], inplace=True)

#     # Define the bounds of Lagos
#     min_lon, max_lon = 2.6327, 4.3517
#     min_lat, max_lat = 6.2648, 6.7027

#     # Drop rows that are not within the bounds of Lagos
#     data = data[data['lat'].notna() & data['lng'].notna()]
#     data = data[data.apply(lambda row: row['lng'] >= min_lon and row['lng'] <= max_lon and row['lat'] >= min_lat and row['lat'] <= max_lat, axis=1)]
#     return data


import logging

def get_location(df, traffic_category, traffic_class_column="traffic_class", place_column="place"):
    from geopy.geocoders import GoogleV3
    from geopy.exc import GeocoderTimedOut
    import pandas as pd
    
    # Create a geocoder object with the API key
    api_key = "AIzaSyDxTCeIB_-YadQbWqDbCSBKtfttEWbF_8w"
    
    geolocator = GoogleV3(api_key=api_key, domain="maps.google.com.ng")
    geolocator.timeout = 10

    data = df[df[traffic_class_column] == traffic_category].dropna()

    def get_location_coordinates(place):
        try:
            location = geolocator.geocode(place)
            if location is not None:
                return f"{location.latitude}, {location.longitude}"
            else:
                return None
        except GeocoderTimedOut:
            return None

    data["location"] = data[place_column].apply(get_location_coordinates)
    data.dropna(subset=["location"], inplace=True)

    try:
        split_result = data["location"].str.split(",", expand=True)
        assert len(split_result.columns) == 2
        data[["lat", "lng"]] = split_result.astype(float)
        data.drop(columns=["location", "Unnamed: 0",'content', 'sentiment'], inplace=True)

        # Define the bounds of Lagos
        min_lon, max_lon = 2.6327, 4.3517
        min_lat, max_lat = 6.2648, 6.7027

        # Drop rows that are not within the bounds of Lagos
        data = data[data['lat'].notna() & data['lng'].notna()]
        data = data[data.apply(lambda row: row['lng'] >= min_lon and row['lng'] <= max_lon and row['lat'] >= min_lat and row['lat'] <= max_lat, axis=1)]
    except Exception as e:
        logging.error(f"Error processing data for traffic category {traffic_category}: {e}")
        data = pd.DataFrame()

    return data.reset_index(drop=True)
