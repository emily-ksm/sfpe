import streamlit as st
import random

# --- Product Data with More Info ---
products = [
    {
        "name": "Hydrating Toner",
        "concerns": ["dryness", "dullness"],
        "ingredients": ["hyaluronic acid"],
        "description": "A lightweight toner that hydrates and preps the skin for better absorption of serums.",
        "benefits": "Replenishes moisture, balances pH, and refreshes skin.",
        "how_to_use": "After cleansing, apply to face with a cotton pad or hands.",
        "skin_type": "Best for dry and combination skin."
    },
    {
        "name": "Vitamin C Serum",
        "concerns": ["dullness", "dark spots"],
        "ingredients": ["vitamin c"],
        "description": "Brightens and evens out your skin tone with a potent dose of Vitamin C.",
        "benefits": "Fades dark spots, protects from free radicals, and boosts radiance.",
        "how_to_use": "Apply 3-4 drops to clean face in the morning before moisturizer.",
        "skin_type": "Best for all skin types."
    },
    {
        "name": "Niacinamide Serum",
        "concerns": ["oiliness", "acne"],
        "ingredients": ["niacinamide"],
        "description": "Controls oil production and minimizes pores while reducing acne.",
        "benefits": "Balances sebum, reduces redness, and prevents breakouts.",
        "how_to_use": "Use after toner and before moisturizer, morning and night.",
        "skin_type": "Best for oily and acne-prone skin."
    },
    {
        "name": "Peptide Cream",
        "concerns": ["aging"],
        "ingredients": ["peptides"],
        "description": "Boosts collagen production and helps to smooth fine lines.",
        "benefits": "Firms skin, reduces wrinkles, and improves elasticity.",
        "how_to_use": "Massage into face and neck as the last step of skincare.",
        "skin_type": "Best for mature and dry skin."
    }
]

# User preferences
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "concerns": ["dryness", "dullness"],
        "liked_ingredients": ["hyaluronic acid", "vitamin c"]
    }

def recommend_products(user_profile, products, n=3):
    scored_products = []
    for product in products:
        score = 0
        for concern in user_profile["concerns"]:
            if concern in product["concerns"]:
                score += 2
        for ingredient in user_profile["liked_ingredients"]:
            if ingredient in product["ingredients"]:
                score += 3
        scored_products.append((product, score))
    scored_products.sort(key=lambda x: x[1], reverse=True)
    return [p[0] for p in scored_products[:n]]

# --- Streamlit UI ---
st.title("🌸 SkinFlix – Your Skincare Recommender")
st.write("Discover skincare products recommended just for you!")

# Sidebar
st.sidebar.header("Your Skin Profile")
concerns = st.sidebar.multiselect(
    "What are your skin concerns?",
    ["dryness", "dullness", "acne", "aging", "dark spots", "oiliness", "sensitivity"],
    default=st.session_state.user_profile["concerns"]
)
liked_ingredients = st.sidebar.multiselect(
    "Favorite ingredients?",
    ["hyaluronic acid", "vitamin c", "retinol", "niacinamide", "peptides", "aloe vera"],
    default=st.session_state.user_profile["liked_ingredients"]
)
st.session_state.user_profile["concerns"] = concerns
st.session_state.user_profile["liked_ingredients"] = liked_ingredients

# Recommendations
st.subheader("Recommended For You")
recommended = recommend_products(st.session_state.user_profile, products)

for p in recommended:
    with st.expander(f"**{p['name']}** – Click for details"):
        st.markdown(f"**Description:** {p['description']}")
        st.markdown(f"**Benefits:** {p['benefits']}")
        st.markdown(f"**How to Use:** {p['how_to_use']}")
        st.markdown(f"**Skin Type:** {p['skin_type']}")
        st.caption(f"Concerns: {', '.join(p['concerns'])} | Ingredients: {', '.join(p['ingredients'])}")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"👍 Like {p['name']}"):
                for ing in p["ingredients"]:
                    if ing not in st.session_state.user_profile["liked_ingredients"]:
                        st.session_state.user_profile["liked_ingredients"].append(ing)
                st.rerun()
        with col2:
            if st.button(f"👎 Dislike {p['name']}"):
                for ing in p["ingredients"]:
                    if ing in st.session_state.user_profile["liked_ingredients"]:
                        st.session_state.user_profile["liked_ingredients"].remove(ing)
                st.rerun()
