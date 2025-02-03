USER_CHAT_TEMPLATE = "<start_of_turn>mtumiaji\n{prompt}<end_of_turn><eos>\n"
MODEL_CHAT_TEMPLATE = "<start_of_turn>mfano\n"

# standard prompt
standard_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Jibu swali lifuatalo la hisabati. Ingiza tu jibu la mwisho kama nambari na usijumuishe maandishi mengine yoyote.\n"
) + "{question}\nJibu: " + MODEL_CHAT_TEMPLATE

# cot prompt
cot_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Jibu swali lifuatalo la hisabati. "
           "Fikiria hatua kwa hatua na acha mchakato wako wa mawazo hapa chini. "
           "Mstari wa mwisho unapaswa kuwa katika muundo 'Jibu ni xxx' ambapo xxx ni nambari.\n"
) + "Swali: {question}\nJibu kwa hatua:\n" + MODEL_CHAT_TEMPLATE

# propose_prompt
propose_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Fikiria kuwa umeundwa na {n} wanahisabati huru wanaozungumza {lang}, "
           "kila mmoja akiwa na mtazamo wa kipekee wa jinsi ya kutatua tatizo la hisabati lenye hatua nyingi.\n\n"
           "Kila mwanahisabati atapendekeza hatua mahususi kuelekea kutatua tatizo hilo. "
           "Hatua hiyo lazima ijumuishe:\n"
           "- **Maelezo mafupi** ya kwa nini hatua hii ni muhimu na jinsi inavyosaidia kutatua tatizo.\n"
           "- **Ulinganisho wazi** au hesabu inayotekeleza hatua hii.\n"
           "- Maelezo mafupi ya nini kinaweza kuwa hatua inayofuata kimantiki.\n\n"
           "Kila mwanahisabati anapaswa kuanza jibu lake na 'Wazo i: ', ambapo 'i' ni 1, 2, ... {n}.\n\n"
           "Majibu yanapaswa kuandikwa **katika mstari mmoja** kwa muundo ufuatao:\n\n"
           "Ufafanuzi wa hisabati unamalizika kwa thamani iliyokokotolewa.\n\n"
           "'Wazo i: Pendekezo. Ulinganisho: [Ufafanuzi wa kihisabati]. Hatua inayofuata: Hatua inayofuata.'\n\n"
           "Kila mwanahisabati anapaswa kushughulikia tatizo kwa uhuru, akizingatia mbinu tofauti au njia mbadala.\n\n"
           "Ikiwa hii ni hatua ya kwanza, kila mwanahisabati ataamua kwa uhuru njia bora ya kuanza.\n"
           "Ikiwa kuna muktadha wa awali, watajenga juu ya mchakato wa mawazo uliopo, kuhakikisha maendeleo yanaendelea.\n\n"
           "Mchakato huu unaendelea hadi jibu la mwisho lipatikane, ambapo kila hatua inachangia kuboresha suluhisho.\n\n"
) + "---\n" \
    "Swali: {question}\n\n" \
    "Muktadha (mchakato wa mawazo wa awali, ikiwa upo):\n{current_thought_process}\n\n" \
    "Hatua mahususi zilizopendekezwa na wanahisabati watatu:\n" \
    + MODEL_CHAT_TEMPLATE
