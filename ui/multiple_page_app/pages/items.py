import streamlit as st
from styles import sidebar, custom_css

import pandas as pd

from api.api import (get_items_by_stock, get_items_stock_greater_than, get_items_stock_less_than,
                     get_items_by_name, get_all_items, create_favorite_item_by_name)



def display_error(error_msg: str):
    st.error(f"Error: {error_msg}")


def display_items_table(items, token):
    if items:
        df = pd.DataFrame(items)
        header_cols = st.columns([3, 2, 2, 1])
        with header_cols[0]:
            st.write("**Name**")
        with header_cols[1]:
            st.write("**Price**")
        with header_cols[2]:
            st.write("**Stock**")
        with header_cols[3]:
            st.write("**Favorites**")

        st.divider()
        for index, row in df.iterrows():
            with st.container():
                cols = st.columns([3, 2, 2, 1])

                with cols[0]:
                    st.write(row['name'])

                with cols[1]:
                    st.write(f"${row['price']}")

                with cols[2]:
                    st.write(f"{row['stock']}")

                with cols[3]:
                    if st.button("❤️", key=f"fav_{row['name']}"):
                        if token:
                            response = create_favorite_item_by_name(token, row['name'])
                            if response:
                                st.success(f"{row['name']} added to favorites!")
                                st.rerun()
                            else:
                                st.error("Failed to add item to favorites")
                        else:
                            st.error("Please login")

                st.divider()

        st.divider()

    else:
        st.info("No items found")


def search_by_stock(token):
    col1, col2 = st.columns([2, 1])
    with col1:
        search_type = st.selectbox(
            "Select search type",
            ["Exact stock", "Stock greater than", "Stock less than"]
        )
    with col2:
        stock_value = st.number_input("Stock quantity", min_value=0, step=1)

    if st.button("Search by Stock"):
        try:
            if search_type == "Exact stock":
                items = get_items_by_stock(stock_value)
            elif search_type == "Stock greater than":
                items = get_items_stock_greater_than(stock_value)
            else:
                items = get_items_stock_less_than(stock_value)
            display_items_table(items, token)
        except Exception as e:
            display_error(str(e))


def search_by_name(token):
    keyword = st.text_input("Enter a search term")
    if st.button("Search by Name") and keyword:
        try:
            items = get_items_by_name(keyword)
            display_items_table(items, token)
        except Exception as e:
            display_error(str(e))


def show_all_items(token):
    if st.button("Show All Items"):
        try:
            items = get_all_items()
            display_items_table(items, token)
        except Exception as e:
            display_error(str(e))


def show_items_page(token=None):
    current_token = token


    st.markdown(custom_css("assets/BG01.png"), unsafe_allow_html=True)
    st.image("assets/Emotion Potion.png", width=400)
    st.header("Search")
    search_option = st.radio(
        "Select a search method",
        ["Show All", "Search by Stock", "Search by Name"],
        horizontal=True,
    )

    st.divider()

    if search_option == "Show All":
        try:
            items = get_all_items()
            display_items_table(items, current_token)
        except Exception as e:
            display_error(str(e))
    elif search_option == "Search by Stock":
        search_by_stock(current_token)
    else:
        search_by_name(current_token)

