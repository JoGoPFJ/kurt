import os
import streamlit as st
from google import genai
from google.genai import types

# ------------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Feldpost Kurt Siegeler – Chatbot",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# 2. EMBEDDED KNOWLEDGE BASE: FELDPOST-TRANSKRIPTE (1944-1947)
# ------------------------------------------------------------------------------
BRIEF_DATENBANK = [
    {
        "datum": "08.01.1944",
        "ort": "Frankreich (O.U.)",
        "absender": "Kurt Siegeler (44-Pz.Gren.)",
        "empfaenger": "Elisabeth, Hermann, Friedrich Siegeler",
        "thema": "Dienstverhältnisse, Verpflegungsengpässe, Gürtel enger schnallen",
        "text": """U.U. den 8.1.44
Liebe Elisabeth, Hermann, Friedrich und Mutter!
Ja, Ihr Lieben, ich schreibe so eine gemeinsame Anschrift für Euch alle. Es ist mir wieder nicht möglich, jedem Einzelnen zu schreiben. Schon wieder ist eine Woche dahin und ich bin nicht zum Schreiben gekommen...
Ich habe aber auch diese Woche tüchtig Wurst gegessen. Es hat nach dem Hungern keinen Zweck. Wer ganz egal, ich muss einfach was Kräftiges bei dem schweren Dienst haben... So kostet z.B. 50 Gramm = 200 Francs. Ich bin schlank und dünn geworden. Den Gürtel habe ich in das fünfte Loch schnallen müssen...
Nachts muss der eine Teil der Wache Schilde und Strauchwerk bewachen, damit man es nicht anstecken kann. Für heute recht vielmals gegrüßt von Eurem besorgten Papa."""
    },
    {
        "datum": "15.01.1944",
        "ort": "Frankreich (O.U.)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "thema": "Verpflegungsnot, Päckchen-Zulassungsmarken",
        "text": """O.U. den 15.1.44
Liebe Elisabeth und Kinder!
Schon wieder ist eine Woche dahin, ohne dass ich ein Lebenszeichen von Euch erhalten habe... Die Verpflegung ist einfach nicht ausreichend bei dem harten Dienst. Ich bin immer hungrig. Nachmittags auf dem Marktplatz bin ich aus lauter Schwäche ohnmächtig geworden... Der Gürtel ist im fünften Loch.
Beiliegend füge ich zwei Päckchen-Zulassungsmarken bei. Schicke mir aber bitte die Päckchen im Abstand von einer Woche, damit ich mir das einteilen kann."""
    },
    {
        "datum": "22.01.1944",
        "ort": "Frankreich (O.U.)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "thema": "Dienstpflichten, Sorgen um die Familie in Oberschelden",
        "text": """O.U. den 22.1.44
Meine liebe Frau Elisabeth!
Ich habe Deinen Brief vom 5.1.44 erhalten. Schön, dass bei Euch in Oberschelden noch alles in Ordnung ist. Sei unbesorgt, wenn der Dienst auch hart ist, wir halten durch. Ich hoffe bald auf Heimaturlaub."""
    },
    {
        "datum": "06.02.1944",
        "ort": "Frankreich (O.U.)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth, Hermann & Friedrich Siegeler",
        "thema": "Nachtmarsch 36 km, Schlittenfahren, Postgrüße",
        "text": """O.U. den 6.2.44
Liebe Elisabeth! Bin soeben von einem 36 km Nachtmarsch zurückgekommen...
Lieber Hermann! Habe Deinen Brief erhalten. Schön, dass Du der Mama auf dem Hof hilfst.
Lieber Friedrich! Mein liebes Müppelchen, Pappas Sonne scheint hier warm. Pass gut auf Mama auf!"""
    },
    {
        "datum": "18.03.1944",
        "ort": "La Grimaudière / France",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "thema": "Bunkerausbau im Garten/Hesselbach, Luftschutz, Diebstahl",
        "text": """O.U. den 18.3.44
Liebe Elisabeth!
Wegen Bunkerausbau hinter der Scheune: Sollte der Fall eintreten, dass die Scheune und der Holzschuppen brennen, würde es in dem Bunker zwischen den Gebäuden zu heiß. Baut den Bunker möglichst nahe an den alten Keller, damit man ihn später als Kartoffelkeller verwenden kann. Der Luftschutzbund gibt hohe Zuschüsse!
Passt gut auf die Wertsachen auf, lasst Schlösser auswechseln!"""
    },
    {
        "datum": "12.04.1944",
        "ort": "Frankreich (O.U.)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Mutter",
        "thema": "Urlaubsgesuch, Dreschmaschine, Zusage für Heimatbesuch",
        "text": """O.U. den 12.4.44
Liebe Elisabeth! Deinen Brief vom 21.3. habe ich erhalten. Du schwebst schon in Urlaubsstimmung, aber so schnell geht das nicht. Schreibe mir stichhaltige Gründe wegen der Landwirtschaft und der Dreschmaschine...
Liebe Mama! Herzliche Glückwünsche nachträglich zum Geburtstag!"""
    },
    {
        "datum": "16.04.1944",
        "ort": "Frankreich (O.U.)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "thema": "Entzündung am Zeigefinger, Innendienst, Lazarett droht",
        "text": """N.U. den 16.4.44
Meine liebe Elisabeth! Es ist Sonntagmittag. Ich bin Stubendienstler, da mein rechter Zeigefinger stark entzündet ist. Wenn der Finger nicht bald besser wird, muss ich ins Lazarett und er muss aufgeschnitten werden. Das ist schade, weil eine Stelle als Schreiber frei wird..."""
    },
    {
        "datum": "12.05.1944",
        "ort": "Lazarett Fontainebleau",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "thema": "Heilung des Fingers, Bunkerbau in Oberschelden, Landwirtschaftstipps",
        "text": """Fontainebleau, den 12.5.44
Liebe Elisabeth! Der Finger ist schon wieder fast zugeheilt, nur der Arm eitert noch etwas. Sorgen bestehen keine mehr.
Dass die Gemeinde Oberschelden in der Hesselbach einen Bunker baut, ist gut, liegt für Euch aber ungünstig. Besser wäre ein eigener Bunker bei den Wohngebäuden.
Zur Landwirtschaft: Schneidet die Äste am Hochwald radikal ab. Streut den frischen Mist täglich aus..."""
    },
    {
        "datum": "14.05.1944",
        "ort": "Lazarett Fontainebleau",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "thema": "Muttertagskarte aus dem Lazarett",
        "text": """Fontainebleau, den 14.5.44
Meine liebe Elisabeth! Zum diesjährigen Muttertag wünsche ich Dir aus dem Lazarett in Fontainebleau alles Gute und mögest Du ihn in bester Gesundheit und alter Frische erleben dürfen. Viele Grüße und Küsse, Dein Kurt."""
    },
    {
        "datum": "15.05.1944",
        "ort": "Lazarett Fontainebleau",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "thema": "Räumung des Lazaretts, Verlegung Richtung Heimat/Südfrankreich",
        "text": """Fontainebleau, den 15.5.44
Liebe Elisabeth! Es ist der Befehl gekommen, das Lazarett Fontainebleau am 16.5.44 morgens um 10 Uhr zu räumen. Ich werde verlegt. Schicke vorerst keine Pakete oder Briefe mehr an die alte Adresse, bis Du meine neue Anschrift hast!"""
    },
    {
        "datum": "17.05.1944",
        "ort": "Lazarett Privas (Südfrankreich)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "thema": "Ankunft in Privas nach 36h Bahnfahrt an der Rhône",
        "text": """Privas, den 17.5.44
Liebe Elisabeth! Nach 1,5-tägiger Bahnfahrt sind wir hier in Privas angekommen (ehemalige franz. Strafanstalt). Die Fahrt entlang der Rhône durch die Obstgegenden war herrlich – Kirschen, Pfirsiche, Weinreben. Wir sind hier zu 60 Mann im Saal untergebracht."""
    },
    {
        "datum": "20.05.1944",
        "ort": "Lazarett Privas",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "thema": "Wundbehandlung, genaue Anweisungen zur Heuernte und Schrotmühle",
        "text": """Privas, den 20.5.44
Liebe Elisabeth u. Kinder! Der Finger ist schön geheilt, nur die Wunde am rechten Unterarm ist wieder aufgeplatzt.
Zur Heuernte: Achtet beim Aufstellen des Heugebläses darauf, dass der Motor mit der großen Riemenscheibe genommen wird! Die Riemenscheibe liegt in der Schrotmühle im Trichter. Die passenden Hölzer liegen in der Schublade im Küchentisch. Besorge rechtzeitig 15-Ampere-Sicherungen! Verbinde Dich mit Übachs Walter."""
    },
    {
        "datum": "30.05.1944",
        "ort": "Privas / Frontleitstelle Lyon",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "thema": "Entlassung aus dem Lazarett, Fahrt nach Lyon, Treibriemen-Pflege",
        "text": """Privas, den 30.5.44
Liebe Elisabeth u. Kinder! Habe soeben die Entlassungspapiere erhalten. Fahre heute Nachmittag um 4 Uhr zur Frontleitstelle Lyon.
Wichtig für die Ernte: Den Treibriemen über Nacht abnehmen! Wenn er feucht wird und aufliegt, längt er sich und treibt nicht mehr gut."""
    },
    {
        "datum": "02.06.1944",
        "ort": "Frankreich (Stammkompanie)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "thema": "Rückkehr zur Stammkompanie, Bombardement während der Zugfahrt",
        "text": """O.U. den 2.6.44
Liebe Elisabeth u. Kinder! Bin soeben wieder bei meiner alten Kompanie gelandet. Die Fahrt war abenteuerlich – nachts gab es Bombenangriffe auf die Bahnhöfe mit 2,5 Stunden Verspätung. Schön, bekannte Gesichter wiederzusehen."""
    },
    {
        "datum": "11.06.1944",
        "ort": "Frankreich (Anmarsch Front)",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "thema": "Invasion in der Normandie ('Zweite Front'), Eilmarsch gen Norden",
        "text": """Frankreich, den 11.6.44
Liebe Elisabeth u. Kinder! Über Nacht ist die zweite Front errichtet worden. Unsere Einheiten sind bestimmt worden, den Engländern bei Le Havre entgegenzutreten. Wir marschieren zu Fuß und per Rad. Der Feind greift mit Bombern Brücken und Bahnen an. Schwerste Strapazen, aber wir vertrauen auf Gott."""
    },
    {
        "datum": "04.07.1944",
        "ort": "Hauptkampflinie (H.K.L.) Nord-Normandie",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "thema": "Einsatz in der H.K.L. (300m vom Feind), Artilleriefeuer, Eingraben",
        "text": """H.K.L. NW-Normandie, den 4.7.44
Liebe Elisabeth und Kinder! Seit 3 Tagen befinden wir uns jetzt in der H.K.L. Wir liegen 300-400 Meter den amerikanischen Truppen gegenüber. Der Feind schießt mächtig mit seinen Geschützen, aber wir haben uns in unsere Löcher verstrichen. Bisher keine Verluste in unserer Kompanie. Ich bin in Gedanken immer bei Euch!"""
    },
    {
        "datum": "01.11.1944",
        "ort": "P.O.W. Camp Rupert, Idaho, USA",
        "absender": "Obergefr. Kurt Siegeler (31 G 141 439)",
        "empfaenger": "Elisabeth, Hermann, Friedrich & Mutter Siegeler",
        "thema": "US-Kriegsgefangenschaft, Zuckerrübenernte, Sorge um Post",
        "text": """Camp Rupert, Idaho, U.S.A., den 1.11.1944
Meine liebe Elisabeth, lieber Hermann, lieber Friedrich, meine liebe Mutter!
Es ist mir eine Freude, Euch die mir wöchentlich erlaubten Zeilen zu schreiben. Bei mir ist alles beim Alten, gesund wie immer. Die Zuckerrübenernte geht langsam dem Ende zu. Meine Sorgen um Euch sind groß, da ich noch keine Post erhalten habe. Haltet das Vieh auf der Höhe und sorgt für Nachwuchs! Hoffentlich dauert der elende Krieg nicht mehr lange."""
    },
    {
        "datum": "02.12.1944",
        "ort": "P.O.W. Camp Ogden, Utah, USA",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth, Hermann, Friedrich & Mutter Siegeler",
        "thema": "Arbeit im Zuckerlagerhaus in Ogden, Sackkarre, Sehnsucht nach Heimarbeit",
        "text": """Ogden, Utah, U.S.A., den 2.12.1944
Meine liebe Elisabeth, lieber Hermann, lieber Friedrich, meine liebe Mutter!
Ich bin seit einiger Zeit in einem großen Zuckerlagerhaus beschäftigt. Wir fahren morgens mit dem Omnibus 15 Minuten zur Arbeit. Es ist saubere Arbeit – die Zuckersäcke werden mit Sackkarren gefahren und auf Transportbänder geladen. Abends um 5 Uhr geht es zurück. Wenn ich an die Arbeit zu Hause denke, kommt die Sehnsucht. Passt gut auf Euch auf!"""
    },
    {
        "datum": "27.01.1945",
        "ort": "P.O.W. Camp Ogden, Utah, USA",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Kinder",
        "thema": "Küchendienst im Lager, Traum von der Jugendzeit, Trost",
        "text": """Ogden, Utah, den 27.1.1945
Meine liebe Elisabeth! Es ist 10 Uhr morgens. Ich greife zur Feder, bevor ich nachmittags wieder in der Lagerküche arbeiten muss.
Liebe Frau, ich habe vergangene Nacht von Dir geträumt – von längst vergangenen Zeiten unserer Jugendzeit. Wenn ich wiederkomme, wollen wir alle Sorgen begraben. Was machen die beiden Jungs? Bleibt gesund!"""
    },
    {
        "datum": "03.02.1945",
        "ort": "P.O.W. Camp Ogden, Utah, USA",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth, Hermann & Friedrich Siegeler",
        "thema": "6 Monate Gefangenschaft, Hausbrand/Kohle bestellen, Landmaschinen",
        "text": """Ogden, Utah, den 3.2.1945
Meine liebe Elisabeth! Nun bin ich schon ein halbes Jahr Kriegsgefangener. Die Zeit ist verhältnismäßig schnell vergangen. Mir geht es sehr gut.
Ratschlag: Decke Dich im Sommer rechtzeitig mit Hausbrand/Kohle ein (über Herrn Schneider in Siegen). Lass das Fahrgeschirr und die Maschinen instand setzen! Wegen der Frühjahrsbestellung besprich Dich mit Deinem Vater oder Karl."""
    },
    {
        "datum": "28.03.1945",
        "ort": "P.O.W. Camp Ogden, Utah, USA",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler",
        "thema": "Schneeschauer in Utah, Nachfrage nach Tochter Ruths Verletzung",
        "text": """Ogden, Utah, den 28.3.1945
Meine liebe Elisabeth! Post ist verteilt worden, aber leider war für mich nichts dabei. Wie hat sich die Verletzung von Ruth gebessert? Hier in Utah wechselt Schneeschauer mit Sonne. Gesundheitlich geht es mir ausgezeichnet! Tausend Grüße, Euer Papa."""
    },
    {
        "datum": "25.04.1945",
        "ort": "P.O.W. Camp Ogden, Utah, USA",
        "absender": "Kurt Siegeler",
        "empfaenger": "Hermann Siegeler (Sohn)",
        "thema": "Ackerarbeiten, Eggen und Fahren im Sommer",
        "text": """Ogden, Utah, den 25.4.1945
Mein lieber Hermann! Wenn Du diese Karte bekommst, seid Ihr mitten im Sommer und Deine Mama hat viel Arbeit. Ich hoffe, dass Du und Friedrich Ihr helft, so viel Ihr könnt. Das Fahren und Eggen werdet Ihr bestimmt schon machen können. Seid brav! Euer Papa."""
    },
    {
        "datum": "30.05.1946",
        "ort": "Camp 409a Wolterton Park, Norwich, England",
        "absender": "Kurt Siegeler (Gef.Nr. B 707975)",
        "empfaenger": "Elisabeth, Hermann & Friedrich Siegeler",
        "thema": "Verlegung von Belgien nach England, Enttäuschung über Verzögerung der Heimkehr",
        "text": """Wolterton Park, Aylsham nr. Norwich, den 30.5.1946
Meine liebe Elisabeth! Ihr werdet staunen, wenn Ihr Post aus England bekommt. Wir sind am 25.5.46 von Belgien (Nähe Brüssel) hierher verlegt worden. Mit dem Nach-Hause-Kommen wird es also so bald nichts werden. Das Schicksal hat es anders gewollt. Emil Klöckner aus Niederschelden ist auch in der Baracke neben mir. Mir geht es noch gut. Tausend Grüße, Euer Papa."""
    },
    {
        "datum": "19.06.1946",
        "ort": "Fridaybridge Camp No. 90, Wisbech, Cambridgeshire",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth, Hermann & Friedrich Siegeler",
        "thema": "Arbeit beim Ziegelaufladen, Landschaft in Südengland, Geburtstagsgrüße",
        "text": """Wisbech, den 19.6.1946
Meine liebe Elisabeth, lieber Hermann und lieber Friedrich!
Ich arbeite seit zwei Tagen beim Ziegelsteine aufladen. Die Gegend hier nahe der Küste ist eben und wunderschön mit Parkanlagen. Wir bewohnen mit 175 Mann ein großes Haus.
Hermann und Friedrich gratuliere ich nachträglich ganz herzlich zum Geburtstag! Euer liebender Papa."""
    },
    {
        "datum": "08.09.1946",
        "ort": "Fridaybridge Camp No. 90, Wisbech",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth Siegeler & Söhne",
        "thema": "Verkauf des Ochsen 'Franz', Kauf einer Mähmaschine/Waschmaschine",
        "text": """Wisbech, den 8.9.1946
Meine liebe Elisabeth!
Verkaufe den kranken Ochsen 'Franz'. Für das Geld kannst Du Dir vielleicht im Frühjahr eine große Fahrkuh oder eine elektrische Waschmaschine/Mähmaschine kaufen. Spare nicht auf Kosten Deines Körpers! Tausend Grüße, Euer Papa."""
    },
    {
        "datum": "28.09.1946",
        "ort": "Fridaybridge Camp No. 90, Wisbech",
        "absender": "Kurt Siegeler",
        "empfaenger": "Elisabeth, Hermann & Friedrich Siegeler",
        "thema": "Umzug in Zeltlager, Arbeit in der Marmeladenfabrik",
        "text": """Wisbech, den 28.9.1946
Meine liebe Elisabeth! Gestern Abend sind wir in ein neues Zeltlager umgezogen. Wir fahren morgens in Lastautos in eine Marmeladenfabrik zum Arbeiten. Verkauf die kleine rote Kuh, wenn Du nicht genug Futter hast. Tausend Grüße, Papa."""
    },
    {
        "datum": "27.12.1946",
        "ort": "Vandernohe",
        "absender": "Georg Mauderer (Heimkehrer / Freund)",
        "empfaenger": "Familie Siegeler (Oberschelden)",
        "thema": "Lebenszeichen nach Verwundung Ostermontag 1945 und Flucht nach Hause",
        "text": """Vandernohe, den 27.12.1946
Liebe Familie Siegeler! Nach sehr langer Zeit gebe ich wieder ein Lebenszeichen. Am Ostermontag 1945 wurde ich verwundet (Arm- und Beindurchschuss). Am 8. Mai 45 ist mein Lazarettzug im Sudetenland stehen geblieben. Bin mit Kameraden abgehauen und am 30. Mai 1945 nach Hause gekommen. Am 23.11.46 habe ich geheiratet. Ist Kurt schon glücklich zu Hause? Herzliche Neujahrsgrüße!"""
    }
]

