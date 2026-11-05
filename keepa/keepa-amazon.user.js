// ==UserScript==
// @name         Keepa on Amazon (mobile)
// @namespace    https://github.com/tatarabeats/my-business
// @version      1.0.0
// @description  スマホのブラウザでAmazon商品ページを開いたとき、Keepaの価格推移グラフを表示する
// @match        https://www.amazon.co.jp/*
// @match        https://amazon.co.jp/*
// @match        https://www.amazon.com/*
// @match        https://www.amazon.co.uk/*
// @match        https://www.amazon.de/*
// @match        https://www.amazon.fr/*
// @match        https://www.amazon.ca/*
// @match        https://www.amazon.it/*
// @match        https://www.amazon.es/*
// @match        https://www.amazon.in/*
// @match        https://www.amazon.com.mx/*
// @run-at       document-idle
// @grant        none
// ==/UserScript==

(function () {
  'use strict';

  var BOX_ID = 'mm-keepa-box';

  // Amazonドメイン → Keepaのドメイン番号
  var DOMAINS = {
    'amazon.com': 1, 'amazon.co.uk': 2, 'amazon.de': 3, 'amazon.fr': 4,
    'amazon.co.jp': 5, 'amazon.ca': 6, 'amazon.it': 8, 'amazon.es': 9,
    'amazon.in': 10, 'amazon.com.mx': 11
  };

  var RANGES = [
    { label: '1ヶ月', days: 31 },
    { label: '3ヶ月', days: 90 },
    { label: '1年', days: 365 },
    { label: '全期間', days: 0 }
  ];

  function getDomain() {
    var host = location.hostname.replace(/^www\./, '');
    if (!DOMAINS[host]) return null;
    return { tld: host.replace(/^amazon\./, ''), id: DOMAINS[host] };
  }

  function getAsin() {
    var m = location.pathname.match(/\/(?:dp|gp\/product|gp\/aw\/d|o\/ASIN|exec\/obidos\/ASIN)\/([A-Z0-9]{10})(?:[/?]|$)/i);
    if (m) return m[1].toUpperCase();
    var input = document.querySelector('input#ASIN, input[name="ASIN"], input[name="asin"]');
    if (input && /^[A-Z0-9]{10}$/i.test(input.value)) return input.value.toUpperCase();
    return null;
  }

  function chartUrl(asin, domain, days) {
    var w = Math.min(Math.max(window.innerWidth - 24, 300), 800);
    var p = [
      'asin=' + asin,
      'domain=' + domain.tld,
      'amazon=1', 'new=1', 'used=1', 'salesrank=1',
      'width=' + w, 'height=' + Math.round(w * 0.6)
    ];
    if (days) p.push('range=' + days);
    return 'https://graph.keepa.com/pricehistory.png?' + p.join('&');
  }

  function findAnchor() {
    var sels = ['#title_feature_div', '#titleSection', '#title', '#productTitle', '#dp-container', '#dp', '#a-page'];
    for (var i = 0; i < sels.length; i++) {
      var el = document.querySelector(sels[i]);
      if (el) return el;
    }
    return document.body;
  }

  function render(asin, domain) {
    var old = document.getElementById(BOX_ID);
    if (old) old.remove();

    var box = document.createElement('div');
    box.id = BOX_ID;
    box.setAttribute('data-asin', asin);
    box.style.cssText = 'margin:12px 0;padding:10px;border:1px solid #d5d9d9;border-radius:8px;background:#fff;color:#0f1111;font:14px/1.4 -apple-system,BlinkMacSystemFont,sans-serif;';

    var head = document.createElement('div');
    head.style.cssText = 'display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;';
    var title = document.createElement('strong');
    title.textContent = 'Keepa 価格推移';
    var link = document.createElement('a');
    link.href = 'https://keepa.com/#!product/' + domain.id + '-' + asin;
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = 'Keepaで詳しく見る ›';
    link.style.cssText = 'color:#007185;text-decoration:none;';
    head.appendChild(title);
    head.appendChild(link);

    var tabs = document.createElement('div');
    tabs.style.cssText = 'display:flex;gap:6px;margin-bottom:8px;';

    var img = document.createElement('img');
    img.alt = 'Keepa価格グラフ';
    img.style.cssText = 'display:block;width:100%;height:auto;min-height:120px;background:#f7f7f7;';
    img.onerror = function () {
      img.replaceWith(document.createTextNode('グラフを読み込めませんでした（Keepaに未登録の商品の可能性があります）'));
    };

    var buttons = [];
    function select(idx) {
      img.src = chartUrl(asin, domain, RANGES[idx].days);
      buttons.forEach(function (b, i) {
        var on = i === idx;
        b.style.background = on ? '#ffd814' : '#fff';
        b.style.borderColor = on ? '#fcd200' : '#d5d9d9';
      });
    }
    RANGES.forEach(function (r, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = r.label;
      b.style.cssText = 'flex:1;padding:6px 0;border:1px solid #d5d9d9;border-radius:6px;font-size:13px;color:#0f1111;';
      b.addEventListener('click', function (e) { e.preventDefault(); select(i); });
      buttons.push(b);
      tabs.appendChild(b);
    });

    box.appendChild(head);
    box.appendChild(tabs);
    box.appendChild(img);

    var anchor = findAnchor();
    if (anchor === document.body) anchor.insertBefore(box, anchor.firstChild);
    else anchor.parentNode.insertBefore(box, anchor.nextSibling);

    select(1); // 初期表示は3ヶ月
  }

  function run() {
    var domain = getDomain();
    var asin = getAsin();
    var box = document.getElementById(BOX_ID);
    if (!domain || !asin) {
      if (box) box.remove();
      return false;
    }
    if (box && box.getAttribute('data-asin') === asin) return true;
    render(asin, domain);
    return true;
  }

  var isBookmarklet = !!window.__mmKeepaBookmarklet;
  var hidden = false;

  // ブックマークレットとして2回目に押されたときは表示/非表示を切り替える
  if (window.__mmKeepaLoaded) {
    window.__mmKeepaToggle();
    return;
  }
  window.__mmKeepaLoaded = true;
  window.__mmKeepaToggle = function () {
    var existing = document.getElementById(BOX_ID);
    if (existing) { hidden = true; existing.remove(); return; }
    hidden = false;
    if (!run()) alert('Amazonの商品ページで実行してください');
  };

  if (!run() && isBookmarklet) alert('Amazonの商品ページで実行してください');

  // バリエーション切替でURLが変わったときや、ページの再描画で枠が消えたときに追従する
  setInterval(function () { if (!hidden) run(); }, 1000);
})();
