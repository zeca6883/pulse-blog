import os
import json
import re
from datetime import datetime
from slugify import slugify
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("ERRO: GROQ_API_KEY não encontrada.")

client = Groq(api_key=api_key)
POSTS_FILE = "../posts.json"

def generate_post():
    prompt = """
Responda APENAS com JSON válido. Sem markdown.
Formato:
{
  "title": "",
  "excerpt": "",
  "image_keyword": "palavra_chave_em_ingles",
  "content": ["parágrafo", "## subtítulo", "parágrafo"]
}
Tema: inteligência artificial aplicada a negócios.
"""
    print("Gerando post e escolhendo imagem...")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    text = (completion.choices[0].message.content or "").strip()
    text = text.replace("```json", "").replace("```", "").strip()
    match = re.search(r"\{.*\}", text, re.S)
    if not match: raise ValueError("JSON inválido")
    return json.loads(match.group(0))

def save_post(post):
    if not os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "w", encoding="utf-8") as f: json.dump([], f)
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        try: posts = json.load(f)
        except: posts = []

    # Monta a URL da imagem usando a palavra-chave da IA
    keyword = post.get("image_keyword", "technology")
    image_url = f"https://images.unsplash.com/photo-1?auto=format&fit=crop&w=800&q=80&keywords={keyword}"

    new_post = {
        "id": max((p.get("id", 0) for p in posts), default=0) + 1,
        "slug": slugify(post["title"]),
        "title": post["title"].strip(),
        "excerpt": post["excerpt"].strip(),
        "category": "IA",
        "date": datetime.now().strftime("%d %b %Y"),
        "author": "AI Writer",
        "coverImage": image_url, # Agora usa a URL externa
        "content": [str(item).strip() for item in post["content"] if str(item).strip()]
    }
    posts.insert(0, new_post)
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    return new_post

def main():
    try:
        post = generate_post()
        saved = save_post(post)
        print(f"✅ Sucesso: {saved['title']}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()