import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Gestor de Reservas", layout="wide")

# Diccionarios auxiliares
dias_semana = {
    0: "LUNES", 1: "MARTES", 2: "MIÉRCOLES", 3: "JUEVES",
    4: "VIERNES", 5: "SÁBADO", 6: "DOMINGO"
}
meses = {
    1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
    5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
    9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
}

def formatear_reservas(reservas):
    resultado = ""
    for r in reservas:
        entrada = r["entrada"]
        salida = r["salida"]
        noches = (salida - entrada).days
        resultado += (
            f"Llegada **{dias_semana[entrada.weekday()]} {entrada.day} DE {meses[entrada.month]}** "
            f"y salida **{dias_semana[salida.weekday()]} {salida.day} DE {meses[salida.month]}** "
            f"({r['nombre'].upper()} - {r['personas']} PERSONAS - {noches} NOCHES)\n\n"
        )
    return resultado.strip()

# Inicializar reservas
if "reservas" not in st.session_state:
    st.session_state.reservas = []

# Tabs
tab1, tab2 = st.tabs(["➕ Generar texto", "👁️ Visualizar/editar"])

# ----------------- TAB 1 -----------------
with tab1:
    st.header("🛠️ Ingreso de reservas")

    with st.form("formulario"):
        col1, col2 = st.columns(2)
        with col1:
            fecha_entrada = st.date_input("Fecha de entrada")
        with col2:
            fecha_salida = st.date_input("Fecha de salida")

        nombre = st.text_input("Nombre del huésped").strip().upper()
        cantidad = st.number_input("Cantidad de personas", min_value=1, step=1)
        enviar = st.form_submit_button("Agregar")

        if enviar:
            if fecha_entrada >= fecha_salida:
                st.error("La salida debe ser posterior a la entrada.")
            elif not nombre:
                st.error("Debe ingresar el nombre del huésped.")
            else:
                st.session_state.reservas.append({
                    "entrada": fecha_entrada,
                    "salida": fecha_salida,
                    "nombre": nombre,
                    "personas": cantidad
                })
                st.success("Reserva agregada.")

    if st.session_state.reservas:
        st.subheader("📝 Texto generado")
        texto = formatear_reservas(st.session_state.reservas)
        st.text_area("Resultado:", value=texto, height=300)
        st.download_button("📥 Descargar como .txt", data=texto, file_name="reservas.txt")

        if st.button("🧹 Limpiar reservas"):
            st.session_state.reservas = []

# ----------------- TAB 2 -----------------
with tab2:
    st.header("📂 Visualizador de reservas")

    archivo = st.file_uploader("Subí un archivo de reservas (.csv, .json, .xls, .xlsx)", type=["csv", "json", "xls", "xlsx"])

    if archivo:
        nombre = archivo.name.lower()
        try:
            if nombre.endswith(".csv"):
                df = pd.read_csv(archivo)
            elif nombre.endswith(".json"):
                df = pd.read_json(archivo, encoding='utf-8')
            elif nombre.endswith((".xls", ".xlsx")):
                df = pd.read_excel(archivo)
            else:
                st.error("Formato de archivo no soportado.")
                df = None

            if df is not None:
                st.subheader("📊 Datos cargados")
                st.dataframe(df)

                # Convertir a lista de reservas válidas
                reservas_archivo = []
                for _, r in df.iterrows():
                    entrada = pd.to_datetime(r["entrada"])
                    salida = pd.to_datetime(r["salida"])
                    reservas_archivo.append({
                        "entrada": entrada,
                        "salida": salida,
                        "nombre": r["nombre"],
                        "personas": int(r["personas"])
                    })

                # Mostrar texto generado automáticamente
                st.markdown("### 📝 Texto generado")
                texto_archivo = formatear_reservas(reservas_archivo)
                st.text_area("Texto formateado desde el archivo:", value=texto_archivo, height=300)
                st.download_button("📥 Descargar texto", data=texto_archivo, file_name="reservas_generadas.txt")

        except Exception as e:
            st.error(f"No se pudo leer el archivo: {e}")
