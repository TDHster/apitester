import streamlit as st
import requests
from PIL import Image
import os


api_endpoint_file = 'api_endpoint.cfg'
def save_value_to_file(value, filename):
    with open(filename, 'w') as file:
        file.write(value)


def load_value_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None


def save_uploaded_file(uploaded_file, upload_dir="uploaded_files"):
    # Create the upload directory if it doesn't exist
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, uploaded_file.name)

    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def send_file_to_api(api_endpoint='http://51.20.224.172:8000/convert_file/', file_path='uploaded_files/mail.eml'):
    with open(file_path, 'rb') as file:
        files = {'file': file}
        try:
            response = requests.post(api_endpoint, files=files, timeout=30)
            if response.status_code == 200:
                return response.status_code, response.headers['Content-Disposition'], response.content
            return response.status_code, response.headers, None
        except Exception as error:
            return None, error, None


def remove_file(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error removing file '{file_path}': {e}")


def main():
    title = 'Mail converter API tester'

    favicon = Image.open("favicon.ico")
    st.set_page_config(
        page_title=title,
        page_icon=favicon,
        initial_sidebar_state="collapsed",
        menu_items=None
    )
    # Remove "deploy" button
    st.markdown(
        r"""
        <style>
        .stDeployButton {
                visibility: hidden;
            }
        </style>
        """, unsafe_allow_html=True
    )
    st.subheader(title)
    api_endpoint = load_value_from_file(api_endpoint_file)
    api_endpoint = api_endpoint if api_endpoint is not None else 'http://localhost:8000/convert_file'
    api_endpoint = st.text_input("API endpoint:", value=api_endpoint)

    uploaded_file = st.file_uploader("Choose a file:", type=["eml"])
    if uploaded_file is not None:
        test_file_path = save_uploaded_file(uploaded_file)

        st.write("File uploaded successfully!")
        if st.button("Send file to API"):
            save_value_to_file(api_endpoint, api_endpoint_file)
            # st.text('Sending to API...')
            empty_sending = st.empty()
            empty_sending.text('Sending to API and waiting response...')
            print(f'To {api_endpoint} sending: {test_file_path}')
            response_status_code, response_disposition, response_content = send_file_to_api(api_endpoint, test_file_path)
            empty_sending.text('Sending to API and waiting response - Done.')
            remove_file(test_file_path)
            st.subheader(f'API response:')
            st.text(f'API response code: {response_status_code} \n\nAPI response header: {response_disposition}')
            print(f'API code: {response_status_code}. With header: {response_disposition}')
            # if response_disposition is not None:
            if response_content is not None:
                st.download_button(
                label="Download file, converted via API",
                data=response_content,
                file_name=response_disposition.split("filename=")[1].strip('"')
            )
            else:
                st.write(f'Response content from API is empty.')
            st.markdown("<hr>", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
