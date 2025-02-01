USER_CHAT_TEMPLATE = "<start_of_turn>benutzer\n{prompt}<end_of_turn><eos>\n"
MODEL_CHAT_TEMPLATE = "<start_of_turn>modell\n"

# standard prompt
standard_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Beantworte die folgende mathematische Frage. Gib nur die endgültige Antwort als Zahl ein und nichts anderes.\n"
) + "{question}\nAntwort: " + MODEL_CHAT_TEMPLATE

# cot prompt
cot_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Beantworte die folgende mathematische Frage. "
           "Denke Schritt für Schritt nach und dokumentiere deinen Denkprozess unten. "
           "Die letzte Zeile sollte die Form 'Die Antwort ist xxx' haben, wobei xxx eine Zahl ist.\n"
) + "Frage: {question}\nSchrittweise Antwort:\n" + MODEL_CHAT_TEMPLATE

# propose_prompt
propose_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Stell dir vor, du bestehst aus {n} unabhängigen Mathematikern, die {lang} sprechen, "
           "und jeder hat eine einzigartige Perspektive darauf, wie ein mehrstufiges mathematisches Problem gelöst werden kann.\n\n"
           "Bevor du mit deinem Denkprozess antwortest, sollte jeder Mathematiker seine Antwort mit "
           "'Mathematiker i: ' beginnen, wobei 'i' 1, 2 oder 3 sein kann.\n\n"
           "Basierend auf der gegebenen Frage und dem aktuellen Denkprozess wird jeder Mathematiker unabhängig "
           "einen einzigartigen, kreativen und gültigen nächsten Schritt zur Lösung des Problems vorschlagen. "
           "Jeder Schritt sollte sich in der Herangehensweise unterscheiden, indem verschiedene mathematische Methoden, "
           "Problembrechungen oder alternative Darstellungen genutzt werden.\n\n"
           "Jeder Mathematiker erklärt seine Überlegungen klar und prägnant, bevor er seinen nächsten Schritt vorschlägt. "
           "Sie fügen nur ihren ersten Schritt hinzu, sodass eine weitere Diskussion und Verfeinerung möglich ist.\n\n"
           "Falls kein vorheriger Kontext existiert, markiert dies den Beginn des Denkprozesses, und die Mathematiker schlagen "
           "verschiedene Möglichkeiten vor, das Problem zu lösen.\n\n"
           "Dieser Prozess wird Schritt für Schritt fortgesetzt, bis eine endgültige Antwort erreicht wird.\n\n"
) + "---\n" \
    "Frage: {question}\n\n" \
    "Kontext (bisheriger Denkprozess, falls vorhanden):\n{current_thought_process}\n\n" \
    "Liste möglicher nächster Schritte (jede Zeile stellt die Perspektive eines einzelnen Mathematikers dar):\n" \
    + MODEL_CHAT_TEMPLATE

