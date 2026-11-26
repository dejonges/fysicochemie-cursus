#!/usr/bin/env python3
"""Zet de LaTeX-hoofdstukken van de cursus Fysico Chemie om naar Quarto-pagina's (.qmd).

De LaTeX (Overleaf) is de enige bron. Deze omzetting draait automatisch bij elke
wijziging (zie .github/workflows); de .qmd-hoofdstukken zelf worden niet bewaard.

Gebruik: python3 tex2qmd.py <map-met-main.tex> <quarto-map>

- Hoofdstukken en volgorde: de \\include-regels in main.tex.
- \\includegraphics{Figuren/naam}: figuur getekend met Python (functie naam() in _figuren/).
- \\includegraphics{Afbeeldingen/x.png}: gewone afbeelding; bestaat ze niet, dan
  verschijnt "Figuur in voorbereiding" met het bijschrift.
- \\interactief{naam}: voegt _interactief/naam.qmd in.
- \\begin{oplossing}...\\end{oplossing}: enkel online, als dichtgeklapt kader.
"""
import os, re, sys, subprocess, shutil, glob

SRC, OUT = sys.argv[1], sys.argv[2]

SLUGS = {  # tex-bestand -> naam van de webpagina (anders: kleine letters met streepjes)
    "Kwantum_uitgebreid": "kwantum",
}

def slug_van(tex):
    return SLUGS.get(tex) or re.sub(r'[^a-z0-9]+', '-', tex.lower()).strip('-')

def hoofdstukken():
    main = open(os.path.join(SRC, 'main.tex'), encoding='utf-8').read()
    main = re.sub(r'(?<!\\)%.*', '', main)
    return [(t.strip(), slug_van(t.strip())) for t in re.findall(r'\\include\{([^}]*)\}', main)]

CHAPTERS = hoofdstukken()

PANDOC = ['pandoc'] if shutil.which('pandoc') else ['quarto', 'pandoc']

# Python-figuren met @animatie (enkel online bewegend)
ANIMATIES = set()
for _py in glob.glob(os.path.join(OUT, '_figuren', 'h*.py')):
    ANIMATIES |= set(re.findall(r'^@animatie\b.*\n(?:@.*\n)*def (\w+)', open(_py, encoding='utf-8').read(), re.M))

CALLOUTS = {  # omgeving -> (Quarto-callout, titelprefix, extra attributen)
    "voorbeeld":  ("callout-tip", "Voorbeeld", ''),
    "toepassing": ("callout-note", "Toepassing", ''),
    "definitie":  ("callout-warning", "Definitie", ''),
    "besluit":    ("callout-important", "Besluit", ''),
    "oefening":   ("callout-note", "Oefening", ' icon="false"'),
    "oplossing":  ("callout-tip", "Oplossing", ' collapse="true" icon="false"'),  # enkel online, dichtgeklapt
}

# ---------------------------------------------------------------- helpers
def strip_comments(s):
    return re.sub(r'(?<!\\)%.*', '', s)

def read_group(s, i):
    """s[i] == '{' -> (inhoud, index na sluitaccolade)."""
    assert s[i] == '{', s[i:i+30]
    depth, j = 0, i
    while j < len(s):
        c = s[j]
        if c == '\\':
            j += 2; continue
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return s[i+1:j], j+1
        j += 1
    raise ValueError("onafgesloten groep")

def skip_ws(s, i):
    while i < len(s) and s[i] in ' \t\n': i += 1
    return i

