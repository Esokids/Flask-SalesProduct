from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)
con = mysql.connector.connect(
    user='root', password='', host='localhost', database='imex_sales')

# ============================== Index ==============================


@app.route('/')
def index():
    cursor = con.cursor(buffered=True)
    query = "SELECT sale.id, sale.sellout, customer.name, customer.tel, customer.email FROM `sale` inner join customer on customer.id=sale.cust_id"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    return render_template('index.html', data=rows)


# ============================== Sales ==============================

@app.route('/add')
def addSell():
    return render_template('addSale.html')


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        sellout = request.form['sellout']
        cust_id = request.form['custid']

        cursor = con.cursor()

        query = "INSERT INTO `sale` (sellout, cust_id) VALUES (%s, %s)"
        cursor.execute(query, (sellout, cust_id))

        con.commit()
        cursor.close()
        return redirect('/')


@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        id = request.form['id']
        sellout = request.form['sellout']

        cursor = con.cursor()

        query = "UPDATE `sale` SET sellout=%s WHERE id=%s"
        cursor.execute(query, (sellout, id))

        con.commit()
        cursor.close()
        return redirect('/')

# ============================== Customer ==============================


@app.route('/customers')
def customers():
    cursor = con.cursor(buffered=True)
    query = "SELECT * FROM `customer`"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    return render_template('customer.html', data=rows)


@app.route('/addCustomer')
def addCustomer():
    return render_template('addCustomer.html')


@app.route('/addCustomer', methods=['POST'])
def addNewCustomer():
    if request.method == "POST":
        name = request.form['name']
        tel = request.form['tel']
        email = request.form['email']

        cursor = con.cursor()

        query = "INSERT INTO `customer` (name, tel, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, tel, email))

        con.commit()
        cursor.close()
        return redirect('/customers')

# ============================== Customer ==============================


@app.route('/products')
def products():
    cursor = con.cursor(buffered=True)
    query = "SELECT * FROM `product`"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    return render_template('product.html', data=rows)


@app.route('/addProduct')
def addProduct():

    return render_template('addProduct.html')


@app.route('/addProduct', methods=['POST'])
def addNewProduct():
    if request.method == "POST":
        id = request.form['id']
        name = request.form['name']
        cursor = con.cursor()

        query = "INSERT INTO `product` (id, name) VALUES (%s, %s)"
        cursor.execute(query, (id, name))

        con.commit()
        cursor.close()
        return redirect('/products')


if __name__ == "__main__":
    app.run(debug=True)
