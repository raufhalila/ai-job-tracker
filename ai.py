import requests

def generate_cover_letter(title, company):
    prompt = f"""
    Write a short, enthusiastic and professional cover letter for a job application.
    The position is '{title}' at the company '{company}'. Mention interest, value, and a strong closing line.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )

    return response.json()["response"]
