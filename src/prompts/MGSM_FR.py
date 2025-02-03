USER_CHAT_TEMPLATE = "<start_of_turn>utilisateur\n{prompt}<end_of_turn><eos>\n"
MODEL_CHAT_TEMPLATE = "<start_of_turn>modèle\n"

# standard prompt
standard_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Répondez à la question mathématique suivante. Entrez uniquement la réponse finale sous forme de nombre et rien d'autre.\n"
) + "{question}\nRéponse : " + MODEL_CHAT_TEMPLATE

# cot prompt
cot_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Répondez à la question mathématique suivante. "
           "Réfléchissez étape par étape et laissez votre raisonnement ci-dessous. "
           "La dernière ligne doit être de la forme 'La réponse est xxx' où xxx est un nombre.\n"
) + "Question : {question}\nRéponse étape par étape :\n" + MODEL_CHAT_TEMPLATE

# propose_prompt
propose_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Imaginez que vous soyez composé de {n} mathématiciens indépendants parlant {lang}, "
           "chacun ayant une perspective unique sur la manière de résoudre un problème mathématique en plusieurs étapes.\n\n"
           "Chaque mathématicien proposera une étape concrète pour résoudre le problème. "
           "L'étape doit inclure :\n"
           "- Une **explication concise** de pourquoi cette étape est nécessaire et comment elle aide à résoudre le problème.\n"
           "- Une **équation claire** ou un calcul qui met en œuvre cette étape.\n"
           "- Une brève indication de la prochaine étape logique.\n\n"
           "Chaque mathématicien doit commencer sa réponse par 'Pensée i : ', où 'i' est 1, 2, ... {n}.\n\n"
           "Les réponses doivent être écrites **sur une seule ligne** dans le format suivant :\n\n"
           "L'expression mathématique se termine par une valeur calculée.\n\n"
           "'Pensée i : Proposition. Équation : [Expression mathématique]. Prochaine étape : Action suivante.'\n\n"
           "Chaque mathématicien doit aborder le problème de manière indépendante, en considérant différentes méthodes ou décompositions.\n\n"
           "Si c'est la première étape, chaque mathématicien décidera indépendamment de la meilleure façon de commencer.\n"
           "Si un contexte préalable existe, ils s'appuieront sur le raisonnement en cours pour assurer une progression continue.\n\n"
           "Ce processus continue jusqu'à ce qu'une réponse définitive soit atteinte, chaque étape affinant la solution.\n\n"
) + "---\n" \
    "Question : {question}\n\n" \
    "Contexte (raisonnement précédent, si applicable) :\n{current_thought_process}\n\n" \
    "Étapes concrètes proposées par trois mathématiciens :\n" \
    + MODEL_CHAT_TEMPLATE

value_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Évaluez si l'étape de raisonnement proposée contribue de manière significative à la résolution du problème. "
           "Répondez uniquement par 'Évaluation : sûr', 'Évaluation : probable' ou 'Évaluation : impossible'. "
           "N'incluez aucune explication ni texte supplémentaire.\n\n"
           "Attribuez l'un des jugements suivants :\n"
           "- sûr : L'étape est correcte et constitue une progression logique vers la solution.\n"
           "- probable : L'étape est plausible mais peut nécessiter un affinement ou manquer de détails clés.\n"
           "- impossible : L'étape est incorrecte, hors sujet ou contredit des faits connus.\n\n"
           "---\n"
           "Question : Un train part de la gare A avec 50 passagers. À l'arrêt suivant, 15 passagers descendent "
           "et 30 nouveaux passagers montent. Combien de passagers y a-t-il maintenant dans le train ?\n\n"
           "Prochaine étape proposée : Calculer le changement net : -15 + 30.\nÉvaluation : sûr\n\n"
           "Prochaine étape proposée : Exprimer la situation sous forme d'équation : 50 - 15 + 30 = x.\nÉvaluation : sûr\n\n"
           "Prochaine étape proposée : Supposer que le train a perdu 20 passagers à l'arrêt suivant et vérifier si le total correspond.\nÉvaluation : impossible\n\n"
           "Prochaine étape proposée : Représenter la relation sous forme de pourcentage : (50 - 15) / 50.\nÉvaluation : impossible\n\n"
           "Prochaine étape proposée : Considérer que le nombre de passagers double à chaque arrêt.\nÉvaluation : impossible\n\n"
           "Prochaine étape proposée : Inverser le raisonnement en supposant que le total final est x et revenir en arrière.\nÉvaluation : sûr\n\n"
           "---\n"
           "Question : Il y avait neuf ordinateurs dans la salle des serveurs. Cinq autres ordinateurs ont été installés chaque jour de lundi à jeudi. "
           "Combien d'ordinateurs y a-t-il maintenant dans la salle des serveurs ?\n\n"
           "Prochaine étape proposée : Calculer le nombre total d'ordinateurs ajoutés : 5 × 4.\nÉvaluation : sûr\n\n"
           "Prochaine étape proposée : Représenter le changement sous forme d'une suite arithmétique : 9 + (5 × n), où n est le nombre de jours.\nÉvaluation : sûr\n\n"
           "Prochaine étape proposée : Considérer que les ordinateurs ont été retirés au lieu d'être ajoutés : 9 - (5 × 4).\nÉvaluation : impossible\n\n"
           "Prochaine étape proposée : Convertir le problème en un ratio : (9 / 5) × 4.\nÉvaluation : impossible\n\n"
           "Prochaine étape proposée : Supposer une croissance exponentielle au lieu d'une addition linéaire.\nÉvaluation : impossible\n\n"
           "Prochaine étape proposée : Vérifier si l'inversion du calcul donne toujours 9 ordinateurs initiaux.\nÉvaluation : sûr\n\n"
) + "---\n" \
    "{question}\n\n" \
    "Prochaine étape proposée : {curr_candidate}\n\n" \
    "Évaluation :" \
    + MODEL_CHAT_TEMPLATE

