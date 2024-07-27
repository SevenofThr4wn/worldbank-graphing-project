from app import app
from flask import render_template, request
import plotly.express as px
import plotly.utils
import json
from app.db import get_db
import pandas as pd


# creates the webpage
@app.route('/graph',  methods=['GET', 'POST'])
def graphPage():
    # Selects all the CountryCode & ShortName except when Region field is equal to NULL
    db = get_db()
    list_sql = "SELECT CountryCode,ShortName FROM Country EXCEPT SELECT CountryCode, ShortName FROM Country WHERE Region IS NULL"
    sql_results2 = db.execute(list_sql)
    countrylist = sql_results2.fetchall()
    # determines when the Submit button is pressed and the country that the user has selected to display on the website
    if request.method == 'POST':
        CountryCode = request.form.get('Country')
    else:
        # Sets the default country to Australia
        CountryCode="AUS"
    sql = "SELECT Value, Year FROM Data WHERE IndicatorCode = 'GE.EST' AND Year BETWEEN 1960 AND 2019 AND CountryCode = ?"
    sql_results = db.execute(sql, (CountryCode,))
    df = pd.DataFrame(sql_results.fetchall(), columns=['Value', 'Year'])
    fig = px.line(df, x="Year", y="Value", title="Global Government Effectiveness",)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', graphJSON=graphJSON, countrylist=countrylist, CountryCode=CountryCode)
