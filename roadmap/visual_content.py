"""
EXA AI HUB – Visual Content Library
SVG educational diagrams for all 6 domains and 3 learner stages.
Each diagram is inline SVG (no external requests) with dark-theme styling,
readable labels, and a short caption.
"""

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _wrap(svg_body: str, caption: str, width: int = 720, height: int = 340) -> dict:
    """Return a dict with inline SVG and caption ready for template rendering."""
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{caption}" '
        f'style="width:100%;max-width:{width}px;height:auto;display:block;margin:0 auto;">'
        + svg_body
        + "</svg>"
    )
    return {"svg": svg, "caption": caption}


# ---------------------------------------------------------------------------
# Shared styling constants (embedded in each SVG as needed)
# ---------------------------------------------------------------------------
_DEFS = """
<defs>
  <filter id="glow">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
"""

# ---------------------------------------------------------------------------
# FULL STACK / WEB DEVELOPMENT VISUALS
# ---------------------------------------------------------------------------

WEB_DNS_FLOW = _wrap(
    _DEFS + """
  <!-- Background -->
  <rect width="720" height="340" rx="16" fill="#0b0f19"/>
  <!-- Title -->
  <text x="360" y="28" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">DNS RESOLUTION FLOW</text>
  <!-- Nodes -->
  <!-- Browser -->
  <rect x="20" y="60" width="110" height="50" rx="10" fill="#1e293b" stroke="#6366f1" stroke-width="2"/>
  <text x="75" y="81" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="11" font-weight="700">BROWSER</text>
  <text x="75" y="97" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">User types URL</text>
  <!-- OS Cache -->
  <rect x="185" y="60" width="110" height="50" rx="10" fill="#1e293b" stroke="#22d3ee" stroke-width="2"/>
  <text x="240" y="81" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="11" font-weight="700">OS CACHE</text>
  <text x="240" y="97" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Local lookup</text>
  <!-- Recursive Resolver -->
  <rect x="350" y="60" width="120" height="50" rx="10" fill="#1e293b" stroke="#34d399" stroke-width="2"/>
  <text x="410" y="81" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="10" font-weight="700">RECURSIVE</text>
  <text x="410" y="94" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="10" font-weight="700">RESOLVER</text>
  <text x="410" y="107" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">ISP DNS Server</text>
  <!-- Root DNS -->
  <rect x="530" y="60" width="110" height="50" rx="10" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="585" y="81" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="11" font-weight="700">ROOT DNS</text>
  <text x="585" y="97" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">13 root servers</text>
  <!-- TLD Server -->
  <rect x="530" y="170" width="110" height="50" rx="10" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="585" y="191" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="11" font-weight="700">TLD SERVER</text>
  <text x="585" y="207" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">.com / .org / .net</text>
  <!-- Auth NS -->
  <rect x="350" y="170" width="120" height="50" rx="10" fill="#1e293b" stroke="#34d399" stroke-width="2"/>
  <text x="410" y="191" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="10" font-weight="700">AUTHORITATIVE</text>
  <text x="410" y="204" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="10" font-weight="700">NAME SERVER</text>
  <text x="410" y="217" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Returns IP address</text>
  <!-- Web Server -->
  <rect x="185" y="170" width="110" height="50" rx="10" fill="#1e293b" stroke="#6366f1" stroke-width="2"/>
  <text x="240" y="191" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="11" font-weight="700">WEB SERVER</text>
  <text x="240" y="207" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Serves content</text>
  <!-- Arrows (horizontal) -->
  <line x1="130" y1="85" x2="183" y2="85" stroke="#67e8f9" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="295" y1="85" x2="348" y2="85" stroke="#67e8f9" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="470" y1="85" x2="528" y2="85" stroke="#67e8f9" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Arrows (vertical) -->
  <line x1="585" y1="110" x2="585" y2="168" stroke="#f59e0b" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Arrows (horizontal return) -->
  <line x1="528" y1="195" x2="472" y2="195" stroke="#34d399" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="348" y1="195" x2="297" y2="195" stroke="#34d399" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="183" y1="195" x2="131" y2="140" stroke="#6366f1" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arr)"/>
  <!-- Labels -->
  <text x="157" y="79" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">query</text>
  <text x="322" y="79" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">query</text>
  <text x="499" y="79" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">query</text>
  <text x="500" y="189" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">TLD ref.</text>
  <text x="310" y="189" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">IP back</text>
  <!-- Step labels -->
  <text x="360" y="275" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="10">① Browser asks OS cache  ② Asks ISP resolver  ③ Resolver queries Root → TLD → Auth NS  ④ IP returned  ⑤ Browser connects</text>
  <!-- Arrow marker -->
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#67e8f9"/>
    </marker>
  </defs>
""",
    "DNS Resolution Flow: How a browser finds the server behind a domain name",
    720, 310,
)

WEB_HTTP_CYCLE = _wrap(
    _DEFS + """
  <rect width="720" height="300" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">HTTP REQUEST / RESPONSE CYCLE</text>
  <!-- Client -->
  <rect x="30" y="60" width="130" height="160" rx="12" fill="#111827" stroke="#6366f1" stroke-width="2"/>
  <text x="95" y="85" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="12" font-weight="700">CLIENT</text>
  <text x="95" y="105" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Browser / App</text>
  <text x="95" y="130" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="9">GET /page HTTP/1.1</text>
  <text x="95" y="145" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="9">Host: example.com</text>
  <text x="95" y="160" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="9">Accept: text/html</text>
  <!-- Server -->
  <rect x="560" y="60" width="130" height="160" rx="12" fill="#111827" stroke="#34d399" stroke-width="2"/>
  <text x="625" y="85" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="12" font-weight="700">SERVER</text>
  <text x="625" y="105" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Django / Node / etc.</text>
  <text x="625" y="130" text-anchor="middle" fill="#34d399" font-family="Inter,sans-serif" font-size="9">HTTP/1.1 200 OK</text>
  <text x="625" y="145" text-anchor="middle" fill="#34d399" font-family="Inter,sans-serif" font-size="9">Content-Type: text/html</text>
  <text x="625" y="160" text-anchor="middle" fill="#34d399" font-family="Inter,sans-serif" font-size="9">&lt;html&gt;...&lt;/html&gt;</text>
  <!-- Middle boxes -->
  <rect x="245" y="80" width="230" height="50" rx="8" fill="#1e293b" stroke="#22d3ee" stroke-width="1"/>
  <text x="360" y="101" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="10" font-weight="700">HTTP REQUEST →</text>
  <text x="360" y="118" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Method · URL · Headers · Body</text>
  <rect x="245" y="160" width="230" height="50" rx="8" fill="#1e293b" stroke="#34d399" stroke-width="1"/>
  <text x="360" y="181" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="10" font-weight="700">← HTTP RESPONSE</text>
  <text x="360" y="198" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Status · Headers · Body</text>
  <!-- Arrows -->
  <line x1="160" y1="105" x2="243" y2="105" stroke="#6366f1" stroke-width="2" marker-end="url(#arr2)"/>
  <line x1="477" y1="105" x2="558" y2="105" stroke="#6366f1" stroke-width="2" marker-end="url(#arr2)"/>
  <line x1="558" y1="185" x2="477" y2="185" stroke="#34d399" stroke-width="2" marker-end="url(#arr3)"/>
  <line x1="243" y1="185" x2="160" y2="185" stroke="#34d399" stroke-width="2" marker-end="url(#arr3)"/>
  <!-- Status codes legend -->
  <text x="360" y="250" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Common status codes:</text>
  <text x="360" y="265" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">200 OK · 301 Redirect · 404 Not Found · 500 Server Error</text>
  <defs>
    <marker id="arr2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#6366f1"/></marker>
    <marker id="arr3" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#34d399"/></marker>
  </defs>
""",
    "HTTP Request/Response Cycle: How client and server communicate",
    720, 290,
)