# Force output prompt
force_output_prompt = USER_CHAT_TEMPLATE.format(
    prompt="En tenant compte de tout le contexte ci-dessous, formulez la réponse finale au problème.\n\n"
           "Respectez strictement ces règles :\n"
           "- Écrivez les équations étape par étape en expliquant logiquement chaque calcul.\n"
           "- Construisez votre raisonnement à partir du contexte fourni, en veillant à ce que chaque étape soit une continuation logique.\n"
           "- Ne répétez pas les étapes déjà présentes dans le contexte.\n"
           "- La dernière ligne doit contenir la réponse finale sous forme de nombre, sans aucun texte supplémentaire.\n\n"
           "Contexte (raisonnement précédent, si disponible) :\n"
           "{context}\n\n"
           "---\n"
           "Question : Une boulangerie vend 25 pains par heure. Si elle fonctionne pendant 8 heures, "
           "combien de pains vend-elle en une journée ?\n\n"
           "Pour déterminer le nombre total de pains vendus, je vais calculer le nombre de pains vendus par heure.\n"
           "La boulangerie vend 25 pains par heure.\n"
           "Étant donné qu'elle fonctionne pendant 8 heures, je vais multiplier 25 par 8.\n\n"
           "25 × 8 = 200.\n"
           "Réponse finale : 200\n\n"
           "---\n"
           "Question : Une voiture roule à une vitesse de 60 km/h. Quelle distance parcourt-elle en 3 heures ?\n\n"
           "Tout d'abord, j'identifie les valeurs connues.\n"
           "La vitesse de la voiture est de 60 km/h et le temps de trajet est de 3 heures.\n"
           "J'utiliserai la formule : Distance = Vitesse × Temps.\n"
           "60 × 3 = 180.\n"
           "Réponse finale : 180\n\n"
) + "---\n" \
    "Contexte (raisonnement précédent, si disponible) :\n{context}\n\n" \
    "Question : {question}\n\n" \
    "Solution :\n" \
    "Étape 1 : " \
    + MODEL_CHAT_TEMPLATE

# Choose final answer
final_judge_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Vous êtes un juge mathématique chargé de déterminer la réponse finale à un problème.\n\n"
           "D'abord, analysez attentivement l'énoncé du problème. Ensuite, examinez rigoureusement les réponses candidates ci-dessous.\n"
           "Comparez le raisonnement dans chaque réponse candidate et déterminez le résultat final le plus précis.\n\n"
           "Suivez ces règles :\n"
           "- Réfléchissez logiquement au problème avant de prendre une décision.\n"
           "- S'il existe plusieurs réponses valides, choisissez celle qui est la mieux justifiée.\n"
           "- Si une réponse candidate contient des incohérences ou des étapes manquantes, ne la considérez pas.\n"
           "- Votre sortie finale doit être un nombre unique, sans explications ni texte supplémentaire.\n\n"
           "---\n"
           "Énoncé du problème :\n"
           "{question}\n\n"
           "Réponses candidates :\n"
           "{candidate_answers}\n\n"
           "---\n"
           "Réponse finale : "
) + MODEL_CHAT_TEMPLATE