# System-Instruktion für das KI-Modell
SYSTEM_PROMPT = f"""
Du bist ein sachkundiger, historisch präziser KI-Assistent für das Feldpost-Archiv von **Kurt Siegeler** (1944–1947).
Deine Aufgabe ist es, Fragen von Nutzern, Schülern oder Historikern ausschließlich auf Basis der echten Briefinhalte zu beantworten.

Hier sind die vollständigen transkribierten Feldpostbriefe und Dokumente aus dem Archiv fest eingebunden:

{BRIEF_DATENBANK}

VERHALTENSREGELN:
1. Antworte immer freundlich, sachlich und auf Deutsch.
2. Stütze jede Aussage auf konkrete Briefe (nenne Datum, Ort, Absender/Empfänger).
3. Wenn eine Information nicht in den Briefen steht, sage das deutlich.
4. Hebe wichtige Orte (z.B. Fontainebleau, Privas, Ogden/Utah, Wisbech) und Themen (Landwirtschaft, Kriegsgefangenschaft, Lazarett) hervor.
"""

# ------------------------------------------------------------------------------
# 3. SEITENLEISTE: API-KEY & BRIEF-BROWSER
# ------------------------------------------------------------------------------
st.sidebar.title("✉️ Feldpost-Archiv")
st.sidebar.markdown("**Kurt Siegeler (1906–1985)**\nFeldpostbriefe & Gefangenenpost 1944–1947")

