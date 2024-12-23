import requests
import base64
from io import BytesIO
from PIL import Image
import streamlit as st

# Flask API endpoint
def generate(prompt):
    url = "http://43.205.115.114/generate"

    # The prompt for image generation
    data = {
        "prompt": prompt
    }

    # Send the POST request
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the response JSON containing the Base64 encoded image
        response_data = response.json()
        
        if "image" in response_data:
            # The Base64 encoded image
            img_base64 = response_data["image"]
            print("Base64 encoded image:")
            print(img_base64)
            
            # Decode the Base64 image
            img_data = base64.b64decode(img_base64)
            
            # Open the image using PIL
            image = Image.open(BytesIO(img_data))
            return image
            
        else:
            print("Error: No image data found in the response.")
    else:
        print(f"Error {response.status_code}: {response.text}")

# Function to encode the logo image to Base64
def encode_logo_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            # Read the image and encode it in base64
            base64_str = base64.b64encode(image_file.read()).decode()
            return base64_str
    except Exception as e:
        print(f"Error encoding logo: {e}")
        return None

# Display the logo in the top-left corner using custom CSS
st.markdown(
    """
    <style>
    .logo {
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 1000;
        width: 150px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Test the path and encoding of the logo
logo_base64 = encode_logo_to_base64("Zunno logo (1).png")

# Check if the encoding is successful
if logo_base64:
    print("Logo encoded to Base64 successfully.")
    st.markdown(f'<img class="logo" src="data:image/png;base64,{logo_base64}" alt="Logo"/>', unsafe_allow_html=True)
else:
    print("Failed to encode the logo. Please check the image path.")

# Main content
st.write("Create a realistic image of [Brand Name]'s [Product Name] in a stylish, everyday setting. Add text overlay: 'Holiday Sale – 50% Off!' with festive elements like snowflakes or subtle Christmas décor. Natural lighting highlights the product, conveying warmth, quality, and an inviting atmosphere for the season’s best deal.")

# Input prompt from user
if prompt := st.chat_input("Create a realistic image of [Brand Name]'s [Product Name] in a ...."):
    image = generate(prompt=prompt)
    if image:
        st.image(image)