WEB_API_ARCHITECTURE = _wrap(
    _DEFS + """
  <rect width="720" height="320" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">REST API ARCHITECTURE</text>
  <!-- Frontend -->
  <rect x="20" y="60" width="130" height="180" rx="12" fill="#111827" stroke="#6366f1" stroke-width="2"/>
  <text x="85" y="82" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="11" font-weight="700">FRONTEND</text>
  <text x="85" y="100" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">React / HTML</text>
  <rect x="35" y="115" width="100" height="22" rx="5" fill="rgba(99,102,241,0.2)" stroke="rgba(99,102,241,0.4)" stroke-width="1"/>
  <text x="85" y="131" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="9">GET /api/users</text>
  <rect x="35" y="145" width="100" height="22" rx="5" fill="rgba(52,211,153,0.15)" stroke="rgba(52,211,153,0.3)" stroke-width="1"/>
  <text x="85" y="161" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="9">POST /api/users</text>
  <rect x="35" y="175" width="100" height="22" rx="5" fill="rgba(245,158,11,0.15)" stroke="rgba(245,158,11,0.3)" stroke-width="1"/>
  <text x="85" y="191" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="9">PUT /api/users/1</text>
  <rect x="35" y="205" width="100" height="22" rx="5" fill="rgba(244,63,94,0.15)" stroke="rgba(244,63,94,0.3)" stroke-width="1"/>
  <text x="85" y="221" text-anchor="middle" fill="#fb7185" font-family="Inter,sans-serif" font-size="9">DELETE /api/users/1</text>
  <!-- API Gateway -->
  <rect x="250" y="90" width="130" height="130" rx="12" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <text x="315" y="112" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="11" font-weight="700">API LAYER</text>
  <text x="315" y="130" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Django REST / Express</text>
  <text x="315" y="152" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">• Auth / JWT</text>
  <text x="315" y="167" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">• Rate limiting</text>
  <text x="315" y="182" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">• Serialisation</text>
  <text x="315" y="197" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">• JSON responses</text>
  <!-- Database -->
  <rect x="490" y="90" width="130" height="130" rx="12" fill="#111827" stroke="#34d399" stroke-width="2"/>
  <text x="555" y="112" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="11" font-weight="700">DATABASE</text>
  <text x="555" y="132" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">PostgreSQL / SQLite</text>
  <ellipse cx="555" cy="158" rx="45" ry="14" fill="rgba(52,211,153,0.1)" stroke="rgba(52,211,153,0.4)" stroke-width="1"/>
  <text x="555" y="163" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="9">Tables / ORM</text>
  <ellipse cx="555" cy="183" rx="45" ry="14" fill="rgba(52,211,153,0.06)" stroke="rgba(52,211,153,0.25)" stroke-width="1"/>
  <text x="555" y="188" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="9">Queries / Indexes</text>
  <!-- Arrows -->
  <line x1="150" y1="150" x2="248" y2="150" stroke="#22d3ee" stroke-width="2" marker-end="url(#arr4)"/>
  <line x1="380" y1="150" x2="488" y2="150" stroke="#22d3ee" stroke-width="2" marker-end="url(#arr4)"/>
  <defs>
    <marker id="arr4" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#22d3ee"/></marker>
  </defs>
  <text x="360" y="280" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="9">HTTP verbs: GET (read) · POST (create) · PUT/PATCH (update) · DELETE (remove)</text>
""",
    "REST API Architecture: Frontend → API Layer → Database",
    720, 300,
)

WEB_DB_DIAGRAM = _wrap(
    _DEFS + """
  <rect width="720" height="300" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">RELATIONAL DATABASE DIAGRAM</text>
  <!-- Users table -->
  <rect x="30" y="50" width="180" height="160" rx="10" fill="#111827" stroke="#6366f1" stroke-width="2"/>
  <rect x="30" y="50" width="180" height="36" rx="10" fill="rgba(99,102,241,0.25)"/>
  <text x="120" y="74" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="12" font-weight="800">users</text>
  <text x="45" y="102" fill="#fbbf24" font-family="monospace" font-size="10">🔑 id          INTEGER PK</text>
  <text x="45" y="120" fill="#94a3b8" font-family="monospace" font-size="10">   username    TEXT</text>
  <text x="45" y="138" fill="#94a3b8" font-family="monospace" font-size="10">   email       TEXT</text>
  <text x="45" y="156" fill="#94a3b8" font-family="monospace" font-size="10">   created_at  DATETIME</text>
  <text x="45" y="174" fill="#94a3b8" font-family="monospace" font-size="10">   is_active   BOOLEAN</text>
  <!-- Posts table -->
  <rect x="280" y="50" width="200" height="190" rx="10" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <rect x="280" y="50" width="200" height="36" rx="10" fill="rgba(34,211,238,0.15)"/>
  <text x="380" y="74" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="12" font-weight="800">posts</text>
  <text x="295" y="102" fill="#fbbf24" font-family="monospace" font-size="10">🔑 id          INTEGER PK</text>
  <text x="295" y="120" fill="#fb7185" font-family="monospace" font-size="10">🔗 user_id     INTEGER FK</text>
  <text x="295" y="138" fill="#94a3b8" font-family="monospace" font-size="10">   title       TEXT</text>
  <text x="295" y="156" fill="#94a3b8" font-family="monospace" font-size="10">   body        TEXT</text>
  <text x="295" y="174" fill="#94a3b8" font-family="monospace" font-size="10">   created_at  DATETIME</text>
  <text x="295" y="192" fill="#94a3b8" font-family="monospace" font-size="10">   category_id INTEGER FK</text>
  <!-- Categories -->
  <rect x="550" y="50" width="155" height="130" rx="10" fill="#111827" stroke="#34d399" stroke-width="2"/>
  <rect x="550" y="50" width="155" height="36" rx="10" fill="rgba(52,211,153,0.15)"/>
  <text x="627" y="74" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="12" font-weight="800">categories</text>
  <text x="565" y="102" fill="#fbbf24" font-family="monospace" font-size="10">🔑 id     INTEGER PK</text>
  <text x="565" y="120" fill="#94a3b8" font-family="monospace" font-size="10">   name   TEXT</text>
  <text x="565" y="138" fill="#94a3b8" font-family="monospace" font-size="10">   slug   TEXT</text>
  <!-- Relationship lines -->
  <line x1="210" y1="120" x2="278" y2="120" stroke="#fb7185" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="244" y="115" text-anchor="middle" fill="#fb7185" font-family="Inter,sans-serif" font-size="8">1 : N</text>
  <line x1="480" y1="140" x2="548" y2="120" stroke="#34d399" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="514" y="125" text-anchor="middle" fill="#34d399" font-family="Inter,sans-serif" font-size="8">N : 1</text>
  <text x="360" y="265" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="9">🔑 Primary Key  🔗 Foreign Key (references another table's PK) · One user → Many posts</text>
""",
    "Relational Database Diagram: Tables, primary keys, foreign keys, and relationships",
    720, 285,
)


# ---------------------------------------------------------------------------
# AI / MACHINE LEARNING VISUALS
# ---------------------------------------------------------------------------

AI_ML_PIPELINE = _wrap(
    _DEFS + """
  <rect width="720" height="300" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#a78bfa" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">MACHINE LEARNING PIPELINE</text>
  <!-- Steps -->
  <!-- 1 Raw Data -->
  <rect x="14" y="60" width="90" height="70" rx="10" fill="#1e293b" stroke="#6366f1" stroke-width="2"/>
  <text x="59" y="82" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="10" font-weight="700">RAW DATA</text>
  <text x="59" y="98" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">CSV / DB</text>
  <text x="59" y="113" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Images / Text</text>
  <text x="59" y="148" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">①</text>
  <!-- 2 Data Prep -->
  <rect x="120" y="60" width="90" height="70" rx="10" fill="#1e293b" stroke="#22d3ee" stroke-width="2"/>
  <text x="165" y="80" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="10" font-weight="700">DATA</text>
  <text x="165" y="94" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="10" font-weight="700">PREP</text>
  <text x="165" y="110" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Clean · Split</text>
  <text x="165" y="123" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Train/Test</text>
  <text x="165" y="148" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">②</text>
  <!-- 3 Feature Eng -->
  <rect x="226" y="60" width="90" height="70" rx="10" fill="#1e293b" stroke="#34d399" stroke-width="2"/>
  <text x="271" y="80" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="10" font-weight="700">FEATURE</text>
  <text x="271" y="94" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="10" font-weight="700">ENGINEERING</text>
  <text x="271" y="110" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Scale · Encode</text>
  <text x="271" y="123" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Transform</text>
  <text x="271" y="148" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">③</text>
  <!-- 4 Model Training -->
  <rect x="332" y="60" width="90" height="70" rx="10" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="377" y="80" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="10" font-weight="700">MODEL</text>
  <text x="377" y="94" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="10" font-weight="700">TRAINING</text>
  <text x="377" y="110" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Fit on</text>
  <text x="377" y="123" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">training set</text>
  <text x="377" y="148" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">④</text>
  <!-- 5 Evaluation -->
  <rect x="438" y="60" width="90" height="70" rx="10" fill="#1e293b" stroke="#fb7185" stroke-width="2"/>
  <text x="483" y="80" text-anchor="middle" fill="#fda4af" font-family="Inter,sans-serif" font-size="10" font-weight="700">EVALUATION</text>
  <text x="483" y="98" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Accuracy</text>
  <text x="483" y="112" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Precision/Recall</text>
  <text x="483" y="125" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">F1 / MSE</text>
  <text x="483" y="148" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">⑤</text>
  <!-- 6 Deploy -->
  <rect x="544" y="60" width="90" height="70" rx="10" fill="#1e293b" stroke="#a78bfa" stroke-width="2"/>
  <text x="589" y="80" text-anchor="middle" fill="#c4b5fd" font-family="Inter,sans-serif" font-size="10" font-weight="700">DEPLOY</text>
  <text x="589" y="98" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">API / App</text>
  <text x="589" y="112" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Monitor</text>
  <text x="589" y="125" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Retrain</text>
  <text x="589" y="148" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">⑥</text>
  <!-- Connector arrows -->
  <line x1="104" y1="95" x2="118" y2="95" stroke="#67e8f9" stroke-width="1.5" marker-end="url(#arr5)"/>
  <line x1="210" y1="95" x2="224" y2="95" stroke="#67e8f9" stroke-width="1.5" marker-end="url(#arr5)"/>
  <line x1="316" y1="95" x2="330" y2="95" stroke="#67e8f9" stroke-width="1.5" marker-end="url(#arr5)"/>
  <line x1="422" y1="95" x2="436" y2="95" stroke="#67e8f9" stroke-width="1.5" marker-end="url(#arr5)"/>
  <line x1="528" y1="95" x2="542" y2="95" stroke="#67e8f9" stroke-width="1.5" marker-end="url(#arr5)"/>
  <!-- Feedback loop -->
  <path d="M634 130 Q634 200 377 200 Q120 200 120 132" fill="none" stroke="#6366f1" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#arr6)"/>
  <text x="377" y="220" text-anchor="middle" fill="#6366f1" font-family="Inter,sans-serif" font-size="9">Feedback loop: poor performance → improve data / features / hyperparameters</text>
  <!-- Training vs Test split illustration -->
  <rect x="140" y="240" width="440" height="30" rx="6" fill="#1e293b"/>
  <rect x="140" y="240" width="308" height="30" rx="6" fill="rgba(34,211,238,0.2)"/>
  <text x="294" y="260" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="9" font-weight="600">Training Set (70%)</text>
  <text x="510" y="260" text-anchor="middle" fill="#fda4af" font-family="Inter,sans-serif" font-size="9" font-weight="600">Test Set (30%)</text>
  <defs>
    <marker id="arr5" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#67e8f9"/></marker>
    <marker id="arr6" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#6366f1"/></marker>
  </defs>
""",
    "Machine Learning Pipeline: from raw data through training to deployment",
    720, 290,
)

