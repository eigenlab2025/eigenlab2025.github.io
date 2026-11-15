#!/usr/bin/env python3
"""Build a dependency-free, multilingual site and a self-contained review copy."""
import base64
import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'docs'
COPY = json.loads((ROOT / 'content/copy.json').read_text())
MEMBERS = json.loads((ROOT / 'content/members.json').read_text())
PUBS = json.loads((ROOT / 'content/publications.json').read_text())
PAGES = ['home', 'research', 'people', 'publications', 'life', 'join', 'contact', 'projects']
PROJECTS = json.loads((ROOT / 'content/projects.json').read_text())
PERSONAL = 'https://sites.google.com/view/xunshen/home'
SCHOLAR = 'https://scholar.google.com/citations?user=TPQUTVsAAAAJ&hl=ja'
RESEARCHMAP = 'https://researchmap.jp/shinjin'
e = html.escape

def link(lang, page, label, cls='', section=''):
    name = 'index' if page == 'home' else page
    anchor = f'#{section}' if section else ''
    return f'<a class="{cls}" href="../{lang}/{name}.html{anchor}" data-route="{lang}/{page}" data-section="{section}">{label}</a>'

def external(url, text, cls=''):
    return f'<a class="{cls}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{text}<span class="visually-hidden"> (external link)</span></a>'

def arrow(label):
    return label + '<span class="arrow" aria-hidden="true">↗</span>'

def pic(name, alt, lazy=True):
    return f'<img src="../assets/{name}" data-asset="{name}" alt="{e(alt)}" loading="eager" decoding="async">'

def logo():
    return '<svg class="brand-mark" viewBox="0 0 40 42" aria-hidden="true"><path d="M4 35V9M4 35H33" fill="none" stroke="#8d9d78" stroke-width="1.3"/><path d="M4 35L27 7M4 35L34 23" stroke="#245d49" stroke-width="2.6" fill="none"/><path d="M20 10L27 7L26 15M27 21L34 23L29 29" stroke="#245d49" stroke-width="2.6" fill="none"/></svg>'

def hero_art(c):
    a=c['art']
    return f'''<figure class="hero-art" aria-label="{e(' / '.join(a[:3]))}">
    <svg viewBox="0 0 500 540" role="img" aria-label="{e(' / '.join(a))}">
    <defs><pattern id="grid" width="35" height="35" patternUnits="userSpaceOnUse"><path d="M35 0H0V35" fill="none" stroke="#c7d5bc" stroke-width=".65"/></pattern></defs>
    <rect x="20" y="20" width="460" height="450" fill="url(#grid)" opacity=".65"/>
    <g stroke="#b7c9a7" fill="none" stroke-width="1"><ellipse cx="291" cy="262" rx="192" ry="109" transform="rotate(-34 291 262)"/><ellipse cx="291" cy="262" rx="165" ry="88" transform="rotate(-34 291 262)"/><ellipse cx="291" cy="262" rx="136" ry="67" transform="rotate(-34 291 262)"/><ellipse cx="291" cy="262" rx="105" ry="48" transform="rotate(-34 291 262)"/><ellipse cx="291" cy="262" rx="70" ry="31" transform="rotate(-34 291 262)"/></g>
    <path d="M72 405C137 400 152 274 220 270S305 267 404 142L440 188C364 305 296 340 233 327S140 461 72 439Z" fill="#d3e4b6" opacity=".85"/>
    <path d="M72 424C126 418 160 293 225 299S331 291 422 165" class="curve" fill="none" stroke="#245d49" stroke-width="3"/>
    <path d="M225 299C290 334 351 398 425 410" fill="none" stroke="#9eaf8c" stroke-width="1.4" stroke-dasharray="5 6"/>
    <path d="M226 95V430" stroke="#a7b79a" stroke-dasharray="3 7"/>
    <g fill="#245d49"><circle cx="74" cy="424" r="4"/><circle cx="99" cy="412" r="4"/><circle cx="126" cy="385" r="4"/><circle cx="151" cy="347" r="4"/><circle cx="176" cy="315" r="4"/><circle cx="202" cy="301" r="4"/></g>
    <circle cx="226" cy="299" r="10" fill="#f8f9f3" stroke="#245d49" stroke-width="2"/>
    <circle cx="422" cy="165" r="9" fill="#cce883" stroke="#245d49" stroke-width="2"/>
    <path d="M344 166L407 166" stroke="#245d49" stroke-width="1"/><path d="M339 149L283 149" stroke="#245d49" stroke-width="1"/>
    <g font-family="Arial, sans-serif" fill="#245d49" font-size="10" letter-spacing="1.5"><text x="69" y="461">{a[0]}</text><text x="257" y="457">{a[1]}</text><text x="282" y="139">{a[2]}</text></g>
    </svg><figcaption class="art-caption"><span>EIGEN LAB</span><span>{a[3]}</span></figcaption></figure>'''

