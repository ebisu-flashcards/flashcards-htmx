{ 
    "name":  "Irregular Verb PT 🇵🇹 / EN 🇬🇧", 
    "description":  "Creates a card for each conjugation of the verb and their reverse. Generates 10 cards.", 
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
        'eu': {'question': '🇵🇹 {{ eu }}', 'answer': 'I {{ I }}'},
        'tu': {'question': '🇵🇹 {{ tu }}', 'answer': 'You {{ you }}'},
        'ele': {'question': '🇵🇹 {{ ele }}', 'answer': 'He/She {{ he }}'},
        'nos': {'question': '🇵🇹 {{ nos }}', 'answer': 'We {{ you }}'},
        'eles': {'question': '🇵🇹 {{ eles }}', 'answer': 'They {{ you }}'},
        'I': {'question': '🇬🇧 I {{ I }}', 'answer': '{{ eu }}'},
        'you': {'question': '🇬🇧 You {{ you }}', 'answer': '{{ tu }}'},
        'he': {'question': '🇬🇧 He/She {{ he }}', 'answer': '{{ ele }}'},
        'we': {'question': '🇬🇧 We {{ you }}', 'answer': '{{ nos }}'},
        'they': {'question': '🇬🇧 They {{ you }}', 'answer': '{{ eles }}'},
    },
}


{ 
    "name":  "Irregular Verb PT 🇵🇹 / IT 🇮🇹", 
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
        'eu': {'question': '🇵🇹 {{ eu }}', 'answer': '{{ io }}'},
        'tu_pt': {'question': '🇵🇹 {{ tu_pt }}', 'answer': '{{ tu_it }}'},
        'ele': {'question': '🇵🇹 {{ ele }}', 'answer': '{{ lui }}'},
        'nos': {'question': '🇵🇹 {{ nos }}', 'answer': '{{ noi }}'},
        'eles': {'question': '🇵🇹 {{ eles }}', 'answer': '{{ loro }}'},
        'io': {'question': '🇮🇹 {{ io }}', 'answer': '{{ eu }}'},
        'tu_it': {'question': '🇮🇹 {{ tu_it }}', 'answer': '{{ tu_pt }}'},
        'lui': {'question': '🇮🇹 {{ lui }}', 'answer': '{{ ele }}'},
        'noi': {'question': '🇮🇹 {{ noi }}', 'answer': '{{ nos }}'},
        'loro': {'question': '🇮🇹 {{ loro }}', 'answer': '{{ eles }}'},
    },
}