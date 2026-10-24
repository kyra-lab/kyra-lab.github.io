// Mobile menu
(function(){
  var t=document.querySelector('.nav-toggle'),n=document.getElementById('site-nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});}
})();
// News filters
(function(){
  var bar=document.querySelector('.filters');if(!bar)return;
  var items=document.querySelectorAll('.news-item');
  bar.addEventListener('click',function(e){
    var b=e.target.closest('button');if(!b)return;
    bar.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
    var f=b.dataset.filter;
    items.forEach(function(it){it.hidden=!(f==='all'||it.dataset.tags.split(' ').indexOf(f)>-1);});
  });
})();
// Respect reduced motion: don't autoplay videos
if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){document.querySelectorAll('video[autoplay]').forEach(function(v){v.removeAttribute('autoplay');v.pause();});}
