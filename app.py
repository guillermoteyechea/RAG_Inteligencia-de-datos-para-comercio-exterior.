import streamlit as st
from rag import responder

IMAGENES_POR_CODIGO = {
    "0701": "Images/papa.jpeg",
    "0702": "Images/tomate.jpeg",
    "0703": "Images/ajo.jpeg",
    "0704": "Images/canasta.jpeg",
    "0705": "Images/canasta.jpeg",
    "0706": "Images/zanahoria.jpeg",
    "0707": "Images/canasta.jpeg",
    "0708": "Images/canasta.jpeg",
    "0709": "Images/canasta.jpeg",
    "0710": "Images/zanahoria.jpeg",
    "0711": "Images/zanahoria.jpeg",
    "0712": "Images/limon.jpeg",
    "0713": "Images/limon.jpeg",
    "0714": "Images/limon.jpeg",

    "0801": "Images/nuez.jpeg",
    "0802": "Images/nuez.jpeg",
    "0803": "Images/mandarina.jpeg",
    "0804": "Images/mandarina.jpeg",
    "0805": "Images/limon.jpeg",
    "0806": "Images/papaya.jpeg",
    "0807": "Images/papaya.jpeg",
    "0808": "Images/papaya.jpeg",
    "0809": "Images/papaya.jpeg",
    "0810": "Images/papaya.jpeg",
    "0811": "Images/papaya.jpeg",
    "0812": "Images/papaya.jpeg",
    "0813": "Images/papaya.jpeg",
    "0814": "Images/papaya.jpeg",

    "2201": "Images/Palonegro.jpeg",
    "2202": "Images/amaras.jpeg",
    "2203": "Images/dolores.jpeg",
    "2204": "Images/novia.jpeg",
    "2205": "Images/amaras.jpeg",
    "2206": "Images/dolores.jpeg",
    "2207": "Images/novia.jpeg",

    "220820": "Images/amaras.jpeg",
    "220830": "Images/dolores.jpeg",
    "220840": "Images/novia.jpeg",
    "220850": "Images/amaras.jpeg",
    "220860": "Images/dolores.jpeg",
    "220870": "Images/novia.jpeg",
    "2208900301": "Images/amaras.jpeg",
    "2208900391": "Images/dolores.jpeg",
    "2208900400": "Images/novia.jpeg",
    "2208900500": "Images/amaras.jpeg",
}

def obtener_imagen_por_fraccion(fraccion: str) -> str:
    codigo = str(fraccion).split()[0].replace("-", "").strip()

    # Busca primero coincidencias largas, luego cortas
    for largo in [10, 6, 4]:
        clave = codigo[:largo]
        if clave in IMAGENES_POR_CODIGO:
            return IMAGENES_POR_CODIGO[clave]

    return "Images/canasta.jpeg"


st.set_page_config(page_title="Motor de Inteligencia Comercial", layout="centered")

st.title("Motor de Inteligencia Comercial")
st.image("Images/ramo.jpeg", width="stretch")
st.title("Enfoque para evaluar exportaciones de México a España con Norteamerica como referencia")

with st.expander("ℹ️ ¿Cómo interpretar las métricas?"):
    st.markdown("""
    **Norteamérica:** valor exportado del producto de México hacia la región de Norteamérica, de acuerdo con la base de exportaciones utilizada.

    **España:** valor exportado del producto de México hacia España.

    **Índice actual:** compara el nivel relativo de penetración del producto en España frente a Norteamérica. Tomando como referencia el valor del volumen exportado y la población mexicana en el país.  
    - Si es menor a 1, España muestra menor penetración relativa.  
    - Si es cercano a 1, ambos mercados presentan niveles similares.  
    - Si es mayor a 1, España presenta una penetración relativamente alta.

    **Índice oportunidad:** estima el margen potencial de crecimiento.  
    - Valores positivos sugieren oportunidad de crecimiento.  
    - Valores cercanos a cero indican poca diferencia relativa.  
    - Valores negativos sugieren que el producto ya tiene alta penetración en España, incluso mayor que Norteamérica.

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


    if not r["ok"]:
        st.error(r["mensaje"])
    else:
        st.success("Consulta procesada correctamente. Si desea buscar otro producto, simplemente vuelva al buscador.")
        imagen = obtener_imagen_por_fraccion(r["fraccion_seleccionada"])
        st.image(imagen, width="stretch")
        st.subheader("🔎 Interpretación")
        st.write(f"**Original:** {r['consulta_original']}")
        st.write(f"**Interpretada:** {r['consulta_interpretada']}")

        st.subheader("📦 Fracción seleccionada")
        st.write(r["fraccion_seleccionada"])

        st.subheader("📊 Exportaciones")
        
        m = r["metricas"]
        col1, col2 = st.columns(2)

        with col1:
           st.metric("Valor exportado a Norteamérica", f"${r['valor_norte_america']:,.0f}")
           st.metric("Población de referencia Norteamérica", f"{109_300_000:,.0f}")
           st.metric("Gasto por persona Norteamérica", f"${m['gasto_norte_america']:,.2f}")

       with col2:
          st.metric("Valor exportado a España", f"${r['valor_espana']:,.0f}")
          st.metric("Población de referencia España", f"{47_500_000:,.0f}")
          st.metric("Gasto por persona España", f"${m['gasto_espana']:,.2f}")

        st.subheader("📈 Potencial")

   
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
