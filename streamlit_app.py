# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

@st.fragment(run_every="30s") # Check every 30 seconds
def auto_function():
        timeout_seconds = 600 # 5 minutes
        if time.time() - st.session_state.last_activity_timestamp > timeout_seconds:
            st.logout() # Logs out the user and clears session state

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)

name_on_order = st.text_input("Name on Smoothie:")
# st.write(name_on_order)
# option = st.selectbox('How would you like to be contacted',('Email','Home Phone', 'Mobile Phone'))
# st.write('You Selected:',option)

# fruit_option = st.selectbox('What is your favorite fruit?',('Banana','Stawberry','Peaches'))
# st.write('Your favourite frut is:',fruit_option)
# import streamlit as st


session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect('Choose up to 5 ingredients',my_dataframe,max_selections=5)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) values 
    ('""" + ingredients_string + """','""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if ingredients_string and time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered,"+name_on_order+"!", icon="✅")


    
