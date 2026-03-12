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
    # Lista de temas para alternar automaticamente e evitar repetição
    temas = [
        "IA generativa para pequenas empresas",
        "O futuro do trabalho com assistentes de IA",
        "Como usar IA para análise de dados de vendas",
        "Segurança de dados na era da inteligência artificial",
        "IA e a personalização da experiência do cliente"
    ]
    tema_escolhido = random.choice(temas)

    prompt = f"""
    Responda APENAS com JSON válido. Sem markdown.
    Crie um post ÚNICO e CRIATIVO sobre o tema: {tema_escolhido}.
    
    Regras:
    1. O título deve ser chamativo e diferente de "Inteligência Artificial nos Negócios".
    2. O excerpt deve ser um resumo curto e instigante.
    3. image_keyword: uma palavra única em INGLÊS que represente o post (ex: 'robot', 'office', 'data').
    4. O conteúdo deve ter pelo menos 3 parágrafos e 1 subtítulo (usando ##).

    Formato:
    {{
      "title": "",
      "excerpt": "",
      "image_keyword": "",
      "content": []
    }}
    """
    
    print(f"Gerando post único sobre: {tema_escolhido}...")
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8 # Aumentado para gerar mais variedade
    )
    
    text = (completion.choices[0].message.content or "").strip()
    text = text.replace("```json", "").replace("```", "").strip()
    
    match = re.search(r"\{.*\}", text, re.S)
    if not match: 
        raise ValueError("A IA não retornou um JSON válido.")
        
    return json.loads(match.group(0))

def save_post(post):
    if not os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "w", encoding="utf-8") as f: 
            json.dump([], f)
            
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        try: 
            posts = json.load(f)
        except: 
            posts = []

    # Gerador de imagem usando um serviço estável (Unsplash via API direta de busca)
    keyword = post.get("image_keyword", "technology").lower()
    # Usando um ID aleatório na URL para evitar que todos os posts usem a mesma foto
    random_id = random.randint(1, 1000)
    image_url = f"https://images.unsplash.com/photo-{random_id}?auto=format&fit=crop&w=800&q=80&sig={random_id}&{keyword}"

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
    
    # Adiciona no início da lista
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
        print(f"❌ Erro durante o processo: {e}")

if __name__ == "__main__":
    main()