import streamlit as st
from api.api import (
    get_all_favorites_by_username,
    get_favorite_item_by_name,
    create_favorite_item_by_name,
    delete_favorite_item_by_name,
    get_all_items
)

from styles import sidebar, custom_css


def show_favorites_page(user=None, token=None):
    current_user = user
    current_token = token

    if not current_user or not current_token:
        st.warning("You must be logged in to view favorites")
        return

    if "favorites_action" not in st.session_state:
        st.session_state["favorites_action"] = "View Favorites"

    st.markdown(custom_css("assets/BG02.png"), unsafe_allow_html=True)
    st.image("assets/Emotion Potion.png", width=400)
    st.title("My Favorites")

    action = st.radio(
        "Select an action",
        ["View Favorites", "Add Favorite", "Delete Favorite"],
        horizontal=True,
        key="favorites_radio",
        index=["View Favorites", "Add Favorite", "Delete Favorite"].index(
            st.session_state.get("favorites_action", "View Favorites")
        )
    )

    st.session_state.favorites_action = action

    if action == "View Favorites":
        display_favorites(current_token, current_user)
    elif action == "Add Favorite":
        add_favorite(current_token)
    elif action == "Delete Favorite":
        delete_favorite(current_token, current_user)


def display_favorites(token, username):
    if not token:
        st.error("Invalid token. Please log in again.")
        return

    favorites = get_all_favorites_by_username(token, username)
    if isinstance(favorites, dict) and "error" in favorites:
        st.error(f"Error fetching favorites: {favorites['error']}")
        return

    if not favorites:
        st.info("You have no favorite items yet")
        return

    for favorite in favorites:
        with st.container():
            st.subheader(favorite['item_name'])
            st.write(f"Price: ${favorite.get('item_price')}")
            st.write(f"Stock: {favorite.get('item_stock')}")


def add_favorite(token):
    if not token:
        st.error("Invalid token. Please log in again.")
        return

    items = get_all_items()
    if not items:
        st.info("No items available to add to favorites")
        return

    selected_items = st.multiselect("Select items to add to favorites", [item['name'] for item in items])

    if st.button("Add Selected Items to Favorites"):
        for item_name in selected_items:
            response = create_favorite_item_by_name(token, item_name)
            if response:
                st.success("Selected items added to favorites")
            else:
                st.error("Failed to add items to favorites")


def delete_favorite(token, username):
    if not token:
        st.error("Invalid token. Please log in again.")
        return

    favorites = get_all_favorites_by_username(token, username)
    if not favorites:
        st.info("You have no favorite items to delete")
        return

    for index, favorite in enumerate(favorites):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(favorite['item_name'])
        with col2:
            if st.button("Delete", key=f"delete_{index}"):
                delete_favorite_item_by_name(token, favorite['item_name'])
                st.success(f"{favorite['item_name']} deleted successfully")
                st.rerun()
