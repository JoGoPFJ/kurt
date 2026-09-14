"""
Streamlit Web-App: Q&A Chatbot für die Feldpost von Kurt Siegeler (1944–1947)

Voraussetzungen:
    pip install streamlit google-genai

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
st.caption("Ein interaktiver KI-Chatbot zur Erkundung der historischen Feldpostbriefe und Kriegsgefangenenpost.")

# ------------------------------------------------------------------------------
# 2. Integrierte Brief-Datenbank (Wissensbasis)
# ------------------------------------------------------------------------------
BRIEF_DATENBANK = [
    {
        "datum": "08.01.1944",
        "ort": "Frankreich (O.U.)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth, Hermann & Friedrich Siegeler",
        "kategorie": "Frankreich / Stammkompanie",
        "text": """U. den 8.1.44. Liebe Elisabeth, Hermann, Friedrich und Mama. Ja, ihr Lieben, ich schreibe nun eine Anschrift für Euch alle. Es ist mir nicht möglich, jedem Einzelnen zu schreiben... Der Dienst geht von morgens 6 Uhr bis abends. Verpflegung ist recht knapp. 50 Francs für Verbesserung der Verpflegung. Es ist ein sonderbares Land..."""
    },
    {
        "datum": "15.01.1944",
        "ort": "Frankreich (O.U.)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "kategorie": "Frankreich / Verpflegung",
        "text": """O.U. den 15.1.44. Schon wieder ist eine Woche dahin, ohne dass ich ein Lebenszeichen von Euch erhalten habe... Die Verpflegung ist einfach nicht ausreichend bei dem harten Dienst. Ich habe immer Hunger. Ich bin schlank und mager geworden. Habe im 5. Gürtelloch schnallen müssen. Bitte schicke mir regelmäßig Päckchen..."""
    },
    {
        "datum": "06.02.1944",
        "ort": "Frankreich (O.U.)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "kategorie": "Frankreich / Dienst",
        "text": """O.U. den 6.2.44. Wir fassten um 6 Uhr abends in die Kompanie beladen. Marschschalldämpfer... 40-50 Mann. Französische Offiziere als Banditen zu stellen. Es war also im kriegsmäßigen Dienst..."""
    },
    {
        "datum": "18.03.1944",
        "ort": "Frankreich (O.U.) / La Grimaudiere",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "kategorie": "Frankreich / Heimatbunker",
        "text": """O.U. den 18.3.44. Befehl erhalten, sofort Sachen zu packen und zurück nach La Grimaudiere zu fahren... Wegen Bunker hinter der Scheune: Sollte der Fall eintreten, dass Scheune und Holzschuppen verbrennen, würde es im Bunker zwischen den Gebäuden zu heiß. Besser alten Keller nutzen. Der Luftschutzbund gibt Zuschüsse... Natja und Polen im Auge behalten, Schlüssel nachmachen lassen..."""
    },
    {
        "datum": "12.04.1944",
        "ort": "Frankreich (O.U.)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "kategorie": "Frankreich / Heimatbunker & Landwirtschaft",
        "text": """O.U. den 12.4.44. Deinen Brief vom 21.3.44 erhalten. Wenn ich aus dem Lazarett entlassen werde, muss ich zur Frontleitstelle nach Paris. Bei uns SS-Männern geht es nicht nach Deutschland, sondern wieder zur Truppe. Luftschutzbunker Hesselbach... Zwecks Heuernte Äste am Hochewald radikal beschneiden. Vorschriften für Mist und Stroh..."""
    },
    {
        "datum": "04.05.1944",
        "ort": "Lazarett (Frankreich)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "kategorie": "Frankreich / Lazarett",
        "text": """O.U. den 4.5.1944. Wunden sind gut am Heilen. Einen Siegerländer Kameraden Mühlenbach aus Geisweid im Lazarett getroffen. Er ist Autofahrer bei der Luftwaffe. Verpflegung und Baderaum gut. Känguruzuteilung und Rationierung in der Heimat beachten..."""
    },
    {
        "datum": "12.05.1944",
        "ort": "Lazarett Fontainebleau",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "kategorie": "Frankreich / Lazarett Fontainebleau",
        "text": """Fontainebleau, den 12.5.44. Finger fast zugeheilt, Arm eitert noch etwas. Keine Sorgen machen. Nach Entlassung geht es zur Frontleitstelle Paris. Bunkerbau in Oberschelden/Hesselbach. Ratschläge zur Viehhaltung und Landwirtschaft..."""
    },
    {
        "datum": "15.05.1944",
        "ort": "Lazarett Fontainebleau",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "kategorie": "Frankreich / Evakuierung Lazarett",
        "text": """Fontainebleau, den 15.5.1944. Unerwartet Befehl erhalten, das Lazarett Fontainebleau am 16.5.44 morgens 10 Uhr zu räumen. Fahrt geht vermutlich Richtung Südfrankreich/Schweizer Grenze. Wunden fast zu..."""
    },
    {
        "datum": "17.05.1944",
        "ort": "Lazarett Privas (Rhône)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "kategorie": "Frankreich / Lazarett Privas",
        "text": """Privas, den 17.5.44. Nach 1,5-tägiger Bahnfahrt in Privas angekommen. Wunderschöne Fahrt durch Obstgegend entlang der Rhône (Kirschen, Pfirsiche, Weinreben). Lazarett in ehemaliger französischer Strafanstalt untergebracht mit 3000 Soldaten..."""
    },
    {
        "datum": "20.05.1944",
        "ort": "Lazarett Privas (Rhône)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "kategorie": "Frankreich / Heuernte-Anweisungen",
        "text": """Privas, den 20.5.44. Zum ersten Mal vor dem Arzt in Privas, Verband am Zeigefinger entfernt. Wunde am Unterarm verpflastert. Anweisungen zur Heuernte: Motor mit großer Riemenscheibe für das Heugebläse nutzen. Passendes Holz liegt in der Schrotmühle. 15-Ampere-Sicherungen besorgen..."""
    },
    {
        "datum": "30.05.1944",
        "ort": "Privas / Frontleitstelle Lyon",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "kategorie": "Frankreich / Verlegung Front",
        "text": """Privas, den 30.5.44. Entlassungspapiere erhalten. fahre heute Nachmittag 4 Uhr zur Frontleitstelle Lyon. Von dort Weiterfahrt zur Stammkompanie. Wichtiger Hinwies: Riemen beim Heublesen nachts abnehmen, damit er sich nicht längt..."""
    },
    {
        "datum": "02.06.1944",
        "ort": "Frankreich (Stammkompanie)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "kategorie": "Frankreich / Rückkehr Truppe",
        "text": """O.U. den 2.6.44. Wieder bei der alten Kompanie gelandet. Bekannte Gesichter wiedergesehen. Fahrt ging nachts per Express... 5 Briefe auf einmal erhalten..."""
    },
    {
        "datum": "11.06.1944",
        "ort": "Frankreich (Anmarsch Normandie)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "kategorie": "Frankreich / Invasion Zweite Front",
        "text": """Frankreich, den 11.6.44. Über Nacht ist die zweite Front (Invasion der Alliierten) errichtet worden. Unsere Einheiten sind bestimmt worden, die Engländer bei Le Havre anzugreifen. Anmarsch zu Fuß und per Rad... Gehe gefasst dem Feind entgegen..."""
    },
    {
        "datum": "04.07.1944",
        "ort": "H.K.L. Nord-Normandie",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "kategorie": "Frankreich / Frontsatz Normandie",
        "text": """NW-Normandie, den 4.7.44. Endlich in der H.K.L. (Hauptkampflinie) angelangt. Wir liegen 300-400 Meter den amerikanischen Truppen gegenüber. Schweres Artilleriefeuer, aber wir haben gelernt, uns rechtzeitig in Löchern zu verschanzen. Kompanie bisher ohne Ausfall..."""
    },
    {
        "datum": "01.11.1944",
        "ort": "POW Camp Rupert, Idaho (USA)",
        "absender": "Kurt Siegeler (Obergefr., POW 31G 141439)",
        "empfaenger": "Elisabeth Siegeler & Familie",
        "kategorie": "US-Kriegsgefangenschaft / Idaho",
        "text": """1. November 1944. P.O.W. Camp Rupert, Idaho. Bin gesund. Arbeiten bei der Zuckerrübenernte. Fragen zur Heimat: Viehbestand, Futter, Weide auf dem Speifel, Hilfe durch Manda/Polen. Sehnsucht nach der Familie..."""
    },
    {
        "datum": "02.12.1944",
        "ort": "POW Camp Ogden, Utah (USA)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Familie",
        "kategorie": "US-Kriegsgefangenschaft / Utah",
        "text": """2.12.1944. Camp Ogden, Utah. Arbeite in einem großen Zuckerlagerhaus. Säcke verladen mit Packkarre und Transportband. Wetter gut, Schnee in den Bergen. Gedanken an die Arbeit zu Hause..."""
    },
    {
        "datum": "27.01.1945",
        "ort": "POW Camp Ogden, Utah (USA)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "kategorie": "US-Kriegsgefangenschaft / Utah",
        "text": """27.1.1945. Camp Ogden, Utah. Arbeite in der Küche. Traum von Elisabeth und früheren Zeiten in der Jugend. Bitte um Nachrichten von Verwandten (Alfred, Walter, Henriette)..."""
    },
    {
        "datum": "03.02.1945",
        "ort": "POW Camp Ogden, Utah (USA)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "kategorie": "US-Kriegsgefangenschaft / Utah",
        "text": """3.2.1945. Nun bin ich schon ein halbes Jahr Kriegsgefangener. Zeit ging verhältnismäßig schnell vorbei. Ratschläge für Kohlenbeschaffung in Siegen (Herr Schneider / Fräulein Söhngen). Vorbereitung für Frühjahrsbestellung..."""
    },
    {
        "datum": "30.05.1946",
        "ort": "Camp Wolterton Park / Norwich (UK)",
        "absender": "Kurt Siegeler (Gef. B 707975)",
        "empfaenger": "Elisabeth Siegeler",
        "kategorie": "Britische Gefangenschaft / Norwich",
        "text": """30. Mai 1946. Wolterton Park near Norwich. Am 25.5.46 von Belgien nach England verlegt. Entlassung verzögert sich. Emil Klöckner aus Niederschelden ist im selben Lager..."""
    },
    {
        "datum": "19.06.1946",
        "ort": "Fridaybridge Camp 90, Wisbech (UK)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth, Hermann & Friedrich",
        "kategorie": "Britische Gefangenschaft / Wisbech",
        "text": """19.6.1946. Camp 90 Wisbech, Cambridgeshire. Arbeit beim Ziegelsteine-Verladen. Unterbringung mit 175 Mann in einem großen Haus. Landschaft eben mit vielen Parkanlagen, oft Regen. Glückwunsch zum Geburtstag der Söhne..."""
    },
    {
        "datum": "28.09.1946",
        "ort": "Fridaybridge Camp 90, Wisbech (UK)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth, Hermann & Friedrich",
        "kategorie": "Britische Gefangenschaft / Wisbech",
        "text": """28.9.1946. Umgezogen in ein neues Zeltlager. Wir fahren morgens mit Lastautos zur Arbeit in eine Marmeladenfabrik. Anweisungen zum Verkauf der kleinen roten Kuh..."""
    }
]

# ------------------------------------------------------------------------------
# 3. Seitenleiste: Einstellungen, Modellauswahl & Briefbrowser
# ------------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Einstellungen & Optionen")
    
    # API Key Eingabe
    api_key_input = st.text_input(
        "Google Gemini API Key",
        type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Gib hier deinen Gemini API Key ein. Kostenlos erhältlich auf aistudio.google.com"
    )

    # Modellauswahl zur Vermeidung von Deprecation/404-Fehlern
    selected_model = st.selectbox(
        "Gemini KI-Modell",
        options=["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash"],
        index=0,
        help="Wähle das gewünschte Modell. Bei API-Änderungen kannst du hier leicht umschalten."
    )
    
    st.divider()
    
    # Brief-Browser zum direkten Nachschlagen
    st.header("📜 Brief-Archiv Durchsuchen")
    kategorien = sorted(list(set(b["kategorie"] for b in BRIEF_DATENBANK)))
    kat_wahl = st.selectbox("Kategorie filtern:", ["Alle"] + kategorien)
    
    gefilterte_briefe = BRIEF_DATENBANK if kat_wahl == "Alle" else [b for b in BRIEF_DATENBANK if b["kategorie"] == kat_wahl]
    brief_titel = [f"{b['datum']} – {b['ort']} ({b['empfaenger']})" for b in gefilterte_briefe]
    
    selected_brief_idx = st.selectbox("Brief auswählen & lesen:", range(len(brief_titel)), format_func=lambda i: brief_titel[i])
    
    if gefilterte_briefe:
        b_info = gefilterte_briefe[selected_brief_idx]
        with st.expander("📖 Transkript-Auszug anzeigen", expanded=False):
            st.markdown(f"**Datum:** {b_info['datum']}")
            st.markdown(f"**Ort:** {b_info['ort']}")
            st.markdown(f"**Absender:** {b_info['absender']}")
            st.markdown(f"**Empfänger:** {b_info['empfaenger']}")
            st.divider()
            st.write(b_info["text"])

# ------------------------------------------------------------------------------
# 4. Kontext-Aufbereitung für den System-Prompt
# ------------------------------------------------------------------------------
kontext_text = "\n\n".join([
    f"=== BRIEF VOM {b['datum']} ({b['ort']}) ===\nAbsender: {b['absender']} | Empfänger: {b['empfaenger']}\nText:\n{b['text']}"
    for b in BRIEF_DATENBANK
])

SYSTEM_INSTRUCTION = f"""
Du bist ein historischer Dokumenten-Assistent für die Briefsammlung "Feldpost von Kurt Siegeler" (1944–1947).
Deine Aufgabe ist es, Fragen von Nutzerinnen und Nutzern präzise, sachlich und streng quellentreu zu beantworten.