def math_spans(s):
    """Sequentiële scanner: geeft (start, eind)-intervallen van wiskunde terug."""
    spans, i, n = [], 0, len(s)
    envs = r'(equation|align|gather|multline|eqnarray|displaymath|math)\*?'
    start, closer = None, None
    while i < n:
        c = s[i]
        if start is None:
            m = re.match(r'\\begin\{' + envs + r'\}', s[i:])
            if m:
                start, closer = i, re.compile(r'\\end\{' + re.escape(m.group(0)[7:-1]) + r'\}')
                i += m.end(); continue
            if s.startswith('\\[', i): start, closer = i, '\\]'; i += 2; continue
            if s.startswith('\\(', i): start, closer = i, '\\)'; i += 2; continue
            if c == '\\': i += 2; continue
            if s.startswith('$$', i): start, closer = i, '$$'; i += 2; continue
            if c == '$': start, closer = i, '$'; i += 1; continue
            i += 1
        else:
            if isinstance(closer, str):
                if s.startswith(closer, i) and not (closer == '$' and s.startswith('$$', i) and False):
                    i += len(closer); spans.append((start, i)); start = None; continue
                if c == '\\': i += 2; continue
                i += 1
            else:
                m = closer.match(s, i)
                if m: i = m.end(); spans.append((start, i)); start = None; continue
                i += 1
    return spans

def in_spans(pos, spans):
    return any(a <= pos < b for a, b in spans)

# ---------------------------------------------------------------- siunitx
PREFIX = {'kilo': 'k', 'mega': 'M', 'giga': 'G', 'milli': 'm', 'micro': r'\mu ', 'nano': 'n',
          'centi': 'c', 'pico': 'p', 'deci': 'd', 'femto': 'f', 'tera': 'T', 'hecto': 'h'}
UNIT = {'joule': 'J', 'mole': 'mol', 'kelvin': 'K', 'metre': 'm', 'meter': 'm', 'second': 's',
        'pascal': 'Pa', 'litre': 'L', 'liter': 'L', 'gram': 'g', 'kilogram': 'kg', 'bar': 'bar',
        'atm': 'atm', 'atmosphere': 'atm', 'hour': 'h', 'minute': 'min', 'newton': 'N', 'watt': 'W',
        'volt': 'V', 'ampere': 'A', 'coulomb': 'C', 'hertz': 'Hz', 'angstrom': r'\unicode{x212B}',
        'electronvolt': 'eV', 'calorie': 'cal', 'molar': 'M', 'ohm': r'\Omega', 'siemens': 'S',
        'farad': 'F', 'tesla': 'T', 'day': 'd', 'nm': 'nm', 'mmHg': 'mmHg', 'torr': 'Torr',
        'dalton': 'Da', 'radian': 'rad', 'steradian': 'sr', 'candela': 'cd', 'lumen': 'lm'}

def unit_tex(u):
    u = u.strip()
    if not u:
        return ''
    if '\\' not in u:  # letterlijke eenheid, bv. {J/mol}
        return r'\mathrm{' + u.replace('.', r'\,').replace('~', r'\,') + '}'
    toks = re.findall(r'\\[a-zA-Z]+(?:\{[^}]*\})?|[^\\\s]+', u)
    parts, per, prefix = [], False, ''
    special = {'celsius': r'{}^{\circ}\mathrm{C}', 'percent': r'\%', 'degree': r'^{\circ}'}
    for t in toks:
        name = t[1:] if t.startswith('\\') else None
        if name == 'per': per = True; continue
        if name in PREFIX: prefix = PREFIX[name]; continue
        if name in ('squared', 'cubed') or (name and name.startswith('tothe')):
            exp = {'squared': '2', 'cubed': '3'}.get(name) or re.search(r'\{([^}]*)\}', t).group(1)
            b, e = parts[-1]
            parts[-1] = (b, str((int(e) if e else 1) * int(exp)) if e else exp)
            continue
        if name in special:
            parts.append((special[name], None)); continue
        sym = UNIT.get(name, name) if name else t
        base = r'\mathrm{' + prefix + sym + '}'
        prefix = ''
        parts.append((base, '-1' if per else None))
        per = False
    out = []
    for b, e in parts:
        if e is None: out.append(b)
        elif e.startswith('-') or e.lstrip('-').isdigit():
            out.append(b + '^{' + (e if not per else e) + '}')
    return r'\,'.join(out)

