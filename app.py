# All code is based on the CS 340 starter code**********

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = '' #last 4 of onid
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


@app.route('/homepage')
def root():
    return render_template("Homepage.j2")

# Products ------------------------------------------

# Create and read functions for products table
@app.route('/products', methods=["POST", "GET"])
def products():
    # Separate out the request methods, in this case this is for a POST
    # insert a product into the product entity
    if request.method == "POST":
        # fire off if user presses the Add Product button
        if request.form.get("Add_Product"):
            prod_name = request.form["prod_name"]
            sale_price = request.form["sale_price"]

            query = "INSERT INTO Products (prod_name, sale_price) VALUES (%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (prod_name, sale_price))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/products")

    # Grab products data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all 
        query = "SELECT Products.prod_name, sale_price FROM Products"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("Products.j2", data=data)

# delete function for products table
@app.route("/delete_product/<prod_name>")
def delete_product(prod_name):
    query = "DELETE FROM Products WHERE prod_name = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (prod_name,))
    mysql.connection.commit()
    return redirect("/products")

# update functions for products table
@app.route("/edit_product/<prod_name>", methods=["POST", "GET"])
def edit_product(prod_name):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        try:
            query = "SELECT * FROM Products WHERE prod_name = '%s'" % (prod_name)
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()
            return render_template("edit_products.j2", data=data)
        except Exception as e:
                print("Error occurred:", e)
                return str(e)  # Or return a custom error page

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Products' button
        if request.form.get("Edit_Product"):
            try:
            # grab user form inputs
                original_name = request.form["original_name"]
                prod_name = request.form["prod_name"]
                sale_price = request.form["sale_price"]

                query = "UPDATE Products SET Products.prod_name = %s, Products.sale_price = %s WHERE Products.prod_name = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (prod_name, sale_price, original_name))
                mysql.connection.commit()

                return redirect("/products")
            except Exception as e:
                print("Error occurred:", e)
                return str(e)  # Or return a custom error page

# Products ------------------------------------------



# Sales -----------------------------------------

# Create and Read functions for Sales table
@app.route('/sales', methods=["POST", "GET"])
def sales():
    # Separate out the request methods, in this case this is for a POST
    # insert a sale
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Sale"):
            # grab user form inputs
            total_cost = request.form["total_cost"]
            employee_ID = request.form["employee_ID"]

            try:
                query = "INSERT INTO Sales (total_cost, employee_ID) VALUES (%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (total_cost, employee_ID))
                mysql.connection.commit()

                return redirect("/sales")
            except Exception as e:
                print("Error occurred:", e)
                return str(e)  # Or return a custom error page

    if request.method == "GET":
        # mySQL query to grab all the sales
        try:
            # query = "SELECT Sales.transaction_ID, total_cost, employee_ID FROM Sales"
            query = "SELECT Sales.transaction_ID, total_cost, Employees.employee_name as Employee FROM Sales LEFT JOIN Employees ON Sales.employee_ID = Employees.employee_ID"
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            # mySQL query to grab data for our dropdown
            query2 = "SELECT employee_ID, employee_name FROM Employees"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            employee_data = cur.fetchall()

            # render sales page passing our query data and employees data to the edit_sales template
            return render_template("Sales.j2", data=data, employees=employee_data)
        except Exception as e:
                print("Error occurred:", e)
                return str(e)  # Or return a custom error page

# delete function for sales table
@app.route("/delete_sale/<int:transaction_ID>")
def delete_sale(transaction_ID):
    try:
        # mySQL query to delete the sale with our passed id
        query = "DELETE FROM Sales WHERE transaction_ID = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (transaction_ID,))
        mysql.connection.commit()

        # redirect back to people page
        return redirect("/sales")
    except Exception as e:
        print("Error occurred:", e)
        return str(e)  # Or return a custom error page

