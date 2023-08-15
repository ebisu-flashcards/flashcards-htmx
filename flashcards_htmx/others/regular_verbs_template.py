{ 
    "name":  "Regular Verb 🇵🇹", 
    "description":  "The same card and its reverse is rendered with a random conjugation of the verb. Produces 2 cards.", 
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
        "pt_en": "pt, en = random.choice([(eu, I), (tu, you), (ele, he), (nos, you), (eles, you)]); card = {'question': pt, 'answer': en}",
        "en_pt": "pt, en = random.choice([(eu, I), (tu, you), (ele, he), (nos, you), (eles, you)]); card = {'question': en, 'answer': pt}"
    },
}
