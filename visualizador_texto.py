import streamlit as st
import requests

st.set_page_config(page_title="Visualizador de Reservas", layout="wide")
st.title("📄 Visualizador de Reservas")

# Puedes elegir entre archivo local o desde GitHub
origen = st.radio("¿De dónde cargar el texto?", ["Archivo local", "Desde GitHub"])

texto = ""

if origen == "Archivo local":
    archivo = st.file_uploader("Sube el archivo con el texto generado (.txt o .md)", type=["txt", "md"])
    if archivo is not None:
        texto = archivo.read().decode("utf-8")

elif origen == "Desde GitHub":
    url = st.text_input("Pega aquí la URL cruda (raw) del archivo en GitHub")
    if url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            texto = response.text
        except Exception as e:
            st.error(f"No se pudo cargar el archivo: {e}")

# Mostrar el contenido limpio
if texto:
    st.subheader("📋 Texto de reservas")
    st.markdown(texto)
    editar = st.checkbox("Editar texto")
    if editar:
        texto_editado = st.text_area("Edita el texto aquí:", value=texto, height=300)
        if st.button("Guardar cambios (temporal)"):
            st.session_state.texto_editado = texto_editado
            st.success("Texto editado y guardado temporalmente.")
else:
    st.info("Sube un archivo o carga una URL para visualizar las reservas.")
