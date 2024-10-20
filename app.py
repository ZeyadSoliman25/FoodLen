%%writefile app.py
import Dataset
import Models
import streamlit as st


def NoodlesPredict(image):
    kaludipredict = Models.KaludiPredications(image)
    naterawpredict = Models.NaterawPredications(image)

    if kaludipredict == "Vegetable" or kaludipredict == "Fruit":
        fruvegpredict = Models.FruVegPredictions(image)
        return fruvegpredict
    elif naterawpredict == "fried_rice":
        return kaludipredict
    else:
        return naterawpredict


# Sidebar
st.sidebar.title("Dashboard")
AppMode = st.sidebar.selectbox("Select Page", ["Home", "About Project", "Predictions"])

# Main Page
if AppMode == "Home":
    st.header("Welcome to FoodLen Food Recognition")
    BackgroundImage = "/content/drive/MyDrive/Rowad_Misr_Project_Assets/background.png"
    st.image(BackgroundImage)

elif AppMode == "About Project":
    st.header("About Project")
    st.text("We offer FoodLen app to make food predictions and estimate the calories and nutrients in the given"
            "meal, vegetable or fruit ")
    st.text("FoodLen app was built on three different machine learning models which are: ")
    st.text("1) Kaludi/food-category-classification-v2.0, check on hugging face: ")
    st.markdown("https://huggingface.co/Kaludi/food-category-classification-v2.0")
    st.text("2) nateraw/food, check on hugging face:")
    st.markdown("https://huggingface.co/nateraw/food ")
    st.text("3) Our own model, you can download it from this drive link: ")
    st.markdown("https://drive.google.com/file/d/1GQ4cjaYVD07jYZuotO346fdl-b_tP8K1/view?usp=sharing")
    st.text(" ")
    st.text("In addition to the mentioned models, the datasets used for training and evaluating are: ")
    st.text("Fruits and Vegetables Image Recognition Dataset: ")
    st.markdown("https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition")
    st.text("USDA Nutritional Facts Database: ")
    st.markdown("https://data.world/awram/food-nutritional-values")


elif AppMode == "Predictions":
    st.header("FoodLen Predict")
    image_ = st.file_uploader("Choose an image: ")

    if image_:
        if 'prediction' not in st.session_state:
            st.session_state.prediction = None

        # Assuming NoodlesPredict is a function that returns a prediction based on the image
        st.session_state.prediction = NoodlesPredict(image_)

    # Show image button
    if st.button("Show image") and image_:
        st.image(image_, width=4, use_column_width=True)

    # Predict button
    if st.button("Predict") and st.session_state.get("prediction"):
        st.write("FoodLen predict it is: ", st.session_state.prediction)

    if st.button("Get Recipes"):

        if 'recipes' not in st.session_state:
            st.session_state.recipes = None

        st.session_state.recipes = Dataset.ReturnAllPossibleEntries(st.session_state.prediction)

        st.write("Recipes fetched, you can now search the wanted recipe and get the nutrients")

    if "recipes" in st.session_state and st.session_state.recipes:
        # Show the select-box with the filtered choices
        selected_choice = st.selectbox("Select an option", st.session_state.recipes)

        if st.button("Get Nutrients"):
            st.session_state.selected_choice = selected_choice

    if st.button("Get") and "selected_choice" in st.session_state:
        nutrients = Dataset.SearchDataset(st.session_state.selected_choice)
        st.session_state.nutrients = nutrients

    if "nutrients" in st.session_state:
        st.write("Selected recipe: ", st.session_state.selected_choice)
        st.write("Nutrients per ", st.session_state.nutrients[4])
        st.write("Amount of water in milli-grams: ", st.session_state.nutrients[0])
        st.write("Amount of calories in KCAL: ", st.session_state.nutrients[1])
        st.write("Amount of protein in milli-grams", st.session_state.nutrients[2])
        st.write("Amount of carbohydrates in milli-grams", st.session_state.nutrients[3])
