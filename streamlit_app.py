import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gestor de Reservas", layout="wide")

# Función con * en vez de ** para negrita estilo WhatsApp
def formatear_reservas(reservas):
    dias_semana = {
        0: "LUNES", 1: "MARTES", 2: "MIÉRCOLES", 3: "JUEVES",
        4: "VIERNES", 5: "SÁBADO", 6: "DOMINGO"
    }
    meses = {
        1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
        5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
        9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
    }
    resultado = ""
    for r in reservas:
        entrada = r["entrada"]
        salida = r["salida"]
        noches = (salida - entrada).days
        resultado += (
            f"Llegada *{dias_semana[entrada.weekday()]} {entrada.day} DE {meses[entrada.month]}* "
            f"y salida *{dias_semana[salida.weekday()]} {salida.day} DE {meses[salida.month]}* "
            f"({r['nombre'].upper()} - {r['personas']} PERSONAS - {noches} NOCHES)\n\n"
        )
    return resultado.strip()

if "reservas" not in st.session_state:
    st.session_state.reservas = []

tab1, tab2 = st.tabs(["➕ Ingresar reservas", "📂 Visualizar desde archivo"])

# TAB 1: Ingreso manual
with tab1:
    st.header("➕ Agregar reserva manualmente")

    with st.form("formulario_reserva"):
        col1, col2 = st.columns(2)
        with col1:
            entrada = st.date_input("Fecha de entrada")
        with col2:
            salida = st.date_input("Fecha de salida")

        nombre = st.text_input("Nombre del huésped").strip()
        personas = st.number_input("Cantidad de personas", min_value=1, step=1)

        agregar = st.form_submit_button("Agregar")

        if agregar:
            if entrada >= salida:
                st.error("La fecha de salida debe ser posterior a la de entrada.")
            elif not nombre:
                st.error("Debes ingresar el nombre del huésped.")
            else:
                st.session_state.reservas.append({
                    "entrada": entrada,
                    "salida": salida,
                    "nombre": nombre,
                    "personas": personas
                })
                st.success("Reserva agregada.")

    if st.session_state.reservas:
        st.subheader("📝 Texto generado")
        texto = formatear_reservas(st.session_state.reservas)
        st.text_area("Resultado:", value=texto, height=300)
        st.download_button("📥 Descargar como .txt", data=texto, file_name="reservas.txt")
        st.code("Seleccioná y copiá el texto con Ctrl+C o clic derecho", language="")

        if st.button("🧹 Limpiar reservas"):
            st.session_state.reservas = []

# TAB 2: Desde archivo
with tab2:
    st.header("📂 Visualizador de reservas desde archivo")

    archivo = st.file_uploader("Subí un archivo (.csv, .xls, .xlsx)", type=["csv", "xls", "xlsx"])

    if archivo:
        nombre = archivo.name.lower()
        try:
            if nombre.endswith(".csv"):
                df = pd.read_csv(archivo, sep=";")
            elif nombre.endswith((".xls", ".xlsx")):
                df = pd.read_excel(archivo)
            else:
                st.error("Formato de archivo no soportado.")
                df = None

            if df is not None:
                df.columns = df.columns.str.strip().str.lower()
                df.rename(columns={
                    "nombre del cliente (o clientes)": "nombre",
                    "personas": "personas",
                    "entrada": "entrada",
                    "salida": "salida"
                }, inplace=True)

                columnas_necesarias = {"entrada", "salida", "nombre", "personas"}
                if not columnas_necesarias.issubset(df.columns):
                    st.error(f"Faltan columnas necesarias: {columnas_necesarias - set(df.columns)}")
                else:
                    st.subheader("📊 Datos del archivo")
                    st.dataframe(df[["entrada", "salida", "nombre", "personas"]])

                    reservas = []
                    for _, r in df.iterrows():
                        reservas.append({
                            "entrada": pd.to_datetime(r["entrada"]),
                            "salida": pd.to_datetime(r["salida"]),
                            "nombre": str(r["nombre"]).strip(),
                            "personas": int(r["personas"])
                        })

                    texto = formatear_reservas(reservas)
                    st.markdown("### 📝 Texto generado")
                    st.text_area("Texto formateado desde el archivo:", value=texto, height=300)
                    st.download_button("📥 Descargar como .txt", data=texto, file_name="reservas.txt")
                    st.code("Seleccioná y copiá el texto con Ctrl+C o clic derecho", language="")

        except Exception as e:
            st.error(f"No se pudo procesar el archivo: {e}")
