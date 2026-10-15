"""Render 2017.html / 2018.html / 2019.html / index.html from data/convai.json."""
import json, html, os, re
ROOT=os.path.join(os.path.dirname(__file__),'..')
D=json.load(open(os.path.join(ROOT,'data','convai.json')))
e=html.escape
YEARS=[('19','2019'),('18','2018'),('17','2017')]
ICON_CAL='<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>'
ICON_PIN='<svg viewBox="0 0 24 24"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>'
ICON_PDF='<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>'
def person(n,a,u,p=None):
    name=f'<a href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a>' if u else e(n)
    ini=''.join(w[0] for w in n.replace('-',' ').split()[:2]).upper()
    pic=f'<img class="face" src="{e(p)}" alt="" loading="lazy">' if p else f'<span class="face ini">{e(ini)}</span>'
    return f'<div class="person">{pic}<div><b>{name}</b><span>{e(a)}</span></div></div>'
def rail(cur):
    out=[]
    for k,y in YEARS:
        d=D[k]; on=' class="on"' if k==cur else ''
        out.append(f'<li{on}><a href="{y}.html"><span class="dot"></span><span><span class="y">{y}</span><br><span class="w">{e(d["city"].split(",")[0])} · {e(d["date"].replace(", "+y,""))}</span></span></a></li>')
    return '<ol>'+''.join(out)+'</ol>'
def paper(p):
    pdf=f'<a class="pdf" href="{e(p["pdf"])}" target="_blank" rel="noopener">{ICON_PDF} PDF</a>' if p.get('pdf') else ''
    award='<span class="award">Best paper</span>' if p.get('award') else ''
    return f'<li><div><div class="pt">{e(p["title"])}{award}</div><div class="pa">{e(p["authors"])}</div></div>{pdf}</li>'
def sched(items):
    out=[]
    for it in items:
        links=''.join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(l.strip("[ ").replace("Link",""))} ↗</a>' for l,u in it['links'])
        if not it['time']:
            out.append(f'<li class="sess">{links}</li>'); continue
        cls=' class="brk"' if re.search(r'break|lunch|poster session|hangup',it['what'],re.I) else ''
        out.append(f'<li{cls}><span class="t">{e(it["time"])}</span><span>{it["what"]}<span class="l">{links}</span></span></li>')
    return '<ul class="sched">'+''.join(out)+'</ul>'
def page(k):
    d=D[k]; y=str(d['year'])
    desc=''.join(f'<p>{p}</p>' for p in d['description'])
    dates=''.join(f'<div><div class="dl">{e(l)}</div><div class="dv">{v}</div></div>' for l,v in d['dates'] if l!='_note')
    notes=''.join(f'<p class="note">{v}</p>' for l,v in d['dates'] if l=='_note' and not v.endswith(':'))
    speakers=''.join(person(*x) for x in d['speakers'])
    chairs=''.join(person(*x) for x in d['chairs']); orgs=''.join(person(*x) for x in d['organizers'])
    talks=''.join(paper(p) for p in d['talks']); posters=''.join(paper(p) for p in d['posters'])
    pc=''.join(f'<div>{e(p)}</div>' for p in d['pc'])
    gallery=''.join(f'<figure><img src="{e(ph["src"])}" alt="{e(ph["caption"])}" loading="lazy"><figcaption>{e(ph["caption"])}</figcaption></figure>' for ph in d.get('photos',[]))
    photos_sec=f'<section id="photos"><div class="eyebrow">On the day</div><h2>Photos</h2><div class="gallery">{gallery}</div></section>' if gallery else ''
    photos_tab='<a href="#photos">Photos</a>' if gallery else ''
    bp=f'<p class="note">{e(d["best_paper_note"])}</p>' if d.get('best_paper_note') else ''
    stats=''.join(f'<span>{e(s.strip())}</span>' for s in d['stats'].split('·'))
    logo='assets/logo.png'
    vc=d.get('venue_credit') or {}
    credit=(f'<a class="credit" href="{e(vc["page"])}" target="_blank" rel="noopener">{e(d["location"].split(",")[0])} · photo: {e(vc["artist"][:40])} ({e(vc["license"])})</a>' if vc.get('artist') else f'<span class="credit">{e(d["location"].split(",")[0])}</span>')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Conversational AI Workshop · {d['conf']}</title>
<meta name="description" content="{d['edition']} Conversational AI workshop at {d['conf']}: Today's Practice and Tomorrow's Potential.">
<link rel="icon" href="{logo}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="banner"><div class="in"><img src="{logo}" alt=""><div class="t">Conversational AI</div></div></header>
<div class="layout">
  <aside class="rail">{rail(k)}</aside>
  <main class="main">
    <div class="hero photo" style="background-image:url('{e(d.get("venue_image",""))}');background-position:{e(d.get("venue_focus","center"))}">
      {credit}
      <div class="k">{d['conf']} workshop · {d['edition']} edition</div>
      <h1>Conversational AI: Today's Practice and Tomorrow's Potential</h1>
      <div class="meta"><span>{ICON_CAL}{e(d['date'])}</span><span>{ICON_PIN}<a href="{e(d['location_url'])}" target="_blank" rel="noopener">{e(d['location'])}</a>, {e(d['city'])}</span></div>
      <div class="stats">{stats}</div>
    </div>
    <nav class="tabs"><a href="#overview">Overview</a><a href="#speakers">Speakers</a><a href="#schedule">Schedule</a><a href="#papers">Accepted papers</a><a href="#cfp">Call for papers</a><a href="#organizers">Organizers</a><a href="#committee">Program committee</a>{photos_tab}</nav>
    <section id="overview"><div class="eyebrow">Overview</div><h2>About the workshop</h2><div class="card desc">{desc}</div></section>
    <section id="speakers"><div class="eyebrow">Invited</div><h2>Speakers</h2><div class="people">{speakers}</div></section>
    <section id="schedule"><div class="eyebrow">Program</div><h2>Schedule</h2>{sched(d['schedule'])}</section>
    <section id="papers"><div class="eyebrow">Contributed</div><h2>Accepted papers</h2>{bp}<div class="sub">Talks</div><ol class="papers">{talks}</ol><div class="sub">Posters</div><ol class="papers">{posters}</ol></section>
    <section id="cfp"><div class="eyebrow">Archive</div><h2>Call for papers</h2><div class="card desc">{''.join(f'<p>{p}</p>' for p in d['cfp'])}{notes}</div><div class="sub">Important dates</div><div class="dates">{dates}</div></section>
    <section id="organizers"><div class="eyebrow">People</div><h2>Organizers</h2><div class="sub">Co-chairs</div><div class="people">{chairs}</div><div class="sub">Organizing committee</div><div class="people">{orgs}</div></section>
    <section id="committee"><div class="eyebrow">Reviewers</div><h2>Program committee</h2><div class="pc">{pc}</div></section>
    {photos_sec}
  </main>
</div>
<footer>Conversational AI Workshop series, NeurIPS 2017 – 2019 · Organized by <a href="https://alborz-geramifard.com">Alborz Geramifard</a> and colleagues · Archived from the original workshop websites.</footer>
</body>
</html>'''
for k,y in YEARS:
    open(os.path.join(ROOT,f'{y}.html'),'w').write(page(k))
open(os.path.join(ROOT,'index.html'),'w').write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=2019.html"><title>Conversational AI Workshop</title><a href="2019.html">Conversational AI Workshop</a>')
print('built', [y for _,y in YEARS])
