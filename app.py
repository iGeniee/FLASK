from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import json

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('Data.csv', encoding='ISO-8859-1')

@app.route('/')
def dashboard():
    # Filter and sort top 5 by 'Yearly Gallons Per Capita'
    top_5_consumption_data = data.sort_values(by='Yearly Gallons Per Capita', ascending=False).head(5)
    top_5_price_data = data.sort_values(by='Price Per Gallon (USD)', ascending=False).head(5)
    top_5_consumption_share_data = data.sort_values(by='Daily Oil Consumption (Barrels)', ascending=False).head(5)

    # Convert data to HTML table (top 5 rows)
    table_html = top_5_consumption_data.to_html(classes='table table-striped', index=False)

    # Bar Chart: Price Per Gallon (USD) by Country
    bar_chart = px.bar(top_5_price_data, x='Country', y='Price Per Gallon (USD)',
                       title='Price Per Gallon (USD) by Country',
                       labels={'Price Per Gallon (USD)': 'Price (USD)'})
    bar_chart_json = bar_chart.to_json()  # Convert the chart to JSON

    # Line Chart: Daily Oil Consumption by Country (Top 5)
    line_chart = px.line(top_5_consumption_share_data, x='Country', y='Daily Oil Consumption (Barrels)',
                         title='Daily Oil Consumption (Barrels) by Country')
    line_chart_json = line_chart.to_json()  # Convert the chart to JSON

    # Pie Chart: Yearly Gallons Per Capita by Country (Top 5)
    pie_chart = px.pie(top_5_consumption_data, names='Country', values='Yearly Gallons Per Capita',
                       title='Yearly Gallons Per Capita by Country')
    pie_chart_json = pie_chart.to_json()  # Convert the chart to JSON

    return render_template('dashboard.html',
                           table_html=table_html,
                           bar_chart=bar_chart_json,
                           line_chart=line_chart_json,
                           pie_chart=pie_chart_json)

if __name__ == '__main__':
    app.run(debug=True)
