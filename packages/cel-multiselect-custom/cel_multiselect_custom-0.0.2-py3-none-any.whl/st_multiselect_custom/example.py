import streamlit as st
from st_multiselect_custom import st_multiselect_custom

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run st_multiselect_custom/example.py`

st.subheader("Component with constant args")


# Create an instance of our component with a constant `name` arg, and
# print its output value.
with st.sidebar:
    num_clicks = st_multiselect_custom(["A", "B", "C", "D", "E", "F"])
    st.markdown(num_clicks)
