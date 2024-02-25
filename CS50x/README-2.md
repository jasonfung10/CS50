# Online Men's Fashion Shops' Price Monitor
#### Video Demo: <https://youtu.be/GghkTQy5pGU>

#### Description:
**-Background**

Online shopping has basically become the norm as it is easier to browse differently within clicks instead of visiting the shops physically that take time and money. Besides, online shops always have a larger selection of items compared to its physical one due to the limitation of shop floor space. Percentage of online retails sales has been increasing and currently accounts 30% of total sales (both online and brick and mortar sales).

Before consumers make their purchase decision, it is very likely they will compare the price of the same item from different retailers. There are different online shop price checker exist in the current market already. The most famous one is surely CamelCamelCamel which tracks the Amazon price. As Amazon provides API for developers to track their item's price, it will be handy to record it.

Apart from CamelCamelCamel, there are generic online price checkers as well, but they mainly focus on electronics and have limited support of different online stores (mainly large chains), and the prices shown on these websites are not in real time as they will update the price at regular time intervals. To bridge the gap, I have developed a simple web application that tracks a few online UK mens online stores to allow consumers to make a wise decision before purchase.


**-Language/ Framework used**
- `Python`
- `HTML`
- `CSS`
- `Javascript/ jQuery`
- `SQLite`
- `Flask`
- `Jinja`
- `Bootstrap`

#### Building the website

**-Flask**

The framework is used for web applications. It is based on the `Jinja ` template for `Python` - the programming language. As per `Flask` documentation, web pages are stored in `templates` folder and `javascript` and `CSS` are stored in `static` folder. The `app.py` is the main application of `Flask`

**-HTML**

A base webpage (`base.hmlt`)is created with Navbar and footer as the fundamental element of every web page in the application. `Bootstrap` is used for styling the webpage as it provides an easy to use framework. External `CSS` and `Javascript` are linked in the files saved in static.

```
<!doctype html>
<html lang="en">
 <head>
   <meta charset="utf-8">
   <meta name="viewport" content="width=device-width, initial-scale=1">
   <title>{% block title %}{% endblock %}</title>
   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
   <link href="/static/styles.css" rel="stylesheet">
   <script src="/static/javascript.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
 </head>
 <body>
   <nav class="navbar navbar-expand-lg bg-body-tertiary">
       <div class="container-fluid">
         <a class="navbar-brand" href="/">
           <img src="https://prisync.com/wp-content/uploads/2018/03/price-monitoring.jpg" alt="Logo" width="30" height="24" class="d-inline-block align-text-top">
           Price Checker
         </a>
         <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
           <span class="navbar-toggler-icon"></span>
         </button>
         <div class="collapse navbar-collapse" id="navbarNav">
           <ul class="navbar-nav">
             <li class="nav-item">
               <a class="nav-link active" aria-current="page" href="/">Home</a>
             </li>
             <li class="nav-item">
               <a class="nav-link" href="/add">Add Link</a>
             </li>
           </ul>
         </div>
       </div>
     </nav>
   <main>
     <script src="/static/javascript.js"></script>
        {% block body %}{% endblock %}
   </main>
   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>
 </body>
 <footer class="text-muted">
   Copyright&#169 by Jason Fung for CS50 final project
 </footer>
</html>
```
Flash messages are displayed when an action is made. The flash messages will be closed automatically by using jQuery.

```
$(document).ready(function() {
   // show the alert
   setTimeout(function() {
       $(".alert").alert('close');
   }, 1500);
});
```

Total 3 `HTML` pages are created.
- index.html
- add.htmml
- error.html

index.html
- the main page which shows saved items name, price, URL.
- remove button to get rid of the item if no longer needed.
- refresh all the data of the saved item to make sure price and size are up to date.
![index screencap](screencap/indexpage.png)

add.htmml
- page allow users to add the URL of the item that want to check the price.
![add screencap](screencap/addlinkpage.png)

error.html
- page to show error message if the input link to check the price is not valid
![add screencap](screencap/errorpage.png)

#### -Web Scraping

Web Scraping plays a major role in this simple web application. In order to scrap the relevant data from the respective online store, a different library is imported into `Python`.

`Beautiful Soup` is a common library used for web scraping.
```
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
page = requests.get(url, headers = headers)
soup = BeautifulSoup(page.content, "html.parser")
```
`header` gives the website server details of request and tries to mimic the request from a true user instead of scraping data.
`request.get` used to get a response from the online store server. Then the data received is parsed via `BeautifulSoup`. It will automatically understand the `HTML` tag used in the website and so can find the relevant data.
```
name = soup.find(class_="pdp-title").text
```
This will return data that with a `HTML` tag of class 'pdp-title'

Unfortunately, `BeautifulSoup` can only handle static website. For dynamic website which data usually presented by `Javascript`, there are different ways to handle. For example, another library called `selenium` can be used. But in this project, it is not used as only 1 of the webstore requires scraping dynamic data, it will not be efficient to import 1 library for a relatively small part of the application. Also, data can still be retrieved with `BeautifulSoup`, but requires additional work. Usually the dynamic website will send the data to the user computer in `json` format, so if we load the data with `json` library, useful data can be retrieved.

After getting the item's name, size, price. Data will be stored in a database. In this project, `SQLite` is used as there will only be a small amount of data in this application. Other databases will be more useful if the data volume is huge.

The web application is first linked to the database. A table is created in the database in advance.
```
db = SQL("sqlite:///data.db")
```
A function is created to add all data into the database.
```
def add_into_db(url, price, sizelist, name):
   if db.execute ("SELECT * FROM Price_check WHERE url = ?", url):
       lowest_price= db.execute ("SELECT lowest_price FROM Price_check WHERE url = ?", url)[0]['lowest_price']
       if lowest_price < price:
           db.execute("UPDATE Price_check SET price = ?, size = ? WHERE url = ?",price, sizelist, url)
       else:
           db.execute("UPDATE Price_check SET price = ?, lowest_price = ?, size = ? WHERE url = ?",price, price, sizelist, url)
   else:
       db.execute("INSERT INTO Price_check (product_name, price, lowest_price, size, url) VALUES (?,?,?,?,?)", name, price, price, sizelist, url)

```
In the index.html, all data stored in the database is then parsed and shown in a table.
```
def index():
   if not db.execute("SELECT * FROM Price_check"):
       return render_template("error.html",name="You have no saved search")
   else :
       links = db.execute("SELECT * FROM Price_check ORDER BY  product_name")
       return render_template("index.html", links = links)
```


In order to delete any data, the following code will be executed.
```
db.execute("DELETE from Price_check WHERE url = ?", url)
```

#### -How to use

It is a simple web application so it is very straightforward to use it to track online store item prices.
It only supports 3 UK's menswear online stores at the moment which are EndClothing, TheHipStore, UrbanIndustry.

-The homepage will show all saved items if there are any. Item name, current price, lowest price, size and URL is shown.

-To add items for price monitoring, click the `Add link` in the top nav bar. Then input the URL of your items. It will then be shown in the home page if the link is valid.

-Saved items can be removed by clicking the `remove` button in the homepage.

-A `refresh` button is used to refresh all save items data manually. It is recommended to click the `refresh` button every time you visit the website as the data is not updated automatically.