# API-Key Konfiguration
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Gemini API Key eingeben:", type="password", help="Hole dir einen kostenlosen Key unter aistudio.google.com")

st.sidebar.divider()

# Interaktiver Brief-Browser
st.sidebar.subheader("📖 Transkripte durchsuchen")
selected_brief_idx = st.sidebar.selectbox(
    "Wähle einen Brief zum Lesen:",
    range(len(BRIEF_DATENBANK)),
    format_func=lambda i: f"{BRIEF_DATENBANK[i]['datum']} – {BRIEF_DATENBANK[i]['ort']}"
)

b = BRIEF_DATENBANK[selected_brief_idx]
with st.sidebar.expander(f"Details: Brief vom {b['datum']}", expanded=True):
    st.write(f"**Absender:** {b['absender']}")
    st.write(f"**Empfänger:** {b['empfaenger']}")
    st.write(f"**Thema:** {b['thema']}")
    st.caption("Textauszug / Transkription:")
    st.info(b["text"])

# ------------------------------------------------------------------------------
# 4. HAUPTBEREICH: CHAT-INTERFACE
# ------------------------------------------------------------------------------
st.title("✉️ Chatbot: Feldpost von Kurt Siegeler")
st.markdown("""
Frage die KI nach Ereignissen, Daten, Lazarettaufenthalten in Frankreich, den US-/britischen Gefangenenlagern oder den landwirtschaftlichen Anweisungen von Kurt Siegeler an seine Frau Elisabeth.
""")