def num_tex(n):
    n = n.strip()
    def one(x):
        m = re.fullmatch(r'([-+]?[\d.,]*)\s*[eE]\s*([-+]?\d+)', x.strip())
        if m:
            mant, ex = m.group(1), m.group(2).lstrip('+')
            if mant in ('', '1') and m.group(1) == '': return r'10^{' + ex + '}'
            if mant == '1': return r'10^{' + ex + '}'
            return mant + r'\times10^{' + ex + '}'
        return x.replace('+-', r'\pm ')
    if r'\pm' in n or '+-' in n:
        return r'\pm '.join(one(p) for p in re.split(r'\\pm|\+-', n))
    return one(n)

def si_expr(kind, args):
    if kind == 'SI':
        n, u = args; ut = unit_tex(u)
        sep = '' if r'\%' in ut or ut.startswith('{}^') else r'\,'
        return num_tex(n) + sep + ut
    if kind == 'si':
        return unit_tex(args[0])
    if kind == 'num':
        return num_tex(args[0])
    if kind == 'SIrange':
        a, b, u = args; ut = unit_tex(u)
        return num_tex(a) + r'\text{ tot }' + num_tex(b) + r'\,' + ut
    if kind == 'ce':
        return r'\ce{' + args[0] + '}'

NARGS = {'SIrange': 3, 'SI': 2, 'si': 1, 'num': 1, 'ce': 1}

def convert_si_ce(s):
    spans = math_spans(s)
    out, i = [], 0
    pat = re.compile(r'\\(SIrange|SI|si|num|ce)(?![a-zA-Z])')
    while True:
        m = pat.search(s, i)
        if not m:
            out.append(s[i:]); break
        kind = m.group(1)
        j = m.end()
        if j < len(s) and s[j] == '[':  # optionele opties negeren
            j = s.index(']', j) + 1
        args = []
        try:
            for _ in range(NARGS[kind]):
                j = skip_ws(s, j)
                a, j = read_group(s, j)
                args.append(a)
        except Exception:
            out.append(s[i:m.end()]); i = m.end(); continue
        expr = si_expr(kind, args)
        if kind == 'ce' and in_spans(m.start(), spans):
            expr = r'\ce{' + args[0] + '}'
        out.append(s[i:m.start()])
        out.append(expr if in_spans(m.start(), spans) else '$' + expr + '$')
        i = j
    return ''.join(out)

# ---------------------------------------------------------------- labels
def qid(label):
    l = re.sub(r'[^a-z0-9]+', '-', label.lower()).strip('-')
    if label.startswith('ch:'): return 'sec-' + l          # ch-energie -> sec-ch-energie
    if label.startswith('sec:'): return 'sec-' + l[4:]
    if label.startswith('eq:'): return 'eq-' + l[3:]
    if label.startswith('fig:'): return 'fig-' + l[4:]
    if label.startswith('tab:') or label.startswith('table:'): return 'tbl-' + l.split('-', 1)[1]
    return 'anker-' + l

def pandoc_inline(tex):
    r = subprocess.run(PANDOC + ['-f', 'latex', '-t', 'markdown', '--wrap=none'],
                       input=tex, capture_output=True, text=True)
    return r.stdout.strip().replace('\n', ' ')

# ---------------------------------------------------------------- per hoofdstuk
labels = []        # index -> label
label_kind = {}    # label -> 'heading' | 'eq' | 'fig' | 'tbl' | 'other'
images_used = set()
missing_images = []

def tok_label(lbl):
    if lbl not in labels: labels.append(lbl)
    return f'QLAB{labels.index(lbl)}Q'

