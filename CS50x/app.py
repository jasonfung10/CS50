import requests
import json
from cs50 import SQL
from bs4 import BeautifulSoup
import re
from flask import Flask, redirect, render_template, flash, request

app = Flask(__name__)
app.config['SECRET_KEY'] = '_5#y2L"F4Q8z\n\xec]/'


#Creat database
#open("data.db", "w").close()
db = SQL("sqlite:///data.db")
#db.execute("CREATE TABLE Price_check (id INTEGER, product_name TEXT NOT NULL, price NUMERIC NOT NULL, lowest_price NUMERIC NOT NULL DEFAULT 0, size TEXT NOT NULL, url TEXT NOT NULL, PRIMARY KEY(id))")


@app.route("/", methods=['GET','POST'])
def index():
    if not db.execute("SELECT * FROM Price_check"):
        return render_template("index.html",name="You have no saved search")
    else :
        links = db.execute("SELECT * FROM Price_check ORDER BY 	product_name")
        return render_template("index.html", links = links)



@app.route("/add", methods=['GET','POST'])
def add():
    #parse webpage
    if request.method == "POST":
        headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        if not request.form.get("url"):
            return render_template("error.html", name="Please input URL")
        url = request.form.get("url")
        if not url.startswith('http'):
            return render_template("error.html", name="Please input URL starts with http")
        source = re.findall('(?<=www\.).*(?=\.c)',url)
        support_stores = ['endclothing','thehipstore','urbanindustry']
        if not any(store in source for store in support_stores):
            flash ("Only support End clothing, The Hip Store or Urban Industry")
            return render_template("error.html",name="Stores not supported")
        page = requests.get(url, headers = headers)
        soup = BeautifulSoup(page.content, "html.parser")
        if "urbanindustry" in source:
            try:
                urbanindustry (soup, url)
            except:
                flash ('Urban Industry link not valid')
                return render_template("error.html",name="Link not valid")
        elif "thehipstore"in source:
            try:
                hipstore (soup, url)
            except:
                flash ('The Hip Store link not valid')
                return render_template("error.html",name="Link not valid")
        elif "endclothing" in source:
            try:
                endclothing (soup, url)
            except:
                flash ('End Clothing link not valid')
                return render_template("error.html",name="Link not valid")
        flash ('Link added successfully')
        return render_template("add.html")

    else:
        return render_template("add.html")

@app.route("/error", methods=['GET','POST'])
def error():
    if request.method == "POST":
        return redirect ("/add")


@app.route("/remove", methods=['POST'])
def remove():
    if request.method == "POST":
        url = request.form.get("remove_url")
        db.execute("DELETE from Price_check WHERE url = ?", url)
        flash ("Link removed successfully")
        return redirect ("/")

@app.route("/refresh", methods=['POST'])
def refresh():
    if request.method == "POST":
        links = db.execute("SELECT url FROM Price_check")
        for link in links:
            url=link['url']
            headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            page = requests.get(url, headers = headers)
            soup = BeautifulSoup(page.content, "html.parser")
            source = re.findall('(?<=www\.).*(?=\.c)',url)
            if "urbanindustry" in source:
                urbanindustry (soup, url)
            elif "thehipstore"in source:
                hipstore (soup, url)
            elif "endclothing" in source:
                endclothing (soup, url)
        flash ("Link refreshed successfully")
        return redirect ("/")


@app.route("/test", methods=['GET','POST'])
def test():
    flash ("HIHI")
    return render_template("test.html")

#for END clothing webscrap
def endclothing (soup, url):
    try:
        print (soup.find('span', {'data-test': 'ProductDetails__Title'}).text)
    except:
        return render_template("error.html",name="Link not valid")
    else:
        name = soup.find('span', {'data-test': 'ProductDetails__Title'}).text
        price = int(soup.find(id="pdp__details__final-price").text[1:])
        #get the size via parsing json
        sizes = soup.find("script", id="__NEXT_DATA__").text.strip()
        data = json.loads(sizes)
        #check product is still in stock or not
        try:
            data = data['props']['initialProps']['pageProps']['product']['configurable_product_options'][0]['values']
            sizelist=""
            for size in data:
                sizelist =  "{}{}, ".format(sizelist, size["label"])
            sizelist=sizelist[0:-2]
        except:
            sizelist = 'Out of stock'
        add_into_db(url,price, sizelist, name )

def hipstore (soup, url):
        name = soup.find(class_="pdp-title").text.replace('\n', ' ').strip()
        if not soup.find('span', class_="now"):
            price = int(soup.find('span', class_="pri").text[1:-3])
        else:
            price = int(soup.find('span', class_="now").text[1:-3])
        sizelist = ", ".join(soup.find('div',id="productSizeStock").text.replace('UK','').split())
        if sizelist.startswith('ONE'):
            sizelist = 'One size'
        add_into_db(url,price, sizelist, name )


def urbanindustry (soup, url):
        converstion = 0.84
        name = soup.find(class_="pdp-title").text.strip()
        price = round(int(soup.find(class_="pdp-price").text[2:-4]) *converstion)
        #sizelist = ", ".join(soup.find('ul',class_="pdp-variants").text.split())
        allsize = soup.find('ul',class_="pdp-variants")
        children = allsize.findChildren("li" , recursive=False)
        sizelist=''
        for child in children:
            if child.find('label',class_='disabled-option'):
                continue
            sizelist = "{}{}, ".format(sizelist, child.text)
            sizelist = ', '.join(sizelist[:-2].split()).strip()
        if sizelist.startswith('ONE'):
            sizelist = 'One size'
        add_into_db(url,price, sizelist, name )



#Add URL into databas and check whether the data base has the item already or not
def add_into_db(url, price, sizelist, name):
    if db.execute ("SELECT * FROM Price_check WHERE url = ?", url):
        lowest_price= db.execute ("SELECT lowest_price FROM Price_check WHERE url = ?", url)[0]['lowest_price']
        if lowest_price < price:
            db.execute("UPDATE Price_check SET price = ?, size = ? WHERE url = ?",price, sizelist, url)
        else:
            db.execute("UPDATE Price_check SET price = ?, lowest_price = ?, size = ? WHERE url = ?",price, price, sizelist, url)
    else:
        db.execute("INSERT INTO Price_check (product_name, price, lowest_price, size, url) VALUES (?,?,?,?,?)", name, price, price, sizelist, url)



