import streamlit as st
from rag import responder

st.set_page_config(page_title="Motor de Inteligencia Comercial", layout="centered")

st.image("Images/ramo.jpeg", width="stretch")
st.title("Motor de Inteligencia Comercial para evaluar exportaciones de México a España")

with st.expander("ℹ️ ¿Cómo interpretar las métricas?"):
    st.markdown("""
    **Norteamérica:** valor exportado del producto hacia la región de Norteamérica, de acuerdo con la base de exportaciones utilizada.

    **España:** valor exportado del producto hacia España.

    **Índice actual:** compara el nivel relativo de penetración del producto en España frente a Norteamérica.  
    - Si es menor a 1, España muestra menor penetración relativa.  
    - Si es cercano a 1, ambos mercados presentan niveles similares.  
    - Si es mayor a 1, España presenta una penetración relativamente alta.

    **Índice oportunidad:** estima el margen potencial de crecimiento.  
    - Valores positivos sugieren oportunidad de crecimiento.  
    - Valores cercanos a cero indican poca diferencia relativa.  
    - Valores negativos sugieren que el producto ya tiene alta penetración en España.

    **Valor potencial:** estimación del tamaño que podría alcanzar el mercado español si tuviera un comportamiento similar al mercado de referencia.

    **Crecimiento estimado:** diferencia entre el valor potencial calculado y el valor actual exportado a España.
    """)

with st.expander("📚 Fuentes de datos"):
    st.markdown("""
    **Exportaciones:** Banco de México. Cubo de comercio exterior: Valor de exportaciones por producto y región.  
    https://www.banxico.org.mx/CuboComercioExterior/ValorDolares/matrizprodregion

    **Información arancelaria:** Unión Europea. (2013). Reglamento (UE) n.º 952/2013 del Parlamento Europeo y del Consejo, por el que se establece el Código Aduanero de la Unión.  
    https://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2013:290:0001:0901:ES:PDF

    **Población:** Instituto de Mexicanas y Mexicanos en el Exterior. (2024). Población mexicana en el exterior. Gobierno de México.  
    https://www.datos.gob.mx/dataset/poblacion_mexicana_exterior
    """)

pregunta = st.text_input("Escribe un producto:")

if st.button("Consultar") and pregunta:
    with st.spinner("Procesando consulta..."):
        r = responder(pregunta)

    nombre = r.get("consulta_interpretada", "").lower()

    if nombre:
        letra = nombre[0]

        if letra in ["a", "b", "c"]:
            st.image("Images/Palonegro.jpeg", width="stretch")
        elif letra in ["d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]:
            st.image("Images/canasta.jpeg", width="stretch")
        else:
            st.image("Images/nuez.jpeg", width="stretch")

    if not r["ok"]:
        st.error(r["mensaje"])
    else:
        st.success("Consulta procesada correctamente. Si desea buscar otro producto, simplemente vuelva al buscador.")

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