def convert_chapter(texname, slug, chapnum):
    s = open(os.path.join(SRC, texname + '.tex'), encoding='utf-8').read()
    s = strip_comments(s)
    # oefenbestanden: \input{...} invoegen
    s = re.sub(r'\\input\{([^}]*)\}', lambda m: strip_comments(open(os.path.join(SRC, m.group(1) if m.group(1).endswith('.tex') else m.group(1) + '.tex'), encoding='utf-8').read()), s)
    s = convert_si_ce(s)
    s = re.sub(r'\\interactief\{([^}]*)\}', r'\n\nQINT\1QINT\n\n', s)
    # opsommingen met \item[(a)], \item[(b)], ...: als (a), (b) tonen (pandoc kent [(a)])
    def abc(m):
        body = m.group(2)
        if not re.match(r'\s*\\item\[\(a\)\]', body):
            return m.group(0)
        return m.group(1) + '[(a)]' + re.sub(r'\\item\[\([a-z]\)\]', r'\\item', body)
    s = re.sub(r'(\\begin\{enumerate\})((?:(?!\\begin\{enumerate\}).)*?\\end\{enumerate\})', abc, s, flags=re.S)
    s = re.sub(r'(\\begin\{(?:equation|align|gather|multline)\*?\})(\s*)\[', r'\1\2{}[', s)
    s = re.sub(r'(\\\\)(\s*)\[', r'\1{}\2[', s)

    # figuren apart behandelen
    figs = []
    def fig_repl(m):
        body = m.group(1)
        img = re.search(r'\\includegraphics(?:\[([^\]]*)\])?\{([^}]*)\}', body)
        cap_i = body.find(r'\caption')
        cap = ''
        if cap_i >= 0:
            cap, _ = read_group(body, skip_ws(body, cap_i + len(r'\caption')))
        lab = re.search(r'\\label\{([^}]*)\}', body)
        figs.append((img.group(2) if img else None, img.group(1) if img else None,
                     cap, lab.group(1) if lab else None))
        return f'\n\nQFIG{len(figs)-1}Q\n\n'
    s = re.sub(r'\\begin\{figure\}(?:\[[^\]]*\])?(.*?)\\end\{figure\}', fig_repl, s, flags=re.S)

    # callout-omgevingen met titel
    titles = []
    oef = [0]
    def env_open(m):
        env = m.group(1)
        j = m.end()
        title = ''
        if env == 'oefening':
            oef[0] += 1
            opt = ''
            if j < len(s) and s[j] == '[':
                k = s.index(']', j); opt = s[j+1:k]; j = k + 1
            title = f'{chapnum}.{oef[0]}' + (f' ({opt})' if opt else '')
        elif env == 'oplossing':
            title = ''
        else:
            jj = skip_ws(s, j)
            if jj < len(s) and s[jj] == '{':
                title, j = read_group(s, jj)
        titles.append((env, title))
        return j, f'\n\nQCO{len(titles)-1}Q\n\n'
    out, i = [], 0
    pat = re.compile(r'\\begin\{(' + '|'.join(CALLOUTS) + r')\}')
    while True:
        m = pat.search(s, i)
        if not m: out.append(s[i:]); break
        out.append(s[i:m.start()])
        j, rep = env_open(m)
        out.append(rep); i = j
    s = ''.join(out)
    # sluiten als losse markeringsalinea: hangt niet af van hoe pandoc
    # onbekende omgevingen behandelt (verschilt tussen pandoc-versies)
    s = re.sub(r'\\end\{(?:' + '|'.join(CALLOUTS) + r')\}', '\n\nQCCQ\n\n', s)

    # labels en verwijzingen als tokens
    s = re.sub(r'\\label\{([^}]*)\}', lambda m: tok_label(m.group(1)), s)
    s = re.sub(r'\\eqref\{([^}]*)\}', lambda m: 'QEQR' + tok_label(m.group(1))[4:], s)
    s = re.sub(r'\\(?:ref|autoref|cref)\{([^}]*)\}', lambda m: 'QREF' + tok_label(m.group(1))[4:], s)
    s = s.replace(r'\chapter*', r'\chapter')

    r = subprocess.run(PANDOC + ['-f', 'latex-auto_identifiers', '-t',
                        'markdown-simple_tables-multiline_tables-grid_tables-raw_attribute+pipe_tables',
                        '--wrap=none', '--shift-heading-level-by=0'],
                       input=s, capture_output=True, text=True)
    if r.stderr.strip():
        print(f'[{texname}] pandoc:', r.stderr.strip()[:500], file=sys.stderr)
    md = r.stdout

    # callouts
    def callout_repl(m):
        idx = int(m.group(1)); env = titles[idx][0]
        kind, prefix, extra = CALLOUTS[env]
        t = titles[idx][1]
        t_md = pandoc_inline(t) if t else ''
        head = f'{prefix} {t_md}' if env == 'oefening' else (f'{prefix}: {t_md}' if t_md else prefix)
        return f'::: {{.{kind}{extra}}}\n## {head}'
    md = re.sub(r'^[ \t]*QCO(\d+)Q[ \t]*$', callout_repl, md, flags=re.M)
    md = re.sub(r'^[ \t]*QCCQ[ \t]*$', ':::', md, flags=re.M)

    # figuren
    pyfigs = []
    def figmd(m):
        path, opts, cap, lab = figs[int(m.group(1))]
        cap_md = pandoc_inline(cap) if cap else ''
        cap_md = re.sub(r'QLAB\d+Q', '', cap_md).strip()
        idattr = ''
        if lab:
            label_kind[lab] = 'fig'
            idattr = '#' + qid(lab)
        w = ''
        if opts:
            mw = re.search(r'width=([\d.]+)\\(?:line|text)width', opts)
            if mw: w = f' width="{round(float(mw.group(1))*100)}%"'
        if path and path.startswith('Figuren/'):
            naam = os.path.splitext(path[len('Figuren/'):])[0]
            pyfigs.append(naam)
            attr = idattr
            if w and w != ' width="70%"':
                attr += ' breedte="' + w.split('"')[1] + '"'
            opties = '' if naam in ANIMATIES else '#| renderings: [light, dark]\n'
            return (f'::: {{{attr}}}\n```{{python}}\n{opties}fig.toon(fig.{naam})\n```\n\n'
                    f'{cap_md}\n:::')
        fn = os.path.basename(path) if path else None
        if fn and os.path.exists(os.path.join(SRC, 'Afbeeldingen', fn)):
            images_used.add(fn)
            return f'![{cap_md}](afbeeldingen/{fn}){{{idattr}{w}}}'
        missing_images.append((texname, fn))
        return (f'::: {{{idattr}}}\n::: {{.callout-note appearance="minimal" icon="false"}}\n'
                f'🖼️ *Figuur in voorbereiding* (`{fn}`)\n:::\n\n{cap_md}\n:::')
    md = re.sub(r'QFIG(\d+)Q', figmd, md)
    md = re.sub(r'QINT(.+?)QINT', r'{{< include _interactief/\1.qmd >}}', md)

    # labels: koppen
    def head_lab(m):
        lab = labels[int(m.group(3))]
        label_kind[lab] = 'heading'
        h = re.sub(r'\s*\{[^}]*\}\s*$', '', m.group(2)).rstrip()
        return f'{m.group(1)} {h} {{#{qid(lab)}}}'
    md = re.sub(r'^(#+) (.*?)\n\nQLAB(\d+)Q *\n', lambda m: head_lab(m) + '\n', md, flags=re.M)
    md = re.sub(r'^(#+) (.*?) ?QLAB(\d+)Q(.*)$', lambda m: head_lab(m), md, flags=re.M)

    # labels: vergelijkingen
    def eq_lab(m):
        body = m.group(1)
        labs = [labels[int(x)] for x in re.findall(r'QLAB(\d+)Q', body)]
        body = re.sub(r'\s*QLAB\d+Q', '', body)
        if not labs:
            return m.group(0)
        main = labs[0]
        for l in labs:
            label_kind[l] = 'eq'
            if l != main: label_alias[l] = main
        return f'$${body}$$ {{#{qid(main)}}}'
    md = re.sub(r'\$\$(.*?)\$\$', eq_lab, md, flags=re.S)

    # labels: tabelbijschriften
    def tbl_lab(m):
        lab = labels[int(m.group(2))]
        label_kind[lab] = 'tbl'
        return f'{m.group(1).rstrip()} {{#{qid(lab)}}}'
    md = re.sub(r'^(: .*?)QLAB(\d+)Q(.*)$', lambda m: tbl_lab(m) + m.group(3), md, flags=re.M)

    # overige labels -> anker
    def other_lab(m):
        lab = labels[int(m.group(1))]
        label_kind.setdefault(lab, 'other')
        return f'[]{{#{qid(lab)}}}'
    md = re.sub(r'QLAB(\d+)Q', other_lab, md)

    # hoofdstuktitel: eerste kop wordt niveau 1
    md = md.replace('\\\n', '\n')
    if pyfigs:  # figuren uit _figuren/ beschikbaar maken als fig.naam
        kop = ('```{python}\n#| include: false\n# Figuren: zie _figuren/ (h1.py, h2.py, ...)\n'
               'import sys\nsys.path.insert(0, "_figuren")\nimport alle as fig\n```\n\n')
        md = re.sub(r'^(# .*\n)', lambda m: m.group(1) + '\n' + kop, md, count=1, flags=re.M)
    return md

