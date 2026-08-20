#!/usr/bin/env python3
"""
build.py - regenerate index.html for the AI Cost Watch interactive tool.

Reads costwatch.json (the frozen dataset) and writes a single self-contained,
dependency-free index.html with the data embedded verbatim. Standard library only.

Usage (run in your terminal):
  python3 build.py

To add a new issue: append one object to "issues" in costwatch.json (and any new
"readings" to the indicators), then re-run this script. Nothing else changes.
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
DATA = json.loads((HERE / "costwatch.json").read_text(encoding="utf-8"))

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Cost Watch (interactive)</title>
<style>
  html[data-theme="light"] {
    --fill: #1a365d;
    --fill-fg: #f8fafc;
    --bg: #f8fafc;
    --bg-card: #ffffff;
    --navy: #1a365d;
    --slate: #4a5568;
    --body: #2d3748;
    --alt: #f1f5f9;
    --line: #cbd5e1;
    --good: #15803d;
    --goodbg: #f0fdf4;
    --bad: #b91c1c;
    --badbg: #fef2f2;
    --accent: #2563eb;
    --amber: #b45309;
    --amberbg: #fffbeb;
  }
  html[data-theme="dark"] {
    --fill: #1e293b;
    --fill-fg: #f1f5f9;
    --bg: #0b0f19;
    --bg-card: #111827;
    --navy: #ffffff;
    --slate: #94a3b8;
    --body: #f1f5f9;
    --alt: #162032;
    --line: #1e293b;
    --good: #34d399;
    --goodbg: rgba(52,211,153,0.15);
    --bad: #f87171;
    --badbg: rgba(248,113,113,0.15);
    --accent: #38bdf8;
    --amber: #f59e0b;
    --amberbg: rgba(245,158,11,0.15);
  }
  *{box-sizing:border-box}
  body{font-family:Arial,Helvetica,sans-serif;color:var(--body);margin:0;
    background:var(--bg);line-height:1.5;-webkit-font-smoothing:antialiased}
  .wrap{max-width:1000px;margin:0 auto;padding:28px 22px 64px}
  h1{color:var(--navy);font-size:26px;margin:0 0 4px}
  .sub{color:var(--slate);font-size:14px;margin:0 0 8px;max-width:760px}
  .stamp{color:var(--slate);font-size:12.5px;margin:6px 0 0}
  .stamp a{color:var(--accent);text-decoration:none}
  .stamp a:hover{text-decoration:underline}

  .signal{margin:20px 0 6px;padding:14px 18px;border-radius:8px;
    border:1px solid var(--line);background:var(--alt);display:flex;
    flex-wrap:wrap;gap:6px 18px;align-items:baseline}
  .signal .lab{font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;
    color:var(--slate);font-weight:bold}
  .signal .val{font-size:16px;font-weight:bold;color:var(--good)}
  .signal .val .dot{display:inline-block;width:9px;height:9px;border-radius:50%;
    background:var(--good);margin-right:7px;vertical-align:middle}
  .signal .note{font-size:13px;color:var(--body);flex:1 1 100%;margin-top:4px}

  .controls{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;
    margin:18px 0 8px;padding:14px 16px;background:var(--alt);
    border:1px solid var(--line);border-radius:8px}
  .ctl label{display:block;font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;
    color:var(--slate);font-weight:bold;margin-bottom:6px}
  .seg{display:inline-flex;border:1px solid var(--navy);border-radius:6px;overflow:hidden;flex-wrap:wrap}
  .seg button{appearance:none;border:0;background:#fff;color:var(--navy);
    padding:8px 14px;font-size:13.5px;cursor:pointer;font-family:inherit}
  .seg button+button{border-left:1px solid var(--navy)}
  .seg button.on{background:var(--fill);color:var(--fill-fg);font-weight:bold}
  select{padding:8px 10px;font-size:14px;font-family:inherit;
    border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--body);min-width:260px}

  .card{margin-top:16px;border:1px solid var(--line);border-radius:8px;overflow:hidden}
  .card .head{padding:14px 18px;background:#fbfdff;border-bottom:1px solid var(--line)}
  .card .head h2{margin:0;color:var(--navy);font-size:18px}
  .card .head .meta{color:var(--slate);font-size:12.5px;margin-top:3px}
  .badge{display:inline-block;padding:2px 9px;border-radius:11px;font-size:11.5px;
    font-weight:bold;margin-left:8px;vertical-align:middle}
  .badge.exp{color:var(--good);background:var(--goodbg)}
  .badge.trig{color:var(--bad);background:var(--badbg)}
  .card .body{padding:16px 18px}
  .thread{font-size:14.5px;color:var(--body);border-left:4px solid var(--navy);
    padding:2px 0 2px 14px;margin:0 0 14px}
  .subh{font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--slate);
    font-weight:bold;margin:16px 0 8px}
  ul.dev{margin:0;padding-left:20px}
  ul.dev li{margin:0 0 9px;font-size:13.5px}
  ul.watch{margin:0;padding-left:20px}
  ul.watch li{margin:0 0 6px;font-size:13px;color:var(--slate)}
  .net{margin:14px 0 0;padding:12px 14px;background:var(--alt);border-radius:6px;font-size:13.5px}
  .net b{color:var(--navy)}

  table{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:6px}
  thead th{background:var(--fill);color:var(--fill-fg);text-align:left;padding:9px 10px;font-size:12.5px}
  tbody td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
  tbody tr:nth-child(even){background:var(--alt)}
  td.val{font-weight:bold;color:var(--navy);white-space:nowrap;font-variant-numeric:tabular-nums}
  td.iss{color:var(--slate);white-space:nowrap}
  .foot{margin-top:26px;font-size:12px;color:var(--slate);line-height:1.55}
  .foot b{color:var(--body)}
  .hide{display:none}
  .themebtn{position:fixed;top:14px;right:14px;z-index:99;font:600 11px/1 Arial,Helvetica,sans-serif;
    letter-spacing:.05em;padding:7px 11px;border-radius:5px;cursor:pointer;
    border:1px solid var(--line);background:var(--bg-card,var(--alt));color:var(--slate)}
  .themebtn:hover{border-color:var(--accent);color:var(--accent)}
</style>
<script>(function(){try{var t=localStorage.getItem('nmai-theme');if(t){document.documentElement.setAttribute('data-theme',t);}}catch(e){}})();</script>
</head>
<body>
<div class="wrap">
  <h1>AI Cost Watch</h1>
  <p class="sub" id="sub"></p>
  <p class="stamp" id="stamp"></p>

  <div class="signal">
    <span class="lab">Signal</span>
    <span class="val" id="sigval"><span class="dot"></span><span id="sigtxt"></span></span>
    <span class="note" id="signote"></span>
  </div>

  <div class="controls">
    <div class="ctl">
      <label>View</label>
      <div class="seg" id="viewseg">
        <button data-v="edition" class="on">By edition</button>
        <button data-v="indicator">By indicator across editions</button>
      </div>
    </div>
    <div class="ctl" id="editionctl">
      <label>Edition</label>
      <div class="seg" id="editionseg"></div>
    </div>
    <div class="ctl hide" id="indicatorctl">
      <label>Indicator</label>
      <select id="indsel"></select>
    </div>
  </div>

  <div id="editionview"></div>
  <div id="indicatorview" class="hide"></div>

  <div class="foot" id="foot"></div>
</div>

<script>
const DATA = __DATA__;
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const doiUrl = d => 'https://doi.org/' + String(d).replace(/^10\.5281\/zenodo\./i,'10.5281/zenodo.');

// header
$('#sub').textContent = DATA.series.subtitle;
$('#stamp').innerHTML = 'Series concept DOI (always resolves to the latest issue): '
  + '<a href="' + doiUrl(DATA.series.concept_doi) + '" target="_blank" rel="noopener">'
  + esc(DATA.series.concept_doi) + '</a> &middot; ' + esc(DATA.series.author)
  + ' &middot; ORCID <a href="https://orcid.org/' + esc(DATA.series.orcid)
  + '" target="_blank" rel="noopener">' + esc(DATA.series.orcid) + '</a> &middot; CC BY 4.0'
  + '<br><span style="font-style:italic">AI disclosure: the research is the author's; this text was drafted with AI assistance and reviewed by the author. The model, and the conflict it creates, are named in the Conflict of interest section of the linked issue.</span>';

// signal spine
const anyTrig = DATA.issues.some(i => i.trigger);
$('#sigtxt').textContent = anyTrig ? 'TRIGGER FIRED' : 'Expansion, no trigger';
if (anyTrig){ $('#sigval').style.color = 'var(--bad)'; $('#sigval').querySelector('.dot').style.background = 'var(--bad)'; }
$('#signote').innerHTML = '<b>' + esc(DATA.series.signal_name) + '.</b> ' + esc(DATA.series.signal_note)
  + ' Read across ' + DATA.issues.length + ' issues to date.';

// edition buttons
const eseg = $('#editionseg');
DATA.issues.forEach((it, ix) => {
  const b = document.createElement('button');
  b.textContent = 'Issue ' + it.n;
  b.dataset.ix = ix;
  if (ix === DATA.issues.length - 1) b.classList.add('on');
  b.onclick = () => { eseg.querySelectorAll('button').forEach(x=>x.classList.remove('on')); b.classList.add('on'); renderEdition(ix); };
  eseg.appendChild(b);
});

function renderEdition(ix){
  const it = DATA.issues[ix];
  const badge = it.trigger ? '<span class="badge trig">'+esc(it.status)+'</span>'
                           : '<span class="badge exp">'+esc(it.status)+' &middot; no trigger</span>';
  let h = '<div class="card"><div class="head">';
  h += '<h2>Issue ' + it.n + ': ' + esc(it.week) + badge + '</h2>';
  h += '<div class="meta">Published ' + esc(it.pub) + ' &middot; <a href="' + doiUrl(it.doi)
     + '" target="_blank" rel="noopener">' + esc(it.doi) + '</a></div>';
  h += '</div><div class="body">';
  h += '<p class="thread">' + esc(it.thread) + '</p>';
  h += '<div class="subh">What moved</div><ul class="dev">';
  it.developments.forEach(d => h += '<li>' + esc(d) + '</li>');
  h += '</ul>';
  h += '<div class="net"><b>Net read.</b> ' + esc(it.net_read) + '</div>';
  h += '<div class="subh">Indicators watched next</div><ul class="watch">';
  it.watching.forEach(w => h += '<li>' + esc(w) + '</li>');
  h += '</ul></div></div>';
  $('#editionview').innerHTML = h;
}

// indicator select
const isel = $('#indsel');
DATA.indicators.forEach((ind, ix) => {
  const o = document.createElement('option'); o.value = ix; o.textContent = ind.name; isel.appendChild(o);
});
isel.onchange = () => renderIndicator(+isel.value);

function issueMeta(n){ return DATA.issues.find(i => i.n === n) || {}; }
function renderIndicator(ix){
  const ind = DATA.indicators[ix];
  let h = '<div class="card"><div class="head"><h2>' + esc(ind.name) + '</h2>';
  h += '<div class="meta">' + esc(ind.unit) + '</div></div><div class="body">';
  h += '<p class="thread">' + esc(ind.note) + '</p>';
  h += '<table><thead><tr><th>Edition</th><th>Reading</th><th>Detail</th></tr></thead><tbody>';
  ind.readings.forEach(r => {
    const m = issueMeta(r.issue);
    h += '<tr><td class="iss">Issue ' + r.issue + '<br><span style="font-size:11px">' + esc(m.week||'') + '</span></td>'
       + '<td class="val">' + esc(r.value) + '</td>'
       + '<td>' + esc(r.note||'') + '</td></tr>';
  });
  h += '</tbody></table>';
  const seen = ind.readings.map(r=>r.issue);
  const missing = DATA.issues.map(i=>i.n).filter(n=>!seen.includes(n));
  if (missing.length) h += '<p style="font-size:12px;color:var(--slate);margin-top:10px">Not separately logged in issue'
    + (missing.length>1?'s ':' ') + missing.join(', ') + '.</p>';
  h += '</div></div>';
  $('#indicatorview').innerHTML = h;
}

// view toggle
$('#viewseg').querySelectorAll('button').forEach(b => {
  b.onclick = () => {
    $('#viewseg').querySelectorAll('button').forEach(x=>x.classList.remove('on')); b.classList.add('on');
    const ed = b.dataset.v === 'edition';
    $('#editionview').classList.toggle('hide', !ed);
    $('#indicatorview').classList.toggle('hide', ed);
    $('#editionctl').classList.toggle('hide', !ed);
    $('#indicatorctl').classList.toggle('hide', ed);
  };
});

$('#foot').innerHTML = '<b>Method.</b> Each edition is a frozen, dated note; every figure is sourced in the '
  + 'linked paper and stated at its true tier (vendor claims labelled by the seller\'s business model, not treated as findings). '
  + 'This front-end embeds the frozen dataset verbatim and is regenerated by <code>build.py</code>; the citable record is the Zenodo DOI per issue, '
  + 'and the series concept DOI above always resolves to the latest. '
  + '<br><b>Conflict of interest.</b> The series is produced with assistance from an Anthropic model, and Anthropic is among the companies it tracks '
  + '(Claude pricing, run-rate revenue, the S-1, the Fable/Mythos suspension, custom-chip talks). Any reading that touches Anthropic is non-neutral; '
  + 'primary and vendor-independent sources are preferred. This is independent analysis, not investment advice.';

// initial paint
renderEdition(DATA.issues.length - 1);
renderIndicator(0);
</script>
<script>(function(){
  var b=document.createElement('button');b.className='themebtn';
  function lbl(){b.textContent=(document.documentElement.getAttribute('data-theme')==='dark')?'\u25D1 LIGHT':'\u25D1 DARK';}
  b.onclick=function(){var d=document.documentElement.getAttribute('data-theme')==='dark';
    var n=d?'light':'dark';document.documentElement.setAttribute('data-theme',n);
    try{localStorage.setItem('nmai-theme',n);}catch(e){}lbl();};
  lbl();document.body.appendChild(b);
})();</script>
</body>
</html>
"""

def main():
    html = TEMPLATE.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
    out = HERE / "index.html"
    out.write_text(html, encoding="utf-8")
    print("wrote", out, "(", len(DATA["issues"]), "issues,", len(DATA["indicators"]), "indicators )")

if __name__ == "__main__":
    main()
