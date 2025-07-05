import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Food Product Explorer", layout="wide")

st.title("🍎 Open Food Facts Explorer")
st.write("Search for a food product using its **barcode** to get real-time data.")

# Input for barcode
barcode = st.text_input("Enter product barcode (e.g., 737628064502):")

def fetch_product_data(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        if data.get("status") == 1:
            return data["product"]
    return None

if barcode:
    product = fetch_product_data(barcode)
    
    if product:
        st.success("Product found!")
        
        col1, col2 = st.columns([1, 2])
        
        # Show image
        with col1:
            image_url = product.get("image_url")
            if image_url:
                image = Image.open(BytesIO(requests.get(image_url).content))
                st.image(image, caption=product.get("product_name", "N/A"))
        
        # Show details
        with col2:
            st.subheader(product.get("product_name", "N/A"))
            st.write(f"**Brands:** {product.get('brands', 'N/A')}")
            st.write(f"**Quantity:** {product.get('quantity', 'N/A')}")
            st.write(f"**Nutrition Grade:** {product.get('nutrition_grades', 'N/A')}")
            st.write(f"**Categories:** {product.get('categories', 'N/A')}")
            st.write(f"**Countries Sold:** {product.get('countries', 'N/A')}")
            st.markdown("**Ingredients:**")
            st.code(product.get("ingredients_text", "N/A"), language="markdown")
    else:
        st.error("Product not found or barcode invalid.")
