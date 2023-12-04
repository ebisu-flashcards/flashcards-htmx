{ 
    "name":  "Regular Verb PT 🇵🇹 / EN 🇬🇧", 
    "description":  "The same card and its reverse is rendered with a random conjugation of the verb. Produces 2 cards.", 
    "form":  """
        <label for='pt_inf'>PT 🇵🇹 Infinitive</label>
        <input type='text' name='pt_inf' value='{{ pt_inf }}'>

        <label for='eng_inf'>EN 🇬🇧 Infinitive</label>
        <input type='text' name='eng_inf' value='{{ eng_inf }}'>

        <label for='I'>🇬🇧 I..</label>
        <input type='text' name='I' value='{{ I }}'>

        <label for='you'>🇬🇧 You..</label>
        <input type='text' name='you' value='{{ you }}'>

        <label for='he'>🇬🇧 He/She..</label>
        <input type='text' name='he' value='{{ he }}'>

        <label for='eu'>🇵🇹 Eu..</label>
        <input type='text' name='eu' value='{{ eu }}'>

        <label for='tu'>🇵🇹 Tu...</label>
        <input type='text' name='tu' value='{{ tu }}'>

        <label for='ele'>🇵🇹 Você/Ele/Ela</label>
        <input type='text' name='ele' value='{{ ele }}'>

        <label for='nos'>🇵🇹 Nós</label>
        <input type='text' name='nos' value='{{ nos }}'>

        <label for='eles'>🇵🇹 Vocês/Eles/Elas</label>
        <input type='text' name='eles'  value='{{ eles }}'>
    """, 
    "preview":  "🇵🇹 {{ pt_inf }} / 🇬🇧 {{ eng_inf }}", 
    "cards":  {
        'pt_en': "pt, en = random.choice([(eu, I), (tu, you), (ele, he), (nos, you), (eles, you)]); card = {'question': f'🇵🇹 {pt}', 'answer': f'🇬🇧 {en}'}",
        'en_pt': "pt, en = random.choice([(eu, I), (tu, you), (ele, he), (nos, you), (eles, you)]); card = {'question': f'🇬🇧 {en}', 'answer': f'🇵🇹 {pt}'}",
    }
}


{ 
    "name":  "Regular Verb PT 🇵🇹 / IT 🇮🇹", 
    "description":  "The same card and its reverse is rendered with a random conjugation of the verb. Produces 2 cards.", 
    "form":  """
        <label for='pt_inf'>PT 🇵🇹 Infinitive</label>
        <input type='text' name='pt_inf' value='{{ pt_inf }}'>

        <label for='it_inf'>IT 🇮🇹 Infinitive</label>
        <input type='text' name='it_inf' value='{{ it_inf }}'>

        <label for='io'>🇮🇹 Io..</label>
        <input type='text' name='io' value='{{ io }}'>

        <label for='tu_it'>🇮🇹 Tu..</label>
        <input type='text' name='tu_it' value='{{ tu_it }}'>

        <label for='lui'>🇮🇹 Lui/Lei..</label>
        <input type='text' name='lui' value='{{ lui }}'>

        <label for='noi'>🇮🇹 Noi..</label>
        <input type='text' name='noi' value='{{ noi }}'>

        <label for='loro'>🇮🇹 Loro..</label>
        <input type='text' name='loro' value='{{ loro }}'>

        <label for='eu'>🇵🇹 Eu..</label>
        <input type='text' name='eu' value='{{ eu }}'>

        <label for='tu_pt'>🇵🇹 Tu...</label>
        <input type='text' name='tu_pt' value='{{ tu_pt }}'>

        <label for='ele'>🇵🇹 Você/Ele/Ela</label>
        <input type='text' name='ele' value='{{ ele }}'>

        <label for='nos'>🇵🇹 Nós</label>
        <input type='text' name='nos' value='{{ nos }}'>

        <label for='eles'>🇵🇹 Vocês/Eles/Elas</label>
        <input type='text' name='eles'  value='{{ eles }}'>
    """, 
    "preview":  "🇵🇹 {{ pt_inf }} / 🇮🇹 {{ it_inf }}", 
    "cards":  {
        'pt_it': "pt, it = random.choice([(eu, io), (tu_pt, tu_it), (ele, lui), (nos, noi), (eles, loro)]); card = {'question': f'🇵🇹 {pt}', 'answer': f'🇮🇹 {it}'}",
        'it_pt': "pt, it = random.choice([(eu, io), (tu_pt, tu_it), (ele, lui), (nos, noi), (eles, loro)]); card = {'question': f'🇮🇹 {it}', 'answer': f'🇵🇹 {pt}'}",
    },
}