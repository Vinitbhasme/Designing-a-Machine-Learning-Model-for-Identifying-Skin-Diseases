from flask import Flask, request, render_template
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import os
import base64
from io import BytesIO

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)

# Load the model
model = load_model("skin_disease_model.h5")

# 9 class labels 
class_names = ["Cellulitis", "Impetigo", "Athelete-Foot", "Nail-Fungus", "Ringworm",
               "Cutaneous-larva-migrans", "Chickenpox", "Shingles", "Unknown"]

# Skin disease info
disease_data = {
    "Cellulitis": {
        "description": "A bacterial skin infection causing redness, swelling, and pain.",
        "medicines": ["Cephalexin", "Dicloxacillin", "Clindamycin"],
        "tips": ["Keep the infected area clean", "Elevate the affected limb", "Take full course of antibiotics"],
        "home_treatments": ["Warm compress on affected area", "Hydration", "Rest"],
        "diagnosis_tests": ["Physical examination", "Wound culture", "Blood tests (CBC)"]
    },
    "Impetigo": {
        "description": "Contagious infection forming sores around nose and mouth.",
        "medicines": ["Mupirocin", "Retapamulin", "Cephalexin"],
        "tips": ["Avoid touching sores", "Keep area clean and dry", "Wash hands frequently"],
        "home_treatments": ["Warm soaks to remove crusts", "Use prescribed antibiotic cream", "Avoid close contact with others"],
        "diagnosis_tests": ["Physical examination", "Bacterial culture", "Gram stain test"]
    },
    "Athelete-Foot": {
        "description": "Fungal infection starting between the toes.",
        "medicines": ["Clotrimazole", "Terbinafine", "Miconazole"],
        "tips": ["Keep feet dry", "Change socks regularly", "Use antifungal powders"],
        "home_treatments": ["Soak feet in salt water", "Apply antifungal creams", "Use tea tree oil"],
        "diagnosis_tests": ["Skin scraping test", "Fungal culture", "KOH test"]
    },
    "Nail-Fungus": {
        "description": "Starts as a yellow spot under the nail tip.",
        "medicines": ["Terbinafine", "Itraconazole", "Ciclopirox"],
        "tips": ["Trim nails regularly", "Keep feet dry", "Avoid walking barefoot in public areas"],
        "home_treatments": ["Vinegar soaks", "Apply tea tree oil", "Use antifungal nail lacquer"],
        "diagnosis_tests": ["Nail clipping test", "Fungal culture", "KOH preparation"]
    },
    "Ringworm": {
        "description": "Fungal infection with a red circular rash.",
        "medicines": ["Clotrimazole", "Ketoconazole", "Griseofulvin"],
        "tips": ["Avoid sharing personal items", "Keep area dry", "Use antifungal cream regularly"],
        "home_treatments": ["Apply garlic paste", "Use turmeric paste", "Coconut oil application"],
        "diagnosis_tests": ["Skin scraping test", "Wood's lamp examination", "Fungal culture"]
    },
    "Cutaneous-larva-migrans": {
        "description": "Skin disease caused by hookworm larvae.",
        "medicines": ["Albendazole", "Ivermectin"],
        "tips": ["Avoid walking barefoot on sandy soils", "Keep skin covered in endemic areas", "Seek medical attention if rash spreads"],
        "home_treatments": ["Cool compress for itching", "Topical anti-itch creams", "Oral antihistamines"],
        "diagnosis_tests": ["Clinical observation", "Skin biopsy", "Travel and exposure history"]
    },
    "Chickenpox": {
        "description": "Viral infection causing itchy, blister-like rash.",
        "medicines": ["Calamine lotion", "Acyclovir", "Antihistamines"],
        "tips": ["Avoid scratching the rash", "Keep fingernails trimmed", "Rest and hydrate well"],
        "home_treatments": ["Cool baths with baking soda", "Apply calamine lotion", "Use antihistamines for itch relief"],
        "diagnosis_tests": ["Physical examination", "Polymerase Chain Reaction (PCR)", "Blood test for varicella antibodies"]
    },
    "Shingles": {
        "description": "Painful rash from reactivated chickenpox virus.",
        "medicines": ["Acyclovir", "Valacyclovir", "Pain relievers"],
        "tips": ["Avoid contact with pregnant women and infants", "Keep rash covered", "Take antivirals early"],
        "home_treatments": ["Cool compresses", "Oatmeal baths", "Topical lidocaine"],
        "diagnosis_tests": ["Physical examination", "PCR for varicella-zoster virus", "Tzanck smear"]
    }
}


def preprocess_image(img, target_size=(224, 224)):
    img = img.resize(target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array

def encode_image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            image = Image.open(file.stream).convert("RGB")
            processed_img = preprocess_image(image)
            prediction = model.predict(processed_img)[0]

            predicted_class = class_names[np.argmax(prediction)]
            encoded_image = encode_image_to_base64(image)

            # Handle Unknown case
            if predicted_class == "Unknown":
                return render_template("index.html",
                                       prediction="This is a Normal Skin image. Please upload a valid one.",
                                       description="N/A",
                                       medicines=[],
                                       image_data=encoded_image)

            # Normal case
            disease_info = disease_data.get(predicted_class, {})
            return render_template("index.html",
                                   prediction=predicted_class,
                                   image_data=encoded_image,
                                   description=disease_info.get("description", "No info"),
                                   medicines=disease_info.get("medicines", []),
                                   tips=disease_info.get("tips", []),
                                   home_treatments=disease_info.get("home_treatments", []),
                                   diagnosis_tests=disease_info.get("diagnosis_tests", []),
                                   )
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
