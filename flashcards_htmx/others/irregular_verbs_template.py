{ 
    "name":  "Irregular Verb 🇵🇹", 
    "description":  "Creates a card for each conjugation of the verb and their reverse. Generates 10 cards.", 
    "form": """
        <label for='pt_inf'>Portuguese Infinitive</label>
        <input type='text' name='pt_inf' value={{ pt_inf }}>

        <label for='eng_inf'>English Infinitive</label>
        <input type='text' name='eng_inf' value={{ eng_inf }}>

        <label for='I'>I..</label>
        <input type='text' name='I' value={{ I }}>

        <label for='you'>You..</label>
        <input type='text' name='you' value={{ you }}>

        <label for='he'>He/She..</label>
        <input type='text' name='he' value={{ he }}>

        <label for='eu'>Eu..</label>
        <input type='text' name='eu' value={{ eu }}>

        <label for='tu'>Tu...</label>
        <input type='text' name='tu' value={{ tu }}>

        <label for='ele'>Você/Ele/Ela</label>
        <input type='text' name='ele' value={{ ele }}>

        <label for='nos'>Nós</label>
        <input type='text' name='nos' value={{ nos }}>

        <label for='eles'>Vocês/Eles/Elas</label>
        <input type='text' name='eles'  value={{ eles }}>
    """, 
    "preview":  "{{ pt_inf }}  ({{ eng_inf }})", 
    "cards":  {
        'eu': {'question': '{{ eu }}', 'answer': 'I {{ I }}'},
        'tu': {'question': '{{ tu }}', 'answer': 'You {{ you }}'},
        'ele': {'question': '{{ ele }}', 'answer': 'He/She {{ he }}'},
        'nos': {'question': '{{ nos }}', 'answer': 'We {{ you }}'},
        'eles': {'question': '{{ eles }}', 'answer': 'They {{ you }}'},
        'I': {'question': 'I {{ I }}', 'answer': '{{ eu }}'},
        'you': {'question': 'You {{ you }}', 'answer': '{{ tu }}'},
        'he': {'question': 'He/She {{ he }}', 'answer': '{{ ele }}'},
        'we': {'question': 'We {{ you }}', 'answer': '{{ nos }}'},
        'they': {'question': 'They {{ you }}', 'answer': '{{ eles }}'},
    },
}
