# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize your smoothie :cup_with_straw:")
st.write(
  """choose fav fruit.
  """
)



name_on_order=st.text_input('name on smoo')
st.write ('name on s will be:',name_on_order )
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
#convert the snowflake data
pd_df=my.dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
ingredients_list = st.multiselect ( 
    'choose up to 5 ing:'
 , my_dataframe , max_selections=5
)

if ingredients_list:
    ingredients_string=''
    
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen+ ' '
        st.subheader(fruit_chosen+ 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)
      
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('submit order')
      
    if time_to_insert:
      session.sql(my_insert_stmt).collect()
       
      st.success('Your Smoothie is ordered!', icon="✅") 
      