# value_prompt
value_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Tathmini ikiwa hatua ya uamuzi iliyotolewa ina mchango wa maana katika kutatua tatizo. "
           "Jibu tu kwa 'Tathmini: hakika', 'Tathmini: huenda', au 'Tathmini: haiwezekani'. "
           "Usijumuishe maelezo au maandishi mengine yoyote.\n\n"
           "Chagua moja kati ya hukumu zifuatazo:\n"
           "- hakika: Hatua ni sahihi na ni maendeleo ya kimantiki kuelekea suluhisho.\n"
           "- huenda: Hatua hiyo inawezekana lakini huenda ikahitaji uboreshaji zaidi au inakosa maelezo muhimu.\n"
           "- haiwezekani: Hatua hiyo si sahihi, si husika, au inapingana na ukweli unaojulikana.\n\n"
           "---\n"
           "Swali: Treni inaondoka kutoka Kituo A ikiwa na abiria 50. Kwenye kituo kinachofuata, abiria 15 wanashuka, "
           "na abiria wapya 30 wanapanda. Sasa kuna abiria wangapi kwenye treni?\n\n"
           "Hatua inayopendekezwa ijayo: Hesabu mabadiliko halisi: -15 + 30.\nTathmini: hakika\n\n"
           "Hatua inayopendekezwa ijayo: Eleza hali kama mlinganyo: 50 - 15 + 30 = x.\nTathmini: hakika\n\n"
           "Hatua inayopendekezwa ijayo: Kudhani kuwa treni ilipoteza abiria 20 kwenye kituo kinachofuata na kuthibitisha kama jumla inalingana.\nTathmini: haiwezekani\n\n"
           "Hatua inayopendekezwa ijayo: Wasilisha uhusiano kama asilimia: (50 - 15) / 50.\nTathmini: haiwezekani\n\n"
           "Hatua inayopendekezwa ijayo: Fikiria kuongeza idadi ya abiria mara mbili kwa kila kituo.\nTathmini: haiwezekani\n\n"
           "Hatua inayopendekezwa ijayo: Fikiria jibu la mwisho kuwa x na kufanya mahesabu kinyume.\nTathmini: hakika\n\n"
) + "---\n" \
    "{question}\n\n" \
    "Hatua inayopendekezwa ijayo: {curr_candidate}\n\n" \
    "Tathmini:" \
    + MODEL_CHAT_TEMPLATE

# Force output prompt
force_output_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Kwa kuzingatia muktadha wote hapa chini, andika jibu la mwisho la tatizo.\n\n"
           "Fuata sheria hizi kikamilifu:\n"
           "- Andika hesabu hatua kwa hatua, ukieleza kila hatua kwa mantiki.\n"
           "- Jenga juu ya muktadha uliotolewa, kuhakikisha kila hatua ni mwendelezo wa kimantiki.\n"
           "- Usirudie hatua zozote ambazo tayari zipo kwenye muktadha.\n"
           "- Mstari wa mwisho unapaswa kuwa na jibu la mwisho kama nambari pekee bila maandishi mengine.\n\n"
           "Muktadha (mchakato wa mawazo wa awali, ikiwa upo):\n"
           "{context}\n\n"
) + "---\n" \
    "Swali: {question}\n\n" \
    "Suluhisho:\n" \
    "Hatua ya 1: " \
    + MODEL_CHAT_TEMPLATE

# Choose final answer
final_judge_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Wewe ni jaji wa kihisabati unayehusika na kuamua jibu la mwisho la tatizo.\n\n"
           "Kwanza, chunguza kwa makini taarifa ya tatizo. Kisha, kagua kwa kina majibu ya wagombea yaliyotolewa hapa chini.\n"
           "Linganisheni hoja katika kila jibu na kubaini jibu sahihi zaidi.\n\n"
           "Fuata sheria hizi:\n"
           "- Fikiria tatizo kwa mantiki kabla ya kufanya uamuzi.\n"
           "- Ikiwa kuna majibu sahihi zaidi ya moja, chagua jibu lenye hoja bora zaidi.\n"
           "- Ikiwa kuna kutofautiana au hatua zinazokosekana katika jibu la mgombea, usilitilie maanani.\n"
           "- Jibu la mwisho linapaswa kuwa nambari sahihi pekee bila maelezo au maandishi ya ziada.\n\n"
           "---\n"
           "Swali:\n"
           "{question}\n\n"
           "Majibu ya Wagombea:\n"
           "{candidate_answers}\n\n"
           "---\n"
           "Jibu la Mwisho: "
) + MODEL_CHAT_TEMPLATE