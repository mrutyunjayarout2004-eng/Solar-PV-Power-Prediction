
import streamlit as st
import pandas as pd
import joblib

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Solar PV | Power Prediction",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- PROFESSIONAL STYLING ----------------
st.markdown("""
<style>
    .stApp {
        background-color: #F4F7FC;
        color: #172B4D;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #102A43 !important;
    }

    .hero {
        background: linear-gradient(120deg, #102A43, #174A70);
        padding: 30px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
        border-bottom: 5px solid #E7B64B;
    }

    .hero h1 {
        color: white !important;
        margin-bottom: 8px;
    }

    .hero p {
        color: #E5EDF6;
        font-size: 16px;
        margin-bottom: 0;
    }

    .section-card {
        background: white;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #E1E8F0;
        margin-bottom: 16px;
    }

    .result-card {
        background: #102A43;
        padding: 28px;
        border-radius: 16px;
        border-left: 6px solid #E7B64B;
        color: white;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .result-label {
        color: #E5EDF6;
        font-size: 16px;
    }

    .result-number {
        color: #F4CB67;
        font-size: 38px;
        font-weight: 750;
        margin-top: 8px;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background-color: #D9A62E;
        color: #102A43;
        border: none;
        border-radius: 9px;
        font-weight: 700;
        padding: 10px 22px;
        min-height: 45px;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background-color: #EDC65E;
        color: #102A43;
        border: none;
    }

    [data-testid="stMetric"] {
        background: white;
        padding: 16px;
        border: 1px solid #E1E8F0;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #52657A;
    }

    hr {
        border-color: #DCE4EE;
    }

    .footer {
        text-align: center;
        color: #65758B;
        font-size: 13px;
        padding-top: 20px;
    }
/* Improve input label readability */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #102A43 !important;
    font-weight: 600 !important;
}

/* Improve slider label and value readability */
[data-testid="stSlider"] label,
[data-testid="stNumberInput"] label {
    color: #102A43 !important;
}

/* Keep the overall dashboard light */
[data-testid="stAppViewContainer"] {
    background-color: #F4F7FC;
}

/* Make input summary values readable */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #102A43 !important;
    font-weight: 700 !important;
}

/* Improve metric labels */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #486581 !important;
}

/* Make success message text readable */
[data-testid="stAlert"] p {
    color: #14532D !important;
}


</style>
""", unsafe_allow_html=True)

# ---------------- LOAD SAVED MODEL ----------------
@st.cache_resource
def load_model():
    model = joblib.load("solar_pv_power_prediction_model.pkl")
    features = joblib.load("solar_pv_feature_names.pkl")
    return model, features

try:
    model, features = load_model()
except Exception as e:
    st.error(
        "Unable to load the saved model. Make sure both .pkl files "
        "are in the same folder as app.py."
    )
    st.stop()

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>☀️ Solar PV Power Prediction</h1>
    <p>
        Machine-learning-based estimation of solar photovoltaic
        power using environmental conditions.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- INTRODUCTION ----------------
st.markdown("## Prediction Dashboard")
st.write(
    "Enter the environmental conditions below to estimate "
    "the expected solar PV power output."
)

# ---------------- INPUT SECTION ----------------
st.markdown("### 🌦️ Environmental Parameters")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=-10.0,
            max_value=45.0,
            value=25.0,
            step=0.5,
            help="Ambient air temperature."
        )

        humidity = st.slider(
            "Relative Humidity (%)",
            min_value=0,
            max_value=100,
            value=50,
            help="Percentage of moisture in the air."
        )

    with col2:
        irradiance = st.number_input(
            "Solar Irradiance (W/m²)",
            min_value=0.0,
            max_value=1200.0,
            value=700.0,
            step=10.0,
            help="Solar radiation received per square metre."
        )

        wind_speed = st.number_input(
            "Wind Speed (m/s)",
            min_value=0.0,
            max_value=40.0,
            value=3.5,
            step=0.5,
            help="Wind speed near the ground."
        )

    submitted = st.form_submit_button(
        "☀️ Predict Solar PV Power",
        use_container_width=True
    )

# ---------------- PREDICTION ----------------
if submitted:
    input_values = {
        "temperature": temperature,
        "humidity": humidity,
        "irradiance": irradiance,
        "wind_speed": wind_speed
    }

    input_data = pd.DataFrame([input_values])[features]
    prediction = float(model.predict(input_data)[0])

    st.markdown("### Prediction Result")

    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">Estimated Solar PV Power Output</div>
        <div class="result-number">{prediction:,.2f} kW</div>
    </div>
    """, unsafe_allow_html=True)

    st.success("Prediction completed successfully.")

    # Show the entered environmental conditions
    st.markdown("### Input Summary")

    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

    summary_col1.metric("Temperature", f"{temperature:.1f} °C")
    summary_col2.metric("Humidity", f"{humidity}%")
    summary_col3.metric("Irradiance", f"{irradiance:.0f} W/m²")
    summary_col4.metric("Wind Speed", f"{wind_speed:.1f} m/s")

    st.caption(
        "This value is a machine-learning estimate, not a guaranteed "
        "power output. Prediction reliability depends on the training "
        "data and the conditions represented in it."
    )

# ---------------- FEATURE IMPORTANCE ----------------
st.divider()
st.markdown("## 📊 What Influences the Prediction?")

if hasattr(model, "feature_importances_"):
    importance_df = pd.DataFrame({
        "Environmental Parameter": features,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=True)

    st.write(
        "The chart shows how the trained Random Forest model uses "
        "each input feature. Higher importance means greater influence "
        "on the model's prediction, not proof of causation."
    )

    
    import plotly.express as px

    fig = px.bar(
        importance_df,
        x="Importance",
        y="Environmental Parameter",
        orientation="h",
        title="Which Factors Influence Solar Power?",
        text="Importance",
        color="Importance",
        color_continuous_scale=["#D9A62E", "#102A43"]
    )

    fig.update_traces(
        texttemplate="%{text:.1%}",
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#F4F7FC",
        plot_bgcolor="#F4F7FC",
        font=dict(
            family="Arial",
            color="#12304A",
            size=14
        ),
        title=dict(
            text="Which Factors Influence Solar Power?",
            font=dict(color="#12304A", size=22)
        ),
        xaxis=dict(
            title="Relative Importance",
            title_font=dict(color="#12304A", size=14),
            tickfont=dict(color="#526579", size=12),
            showgrid=True,
            gridcolor="#DCE4EE"
        ),
        yaxis=dict(
            title="Environmental Parameter",
            title_font=dict(color="#12304A", size=14),
            tickfont=dict(color="#12304A", size=13)
        ),
        coloraxis_showscale=False,
        margin=dict(l=20, r=60, t=70, b=30),
        height=350
    )

    fig.update_xaxes(showgrid=True, gridcolor="#DCE4EE")
    fig.update_yaxes(title="", categoryorder="total ascending")

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Feature importance is not available for this model.")

# ---------------- PROJECT INFORMATION ----------------
st.divider()
st.markdown("## About This Project")

info1, info2, info3 = st.columns(3)

with info1:
    st.markdown("**Model**")
    st.write("Tuned Random Forest Regressor")

with info2:
    st.markdown("**Input Parameters**")
    st.write("Temperature, humidity, irradiance and wind speed")

with info3:
    st.markdown("**Purpose**")
    st.write("Estimate solar PV power from environmental data")

st.markdown("""
<div class="footer">
    Solar PV Power Prediction Project | Machine Learning
</div>
""", unsafe_allow_html=True)