AI_NEURAL_NETWORK = _wrap(
    _DEFS + """
  <rect width="720" height="320" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#a78bfa" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">NEURAL NETWORK ARCHITECTURE</text>
  <!-- Layer labels -->
  <text x="110" y="55" text-anchor="middle" fill="#6366f1" font-family="Inter,sans-serif" font-size="11" font-weight="700">INPUT LAYER</text>
  <text x="360" y="55" text-anchor="middle" fill="#22d3ee" font-family="Inter,sans-serif" font-size="11" font-weight="700">HIDDEN LAYERS</text>
  <text x="615" y="55" text-anchor="middle" fill="#34d399" font-family="Inter,sans-serif" font-size="11" font-weight="700">OUTPUT LAYER</text>
  <!-- Input neurons -->
  <circle cx="110" cy="90" r="20" fill="#111827" stroke="#6366f1" stroke-width="2"/>
  <text x="110" y="95" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="9">x₁</text>
  <circle cx="110" cy="150" r="20" fill="#111827" stroke="#6366f1" stroke-width="2"/>
  <text x="110" y="155" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="9">x₂</text>
  <circle cx="110" cy="210" r="20" fill="#111827" stroke="#6366f1" stroke-width="2"/>
  <text x="110" y="215" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="9">x₃</text>
  <circle cx="110" cy="270" r="20" fill="#111827" stroke="#6366f1" stroke-width="2"/>
  <text x="110" y="275" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="9">x₄</text>
  <!-- Hidden layer 1 -->
  <circle cx="270" cy="100" r="20" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <text x="270" y="105" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="8">h₁</text>
  <circle cx="270" cy="160" r="20" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <text x="270" y="165" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="8">h₂</text>
  <circle cx="270" cy="220" r="20" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <text x="270" y="225" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="8">h₃</text>
  <circle cx="270" cy="270" r="20" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <text x="270" y="275" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="8">h₄</text>
  <!-- Hidden layer 2 -->
  <circle cx="450" cy="120" r="20" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <text x="450" y="125" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="8">h₅</text>
  <circle cx="450" cy="190" r="20" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <text x="450" y="195" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="8">h₆</text>
  <circle cx="450" cy="250" r="20" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <text x="450" y="255" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="8">h₇</text>
  <!-- Output neurons -->
  <circle cx="615" cy="150" r="22" fill="#111827" stroke="#34d399" stroke-width="2.5"/>
  <text x="615" y="147" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">ŷ₁</text>
  <text x="615" y="160" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="7">Cat</text>
  <circle cx="615" cy="230" r="22" fill="#111827" stroke="#34d399" stroke-width="2.5"/>
  <text x="615" y="227" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">ŷ₂</text>
  <text x="615" y="240" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="7">Dog</text>
  <!-- Connections (simplified) -->
  <g stroke="rgba(99,102,241,0.2)" stroke-width="0.8">
    <line x1="130" y1="90" x2="250" y2="100"/>
    <line x1="130" y1="90" x2="250" y2="160"/>
    <line x1="130" y1="150" x2="250" y2="100"/>
    <line x1="130" y1="150" x2="250" y2="220"/>
    <line x1="130" y1="210" x2="250" y2="160"/>
    <line x1="130" y1="210" x2="250" y2="270"/>
    <line x1="130" y1="270" x2="250" y2="220"/>
    <line x1="130" y1="270" x2="250" y2="270"/>
  </g>
  <g stroke="rgba(34,211,238,0.2)" stroke-width="0.8">
    <line x1="290" y1="100" x2="430" y2="120"/>
    <line x1="290" y1="100" x2="430" y2="190"/>
    <line x1="290" y1="160" x2="430" y2="120"/>
    <line x1="290" y1="160" x2="430" y2="250"/>
    <line x1="290" y1="220" x2="430" y2="190"/>
    <line x1="290" y1="220" x2="430" y2="250"/>
    <line x1="290" y1="270" x2="430" y2="190"/>
    <line x1="290" y1="270" x2="430" y2="250"/>
  </g>
  <g stroke="rgba(52,211,153,0.3)" stroke-width="1.2">
    <line x1="470" y1="120" x2="593" y2="150"/>
    <line x1="470" y1="190" x2="593" y2="150"/>
    <line x1="470" y1="250" x2="593" y2="150"/>
    <line x1="470" y1="120" x2="593" y2="230"/>
    <line x1="470" y1="190" x2="593" y2="230"/>
    <line x1="470" y1="250" x2="593" y2="230"/>
  </g>
  <!-- Activation note -->
  <text x="360" y="305" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="9">Each neuron: weighted sum → activation function (ReLU / Sigmoid) → next layer · Backprop adjusts weights</text>
""",
    "Neural Network: Input → Hidden Layers → Output with weighted connections",
    720, 315,
)

AI_CONFUSION_MATRIX = _wrap(
    _DEFS + """
  <rect width="720" height="300" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#a78bfa" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">CONFUSION MATRIX &amp; CLASSIFICATION METRICS</text>
  <!-- Matrix grid -->
  <text x="280" y="65" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="11">Predicted: Positive</text>
  <text x="440" y="65" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="11">Predicted: Negative</text>
  <text x="130" y="115" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="10">Actual: Pos</text>
  <text x="130" y="185" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="10">Actual: Neg</text>
  <!-- TP -->
  <rect x="170" y="78" width="160" height="80" rx="8" fill="rgba(52,211,153,0.2)" stroke="#34d399" stroke-width="2"/>
  <text x="250" y="110" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="18" font-weight="700">TP</text>
  <text x="250" y="132" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="10">True Positive</text>
  <text x="250" y="148" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Correctly predicted Yes</text>
  <!-- FN -->
  <rect x="340" y="78" width="160" height="80" rx="8" fill="rgba(244,63,94,0.1)" stroke="#f43f5e" stroke-width="2"/>
  <text x="420" y="110" text-anchor="middle" fill="#fb7185" font-family="Inter,sans-serif" font-size="18" font-weight="700">FN</text>
  <text x="420" y="132" text-anchor="middle" fill="#fb7185" font-family="Inter,sans-serif" font-size="10">False Negative</text>
  <text x="420" y="148" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Missed a Yes (Type II)</text>
  <!-- FP -->
  <rect x="170" y="168" width="160" height="80" rx="8" fill="rgba(245,158,11,0.1)" stroke="#f59e0b" stroke-width="2"/>
  <text x="250" y="200" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="18" font-weight="700">FP</text>
  <text x="250" y="222" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="10">False Positive</text>
  <text x="250" y="238" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Wrong alarm (Type I)</text>
  <!-- TN -->
  <rect x="340" y="168" width="160" height="80" rx="8" fill="rgba(52,211,153,0.12)" stroke="#34d399" stroke-width="1.5"/>
  <text x="420" y="200" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="18" font-weight="700">TN</text>
  <text x="420" y="222" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="10">True Negative</text>
  <text x="420" y="238" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Correctly predicted No</text>
  <!-- Metrics legend -->
  <text x="580" y="100" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="10" font-weight="600">Key Metrics</text>
  <text x="580" y="120" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="9">Precision = TP / (TP+FP)</text>
  <text x="580" y="140" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="9">Recall = TP / (TP+FN)</text>
  <text x="580" y="160" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="9">F1 = 2·P·R / (P+R)</text>
  <text x="580" y="180" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="9">Accuracy = (TP+TN) / All</text>
""",
    "Confusion Matrix: TP, FP, TN, FN with Precision, Recall, and F1 Score",
    720, 285,
)