def project_art(idx):
    name=['theme-understanding.webp','theme-safety.webp','theme-collaboration.webp'][idx]
    return '<div class="project-visual theme-illustration" aria-hidden="true">'+pic(name,'')+'</div>'

def domain_icon(i):
    paths=['<path d="M3 17h7l4-9 5 17 4-8h6"/><path d="M7 5C1 7 0 13 4 19L16 30 28 19C34 10 27 1 20 6L16 9 12 6Z"/>','<path d="M16 30V12M16 12L4 7M16 12L23 1M16 12L28 21"/><circle cx="16" cy="12" r="2"/><path d="M10 30H22"/>','<path d="M4 23V14L9 6h15l5 8v9Z"/><path d="M4 15h25"/><circle cx="9" cy="23" r="3"/><circle cx="24" cy="23" r="3"/>']
    return f'<svg viewBox="0 0 34 34" aria-hidden="true">{paths[i]}</svg>'

def header(lang,page,c):
    nav=''.join(link(lang,p,c['nav'][PAGES.index(p)]).replace('<a ', '<a aria-current="page" ',1) if p==page else link(lang,p,c['nav'][PAGES.index(p)]) for p in ['research','projects','people','publications','life','join','contact'])
    languages=''.join(link(l,page,label).replace('<a ',f'<a lang="{COPY[l]["lang"]}" aria-current="{str(l==lang).lower()}" ',1) for l,label in [('ja','日本語'),('en','EN'),('zh','中文')])
    return f'''<a class="skip-link" href="#main">{c['skip']}</a><header class="site-header"><div class="container header-inner">{link(lang,'home',logo()+'<div class="brand-name">EIGEN LAB<span class="brand-sub">'+c['lab']+'</span></div>','brand')}<button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">{c['menu']}</button><nav id="main-nav" class="main-nav" aria-label="{c['menu']}">{nav}</nav><nav class="languages" aria-label="Language">{languages}</nav></div></header>'''

def footer(lang,c):
    links=external(PERSONAL,c['personal'])+external(SCHOLAR,'Google Scholar')+link(lang,'contact',c['nav'][6])
    return f'''<footer class="site-footer"><div class="container"><div class="footer-top"><div class="footer-info"><div class="brand-name">EIGEN LAB</div>{c['footerDescription']}<p>{c['university']}</p></div><div class="footer-links">{links}</div></div><div class="footer-bottom"><span>{c['footerCopyright']}</span><span>{c['footerLocation']}</span></div></div></footer>'''

def cta(lang,c):
    return f'<section class="cta"><div class="container cta-inner"><div><h2>{c["ctaTitle"]}</h2><p>{c["ctaText"]}</p></div>{link(lang,"join",arrow(c["joinBtn"]),"button light")}</div></section>'

def page_head(c,idx,lead):
    return f'<div class="page-head"><div class="eyebrow">EIGEN LAB / {PAGES[idx].upper()}</div><h1>{c["nav"][idx]}</h1><p>{c[lead]}</p></div>'

