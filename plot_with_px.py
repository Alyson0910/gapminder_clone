import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

connection = sqlite3.connect("data/gapminder.db")
sql_quary = """
SELECT *
FROM plotting;
"""
plotting_df = pd.read_sql(sql_quary, con=connection)
connection.close()

print(plotting_df.shape)

fig = px.scatter(plotting_df, x="gdp_per_capita", y="life_expectancy", 
                 animation_frame="dt_year", animation_group="country_name",
                 size="population", color='continent', hover_name='country_name', 
                 size_max=100, range_x=[500, 100000], range_y=[20, 90],log_x=True,
                 title="Gapminder Clone 1800-2023")

fig.write_html("GapminderClone.html", auto_open=True)