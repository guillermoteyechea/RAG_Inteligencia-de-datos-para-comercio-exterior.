import streamlit as st
from rag import responder

st.set_page_config(page_title="Motor de Inteligencia Comercial", layout="centered")

st.image("Images/amaras.jpeg", use_container_width=True)
st.title("Motor de Inteligencia Comercial para evaluar exportaciones de México a España")

pregunta = st.text_input("Escribe un producto:")

if st.button("Consultar") and pregunta:
    with st.spinner("Procesando consulta..."):
        r = responder(pregunta)

if nombre:
    letra = nombre[0]

    if letra in ["a", "b", "c"]:
        st.image("Images/Palonegro.jpeg", use_container_width=True)

    elif letra in ["d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]:
        st.image("Images/canasta.jpeg", use_container_width=True)

    else:
        st.image("Images/nuez.jpeg", use_container_width=True)
    
    if not r["ok"]:
        st.error(r["mensaje"])
    else:
        st.success("Consulta procesada correctamente, si luego desea buscar otro producto, simplemente vuelva al buscador")

        st.subheader("🔎 Interpretación")
        st.write(f"**Original:** {r['consulta_original']}")
        st.write(f"**Interpretada:** {r['consulta_interpretada']}")

        st.subheader("📦 Fracción seleccionada")
        st.write(r["fraccion_seleccionada"])

        st.subheader("📊 Exportaciones")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Norteamérica", f"${r['valor_norte_america']:,.0f}")

        with col2:
            st.metric("España", f"${r['valor_espana']:,.0f}")

        # =========================
        # 🔥 BLOQUE CORREGIDO
        # =========================
        st.subheader("📈 Potencial")

        m = r["metricas"]
        crecimiento = float(m["crecimiento_estimado"])

        st.metric("Índice actual", f"{m['indice_actual']:.2f}")
        st.metric("Índice oportunidad", f"{m['indice_oportunidad']:.2f}")
        st.metric("Valor potencial", f"${m['valor_potencial']:,.0f}")

        if abs(crecimiento) < 1e-6:
            st.metric("Crecimiento estimado", "$0")
            st.info("No contamos con datos suficientes para poder estimar un valor que le pueda ser de utilidad.")
        elif crecimiento < 0:
            st.metric("Crecimiento estimado", f"${crecimiento:,.0f}")
            st.info("El producto presenta una penetración relevante en España, lo que sugiere un mercado ya bien aceptado y con un nivel de madurez considerable.")
        else:
            st.metric("Crecimiento estimado", f"${crecimiento:,.0f}")
            st.success("Se observa una oportunidad de crecimiento estimado en el mercado español.")

        st.subheader("📑 Resultados encontrados")

        for item in r["resultados"]:
            with st.container():
                st.markdown(f"""
                **Fracción:** {item['fraccion']}  
                **Uso:** {item['uso']}  
                **Impuesto:** {item['impuesto_importacion']}  
                **Score:** {item['score']:.3f}
                """)
                st.divider()
