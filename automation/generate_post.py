def save_post(post):
    if not os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "w", encoding="utf-8") as f: 
            json.dump([], f)
            
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        try: 
            posts = json.load(f)
        except: 
            posts = []

    # Ajuste na URL para garantir que o Unsplash retorne uma imagem real
    keyword = post.get("image_keyword", "technology").replace(" ", ",")
    image_url = f"https://source.unsplash.com/featured/800x450?{keyword}"

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