# ---------------------------------------------------------------------------
# ROBOTICS VISUALS
# ---------------------------------------------------------------------------

ROBOTICS_ARCHITECTURE = _wrap(
    _DEFS + """
  <rect width="720" height="320" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#34d399" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">ROBOT SYSTEM ARCHITECTURE</text>
  <!-- Perception -->
  <rect x="20" y="55" width="150" height="200" rx="12" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <text x="95" y="78" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="11" font-weight="700">PERCEPTION</text>
  <text x="95" y="100" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Ultrasonic Sensor</text>
  <text x="95" y="118" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">IR Sensor</text>
  <text x="95" y="136" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Camera</text>
  <text x="95" y="154" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Gyroscope / IMU</text>
  <text x="95" y="172" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Encoder</text>
  <text x="95" y="190" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Temperature</text>
  <text x="95" y="208" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Proximity</text>
  <!-- Processing -->
  <rect x="235" y="55" width="165" height="200" rx="12" fill="#111827" stroke="#34d399" stroke-width="2"/>
  <text x="317" y="78" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="11" font-weight="700">PROCESSING</text>
  <text x="317" y="102" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Microcontroller</text>
  <text x="317" y="118" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">(Arduino / Raspberry Pi)</text>
  <rect x="255" y="130" width="125" height="30" rx="6" fill="rgba(52,211,153,0.15)" stroke="rgba(52,211,153,0.4)" stroke-width="1"/>
  <text x="317" y="150" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="9" font-weight="600">Decision Logic</text>
  <rect x="255" y="168" width="125" height="30" rx="6" fill="rgba(52,211,153,0.1)" stroke="rgba(52,211,153,0.3)" stroke-width="1"/>
  <text x="317" y="188" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="9">PID Control</text>
  <rect x="255" y="206" width="125" height="30" rx="6" fill="rgba(52,211,153,0.08)" stroke="rgba(52,211,153,0.2)" stroke-width="1"/>
  <text x="317" y="226" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="9">State Machine</text>
  <!-- Actuation -->
  <rect x="465" y="55" width="150" height="200" rx="12" fill="#111827" stroke="#f59e0b" stroke-width="2"/>
  <text x="540" y="78" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="11" font-weight="700">ACTUATION</text>
  <text x="540" y="100" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">DC Motors</text>
  <text x="540" y="118" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Servo Motors</text>
  <text x="540" y="136" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Stepper Motors</text>
  <text x="540" y="154" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">LEDs / Displays</text>
  <text x="540" y="172" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Buzzers</text>
  <text x="540" y="190" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Grippers / Arms</text>
  <!-- Arrows -->
  <line x1="170" y1="155" x2="233" y2="155" stroke="#22d3ee" stroke-width="2" marker-end="url(#arr7)"/>
  <text x="200" y="148" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="8">sensor data</text>
  <line x1="400" y1="155" x2="463" y2="155" stroke="#34d399" stroke-width="2" marker-end="url(#arr8)"/>
  <text x="430" y="148" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">commands</text>
  <!-- Feedback loop -->
  <path d="M540 255 Q540 285 360 285 Q180 285 180 258" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arr9)"/>
  <text x="360" y="298" text-anchor="middle" fill="#f59e0b" font-family="Inter,sans-serif" font-size="8">Feedback loop: actuator output informs next sensor reading</text>
  <defs>
    <marker id="arr7" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#22d3ee"/></marker>
    <marker id="arr8" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#34d399"/></marker>
    <marker id="arr9" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#f59e0b"/></marker>
  </defs>
""",
    "Robot System Architecture: Perception (sensors) → Processing (microcontroller) → Actuation (motors)",
    720, 310,
)

ROBOTICS_CIRCUIT = _wrap(
    _DEFS + """
  <rect width="720" height="280" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#34d399" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">LED CIRCUIT WITH ARDUINO</text>
  <!-- Arduino board representation -->
  <rect x="250" y="60" width="220" height="140" rx="10" fill="#1a2e1a" stroke="#34d399" stroke-width="2.5"/>
  <text x="360" y="82" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="11" font-weight="700">ARDUINO UNO</text>
  <!-- Pins -->
  <g fill="#22d3ee" font-family="monospace" font-size="8">
    <rect x="264" y="95" width="50" height="14" rx="2" fill="rgba(34,211,238,0.15)" stroke="rgba(34,211,238,0.4)" stroke-width="1"/>
    <text x="289" y="106" text-anchor="middle" fill="#67e8f9">5V ⊕</text>
    <rect x="264" y="115" width="50" height="14" rx="2" fill="rgba(52,211,153,0.15)" stroke="rgba(52,211,153,0.4)" stroke-width="1"/>
    <text x="289" y="126" text-anchor="middle" fill="#6ee7b7">Pin 13</text>
    <rect x="264" y="135" width="50" height="14" rx="2" fill="rgba(99,102,241,0.15)" stroke="rgba(99,102,241,0.4)" stroke-width="1"/>
    <text x="289" y="146" text-anchor="middle" fill="#a5b4fc">GND ⊖</text>
  </g>
  <!-- LED symbol -->
  <circle cx="540" cy="120" r="22" fill="#111827" stroke="#fbbf24" stroke-width="2"/>
  <text x="540" y="116" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="14">💡</text>
  <text x="540" y="133" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="8">LED</text>
  <!-- Resistor symbol -->
  <rect x="600" y="110" width="50" height="20" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="625" y="124" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="9">220Ω</text>
  <!-- Wires -->
  <line x1="314" y1="122" x2="518" y2="122" stroke="#34d399" stroke-width="2"/>
  <text x="410" y="117" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">Signal wire</text>
  <line x1="562" y1="122" x2="598" y2="122" stroke="#fbbf24" stroke-width="2"/>
  <line x1="650" y1="120" x2="680" y2="120" stroke="#fbbf24" stroke-width="2"/>
  <line x1="680" y1="120" x2="680" y2="143" stroke="#fbbf24" stroke-width="2"/>
  <line x1="680" y1="143" x2="314" y2="143" stroke="#6366f1" stroke-width="2"/>
  <text x="500" y="158" text-anchor="middle" fill="#6366f1" font-family="Inter,sans-serif" font-size="8">Ground wire</text>
  <!-- 5V line -->
  <line x1="314" y1="102" x2="100" y2="102" stroke="#22d3ee" stroke-width="2"/>
  <line x1="100" y1="102" x2="100" y2="200" stroke="#22d3ee" stroke-width="2"/>
  <!-- Code snippet -->
  <rect x="30" y="200" width="660" height="50" rx="8" fill="#050608" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <text x="50" y="222" fill="#38bdf8" font-family="monospace" font-size="10">void loop() {'{'}</text>
  <text x="50" y="240" fill="#38bdf8" font-family="monospace" font-size="10">  digitalWrite(13, HIGH);  delay(1000);  digitalWrite(13, LOW);  delay(1000); {'}'}</text>
""",
    "LED Blink Circuit: Arduino digital pin → current-limiting resistor → LED → Ground",
    720, 265,
)


# ---------------------------------------------------------------------------
# DATA ANALYSIS VISUALS
# ---------------------------------------------------------------------------

