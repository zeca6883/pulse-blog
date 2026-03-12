const POSTS_PER_PAGE = 4;

async function renderPostsPage() {
  const grid = document.getElementById("posts-grid");
  const searchInput = document.getElementById("search-input");
  const pagination = document.getElementById("pagination");
  const resultsCount = document.getElementById("results-count");
  const emptyState = document.getElementById("empty-state");

  if (!grid || !searchInput || !pagination || !resultsCount || !emptyState) return;

  let allPosts = [];
  let filteredPosts = [];
  let currentPage = 1;

  function getFilteredPosts(term) {
    const normalizedTerm = term.trim().toLowerCase();

    if (!normalizedTerm) return allPosts;

    return allPosts.filter((post) => {
      const searchableText = [
        post.title,
        post.excerpt,
        post.category,
        post.author,
        post.content.join(" ")
      ].join(" ").toLowerCase();

      return searchableText.includes(normalizedTerm);
    });
  }

  function renderPagination(totalPages) {
    pagination.innerHTML = "";

    if (totalPages <= 1) return;

    for (let page = 1; page <= totalPages; page += 1) {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = String(page);

      if (page === currentPage) {
        button.classList.add("active");
      }

      button.addEventListener("click", () => {
        currentPage = page;
        renderCurrentPage();
      });

      pagination.appendChild(button);
    }
  }

  function renderCurrentPage() {
    const totalPages = Math.ceil(filteredPosts.length / POSTS_PER_PAGE) || 1;
    const start = (currentPage - 1) * POSTS_PER_PAGE;
    const pageItems = filteredPosts.slice(start, start + POSTS_PER_PAGE);

    grid.innerHTML = pageItems.map(createPostCard).join("");
    emptyState.hidden = filteredPosts.length !== 0;
    resultsCount.textContent = `${filteredPosts.length} post(s) encontrado(s)`;
    renderPagination(totalPages);
  }

  try {
    allPosts = await fetchPosts();
    filteredPosts = allPosts;
    renderCurrentPage();

    searchInput.addEventListener("input", (event) => {
      currentPage = 1;
      filteredPosts = getFilteredPosts(event.target.value);
      renderCurrentPage();
    });
  } catch (error) {
    grid.innerHTML = "<p>Falha ao carregar os posts.</p>";
    resultsCount.textContent = "";
  }
}

renderPostsPage();
