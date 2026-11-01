
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Place Recommendation System",
    page_icon="✈️",
    layout="wide"
)

@st.cache_data
def load_data():
    destinations = pd.read_csv("data/destination_features.csv")
    attractions = pd.read_csv("data/matched_attractions.csv")
    return destinations, attractions

destination_features, attractions = load_data()

st.title("✈️ Place Recommendation System")
st.write("Discover destinations based on your travel interests.")
st.divider()

st.subheader("Tell us about your travel preferences")

user_interests = st.multiselect(
    "What are you interested in?",
    [
        "history", "culture", "religious",
        "nature", "architecture", "entertainment"
    ],
    format_func=lambda x: x.title()
)

top_n = st.slider(
    "Number of recommendations",
    min_value=3,
    max_value=10,
    value=5
)

# Keep recommendations visible after button clicks
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if st.button("Find My Destinations", type="primary"):

    if not user_interests:
        st.warning("Please select at least one travel interest.")
        st.session_state.recommendations = None

    else:
        available_places = destination_features[
            destination_features["total_attractions"] > 0
        ].copy()

        available_places["match_score"] = (
            available_places[user_interests].mean(axis=1)
        )

        st.session_state.recommendations = (
            available_places.sort_values(
                "match_score", ascending=False
            ).head(top_n)
        )

# Display recommendations
if st.session_state.recommendations is not None:

    st.subheader("Your Recommended Destinations")

    for _, place in st.session_state.recommendations.iterrows():

        destination_id = int(place["destination_id"])

        st.markdown(f"### 📍 {place['destination_name']}")
        st.progress(float(place["match_score"]))
        st.write(f"Match score: {place['match_score']:.2%}")

        destination_attractions = attractions[
            attractions["destination_id"] == destination_id
        ]

        attraction_count = len(destination_attractions)

        st.write(f"Available Tourist Places: {attraction_count}")

        button_key = f"view_{destination_id}"

        if button_key not in st.session_state:
            st.session_state[button_key] = False

        if st.button("📋 List of the Tourist Places", key=f"toggle_{destination_id}"):
            st.session_state[button_key] = (
                not st.session_state[button_key]
            )

        if st.session_state[button_key]:

            if attraction_count > 0:
                for number, (_, attraction) in enumerate(
                    destination_attractions.iterrows(), start=1
                ):
                    st.write(
                        f"{number}. **{attraction['name_en']}** "
                        f"— {attraction['category'].title()}"
                    )
            else:
                st.info("No attraction details available.")

        st.divider()
