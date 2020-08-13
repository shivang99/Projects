import  json, os
import sqlite3
from flask import Flask, render_template, Response, request, redirect, url_for, jsonify



# get daily user report for each month
def get_month_brief(month):
    # sql command to get users for a particular month, given month
    month = str(month).zfill(2)
    cursor.execute("SELECT date(AU_date), COUNT(DISTINCT(AU_ID)) AS Total_users FROM all_active WHERE	strftime('%m',AU_DATE) = ?  GROUP BY AU_date", (month,))

    brief_file = cursor.fetchall()


    # returns a list with date and total users for that date
    return brief_file

#get total count of active users for each month
def get_month_total(z):
    allUsers = {}
    months = ['January', 'February', 'March', 'April', 'May']
    i = 0
    # loop to fetch users for each month and store into a dictionary
    while i < z:
        h = str(i+1).zfill(2)
        total_months = cursor.execute(
            "SELECT COUNT(DISTINCT(AU_ID)) AS total from all_active WHERE strftime('%m',AU_date) = ?",(h,))
        temp = total_months.fetchone()
        # fills dictionary with month at that index with the first element of the list from SQL query
        allUsers[months[i]] = temp[0]
        i += 1
    # returns a dictionary with acive users as value and each month as key
    return allUsers


# connect to SQL server

app = Flask(__name__)
cnxn = sqlite3.connect('C:\\sqlite3\\techlite.db',check_same_thread=False)
cursor = cnxn.cursor()


@app.route("/")
def index():
    return render_template('button.html')


@app.route("/dau", methods=['POST'])
def dau():
    if request.method == 'POST':
        option = request.form.get('options')  # access the data inside
        dictionary = {}
        # jsonify dictionary returned for get_month_brief function for different months
        if option == 'Jan':
            rows = get_month_brief(1)
            for row in rows:
                dictionary[row[0]] = row[1]
            return jsonify(dictionary)
        elif option == 'Feb':
            rows = get_month_brief(2)
            for row in rows:
                dictionary[row[0]] = row[1]
            return jsonify(dictionary)
        elif option == 'Mar':
            rows = get_month_brief(3)
            for row in rows:
                dictionary[row[0]] = row[1]
            return jsonify(dictionary)
        elif option == 'Apr':
            rows = get_month_brief(4)
            for row in rows:
                dictionary[row[0]] = row[1]
            return jsonify(dictionary)
        elif option == 'May':
            rows = get_month_brief(5)
            for row in rows:
                dictionary[row[0]] = row[1]
            return jsonify(dictionary)
        # jsonify dictionary returned from get_month_total function
        elif option == 'All':
            data = get_month_total(5)
            return jsonify(data)


if __name__ == '__main__':
    app.run()