def home(lang,c):
    pillars=''.join(f'<article class="pillar"><span class="num">0{i+1}</span><div><h3>{c["pillarTitles"][i]}</h3><p>{c["pillarText"][i]}</p><div class="tags">'+''.join(f'<span>{t}</span>' for t in c['pillarTags'][i])+'</div></div></article>' for i in range(2))
    domains=''.join(f'<div class="domain">{domain_icon(i)}<span>{x}</span></div>' for i,x in enumerate(c['domains']))
    themes=''.join(f'<article class="project">{project_art(i)}<div class="project-body"><div class="eyebrow">{c["projectTags"][i]}</div><h3>{c["projectTitles"][i]}</h3><p>{c["projectText"][i]}</p>{link(lang,"research",arrow(c["learn"]),"text-link",["prediction","decisions","adaptation"][i])}</div></article>' for i in range(3))
    news=''.join(f'<article class="news-item"><time>{x[0]}</time><div><span class="news-category">{x[1]}</span><h3>'+link(lang,'life' if i<2 else 'publications',x[2],section=['nus','fujitsu','ogsrl'][i])+f'</h3><p>{x[3]}</p></div></article>' for i,x in enumerate(c['news']))
    featured=''.join(project_preview(lang,c,x) for x in PROJECTS if x['featured'])
    return f'''<div class="container"><section class="hero"><div class="hero-copy"><div><div class="eyebrow">{c['homeEyebrow']}</div><h1>{c['hero']}</h1><p class="affiliation">{c['heroAffiliation']}</p></div><div class="hero-intro"><p class="lead">{c['heroLead']}</p><div class="actions">{link(lang,'research',arrow(c['researchBtn']),'button')}{link(lang,'projects',arrow(c['fundedBtn']),'text-link')}</div></div></div><figure class="hero-illustration">{pic('hero-science.webp',c['heroImageAlt'],False)}<figcaption>{c['illustrationCaption']}</figcaption></figure></section><a class="feature-strip" href="../{lang}/publications.html#ogsrl" data-route="{lang}/publications" data-section="ogsrl"><span class="tag">RESEARCH HIGHLIGHT</span><p>{c['feature']}<small>{c['featureNote']}</small></p><span class="feature-arrow" aria-hidden="true">↗</span></a><section class="section"><div class="section-head"><div><div class="eyebrow">{c['researchEyebrow']}</div><h2>{c['researchTitle']}</h2></div><p>{c['researchIntro']}</p></div><div class="pillars">{pillars}</div><div class="domain-band">{domains}</div></section></div><section class="section section-tint"><div class="container"><div class="section-head"><div><div class="eyebrow">{c['projectsEyebrow']}</div><h2>{c['projectsTitle']}</h2></div>{link(lang,'research',arrow(c['researchBtn']),'text-link')}</div><div class="project-grid">{themes}</div></div></section><section class="section"><div class="container"><div class="section-head"><div><div class="eyebrow">{c['fundedEyebrow']}</div><h2>{c['fundedTitle']}</h2></div>{link(lang,'projects',arrow(c['fundedBtn']),'text-link')}</div><div class="funded-grid">{featured}</div></div></section><section class="section section-tint"><div class="container news-grid"><div><div class="eyebrow">UPDATES</div><h2>{c['newsTitle']}</h2><p style="font-size:14px;color:var(--muted);margin-top:20px">{c['newsIntro']}</p></div><div class="news-list">{news}</div></div></section><section class="section"><div class="container life-teaser">{pic('source-p6-2.webp',c['story2Caption'])}<div><div class="eyebrow">LIFE IN THE LAB</div><h2>{c['lifeTitle']}</h2><p>{c['lifeText']}</p><div class="actions">{link(lang,'life',arrow(c['lifeBtn']),'text-link')}</div></div></div></section>{cta(lang,c)}'''


def research(lang,c):
    rows=''
    evidence=[['reachable','wind'],['optimization','flipping','ogsrl'],['j025','j003']]
    for i,x in enumerate(c['researchSections']):
        refs=[]
        for pub_id in evidence[i]:
            pub=next((z for z in PUBS if z['id']==pub_id),None)
            if pub:refs.append(link(lang,'publications',e(pub['title']),'evidence-link',pub_id))
        rows+=f'<article class="research-row" id="{["prediction","decisions","adaptation"][i]}"><span class="num">0{i+1}</span><div><div class="eyebrow">{c["projectTags"][i]}</div><h2>{x[0]}</h2><p>{x[1]}</p><h3>{x[2]}</h3><ul>'+''.join(f'<li>{q}</li>' for q in x[3:])+f'</ul><div class="evidence"><h3>{c["evidence"]}</h3>'+''.join(refs)+f'</div></div>{project_art(i)}</article>'
    nodes=''.join(f'<div class="flow-node"><span class="num">0{i+1}</span><h3>{x[0]}</h3><p>{x[1]}</p></div>' for i,x in enumerate(c['flowNodes']))
    apps=''.join(f'<article><h3>{x[0]}</h3><p>{x[1]}</p></article>' for x in c['applicationItems'])
    return f'<div class="container">{page_head(c,1,"researchLead")}<section class="science-flow"><h2>{c["flowTitle"]}</h2><div class="flow-grid">{nodes}</div><p class="flow-feedback">↶ {c["flowFeedback"]}</p><p class="flow-foundation">{c["flowFoundation"]}</p></section>{rows}<section class="application-section"><h2>{c["applicationTitle"]}</h2><div class="application-grid">{apps}</div></section><aside class="principle"><h2>{c["researchMethodTitle"]}</h2><p>{c["researchMethodText"]}</p></aside></div>{cta(lang,c)}'


