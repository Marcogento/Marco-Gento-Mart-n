import streamlit as st
import pandas as pd
import plotly.express as px
import os
# Load Data
csv_file = os.path.join(os.path.dirname(_file_), "airbnb.csv")
data = pd.read_csv(csv_file)

# Clean Data
data = data.dropna(subset=['room_type', 'price', 'number_of_reviews', 'neighbourhood', 'availability_365'])

# Streamlit App Title
st.title("Marco Gento Martín")

# Sidebar Filters
st.sidebar.header("Filter Listings")
selected_neighbourhood = st.sidebar.selectbox("Select Neighbourhood", options=data['neighbourhood'].unique())
selected_room_type = st.sidebar.selectbox("Select Room Type", options=data['room_type'].unique())
price_range = st.sidebar.slider("Price Range", min_value=int(data['price'].min()), max_value=int(data['price'].max()), value=(50, 200))

# Apply Filters
filtered_data = data[(data['neighbourhood'] == selected_neighbourhood) &
                     (data['room_type'] == selected_room_type) &
                     (data['price'].between(price_range[0], price_range[1]))]

# Tabs
tab1, tab2 = st.tabs(["Analysis", "Top Listings"])

# Graph 1: Room Type vs. Availability (as a proxy for 'number of people')
with tab1:
    st.subheader("Room Type vs. Availability")
    fig1 = px.box(filtered_data, x="room_type", y="availability_365", title="Availability by Room Type")
    st.plotly_chart(fig1)

# Graph 2: Price Distribution by Room Type
with tab1:
    st.subheader("Price Distribution")
    fig2 = px.histogram(filtered_data, x="price", color="room_type", title="Price vs Room Type")
    st.plotly_chart(fig2)

# Graph 3: Top Reviewed Listings
with tab2:
    top_reviews = data.sort_values(by='number_of_reviews', ascending=False).head(10)
    st.subheader("Top Listings by Reviews")
    fig3 = px.bar(top_reviews, x='name', y='number_of_reviews', color='neighbourhood', title="Most Reviewed Listings")
    st.plotly_chart(fig3)

# Price Recommendation Simulator
st.sidebar.header("Price Recommendation Simulator")
selected_sim_neighbourhood = st.sidebar.selectbox("Select Neighbourhood for Pricing", options=data['neighbourhood'].unique())
selected_sim_room_type = st.sidebar.selectbox("Select Room Type for Pricing", options=data['room_type'].unique())

similar_listings = data[(data['neighbourhood'] == selected_sim_neighbourhood) & (data['room_type'] == selected_sim_room_type)]
if not similar_listings.empty:
    suggested_price_range = (similar_listings['price'].quantile(0.25), similar_listings['price'].quantile(0.75))
    st.sidebar.write(f"Suggested Price Range: ${suggested_price_range[0]:.2f} - ${suggested_price_range[1]:.2f}")
else:
    st.sidebar.write("No similar listings found to suggest a price range.")