# Update function for sales table
@app.route("/edit_sale/<int:transaction_ID>", methods=["POST", "GET"])
def edit_sale(transaction_ID):
    if request.method == "GET":
        # mySQL query to grab the info with our passed id
        query = "SELECT * FROM Sales WHERE transaction_ID = %s" % (transaction_ID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

         # mySQL query to grab data for our dropdown
        query2 = "SELECT employee_ID, employee_name FROM Employees"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        sale_data = cur.fetchall()

        return render_template("edit_sales.j2", data=data, sales=sale_data)


    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Employees' button
        if request.form.get("Edit_Sale"):
            # grab user form inputs
            transaction_ID = request.form["transaction_ID"]
            total_cost = request.form["total_cost"]
            employee_ID = request.form["employee_ID"]

            try:
                query = "UPDATE Sales SET Sales.total_cost = %s, Sales.employee_ID = %s WHERE Sales.transaction_ID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (total_cost, employee_ID, transaction_ID))
                mysql.connection.commit()
                return redirect("/sales")
            except Exception as e:
                print("Error occurred:", e)
                return str(e)  # Or return a custom error page

# Sales------------------------------------------

# Ingredients-------------------------------------

# Create and Read function for ingredients table
@app.route('/ingredients', methods=["POST", "GET"])
def ingredients():
    # Separate out the request methods, in this case this is for a POST
    # insert an ingredient into the ingredients entity
    if request.method == "POST":
        # fire off if user presses the Add Ingredient button
        if request.form.get("Add_Ingredient"):
            # grab user form inputs
            item_name = request.form["item_name"]
            item_quantity = request.form["item_quantity"]
            unit_price = request.form["unit_price"]

            query = "INSERT INTO Ingredients (item_name, item_quantity, unit_price) VALUES (%s,%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (item_name, item_quantity, unit_price))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/ingredients")

    # Grab ingredients data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab data in ingredients
        query = "SELECT Ingredients.ingredient_ID, item_name, item_quantity, unit_price FROM Ingredients"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("Ingredients.j2", data=data)