def member_card(m,lang,c):
    native=f'<span class="member-native">{e(m["native_name"])}</span>' if m.get('native_name') else ''
    affiliation=''
    if m.get('affiliation'):
        affiliation='<div class="member-affiliation">'+'<br>'.join(e(x) for x in m['affiliation'][lang])+f'</div><span class="coadvised-label">{c["coadvisedBy"]}</span>'
    return f'<article class="member">{pic(m["image"],m["name"])}<h3>{e(m["name"])}{native}</h3><p>{c["topics"][m["topic"]]}</p>{affiliation}</article>'

def people(lang,c):
    groups=''
    for group in ['doctoral','coadvised','masters','undergrad']:
        members=[m for m in MEMBERS if m['group']==group]
        cards=''.join(member_card(m,lang,c) for m in members)
        groups+=f'<section class="member-group"><div class="group-heading"><h2>{c["groups"][group]}</h2><span>{c["groupLabels"][group]}</span></div><div class="members-grid">{cards}</div></section>'
    return f'''<div class="container">{page_head(c,2,'peopleLead')}<section class="faculty"><div class="faculty-sign">{pic("xun-shen.png",c["facultyTitle"],False)}<div><h2>{c['facultyTitle']}</h2><p>{c['facultyRole']}</p></div></div><div class="faculty-body"><div class="eyebrow">PRINCIPAL INVESTIGATOR</div><h3>{c['facultyHeading']}</h3><p>{c['facultyBio']}</p><p>{c['facultyDegrees']}</p>{affiliations(c)}<div class="actions">{external(PERSONAL,arrow(c['personal']),'text-link')}{external(SCHOLAR,arrow('Google Scholar'),'text-link')}</div><p style="margin-top:25px"><a href="mailto:shen@go.tuat.ac.jp">shen@go.tuat.ac.jp</a></p></div></section><p class="roster-note">{c['rosterNote']}</p>{groups}</div>{cta(lang,c)}'''

