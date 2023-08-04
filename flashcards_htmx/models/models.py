"""
Data structure:

{
    "templates": {
        "Q/A": {
            "question": "{{ word }}"
            "answer": "{{ word }}"
            "preview": "{{ question }} -> {{ answer }}"
        }
    }
    "decks": {
        "0": {
            "name": "Deck 0",
            "description": "Description for deck 0",
            "algorithm": "Random",
            "cards": {
                "0": {
                    "type": "Q/A",
                    "tags": ["tag 0"],
                    "question_data": {
                        "word": "Question 0",
                        "example": "Example 0",
                    }
                    "answer_data": {
                        "word": "Answer 0",
                        "context": "Some context"
                    }
                    "preview_data": {
                        "question: "Question 0",
                        "answer": "Answer 0"
                    }
                    "reviews: {
                        "0": { 
                            "date": "2021-01-01",
                            "result: "Correct"
                        }
                    }
                },
                "1": { ... }
            }   
        },
        "1": { ... }
    }
}
"""
