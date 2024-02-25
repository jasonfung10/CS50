import googlemaps
import sys, time
import pandas as pd
import random

gmaps = googlemaps.Client(key = 'AIzaSyA7PK9BPenAOwM0azd3-GVxYdMqkgdVkE4')
food_establishment_types = "bakery, bar, cafe, liquor_store, meal_takeaway, night_club, restaurant, supermarket"

def main():
    eatery = type_of_restaurant(input(f"Type of food establishment ({food_establishment_types}): ").lower().strip())
    lat_lng = get_geocode(input('Please enter current postcode/address: '))
    rest_list = get_restaurant(lat_lng, eatery)
    data = data_frame(rest_list)
    '''
    print (data)
    print (f"data shape {data.shape[0]}")
    '''
    pick = pick_3(data)
    ran_3_name (*pick,data)

def pick_3(data):
    return random.sample(range(data.shape[0]), 3)

def ran_3_name(first, second, third, data):
    print ("3 daily choices are:")
    print (data.values[first])
    print (data.values[second])
    print (data.values[third])

def data_frame(rest_list):
    df = pd.DataFrame(rest_list)
    df_filtered = df[(df["rating"]>=4.5) & (df["user_rating"]>100)]
    df_sorted = df_filtered.sort_values("rating", ascending=False)
    df_sorted = df_sorted.reset_index(drop=True)
    return df_sorted

def type_of_restaurant(types):
    if types == "liquor":
        return 'liquor_store'
    elif types == "club" or types == "clubbing":
        return "night_club"
    elif types == "takeaway":
        return "meal_takeaway"
    elif types not in ['bakery','bar','cafe','liquor_store','meal_takeaway','night_club','restaurant','supermarket']:
        sys.exit('Type of places invlaid')
    else:
        return types

def get_geocode(address):
    try:
        geocode_result = gmaps.geocode(address)
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return (lat, lng)
    except:
        sys.exit("Invalid Address")

def get_restaurant(lat_lng, eatery):
    result = gmaps.places(location = (lat_lng), radius = 1000, type = eatery)
    rest_name = [list["name"] for list in result["results"]]
    rest_rating = [list["rating"] for list in result["results"]]
    rest_user_rating = [list["user_ratings_total"] for list in result["results"]]
    next_token = result["next_page_token"]
    while True:
        if next_token:
            time.sleep(2)
            next_result = gmaps.places(location = (lat_lng), radius = 1000, type = eatery, page_token = next_token)
            for list in next_result["results"]:
                rest_name.append(list["name"])
                rest_rating.append(list["rating"])
                rest_user_rating.append(list["user_ratings_total"])
            try:
                next_token = next_result["next_page_token"]
            except:
                break
    data = {}
    data['name'],data['rating'],data['user_rating'] = rest_name, rest_rating, rest_user_rating
    return data

if __name__ == "__main__":
    main()

