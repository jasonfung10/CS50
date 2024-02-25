# Food Chooser with Google Map
#### Video Demo: <https://youtu.be/NSZc9wbmXgE>

#### Description:
**-Background**

Deciding what to eat is not always a easy choice no matter whether you are new to the area or you are a local already. In order to solve this problem, a very simple python application is created to guide you to the right food establishment.

The application will prompt useer to input the type of food establishment (restaurant, cafe, bar, club, takeaway, bakery, liquor store, supermrket) (based on Google Map available types) and location. Then will return 3 names of the selected food establishment which has rating >4.5 and more than 100 ratings.

**-Library Used**
- `googlemaps`
- `pandas`
- `random`
- `system`
- `time`

`googlemaps`
: It is a python library used communicate with Google Map API. Strictly speaking, it is not essential to use it as typing the parameter in a URL can also retrive the same result from Google Map. But obviously use this library will make things easier.

`pandas`: library used to store the data into a dataframe which is easier to clean/sort/filter.

`random`: Used to randomly pick 3 restaurant from a list of restaurants.

`system`: exit the programme when there is invalid input

`time`: it is used for the Google Map API. As everytime Google Map will only return 20 results of each request but will provide a "next page token" to return another 20 results (maxium return is 60 only in normal users). In order to get the get the next page token and feed to Google Map again, a small idle time is needed to get 20 x 3 results in a sequence.


**Get food establishment type**
```
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
```
Make sure the input fit standard made by Google Map. Otherwise, will exit the application with error message.

**Get the latitude and longitude of the location**
```
def get_geocode(address):
    try:
        geocode_result = gmaps.geocode(address)
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return (lat, lng)
    except:
        sys.exit("Invalid Address")
```
Will exit the application with error message if the address is unknown.

**Get the food establishments data by using Google Map API**
Set the API key first
```
gmaps = googlemaps.Client(key = 'YOUR_API_HERE')
```
use the library function `.places`. There are different functions in the `googlemaps` which can be useful for example `places_nearby`. A json format data will then be returned from Google Map. To make the data readable, the data is parsed by this fucntion which return a dictionary consists the name of food establishment, rating and number of ratings.
```
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
```
**Create dataframe**

The dictinary is used to create a dataframe by `pandas` which is a very common library used in data cleaning. The data is then filterd ( with rating >4.5 and more than 100 ratings) and then sorted. (it is not essential to sort the data as 3 of them will be selected randomly.)
```
def data_frame(rest_list):
    df = pd.DataFrame(rest_list)
    df_filtered = df[(df["rating"]>=4.5) & (df["user_rating"]>100)]
    df_sorted = df_filtered.sort_values("rating", ascending=False)
    df_sorted = df_sorted.reset_index(drop=True)
    print (df)
    print (len(rest_list["name"]))
    #print (df)
    print(df_sorted)
    return df_sorted
```

** Generate 3 random number based on the length of data**
```
def pick_3(data):
    return random.sample(range(data.shape[0]), 3)
```

**After generating 3 random numbers, they are then used to get the values of the repective food establishment name and rating information**
```
def ran_3_name(first, second, third, data):
    print ("3 daily choices are:")
    print (data.values[first])
    print (data.values[second])
    print (data.values[third])
```

That's it! A simply python application that help you to deicde where to eat from your location.