def publications(lang,c):
    rows=''
    ordered=sorted(PUBS,key=lambda p:(-(p.get('year') or 9999),{'journal':0,'conference':1,'talk':2,'thesis':3,'patent':4}[p['type']],p['id']))
    for p in ordered:
        students=p.get('student_authors',[])
        authors=e(p['authors']).replace('Xun Shen','<strong>Xun Shen</strong>')
        co_supervised=p.get('co_supervised_authors',[])
        for student in sorted(students,key=len,reverse=True):
            marker='‡' if student in co_supervised else '†'
            authors=authors.replace(e(student),f'<span class="student-author">{e(student)}<sup>{marker}</sup></span>')
        year=str(p.get('year') or c['noYear'])
        title=external(p['url'],e(p['title'])) if p.get('url') else e(p['title'])
        outgoing=external(p['url'],'↗<span class="visually-hidden">'+c['paper']+'</span>','pub-out') if p.get('url') else '<span></span>'
        note=p.get('note',{}).get(lang,'')
        status=p.get('status','published')
        badge=f'<span class="student-badge">{c["studentFirst"] if p.get("student_first") else c["studentCoauthor"]}</span>' if students else ''
        if co_supervised:badge+=f'<span class="coadvised-badge">{c["coadvisedPaper"]}</span>'
        rows+=f'''<article class="publication" id="{p['id']}" data-year="{p.get('year') or ''}" data-type="{p['type']}" data-student="{str(bool(students)).lower()}"><div class="pub-year">{year}</div><div><div class="pub-tag"><span>{c[p['type']]}</span><span>{c.get(status,status)}</span>{badge}</div><h2>{title}</h2><p class="pub-authors">{authors}</p><p class="pub-venue">{e(p['venue'])}</p>{f'<p class="pub-note">{note}</p>' if note else ''}</div>{outgoing}</article>'''
    years=sorted({p['year'] for p in PUBS if p.get('year')},reverse=True)
    yoptions=''.join(f'<option value="{y}">{y}</option>' for y in years)
    types=''.join(f'<option value="{x}">{c[x]}</option>' for x in ['journal','conference','talk','thesis','patent'])
    papers=sum(p['type'] in ['journal','conference'] for p in PUBS);student_count=sum(bool(p.get('student_authors')) for p in PUBS)
    stats=f'<div class="pub-stats"><div><strong>{papers}</strong><span>{c["paperCount"]}</span></div><div><strong>{student_count}</strong><span>{c["studentCount"]}</span></div><div><strong>{len(PUBS)-papers}</strong><span>{c["otherCount"]}</span></div></div>'
    return f'''<div class="container">{page_head(c,3,'publicationsLead')}{stats}<p class="student-legend">{c['studentLegend']}</p><div class="filters" role="search"><label class="visually-hidden" for="pub-search">{c['search']}</label><input id="pub-search" type="search" placeholder="{c['search']}"><label class="visually-hidden" for="pub-type">{c['allTypes']}</label><select id="pub-type"><option value="">{c['allTypes']}</option>{types}</select><label class="visually-hidden" for="pub-year">{c['allYears']}</label><select id="pub-year"><option value="">{c['allYears']}</option>{yoptions}</select><label class="student-toggle"><input type="checkbox" id="pub-student">{c['studentFilter']}</label><button id="pub-reset" type="button">{c['resetFilters']}</button><span class="filter-count" aria-live="polite"><span id="pub-count">{len(PUBS)}</span> {c['results']}</span></div><div id="publication-list">{rows}</div><p id="empty-results" class="empty-results" hidden>{c['none']}</p><div class="archive-note"><p>{c['publicationNote']}</p><div class="actions">{external(PERSONAL,arrow(c['record']),'text-link')}{external(SCHOLAR,arrow('Google Scholar'),'text-link')}{external(RESEARCHMAP,arrow('researchmap'),'text-link')}</div></div></div>'''


def steps(c):
    return '<div class="steps">'+''.join(f'<article class="step"><span class="num">0{i+1}</span><h3>{x[0]}</h3><p>{x[1]}</p></article>' for i,x in enumerate(c['steps']))+'</div>'

def life(lang,c):
    return f'''<div class="container">{page_head(c,4,'lifeLead')}<article class="story" id="nus"><figure>{pic('source-p5-2.webp',c['story1Caption'],False)}<figcaption>{c['story1Caption']}</figcaption></figure><div><div class="eyebrow">24–26 SEPTEMBER 2026 · SINGAPORE</div><h2>{c['story1Title']}</h2><p>{c['story1Text']}</p></div></article><article class="story reverse" id="fujitsu"><figure>{pic('source-p6-2.webp',c['story2Caption'])}<figcaption>{c['story2Caption']}</figcaption></figure><div><div class="eyebrow">FEBRUARY 2026 · LAB ACTIVITY</div><h2>{c['story2Title']}</h2><p>{c['story2Text']}</p></div></article></div><section class="section section-tint"><div class="container"><div class="section-head"><div><div class="eyebrow">OUR APPROACH</div><h2>{c['cultureTitle']}</h2></div><p>{c['cultureIntro']}</p></div>{steps(c)}</div></section>{cta(lang,c)}'''

def join(lang,c):
    cards=''.join(f'<article class="join-card"><h2>{x[0]}</h2><p>{x[1]}</p><ul>'+''.join(f'<li>{v}</li>' for v in x[2])+'</ul></article>' for x in c['joinCards'])
    faq=''.join(f'<details><summary>{x[0]}</summary><p>{x[1]}</p></details>' for x in c['faq'])
    admission_url='https://www.tuat.ac.jp/admission/' if lang=='ja' else 'https://www.tuat.ac.jp/en/admission/'
    return f'''<div class="container">{page_head(c,5,'joinLead')}<div class="join-grid">{cards}</div><section class="section-head"><div><div class="eyebrow">LEARN THROUGH RESEARCH</div><h2>{c['cultureTitle']}</h2></div><p>{c['cultureIntro']}</p></section>{steps(c)}<section class="contact-instruction"><h2>{c['emailTitle']}</h2><p>{c['emailIntro']}</p><a class="button" href="mailto:shen@go.tuat.ac.jp?subject=Eigen%20Lab%20inquiry">{arrow(c['contactBtn'])}</a></section><p class="archive-note">{c['admissionNote']}<br>{external(admission_url,c['admissions'])}</p><section class="faq"><h2>{c['faqTitle']}</h2>{faq}</section></div>'''

