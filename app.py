import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def train_model():
    data = pd.DataFrame({
        'uim_status': [0,1,1,0],
        'osm_status': [1,1,0,0],
        'brm_status': [0,1,1,0],
        'delay_type': ['None','SIM Delay','BRM Hold','None']
    })
    data['label'] = data['delay_type'].astype('category').cat.codes
    model = RandomForestClassifier()
    model.fit(data[['uim_status','osm_status','brm_status']], data['label'])
    label_map = dict(enumerate(data['delay_type'].astype('category').cat.categories))
    return model, label_map

model, label_map = train_model()

st.title("📦 Oracle Order Delay Predictor")
uim = st.selectbox("UIM Provisioning Status", ['Not Started', 'In Progress'])
osm = st.selectbox("OSM Order Status", ['In Progress', 'Completed'])
brm = st.selectbox("BRM Billing Status", ['Pending', 'Posted'])

uim_bin = 1 if uim == 'In Progress' else 0
osm_bin = 1 if osm == 'Completed' else 0
brm_bin = 1 if brm == 'Posted' else 0

if st.button("Predict Delay Reason"):
    pred = model.predict([[uim_bin, osm_bin, brm_bin]])[0]
    st.success(f"📊 Likely Delay Status: {label_map[pred]}")