# Delete function for ingredients table
@app.route("/delete_ingredient/<int:ingredient_ID>")
def delete_ingredient(ingredient_ID):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Ingredients WHERE ingredient_ID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (ingredient_ID,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/ingredients")

# Update function for ingredients table
@app.route("/edit_ingredient/<int:ingredient_ID>", methods=["POST", "GET"])
def edit_ingredient(ingredient_ID):
    if request.method == "GET":
        # mySQL query to grab the info of the ingredient with our passed id
        query = "SELECT * FROM Ingredients WHERE ingredient_ID = %s" % (ingredient_ID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_ingredients.j2", data=data)


    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Ingredient' button
        if request.form.get("Edit_Ingredient"):
            # grab user form inputs
            ingredient_ID = request.form["ingredient_ID"]
            item_name = request.form["item_name"]
            item_quantity = request.form["item_quantity"]
            unit_price = request.form["unit_price"]

            query = "UPDATE Ingredients SET Ingredients.item_name = %s, Ingredients.item_quantity = %s, Ingredients.unit_price = %s WHERE Ingredients.ingredient_ID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (item_name, item_quantity, unit_price, ingredient_ID))
            mysql.connection.commit()

            return redirect("/ingredients")
# Ingredients-------------------------------------


# Employees----------------------------------------

# Create and Read functions for employees table
@app.route('/employees', methods=["POST", "GET"])
def employees():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the employees entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Employee"):
            # grab user form inputs
            employee_name = request.form["employee_name"]
            employee_hours = request.form["employee_hours"]
            job = request.form["job"]

            # query = "INSERT INTO Employees (employee_name, employee_hours) VALUES (%s,%s)"
            # cur = mysql.connection.cursor()
            # cur.execute(query, (employee_name, employee_hours))
            # mysql.connection.commit()

            # Account for null job
            if job == "":
                query = "INSERT INTO Employees (employee_name, employee_hours) VALUES (%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (employee_name, employee_hours))
                mysql.connection.commit()

            else:
                query = "INSERT INTO Employees (employee_name, employee_hours, job_ID) VALUES (%s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (employee_name, employee_hours, job))
                mysql.connection.commit()

            # redirect back to people page
            return redirect("/employees")

    # Grab employees data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the employees
        query = "SELECT Employees.employee_ID, employee_name, employee_hours, Jobs.job_title AS job FROM Employees LEFT JOIN Jobs ON Employees.job_ID = Jobs.job_ID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab data for our dropdown
        query2 = "SELECT job_ID, job_title FROM Jobs"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        job_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("Employees.j2", data=data, jobs=job_data)

# Delete function for employees table
@app.route("/delete_employee/<int:employee_id>")
def delete_employee(employee_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Employees WHERE employee_ID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (employee_id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/employees")

# update function for employees table
@app.route("/edit_employee/<int:employee_id>", methods=["POST", "GET"])
def edit_employee(employee_id):
    if request.method == "GET":
        # mySQL query to grab the info with our passed id
        query = "SELECT * FROM Employees WHERE employee_id = %s" % (employee_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

         # mySQL query to grab data for our dropdown
        query2 = "SELECT job_ID, job_title FROM Jobs"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        job_data = cur.fetchall()

        return render_template("edit_employees.j2", data=data, jobs=job_data)


    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Employees' button
        if request.form.get("Edit_Employee"):
            # grab user form inputs
            employee_ID = request.form["employee_ID"]
            employee_name = request.form["employee_name"]
            employee_hours = request.form["employee_hours"]
            job = request.form["job"]

            query = "UPDATE Employees SET Employees.employee_name = %s, Employees.employee_hours = %s, Employees.job_ID = %s WHERE Employees.employee_ID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (employee_name, employee_hours, job, employee_ID))
            mysql.connection.commit()
            return redirect("/employees")
            
# Employees----------------------------------------

# Jobs --------------------------------------------

# Create and Read function for jobs table
@app.route("/jobs", methods=["POST", "GET"])
def jobs():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the jobs entity
    if request.method == "POST":
        # fire off if user presses the Add Job button
        if request.form.get("Add_Job"):
            job_title = request.form["job_title"]
            wage = request.form["wage"]

            query = "INSERT INTO Jobs (job_title, wage) VALUES (%s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (job_title, wage))
            mysql.connection.commit()

            # redirect back to jobs page
            return redirect("/jobs")

    # Grab data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all 
        query = "SELECT Jobs.job_ID, job_title, wage FROM Jobs"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("Jobs.j2", data=data)

# Delete function for jobs page
@app.route("/delete_jobs/<int:job_id>")
def delete_jobs(job_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Jobs WHERE job_ID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (job_id,))
    mysql.connection.commit()

    # redirect back to jobs page
    return redirect("/jobs")

# Edit function for jobs page
@app.route("/edit_jobs/<int:job_id>", methods=["POST", "GET"])
def edit_jobs(job_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Jobs WHERE job_id = %s" % (job_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_jobs.j2", data=data)


    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Jobs' button
        if request.form.get("Edit_Jobs"):
            # grab user form inputs
            job_ID = request.form["job_ID"]
            job_title = request.form["job_title"]
            wage = request.form["wage"]

            query = "UPDATE Jobs SET Jobs.job_title = %s, Jobs.wage = %s WHERE Jobs.job_ID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (job_title, wage, job_ID))
            mysql.connection.commit()

            return redirect("/jobs")

# Jobs --------------------------------------------


# Ingredients_Products Intersection Table ---------

# Create and Read functions for intersection table
@app.route("/ingredients_products", methods=["POST", "GET"])
def ingredients_products():
    if request.method == "POST":
        if request.form.get("Add_Ingredient_Product"):
            ingredient_ID = request.form["ingredient_ID"]
            prod_name = request.form["prod_name"]
            try:
                query = "INSERT INTO Ingredients_Products (ingredient_ID, prod_name) VALUES (%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (ingredient_ID, prod_name))
                mysql.connection.commit()
                return redirect("/ingredients_products")
            except Exception as e:
                print("Error occurred:", e)
                return str(e)  # Or return a custom error page

    if request.method == "GET":
        # mySQL query to grab all 
        query = "SELECT Ingredients_Products.ingredients_products_ID, Ingredients.item_name as ingredient, prod_name FROM Ingredients_Products LEFT JOIN Ingredients ON Ingredients_Products.ingredient_ID = Ingredients.ingredient_ID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Select for dropdown
        query2 = "SELECT ingredient_ID, item_name FROM Ingredients"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        ingredient_data = cur.fetchall()

        # Select for dropdown
        query3 = "SELECT prod_name FROM Products"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        product_data = cur.fetchall()

        return render_template("Ingredients_Products.j2", data=data, ingredients=ingredient_data, products=product_data)


# Delete function for intersection table
@app.route("/delete_ingredient_product/<int:ingredients_products_ID>")
def delete_ingredients_products(ingredients_products_ID):
    try:
        # mySQL query to delete the sale with our passed id
        query = "DELETE FROM Ingredients_Products WHERE ingredients_products_ID = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (ingredients_products_ID,))
        mysql.connection.commit()

        # redirect back to ingredients_products page
        return redirect("/ingredients_products")
    except Exception as e:
        print("Error occurred:", e)
        return str(e)  # Or return a custom error page


# Update function for intersection table
@app.route("/edit_ingredient_product/<int:ingredients_products_ID>", methods=["POST", "GET"])
def edit_ingredient_product(ingredients_products_ID):
    if request.method == "GET":
        try:
        # mySQL query to grab the info with our passed id
            query = "SELECT * FROM Ingredients_Products WHERE ingredients_products_ID = %s" % (ingredients_products_ID)
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            # mySQL query to grab data for our dropdown
            query2 = "SELECT ingredient_ID, item_name FROM Ingredients"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            ingredient_data = cur.fetchall()

            query3 = "SELECT prod_name FROM Products"
            cur = mysql.connection.cursor()
            cur.execute(query3)
            product_data = cur.fetchall()

            return render_template("edit_ingredient_product.j2", data=data, ingredients=ingredient_data, products=product_data)
        except Exception as e:
            print("Error occurred:", e)
            return str(e)  # Or return a custom error page
    
    if request.method == "POST":
        # fire off if user clicks the 'Edit Employees' button
        if request.form.get("Edit_Ingredient_Product"):
            # grab user form inputs
            ingredients_products_ID = request.form["ingredients_products_ID"]
            # original_name = request.form["original_name"]
            ingredient_ID = request.form["ingredient_ID"]
            prod_name = request.form["prod_name"]
            
            try:   
                query = "UPDATE Ingredients_Products SET Ingredients_Products.ingredient_ID = %s, Ingredients_Products.prod_name = %s WHERE Ingredients_Products.ingredients_products_ID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (ingredient_ID, prod_name, ingredients_products_ID))
                mysql.connection.commit()
                return redirect("/ingredients_products")
            except Exception as e:
                print("Error occurred:", e)
                return str(e)  # Or return a custom error page

# Ingredients_Products Intersection Table ---------


# Products_Sales Intersection Table ---------

# Create and Read function for intersection table
@app.route("/products_sales", methods=["POST", "GET"])
def products_sales():

    if request.method == "POST":
        if request.form.get("Add_Product_Sale"):
            prod_name = request.form["prod_name"]
            transaction_ID = request.form["transaction_ID"]
            quantity_sold = request.form["quantity_sold"]

            try:
                query = "INSERT INTO Products_Sales (prod_name, transaction_ID, quantity_sold) VALUES (%s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (prod_name, transaction_ID, quantity_sold))
                mysql.connection.commit()
                return redirect("/products_sales")
            except Exception as e:
                print("Error occurred:", e)
                return str(e)  # Or return a custom error page


    if request.method == "GET":
        # mySQL query to grab all 
        try:
            query = "SELECT Products_Sales.product_sales_ID, prod_name, transaction_ID, quantity_sold FROM Products_Sales ORDER BY transaction_ID"
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            # Select for dropdown
            query2 = "SELECT prod_name FROM Products"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            product_data = cur.fetchall()

            # Select for dropdown
            query3 = "SELECT transaction_ID FROM Sales"
            cur = mysql.connection.cursor()
            cur.execute(query3)
            sale_data = cur.fetchall()

            return render_template("Products_Sales.j2", data=data, products=product_data, sales=sale_data)
        except Exception as e:
            print("Error occurred:", e)
            return str(e)  # Or return a custom error page


# Delete function for intersection table
@app.route("/delete_product_sale/<int:product_sales_ID>")
def delete_product_sale(product_sales_ID):
    try:
        # mySQL query to delete the sale with our passed id
        query = "DELETE FROM Products_Sales WHERE product_sales_ID = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (product_sales_ID,))
        mysql.connection.commit()

        # redirect back to people page
        return redirect("/products_sales")
    except Exception as e:
        print("Error occurred:", e)
        return str(e)  # Or return a custom error page


# Update function for intersection table
@app.route("/edit_product_sale/<int:product_sales_ID>", methods=["POST", "GET"])
def edit_product_sales(product_sales_ID):
    if request.method == "GET":
        try:
        # mySQL query to grab the info with our passed id
            query = "SELECT * FROM Products_Sales WHERE product_sales_ID = %s" % (product_sales_ID)
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            # Select for dropdown
            query2 = "SELECT prod_name FROM Products"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            product_data = cur.fetchall()
            
            # Select for dropdown
            query3 = "SELECT transaction_ID FROM Sales"
            cur = mysql.connection.cursor()
            cur.execute(query3)
            sale_data = cur.fetchall()

            return render_template("edit_products_sales.j2", data=data, products=product_data, sales=sale_data)
        except Exception as e:
            print("Error occurred:", e)
            return str(e)  # Or return a custom error page
     
    if request.method == "POST":
        # fire off if user clicks the 'Edit Employees' button
        if request.form.get("Edit_Product_Sale"):
            # grab user form inputs
            product_sales_ID = request.form["product_sales_ID"]
            prod_name = request.form["prod_name"]
            transaction_ID = request.form["transaction_ID"]
            
            try:   
                query = "UPDATE Products_Sales SET Products_Sales.prod_name = %s, Products_Sales.transaction_ID = %s WHERE Products_Sales.product_sales_ID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (prod_name, transaction_ID, product_sales_ID))
                mysql.connection.commit()
                return redirect("/products_sales")
            except Exception as e:
                print("Error occurred:", e)
                return str(e)  # Or return a custom error page
# Products_Sales Intersection Table ---------

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=4502, debug=True)