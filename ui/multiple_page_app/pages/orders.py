import streamlit as st
from api.api import (
    get_orders_by_username,
    create_order,
    close_order,
    get_all_items,
    delete_order,
    get_user_by_username
)


def show_orders_page(user=None, token=None):
    current_user = user
    current_token = token

    if not current_user or not current_token:
        st.warning("You must be logged in to view orders")
        return

    try:
        user_data = get_user_by_username(current_user, current_token)
        if not user_data or "id" not in user_data:
            st.error("Could not retrieve user information")
            return
        user_id = user_data["id"]
        city = str(user_data["city"])
        country = str(user_data["country"])
        user_shipping_address = f"{city} , {country}"
    except Exception as e:
        st.error(f"Error retrieving user information: {str(e)}")
        return

    st.title("Your Orders")

    st.subheader("✦ Create New Order")
    items = get_all_items()
    if not items:
        st.info("There are no available items to create an order.")
    else:
        selected_items = st.multiselect("Select items for order", [item['name'] for item in items])
        shipping_address = st.text_input("Shipping Address", user_shipping_address)

        item_quantities = {}
        for item_name in selected_items:
            item_quantities[item_name] = st.number_input(f"Quantity for {item_name}", min_value=1, value=1)

        if st.button("Create Order"):
            order_items = []
            total_price = 0
            for item_name in item_quantities.keys():
                for item in items:
                    if item["name"] == item_name:
                        item_id = item["id"]
                        item_price = item["price"]
                        item_quantity = item_quantities[item_name]
                        total_price += item_price * item_quantity

                        order_items.append({
                            "item_id": item_id,
                            "quantity": item_quantities[item_name]
                        })

            if order_items:
                order_data = {
                    "shipping_address": shipping_address,
                    "items": order_items,
                    "total_price": total_price
                }
                result = create_order(order_data, current_token)
                if result:
                    st.success("Order created successfully!")
                    st.rerun()

    try:
        orders = get_orders_by_username(current_user, current_token)
    except Exception as e:
        st.error(f"Error fetching orders: {str(e)}")
        orders = []

    if not orders:
        st.info("You don't have any orders yet.")
        return

    temp_orders = [order for order in orders if order.get('status') == 'TEMP']
    closed_orders = [order for order in orders if order.get('status') == 'CLOSE']

    if temp_orders:
        st.subheader("🟢 Open Orders (TEMP)")

        for order in temp_orders:
            with st.expander(f"Order #{order['id']} - {order.get('total_price', '0')}$"):
                st.write(f"Shipping Address: {order.get('shipping_address', 'Not specified')}")
                st.write("Items in order:")

                if order['items']:
                    updated_items = order['items'].copy()
                    for i, item in enumerate(updated_items):
                        col1, col2 = st.columns([1, 10])
                        with col1:
                            if st.button("✖", key=f"remove_{order['id']}_{i}", help="Remove item"):
                                updated_items.pop(i)
                                if not updated_items:
                                    delete_order(order['id'], current_token)
                                else:
                                    order_data = {
                                        "shipping_address": order.get('shipping_address'),
                                        "items": updated_items,
                                        "total_price": sum(item.get('price', 0) * item.get('quantity', 0)
                                                           for item in updated_items)
                                    }
                                    delete_order(order['id'], current_token)
                                    create_order(order_data, current_token)
                                st.rerun()
                        with col2:
                            item_title = item.get('title')
                            item_price = item.get('price')
                            item_quantity = item.get('quantity')
                            st.write(f"{item_title} (x{item_quantity}) - {item_price}$")
                else:
                    st.write("No items in this order")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"️ Purchase", key=f"purchase_{order['id']}"):
                        close_order(order['id'], user_id, current_token)
                        st.rerun()
                with col2:
                    if st.button(f"️ Delete", key=f"delete_{order['id']}"):
                        delete_order(order['id'], current_token)
                        st.rerun()

    if closed_orders:
        st.subheader("Closed Orders (CLOSE)")
        for order in closed_orders:
            with st.expander(f"Order #{order['id']} - {order.get('total_price', '0')}$"):
                st.write(f"Shipping Address: {order.get('shipping_address', 'Not specified')}")
                st.write("Items in order:")
                if 'items' in order and order['items']:
                    for item in order['items']:
                        item_title = item.get('title', 'Unknown')
                        item_price = item.get('price', 0)
                        item_quantity = item.get('quantity', 0)
                        st.write(f"- {item_title} (x{item_quantity}) - {item_price}$")
                else:
                    st.write("No items in this order")