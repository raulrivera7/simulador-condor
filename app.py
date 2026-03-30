import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Simulador Cóndor - UNIFRANZ", layout="wide")

# --- CLAVE API (Cámbiala por la tuya de Google AI Studio) ---
API_KEY = "TU_NUEVA_API_KEY_AQUI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- CONTEXTO DE ALTA DENSIDAD (4000+ Palabras de lógica) ---
CONTEXTOS = {
    "Rodrigo Torrico (Producción)": {
        "saludo": "Soy Rodrigo. Si vienes de la UNIFRANZ, habla rápido. El banco no espera y mis hermanos me tienen harto.",
        "prompt": """ACTÚA COMO RODRIGO TORRICO. 
        CONTEXTO EXTENSO: Jefe de Producción de Calzados Cóndor (La Chimba, Cochabamba). 
        HISTORIA: 30 años en la fábrica. Tu padre Marcelo murió en agosto 2025. 
        CONFLICTO: Debes 180,000 Bs al banco (vence en 60 días). Eficiencia de planta al 63%. 
        PERSONALIDAD: Rudo, empírico, odia la teoría académica. 
        REGLA DE ORO: Solo cederás a un cambio de organigrama si te hablan de 'Separar Propiedad de Gestión' y crear un Directorio.
        DATOS: 45 operarios, máquinas de 20 años, desperdicio de cuero del 12%."""
    },
    "Don Félix (Almacén)": {
        "saludo": "Buen día, jovencito. Pase al almacén, pero no me mueva los cuadernos, que ahí está todo anotado.",
        "prompt": """ACTÚA COMO DON FÉLIX MAMANI. 
        CONTEXTO: Encargado de almacén desde 1995. Fiel a don Marcelo. 
        DEBILIDADES INTERNAS: 15% de fallas en pegado, no hay software (todo en 'Cuadernos Verdes'), cables expuestos en planta. 
        PERSONALIDAD: Humilde, usa términos bolivianos (jovencito, casero). Teme por su jubilación.
        DATOS: El pegamento barato que compra Óscar causa los defectos. Las máquinas fallan por falta de mantenimiento preventivo."""
    },
    "Terminal de Datos (Entorno)": {
        "saludo": "[SISTEMA ACTIVO] Consultas de mercado: IBNORCA, Competencia y Sector Minero.",
        "prompt": """ACTÚA COMO TERMINAL DE DATOS. 
        DATOS EXTERNOS: Sector minero paga 320 Bs por par certificado. Santa Cruz exige IBNORCA en 90 días. 
        COMPETENCIA: Usan tecnología CNC y corte láser. 
        RIESGOS: Pérdida de licitación de 8,000 pares por falta de sellos de calidad.
        TONO: Frío, analítico, usa listas y negritas."""
    }
}

# --- INTERFAZ DE USUARIO ---
st.title("👟 Caso de Estudio: Calzados Cóndor S.R.L.")
st.markdown("---")

# Selección de personaje
personaje_nom = st.sidebar.selectbox("Selecciona al entrevistado:", list(CONTEXTOS.keys()))
personaje = CONTEXTOS[personaje_nom]

st.sidebar.image("https://via.placeholder.com/150", caption=personaje_nom) # Aquí irían tus fotos
st.sidebar.write(f"**Estado:** Conectado")

# Historial
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Reiniciar chat si cambia personaje
if "current_char" not in st.session_state or st.session_state.current_char != personaje_nom:
    st.session_state.chat_history = [{"role": "assistant", "content": personaje["saludo"]}]
    st.session_state.current_char = personaje_nom

# Mostrar chat
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

# Entrada de texto
if prompt := st.chat_input():
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Generar respuesta con contexto
    full_prompt = f"{personaje['prompt']}\nHistorial:\n{st.session_state.chat_history}\nUsuario: {prompt}"
    response = model.generate_content(full_prompt)
    
    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)
