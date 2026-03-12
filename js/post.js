async function renderSinglePost() {
  const container = document.getElementById("post-content");
  if (!container) return;

  const params = new URLSearchParams(window.location.search);
  const slug = params.get("slug");

  if (!slug) {
    container.innerHTML = `
      <h1>Post nao encontrado</h1>
      <p class="article-lead">O link informado nao possui um slug valido.</p>
    `;
    return;
  }

  try {
    const posts = await fetchPosts();
    const post = posts.find((item) => item.slug === slug);

    if (!post) {
      container.innerHTML = `
        <h1>Post nao encontrado</h1>
        <p class="article-lead">Nao localizamos o conteudo solicitado.</p>
      `;
      return;
    }

    document.title = `${post.title} | Pulse Blog`;
    updateMetaDescription(post.excerpt);

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
    container.innerHTML = `
      <h1>Erro ao carregar</h1>
      <p class="article-lead">Nao foi possivel buscar o conteudo do post.</p>
    `;
  }
}

renderSinglePost();
