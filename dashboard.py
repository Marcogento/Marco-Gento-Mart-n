import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data  # Cache the data to avoid reloading
def load_data():
    df = pd.read_csv("airbnb.csv")  # Replace with your file path
    return df

df = load_data()

# Clean Data (if needed)
df = df.dropna(subset=['neighbourhood', 'room_type', 'price', 'number_of_reviews', 'availability_365'])

# Streamlit App Title
st.title("Airbnb Listings Dashboard - Marco Gento Martín")

# Sidebar Filters
st.sidebar.header("Filter Listings")
selected_neighbourhood = st.sidebar.selectbox("Select Neighbourhood", options=df['neighbourhood'].unique())
selected_room_type = st.sidebar.selectbox("Select Room Type", options=df['room_type'].unique())
price_range = st.sidebar.slider("Price Range", min_value=int(df['price'].min()), max_value=int(df['price'].max()), value=(50, 200))

# Apply Filters
filtered_data = df[
    (df['neighbourhood'] == selected_neighbourhood) &
    (df['room_type'] == selected_room_type) &
    (df['price'].between(price_range[0], price_range[1]))
]

# Tabs
tab1, tab2 = st.tabs(["Analysis", "Top Listings"])

# Tab 1: Analysis
with tab1:
    st.header("Analysis of Airbnb Listings")

    # Graph 1: Relationship between Room Type and Number of Reviews
    st.subheader("Room Type vs. Number of Reviews")
    fig1 = px.scatter(filtered_data, x="room_type", y="number_of_reviews", color="price", 
                      title="Room Type vs. Number of Reviews (Colored by Price)")
    st.plotly_chart(fig1)

    # Graph 2: Price Distribution by Neighbourhood (Violin Plot)
    st.subheader("Price Distribution by Neighbourhood")
    fig2 = px.violin(filtered_data, x="neighbourhood", y="price", box=True, points="all", 
                     title="Price Distribution by Neighbourhood")
    st.plotly_chart(fig2)

# Tab 2: Top Listings
with tab2:
    st.header("Top Airbnb Listings")

    # Graph 3: Top 10 Listings by Price and Reviews (Bubble Chart)
    st.subheader("Top 10 Listings by Price and Reviews")
    top_listings = df.nlargest(10, 'number_of_reviews')
    fig3 = px.scatter(top_listings, x="price", y="number_of_reviews", size="availability_365", 
                      color="neighbourhood", hover_name="name", 
                      title="Top 10 Listings by Price and Reviews (Size = Availability)")
    st.plotly_chart(fig3)

    # Graph 4: Average Price by Room Type and Neighbourhood (Heatmap)
    st.subheader("Average Price by Room Type and Neighbourhood")
    avg_price = df.groupby(['neighbourhood', 'room_type'])['price'].mean().unstack()
    fig4 = px.imshow(avg_price, labels=dict(x="Room Type", y="Neighbourhood", color="Price"), 
                     title="Average Price by Room Type and Neighbourhood")
    st.plotly_chart(fig4)

# Optional: Price Recommendation Simulator
st.sidebar.header("Price Recommendation Simulator")
sim_neighbourhood = st.sidebar.selectbox("Select Neighbourhood for Pricing", options=df['neighbourhood'].unique())
sim_room_type = st.sidebar.selectbox("Select Room Type for Pricing", options=df['room_type'].unique())
sim_min_nights = st.sidebar.slider("Minimum Nights", min_value=1, max_value=365)

# Simulate price range (example logic)
similar_listings = df[
    (df['neighbourhood'] == sim_neighbourhood) &
    (df['room_type'] == sim_room_type) &
    (df['minimum_nights'] == sim_min_nights)
]
if not similar_listings.empty:
    suggested_price_range = (similar_listings['price'].quantile(0.25), similar_listings['price'].quantile(0.75))
    st.sidebar.write(f"Suggested Price Range: ${suggested_price_range[0]:.2f} - ${suggested_price_range[1]:.2f}")
else:
    st.sidebar.write("No similar listings found to suggest a price range.")