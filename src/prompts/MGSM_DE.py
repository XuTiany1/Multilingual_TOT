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
    prompt="Stellen Sie sich vor, Sie bestehen aus {n} unabhängigen Mathematikern, die {lang} sprechen, "
           "jeder mit einer einzigartigen Perspektive darauf, wie man ein mehrstufiges mathematisches Problem löst.\n\n"
           "Jeder Mathematiker wird einen konkreten Schritt zur Lösung des Problems vorschlagen. "
           "Der Schritt muss Folgendes beinhalten:\n"
           "- Eine **prägnante Erklärung**, warum dieser Schritt notwendig ist und wie er zur Lösung des Problems beiträgt.\n"
           "- Eine **klare Gleichung** oder Berechnung, die diesen Schritt umsetzt.\n"
           "- Eine kurze Angabe, was der nächste logische Schritt sein könnte.\n\n"
           "Jeder Mathematiker sollte seine Antwort mit 'Gedanke i: ' beginnen, wobei 'i' 1, 2, ... {n} ist.\n\n"
           "Antworten müssen **in einer einzigen Zeile** im folgenden Format geschrieben werden:\n\n"
           "Der mathematische Ausdruck endet mit einem berechneten Wert.\n\n"
           "'Gedanke i: Vorschlag. Gleichung: [Mathematischer Ausdruck]. Nächster Schritt: Nächste Aktion.'\n\n"
           "Jeder Mathematiker sollte das Problem unabhängig angehen und verschiedene Methoden oder Zerlegungen in Betracht ziehen.\n\n"
           "Falls dies der erste Schritt ist, entscheidet jeder Mathematiker unabhängig über den besten Einstieg.\n"
           "Falls ein vorheriger Kontext existiert, bauen sie auf dem aktuellen Denkprozess auf, um kontinuierlichen Fortschritt zu gewährleisten.\n\n"
           "Dieser Prozess wird fortgesetzt, bis eine endgültige Antwort erreicht ist, wobei jeder Schritt die Lösung weiter verfeinert.\n\n"
) + "---\n" \
    "Frage: {question}\n\n" \
    "Kontext (bisheriger Denkprozess, falls vorhanden):\n{current_thought_process}\n\n" \
    "Konkrete Schritte, die von drei Mathematikern vorgeschlagen wurden:\n" \
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