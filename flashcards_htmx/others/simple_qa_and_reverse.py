{ 
    "name":  "PT 🇵🇹 to EN 🇬🇧 with reverse", 
    "description":  "Generates two cards: 🇵🇹 -> 🇬🇧 and 🇬🇧 -> 🇵🇹 ", 
    "form": """
            <label for='question'>PT 🇵🇹</label>
            <input type='text' name='question' value='{{ question }}'>

            <label for='answer'>EN 🇬🇧</label>
            <input type='text' name='answer'  value='{{ answer }}'>
    """, 
    "preview":  "🇵🇹 {{ question }} <-> 🇬🇧 {{ answer }}", 
    "cards":  {
        'direct': {'question': '🇵🇹 {{ question }}', 'answer': '{{ answer }} '},
        'reverse': {'question': '🇬🇧 {{ answer }}', 'answer': '{{ question }}'},
    },
}

{ 
    "name":  "PT 🇵🇹 to EN 🇬🇧 ", 
    "description":  "Generates one cards: 🇵🇹 -> 🇬🇧 ", 
    "form": """
        <label for='question'>PT 🇵🇹</label>
        <input type='text' name='question' value='{{ question }}'>

        <label for='answer'>EN 🇬🇧</label>
        <input type='text' name='answer'  value='{{ answer }}'>
    """, 
    "preview":  "🇵🇹 {{ question }} -> 🇬🇧 {{ answer }}", 
    "cards":  {
        'card': {'question': '🇵🇹 {{ question }}', 'answer': '{{ answer }} '},
    },
}

{ 
    "name":  "EN 🇬🇧 to PT 🇵🇹", 
    "description":  "Generates one card:  🇬🇧 -> 🇵🇹", 
    "form": """
            <label for='question'>EN 🇬🇧</label>
            <input type='text' name='question' value='{{ question }}'>

            <label for='answer'>PT 🇵🇹</label>
            <input type='text' name='answer'  value='{{ answer }}'>
        """, 
    "preview":  "🇬🇧 {{ question }} -> 🇵🇹 {{ answer }}", 
    "cards":  {
        'card': {'question': '🇬🇧 {{ question }}', 'answer': '{{ answer }} '},
    },
}

{ 
    "name":  "PT 🇵🇹 to IT 🇮🇹 with reverse", 
    "description":  "Generates two cards: 🇵🇹 -> 🇮🇹 and 🇮🇹 -> 🇵🇹 ", 
    "form":  """
                <label for='question'>PT 🇵🇹</label>
                <input type='text' name='question' value='{{ question }}'>

                <label for='answer'>IT 🇮🇹</label>
                <input type='text' name='answer'  value='{{ answer }}'>
    """, 
    "preview":  "🇵🇹 {{ question }} <->  🇮🇹 {{ answer }}", 
    "cards":  {
        'direct': {'question': '🇵🇹 {{ question }}', 'answer': '{{ answer }} '},
        'reverse': {'question': '🇮🇹 {{ answer }}', 'answer': '{{ question }}'},
    },
}

{ 
    "name":  "PT 🇵🇹 to IT 🇮🇹", 
    "description":  "Generates one card: 🇵🇹 -> 🇮🇹", 
    "form":  """
            <label for='question'>PT 🇵🇹</label>
            <input type='text' name='question' value='{{ question }}'>

            <label for='answer'>IT 🇮🇹</label>
            <input type='text' name='answer'  value='{{ answer }}'>
        """, 
    "preview":  "🇵🇹 {{ question }} <->  🇮🇹 {{ answer }}", 
    "cards":  {
        'card': {'question': '🇵🇹 {{ question }}', 'answer': '{{ answer }} '},
    },
}

{ 
    "name":  "IT 🇮🇹 to PT 🇵🇹", 
    "description":  "Generates one card: 🇮🇹 -> 🇵🇹", 
    "form":  """
        <label for='question'>IT 🇮🇹</label>
        <input type='text' name='question' value='{{ question }}'>

        <label for='answer'>PT 🇵🇹</label>
        <input type='text' name='answer' value='{{ answer }}'>
    """, 
    "preview":  "🇮🇹 {{ question }} <-> 🇵🇹 {{ answer }}", 
    "cards":  {
        'card': {'question': '🇮🇹 {{ question }}', 'answer': '{{ answer }} '},
    },
}