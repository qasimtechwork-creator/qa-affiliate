/* QA Affiliate — front-end engine.
   Loads the data layer (config + products), renders reusable components,
   powers search/filters, tracks affiliate clicks, injects GA4. No affiliate
   URLs are hardcoded — every CTA resolves through data/products.json. */
(function(){
"use strict";
var QA = window.QA = {};
var state = { site:null, affiliates:null, categories:null, products:[] };

function getJSON(path){
  return fetch(path).then(function(r){ if(!r.ok) throw new Error("load failed: "+path); return r.json(); });
}
function esc(s){
  return String(s==null?"":s).replace(/[&<>"']/g,function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
  });
}
function money(n){ return "$"+Number(n).toFixed(2); }
function hasPrice(p){ return p && p.price!=null && !isNaN(Number(p.price)); }
function discountPct(p){
  if(!hasPrice(p) || !p.original_price || p.original_price<=p.price) return 0;
  return Math.round((1-p.price/p.original_price)*100);
}
function priceRow(p){
  if(hasPrice(p)){
    var off=discountPct(p);
    return '<div class="price-row"><span class="price">'+money(p.price)+'</span>'+
      (p.original_price&&p.original_price>p.price?'<span class="price-old">'+money(p.original_price)+'</span>':'')+
      (off>0?'<span class="price-off">-'+off+'%</span>':'')+'</div>';
  }
  return '<div class="price-row"><span class="price-na">Price varies — see live '+esc(merchantName(p))+' deal</span></div>';
}
function soldNote(p){
  return p.sold_count ? '<div class="sold-note">'+esc(p.sold_count)+' on '+esc(merchantName(p))+'</div>' : '';
}
function stars(r){
  if(r==null) return '';
  var full=Math.round(r), s="";
  for(var i=0;i<5;i++) s+= i<full ? "★" : "☆";
  return '<span class="stars">'+s+' <span>('+r.toFixed(1)+')</span></span>';
}
function merchantName(p){
  var m = state.affiliates && state.affiliates.merchants[p.merchant];
  return m ? m.name : p.merchant;
}
function categoryName(id){
  var c = state.categories && state.categories.categories.find(function(x){return x.id===id;});
  return c ? c.name : id;
}
function badges(p){
  var out=[];
  (p.badges||[]).forEach(function(b){
    var label={ "best-seller":"Best Seller","top-rated":"Top Rated","best-deal":"Best Deal","new":"New" }[b]||b;
    out.push('<span class="badge '+esc(b)+'">'+esc(label)+'</span>');
  });
  if(p.trend_status==="viral") out.push('<span class="badge viral">Viral</span>');
  else if(p.trend_status==="trending") out.push('<span class="badge trending">Trending</span>');
  return out.join("");
}
function sampleTag(p){
  return p.sample ? '<span class="sample-tag">Sample listing</span>' : '';
}
/* Branded fallback for products with no merchant image: never a fake/AI photo. */
function imgFallback(p){
  var cat=categoryName(p.category);
  return '<div class="img-unavailable" role="img" aria-label="'+esc(p.name)+' — merchant image unavailable">'+
    '<span class="iu-mono">QA</span>'+
    '<span class="iu-title">'+esc(cat||"QA Affiliate")+'</span>'+
    '<span class="iu-sub">Merchant image unavailable — see the live listing for photos</span></div>';
}
/* Swap a dead merchant image for the branded placeholder (never a broken-image icon). */
window.qaImgErr=function(el){
  el.onerror=null;
  var p=(state.products||[]).find(function(x){return x.id===el.getAttribute('data-pid');});
  if(!p){ el.style.display='none'; return; }
  var d=document.createElement('div'); d.innerHTML=imgFallback(p);
  el.replaceWith(d.firstChild);
};
QA.productCard = function(p){
  var img=p.image_url ?
    '<img src="'+esc(p.image_url)+'" alt="'+esc(p.name)+'" loading="lazy" data-pid="'+esc(p.id)+'" onerror="qaImgErr(this)">' :
    imgFallback(p);
  return '<article class="product-card">'+
    '<div class="product-media"><a href="/product.html?id='+esc(p.id)+'" aria-label="'+esc(p.name)+'">'+
    img+'</a>'+
    '<div class="badge-row">'+badges(p)+'</div>'+sampleTag(p)+'</div>'+
    '<div class="product-body">'+
    '<div class="product-merchant">'+esc(merchantName(p))+'</div>'+
    '<h3 class="product-name"><a href="/product.html?id='+esc(p.id)+'">'+esc(p.name)+'</a></h3>'+
    stars(p.rating)+soldNote(p)+
    priceRow(p)+
    '<div class="product-cta"><a class="btn btn-rose btn-block" data-aff data-id="'+esc(p.id)+'" href="'+esc(p.affiliate_url)+'" target="_blank" rel="nofollow sponsored noopener">View Deal</a></div>'+
    '</div></article>';
};
/* Deals page card: same visual component as QA.productCard, but every link
   stays on-site to the canonical /item/<id> page (never a direct merchant
   link); the affiliate CTA lives on the item page. */
QA.dealCard = function(p){
  var url='/item/'+esc(p.id);
  var img=p.image_url ?
    '<img src="'+esc(p.image_url)+'" alt="'+esc(p.name)+'" loading="lazy" data-pid="'+esc(p.id)+'" onerror="qaImgErr(this)">' :
    imgFallback(p);
  return '<article class="product-card">'+
    '<div class="product-media"><a href="'+url+'" aria-label="'+esc(p.name)+'">'+
    img+'</a>'+
    '<div class="badge-row">'+badges(p)+'</div>'+sampleTag(p)+'</div>'+
    '<div class="product-body">'+
    '<div class="product-merchant">'+esc(categoryName(p.category))+' · '+esc(merchantName(p))+'</div>'+
    '<h3 class="product-name"><a href="'+url+'">'+esc(p.name)+'</a></h3>'+
    stars(p.rating)+soldNote(p)+
    priceRow(p)+
    '<div class="product-cta"><a class="btn btn-rose btn-block" href="'+url+'">View Deal</a></div>'+
    '</div></article>';
};
function renderGrid(el, list){
  if(!list.length){ el.innerHTML='<div class="empty-state"><h3>Nothing found</h3><p>Try adjusting your search or filters.</p></div>'; return; }
  el.innerHTML=list.map(QA.productCard).join("");
}
/* ---------- header / footer ---------- */
function socialLinks(){
  var s=state.site.social, out="";
  var sw='width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"';
  var icons={
    instagram:'<svg '+sw+'><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/></svg>',
    tiktok:'<svg '+sw+'><path d="M9 17.5a3 3 0 1 0 3 3V6.5c.8 2.3 2.6 4 5 4.4"/><path d="M12 6.5c.8 2.3 2.6 4 5 4.4V7.6"/></svg>',
    youtube:'<svg '+sw+'><rect x="2.5" y="6" width="19" height="12" rx="4"/><path d="M10.5 9.8v4.4L14.8 12z" fill="currentColor" stroke="none"/></svg>',
    facebook:'<svg '+sw+'><path d="M14.5 8.5H16V5.5h-1.5a3.5 3.5 0 0 0-3.5 3.5v2.5H9V15h2v5.5h3V15h2.2l.8-3.5h-3V9c0-.3.2-.5.5-.5z"/></svg>',
    x:'<svg '+sw+'><path d="M5 5l14 14M19 5L5 19"/></svg>'
  };
  Object.keys(icons).forEach(function(k){
    if(s[k]) out+='<a href="'+esc(s[k])+'" target="_blank" rel="noopener" aria-label="'+k+'">'+icons[k]+'</a>';
  });
  return out;
}
function renderChrome(){
  var s=state.site;
  document.querySelectorAll("[data-site-header]").forEach(function(el){
    el.innerHTML=
    (s.demo_mode?'<div class="demo-notice">Demonstration catalog — sample listings shown. Connect affiliate feeds to go live. <a href="/legal/disclosure.html">How we make money</a></div>':'')+
    '<header class="site-header"><div class="container header-inner">'+
    '<a class="brand" href="/"><img src="'+esc(s.brand.logo)+'" alt="'+esc(s.brand.logo_alt)+'"><span class="brand-name">'+esc(s.brand.name)+'<small>'+esc(s.brand.tagline)+'</small></span></a>'+
    '<button class="nav-toggle" aria-label="Menu" onclick="document.querySelector(\'.main-nav\').classList.toggle(\'open\')">☰</button>'+
    '<nav class="main-nav">'+
    '<a href="/">Home</a><a href="/products.html">Shop All</a><a href="/trending.html">Trending</a><a href="/deals.html">Deals</a><a href="/guides.html">Guides</a><a href="/about.html">About</a>'+
    '</nav></div></header>';
    var path=location.pathname;
    el.querySelectorAll(".main-nav a").forEach(function(a){
      if(a.getAttribute("href")===path) a.classList.add("active");
    });
  });
  document.querySelectorAll("[data-site-footer]").forEach(function(el){
    var cats=state.categories.categories.slice(0,6).map(function(c){
      return '<li><a href="/category.html?cat='+c.id+'">'+esc(c.name)+'</a></li>';
    }).join("");
    el.innerHTML='<footer class="site-footer"><div class="container">'+
    '<div class="footer-grid">'+
    '<div class="footer-brand"><img src="'+esc(s.brand.logo)+'" alt="'+esc(s.brand.logo_alt)+'"><p>'+esc(s.brand.tagline)+'. Transparent affiliate discovery for women\'s fashion, beauty and lifestyle.</p><div class="social-row">'+socialLinks()+'</div></div>'+
    '<div><h4>Shop</h4><ul>'+cats+'</ul></div>'+
    '<div><h4>Discover</h4><ul><li><a href="/trending.html">Trending & Viral</a></li><li><a href="/deals.html">Best Deals</a></li><li><a href="/products.html">All Products</a></li><li><a href="/guides.html">Buying Guides</a></li></ul></div>'+
    '<div><h4>Company</h4><ul><li><a href="/about.html">About</a></li><li><a href="/contact.html">Contact</a></li><li><a href="/faq.html">FAQ</a></li><li><a href="/legal/disclosure.html">Affiliate Disclosure</a></li><li><a href="/legal/privacy.html">Privacy Policy</a></li><li><a href="/legal/terms.html">Terms</a></li></ul></div>'+
    '</div>'+
    '<div class="footer-bottom"><span>© '+new Date().getFullYear()+' '+esc(s.brand.name)+'. All rights reserved.</span><span><a href="/legal/advertising.html">Advertising Disclosure</a> · <a href="/legal/cookies.html">Cookie Notice</a></span></div>'+
    '</div></footer>';
  });
  document.title=document.title.replace("{brand}",s.brand.name);
}
/* ---------- GA4 + affiliate click tracking ---------- */
function initAnalytics(){
  var id=state.site.analytics.ga4_measurement_id;
  if(!id) return;
  var g=document.createElement("script");
  g.async=true; g.src="https://www.googletagmanager.com/gtag/js?id="+encodeURIComponent(id);
  document.head.appendChild(g);
  window.dataLayer=window.dataLayer||[];
  window.gtag=function(){window.dataLayer.push(arguments);};
  window.gtag("js",new Date());
  window.gtag("config",id,{anonymize_ip:true});
}
function trackAffiliateClick(p){
  var payload={event:"affiliate_click",product_id:p.id,product_name:p.name,merchant:p.merchant,category:p.category,value:p.price,currency:"USD"};
  if(window.gtag) window.gtag("event","affiliate_click",payload);
  try{
    var log=JSON.parse(localStorage.getItem("qa_aff_clicks")||"[]");
    log.push(Object.assign({ts:new Date().toISOString()},payload));
    localStorage.setItem("qa_aff_clicks",JSON.stringify(log.slice(-500)));
  }catch(e){}
}
document.addEventListener("click",function(e){
  var a=e.target.closest("[data-aff]");
  if(!a) return;
  var p=state.products.find(function(x){return x.id===a.getAttribute("data-id");});
  if(p) trackAffiliateClick(p);
});
/* ---------- promo links (config-driven, never hardcoded in HTML) ---------- */
function initPromoLinks(){
  var promos=(state.site&&state.site.promotions)||{};
  document.querySelectorAll("[data-promo]").forEach(function(a){
    var url=promos[a.getAttribute("data-promo")];
    if(url) a.setAttribute("href",url);
  });
}
/* ---------- canonical URL ---------- */
function setCanonical(){
  var base=(state.site&&state.site.domain&&state.site.domain.canonical)||"";
  if(!base) return;
  var href=base.replace(/\/$/,"")+location.pathname+location.search;
  var link=document.querySelector('link[rel="canonical"]');
  if(!link){ link=document.createElement("link"); link.setAttribute("rel","canonical"); document.head.appendChild(link); }
  link.setAttribute("href",href);
}
/* ---------- newsletter (provider-independent, honest state) ---------- */
function initNewsletter(){
  document.querySelectorAll("[data-newsletter-form]").forEach(function(form){
    var cfg=(state.site&&state.site.newsletter)||{};
    var msg=form.parentElement.querySelector("[data-newsletter-msg]");
    if(!cfg.provider||!cfg.action_url){
      /* No provider connected: do not collect emails or imply a subscription happened. */
      var input=form.querySelector('input[type="email"]');
      if(input) input.disabled=true;
      var btn=form.querySelector('button[type="submit"]');
      if(btn) btn.disabled=true;
      if(msg) msg.textContent="Our newsletter launches soon — we're connecting our email provider. Check back shortly!";
      return;
    }
    form.addEventListener("submit",function(e){
      e.preventDefault();
      var email=form.querySelector('input[type="email"]').value.trim();
      if(!email||email.indexOf("@")<0){ msg.textContent="Please enter a valid email address."; return; }
      msg.textContent="Subscribing…";
      fetch(cfg.action_url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:email})})
        .then(function(r){ if(!r.ok) throw new Error("bad response"); msg.textContent="Thanks — please check your inbox to confirm your subscription."; form.reset(); })
        .catch(function(){ msg.textContent="Something went wrong — please try again in a moment."; });
    });
  });
}
/* ---------- filters ---------- */
function applyFilters(list,f){
  return list.filter(function(p){
    if(f.q && (p.name+" "+p.short_description+" "+p.category+" "+p.subcategory).toLowerCase().indexOf(f.q.toLowerCase())<0) return false;
    if(f.cat && p.category!==f.cat) return false;
    if(f.sub && p.subcategory!==f.sub) return false;
    if(f.minPrice!=null && hasPrice(p) && p.price<f.minPrice) return false;
    if(f.maxPrice!=null && hasPrice(p) && p.price>f.maxPrice) return false;
    if(f.minRating!=null && (p.rating==null||p.rating<f.minRating)) return false;
    if(f.minDiscount!=null && discountPct(p)<f.minDiscount) return false;
    if(f.store && p.merchant!==f.store) return false;
    if(f.trendingOnly && !p.trend_status) return false;
    return true;
  });
}
function sortList(list,sort){
  var l=list.slice();
  if(sort==="price-asc") l.sort(function(a,b){return (a.price==null?Infinity:+a.price)-(b.price==null?Infinity:+b.price);});
  else if(sort==="price-desc") l.sort(function(a,b){return (b.price==null?-Infinity:+b.price)-(a.price==null?-Infinity:+a.price);});
  else if(sort==="rating") l.sort(function(a,b){return (b.rating||0)-(a.rating||0);});
  else if(sort==="discount") l.sort(function(a,b){return discountPct(b)-discountPct(a);});
  else if(sort==="newest") l.sort(function(a,b){return (b.badges||[]).indexOf("new")-(a.badges||[]).indexOf("new");});
  return l;
}
/* ---------- page renderers ---------- */
var GUIDES={
 "glass-skin-routine":{title:"The Glass-Skin Routine: A Beginner's Buying Guide",url:"/guides/glass-skin-routine.html",desc:"How to build a simple, effective skincare routine — and what to look for in each step."},
 "capsule-wardrobe":{title:"Build a 12-Piece Capsule Wardrobe",url:"/guides/capsule-wardrobe.html",desc:"Twelve versatile pieces, dozens of outfits — a practical guide to buying less and wearing more."},
 "heatless-curls-guide":{title:"Heatless Curls That Actually Work: A Beginner's Guide",url:"/guides/heatless-curls-guide.html",desc:"Satin rods, foam curlers and braids — the methods, the technique, and what to buy."},
 "jewelry-that-doesnt-tarnish":{title:"How to Buy Jewelry That Doesn't Tarnish",url:"/guides/jewelry-that-doesnt-tarnish.html",desc:"Materials ranked, listing red flags, and care rules that double your jewelry's life."},
 "makeup-brush-guide":{title:"The 15-Piece Makeup Brush Guide: What Each Brush Actually Does",url:"/guides/makeup-brush-guide.html",desc:"The five brushes that matter, what the rest do, and how to buy a set that lasts."}
};
function artClass(url){
  if(url.indexOf("glass-skin")>=0) return "ga-skincare";
  if(url.indexOf("capsule-wardrobe")>=0) return "ga-wardrobe";
  if(url.indexOf("heatless-curls")>=0) return "ga-curls";
  if(url.indexOf("tarnish")>=0) return "ga-jewelry";
  if(url.indexOf("makeup-brush")>=0) return "ga-brushes";
  return "ga-default";
}
/* ---------- guide cover photos (real merchant photography) ---------- */
var GUIDE_PHOTOS={
  "ga-skincare":{src:"/assets/images/guides/glass-skin.jpg",alt:"Jade roller and gua sha skincare tools"},
  "ga-wardrobe":{src:"/assets/images/guides/capsule-wardrobe.jpg",alt:"Elegant open-front fashion jacket"},
  "ga-curls":{src:"/assets/images/guides/heatless-curls.jpg",alt:"Heatless curling rod set"},
  "ga-jewelry":{src:"/assets/images/guides/jewelry.jpg",alt:"Gold jewelry set"},
  "ga-brushes":{src:"/assets/images/guides/makeup-brushes.jpg",alt:"Professional makeup brush set"}
};
function enhanceGuideArt(){
  var els=document.querySelectorAll(".guide-art");
  for(var i=0;i<els.length;i++){
    var el=els[i];
    if(el.querySelector(".ga-photo")) continue;
    for(var k in GUIDE_PHOTOS){
      if(el.classList.contains(k)){
        var p=GUIDE_PHOTOS[k];
        el.insertAdjacentHTML("afterbegin",'<img class="ga-photo" src="'+p.src+'" alt="'+p.alt+'" loading="lazy"><span class="ga-shade"></span>');
        break;
      }
    }
  }
}
/* ---------- 3D category icons (clean names; missing files hide gracefully) ---------- */
var CATEGORY_ICONS={
  "fashion":"/assets/images/categories/icon-fashion.webp",
  "shoes":"/assets/images/categories/icon-shoes.webp",
  "jewelry":"/assets/images/categories/icon-jewelry.webp",
  "bags":"/assets/images/categories/icon-bags.webp",
  "beauty":"/assets/images/categories/icon-beauty.webp",
  "skincare":"/assets/images/categories/icon-skincare.webp",
  "hair":"/assets/images/categories/icon-hair.webp",
  "accessories":"/assets/images/categories/icon-accessories.webp",
  "lingerie":"/assets/images/categories/icon-lingerie.webp",
  "fitness":"/assets/images/categories/icon-fitness.webp",
  "trending":"/assets/images/categories/icon-trending.webp",
  "home":"/assets/images/categories/icon-home.webp"
};
var pages={
home:function(){
  var P=state.products;
  var trending=P.filter(function(p){return p.trend_status;}).slice(0,8);
  var best=P.filter(function(p){return (p.badges||[]).indexOf("best-seller")>=0;}).slice(0,4);
  var top=P.slice().sort(function(a,b){return (b.rating||0)-(a.rating||0);}).slice(0,4);
  var editors=P.slice().sort(function(a,b){return (b.rating||0)-(a.rating||0);}).slice(0,4);
  renderGrid(document.getElementById("sec-trending"),trending);
  renderGrid(document.getElementById("sec-best"),best);
  renderGrid(document.getElementById("sec-top"),top);
  renderGrid(document.getElementById("sec-editors"),editors);
  var cg=document.getElementById("cat-tiles");
  cg.innerHTML=state.categories.categories.map(function(c){
    var href=c.special?"/trending.html":"/category.html?cat="+c.id;
    var ci=CATEGORY_ICONS[c.id];
    var iconHtml=ci?'<div class="cat-icon"><img src="'+ci+'" alt="'+esc(c.name)+' icon" loading="lazy" onerror="this.closest(\'.cat-icon\').classList.add(\'no-img\');this.remove()"></div>':'';
    return '<a class="cat-tile" href="'+href+'">'+iconHtml+'<h3>'+esc(c.name)+'</h3><p>'+esc(c.tagline)+'</p></a>';
  }).join("");
},
browse:function(){ initFilterPage({}); },
category:function(){
  var cat=new URLSearchParams(location.search).get("cat");
  var c=state.categories.categories.find(function(x){return x.id===cat;});
  var title=document.getElementById("cat-title"), sub=document.getElementById("cat-sub");
  if(!c){ title.textContent="Category not found"; return; }
  var ci=CATEGORY_ICONS[c.id];
  title.innerHTML=(ci?'<img class="cat-head-icon" src="'+ci+'" alt="" loading="lazy" onerror="this.remove()">':'')+'<span>'+esc(c.name)+'</span>';
  sub.textContent=c.tagline;
  document.title=c.name+" — "+state.site.brand.name;
  var crumb=document.getElementById("crumb-cat"); if(crumb) crumb.textContent=c.name;
  var bi=document.getElementById("cat-banner-img"), bf=document.getElementById("cat-banner-fallback");
  if(bi){ bi.src="/assets/images/categories/banners/"+c.id+".gif?v=7"; bi.alt=c.name; }
  if(bf){ bf.src="/assets/images/categories/banners/"+c.id+".jpg?v=7"; bf.alt=c.name; }
  /* 3D parallax: banner bg drifts slightly, foreground petals drift more */
  (function(){
    var banner=document.querySelector(".cat-banner"); if(!banner) return;
    if(window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if(window.matchMedia("(hover: none)").matches) return;
    var bg=banner.querySelector(".cat-banner-bg"), fx=banner.querySelector(".cat-fx");
    banner.addEventListener("mousemove",function(e){
      var r=banner.getBoundingClientRect();
      var dx=(e.clientX-r.left)/r.width-0.5, dy=(e.clientY-r.top)/r.height-0.5;
      if(bg) bg.style.transform="translate3d("+(-dx*14)+"px,"+(-dy*10)+"px,0)";
      if(fx) fx.style.transform="translate3d("+(dx*26)+"px,"+(dy*18)+"px,0)";
    });
    banner.addEventListener("mouseleave",function(){
      if(bg) bg.style.transform=""; if(fx) fx.style.transform="";
    });
  })();
  var descEl=document.getElementById("cat-desc");
  if(descEl&&c.description) descEl.textContent=c.description;
  var rg=document.getElementById("cat-guides");
  if(rg){
    var gl=(c.related_guides||[]).map(function(slug){return GUIDES[slug];}).filter(Boolean);
    if(gl.length){
      rg.innerHTML='<h3 class="related-h">Helpful guides for this category</h3><div class="guide-grid">'+
        gl.map(function(g){
          return '<a class="guide-card" href="'+g.url+'"><div class="guide-art ga-mini '+artClass(g.url)+'"><span class="ga-kicker">Guide</span><span class="ga-title">'+esc(g.title)+'</span></div><div class="pad"><h3>'+esc(g.title)+'</h3><p>'+esc(g.desc)+'</p></div></a>';
        }).join("")+'</div>';
    }
  }
  initFilterPage({cat:cat});
},
trending:function(){
  var list=state.products.filter(function(p){return p.trend_status;});
  list.sort(function(a,b){return (b.trend_status==="viral")-(a.trend_status==="viral");});
  renderGrid(document.getElementById("trend-grid"),list);
  document.getElementById("trend-count").textContent=list.length+" trending finds";
},
deals:function(){
  var el=document.getElementById("deals-grid");
  if(!el) return;
  var ids=window.QA_DEAL_IDS||[];
  var byId={};
  state.products.forEach(function(p){ byId[p.id]=p; });
  var list=ids.map(function(id){return byId[id];}).filter(Boolean);
  if(!list.length){
    el.innerHTML='<div class="empty-state"><h3>Deal picks are being refreshed</h3><p>Please check back shortly.</p></div>';
    return;
  }
  el.innerHTML=list.map(QA.dealCard).join("");
},
product:function(){
  var id=new URLSearchParams(location.search).get("id");
  var p=state.products.find(function(x){return x.id===id;});
  var wrap=document.getElementById("pd-wrap");
  if(!p){ wrap.innerHTML='<div class="empty-state"><h3>Product not found</h3><p><a href="/products.html">Browse all products</a></p></div>'; return; }
  document.title=p.name+" — "+state.site.brand.name;
  var off=discountPct(p);
  var cat=state.categories.categories.find(function(x){return x.id===p.category;});
  var metaD=document.querySelector('meta[name="description"]');
  if(metaD){ metaD.setAttribute('content', p.name+" — "+(cat?cat.name:"product")+" pick from "+merchantName(p)+", curated by QA Affiliate. Price varies; see the live deal for today's price."); }
  var pdImg=p.image_url ?
    '<img src="'+esc(p.image_url)+'" alt="'+esc(p.name)+'" data-pid="'+esc(p.id)+'" onerror="qaImgErr(this)">' :
    imgFallback(p);
  var pdPrice=hasPrice(p)
    ? '<div class="pd-price">'+money(p.price)+(p.original_price&&p.original_price>p.price?' <span class="price-old">'+money(p.original_price)+'</span> <span class="price-off">Save '+off+'%</span>':'')+'</div>'
    : '<div class="pd-price"><span class="price-na">Price varies — see live '+esc(merchantName(p))+' deal</span></div>';
  var keyFeatures=(p.key_features&&p.key_features.length)?'<h3>Key features</h3><ul class="spec-list">'+p.key_features.map(function(f){return "<li>"+esc(f)+"</li>";}).join("")+'</ul>':'';
  var prosCons=((p.pros&&p.pros.length)||(p.cons&&p.cons.length))?
    '<div class="pros-cons">'+
    (p.pros&&p.pros.length?'<div><h4>What we like</h4><ul class="pros">'+p.pros.map(function(x){return "<li>"+esc(x)+"</li>";}).join("")+'</ul></div>':'')+
    (p.cons&&p.cons.length?'<div><h4>Keep in mind</h4><ul class="cons">'+p.cons.map(function(x){return "<li>"+esc(x)+"</li>";}).join("")+'</ul></div>':'')+
    '</div>':'';
  var related=state.products.filter(function(x){return x.id!==p.id&&x.category===p.category;}).slice(0,4);
  var relHtml=related.length?
    '<section class="related-section"><h2 class="section-title">You may also like</h2><p class="section-sub">More picks from '+esc(cat?cat.name:"this category")+'.</p><div class="product-grid">'+related.map(QA.productCard).join("")+'</div></section>':'';
  var rguides=((cat&&cat.related_guides)||[]).map(function(slug){return GUIDES[slug];}).filter(Boolean);
  var rguidesHtml=rguides.length?
    '<section class="related-section"><h2 class="section-title">Helpful guides</h2><div class="guide-grid">'+
    rguides.map(function(g){
      return '<a class="guide-card" href="'+g.url+'"><div class="guide-art ga-mini '+artClass(g.url)+'"><span class="ga-kicker">Guide</span><span class="ga-title">'+esc(g.title)+'</span></div><div class="pad"><h3>'+esc(g.title)+'</h3><p>'+esc(g.desc)+'</p></div></a>';
    }).join("")+'</div></section>':'';
  wrap.innerHTML=
  '<div class="breadcrumb"><a href="/">Home</a> / '+(cat?'<a href="/category.html?cat='+cat.id+'">'+esc(cat.name)+'</a> / ':'')+esc(p.name)+'</div>'+
  '<div class="pd-layout"><div><div class="pd-media">'+pdImg+'</div></div>'+
  '<div class="pd-info"><div class="badge-row" style="position:static;margin-bottom:10px">'+badges(p)+'</div>'+(p.sample?'<p style="margin-bottom:10px"><span class="sample-tag" style="position:static">Sample listing — demo data</span></p>':'')+
  '<h1>'+esc(p.name)+'</h1>'+
  '<div class="pd-meta"><span>'+stars(p.rating)+'</span>'+(p.review_count?'<span>'+Number(p.review_count).toLocaleString()+' reviews</span>':'')+(p.sold_count?'<span>'+esc(p.sold_count)+' on '+esc(merchantName(p))+'</span>':'')+'<span>Sold by '+esc(merchantName(p))+'</span></div>'+
  pdPrice+
  '<p class="pd-desc">'+esc(p.short_description)+'</p>'+
  '<div class="pd-cta-row"><a class="btn btn-rose" data-aff data-id="'+esc(p.id)+'" href="'+esc(p.affiliate_url)+'" target="_blank" rel="nofollow sponsored noopener">View Deal at '+esc(merchantName(p))+'</a></div>'+
  '<div class="disclosure-box"><strong>Affiliate disclosure:</strong> '+esc((state.affiliates.merchants[p.merchant]||{}).disclosure_short||"QA Affiliate may earn a commission on qualifying purchases.")+'</div>'+
  keyFeatures+
  prosCons+
  '</div></div>'+
  relHtml+rguidesHtml;
}
};
function initFilterPage(preset){
  var grid=document.getElementById("filter-grid"), count=document.getElementById("filter-count");
  var subSel=document.getElementById("f-sub");
  function subcats(){
    var cat=(document.getElementById("f-cat")||{}).value||preset.cat||"";
    var c=state.categories.categories.find(function(x){return x.id===cat;});
    return c?c.subcategories:[];
  }
  function refreshSubs(){
    if(!subSel) return;
    var subs=subcats(), cur=subSel.value;
    subSel.innerHTML='<option value="">All subcategories</option>'+subs.map(function(s){return '<option value="'+s+'">'+s.replace(/-/g," ")+'</option>';}).join("");
    if(subs.indexOf(cur)>=0) subSel.value=cur;
  }
  function current(){
    function val(id){ var el=document.getElementById(id); return el?el.value:""; }
    function num(id){ var v=parseFloat(val(id)); return isNaN(v)?null:v; }
    return { q:val("f-q"), cat:val("f-cat")||preset.cat||"", sub:val("f-sub"),
      minPrice:num("f-minp"), maxPrice:num("f-maxp"),
      minRating:num("f-rating"), minDiscount:num("f-discount"),
      store:val("f-store"), trendingOnly:document.getElementById("f-trend")?document.getElementById("f-trend").checked:false,
      sort:val("f-sort") };
  }
  function run(){
    var f=current();
    var list=sortList(applyFilters(state.products,f),f.sort);
    renderGrid(grid,list);
    count.textContent=list.length+" result"+(list.length===1?"":"s");
  }
  ["f-q","f-cat","f-sub","f-minp","f-maxp","f-rating","f-discount","f-store","f-sort"].forEach(function(id){
    var el=document.getElementById(id); if(el) el.addEventListener("input",run);
  });
  var ft=document.getElementById("f-trend"); if(ft) ft.addEventListener("change",run);
  var fc=document.getElementById("f-cat"); if(fc){ fc.addEventListener("change",function(){refreshSubs();run();}); }
  if(preset.cat&&fc){ fc.value=preset.cat; }
  refreshSubs(); run();
}
/* ---------- boot ---------- */
function boot(){
  Promise.all([getJSON("/config/site.json"),getJSON("/config/affiliates.json"),getJSON("/data/categories.json"),getJSON("/data/products.json")])
  .then(function(r){
    state.site=r[0]; state.affiliates=r[1]; state.categories=r[2]; state.products=r[3].products;
    renderChrome(); initAnalytics(); initNewsletter(); initPromoLinks(); setCanonical();
    var page=document.body.getAttribute("data-page");
    if(page&&pages[page]) pages[page]();
    enhanceGuideArt();
  }).catch(function(err){
    document.body.insertAdjacentHTML("afterbegin",'<div class="demo-notice">Could not load site data. Please check your connection and reload.</div>');
  });
}
if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",boot);
else boot();
})();
