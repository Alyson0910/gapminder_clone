import sqlite3
import pandas as pd

class CreateGapminderDB:
    def __init__(self):
        self.file_names = ["ddf--datapoints--gdp_pcap--by--country--time", 
                            "ddf--datapoints--lex--by--country--time", 
                            "ddf--datapoints--pop--by--country--time", 
                            "ddf--entities--geo--country"]
        self.table_names = ["gdp_pcap", "life_expectancy", "population", "geography"]
         
    def import_as_dataframe(self):
        df_dict = dict()
        for file_name, table_name in zip(self.file_names, self.table_names):
            file_path = f"data/{file_name}.csv"
            df = pd.read_csv(file_path)
            df_dict[table_name] = df
        return df_dict
    
    def create_database(self):
        df_dict = self.import_as_dataframe()
        connection = sqlite3.connect('data/gapminder.db')
        for k, v in df_dict.items():
            v.to_sql(name=k, con=connection, index=False, if_exists='replace')

        drop_view_sql = """
        DROP VIEW IF EXISTS plotting;
        """

        create_view_sql = """
        CREATE VIEW plotting AS
        SELECT 
            geography.name AS country_name,
            geography.world_4region AS continent,
            gdp_pcap.time AS dt_year,
            gdp_pcap.gdp_pcap AS gdp_per_capita,
            life_expectancy.lex AS life_expectancy,
            population.pop AS population
        FROM gdp_pcap
        JOIN geography
        ON 
            gdp_pcap.country = geography.country
            JOIN life_expectancy
        ON 
            gdp_pcap.country = life_expectancy.country AND 
            gdp_pcap.time = life_expectancy.time
        JOIN population
        ON 
            gdp_pcap.country = population.country AND 
            gdp_pcap.time = population.time
        WHERE gdp_pcap.time < 2024;
        """

        cur = connection.cursor()
        cur.execute(drop_view_sql)
        cur.execute(create_view_sql)

        connection.close()

create_gapminder_db = CreateGapminderDB()
create_gapminder_db.create_database()
