import os
import json
import re
import random
import time
from datetime import datetime
from slugify import slugify
from groq import Groq

# =========================
# Configuração
# =========================
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("ERRO: GROQ_API_KEY não encontrada.")

client = Groq(api_key=api_key)
POSTS_FILE = "../posts.json"

# Stopwords simples para filtrar palavras pouco úteis
STOPWORDS_PT = {
    "a", "o", "e", "é", "de", "da", "do", "das", "dos", "em", "no", "na",
    "nos", "nas", "um", "uma", "uns", "umas", "para", "por", "com", "sem",
    "sobre", "como", "mais", "menos", "que", "se", "ao", "à", "às", "os",
    "as", "ou", "ser", "sua", "seu", "suas", "seus", "já", "não", "sim",
    "entre", "até", "após", "antes", "durante", "isso", "essa", "esse",
    "essas", "esses", "real", "valor", "futuro", "guia", "prático"
}

# Mapeamento de temas para tags visuais melhores para busca de imagem
TOPIC_IMAGE_MAP = {
    "agentes": ["artificial-intelligence", "technology", "automation", "robot"],
    "ia": ["artificial-intelligence", "technology", "digital"],
    "inteligencia": ["artificial-intelligence", "technology", "digital"],
    "automacao": ["automation", "workflow", "office", "technology"],
    "processos": ["workflow", "office", "business", "technology"],
    "seo": ["marketing", "analytics", "laptop", "digital"],
    "seguranca": ["cybersecurity", "computer", "code", "technology"],
    "cibernetica": ["cybersecurity", "computer", "code", "technology"],
    "design": ["design", "creative", "workspace", "modern"],
    "sites": ["website", "design", "laptop", "digital"],
    "dados": ["data", "analytics", "dashboard", "technology"],
    "data": ["data", "analytics", "dashboard", "technology"],
    "science": ["data", "analytics", "dashboard", "technology"],
    "negocios": ["business", "office", "meeting", "startup"],
    "empresa": ["business", "office", "startup", "team"],
    "empresas": ["business", "office", "startup", "team"],
    "marketing": ["marketing", "laptop", "office", "digital"],
    "produtividade": ["productivity", "workspace", "laptop", "minimalist"],
    "chatbot": ["artificial-intelligence", "chat", "technology", "computer"],
    "machine": ["machine-learning", "code", "technology", "computer"],
    "aprendizado": ["machine-learning", "code", "technology", "computer"],
    "interface": ["interface", "design", "technology", "modern"],
    "ux": ["design", "interface", "workspace", "creative"],
    "startup": ["startup", "office", "technology", "team"]
}

TITLE_STYLES = [
    "provocativo",
    "estratégico",
    "analítico",
    "visionário",
    "direto",
    "storytelling executivo",
    "comparativo",
    "orientado a tendências",
    "orientado a resultados",
    "futurista"
]


def normalize_text(text: str) -> str:
    text = slugify(text or "").replace("-", " ")
    return text.lower().strip()


def extract_keywords(post: dict, max_keywords: int = 5):
    """
    Extrai palavras-chave relevantes do título, excerpt e conteúdo.
    """
    raw_parts = [
        post.get("title", ""),
        post.get("excerpt", ""),
        " ".join(post.get("content", []))
    ]
    full_text = normalize_text(" ".join(raw_parts))
    words = re.findall(r"\b[a-z]{4,}\b", full_text)

    freq = {}
    for word in words:
        if word in STOPWORDS_PT:
            continue
        freq[word] = freq.get(word, 0) + 1

    sorted_words = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return [word for word, _ in sorted_words[:max_keywords]]


def build_image_tags(post: dict):
    """
    Gera tags mais coerentes para a imagem com base no conteúdo.
    """
    keywords = extract_keywords(post, max_keywords=8)

    visual_tags = []
    for word in keywords:
        if word in TOPIC_IMAGE_MAP:
            for tag in TOPIC_IMAGE_MAP[word]:
                if tag not in visual_tags:
                    visual_tags.append(tag)

    # fallback caso não encontre nada muito bom
    if not visual_tags:
        visual_tags = ["technology", "business", "modern"]

    # limita para não ficar exagerado
    visual_tags = visual_tags[:3]

    # adiciona uma tag complementar visual para mais variedade
    complementares = ["workspace", "digital", "minimalist", "innovation", "office"]
    extra = random.choice(complementares)
    if extra not in visual_tags:
        visual_tags.append(extra)

    return visual_tags[:4]