def contact(lang,c):
    return f'''<div class="container">{page_head(c,6,'contactLead')}<div class="contact-grid"><div><h2>{c['contactHeading']}</h2><p>{c['contactIntro']}</p><a class="contact-email" href="mailto:shen@go.tuat.ac.jp">shen@go.tuat.ac.jp</a><p>{c['university']}<br>{c['department']}<br>{c['graduate']}</p><div class="address"><h2>{c['addressHeading']}</h2><p>{c['addressText']}</p></div></div><aside class="contact-card"><h2>{c['visitTitle']}</h2><p>{c['visitText']}</p><dl><dt>{c['office']}</dt><dd>{c['officeValue']}</dd><dt>{c['studentRoom']}</dt><dd>{c['studentRoomValue']}</dd></dl>{external('https://www.tuat.ac.jp/',arrow(c['universityLink']),'text-link')}</aside></div><div class="principle"><h2>{c['linksTitle']}</h2><div class="actions" style="margin-top:0">{external(PERSONAL,arrow(c['personal']),'text-link')}{external(SCHOLAR,arrow('Google Scholar'),'text-link')}{external(RESEARCHMAP,arrow('researchmap'),'text-link')}</div></div></div>'''

def affiliations(c):
    vals=[c['department'],c['undergraduate'],c['graduate']]
    return '<section class="affiliations"><h2>'+c['affiliationTitle']+'</h2><dl>'+''.join(f'<div><dt>{lab}</dt><dd>{val}</dd></div>' for lab,val in zip(c['affiliationLabels'],vals))+'</dl></section>'

def project_preview(lang,c,p):
    return f'<article class="funded-card">{link(lang,"projects",pic(p["image"],p["tagline"][lang]),section=p["id"])}<div class="funded-card-body"><div class="eyebrow">{p["category"][lang]}</div><h3>{link(lang,"projects",p["tagline"][lang],section=p["id"])}</h3><p>{p["title"][lang]}</p><small>{p["grant"]} · {p["period"][lang]}</small>{link(lang,"projects",arrow(c["learn"]),"text-link",p["id"])}</div></article>'

def projects(lang,c):
    items='';past=''
    for p in PROJECTS:
        if not p['featured']:
            past+=f'<article class="past-project"><div class="eyebrow">{p["category"][lang]}</div><h3>{p["title"][lang]}</h3><p>{p["summary"][lang]}</p><small>{p["grant"]} · {p["period"][lang]}</small><div class="actions">{external(p["url"],arrow(c["projectSource"]),"text-link")}</div></article>'
            continue
        goals=''.join(f'<li>{x}</li>' for x in p['goals'][lang])
        items+=f'<article class="funded-project" id="{p["id"]}"><div class="funded-intro"><div><div class="eyebrow">{p["category"][lang]}</div><h2>{p["tagline"][lang]}</h2><h3>{p["title"][lang]}</h3><p class="project-meta">{p["grant"]} · {p["period"][lang]}<br>{c["projectPI"]}</p></div><figure>{pic(p["image"],p["tagline"][lang])}</figure></div><div class="funded-details"><div><p class="project-summary">{p["summary"][lang]}</p><p class="institutional-note">{p["institutional_note"][lang]}</p><div class="actions">{external(p["url"],arrow(c["projectSource"]),"text-link")}</div></div><div class="project-goals"><h3>{c["projectGoals"]}</h3><ol>{goals}</ol></div></div></article>'
    return f'<div class="container">{page_head(c,7,"fundedLead")}{items}<p class="illustration-note">{c["projectIllustrationNote"]}</p><section class="past-section"><h2>{c["projectPast"]}</h2><div class="past-grid">{past}</div></section></div>{cta(lang,c)}'

RENDER={'projects':projects,'home':home,'research':research,'people':people,'publications':publications,'life':life,'join':join,'contact':contact}

