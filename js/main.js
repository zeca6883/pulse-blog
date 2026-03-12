function setupResponsiveMenu() {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".site-nav");

  if (!toggle || !nav) return;

  toggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });
}

async function fetchPosts() {
  const response = await fetch("posts.json");

  if (!response.ok) {
    throw new Error("Nao foi possivel carregar os posts.");
  }

  return response.json();
}

function createPostCard(post) {
  return `
    <article class="post-card">
      <img class="post-cover" src="${post.coverImage}" alt="${post.title}">
      <div class="post-card-content">
        <div class="post-card-meta">
          <span>${post.category}</span>
          <span>${post.date}</span>
        </div>
        <h3>${post.title}</h3>
        <p>${post.excerpt}</p>
        <a href="post.html?slug=${post.slug}">Ler post</a>
      </div>
    </article>
  `;
}

function updateMetaDescription(description) {
  const meta = document.querySelector('meta[name="description"]');

  if (meta) {
    meta.setAttribute("content", description);
  }
}

setupResponsiveMenu();
