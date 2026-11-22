const money = value => value == null ? "—" : "₹" + Number(value).toLocaleString("en-IN", {maximumFractionDigits:2});
async function getJSON(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  return response.json();
}
async function loadSummary() {
  const d = await getJSON("/api/analytics/summary/");
  document.getElementById("total").textContent = d.total_products;
  document.getElementById("avg-price").textContent = money(d.average_price);
  document.getElementById("median-price").textContent = money(d.median_price);
  document.getElementById("avg-rating").textContent = d.average_rating ?? "—";
  document.getElementById("reviews").textContent = Number(d.total_reviews).toLocaleString("en-IN");
}
function drawBars(targetId, rows, labelKey, valueKey) {
  const target = document.getElementById(targetId);
  target.innerHTML = "";
  const max = Math.max(1, ...rows.map(x => Number(x[valueKey])));
  rows.forEach(row => {
    const line = document.createElement("div"); line.className = "bar-row";
    const label = document.createElement("span"); label.textContent = row[labelKey];
    const bg = document.createElement("div"); bg.className = "bar-bg";
    const bar = document.createElement("div"); bar.className = "bar";
    bar.style.width = `${Number(row[valueKey]) / max * 100}%`; bg.appendChild(bar);
    const count = document.createElement("b"); count.textContent = row[valueKey];
    line.append(label,bg,count); target.appendChild(line);
  });
}
async function loadCategories() {
  const d = await getJSON("/api/analytics/categories/");
  drawBars("categories", d.results, "category", "product_count");
  const select = document.getElementById("category");
  const selected = select.value;
  select.innerHTML = '<option value="">All categories</option>';
  d.results.forEach(row => { const option=document.createElement("option");option.value=row.category;option.textContent=row.category;select.appendChild(option); });
  select.value = selected;
}
async function loadPrices() {
  const d = await getJSON("/api/analytics/price-distribution/");
  drawBars("prices", d.results, "range", "count");
}
async function loadProducts() {
  const params = new URLSearchParams();
  const search = document.getElementById("search").value.trim();
  const category = document.getElementById("category").value;
  if (search) params.set("search", search);
  if (category) params.set("category", category);
  params.set("ordering", document.getElementById("ordering").value);
  const d = await getJSON("/api/products/?" + params.toString());
  const body = document.getElementById("products"); body.innerHTML = "";
  d.results.forEach(p => {
    const tr = document.createElement("tr");
    [p.name,p.category,money(p.price),p.rating ?? "Unrated",Number(p.review_count).toLocaleString("en-IN")].forEach(value => {
      const td=document.createElement("td");td.textContent=value;tr.appendChild(td);
    });
    body.appendChild(tr);
  });
  document.getElementById("status").textContent = `Showing ${d.results.length} of ${d.count} products.`;
}
async function loadTopRated() {
  const d = await getJSON("/api/analytics/top-rated/");
  const target = document.getElementById("top-rated"); target.innerHTML = "";
  d.results.slice(0,6).forEach(p => {
    const item=document.createElement("div");item.className="top-item";
    const name=document.createElement("strong");name.textContent=p.name;
    const detail=document.createElement("small");detail.textContent=`${p.category} • ${p.rating}/5 • ${p.review_count} reviews`;
    item.append(name,detail);target.appendChild(item);
  });
}
async function refreshAll() {
  try {
    await Promise.all([loadSummary(),loadCategories(),loadPrices(),loadProducts(),loadTopRated()]);
  } catch (error) { document.getElementById("status").textContent = "Could not load dashboard. Check server and database."; console.error(error); }
}
let searchTimer;
document.getElementById("search").addEventListener("input",()=>{clearTimeout(searchTimer);searchTimer=setTimeout(loadProducts,250);});
document.getElementById("category").addEventListener("change",loadProducts);
document.getElementById("ordering").addEventListener("change",loadProducts);
document.getElementById("refresh").addEventListener("click",refreshAll);
refreshAll();