# Beispielfragen als Buttons
st.markdown("**Beispielfragen:**")
col1, col2, col3 = st.columns(3)

prompt_input = None
if col1.button("🏥 Lazarett Fontainebleau & Privas"):
    prompt_input = "In welchen Lazaretten lag Kurt Siegeler 1944 in Frankreich und woran war er verletzt?"
if col2.button("🚜 Anweisungen zur Heuernte"):
    prompt_input = "Welche genauen Anweisungen gab Kurt seiner Frau Elisabeth zur Heuernte und zur Schrotmühle?"
if col3.button("🇺🇸 US-Gefangenencamp Ogden"):
    prompt_input = "Was berichtete Kurt aus dem P.O.W. Camp Ogden in Utah über seine Arbeit und das Lagerleben?"

# Session State für Chat-Historie
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hallo! Ich kenne alle transkribierten Feldpostbriefe von Kurt Siegeler aus den Jahren 1944 bis 1947. Was möchtest du erfahren?"}
    ]

# Bisherigen Verlauf anzeigen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Tastatur-Eingabe
user_query = st.chat_input("Deine Frage zu den Feldpostbriefen...") or prompt_input

if user_query:
    if not api_key:
        st.error("Bitte gib zuerst einen validen Gemini API Key in der Seitenleiste ein oder setze GEMINI_API_KEY als Umgebungsvariable.")
    else:
        # Nachricht des Nutzers hinzufügen
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Gemini API-Aufruf
        with st.chat_message("assistant"):
            with st.spinner("Durchsuche die transkribierten Briefe..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    # Gesprächsverlauf aufbauen
                    history_contents = [SYSTEM_PROMPT]
                    for m in st.session_state.messages:
                        history_contents.append(f"{m['role'].upper()}: {m['content']}")

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents="\n\n".join(history_contents),
                        config=types.GenerateContentConfig(
                            temperature=0.2,
                            max_output_tokens=1000,
                        )
                    )
                    
                    reply_text = response.text
                    st.markdown(reply_text)
                    st.session_state.messages.append({"role": "assistant", "content": reply_text})

                except Exception as e:
                    st.error(f"Fehler bei der Anfrage an die Gemini API: {e}")