def generate_post():
    temas = [
        "A revolução dos Agentes de IA no fluxo de trabalho",
        "Como a automação de processos economiza 20h por semana",
        "IA Generativa: além do chat, a criação de valor real",
        "Segurança cibernética baseada em aprendizado de máquina",
        "Otimização de SEO usando modelos de linguagem avançados",
        "Futuro das interfaces: como a IA mudará o design de sites",
        "Data Science para pequenas empresas: guia prático",
        "Como empresas estão criando vantagem competitiva com IA",
        "A nova era da produtividade com copilotos inteligentes",
        "O impacto da IA em marketing, vendas e atendimento",
        "Automação inteligente para operações internas",
        "Como usar IA para escalar conteúdo e reduzir custos",
        "Análise de dados com IA para decisões mais rápidas",
        "Experiência do cliente orientada por inteligência artificial"
    ]

    estilos_titulo = [
        "provocativo",
        "estratégico",
        "curioso",
        "futurista",
        "direto e forte",
        "orientado a negócios",
        "com contraste",
        "com promessa de transformação"
    ]

    estruturas = [
        "artigo analítico",
        "guia prático",
        "texto com visão estratégica",
        "post com exemplos reais",
        "post em formato de tendências",
        "post com tom provocativo e autoridade"
    ]

    tema_base = random.choice(temas)
    estilo_titulo = random.choice(estilos_titulo)
    estrutura = random.choice(estruturas)
    timestamp = int(time.time())

    prompt = f"""
Responda APENAS com JSON válido. Sem explicações. Sem markdown.
ID criativo único: {timestamp}

Crie um post de blog altamente atrativo, original e persuasivo em português sobre:
TEMA: {tema_base}
ESTILO DE TÍTULO: {estilo_titulo}
FORMATO: {estrutura}

OBJETIVO:
O conteúdo deve fazer o leitor sentir que encontrou algo valioso, atual e inteligente.
O texto precisa prender atenção já no início e dar vontade de continuar lendo até o fim.

REGRAS OBRIGATÓRIAS:

1. TÍTULO
- Crie um título forte, original e menos previsível
- Evite títulos genéricos e repetitivos
- Gere curiosidade, tensão, desejo ou visão de oportunidade
- Não usar sempre padrões como "Como..." ou "O futuro de..."

2. EXCERPT
- Deve ser curto, magnético e convincente
- Soar como chamada de destaque de blog premium
- Máximo de 220 caracteres

3. INTRODUÇÃO
- O primeiro parágrafo deve ter GANCHO FORTE
- Pode começar com:
  - uma mudança de mercado,
  - uma dor empresarial,
  - uma quebra de expectativa,
  - uma oportunidade ignorada,
  - ou uma frase de impacto
- Nunca começar de forma morna ou genérica

4. CONTEÚDO
- JSON com lista em "content"
- Misture parágrafos e subtítulos com ##
- O conteúdo deve ser profundo sem ficar cansativo
- Traga utilidade real, não só opinião vaga
- Incluir:
  - exemplos de aplicação prática
  - implicações de negócio
  - erros comuns
  - oportunidades futuras
  - diferenciais competitivos
- Evite clichês e frases vazias

5. ESTILO
- Tom profissional, moderno e inteligente
- Linguagem clara, elegante e envolvente
- Soar como blog premium de inovação, tecnologia e negócios
- Variar estrutura e ritmo entre execuções

6. FINAL
- O encerramento deve ser forte
- Pode trazer visão de futuro, urgência, reflexão estratégica ou chamada mental para ação
- Não terminar de forma genérica

RETORNE EXATAMENTE NESTE FORMATO:
{{
  "title": "Título único aqui",
  "excerpt": "Resumo magnético aqui",
  "content": [
    "Parágrafo de abertura forte",
    "## Subtítulo",
    "Parágrafo com valor real",
    "## Subtítulo",
    "Parágrafo com exemplo ou insight",
    "## Subtítulo",
    "Parágrafo final marcante"
  ]
}}
"""

    print(f"🚀 Gerando post premium sobre: {tema_base}...")

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.15
    )

    text = (completion.choices[0].message.content or "").strip()
    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError("IA falhou ao retornar JSON válido.")

    data = json.loads(match.group(0))

    if not isinstance(data.get("content"), list):
        raise ValueError("Campo 'content' inválido.")
    if not data.get("title") or not data.get("excerpt"):
        raise ValueError("JSON sem título ou excerpt.")

    return data


def build_image_url(post: dict):
    """
    Cria URL de imagem mais coerente com o conteúdo do post.
    """
    tags = build_image_tags(post)
    tag_string = ",".join(tags)
    random_sig = random.randint(1, 100000)

    # Pode trocar por outra fonte no futuro, mantendo a lógica de tags
    return f"https://loremflickr.com/800/450/{tag_string}/all?lock={random_sig}"


def save_post(post):
    if not os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        try:
            posts = json.load(f)
        except Exception:
            posts = []

    # evita títulos idênticos
    if any(p.get("title") == post["title"] for p in posts):
        post["title"] += f" ({datetime.now().strftime('%H:%M')})"

    image_url = build_image_url(post)

    new_post = {
        "id": max((p.get("id", 0) for p in posts), default=0) + 1,
        "slug": slugify(post["title"]),
        "title": post["title"].strip(),
        "excerpt": post["excerpt"].strip(),
        "category": "Inovação",
        "date": datetime.now().strftime("%d %b %Y"),
        "author": "Pulse AI Writer",
        "coverImage": image_url,
        "content": [str(item).strip() for item in post["content"]]
    }

    posts.insert(0, new_post)

    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    return new_post


if __name__ == "__main__":
    try:
        data = generate_post()
        saved = save_post(data)

        print(f"✅ Post Criado: {saved['title']}")
        print(f"🖼️ Imagem: {saved['coverImage']}")
    except Exception as e:
        print(f"❌ Erro: {e}")