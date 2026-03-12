import os
import json
import re
import random
from datetime import datetime
from slugify import slugify
from groq import Groq

# Configuração de Segurança
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("ERRO: GROQ_API_KEY não encontrada. Verifique as variáveis de ambiente.")

client = Groq(api_key=api_key)
POSTS_FILE = "../posts.json"

def generate_post():
    # Temas variados para evitar repetição
    temas = [
        "O impacto da IA na produtividade empresarial",
        "Como a IA generativa está a mudar o marketing digital",
        "Automação inteligente: o futuro dos processos de negócio",
        "Análise de dados e IA: tomadas de decisão mais rápidas",
        "Cibersegurança e Inteligência Artificial"
    ]
    tema_escolhido = random.choice(temas)

    prompt = f"""
    Responda APENAS com JSON válido. Sem markdown.
    Crie um post ÚNICO sobre o tema: {tema_escolhido}.
    
    Formato:
    {{
      "title": "",
      "excerpt": "",
      "content": ["parágrafo", "## subtítulo", "parágrafo"]
    }}
    """
    
    print(f"Gerando conteúdo sobre: {tema_escolhido}...")
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
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

    # NOVO GERADOR DE IMAGEM: Picsum Photos (Usa um ID aleatório de 1 a 1000)
    img_id = random.randint(1, 1000)
    image_url = f"https://picsum.photos/id/{img_id}/800/450"

    new_post = {
        "id": max((p.get("id", 0) for p in posts), default=0) + 1,
        "slug": slugify(post["title"]),
        "title": post["title"].strip(),
        "excerpt": post["excerpt"].strip(),
        "category": "IA",
        "date": datetime.now().strftime("%d %b %Y"),
        "author": "AI Writer",
        "coverImage": image_url,
        "content": [str(item).strip() for item in post["content"] if str(item).strip()]
    }
    
    posts.insert(0, new_post)
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    return new_post

def main():
    try:
        post_data = generate_post()
        saved = save_post(post_data)
        print(f"✅ Post criado com sucesso: {saved['title']}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()