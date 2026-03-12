async function renderFeaturedPosts() {
  const grid = document.getElementById("featured-posts-grid");
  if (!grid) return;

  try {
    const posts = await fetchPosts();
    const featured = posts.slice(0, 3);

    grid.innerHTML = featured.map(createPostCard).join("");
  } catch (error) {
    grid.innerHTML = "<p>Os posts nao puderam ser carregados agora.</p>";
  }
}

renderFeaturedPosts();