DATA_CHART_TYPES = _wrap(
    _DEFS + """
  <rect width="720" height="310" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#38bdf8" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">DATA VISUALISATION CHART TYPES</text>
  <!-- Bar Chart -->
  <rect x="20" y="50" width="160" height="140" rx="10" fill="#111827" stroke="#6366f1" stroke-width="2"/>
  <text x="100" y="70" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="10" font-weight="700">BAR CHART</text>
  <text x="100" y="84" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="8">Compare categories</text>
  <rect x="38" y="148" width="18" height="28" fill="#6366f1"/>
  <rect x="62" y="128" width="18" height="48" fill="#6366f1" opacity="0.8"/>
  <rect x="86" y="110" width="18" height="66" fill="#6366f1" opacity="0.6"/>
  <rect x="110" y="120" width="18" height="56" fill="#6366f1" opacity="0.7"/>
  <rect x="134" y="138" width="18" height="38" fill="#6366f1" opacity="0.5"/>
  <line x1="30" y1="176" x2="165" y2="176" stroke="#94a3b8" stroke-width="1"/>
  <!-- Line Chart -->
  <rect x="195" y="50" width="160" height="140" rx="10" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <text x="275" y="70" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="10" font-weight="700">LINE CHART</text>
  <text x="275" y="84" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="8">Show trends over time</text>
  <polyline points="210,165 230,145 255,155 280,120 305,130 335,105 350,115" fill="none" stroke="#22d3ee" stroke-width="2.5"/>
  <circle cx="210" cy="165" r="3" fill="#22d3ee"/>
  <circle cx="230" cy="145" r="3" fill="#22d3ee"/>
  <circle cx="255" cy="155" r="3" fill="#22d3ee"/>
  <circle cx="280" cy="120" r="3" fill="#22d3ee"/>
  <circle cx="305" cy="130" r="3" fill="#22d3ee"/>
  <circle cx="335" cy="105" r="3" fill="#22d3ee"/>
  <!-- Pie Chart -->
  <rect x="370" y="50" width="160" height="140" rx="10" fill="#111827" stroke="#34d399" stroke-width="2"/>
  <text x="450" y="70" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="10" font-weight="700">PIE CHART</text>
  <text x="450" y="84" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="8">Show proportions</text>
  <circle cx="450" cy="140" r="38" fill="none" stroke="#1e293b" stroke-width="1"/>
  <path d="M450,140 L450,102 A38,38 0 0 1 483,159 Z" fill="#6366f1"/>
  <path d="M450,140 L483,159 A38,38 0 0 1 430,177 Z" fill="#22d3ee"/>
  <path d="M450,140 L430,177 A38,38 0 0 1 413,119 Z" fill="#34d399"/>
  <path d="M450,140 L413,119 A38,38 0 0 1 450,102 Z" fill="#f59e0b"/>
  <!-- Scatter Plot -->
  <rect x="545" y="50" width="160" height="140" rx="10" fill="#111827" stroke="#f59e0b" stroke-width="2"/>
  <text x="625" y="70" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="10" font-weight="700">SCATTER PLOT</text>
  <text x="625" y="84" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="8">Show correlation</text>
  <circle cx="570" cy="158" r="4" fill="#f59e0b"/>
  <circle cx="585" cy="150" r="4" fill="#f59e0b"/>
  <circle cx="598" cy="145" r="4" fill="#f59e0b"/>
  <circle cx="612" cy="138" r="4" fill="#f59e0b"/>
  <circle cx="628" cy="130" r="4" fill="#f59e0b"/>
  <circle cx="643" cy="122" r="4" fill="#f59e0b"/>
  <circle cx="658" cy="116" r="4" fill="#f59e0b"/>
  <line x1="563" y1="168" x2="668" y2="108" stroke="rgba(245,158,11,0.4)" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="625" y="176" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="7">trend line</text>
  <!-- When to use legend -->
  <text x="360" y="220" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="10" font-weight="600">When to use each chart:</text>
  <text x="360" y="240" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Bar → categories · Line → time trends · Pie → proportions (≤ 6 slices) · Scatter → correlations</text>
  <text x="360" y="258" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="8">Rule: choose the chart that best answers your specific business question</text>
""",
    "Chart Types: Bar, Line, Pie, and Scatter plots — when to use each",
    720, 270,
)

DATA_PIVOT_TABLE = _wrap(
    _DEFS + """
  <rect width="720" height="300" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#38bdf8" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">EXCEL PIVOT TABLE CONCEPT</text>
  <!-- Raw data table -->
  <text x="175" y="58" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="11" font-weight="600">Raw Data</text>
  <rect x="20" y="65" width="310" height="185" rx="10" fill="#111827" stroke="rgba(148,163,184,0.3)" stroke-width="1.5"/>
  <rect x="20" y="65" width="310" height="28" rx="10" fill="rgba(99,102,241,0.2)"/>
  <g font-family="monospace" font-size="9" fill="#a5b4fc">
    <text x="45" y="84">Region</text>
    <text x="120" y="84">Product</text>
    <text x="210" y="84">Month</text>
    <text x="280" y="84">Sales</text>
  </g>
  <g font-family="monospace" font-size="9" fill="#94a3b8">
    <text x="45" y="108">North</text><text x="120" y="108">Laptop</text><text x="210" y="108">Jan</text><text x="280" y="108">1200</text>
    <text x="45" y="124">South</text><text x="120" y="124">Phone</text><text x="210" y="124">Jan</text><text x="280" y="124">800</text>
    <text x="45" y="140">North</text><text x="120" y="140">Phone</text><text x="210" y="140">Feb</text><text x="280" y="140">950</text>
    <text x="45" y="156">East</text><text x="120" y="156">Laptop</text><text x="210" y="156">Feb</text><text x="280" y="156">1400</text>
    <text x="45" y="172">South</text><text x="120" y="172">Laptop</text><text x="210" y="172">Jan</text><text x="280" y="172">1100</text>
    <text x="45" y="188">East</text><text x="120" y="188">Phone</text><text x="210" y="188">Feb</text><text x="280" y="188">700</text>
    <text x="45" y="204">North</text><text x="120" y="204">Laptop</text><text x="210" y="204">Mar</text><text x="280" y="204">1350</text>
    <text x="45" y="220">South</text><text x="120" y="220">Phone</text><text x="210" y="220">Mar</text><text x="280" y="220">860</text>
  </g>
  <!-- Arrow + pivot label -->
  <text x="360" y="152" text-anchor="middle" fill="#22d3ee" font-family="Inter,sans-serif" font-size="16">→</text>
  <text x="360" y="168" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="8">PIVOT</text>
  <!-- Pivot result -->
  <text x="555" y="58" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="11" font-weight="600">Pivot Result (Sum of Sales)</text>
  <rect x="390" y="65" width="310" height="170" rx="10" fill="#111827" stroke="rgba(34,211,238,0.4)" stroke-width="1.5"/>
  <rect x="390" y="65" width="310" height="28" rx="10" fill="rgba(34,211,238,0.15)"/>
  <g font-family="monospace" font-size="9">
    <text x="420" y="84" fill="#67e8f9">Region</text>
    <text x="505" y="84" fill="#67e8f9">Laptop</text>
    <text x="590" y="84" fill="#67e8f9">Phone</text>
    <text x="672" y="84" fill="#67e8f9">Total</text>
    <text x="420" y="110" fill="#94a3b8">North</text><text x="505" y="110" fill="#34d399">2,550</text><text x="590" y="110" fill="#34d399">950</text><text x="672" y="110" fill="#fbbf24">3,500</text>
    <text x="420" y="130" fill="#94a3b8">South</text><text x="505" y="130" fill="#34d399">1,100</text><text x="590" y="130" fill="#34d399">1,660</text><text x="672" y="130" fill="#fbbf24">2,760</text>
    <text x="420" y="150" fill="#94a3b8">East</text><text x="505" y="150" fill="#34d399">1,400</text><text x="590" y="150" fill="#34d399">700</text><text x="672" y="150" fill="#fbbf24">2,100</text>
    <text x="420" y="178" fill="#6366f1" font-weight="700">Grand Total</text><text x="505" y="178" fill="#a5b4fc">5,050</text><text x="590" y="178" fill="#a5b4fc">3,310</text><text x="672" y="178" fill="#a5b4fc">8,360</text>
  </g>
  <text x="360" y="270" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="9">Pivot tables instantly summarise hundreds of rows into a meaningful cross-tab using drag-and-drop fields</text>
""",
    "Excel Pivot Table: Converting raw sales records into a cross-tabulated summary",
    720, 285,
)


# ---------------------------------------------------------------------------
# ELECTRICAL & ELECTRONICS ENGINEERING VISUALS
# ---------------------------------------------------------------------------