def body(lang,page):
    c=COPY[lang]
    return header(lang,page,c)+f'<main id="main" tabindex="-1">{RENDER[page](lang,c)}</main>'+footer(lang,c)

JS='''
(() => {
 const app = document.getElementById('app');
 const isPreview = typeof REVIEW_PAGES !== 'undefined';
 function filterPublications(){
  const q=(document.getElementById('pub-search')?.value||'').trim().toLowerCase();
  const type=document.getElementById('pub-type')?.value||'';
  const year=document.getElementById('pub-year')?.value||'';
  const student=document.getElementById('pub-student')?.checked||false;
  let count=0;
  document.querySelectorAll('.publication').forEach(p=>{const show=(!type||p.dataset.type===type)&&(!year||p.dataset.year===year)&&(!student||p.dataset.student==='true')&&p.textContent.toLowerCase().includes(q);p.hidden=!show;count+=show;});
  const counter=document.getElementById('pub-count');if(counter)counter.textContent=count;
  const empty=document.getElementById('empty-results');if(empty)empty.hidden=count!==0;
 }
 function renderPreview(){
  const parts=location.hash.slice(1).split('/');
  const lang=['ja','en','zh'].includes(parts[0])?parts[0]:'ja';
  const page=REVIEW_PAGES[lang+'/'+parts[1]]?parts[1]:'home';
  const item=REVIEW_PAGES[lang+'/'+page];
  document.documentElement.lang=item.lang;document.title=item.title;
  document.body.dataset.lang=lang;document.body.dataset.page=page;
  app.innerHTML=item.html;
  app.querySelectorAll('a[data-route]').forEach(a=>{a.href='#'+a.dataset.route+(a.dataset.section?'/'+a.dataset.section:'');});
  app.querySelectorAll('[data-asset]').forEach(im=>{im.src=REVIEW_ASSETS[im.dataset.asset];});
  document.getElementById('review-label').textContent=REVIEW_COPY[lang].reviewLabel;
  document.getElementById('review-open').textContent=REVIEW_COPY[lang].reviewButton;
  const dialog=document.getElementById('review-dialog');
  dialog.innerHTML='<h2>'+REVIEW_COPY[lang].reviewTitle+'</h2><p>'+REVIEW_COPY[lang].reviewIntro+'</p><ol>'+REVIEW_COPY[lang].reviewItems.map(x=>'<li>'+x+'</li>').join('')+'</ol><button class="button" id="review-close">'+REVIEW_COPY[lang].close+'</button>';
  window.scrollTo(0,0);
  if(parts[2])requestAnimationFrame(()=>document.getElementById(parts[2])?.scrollIntoView());
 }
 document.addEventListener('click',ev=>{
  if(isPreview&&ev.target.closest('.skip-link')){ev.preventDefault();document.getElementById('main').focus();document.getElementById('main').scrollIntoView();return;}
  const toggle=ev.target.closest('.menu-toggle');if(toggle){const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',open);document.getElementById('main-nav').classList.toggle('open',open);return;}
  const route=ev.target.closest('a[data-route]');
  if(route&&isPreview&&!ev.ctrlKey&&!ev.metaKey&&!ev.shiftKey){ev.preventDefault();const target=route.dataset.route+(route.dataset.section?'/'+route.dataset.section:'');if(location.hash.slice(1)===target){window.scrollTo(0,0);}else{location.hash=target;}return;}
  if(ev.target.closest('#pub-reset')){document.getElementById('pub-search').value='';document.getElementById('pub-type').value='';document.getElementById('pub-year').value='';document.getElementById('pub-student').checked=false;filterPublications();}
  if(ev.target.closest('#review-open'))document.getElementById('review-dialog').showModal();
  if(ev.target.closest('#review-close'))document.getElementById('review-dialog').close();
 });
 document.addEventListener('keydown',ev=>{if(ev.key==='Escape'){document.querySelector('.main-nav')?.classList.remove('open');document.querySelector('.menu-toggle')?.setAttribute('aria-expanded','false');}});
 document.addEventListener('input',ev=>{if(ev.target.id==='pub-search')filterPublications();});
 document.addEventListener('change',ev=>{if(['pub-type','pub-year','pub-student'].includes(ev.target.id))filterPublications();});
 if(isPreview){window.addEventListener('hashchange',renderPreview);renderPreview();}
})();
'''

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--production', action='store_true')
    parser.add_argument('--base-url', default='https://eigenlab2025.github.io')
    args=parser.parse_args()
    base=args.base_url.rstrip('/')
    robots='index,follow' if args.production else 'noindex,nofollow'
    DIST.mkdir(exist_ok=True)
    (DIST/'assets/site.js').write_text(JS)
    page_data={}
    for lang,c in COPY.items():
        folder=DIST/lang;folder.mkdir(exist_ok=True)
        for i,page in enumerate(PAGES):
            title=c['nav'][i]+' | Eigen Lab · '+c['university']
            content=body(lang,page)
            filename='index' if page=='home' else page
            prefix=base if args.production else '..'
            hreflangs=''.join(f'<link rel="alternate" hreflang="{COPY[l]["lang"]}" href="{prefix}/{l}/{filename}.html">' for l in COPY)
            canonical=f'<link rel="canonical" href="{base}/{lang}/{filename}.html"><link rel="alternate" hreflang="x-default" href="{base}/ja/{filename}.html">' if args.production else ''
            doc=f'''<!doctype html><html lang="{c['lang']}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="{robots}"><title>{e(title)}</title><meta name="description" content="{e(c['heroLead'])}">{canonical}{hreflangs}<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../assets/site.css"><script src="../assets/site.js" defer></script></head><body data-lang="{lang}" data-page="{page}"><div id="app">{content}</div></body></html>'''
            (folder/f'{filename}.html').write_text(doc)
            page_data[f'{lang}/{page}']={'html':content,'title':title,'lang':c['lang']}
    (DIST/'index.html').write_text('<!doctype html><html lang="ja"><head><meta charset="UTF-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url=ja/index.html"><title>Eigen Lab</title></head><body><a href="ja/index.html">日本語</a> · <a href="en/index.html">English</a> · <a href="zh/index.html">中文</a></body></html>')
    (DIST/'.nojekyll').write_text('')
    (DIST/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
    if args.production:
        (DIST/'index.html').write_text(f'<!doctype html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow"><link rel="canonical" href="{base}/ja/index.html"><meta http-equiv="refresh" content="0;url=ja/index.html"><title>Eigen Lab | Shen Laboratory</title></head><body><a href="ja/index.html">日本語</a> · <a href="en/index.html">English</a> · <a href="zh/index.html">中文</a></body></html>')
        (DIST/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n')
        urls=''.join(f'<url><loc>{base}/{l}/{"index" if p=="home" else p}.html</loc></url>' for l in COPY for p in PAGES)
        (DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>')
    (DIST/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="5" fill="#00876c"/><path d="M10 37L29 9M10 37L39 25M23 11L29 9L28 16M32 23L39 25L35 32" fill="none" stroke="#ffffff" stroke-width="2.7"/></svg>')
    if args.production:
        print(f'Built {len(page_data)} public pages at {base}.')
        return
    assets={p.name:'data:image/webp;base64,'+base64.b64encode(p.read_bytes()).decode() for p in (DIST/'assets').glob('*.webp') if p.name not in ['source-p5-1.webp','source-p6-1.webp']}
    css=(DIST/'assets/site.css').read_text()
    for font in (DIST/'assets').glob('*.woff2'):
        css=css.replace("url('"+font.name+"')", "url('data:font/woff2;base64,"+base64.b64encode(font.read_bytes()).decode()+"')")
    review_copy={lang:{k:v for k,v in c.items() if k.startswith('review') or k=='close'} for lang,c in COPY.items()}
    preview=f'''<!doctype html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Eigen Lab | Unpublished review</title><style>{css}</style></head><body><div class="review-bar"><strong id="review-label">UNPUBLISHED REVIEW · V2</strong><button id="review-open">Review notes</button></div><div id="app"></div><dialog id="review-dialog" class="review-dialog"></dialog><script>const REVIEW_PAGES={json.dumps(page_data,ensure_ascii=False)};const REVIEW_ASSETS={json.dumps(assets)};const REVIEW_COPY={json.dumps(review_copy,ensure_ascii=False)};</script><script>{JS}</script><noscript>Please enable JavaScript to use this self-contained review. The source package also contains static HTML pages.</noscript></body></html>'''
    (DIST/'review.html').write_text(preview)
    print(f'Built {len(page_data)} pages + standalone preview ({len(preview.encode())/1e6:.2f} MB).')

if __name__=='__main__':
    main()