Hier sind die maßgeblichen Transkripte und Auszüge aus den Briefen von Kurt Siegeler:
{kontext_text}

Verhaltensregeln:
1. Beantworte Fragen ausschließlich auf Basis des oben bereitgestellten Briefkontextes.
2. Nenne stets das konkrete Datum, den Absendeort (z.B. Lazarett Privas, POW Camp Ogden/Utah, Wisbech/England) und den Kontext.
3. Spekuliere nicht und erfinde keine Tatsachen, die nicht in den Briefen belegt sind.
4. Antworte in klarem, gut strukturiertem Deutsch mit passenden Hervorhebungen.
"""

# ------------------------------------------------------------------------------
# 5. Chat-Historie initialisieren
# ------------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hallo! Ich bin dein digitaler Assistent für die Feldpost von Kurt Siegeler. Alle Transkripte (1944–1947) sind fest eingebunden. Was möchtest du über seine Dienstzeit in Frankreich, den Aufenthalt in den US-Lagern (Idaho, Utah) oder die Kriegsgefangenschaft in England erfahren?"
        }
    ]

# ------------------------------------------------------------------------------
# 6. Bisherigen Chat-Verlauf anzeigen
# ------------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------------------------------------------------------------------
# 7. Benutzereingabe & API-Aufruf
# ------------------------------------------------------------------------------
user_prompt = st.chat_input("Stelle eine Frage (z. B. 'Was schrieb Kurt über die Heuernte in Privas?')...")

if user_prompt:
    api_key = api_key_input or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("🔑 Bitte gib einen gültigen Gemini API Key in der Seitenleiste ein oder setze GEMINI_API_KEY als Secret.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Gemini Client mit gewähltem Modell aufrufen
    client = genai.Client(api_key=api_key)

    with st.chat_message("assistant"):
        with st.spinner(f"Durchsuche Korrespondenz mit {selected_model}..."):
            try:
                contents = []
                for m in st.session_state.messages[1:]:
                    role = "user" if m["role"] == "user" else "model"
                    contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))

                response = client.models.generate_content(
                    model=selected_model,
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
                st.error(f"Fehler bei der Anfrage an die Gemini API: {e}")
                st.info("💡 Tipp: Falls ein Modell nicht verfügbar ist (404-Fehler), wähle in der linken Seitenleiste ein anderes Modell wie 'gemini-1.5-flash' oder 'gemini-2.0-flash'.")
