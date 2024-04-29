import requests

# Define the base URL and API key (replace with your own)
base_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
api_key = "zLeRtMvpOXSFXDlAGp2vo5J11ny0egPNX0qSlepg"

# Define search parameters
params = {
    "api_key": api_key,
    "query":"pizza",
    # "pageSize": 200,  # Adjust page size as needed
    # "sort": "brandOwner",  # Sort by brand owner
    # "dataType": "[Branded Foods]"  # Search for branded foods only
}




# Open file for writing in append mode
with open("raw_data.json", "a") as f:
    query = 'Lays'  
    url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key=EOcBurjhuDFV9xf0NhZtNgMxQhzZ2YTu4NqeZ0b6&query={query}'
    response = requests.get(url).json()
    # response = requests.get(base_url, params=params)
    data = response


    # Write raw data to file
    f.write(str(data))  # Convert data to string before writing
    template = "[]"

    for item in data['foods']:
        pass

ingredient_template = "[]"
product_template = "[]"
company_template = "[]"



print("Data retrieval complete. Check raw_data.txt")