async function renderSinglePost() {
  const container = document.getElementById("post-content");
  if (!container) return;

  const params = new URLSearchParams(window.location.search);
  const slug = params.get("slug");

  if (!slug) return;

  try {
    const posts = await fetchPosts();
    const post = posts.find((item) => item.slug === slug);

    if (!post) return;

    // SEO: Atualiza o título da aba e a meta descrição
    document.title = `${post.title} | Pulse Blog`;
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription) {
      metaDescription.setAttribute("content", post.excerpt);
    }

    const paragraphs = post.content
      .map((paragraph) => {
        if (paragraph.startsWith("## ")) {
          return `<h2>${paragraph.replace("## ", "")}</h2>`;
        }
        return `<p>${paragraph}</p>`;
      })
      .join("");

    container.innerHTML = `
      <div class="article-meta">
        <span>${post.category}</span>
        <span>${post.date}</span>
        <span>${post.author}</span>
      </div>
      <h1>${post.title}</h1>
      <p class="article-lead">${post.excerpt}</p>
      <img class="post-cover" src="${post.coverImage}" alt="${post.title}">
      <div class="article-body">${paragraphs}</div>
    `;
  } catch (error) {
    console.error("Erro no SEO/Renderização:", error);
  }
}

renderSinglePost();