EEE_OHM_LAW = _wrap(
    _DEFS + """
  <rect width="720" height="300" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">OHM'S LAW &amp; BASIC CIRCUIT</text>
  <!-- Triangle -->
  <polygon points="280,60 200,200 360,200" fill="none" stroke="#f59e0b" stroke-width="2.5"/>
  <line x1="280" y1="130" x2="280" y2="200" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,3"/>
  <line x1="200" y1="130" x2="360" y2="130" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="280" y="112" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="20" font-weight="800">V</text>
  <text x="225" y="170" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="18" font-weight="800">I</text>
  <text x="335" y="170" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="18" font-weight="800">R</text>
  <!-- Labels -->
  <text x="280" y="90" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Voltage (V)</text>
  <text x="185" y="182" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Current (I)</text>
  <text x="375" y="182" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Resistance (R)</text>
  <!-- Formulas -->
  <rect x="415" y="60" width="280" height="160" rx="12" fill="#111827" stroke="rgba(245,158,11,0.3)" stroke-width="1.5"/>
  <text x="555" y="88" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="12" font-weight="700">Formula Triangle</text>
  <text x="555" y="115" text-anchor="middle" fill="#f8fafc" font-family="monospace" font-size="14" font-weight="700">V = I × R</text>
  <text x="555" y="140" text-anchor="middle" fill="#67e8f9" font-family="monospace" font-size="13">I = V ÷ R</text>
  <text x="555" y="165" text-anchor="middle" fill="#6ee7b7" font-family="monospace" font-size="13">R = V ÷ I</text>
  <text x="555" y="188" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Cover the unknown to read the formula</text>
  <!-- Simple series circuit -->
  <text x="360" y="230" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="10" font-weight="600">Series Circuit: V = 9V, R = 100Ω → I = V/R = 0.09A = 90 mA</text>
  <text x="360" y="250" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="9">Units: Voltage (V = Volts) · Current (I = Amperes) · Resistance (R = Ohms Ω)</text>
  <text x="360" y="268" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="9">Power: P = V × I = I²R = V²/R  (Watts)</text>
""",
    "Ohm's Law: V = I × R — Voltage, Current, and Resistance relationship",
    720, 280,
)

EEE_CIRCUIT_DIAGRAM = _wrap(
    _DEFS + """
  <rect width="720" height="300" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">SERIES vs PARALLEL CIRCUITS</text>
  <!-- SERIES -->
  <text x="175" y="58" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="11" font-weight="600">Series Circuit</text>
  <!-- Battery -->
  <rect x="30" y="80" width="30" height="50" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="45" y="102" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="8">9V</text>
  <text x="45" y="116" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="7">Batt</text>
  <!-- Wires series -->
  <line x1="60" y1="90" x2="110" y2="90" stroke="#22d3ee" stroke-width="2"/>
  <!-- R1 -->
  <rect x="110" y="82" width="50" height="18" rx="3" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="135" y="95" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="8">R1 100Ω</text>
  <line x1="160" y1="90" x2="210" y2="90" stroke="#22d3ee" stroke-width="2"/>
  <!-- R2 -->
  <rect x="210" y="82" width="50" height="18" rx="3" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="235" y="95" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="8">R2 150Ω</text>
  <line x1="260" y1="90" x2="300" y2="90" stroke="#22d3ee" stroke-width="2"/>
  <line x1="300" y1="90" x2="300" y2="120" stroke="#22d3ee" stroke-width="2"/>
  <line x1="30" y1="130" x2="300" y2="130" stroke="#22d3ee" stroke-width="2"/>
  <!-- Series formulas -->
  <rect x="30" y="145" width="310" height="55" rx="6" fill="rgba(34,211,238,0.05)" stroke="rgba(34,211,238,0.2)" stroke-width="1"/>
  <text x="185" y="163" text-anchor="middle" fill="#67e8f9" font-family="monospace" font-size="9">R_total = R1+R2 = 250Ω</text>
  <text x="185" y="179" text-anchor="middle" fill="#67e8f9" font-family="monospace" font-size="9">I = 9/250 = 36mA (same everywhere)</text>
  <text x="185" y="195" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">One path · one current · voltages add up</text>
  <!-- PARALLEL -->
  <text x="545" y="58" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="11" font-weight="600">Parallel Circuit</text>
  <!-- Battery parallel -->
  <rect x="385" y="70" width="30" height="70" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="400" y="100" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="8">9V</text>
  <line x1="415" y1="80" x2="460" y2="80" stroke="#34d399" stroke-width="2"/>
  <line x1="460" y1="80" x2="460" y2="130" stroke="#34d399" stroke-width="1.5"/>
  <!-- R1 parallel -->
  <line x1="460" y1="90" x2="540" y2="90" stroke="#34d399" stroke-width="2"/>
  <rect x="490" y="82" width="50" height="18" rx="3" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="515" y="95" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="8">R1 100Ω</text>
  <line x1="540" y1="90" x2="610" y2="90" stroke="#34d399" stroke-width="2"/>
  <!-- R2 parallel -->
  <line x1="460" y1="120" x2="540" y2="120" stroke="#34d399" stroke-width="2"/>
  <rect x="490" y="112" width="50" height="18" rx="3" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="515" y="125" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="8">R2 150Ω</text>
  <line x1="540" y1="120" x2="610" y2="120" stroke="#34d399" stroke-width="2"/>
  <line x1="610" y1="80" x2="610" y2="130" stroke="#34d399" stroke-width="1.5"/>
  <line x1="610" y1="105" x2="680" y2="105" stroke="#34d399" stroke-width="2"/>
  <line x1="680" y1="105" x2="680" y2="140" stroke="#34d399" stroke-width="2"/>
  <line x1="385" y1="140" x2="680" y2="140" stroke="#34d399" stroke-width="2"/>
  <!-- Parallel formula -->
  <rect x="385" y="150" width="310" height="55" rx="6" fill="rgba(52,211,153,0.05)" stroke="rgba(52,211,153,0.2)" stroke-width="1"/>
  <text x="540" y="168" text-anchor="middle" fill="#6ee7b7" font-family="monospace" font-size="9">1/R = 1/100+1/150 = 60Ω</text>
  <text x="540" y="184" text-anchor="middle" fill="#6ee7b7" font-family="monospace" font-size="9">I_total = 9/60 = 150mA</text>
  <text x="540" y="200" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Multi-path · voltage same · currents add</text>
  <text x="360" y="240" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="9">Series: higher resistance, single path. Parallel: lower total resistance, multiple paths (used in home wiring)</text>
""",
    "Series vs Parallel Circuits: How resistance, current, and voltage differ",
    720, 255,
)


# ---------------------------------------------------------------------------
# CYBERSECURITY VISUALS
# ---------------------------------------------------------------------------

CYBER_OSI_MODEL = _wrap(
    _DEFS + """
  <rect width="720" height="330" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#f43f5e" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">OSI MODEL — 7 LAYERS</text>
  <!-- Layers (top to bottom) -->
  <!-- 7 Application -->
  <rect x="180" y="45" width="360" height="32" rx="6" fill="rgba(99,102,241,0.25)" stroke="#6366f1" stroke-width="1.5"/>
  <text x="270" y="65" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="10" font-weight="700">7. Application</text>
  <text x="490" y="65" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">HTTP, FTP, SMTP, DNS — User-facing protocols</text>
  <!-- 6 Presentation -->
  <rect x="180" y="83" width="360" height="32" rx="6" fill="rgba(99,102,241,0.18)" stroke="#6366f1" stroke-width="1"/>
  <text x="270" y="103" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="10" font-weight="700">6. Presentation</text>
  <text x="490" y="103" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">SSL/TLS, encryption, compression, encoding</text>
  <!-- 5 Session -->
  <rect x="180" y="121" width="360" height="32" rx="6" fill="rgba(34,211,238,0.15)" stroke="#22d3ee" stroke-width="1"/>
  <text x="270" y="141" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="10" font-weight="700">5. Session</text>
  <text x="490" y="141" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Session management, authentication, sync</text>
  <!-- 4 Transport -->
  <rect x="180" y="159" width="360" height="32" rx="6" fill="rgba(52,211,153,0.15)" stroke="#34d399" stroke-width="1.5"/>
  <text x="270" y="179" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="10" font-weight="700">4. Transport</text>
  <text x="490" y="179" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">TCP (reliable), UDP (fast) — ports, flow control</text>
  <!-- 3 Network -->
  <rect x="180" y="197" width="360" height="32" rx="6" fill="rgba(245,158,11,0.15)" stroke="#f59e0b" stroke-width="1"/>
  <text x="270" y="217" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="10" font-weight="700">3. Network</text>
  <text x="490" y="217" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">IP addressing, routing (routers) — packets</text>
  <!-- 2 Data Link -->
  <rect x="180" y="235" width="360" height="32" rx="6" fill="rgba(244,63,94,0.12)" stroke="#f43f5e" stroke-width="1"/>
  <text x="270" y="255" text-anchor="middle" fill="#fda4af" font-family="Inter,sans-serif" font-size="10" font-weight="700">2. Data Link</text>
  <text x="490" y="255" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">MAC addresses, switches, frames, error detection</text>
  <!-- 1 Physical -->
  <rect x="180" y="273" width="360" height="32" rx="6" fill="rgba(244,63,94,0.08)" stroke="#f43f5e" stroke-width="1"/>
  <text x="270" y="293" text-anchor="middle" fill="#fda4af" font-family="Inter,sans-serif" font-size="10" font-weight="700">1. Physical</text>
  <text x="490" y="293" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Cables, Wi-Fi signals, bits — actual hardware</text>
  <!-- Side arrows -->
  <text x="145" y="170" text-anchor="middle" fill="#34d399" font-family="Inter,sans-serif" font-size="8">Sender</text>
  <text x="145" y="182" text-anchor="middle" fill="#34d399" font-family="Inter,sans-serif" font-size="8">encapsulates</text>
  <text x="145" y="194" text-anchor="middle" fill="#34d399" font-family="Inter,sans-serif" font-size="8">↓ down</text>
  <text x="590" y="158" text-anchor="middle" fill="#6366f1" font-family="Inter,sans-serif" font-size="8">Receiver</text>
  <text x="590" y="170" text-anchor="middle" fill="#6366f1" font-family="Inter,sans-serif" font-size="8">decodes</text>
  <text x="590" y="182" text-anchor="middle" fill="#6366f1" font-family="Inter,sans-serif" font-size="8">↑ up</text>
  <text x="90" y="170" fill="#34d399" font-family="Inter,sans-serif" font-size="18">↓</text>
  <text x="635" y="178" fill="#6366f1" font-family="Inter,sans-serif" font-size="18">↑</text>
  <!-- Mnemonic -->
  <text x="360" y="318" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="9">Mnemonic: "Please Do Not Throw Sausage Pizza Away" (Physical → Application)</text>
""",
    "OSI Model: 7 network layers from Physical hardware to Application protocols",
    720, 325,
)

