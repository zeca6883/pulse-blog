import json
import re
from datetime import datetime
from slugify import slugify
from groq import Groq

# coloque sua chave aqui
client = Groq(api_key="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")

POSTS_FILE = "../posts.json"


def generate_post():

    prompt = """
Responda APENAS com JSON válido.

Formato:
{
"title": "",
"excerpt": "",
"content": [
"parágrafo",
"## subtítulo",
"parágrafo",
"parágrafo"
]
}

Tema: inteligência artificial aplicada a negócios.
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    text = completion.choices[0].message.content.strip()

    # remove markdown caso venha
    text = text.replace("```json", "").replace("```", "")

    match = re.search(r"\{.*\}", text, re.S)

    if not match:
        raise ValueError("Resposta da IA não contém JSON válido")

    json_text = match.group(0)

    return json.loads(json_text)


def save_post(post):

    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    new_id = max(p["id"] for p in posts) + 1

    slug = slugify(post["title"])

    new_post = {
        "id": new_id,
        "slug": slug,
        "title": post["title"],
        "excerpt": post["excerpt"],
        "category": "IA",
        "date": datetime.now().strftime("%d %b %Y"),
        "author": "AI Writer",
        "coverImage": "assets/hero-illustration.svg",
        "content": post["content"]
    }

    posts.insert(0, new_post)

    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    return new_post


def main():

    post = generate_post()

    saved = save_post(post)

    print("Post criado com sucesso!")
    print("Título:", saved["title"])
    print("Slug:", saved["slug"])


if __name__ == "__main__":
    main()