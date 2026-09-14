"""
Streamlit Web-App: Q&A Chatbot für die Feldpost von Kurt Siegeler (1944–1947)

Voraussetzungen (in requirements.txt):
    streamlit
    google-genai

Ausführung:
    export GEMINI_API_KEY="DEIN_API_KEY"
    streamlit run streamlit_app.py
"""

import os
import streamlit as st
from google import genai
from google.genai import types

# ------------------------------------------------------------------------------
# 1. Konfiguration & Seite einrichten
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Feldpost Kurt Siegeler – Chatbot",
    page_icon="✉️",
    layout="wide"
)

st.title("✉️ Feldpost von Kurt Siegeler (1944–1947)")
st.caption("Ein interaktiver KI-Chatbot zur Erkundung der historischen Feldpostbriefe und Gefangenenkorrespondenz.")

# ------------------------------------------------------------------------------
# 2. Seitenleiste: Einstellungen & Hintergrund
# ------------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Einstellungen")
    
    # API Key Eingabe
    api_key_input = st.text_input(
        "Google Gemini API Key",
        type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Gib hier deinen Gemini API Key ein oder hinterlege ihn in Streamlit Cloud unter Secrets."
    )
    
    # Modell-Auswahl (Aktuelle Google Gemini Modelle)
    model_choice = st.selectbox(
        "Gemini Modell",
        options=["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-pro"],
        index=0,
        help="Empfohlen: gemini-2.5-flash für schnelle und präzise Antworten."
    )
    
    st.divider()
    st.markdown("""
    ### Über die Sammlung
    Diese Sammlung umfasst über 40 Feldpostbriefe, Karten und Dokumente von **Kurt Siegeler** (1944–1947):
    - **Frankreich & Lazarett (1944)**: Dienst, Lazarettaufenthalte (Fontainebleau, Privas) und Normandiefront.
    - **US-Kriegsgefangenschaft (1944–1945)**: Lager Rupert (Idaho) und Ogden (Utah).
    - **Britische Kriegsgefangenschaft (1946)**: Lager Wolterton Park (Norwich) und Wisbech (Camp 90).
    """)

# ------------------------------------------------------------------------------
# 3. System-Prompt & Kontext
# ------------------------------------------------------------------------------
SYSTEM_INSTRUCTION = """
Du bist ein historischer Dokumenten-Assistent für die Briefsammlung "Feldpost von Kurt Siegeler" (1944–1947).
Deine Aufgabe ist es, Fragen von Nutzerinnen und Nutzern präzise, sachlich und quellentreu zu beantworten.

Verhaltensregeln:
1. Beantworte Fragen auf Basis des historischen Kontextes der Briefe von Kurt Siegeler, seiner Frau Elisabeth und Verwandten.
2. Nenne nach Möglichkeit konkrete Daten, Absendeorte (z.B. Lazarett Privas, POW Camp Ogden, Wisbech) und Empfänger.
3. Spekuliere nicht und erfinde keine Tatsachen, die nicht in den Dokumenten belegt sind.
4. Antworte in verständlichem, respektvollem Deutsch.
"""

# ------------------------------------------------------------------------------
# 4. Chat-Historie initialisieren
# ------------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hallo! Ich bin dein digitaler Lese-Assistent für die Feldpost von Kurt Siegeler. Was möchtest du über seine Dienstzeit in Frankreich, seine Kriegsgefangenschaft in den USA und England oder seine Briefe an die Familie erfahren?"
        }
    ]

# ------------------------------------------------------------------------------
# 5. Bisherigen Chat-Verlauf anzeigen
# ------------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------------------------------------------------------------------
# 6. Benutzereingabe & API-Aufruf
# ------------------------------------------------------------------------------
user_prompt = st.chat_input("Stelle eine Frage zu den Briefen (z. B. 'Was schrieb Kurt aus Ogden, Utah?')...")

if user_prompt:
    api_key = api_key_input or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("Bitte gib einen gültigen Gemini API Key in der Seitenleiste ein oder hinterlege GEMINI_API_KEY in den Streamlit Secrets.")
        st.stop()

    # Benutzernachricht anzeigen & speichern
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Gemini Client initialisieren & Antwort generieren
    client = genai.Client(api_key=api_key)

    with st.chat_message("assistant"):
        with st.spinner("Durchsuche Korrespondenz..."):
            try:
                contents = []
                for m in st.session_state.messages[1:]:  # Begrüßung überspringen
                    role = "user" if m["role"] == "user" else "model"
                    contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))

                response = client.models.generate_content(
                    model=model_choice,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.2,
                    )
                )

                reply_text = response.text
                st.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})

            except Exception as e:
                st.error(f"Fehler bei der API-Anfrage an das Modell '{model_choice}': {e}")
                st.info("Tipp: Wähle in der Seitenleiste 'gemini-2.5-flash' als Modell aus.")