label_alias = {'ch:eerstehoofdwet': 'ch:energie', 'ch:kristallografie': 'ch:vastestof'}

def fix_refs(md):
    def ref(m, eq):
        lab = labels[int(m.group(1))]
        lab = label_alias.get(lab, lab)
        k = label_kind.get(lab)
        if k in ('heading', 'eq', 'fig', 'tbl'):
            r = f'[-@{qid(lab)}]'
            return f'({r})' if eq else r
        if k == 'other':
            return f'[↗](#{qid(lab)})'
        return '(?)'
    md = re.sub(r'QEQR(\d+)Q', lambda m: ref(m, True), md)
    md = re.sub(r'QREF(\d+)Q', lambda m: ref(m, False), md)
    return md

# compacte opsommingen (geen witregel tussen items)
MARK = re.compile(r'^\s*(?:[-*+]|\d+\.|\([a-z]\))\s+\S')
def tighten_lists(md):
    lines = md.split('\n'); out = []
    for i, l in enumerate(lines):
        if l.strip() == '' and out and i + 1 < len(lines):
            prev, nxt = out[-1], lines[i + 1]
            if MARK.match(nxt) and prev.strip() and (MARK.match(prev) or prev.startswith('    ')):
                continue
        out.append(l)
    return '\n'.join(out)