# value_prompt
value_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Bewerte, ob der gegebene Denkprozessschritt einen sinnvollen Beitrag zur Lösung des Problems leistet. "
           "Antworte nur mit 'Bewertung: sicher', 'Bewertung: wahrscheinlich' oder 'Bewertung: unmöglich'. "
           "Füge keine Erklärungen oder zusätzlichen Texte hinzu.\n\n"
           "Wähle eine der folgenden Bewertungen:\n"
           "- sicher: Der Schritt ist korrekt und eine logische Fortsetzung der Lösung.\n"
           "- wahrscheinlich: Der Schritt ist plausibel, könnte jedoch weiter verfeinert werden oder es fehlen wichtige Details.\n"
           "- unmöglich: Der Schritt ist falsch, irrelevant oder widerspricht bekannten Fakten.\n\n"
           "---\n"
           "Frage: Ein Zug fährt mit 50 Passagieren vom Bahnhof A ab. An der nächsten Haltestelle steigen 15 Passagiere aus, "
           "und 30 neue Passagiere steigen ein. Wie viele Passagiere sind jetzt im Zug?\n\n"
           "Vorgeschlagener nächster Schritt: Berechne die Nettoänderung: -15 + 30.\nBewertung: sicher\n\n"
           "Vorgeschlagener nächster Schritt: Stelle die Situation als Gleichung dar: 50 - 15 + 30 = x.\nBewertung: sicher\n\n"
           "Vorgeschlagener nächster Schritt: Gehe davon aus, dass der Zug an der nächsten Haltestelle 20 Passagiere verloren hat und überprüfe, ob die Gesamtzahl übereinstimmt.\nBewertung: unmöglich\n\n"
           "Vorgeschlagener nächster Schritt: Stelle die Beziehung als Prozentsatz dar: (50 - 15) / 50.\nBewertung: unmöglich\n\n"
           "Vorgeschlagener nächster Schritt: Erwäge, die Anzahl der Passagiere an jeder Haltestelle zu verdoppeln.\nBewertung: unmöglich\n\n"
           "Vorgeschlagener nächster Schritt: Kehre die Überlegung um, indem du davon ausgehst, dass die Endzahl x ist, und arbeite rückwärts.\nBewertung: sicher\n\n"
           "---\n"
           "Frage: Im Serverraum gab es neun Computer. Von Montag bis Donnerstag wurden jeden Tag fünf weitere Computer installiert. "
           "Wie viele Computer befinden sich jetzt im Serverraum?\n\n"
           "Vorgeschlagener nächster Schritt: Berechne die insgesamt hinzugefügten Computer: 5 × 4.\nBewertung: sicher\n\n"
           "Vorgeschlagener nächster Schritt: Stelle die Änderung als arithmetische Folge dar: 9 + (5 × n), wobei n die Anzahl der Tage ist.\nBewertung: sicher\n\n"
           "Vorgeschlagener nächster Schritt: Berücksichtige, dass die Computer entfernt statt hinzugefügt wurden: 9 - (5 × 4).\nBewertung: unmöglich\n\n"
           "Vorgeschlagener nächster Schritt: Wandle das Problem in ein Verhältnis um: (9 / 5) × 4.\nBewertung: unmöglich\n\n"
           "Vorgeschlagener nächster Schritt: Gehe von einem exponentiellen Wachstumsmuster statt einer linearen Addition aus.\nBewertung: unmöglich\n\n"
           "Vorgeschlagener nächster Schritt: Überprüfe, ob die Umkehrung der Berechnung immer noch zu den ursprünglichen 9 Computern führt.\nBewertung: sicher\n\n"
) + "---\n" \
    "{question}\n\n" \
    "Vorgeschlagener nächster Schritt: {curr_candidate}\n\n" \
    "Bewertung:" \
    + MODEL_CHAT_TEMPLATE

# Force output prompt
force_output_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Angesichts des unten stehenden Kontexts, formuliere die endgültige Antwort auf das Problem.\n\n"
           "Befolge diese Regeln strikt:\n"
           "- Schreibe die Gleichungen Schritt für Schritt auf und erkläre jede Berechnung logisch.\n"
           "- Baue auf dem bereitgestellten Kontext auf und stelle sicher, dass jeder Schritt eine logische Fortsetzung ist.\n"
           "- Wiederhole keine bereits vorhandenen Schritte aus dem Kontext.\n"
           "- Die letzte Zeile sollte nur die endgültige Antwort als Zahl enthalten und nichts weiter.\n\n"
           "Kontext (bisheriger Denkprozess, falls vorhanden):\n"
           "{context}\n\n"
) + "---\n" \
    "Frage: {question}\n\n" \
    "Lösung:\n" \
    "Schritt 1: " \
    + MODEL_CHAT_TEMPLATE

# Choose final answer
final_judge_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Du bist ein mathematischer Richter, der die endgültige Antwort auf ein Problem bestimmen soll.\n\n"
           "Analysiere zunächst die Problemstellung sorgfältig. Untersuche dann gründlich die unten aufgeführten Kandidatenantworten.\n"
           "Vergleiche die Begründungen in jeder Antwort und bestimme die genaueste endgültige Lösung.\n\n"
           "Befolge diese Regeln:\n"
           "- Denke logisch über das Problem nach, bevor du eine Entscheidung triffst.\n"
           "- Falls es mehrere gültige Antworten gibt, wähle die am besten begründete aus.\n"
           "- Falls eine Antwort Inkonsistenzen oder fehlende Schritte enthält, ignoriere sie.\n"
           "- Deine endgültige Ausgabe sollte nur die korrekte Zahl sein, ohne Erklärungen oder zusätzlichen Text.\n\n"
           "---\n"
           "Problemstellung:\n"
           "{question}\n\n"
           "Kandidatenantworten:\n"
           "{candidate_answers}\n\n"
           "---\n"
           "Endgültige Antwort: "
) + MODEL_CHAT_TEMPLATE