CYBER_ENCRYPTION = _wrap(
    _DEFS + """
  <rect width="720" height="300" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#f43f5e" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">ENCRYPTION: SYMMETRIC vs ASYMMETRIC</text>
  <!-- Symmetric -->
  <rect x="20" y="50" width="320" height="200" rx="12" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <text x="180" y="74" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="11" font-weight="700">SYMMETRIC (AES)</text>
  <text x="180" y="90" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Same key for encrypt &amp; decrypt</text>
  <!-- Key icon -->
  <text x="80" y="130" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="28">🔑</text>
  <text x="80" y="152" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Shared Secret Key</text>
  <!-- Encrypt arrow -->
  <line x1="130" y1="130" x2="230" y2="130" stroke="#22d3ee" stroke-width="2" marker-end="url(#arre)"/>
  <text x="180" y="122" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="8">Encrypt →</text>
  <!-- Ciphertext -->
  <rect x="230" y="112" width="85" height="34" rx="5" fill="rgba(34,211,238,0.1)" stroke="rgba(34,211,238,0.3)" stroke-width="1"/>
  <text x="272" y="134" text-anchor="middle" fill="#64748b" font-family="monospace" font-size="8">x9#Kp!2Q</text>
  <!-- Decrypt arrow -->
  <line x1="230" y1="160" x2="130" y2="160" stroke="#34d399" stroke-width="2" marker-end="url(#arrd)"/>
  <text x="180" y="152" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">← Decrypt</text>
  <!-- Pros/cons -->
  <text x="180" y="195" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="9">✓ Fast · simple · good for large data</text>
  <text x="180" y="212" text-anchor="middle" fill="#fda4af" font-family="Inter,sans-serif" font-size="9">✗ Key distribution problem</text>
  <text x="180" y="229" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Used in: file encryption, database at rest</text>
  <!-- Asymmetric -->
  <rect x="380" y="50" width="320" height="200" rx="12" fill="#111827" stroke="#f43f5e" stroke-width="2"/>
  <text x="540" y="74" text-anchor="middle" fill="#fda4af" font-family="Inter,sans-serif" font-size="11" font-weight="700">ASYMMETRIC (RSA)</text>
  <text x="540" y="90" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="9">Public key encrypts · Private key decrypts</text>
  <!-- Public key -->
  <text x="420" y="128" text-anchor="middle" fill="#22d3ee" font-family="Inter,sans-serif" font-size="24">🔐</text>
  <text x="420" y="148" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="8">Public Key</text>
  <text x="420" y="160" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="7">(shared openly)</text>
  <!-- Private key -->
  <text x="665" y="128" text-anchor="middle" fill="#f43f5e" font-family="Inter,sans-serif" font-size="24">🗝️</text>
  <text x="665" y="148" text-anchor="middle" fill="#fda4af" font-family="Inter,sans-serif" font-size="8">Private Key</text>
  <text x="665" y="160" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="7">(kept secret)</text>
  <!-- Arrows -->
  <line x1="445" y1="133" x2="640" y2="133" stroke="#f43f5e" stroke-width="2" marker-end="url(#arre2)"/>
  <text x="542" y="125" text-anchor="middle" fill="#fda4af" font-family="Inter,sans-serif" font-size="8">Encrypt with public →</text>
  <!-- Pros/cons -->
  <text x="540" y="195" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="9">✓ Secure key exchange · digital signatures</text>
  <text x="540" y="212" text-anchor="middle" fill="#fda4af" font-family="Inter,sans-serif" font-size="9">✗ Slower · computationally expensive</text>
  <text x="540" y="229" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Used in: HTTPS handshake, SSH, certificates</text>
  <text x="360" y="270" text-anchor="middle" fill="#64748b" font-family="Inter,sans-serif" font-size="9">HTTPS uses both: asymmetric to exchange a session key, then symmetric (AES) for the actual data</text>
  <defs>
    <marker id="arre" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#22d3ee"/></marker>
    <marker id="arrd" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#34d399"/></marker>
    <marker id="arre2" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#f43f5e"/></marker>
  </defs>
""",
    "Encryption: Symmetric (AES) vs Asymmetric (RSA) — keys, flow, and use cases",
    720, 285,
)

CYBER_NETWORK_ATTACK = _wrap(
    _DEFS + """
  <rect width="720" height="300" rx="16" fill="#0b0f19"/>
  <text x="360" y="28" text-anchor="middle" fill="#f43f5e" font-family="Inter,sans-serif" font-size="14" font-weight="700" letter-spacing="1">COMMON NETWORK ATTACK TYPES</text>
  <!-- MITM -->
  <rect x="20" y="55" width="200" height="100" rx="10" fill="#111827" stroke="#f43f5e" stroke-width="2"/>
  <text x="120" y="76" text-anchor="middle" fill="#fda4af" font-family="Inter,sans-serif" font-size="10" font-weight="700">Man-in-the-Middle</text>
  <text x="120" y="93" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Client ⟷ 👤Attacker ⟷ Server</text>
  <text x="120" y="110" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Intercepts &amp; alters traffic</text>
  <text x="120" y="127" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">Defence: HTTPS · Certificate pinning</text>
  <text x="120" y="143" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">· HSTS headers</text>
  <!-- SQL Injection -->
  <rect x="260" y="55" width="200" height="100" rx="10" fill="#111827" stroke="#f59e0b" stroke-width="2"/>
  <text x="360" y="76" text-anchor="middle" fill="#fbbf24" font-family="Inter,sans-serif" font-size="10" font-weight="700">SQL Injection</text>
  <text x="360" y="96" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="8">' OR 1=1 --</text>
  <text x="360" y="112" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Malicious input in DB queries</text>
  <text x="360" y="130" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">Defence: Parameterised queries</text>
  <text x="360" y="145" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">· ORM · Input validation</text>
  <!-- DDoS -->
  <rect x="500" y="55" width="200" height="100" rx="10" fill="#111827" stroke="#6366f1" stroke-width="2"/>
  <text x="600" y="76" text-anchor="middle" fill="#a5b4fc" font-family="Inter,sans-serif" font-size="10" font-weight="700">DDoS Attack</text>
  <text x="600" y="95" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Millions of bots → Server overwhelmed</text>
  <text x="600" y="112" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Floods bandwidth / CPU</text>
  <text x="600" y="130" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">Defence: CDN · Rate limiting</text>
  <text x="600" y="145" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">· WAF · Cloudflare</text>
  <!-- XSS -->
  <rect x="20" y="185" width="200" height="90" rx="10" fill="#111827" stroke="#22d3ee" stroke-width="2"/>
  <text x="120" y="205" text-anchor="middle" fill="#67e8f9" font-family="Inter,sans-serif" font-size="10" font-weight="700">XSS (Cross-Site Scripting)</text>
  <text x="120" y="223" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Injects malicious JS into pages</text>
  <text x="120" y="240" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Steals cookies / session tokens</text>
  <text x="120" y="258" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">Defence: CSP headers · sanitise output</text>
  <!-- Phishing -->
  <rect x="260" y="185" width="200" height="90" rx="10" fill="#111827" stroke="#34d399" stroke-width="2"/>
  <text x="360" y="205" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="10" font-weight="700">Phishing</text>
  <text x="360" y="223" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Fake emails / sites trick users</text>
  <text x="360" y="240" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Steals credentials / payment data</text>
  <text x="360" y="258" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">Defence: MFA · Security awareness</text>
  <!-- Brute Force -->
  <rect x="500" y="185" width="200" height="90" rx="10" fill="#111827" stroke="#f43f5e" stroke-width="2"/>
  <text x="600" y="205" text-anchor="middle" fill="#fda4af" font-family="Inter,sans-serif" font-size="10" font-weight="700">Brute Force</text>
  <text x="600" y="223" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Automated password guessing</text>
  <text x="600" y="240" text-anchor="middle" fill="#94a3b8" font-family="Inter,sans-serif" font-size="8">Tries millions of combinations</text>
  <text x="600" y="258" text-anchor="middle" fill="#6ee7b7" font-family="Inter,sans-serif" font-size="8">Defence: Lockout · MFA · Hashing</text>
""",
    "Common Network Attacks: MITM, SQL Injection, DDoS, XSS, Phishing, Brute Force",
    720, 285,
)


