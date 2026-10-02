/* QA Affiliate Admin — vanilla JS SPA. Pure fetch, no frameworks. */
(function () {
  "use strict";

  var $ = function (id) { return document.getElementById(id); };
  var state = { page: 1, perPage: 20, totalPages: 1, importFormat: "json", categories: [] };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---------- API helper ---------- */
  function api(method, path, body) {
    var opts = { method: method, credentials: "same-origin", headers: {} };
    if (body !== undefined) { opts.headers["Content-Type"] = "application/json"; opts.body = JSON.stringify(body); }
    return fetch(path, opts).then(function (res) {
      if (res.status === 401) { sessionExpired(); return Promise.reject({ auth: true }); }
      return res.json().then(function (data) {
        if (!res.ok) throw new Error((data && (data.error || data.message)) || ("Request failed (" + res.status + ")"));
        return data;
      });
    });
  }
  function sessionExpired() {
    showView("login");
    var e = $("login-error");
    e.textContent = "Session expired — please sign in again.";
    e.hidden = false;
  }

  /* ---------- views / tabs ---------- */
  function showView(which) {
    $("view-login").hidden = which !== "login";
    $("view-dashboard").hidden = which !== "dashboard";
  }
  function showTab(name) {
    document.querySelectorAll(".tab").forEach(function (t) { t.classList.toggle("active", t.dataset.tab === name); });
    document.querySelectorAll(".panel").forEach(function (p) { p.hidden = p.id !== "tab-" + name; });
    if (name === "overview") loadStats();
    if (name === "products") loadProducts();
  }
  document.querySelectorAll(".tab").forEach(function (t) {
    t.addEventListener("click", function () { showTab(t.dataset.tab); });
  });

  /* ---------- login / logout ---------- */
  $("login-form").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var err = $("login-error"); err.hidden = true;
    var btn = $("login-btn"); btn.disabled = true; btn.textContent = "Signing in…";
    api("POST", "/api/admin/login", { u: $("login-user").value, p: $("login-pass").value })
      .then(function (d) {
        if (d && d.ok) { $("login-pass").value = ""; showView("dashboard"); showTab("overview"); }
        else throw new Error((d && (d.error || d.message)) || "Invalid username or password.");
      })
      .catch(function (e) {
        if (e && e.auth) return;
        err.textContent = e.message || "Login failed."; err.hidden = false;
      })
      .finally(function () { btn.disabled = false; btn.textContent = "Sign In"; });
  });

  $("logout-btn").addEventListener("click", function () {
    api("POST", "/api/admin/logout").catch(function () {}).finally(function () { showView("login"); });
  });

  /* ---------- overview ---------- */
  function barRows(counts) {
    var keys = Object.keys(counts || {}).sort(function (a, b) { return counts[b] - counts[a]; });
    var max = keys.length ? counts[keys[0]] : 1;
    return keys.map(function (k) {
      return '<div class="bar-row"><span class="name">' + esc(k) + '</span>' +
        '<div class="bar-track"><div class="bar-fill" style="width:' + Math.max(2, Math.round(counts[k] / max * 100)) + '%"></div></div>' +
        '<span class="count">' + esc(counts[k]) + '</span></div>';
    }).join("");
  }
  function loadStats() {
    api("GET", "/api/admin/stats").then(function (d) {
      var s = d.stats || d.data || d;
      var total = s.total_products || s.total || s.count || 0;
      var cats = s.by_category || s.categories || {};
      var merch = s.by_merchant || s.merchants || {};
      var newest = s.newest || s.latest || [];
      state.categories = Object.keys(cats).sort();
      fillCategorySelects();
      $("stats-cards").innerHTML =
        '<div class="stat"><strong>' + esc(total) + '</strong><span>Total products</span></div>' +
        '<div class="stat"><strong>' + esc(Object.keys(cats).length) + '</strong><span>Categories</span></div>' +
        '<div class="stat"><strong>' + esc(Object.keys(merch).length) + '</strong><span>Merchants</span></div>';
      $("stats-cats").innerHTML = barRows(cats) || '<p class="muted">No data.</p>';
      $("stats-merchants").innerHTML = barRows(merch) || '<p class="muted">No data.</p>';
      $("stats-newest").innerHTML = newest.length ? newest.map(function (p) {
        return '<div class="newest-item"><span>' + esc(p.name || p.id) + '</span><span class="date">' + esc(p.updated || "") + '</span></div>';
      }).join("") : '<p class="muted">No products yet.</p>';
    }).catch(function (e) { if (!(e && e.auth)) console.error(e); });
  }

  function fillCategorySelects() {
    var dl = $("category-datalist"); dl.innerHTML = "";
    var sel = $("prod-cat-filter");
    var cur = sel.value;
    sel.innerHTML = '<option value="">All categories</option>';
    state.categories.forEach(function (c) {
      var o = document.createElement("option"); o.value = c; o.textContent = c;
      sel.appendChild(o);
      var d = document.createElement("option"); d.value = c; dl.appendChild(d);
    });
    sel.value = cur;
  }

  /* ---------- products ---------- */
  var MERCHANTS = ["temu", "aliexpress", "amazon"];
  (function () {
    var sel = $("prod-merchant-filter");
    MERCHANTS.forEach(function (m) { var o = document.createElement("option"); o.value = m; o.textContent = m; sel.appendChild(o); });
  })();

  var searchTimer = null;
  $("prod-search").addEventListener("input", function () { clearTimeout(searchTimer); searchTimer = setTimeout(function () { state.page = 1; loadProducts(); }, 350); });
  $("prod-cat-filter").addEventListener("change", function () { state.page = 1; loadProducts(); });
  $("prod-merchant-filter").addEventListener("change", function () { state.page = 1; loadProducts(); });
  $("pager-prev").addEventListener("click", function () { if (state.page > 1) { state.page--; loadProducts(); } });
  $("pager-next").addEventListener("click", function () { if (state.page < state.totalPages) { state.page++; loadProducts(); } });

  function loadProducts() {
    var err = $("products-error"); err.hidden = true;
    var qs = "?page=" + state.page + "&per_page=" + state.perPage + "&limit=" + state.perPage;
    var q = $("prod-search").value.trim();
    if (q) qs += "&q=" + encodeURIComponent(q) + "&search=" + encodeURIComponent(q);
    if ($("prod-cat-filter").value) qs += "&category=" + encodeURIComponent($("prod-cat-filter").value);
    if ($("prod-merchant-filter").value) qs += "&merchant=" + encodeURIComponent($("prod-merchant-filter").value);
    api("GET", "/api/admin/products" + qs).then(function (d) {
      var items = d.products || d.items || d.data || (Array.isArray(d) ? d : []);
      var total = d.total || d.count || items.length;
      state.totalPages = Math.max(1, Math.ceil(total / state.perPage));
      $("products-tbody").innerHTML = items.map(rowHtml).join("") || '<tr><td colspan="6" class="muted">No products found.</td></tr>';
      $("pager-info").textContent = "Page " + state.page + " of " + state.totalPages + " (" + total + " products)";
      bindRowButtons();
    }).catch(function (e) {
      if (e && e.auth) return;
      err.textContent = e.message || "Failed to load products."; err.hidden = false;
    });
  }

  function rowHtml(p) {
    return '<tr>' +
      '<td class="id-cell" title="' + esc(p.id) + '">' + esc(p.id) + '</td>' +
      '<td class="name-cell" title="' + esc(p.name) + '">' + esc(p.name) + '</td>' +
      '<td><span class="pill ' + esc(p.merchant) + '">' + esc(p.merchant) + '</span></td>' +
      '<td><span class="pill cat-pill">' + esc(p.category) + '</span></td>' +
      '<td>' + esc(p.updated || "") + '</td>' +
      '<td class="actions-col"><div class="row-actions">' +
        '<button class="icon-btn act-edit" data-id="' + esc(p.id) + '" title="Edit">' +
          '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.1 2.1 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></button>' +
        '<button class="icon-btn danger act-del" data-id="' + esc(p.id) + '" title="Delete">' +
          '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button>' +
      '</div></td></tr>';
  }

  function bindRowButtons() {
    document.querySelectorAll(".act-edit").forEach(function (b) {
      b.addEventListener("click", function () { openProductModal(b.dataset.id); });
    });
    document.querySelectorAll(".act-del").forEach(function (b) {
      b.addEventListener("click", function () { confirmDialog("Delete product?", 'Delete "' + b.dataset.id + '"? This cannot be undone.', function () { deleteProduct(b.dataset.id); }); });
    });
  }

  /* ---------- product modal ---------- */
  var FIELDS = ["id", "name", "affiliate_url", "image_url", "merchant", "category", "subcategory",
    "short_description", "badges", "pros", "cons", "key_features", "rating", "sold_count",
    "source", "trend_status", "updated", "sample"];
  var ARRAY_FIELDS = ["badges", "pros", "cons", "key_features"];

  function splitList(v) { return String(v || "").split(/[,;\n]/).map(function (s) { return s.trim(); }).filter(Boolean); }

  function openProductModal(id) {
    var err = $("modal-error"); err.hidden = true;
    $("product-form").reset();
    if (id) {
      $("modal-title").textContent = "Edit Product";
      api("GET", "/api/admin/products?id=" + encodeURIComponent(id)).then(function (d) {
        var p = d.product || d.item || (d.products && d.products[0]) || d;
        fillForm(p); $("pf-original-id").value = id;
        $("product-modal").hidden = false;
      }).catch(function (e) {
        if (e && e.auth) return;
        // fall back: fetch from list row? just open empty edit with id prefilled
        $("pf-id").value = id; $("pf-original-id").value = id;
        $("product-modal").hidden = false;
        err.textContent = "Could not load full product record: " + (e.message || "unknown error"); err.hidden = false;
      });
    } else {
      $("modal-title").textContent = "Add Product";
      $("pf-original-id").value = "";
      $("pf-updated").value = new Date().toISOString().slice(0, 10);
      $("product-modal").hidden = false;
    }
  }

  function fillForm(p) {
    FIELDS.forEach(function (f) {
      var el = $("pf-" + f); if (!el) return;
      var v = p[f];
      if (el.type === "checkbox") { el.checked = !!v; }
      else if (ARRAY_FIELDS.indexOf(f) >= 0) { el.value = Array.isArray(v) ? v.join(", ") : (v || ""); }
      else { el.value = v == null ? "" : v; }
    });
  }

  function collectForm() {
    var p = {};
    FIELDS.forEach(function (f) {
      var el = $("pf-" + f); if (!el) return;
      if (el.type === "checkbox") { p[f] = el.checked; }
      else if (f === "rating") { p[f] = el.value === "" ? null : parseFloat(el.value); }
      else if (ARRAY_FIELDS.indexOf(f) >= 0) { p[f] = splitList(el.value); }
      else { p[f] = el.value.trim(); }
    });
    return p;
  }

  function closeModal() { $("product-modal").hidden = true; }
  $("modal-close").addEventListener("click", closeModal);
  $("modal-cancel").addEventListener("click", closeModal);
  $("product-modal").addEventListener("click", function (e) { if (e.target === $("product-modal")) closeModal(); });

  $("add-product-btn").addEventListener("click", function () { openProductModal(null); });

  $("product-form").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var err = $("modal-error"); err.hidden = true;
    var p = collectForm();
    var saveBtn = $("modal-save"); saveBtn.disabled = true; saveBtn.textContent = "Saving…";
    var origId = $("pf-original-id").value;
    var req = origId
      ? api("PUT", "/api/admin/products?id=" + encodeURIComponent(origId), p)
      : api("POST", "/api/admin/products", p);
    req.then(function (d) {
      if (d && d.ok === false) throw new Error(d.error || "Save failed.");
      closeModal(); loadProducts();
    }).catch(function (e) {
      if (e && e.auth) return;
      err.textContent = e.message || "Save failed."; err.hidden = false;
    }).finally(function () { saveBtn.disabled = false; saveBtn.textContent = "Save Product"; });
  });

  function deleteProduct(id) {
    api("DELETE", "/api/admin/products?id=" + encodeURIComponent(id)).then(function (d) {
      if (d && d.ok === false) throw new Error(d.error || "Delete failed.");
      loadProducts();
    }).catch(function (e) {
      if (e && e.auth) return;
      var err = $("products-error"); err.textContent = e.message || "Delete failed."; err.hidden = false;
    });
  }

  /* ---------- confirm dialog ---------- */
  var confirmCb = null;
  function confirmDialog(title, text, cb) {
    $("confirm-title").textContent = title;
    $("confirm-text").textContent = text;
    confirmCb = cb;
    $("confirm-dialog").hidden = false;
  }
  $("confirm-cancel").addEventListener("click", function () { $("confirm-dialog").hidden = true; confirmCb = null; });
  $("confirm-ok").addEventListener("click", function () { $("confirm-dialog").hidden = true; if (confirmCb) { confirmCb(); confirmCb = null; } });

  /* ---------- import ---------- */
  document.querySelectorAll(".seg-btn").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll(".seg-btn").forEach(function (x) { x.classList.remove("active"); });
      b.classList.add("active");
      state.importFormat = b.dataset.format;
      $("import-text").placeholder = state.importFormat === "json"
        ? '[{"id":"…","name":"…","affiliate_url":"…","image_url":"…","merchant":"temu","category":"fashion",…}]'
        : 'id,name,affiliate_url,image_url,merchant,category,subcategory,rating\n"p1","Name","https://…","https://…","temu","fashion","dresses",4.8';
    });
  });
  $("import-file").addEventListener("change", function (e) {
    var f = e.target.files[0]; if (!f) return;
    $("import-filename").textContent = f.name + " (" + Math.round(f.size / 1024) + " KB)";
    var r = new FileReader();
    r.onload = function () { $("import-text").value = r.result; };
    r.readAsText(f);
    if (/\.csv$/i.test(f.name)) {
      state.importFormat = "csv";
      document.querySelectorAll(".seg-btn").forEach(function (x) { x.classList.toggle("active", x.dataset.format === "csv"); });
    }
  });

  function parseCSV(text) {
    var rows = [], row = [], cur = "", inQ = false;
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (inQ) {
        if (c === '"' && text[i + 1] === '"') { cur += '"'; i++; }
        else if (c === '"') { inQ = false; }
        else { cur += c; }
      } else if (c === '"') { inQ = true; }
      else if (c === ",") { row.push(cur); cur = ""; }
      else if (c === "\n" || c === "\r") { if (c === "\r" && text[i + 1] === "\n") i++; row.push(cur); cur = ""; if (row.length > 1 || row[0] !== "") rows.push(row); row = []; }
      else { cur += c; }
    }
    row.push(cur);
    if (row.length > 1 || row[0] !== "") rows.push(row);
    if (!rows.length) return [];
    var headers = rows[0].map(function (h) { return h.trim(); });
    return rows.slice(1).map(function (r) {
      var o = {};
      headers.forEach(function (h, j) { o[h] = (r[j] || "").trim(); });
      ARRAY_FIELDS.forEach(function (f) { if (typeof o[f] === "string") o[f] = splitList(o[f]); });
      if (o.rating === "") delete o.rating; else if (o.rating) o.rating = parseFloat(o.rating);
      return o;
    });
  }

  $("import-run").addEventListener("click", function () {
    var err = $("import-error"); err.hidden = true;
    $("import-report").hidden = true;
    var raw = $("import-text").value.trim();
    if (!raw) { err.textContent = "Paste data or choose a file first."; err.hidden = false; return; }
    var items;
    try {
      if (state.importFormat === "json") {
        items = JSON.parse(raw);
        if (!Array.isArray(items)) throw new Error("JSON must be an array of product objects.");
      } else {
        items = parseCSV(raw);
      }
    } catch (e) { err.textContent = "Could not parse input: " + e.message; err.hidden = false; return; }
    var btn = $("import-run"); btn.disabled = true; btn.textContent = "Importing…";
    api("POST", "/api/admin/import", { format: state.importFormat, items: items }).then(function (d) {
      var added = d.added != null ? d.added : (d.count || 0);
      var skipped = d.skipped || d.errors || [];
      var html = '<p class="ok-line">✓ ' + esc(added) + ' product(s) added.</p>';
      if (skipped.length) {
        html += '<p class="muted">' + skipped.length + ' skipped:</p><ul class="skip-list">' +
          skipped.map(function (s) {
            var item = s.item || s.id || s.index != null ? "item " + (s.index != null ? "#" + s.index : "") : "item";
            return "<li><strong>" + esc(s.id || item) + "</strong> — <span class='reason'>" + esc(s.reason || s.error || "unknown") + "</span></li>";
          }).join("") + "</ul>";
      }
      $("import-report").innerHTML = html;
      $("import-report").hidden = false;
    }).catch(function (e) {
      if (e && e.auth) return;
      err.textContent = e.message || "Import failed."; err.hidden = false;
    }).finally(function () { btn.disabled = false; btn.textContent = "Validate & Import"; });
  });

  /* ---------- URL tester ---------- */
  $("test-run").addEventListener("click", function () {
    var err = $("test-error"); err.hidden = true;
    $("test-result").hidden = true;
    var url = $("test-url").value.trim();
    if (!url) { err.textContent = "Enter a URL to test."; err.hidden = false; return; }
    var btn = $("test-run"); btn.disabled = true; btn.textContent = "Testing…";
    api("POST", "/api/admin/test-url", { url: url, merchant: $("test-merchant").value || undefined }).then(function (d) {
      var r = d.result || d;
      var verdict = String(r.verdict || "attention").toLowerCase();
      var vclass = /ok|good|healthy/.test(verdict) ? "ok" : (/broken|dead|fail/.test(verdict) ? "broken" : "attention");
      var chain = r.redirect_chain || r.chain || [];
      var match = r.merchant_match;
      var html = '<p><span class="verdict ' + vclass + '">' + esc(r.verdict || vclass) + '</span></p>' +
        '<dl class="kv">' +
        '<dt>Final URL</dt><dd>' + esc(r.final_url || r.finalUrl || url) + '</dd>' +
        '<dt>Final status</dt><dd>' + esc(r.final_status != null ? r.final_status : (r.status != null ? r.status : "—")) + '</dd>' +
        '<dt>Merchant match</dt><dd>' + (match === true ? '<span class="match-yes">yes</span>' : match === false ? '<span class="match-no">no</span>' : "—") + '</dd>' +
        (r.note || r.message ? '<dt>Note</dt><dd>' + esc(r.note || r.message) + '</dd>' : '') +
        '</dl>';
      if (chain.length) {
        html += '<p class="muted" style="margin-top:12px">Redirect chain:</p><ul class="chain">' +
          chain.map(function (c) { return "<li>" + esc(typeof c === "string" ? c : (c.url || JSON.stringify(c))) + "</li>"; }).join("") + "</ul>";
      }
      $("test-result").innerHTML = html;
      $("test-result").hidden = false;
    }).catch(function (e) {
      if (e && e.auth) return;
      err.textContent = e.message || "URL test failed."; err.hidden = false;
    }).finally(function () { btn.disabled = false; btn.textContent = "Test"; });
  });

  /* ---------- backup ---------- */
  $("backup-btn").addEventListener("click", function () {
    var err = $("backup-error"); err.hidden = true;
    var btn = $("backup-btn"); btn.disabled = true;
    fetch("/api/admin/backup", { credentials: "same-origin" }).then(function (res) {
      if (res.status === 401) { sessionExpired(); throw { auth: true }; }
      if (!res.ok) throw new Error("Backup failed (" + res.status + ")");
      return res.blob();
    }).then(function (blob) {
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "qa-affiliate-catalog-" + new Date().toISOString().slice(0, 10) + ".json";
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
    }).catch(function (e) {
      if (e && e.auth) return;
      err.textContent = e.message || "Backup failed."; err.hidden = false;
    }).finally(function () { btn.disabled = false; });
  });

  /* ---------- escape closes modals ---------- */
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeModal(); $("confirm-dialog").hidden = true; confirmCb = null; }
  });
})();
