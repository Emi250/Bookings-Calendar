import streamlit as st
from datetime import datetime

st.title("Generador de texto para reservas")

st.markdown("Introduce los datos de cada reserva y copia el resultado al final.")

if "reservas" not in st.session_state:
    st.session_state.reservas = []

with st.form("form_reserva"):
    col1, col2 = st.columns(2)
    with col1:
        fecha_entrada = st.date_input("Fecha de entrada", format="DD/MM/YYYY")
    with col2:
        fecha_salida = st.date_input("Fecha de salida", format="DD/MM/YYYY")

    nombre = st.text_input("Nombre del huésped").strip().upper()
    cantidad_personas = st.number_input("Cantidad de personas", min_value=1, step=1)

    submit = st.form_submit_button("Agregar reserva")

    if submit:
        if fecha_entrada >= fecha_salida:
            st.error("La fecha de salida debe ser posterior a la fecha de entrada.")
        elif not nombre:
            st.error("El nombre del huésped no puede estar vacío.")
        else:
            noches = (fecha_salida - fecha_entrada).days
            reserva = {
                "entrada": fecha_entrada,
                "salida": fecha_salida,
                "nombre": nombre,
                "personas": cantidad_personas,
                "noches": noches
            }
            st.session_state.reservas.append(reserva)
            st.success("Reserva agregada.")

st.markdown("---")

if st.session_state.reservas:
    st.header("Texto generado")
    resultado = ""
    dias_semana = {
        0: "LUNES", 1: "MARTES", 2: "MIÉRCOLES", 3: "JUEVES",
        4: "VIERNES", 5: "SÁBADO", 6: "DOMINGO"
    }
    meses = {
        1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
        5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
        9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
    }

    for r in st.session_state.reservas:
        entrada = r["entrada"]
        salida = r["salida"]
        resultado += (
            f"Llegada **{dias_semana[entrada.weekday()]} {entrada.day} DE {meses[entrada.month]}** "
            f"y salida **{dias_semana[salida.weekday()]} {salida.day} DE {meses[salida.month]}** "
            f"({r['nombre']} - {r['personas']} PERSONAS - {r['noches']} NOCHES)\n\n"
        )

    st.text_area("Resultado:", value=resultado.strip(), height=300)

    if st.button("Limpiar reservas"):
        st.session_state.reservas = []

---

