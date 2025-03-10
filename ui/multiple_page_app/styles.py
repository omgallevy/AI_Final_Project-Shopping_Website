import base64
import streamlit as st

from api.api import login_user, delete_user_by_username


def get_base64_image(file_path):
    with open(file_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    return f"data:image/png;base64,{encoded}"


def custom_css(background_image_path):
    background_image = get_base64_image(background_image_path)
    return f"""
        <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
         @import url('https://fonts.googleapis.com/css2?family=Sawarabi+Mincho&display=swap');

         h1, h2, h3, h4, h5, h6 {{
             font-family: 'Sawarabi Mincho', serif;
         }}

         * {{
             font-family: 'Sawarabi Mincho', serif;
         }}

        .stApp {{
            background-image: url("{background_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        
         [data-testid="stSidebarNav"] {{
            display: none;
        }}
        
        .stButton > button {{
            background-color: rgba(255, 255, 255, 0.7); 
            border: none;
            box-shadow: 0 4px 8px rgba(255, 192, 203, 0.5);
            border-radius: 10px;
            margin: 0 !important;
            padding: 10px 20px !important;
            display: inline-block;
            text-align: center;
            line-height: 1;
        }}

        .stButton > button:hover {{
            background-color: rgba(255, 255, 255, 0.85);
            box-shadow: 0 6px 10px rgba(255, 192, 203, 0.7);
        }}

        .stButton {{
            display: inline-block;
            margin: 0 !important;
        }}

        div[data-testid="stSidebarUserContent"] .stButton button {{
                width: 100% !important;
                min-width: 100px !important;
                padding: 0.5rem 1rem !important;
                height: 40px !important;
                white-space: nowrap !important;
                margin: 0 !important;
        }}

        .stRadio [role="radiogroup"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p {{
            color: #f249cc !important;
            font-weight: bold;
        }}

        .stRadio [role="radiogroup"] label:has(input:checked)::before {{
            background-color: #f249cc !important;
            border-color: #f249cc !important;
        }}

        [data-testid="stSidebar"] {{
            min-width: 200px; 
            max-width: 250px; 
        }}

        [data-testid="stSidebar"] {{
            background: rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }}
        </style>
    """


def sidebar(user, token, page_state):
    with st.sidebar:
        if user:
            st.header(f"Hey, {user}!")

            menu = st.radio(
                "Menu",
                ["Home", "Items", "Favorites", "Order", "Chat"],
                index=["Home", "Items", "Favorites", "Order", "Chat"].index(page_state["page"].capitalize()),
                key="menu_radio"
            )
            page_state["page"] = menu.lower()

            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                # if st.button("Sign Out"):
                #     page_state["user"] = None
                #     page_state["token"] = None
                #     page_state["page"] = "start"
                #     st.info("You have logged out of the system")
                #     st.rerun()
                if st.button("Sign Out"):
                    st.session_state.clear()
                    st.info("You have logged out of the system")
                    st.rerun()

            with col2:
                if st.button("Delete User"):
                    if user and token:
                        st.write(token)
                        success = delete_user_by_username(user, token)
                        if success:
                            page_state["user"] = None
                            page_state["token"] = None
                            page_state["page"] = "start"
                            st.success("The user was successfully deleted")
                            st.rerun()
                        else:
                            st.error("Error deleting user")
                    else:
                        st.error("Invalid username or token")
        else:
            st.header("Let's connect")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", placeholder="Enter your password", type="password")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login"):
                    token = login_user(username, password)
                    if token:
                        page_state["user"] = username
                        page_state["token"] = token
                        page_state["page"] = "home"
                        st.rerun()
                    else:
                        st.error("Incorrect username or password")
            with col2:
                if st.button("Signup"):
                    page_state["page"] = "registration"
                    st.session_state.page = "registration"
                    st.rerun()