FORUM = '''

---

::: {.callout-note appearance="simple" icon="false"}
## 💬 Vragen over dit hoofdstuk?
Stel ze op het [discussieforum van dit hoofdstuk op Toledo](https://toledo.kuleuven.be). Medestudenten en de docent antwoorden daar.
:::
'''

def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, 'afbeeldingen'), exist_ok=True)
    mds = {}
    for n, (tex, slug) in enumerate(CHAPTERS, 1):
        mds[slug] = convert_chapter(tex, slug, n)
    for slug, md in mds.items():
        md = tighten_lists(fix_refs(md))
        open(os.path.join(OUT, slug + '.qmd'), 'w', encoding='utf-8').write(md.rstrip() + '\n' + FORUM)
    for fn in images_used:
        shutil.copy(os.path.join(SRC, 'Afbeeldingen', fn), os.path.join(OUT, 'afbeeldingen', fn))
    unresolved = [l for l in labels if l not in label_kind and label_alias.get(l) not in label_kind]
    print('hoofdstukken:', len(mds), '| labels:', len(labels), '| onopgeloste verwijzingen:', len(unresolved))
    if unresolved: print('  ', unresolved[:30])
    print('ontbrekende figuren:', len(missing_images))
    # bewerkknop (_docent.html): welke .tex hoort bij welke pagina
    bron = ', '.join(f'"{slug}": "{tex}.tex"' for tex, slug in CHAPTERS)
    open(os.path.join(OUT, '_bronnen.html'), 'w', encoding='utf-8').write(
        f'<script>window.FC_BRON = {{{bron}}};</script>\n')
    quarto = open(os.path.join(OUT, '_quarto.yml'), encoding='utf-8').read()
    for slug in mds:
        if slug + '.qmd' not in quarto:
            print(f'LET OP: {slug}.qmd staat niet in _quarto.yml (hoofdstukkenlijst)')

main()
