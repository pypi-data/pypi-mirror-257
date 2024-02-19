from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import pandas as pd


def snowflake_queries_template(username,password):

    url = URL(
        account='kg71633.ap-south-1.aws',
        user=username,  # Add your username here
        password=password,  # Add your password here
        # Mostly use creds manager but just in case not working
        database='synergy',
        schema='production',
        # warehouse = 'query_wh',
        role='ds_team'
    )
    engine = create_engine(url)
    connection = engine.connect()

    QUERY = """
          select * from synergy.analytics_db.quality_ata_itd 
          where call_date_ist >= '2023-07-01'
          and business_name in ('Redbus', 'Delhivery', 'Classplus')
          and parameter ilike '%disposition%'
        """

    # This function once called will fetch the data from the query declared as a variable.
    def query_data():
        df_temp = pd.read_sql((QUERY), connection)
        return df_temp
    data = query_data()
    return data