# ---------------------------------------------------------------------------
# VISUAL REGISTRY — domain × concept keyword → list of visuals
# ---------------------------------------------------------------------------

# Maps domain slug → list of (keyword_fragment, visual_dict) tuples.
# The teach_concept view will select visuals whose keyword appears in concept.name.lower()

DOMAIN_VISUALS = {
    "web_dev": [
        ("dns", [WEB_DNS_FLOW]),
        ("http", [WEB_HTTP_CYCLE]),
        ("web basic", [WEB_DNS_FLOW, WEB_HTTP_CYCLE]),
        ("api", [WEB_API_ARCHITECTURE]),
        ("rest", [WEB_API_ARCHITECTURE]),
        ("database", [WEB_DB_DIAGRAM]),
        ("sql", [WEB_DB_DIAGRAM]),
        ("auth", [WEB_API_ARCHITECTURE]),
        ("javascript", [WEB_HTTP_CYCLE]),
        ("react", [WEB_API_ARCHITECTURE]),
        ("deploy", [WEB_API_ARCHITECTURE]),
        ("html", [WEB_HTTP_CYCLE]),
        ("css", [WEB_HTTP_CYCLE]),
        ("git", [WEB_API_ARCHITECTURE]),
        ("django", [WEB_API_ARCHITECTURE, WEB_DB_DIAGRAM]),
    ],
    "ai_ml": [
        ("foundation", [AI_ML_PIPELINE]),
        ("regression", [AI_ML_PIPELINE, AI_CONFUSION_MATRIX]),
        ("classification", [AI_CONFUSION_MATRIX, AI_ML_PIPELINE]),
        ("neural", [AI_NEURAL_NETWORK]),
        ("deep learning", [AI_NEURAL_NETWORK]),
        ("pipeline", [AI_ML_PIPELINE]),
        ("feature", [AI_ML_PIPELINE]),
        ("pandas", [AI_ML_PIPELINE]),
        ("decision tree", [AI_CONFUSION_MATRIX]),
        ("random forest", [AI_CONFUSION_MATRIX]),
        ("logistic", [AI_CONFUSION_MATRIX, AI_ML_PIPELINE]),
        ("text", [AI_ML_PIPELINE]),
        ("nlp", [AI_ML_PIPELINE]),
        ("llm", [AI_NEURAL_NETWORK]),
        ("evaluation", [AI_CONFUSION_MATRIX]),
    ],
    "robotics": [
        ("sensor", [ROBOTICS_ARCHITECTURE]),
        ("motor", [ROBOTICS_ARCHITECTURE]),
        ("architecture", [ROBOTICS_ARCHITECTURE]),
        ("arduino", [ROBOTICS_CIRCUIT]),
        ("led", [ROBOTICS_CIRCUIT]),
        ("circuit", [ROBOTICS_CIRCUIT]),
        ("pid", [ROBOTICS_ARCHITECTURE]),
        ("microcontroller", [ROBOTICS_CIRCUIT, ROBOTICS_ARCHITECTURE]),
        ("robot", [ROBOTICS_ARCHITECTURE]),
        ("autonomous", [ROBOTICS_ARCHITECTURE]),
        ("foundation", [ROBOTICS_ARCHITECTURE]),
        ("programming", [ROBOTICS_CIRCUIT]),
    ],
    "data_analytics": [
        ("excel", [DATA_PIVOT_TABLE]),
        ("pivot", [DATA_PIVOT_TABLE]),
        ("chart", [DATA_CHART_TYPES]),
        ("visuali", [DATA_CHART_TYPES]),
        ("power bi", [DATA_CHART_TYPES]),
        ("dashboard", [DATA_CHART_TYPES, DATA_PIVOT_TABLE]),
        ("sql", [DATA_PIVOT_TABLE]),
        ("pandas", [DATA_PIVOT_TABLE]),
        ("statistics", [DATA_CHART_TYPES]),
        ("window function", [DATA_PIVOT_TABLE]),
        ("capstone", [DATA_CHART_TYPES, DATA_PIVOT_TABLE]),
        ("business metrics", [DATA_CHART_TYPES]),
    ],
    "electronics": [
        ("ohm", [EEE_OHM_LAW]),
        ("circuit", [EEE_CIRCUIT_DIAGRAM, EEE_OHM_LAW]),
        ("series", [EEE_CIRCUIT_DIAGRAM]),
        ("parallel", [EEE_CIRCUIT_DIAGRAM]),
        ("voltage", [EEE_OHM_LAW]),
        ("current", [EEE_OHM_LAW]),
        ("resistance", [EEE_OHM_LAW, EEE_CIRCUIT_DIAGRAM]),
        ("power", [EEE_OHM_LAW]),
        ("transistor", [EEE_CIRCUIT_DIAGRAM]),
        ("capacitor", [EEE_CIRCUIT_DIAGRAM]),
        ("diode", [EEE_CIRCUIT_DIAGRAM]),
        ("ac dc", [EEE_OHM_LAW]),
        ("foundation", [EEE_OHM_LAW, EEE_CIRCUIT_DIAGRAM]),
        ("basic", [EEE_OHM_LAW]),
    ],
    "cybersecurity": [
        ("osi", [CYBER_OSI_MODEL]),
        ("network", [CYBER_OSI_MODEL, CYBER_NETWORK_ATTACK]),
        ("encryption", [CYBER_ENCRYPTION]),
        ("cryptograph", [CYBER_ENCRYPTION]),
        ("attack", [CYBER_NETWORK_ATTACK]),
        ("sql injection", [CYBER_NETWORK_ATTACK]),
        ("xss", [CYBER_NETWORK_ATTACK]),
        ("ddos", [CYBER_NETWORK_ATTACK]),
        ("phishing", [CYBER_NETWORK_ATTACK]),
        ("brute force", [CYBER_NETWORK_ATTACK]),
        ("authentication", [CYBER_ENCRYPTION]),
        ("firewall", [CYBER_OSI_MODEL]),
        ("penetration", [CYBER_NETWORK_ATTACK]),
        ("foundation", [CYBER_OSI_MODEL, CYBER_ENCRYPTION]),
        ("basic", [CYBER_OSI_MODEL]),
        ("web security", [CYBER_NETWORK_ATTACK]),
        ("https", [CYBER_ENCRYPTION]),
    ],
}

# Canonical domain slug normalisation (maps goal.domain values → registry keys)
DOMAIN_SLUG_MAP = {
    "web_dev": "web_dev",
    "full stack": "web_dev",
    "full stack development": "web_dev",
    "fullstack": "web_dev",
    "web development": "web_dev",
    "ai_ml": "ai_ml",
    "ai & machine learning": "ai_ml",
    "ai and machine learning": "ai_ml",
    "artificial intelligence": "ai_ml",
    "machine learning": "ai_ml",
    "robotics": "robotics",
    "data_analytics": "data_analytics",
    "data analytics": "data_analytics",
    "data analysis": "data_analytics",
    "electronics": "electronics",
    "electrical & electronics engineering": "electronics",
    "electrical and electronics engineering": "electronics",
    "eee": "electronics",
    "cybersecurity": "cybersecurity",
    "cyber security": "cybersecurity",
}


def get_visuals_for_concept(domain: str, concept_name: str) -> list:
    """
    Return a list of visual dicts (each with 'svg' and 'caption') appropriate
    for this domain and concept.  Returns at most 2 visuals to avoid clutter.
    """
    slug = DOMAIN_SLUG_MAP.get(domain.lower().strip(), "")
    if not slug:
        return []
    registry = DOMAIN_VISUALS.get(slug, [])
    name_lower = concept_name.lower()
    matched = []
    seen_captions = set()
    for keyword, visuals in registry:
        if keyword in name_lower:
            for v in visuals:
                if v["caption"] not in seen_captions:
                    matched.append(v)
                    seen_captions.add(v["caption"])
            if len(matched) >= 2:
                break
    # Fallback: return first visual for the domain if nothing matched
    if not matched and registry:
        first_visual = registry[0][1][0]
        matched = [first_visual]
    return matched[:2]

