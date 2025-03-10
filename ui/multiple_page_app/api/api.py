import requests
import streamlit as st


BASE_URL = "http://localhost:8000"


def get_all_items():
    url = f"{BASE_URL}/items/"
    items = requests.get(url)
    return items.json()


def get_items_by_name(keyword: str):
    url = f"{BASE_URL}/items/name/{keyword}/"
    items = requests.get(url)

    if items.status_code == 200:
        data = items.json()
        if not data:
            return []
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        else:
            raise ValueError("Unexpected items format")
    else:
        raise Exception(f"HTTP Error {items.status_code}: {items.text}")


def get_items_by_stock(stock: int):
    url = f"{BASE_URL}/items/stock/{stock}/"
    items = requests.get(url)
    return items.json()


def get_items_stock_less_than(stock: int):
    url = f"{BASE_URL}/items/stock/less_than/{stock}/"
    items = requests.get(url)
    return items.json()


def get_items_stock_greater_than(stock: int):
    url = f"{BASE_URL}/items/stock/greater_than/{stock}/"
    items = requests.get(url)
    return items.json()


def get_user_by_username(username: str, token: str):
    url = f"{BASE_URL}/user/{username}/"
    headers = {"Authorization": f"Bearer {token['jwt_token']}"}
    response = requests.get(url, headers=headers)
    return response.json()


def create_user(user_request: dict):
    url = f"{BASE_URL}/user/"
    try:
        response = requests.post(url, json=user_request)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"שגיאה בשליחת הנתונים: {e}")


def delete_user(user_id, token):
    url = f"{BASE_URL}/user/delete/{user_id}/"
    headers = {"Authorization": f"Bearer {token['jwt_token']}"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.status_code == 204


def delete_user_by_username(username, token):
    url = f"{BASE_URL}/user/delete/{username}/"
    headers = {"Authorization": f"Bearer {token['jwt_token']}"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        return True
    else:
        response.raise_for_status()


def login_user(username, password):
    url = f"{BASE_URL}/auth/token/"
    data = {
        "username": username,
        "password": password,
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")
        return None


def get_user_id_by_username(username):
    url = f"{BASE_URL}/user/{username}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("id")
    else:
        st.error(f"Error retrieving user ID: {response.status_code} - {response.text}")
        return None


def get_all_favorites_by_username(token, username):
    url = f"{BASE_URL}/favorites/users/username/{username}/favorites"
    headers = {"Authorization": f"Bearer {token['jwt_token']}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"שגיאה בקבלת המועדפים: {response.status_code}")
        return []


def get_favorite_item_by_name(token, item_name):
    url = f"{BASE_URL}/favorites/{item_name}/"
    headers = {"Authorization": f"Bearer {token['jwt_token']}"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None


def create_favorite_item_by_name(token, item_name):
    url = f"{BASE_URL}/favorites/items_name/"
    headers = {"Authorization": f"Bearer {token['jwt_token']}"}

    params = {"item_name": item_name}
    response = requests.post(url, headers=headers, params=params)

    if response.status_code == 200:
        return True
    else:
        st.error(f"Error adding to favorites: {response.status_code} - {response.text}")
        return None


def delete_favorite_item_by_name(token, item_name):
    url = f"{BASE_URL}/favorites/delete/{item_name}/"
    headers = {"Authorization": f"Bearer {token['jwt_token']}"}
    response = requests.delete(url, headers=headers)
    return response.json() if response.status_code == 200 else None


def get_orders_by_username(username, token):
    url = f"{BASE_URL}/orders/username/{username}"
    headers = {"Authorization": f"Bearer {token['jwt_token']}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            orders_data = response.json()
            return orders_data
        else:
            st.error(f"Failed to fetch orders. Status code: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching orders: {str(e)}")
        return []


def create_order(order_data, token):
    url = f"{BASE_URL}/orders/"
    headers = {"Authorization": f"Bearer {token['jwt_token']}"}
    response = requests.post(url, json=order_data, headers=headers)
    if not order_data.get("items") or not order_data.get("total_price"):
        st.error("Missing items or price in order!")
        return None
    if response.status_code == 200:
        st.success("Order created successfully")
        return response.json()
    else:
        st.error(response.json().get("detail"))
        return None


def update_order(order_id, order_data, token):
    url = f"{BASE_URL}/orders/{order_id}/purchase/"
    headers = {"Authorization": f"Bearer {token['jwt_token']}"}
    response = requests.post(url, json=order_data, headers=headers)
    if response.status_code == 204:
        st.success("Order updated successfully")
    else:
        st.error("Failed to update order")


def close_order(order_id, user_id, token):
    url = f"{BASE_URL}/orders/close/{order_id}"
    headers = {"Authorization": f"Bearer {token['jwt_token']}"}
    data = {"user_id": user_id}
    response = requests.post(url, params=data, headers=headers)
    if response.status_code == 200:
        st.success("Order closed successfully")
        return True
    else:
        st.error(f"Failed to close order: {response.text}")
        return False


def delete_order(order_id, token):
    url = f"{BASE_URL}/orders/delete/{order_id}/"
    headers = {"Authorization": f"Bearer {token['jwt_token']}"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        st.success("Order deleted successfully")
    else:
        st.error(f"Failed to delete order. Status code: {response.status_code}")
