import pandas as pd
import streamlit as st
import pickle
from io import StringIO

def generate_detailed_report(model, text):
    text = text.decode('utf-8')
    df = pd.read_csv(StringIO(text), delim_whitespace=True)
    prediction = model.predict(df)[0]
    valence, arousal = prediction[0], prediction[1]
    report = f"\nPrediction:\nValence: {valence}\nArousal: {arousal}\n"

    if valence < 5 and arousal > 5:
        report += "Stress: Yes\n"
        if 0 <= valence <= 2 and 7 <= arousal <= 9:
            report += "   - Severity: Severe Stress\n"
            report += "   - Description: The individual is likely experiencing intense and severe stress.\n"
            background_color = 'red'
        elif 2 < valence <= 4 and 6 <= arousal <= 7:
            report += "   - Severity: Moderate Stress\n"
            report += "   - Description: The individual is likely experiencing moderate levels of stress.\n"
            background_color = 'orange'
        elif 4 < valence <= 5 and 5 <= arousal <= 6:
            report += "   - Severity: Light Stress\n"
            report += "   - Description: The individual is likely experiencing mild or light stress.\n"
            background_color = 'yellow'
        else:
            report += "   - Severity: Normal Stress\n"
            report += "   - Description: The individual is likely experiencing normal levels of stress.\n"
            background_color = 'green'
    else:
        report += "Stress: No\n"
        report += "   - Description: The individual is not showing signs of stress.\n"
        background_color = 'green'

    return report, background_color



def main():

    st.title("Mental Stress Prediction App")
    model = pickle.load(open("knn_model.pkl", "rb"))
    # File upload widget
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    if uploaded_file is not None:
        # Read and display the contents of the uploaded file
        text_contents = uploaded_file.read()
        if st.button("Predict stress State"):
            predictions, background_color = generate_detailed_report(model, text_contents)
            st.text(f"\Predictions:")
            st.text(predictions)

if __name__ == "__main__":
    main()
