import os
import requests
import pandas as pd
import streamlit as st
from prometheus_client.parser import text_string_to_metric_families

API_METRICS_URL = os.getenv("API_METRICS_URL", "http://localhost:8000/metrics")

st.set_page_config(page_title="Tech Challenge - Monitoramento", layout="wide")
st.title("📈 Monitoramento & Analytics")

@st.cache_data(ttl=5)
def fetch_metrics_text() -> str:
    r = requests.get(API_METRICS_URL, timeout=5)
    r.raise_for_status()
    return r.text

def parse_metrics(text: str):
    samples = []
    for family in text_string_to_metric_families(text):
        for sample in family.samples:
            # sample: (name, labels, value, timestamp, exemplar)
            name, labels, value = sample.name, sample.labels, sample.value
            samples.append({"name": name, "value": value, **labels})
    return pd.DataFrame(samples)

try:
    raw = fetch_metrics_text()
    df = parse_metrics(raw)

    c1, c2, c3 = st.columns(3)

    # exemplos comuns do instrumentator: ajuste se necessário depois de ver seus nomes reais
    total_requests = df[df["name"].str.contains("http", na=False)].shape[0]
    c1.metric("Séries de métricas (linhas)", str(len(df)))
    c2.metric("Endpoints monitorados (aprox.)", str(df.get("handler", pd.Series()).nunique() if "handler" in df else "-"))
    c3.metric("Fonte", API_METRICS_URL)

    st.divider()

    st.subheader("Tabela de métricas (filtro rápido)")
    name_filter = st.text_input("Filtrar por nome da métrica (contains)", "http")
    view = df[df["name"].str.contains(name_filter, na=False)].copy()
    st.dataframe(view.head(500), use_container_width=True)

except Exception as e:
    st.error(f"Falha ao ler métricas em {API_METRICS_URL}: {e}")
    st.stop()
