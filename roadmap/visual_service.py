"""Educational Visual Learning Service for EXA AI HUB by TASBI AI SOLUTIONS.

Generates clean, responsive, domain-specific educational visuals (architecture diagrams,
flowcharts, process visualisations, technical illustrations, and comparison tables)
for the six learning domains:
1. Full Stack Development (web_dev)
2. AI & Machine Learning (ai_ml)
3. Robotics (robotics)
4. Data Analysis (data_analytics)
5. Electrical & Electronics Engineering (electronics)
6. Cybersecurity (cybersecurity)
"""

from typing import Dict, Any, List, Optional


def _svg_wrapper(inner_svg: str, view_box: str = "0 0 800 320", min_height: str = "240px") -> str:
    """Wraps SVG with responsive, accessible, scalable attributes."""
    return f"""<div class="visual-svg-container" style="width:100%; overflow-x:auto; margin:1rem 0; border-radius:12px; background:rgba(8,13,24,0.7); border:1px solid rgba(0,229,255,0.2); padding:1rem; box-sizing:border-box;">
<svg viewBox="{view_box}" xmlns="http://www.w3.org/2000/svg" style="width:100%; max-width:800px; height:auto; min-height:{min_height}; display:block; margin:0 auto; font-family:'Inter',system-ui,sans-serif;" role="img" aria-label="Technical Illustration">
<defs>
  <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#6366F1" stop-opacity="0.9"/>
  </linearGradient>
  <linearGradient id="emeraldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#10B981" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#059669" stop-opacity="0.9"/>
  </linearGradient>
  <linearGradient id="amberGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#D97706" stop-opacity="0.9"/>
  </linearGradient>
  <linearGradient id="darkCard" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#151D2F" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="#0B0F19" stop-opacity="0.95"/>
  </linearGradient>
  <filter id="glowEffect" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>
  <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 1 L 10 5 L 0 9 z" fill="#00E5FF" />
  </marker>
  <marker id="arrowEmerald" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981" />
  </marker>
</defs>
{inner_svg}
</svg>
</div>"""


# ==============================================================================
# 1. FULL STACK DEVELOPMENT VISUALS
# ==============================================================================

def _web_dev_request_response_svg() -> str:
    content = """
    <!-- Background grid -->
    <rect width="800" height="300" fill="transparent"/>
    
    <!-- Step 1: Client / Browser -->
    <rect x="40" y="60" width="160" height="180" rx="12" fill="url(#darkCard)" stroke="#6366F1" stroke-width="2"/>
    <circle cx="65" cy="85" r="5" fill="#EF4444"/>
    <circle cx="80" cy="85" r="5" fill="#F59E0B"/>
    <circle cx="95" cy="85" r="5" fill="#10B981"/>
    <text x="120" y="125" fill="#FFFFFF" font-size="14" font-weight="700" text-anchor="middle">Browser (Client)</text>
    <text x="120" y="150" fill="#94A3B8" font-size="11" text-anchor="middle">1. User Action</text>
    <text x="120" y="170" fill="#94A3B8" font-size="11" text-anchor="middle">2. DOM Render</text>
    <text x="120" y="210" fill="#00E5FF" font-size="12" font-weight="600" text-anchor="middle">HTML5 / CSS / JS</text>

    <!-- Arrow 1: HTTP Request -->
    <path d="M 205 110 L 325 110" stroke="#00E5FF" stroke-width="3" fill="none" marker-end="url(#arrow)"/>
    <text x="265" y="98" fill="#00E5FF" font-size="11" font-weight="600" text-anchor="middle">GET / POST HTTP/S</text>

    <!-- Arrow 2: HTTP Response -->
    <path d="M 325 190 L 205 190" stroke="#10B981" stroke-width="3" stroke-dasharray="6,4" fill="none" marker-end="url(#arrowEmerald)"/>
    <text x="265" y="212" fill="#10B981" font-size="11" font-weight="600" text-anchor="middle">JSON / HTML (200 OK)</text>

    <!-- Step 2: Web Server / Backend -->
    <rect x="330" y="60" width="180" height="180" rx="12" fill="url(#darkCard)" stroke="#00E5FF" stroke-width="2"/>
    <rect x="350" y="80" width="140" height="24" rx="4" fill="rgba(0,229,255,0.15)"/>
    <text x="420" y="96" fill="#00E5FF" font-size="12" font-weight="700" text-anchor="middle">Django / Express</text>
    <text x="420" y="135" fill="#FFFFFF" font-size="14" font-weight="700" text-anchor="middle">Web Server / App</text>
    <text x="420" y="160" fill="#94A3B8" font-size="11" text-anchor="middle">URL Router → Views</text>
    <text x="420" y="180" fill="#94A3B8" font-size="11" text-anchor="middle">Auth &amp; Business Logic</text>
    <text x="420" y="210" fill="#6366F1" font-size="12" font-weight="600" text-anchor="middle">RESTful Endpoints</text>

    <!-- Arrow 3: ORM / SQL Query -->
    <path d="M 515 110 L 605 110" stroke="#00E5FF" stroke-width="3" fill="none" marker-end="url(#arrow)"/>
    <text x="560" y="98" fill="#00E5FF" font-size="11" font-weight="600" text-anchor="middle">SQL Query</text>

    <!-- Arrow 4: Record Result -->
    <path d="M 605 190 L 515 190" stroke="#10B981" stroke-width="3" stroke-dasharray="6,4" fill="none" marker-end="url(#arrowEmerald)"/>
    <text x="560" y="212" fill="#10B981" font-size="11" font-weight="600" text-anchor="middle">QuerySet / Rows</text>

    <!-- Step 3: Database -->
    <rect x="610" y="60" width="150" height="180" rx="12" fill="url(#darkCard)" stroke="#10B981" stroke-width="2"/>
    <ellipse cx="685" cy="85" rx="40" ry="12" fill="none" stroke="#10B981" stroke-width="2"/>
    <path d="M 645 85 L 645 125 A 40 12 0 0 0 725 125 L 725 85" fill="none" stroke="#10B981" stroke-width="2"/>
    <text x="685" y="160" fill="#FFFFFF" font-size="14" font-weight="700" text-anchor="middle">Database</text>
    <text x="685" y="185" fill="#94A3B8" font-size="11" text-anchor="middle">PostgreSQL / SQLite</text>
    <text x="685" y="210" fill="#10B981" font-size="11" font-weight="600" text-anchor="middle">Tables, Joins, Indexes</text>
    """
    return _svg_wrapper(content, "0 0 800 300")


def _web_dev_mvc_mvt_svg() -> str:
    content = """
    <!-- MVT Pattern -->
    <rect x="40" y="30" width="720" height="260" rx="14" fill="url(#darkCard)" stroke="rgba(255,255,255,0.08)"/>
    <text x="400" y="60" fill="#00E5FF" font-size="16" font-weight="800" text-anchor="middle" letter-spacing="1">DJANGO MVT (MODEL - VIEW - TEMPLATE) ARCHITECTURE</text>
    
    <!-- User Request -->
    <rect x="70" y="100" width="130" height="90" rx="8" fill="#1E293B" stroke="#6366F1" stroke-width="2"/>
    <text x="135" y="135" fill="#FFFFFF" font-weight="700" font-size="13" text-anchor="middle">1. User Request</text>
    <text x="135" y="160" fill="#94A3B8" font-size="11" text-anchor="middle">urls.py Dispatcher</text>

    <!-- Arrow to View -->
    <path d="M 205 145 L 265 145" stroke="#00E5FF" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- View Controller -->
    <rect x="270" y="90" width="160" height="120" rx="8" fill="#1E293B" stroke="#00E5FF" stroke-width="2"/>
    <text x="350" y="125" fill="#00E5FF" font-weight="700" font-size="14" text-anchor="middle">2. View Logic</text>
    <text x="350" y="150" fill="#CBD5E1" font-size="11" text-anchor="middle">views.py Controller</text>
    <text x="350" y="170" fill="#94A3B8" font-size="10" text-anchor="middle">Calculations &amp; Triage</text>
    <text x="350" y="190" fill="#94A3B8" font-size="10" text-anchor="middle">Form Validation</text>

    <!-- Up/Down Arrows to Model and Template -->
    <path d="M 435 120 L 515 100" stroke="#10B981" stroke-width="2" marker-end="url(#arrowEmerald)"/>
    <path d="M 435 170 L 515 190" stroke="#F59E0B" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- Model -->
    <rect x="520" y="70" width="170" height="70" rx="8" fill="#1E293B" stroke="#10B981" stroke-width="2"/>
    <text x="605" y="98" fill="#10B981" font-weight="700" font-size="13" text-anchor="middle">3. Model (Data)</text>
    <text x="605" y="120" fill="#CBD5E1" font-size="11" text-anchor="middle">models.py &amp; Database ORM</text>

    <!-- Template -->
    <rect x="520" y="165" width="170" height="70" rx="8" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
    <text x="605" y="195" fill="#F59E0B" font-weight="700" font-size="13" text-anchor="middle">4. Template (Presentation)</text>
    <text x="605" y="218" fill="#CBD5E1" font-size="11" text-anchor="middle">HTML5 / Jinja2 Syntax</text>
    """
    return _svg_wrapper(content, "0 0 800 320")


# ==============================================================================
# 2. AI & MACHINE LEARNING VISUALS
# ==============================================================================

def _ai_ml_pipeline_svg() -> str:
    content = """
    <rect width="800" height="300" fill="transparent"/>
    <text x="400" y="40" fill="#00E5FF" font-size="16" font-weight="800" text-anchor="middle">END-TO-END MACHINE LEARNING WORKFLOW PIPELINE</text>

    <!-- Stage 1: Data Ingestion -->
    <rect x="30" y="80" width="125" height="140" rx="10" fill="url(#darkCard)" stroke="#6366F1" stroke-width="2"/>
    <text x="92" y="115" fill="#6366F1" font-size="13" font-weight="700" text-anchor="middle">1. Data</text>
    <text x="92" y="135" fill="#FFFFFF" font-size="11" text-anchor="middle">Ingestion</text>
    <text x="92" y="160" fill="#94A3B8" font-size="10" text-anchor="middle">CSV / SQL / APIs</text>
    <text x="92" y="180" fill="#94A3B8" font-size="10" text-anchor="middle">Raw Data</text>

    <path d="M 160 150 L 175 150" stroke="#00E5FF" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- Stage 2: Preprocessing -->
    <rect x="180" y="80" width="125" height="140" rx="10" fill="url(#darkCard)" stroke="#00E5FF" stroke-width="2"/>
    <text x="242" y="115" fill="#00E5FF" font-size="13" font-weight="700" text-anchor="middle">2. Clean &amp; EDA</text>
    <text x="242" y="135" fill="#FFFFFF" font-size="11" text-anchor="middle">Feature Eng.</text>
    <text x="242" y="160" fill="#94A3B8" font-size="10" text-anchor="middle">Handle Nulls</text>
    <text x="242" y="180" fill="#94A3B8" font-size="10" text-anchor="middle">Scaling (MinMax)</text>

    <path d="M 310 150 L 325 150" stroke="#00E5FF" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- Stage 3: Split -->
    <rect x="330" y="80" width="125" height="140" rx="10" fill="url(#darkCard)" stroke="#F59E0B" stroke-width="2"/>
    <text x="392" y="115" fill="#F59E0B" font-size="13" font-weight="700" text-anchor="middle">3. Train/Test</text>
    <text x="392" y="135" fill="#FFFFFF" font-size="11" text-anchor="middle">Split (80 / 20)</text>
    <text x="392" y="160" fill="#94A3B8" font-size="10" text-anchor="middle">X_train, y_train</text>
    <text x="392" y="180" fill="#94A3B8" font-size="10" text-anchor="middle">Prevent Leakage</text>

    <path d="M 460 150 L 475 150" stroke="#00E5FF" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- Stage 4: Modeling -->
    <rect x="480" y="80" width="135" height="140" rx="10" fill="url(#darkCard)" stroke="#10B981" stroke-width="2"/>
    <text x="547" y="115" fill="#10B981" font-size="13" font-weight="700" text-anchor="middle">4. Fit Model</text>
    <text x="547" y="135" fill="#FFFFFF" font-size="11" text-anchor="middle">Training</text>
    <text x="547" y="160" fill="#94A3B8" font-size="10" text-anchor="middle">Weights &amp; Biases</text>
    <text x="547" y="180" fill="#94A3B8" font-size="10" text-anchor="middle">Gradient Descent</text>

    <path d="M 620 150 L 635 150" stroke="#00E5FF" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- Stage 5: Evaluation & Deploy -->
    <rect x="640" y="80" width="130" height="140" rx="10" fill="url(#darkCard)" stroke="#EC4899" stroke-width="2"/>
    <text x="705" y="115" fill="#EC4899" font-size="13" font-weight="700" text-anchor="middle">5. Evaluate</text>
    <text x="705" y="135" fill="#FFFFFF" font-size="11" text-anchor="middle">Validation</text>
    <text x="705" y="160" fill="#94A3B8" font-size="10" text-anchor="middle">Accuracy &amp; F1</text>
    <text x="705" y="180" fill="#94A3B8" font-size="10" text-anchor="middle">Deploy / Infer</text>

    <text x="400" y="260" fill="#94A3B8" font-size="12" text-anchor="middle">Continuous Feedback Loop: Model Monitoring &amp; Data Drift Detection</text>
    """
    return _svg_wrapper(content, "0 0 800 280")


def _ai_ml_rag_architecture_svg() -> str:
    content = """
    <rect width="800" height="300" fill="transparent"/>
    <text x="400" y="35" fill="#00E5FF" font-size="15" font-weight="800" text-anchor="middle">RETRIEVAL-AUGMENTED GENERATION (RAG) SYSTEM ARCHITECTURE</text>
    
    <!-- User Query -->
    <rect x="40" y="65" width="140" height="90" rx="10" fill="url(#darkCard)" stroke="#6366F1" stroke-width="2"/>
    <text x="110" y="100" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">Learner / User</text>
    <text x="110" y="125" fill="#00E5FF" font-size="11" text-anchor="middle">Prompt Query</text>

    <!-- Embedding Model -->
    <path d="M 185 110 L 235 110" stroke="#00E5FF" stroke-width="2" marker-end="url(#arrow)"/>
    <rect x="240" y="65" width="140" height="90" rx="10" fill="url(#darkCard)" stroke="#00E5FF" stroke-width="2"/>
    <text x="310" y="100" fill="#00E5FF" font-size="12" font-weight="700" text-anchor="middle">Embedding Model</text>
    <text x="310" y="125" fill="#94A3B8" font-size="11" text-anchor="middle">Dense Vector (1536d)</text>

    <!-- Vector DB -->
    <path d="M 385 110 L 435 110" stroke="#00E5FF" stroke-width="2" marker-end="url(#arrow)"/>
    <rect x="440" y="60" width="150" height="100" rx="10" fill="url(#darkCard)" stroke="#10B981" stroke-width="2"/>
    <text x="515" y="95" fill="#10B981" font-size="13" font-weight="700" text-anchor="middle">Vector Database</text>
    <text x="515" y="120" fill="#94A3B8" font-size="11" text-anchor="middle">Cosine Similarity Search</text>
    <text x="515" y="140" fill="#CBD5E1" font-size="10" text-anchor="middle">Top-K Chunks Retrieved</text>

    <!-- LLM Generation -->
    <path d="M 595 110 L 645 110" stroke="#00E5FF" stroke-width="2" marker-end="url(#arrow)"/>
    <rect x="650" y="65" width="120" height="90" rx="10" fill="url(#darkCard)" stroke="#EC4899" stroke-width="2"/>
    <text x="710" y="100" fill="#EC4899" font-size="12" font-weight="700" text-anchor="middle">LLM Reasoning</text>
    <text x="710" y="125" fill="#CBD5E1" font-size="11" text-anchor="middle">Grounded Answer</text>

    <!-- Document Ingestion Process -->
    <rect x="40" y="185" width="730" height="90" rx="10" fill="#151D2F" stroke="rgba(255,255,255,0.08)"/>
    <text x="60" y="215" fill="#F59E0B" font-size="12" font-weight="700">Offline Ingestion Pipeline:</text>
    <text x="60" y="240" fill="#CBD5E1" font-size="11">Raw Documents (.pdf/.txt) ➔ Clean &amp; Semantic Chunking ➔ Embedding Generator ➔ Indexed in Vector Store</text>
    """
    return _svg_wrapper(content, "0 0 800 295")


# ==============================================================================
# 3. ROBOTICS VISUALS
# ==============================================================================

def _robotics_sense_think_act_svg() -> str:
    content = """
    <rect width="800" height="300" fill="transparent"/>
    <text x="400" y="35" fill="#00E5FF" font-size="16" font-weight="800" text-anchor="middle">ROBOTICS FEEDBACK LOOP: SENSE ➔ THINK ➔ ACT</text>

    <!-- Sense Block -->
    <rect x="60" y="80" width="180" height="140" rx="12" fill="url(#darkCard)" stroke="#00E5FF" stroke-width="2"/>
    <text x="150" y="115" fill="#00E5FF" font-size="14" font-weight="700" text-anchor="middle">1. SENSE</text>
    <text x="150" y="145" fill="#FFFFFF" font-size="11" text-anchor="middle">Ultrasonic, LiDAR</text>
    <text x="150" y="165" fill="#94A3B8" font-size="11" text-anchor="middle">IMU / Encoders</text>
    <text x="150" y="195" fill="#10B981" font-size="10" text-anchor="middle">Analog / Digital Signals</text>

    <!-- Arrow Sense to Think -->
    <path d="M 245 150 L 305 150" stroke="#00E5FF" stroke-width="3" fill="none" marker-end="url(#arrow)"/>
    <text x="275" y="140" fill="#00E5FF" font-size="10" text-anchor="middle">Telemetry</text>

    <!-- Think Block -->
    <rect x="310" y="70" width="180" height="160" rx="12" fill="url(#darkCard)" stroke="#6366F1" stroke-width="2"/>
    <text x="400" y="105" fill="#6366F1" font-size="14" font-weight="700" text-anchor="middle">2. THINK</text>
    <text x="400" y="135" fill="#FFFFFF" font-size="11" text-anchor="middle">Microcontroller / ROS</text>
    <text x="400" y="155" fill="#94A3B8" font-size="11" text-anchor="middle">PID Control Loop</text>
    <text x="400" y="175" fill="#94A3B8" font-size="11" text-anchor="middle">State Machine Logic</text>
    <text x="400" y="205" fill="#F59E0B" font-size="10" text-anchor="middle">Error = Target - Measured</text>

    <!-- Arrow Think to Act -->
    <path d="M 495 150 L 555 150" stroke="#00E5FF" stroke-width="3" fill="none" marker-end="url(#arrow)"/>
    <text x="525" y="140" fill="#00E5FF" font-size="10" text-anchor="middle">PWM Signal</text>

    <!-- Act Block -->
    <rect x="560" y="80" width="180" height="140" rx="12" fill="url(#darkCard)" stroke="#10B981" stroke-width="2"/>
    <text x="650" y="115" fill="#10B981" font-size="14" font-weight="700" text-anchor="middle">3. ACT</text>
    <text x="650" y="145" fill="#FFFFFF" font-size="11" text-anchor="middle">DC / Stepper Motors</text>
    <text x="650" y="165" fill="#94A3B8" font-size="11" text-anchor="middle">H-Bridge Driver</text>
    <text x="650" y="195" fill="#00E5FF" font-size="10" text-anchor="middle">Mechanical Motion</text>

    <!-- Feedback Return Path -->
    <path d="M 650 225 L 650 260 L 150 260 L 150 225" stroke="#F59E0B" stroke-width="2" stroke-dasharray="6,4" fill="none" marker-end="url(#arrow)"/>
    <text x="400" y="255" fill="#F59E0B" font-size="11" font-weight="600" text-anchor="middle">Physical Environment Feedback (Closed Loop Loop-Back)</text>
    """
    return _svg_wrapper(content, "0 0 800 280")


# ==============================================================================
# 4. DATA ANALYSIS VISUALS
# ==============================================================================

def _data_analysis_sql_joins_svg() -> str:
    content = """
    <rect width="800" height="280" fill="transparent"/>
    <text x="400" y="35" fill="#00E5FF" font-size="16" font-weight="800" text-anchor="middle">RELATIONAL DATABASE JOINS COMPARED</text>

    <!-- INNER JOIN -->
    <g transform="translate(40, 60)">
      <rect width="210" height="180" rx="10" fill="url(#darkCard)" stroke="rgba(255,255,255,0.1)"/>
      <circle cx="80" cy="80" r="45" fill="rgba(99,102,241,0.2)" stroke="#6366F1" stroke-width="2"/>
      <circle cx="130" cy="80" r="45" fill="rgba(0,229,255,0.2)" stroke="#00E5FF" stroke-width="2"/>
      <!-- Intersection clip -->
      <path d="M 105 45 A 45 45 0 0 1 105 115 A 45 45 0 0 1 105 45" fill="#10B981" opacity="0.8"/>
      <text x="105" y="145" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">INNER JOIN</text>
      <text x="105" y="165" fill="#94A3B8" font-size="10" text-anchor="middle">Matches in BOTH tables</text>
    </g>

    <!-- LEFT JOIN -->
    <g transform="translate(295, 60)">
      <rect width="210" height="180" rx="10" fill="url(#darkCard)" stroke="rgba(255,255,255,0.1)"/>
      <circle cx="80" cy="80" r="45" fill="#10B981" opacity="0.7" stroke="#10B981" stroke-width="2"/>
      <circle cx="130" cy="80" r="45" fill="none" stroke="#00E5FF" stroke-width="2"/>
      <text x="105" y="145" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">LEFT OUTER JOIN</text>
      <text x="105" y="165" fill="#94A3B8" font-size="10" text-anchor="middle">ALL Left + Matched Right</text>
    </g>

    <!-- FULL JOIN -->
    <g transform="translate(550, 60)">
      <rect width="210" height="180" rx="10" fill="url(#darkCard)" stroke="rgba(255,255,255,0.1)"/>
      <circle cx="80" cy="80" r="45" fill="#F59E0B" opacity="0.6" stroke="#F59E0B" stroke-width="2"/>
      <circle cx="130" cy="80" r="45" fill="#F59E0B" opacity="0.6" stroke="#F59E0B" stroke-width="2"/>
      <text x="105" y="145" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">FULL OUTER JOIN</text>
      <text x="105" y="165" fill="#94A3B8" font-size="10" text-anchor="middle">ALL rows from both</text>
    </g>
    """
    return _svg_wrapper(content, "0 0 800 270")


# ==============================================================================
# 5. ELECTRICAL & ELECTRONICS ENGINEERING (EEE) VISUALS
# ==============================================================================

def _electronics_ohms_circuit_svg() -> str:
    content = """
    <rect width="800" height="280" fill="transparent"/>
    <text x="400" y="35" fill="#00E5FF" font-size="16" font-weight="800" text-anchor="middle">OHM'S LAW &amp; BASIC CLOSED CIRCUIT SCHEMATIC</text>

    <!-- Ohm's Law Triangle -->
    <g transform="translate(60, 65)">
      <polygon points="100,20 20,160 180,160" fill="url(#darkCard)" stroke="#00E5FF" stroke-width="2"/>
      <line x1="45" y1="105" x2="155" y2="105" stroke="#00E5FF" stroke-width="2"/>
      <line x1="100" y1="105" x2="100" y2="160" stroke="#00E5FF" stroke-width="2"/>
      <text x="100" y="80" fill="#F59E0B" font-size="22" font-weight="800" text-anchor="middle">V</text>
      <text x="70" y="140" fill="#00E5FF" font-size="20" font-weight="800" text-anchor="middle">I</text>
      <text x="130" y="140" fill="#10B981" font-size="20" font-weight="800" text-anchor="middle">R</text>
      <text x="100" y="185" fill="#CBD5E1" font-size="11" font-weight="600" text-anchor="middle">V = I × R  |  I = V / R</text>
    </g>

    <!-- Circuit Schematic -->
    <g transform="translate(320, 65)">
      <rect width="420" height="170" rx="10" fill="url(#darkCard)" stroke="rgba(255,255,255,0.1)"/>
      
      <!-- Battery DC Source -->
      <line x1="60" y1="50" x2="60" y2="130" stroke="#FFFFFF" stroke-width="2"/>
      <line x1="50" y1="75" x2="70" y2="75" stroke="#EF4444" stroke-width="4"/>
      <text x="45" y="72" fill="#EF4444" font-size="12" font-weight="700">+</text>
      <line x1="55" y1="105" x2="65" y2="105" stroke="#94A3B8" stroke-width="3"/>
      <text x="45" y="115" fill="#94A3B8" font-size="12" font-weight="700">-</text>
      <text x="60" y="150" fill="#CBD5E1" font-size="11" text-anchor="middle">V_supply (5V)</text>

      <!-- Loop Wire Top -->
      <line x1="60" y1="50" x2="180" y2="50" stroke="#00E5FF" stroke-width="2"/>
      
      <!-- Resistor Symbol -->
      <path d="M 180 50 L 190 40 L 200 60 L 210 40 L 220 60 L 230 40 L 240 60 L 250 50" fill="none" stroke="#F59E0B" stroke-width="3"/>
      <text x="215" y="32" fill="#F59E0B" font-size="11" font-weight="700" text-anchor="middle">Resistor R (220Ω)</text>
      <line x1="250" y1="50" x2="340" y2="50" stroke="#00E5FF" stroke-width="2"/>

      <!-- LED Symbol -->
      <line x1="340" y1="50" x2="340" y2="75" stroke="#00E5FF" stroke-width="2"/>
      <polygon points="325,75 355,75 340,105" fill="#10B981"/>
      <line x1="325" y1="105" x2="355" y2="105" stroke="#10B981" stroke-width="2"/>
      <text x="375" y="95" fill="#10B981" font-size="11" font-weight="700">LED</text>
      <line x1="340" y1="105" x2="340" y2="130" stroke="#00E5FF" stroke-width="2"/>

      <!-- Loop Wire Bottom -->
      <line x1="340" y1="130" x2="60" y2="130" stroke="#00E5FF" stroke-width="2"/>
      
      <!-- Current Arrow -->
      <path d="M 110 40 L 140 40" stroke="#00E5FF" stroke-width="2" marker-end="url(#arrow)"/>
      <text x="125" y="32" fill="#00E5FF" font-size="10" text-anchor="middle">Current I</text>
    </g>
    """
    return _svg_wrapper(content, "0 0 800 270")


# ==============================================================================
# 6. CYBERSECURITY VISUALS
# ==============================================================================

def _cybersecurity_defense_in_depth_svg() -> str:
    content = """
    <rect width="800" height="300" fill="transparent"/>
    <text x="400" y="35" fill="#00E5FF" font-size="16" font-weight="800" text-anchor="middle">DEFENSE-IN-DEPTH LAYERED SECURITY ARCHITECTURE</text>

    <!-- Concentric Layers -->
    <rect x="50" y="65" width="700" height="200" rx="14" fill="#0F172A" stroke="#EF4444" stroke-width="2" stroke-dasharray="4,2"/>
    <text x="75" y="90" fill="#EF4444" font-size="12" font-weight="700">Layer 1: Perimeter / Edge Firewall &amp; DDoS Shield</text>

    <rect x="90" y="105" width="620" height="145" rx="12" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
    <text x="115" y="130" fill="#F59E0B" font-size="12" font-weight="700">Layer 2: Network Segmentation &amp; DMZ (WAF, Reverse Proxy)</text>

    <rect x="130" y="145" width="540" height="90" rx="10" fill="#111827" stroke="#00E5FF" stroke-width="2"/>
    <text x="155" y="170" fill="#00E5FF" font-size="12" font-weight="700">Layer 3: Host / App Hardening (RBAC, CSRF, XSS Escaping)</text>

    <rect x="170" y="185" width="460" height="40" rx="8" fill="#0B0F19" stroke="#10B981" stroke-width="2"/>
    <text x="400" y="210" fill="#10B981" font-size="13" font-weight="800" text-anchor="middle">Core Asset: Encrypted Data at Rest &amp; Transit (AES-256 + TLS 1.3)</text>
    """
    return _svg_wrapper(content, "0 0 800 290")


def _cybersecurity_cia_triad_svg() -> str:
    content = """
    <rect width="800" height="280" fill="transparent"/>
    <text x="400" y="35" fill="#00E5FF" font-size="16" font-weight="800" text-anchor="middle">THE CIA TRIAD OF INFORMATION SECURITY</text>

    <!-- Confidentiality -->
    <rect x="50" y="70" width="210" height="170" rx="12" fill="url(#darkCard)" stroke="#00E5FF" stroke-width="2"/>
    <text x="155" y="110" fill="#00E5FF" font-size="15" font-weight="800" text-anchor="middle">CONFIDENTIALITY</text>
    <text x="155" y="140" fill="#FFFFFF" font-size="11" text-anchor="middle">Prevent Unauthorized</text>
    <text x="155" y="160" fill="#FFFFFF" font-size="11" text-anchor="middle">Data Disclosure</text>
    <text x="155" y="195" fill="#94A3B8" font-size="11" text-anchor="middle">AES Encryption, MFA, RBAC</text>

    <!-- Integrity -->
    <rect x="295" y="70" width="210" height="170" rx="12" fill="url(#darkCard)" stroke="#10B981" stroke-width="2"/>
    <text x="400" y="110" fill="#10B981" font-size="15" font-weight="800" text-anchor="middle">INTEGRITY</text>
    <text x="400" y="140" fill="#FFFFFF" font-size="11" text-anchor="middle">Prevent Tampering &amp;</text>
    <text x="400" y="160" fill="#FFFFFF" font-size="11" text-anchor="middle">Unauthorized Alteration</text>
    <text x="400" y="195" fill="#94A3B8" font-size="11" text-anchor="middle">SHA-256 Hashes, Signatures</text>

    <!-- Availability -->
    <rect x="540" y="70" width="210" height="170" rx="12" fill="url(#darkCard)" stroke="#F59E0B" stroke-width="2"/>
    <text x="645" y="110" fill="#F59E0B" font-size="15" font-weight="800" text-anchor="middle">AVAILABILITY</text>
    <text x="645" y="140" fill="#FFFFFF" font-size="11" text-anchor="middle">Ensure Authorized</text>
    <text x="645" y="160" fill="#FFFFFF" font-size="11" text-anchor="middle">Timely System Access</text>
    <text x="645" y="195" fill="#94A3B8" font-size="11" text-anchor="middle">Redundancy, Backups, SLA</text>
    """
    return _svg_wrapper(content, "0 0 800 270")


# ==============================================================================
# DISPATCHER & COMPARISON TABLE BUILDER
# ==============================================================================

def get_concept_visuals(domain_key: str, skill_name: str, concept_name: str) -> Dict[str, Any]:
    """Returns domain-relevant SVG diagrams, process flowcharts, and technical tables.

    Guarantees rich visual educational aids for any concept across the 6 domains.
    """
    dk = (domain_key or '').lower()
    sn = (skill_name or '').lower()
    cn = (concept_name or '').lower()

    # Default visual container
    primary_diagram = None
    diagram_title = "Technical Architectural Diagram"
    diagram_caption = "Detailed technical blueprint illustrating inputs, system logic, and observable outputs."
    comparison_table = None

    if dk in ('web_dev', 'python', 'javascript'):
        if any(w in cn or w in sn for w in ('request', 'http', 'dns', 'server', 'rest', 'api', 'browser', 'web')):
            primary_diagram = _web_dev_request_response_svg()
            diagram_title = "Client-Server Request & Response Flow"
            diagram_caption = "Traces how an HTTP/S request traverses from the browser client, through the application layer, queries the relational database, and renders."
        else:
            primary_diagram = _web_dev_mvc_mvt_svg()
            diagram_title = "Django MVT (Model-View-Template) Architecture"
            diagram_caption = "Illustrates the separation of concerns: URL Dispatcher routs to Views (business logic), interacting with Models (ORM/DB) and rendering Templates."

        comparison_table = {
            "title": "Full Stack Architecture & Protocol Comparison",
            "headers": ["Layer / Component", "Technology / Role", "Primary Responsibility", "Security / Performance Rule"],
            "rows": [
                ["Client (Frontend)", "HTML5, Modern CSS, ES6+ JS", "DOM rendering, user events, UI state", "Input validation & XSS sanitization"],
                ["Application (Backend)", "Django / Express REST API", "Authentication, routing, business logic", "CSRF tokens, parameterized queries"],
                ["Persistence (Database)", "PostgreSQL, SQLite ORM", "ACID transactions, relational joins", "Indexes on foreign keys, normalized schemas"],
                ["Delivery (DevOps)", "Docker, Reverse Proxy (Nginx)", "TLS termination, environment variables", "Zero secret hardcoding, automated tests"],
            ]
        }

    elif dk in ('ai_ml',):
        if any(w in cn or w in sn for w in ('rag', 'vector', 'search', 'llm', 'embedding')):
            primary_diagram = _ai_ml_rag_architecture_svg()
            diagram_title = "Retrieval-Augmented Generation (RAG) Architecture"
            diagram_caption = "Shows how dense vector search augments prompt context before LLM generation to prevent hallucinations and cite ground-truth sources."
        else:
            primary_diagram = _ai_ml_pipeline_svg()
            diagram_title = "Machine Learning Engineering Pipeline"
            diagram_caption = "Covers the end-to-end ML lifecycle from raw data ingestion and feature engineering to model fitting, validation, and production inference."

        comparison_table = {
            "title": "Machine Learning Paradigms & Metrics Reference",
            "headers": ["Paradigm / Metric", "Key Characteristics", "Typical Algorithms", "Evaluation Measure"],
            "rows": [
                ["Supervised Learning", "Labeled training pairs (X ➔ y)", "Linear/Logistic Reg, Random Forest", "RMSE, MAE, Accuracy, F1-Score"],
                ["Unsupervised Learning", "Unlabeled data; discovers hidden patterns", "K-Means, PCA, Hierarchical", "Silhouette Score, Inertia, Variance"],
                ["Deep Learning / NLP", "Multi-layer neural nets with embeddings", "Transformers, CNNs, Bi-LSTM", "Perplexity, BLEU, ROC-AUC"],
                ["RAG / Knowledge AI", "Retrieval over vector embeddings + LLM", "Cosine Sim, BM25, Prompt Chaining", "Retrieval Recall, Groundedness Score"],
            ]
        }

    elif dk in ('robotics',):
        primary_diagram = _robotics_sense_think_act_svg()
        diagram_title = "Robotic Sense-Think-Act Control Loop"
        diagram_caption = "Demonstrates how sensors continuously feed physical telemetry into the controller, which computes correction signals to drive actuators in real time."

        comparison_table = {
            "title": "Robotics Control & Actuation Hierarchy",
            "headers": ["Subsystem", "Hardware Components", "Operating Principle", "Key Challenge"],
            "rows": [
                ["Sensory Input", "LiDAR, Ultrasonic, IMU, Optical Encoders", "Time-of-flight, capacitance, inertia", "Sensor noise filtering (Kalman)"],
                ["Computation & Logic", "Microcontroller (ESP32/Arduino), ROS 2", "PID control loop, finite state machine", "Real-time latency constraints"],
                ["Motor Drivers", "H-Bridge (L298N/DRV8833), MOSFETs", "PWM duty-cycle voltage chopping", "Thermal dissipation & back-EMF protection"],
                ["Mechanical Actuation", "DC Geared, Stepper, Servo Motors", "Electromagnetic torque to rotation", "Gear backlash, torque-speed trade-off"],
            ]
        }

    elif dk in ('data_analytics',):
        primary_diagram = _data_analysis_sql_joins_svg()
        diagram_title = "Relational SQL Joins & Set Operations"
        diagram_caption = "Visual Venn and set diagram illustrating how records match across keys in INNER, LEFT, and FULL relational joins."

        comparison_table = {
            "title": "Data Analytics Transformation Framework",
            "headers": ["Phase", "Core Tools", "Typical Transformations", "Deliverable Outcome"],
            "rows": [
                ["1. Data Ingestion", "SQL SELECT, Pandas read_csv", "Schema detection, type coercion", "Verified raw dataframe"],
                ["2. Cleaning & Audit", "dropna(), fillna(), IQR outlier check", "Null imputation, duplicate removal", "Trustworthy clean dataset"],
                ["3. Aggregation", "GROUP BY, Pivot Tables, Window Funcs", "SUM, AVG, COUNT, Rolling 7-day", "Summary metric tables"],
                ["4. Communication", "Matplotlib, Seaborn, PowerBI", "Bar charts, cohort retention curves", "Actionable business dashboard"],
            ]
        }

    elif dk in ('electronics',):
        primary_diagram = _electronics_ohms_circuit_svg()
        diagram_title = "Ohm's Law & Circuit Analysis Schematic"
        diagram_caption = "Defines the fundamental relationship between Voltage (V), Current (I), and Resistance (R), illustrated with a practical LED closed circuit."

        comparison_table = {
            "title": "Circuit Topologies & Component Behavior",
            "headers": ["Circuit Characteristic", "Series Configuration", "Parallel Configuration", "Engineering Application"],
            "rows": [
                ["Current (I)", "Same through all components: I_total = I1 = I2", "Splits across branches: I_total = I1 + I2", "Current limiting resistors"],
                ["Voltage (V)", "Splits across components: V_total = V1 + V2", "Identical across all branches: V1 = V2", "Power rails (e.g. +5V distribution)"],
                ["Equivalent Resistance", "R_eq = R1 + R2 + ...", "1/R_eq = 1/R1 + 1/R2 + ...", "Voltage divider networks"],
                ["Component Failure", "One open breaks the entire loop", "Remaining branches continue to operate", "Home electrical wiring & multi-rail systems"],
            ]
        }

    elif dk in ('cybersecurity',):
        if any(w in cn or w in sn for w in ('cia', 'confidentiality', 'integrity', 'availability', 'triad')):
            primary_diagram = _cybersecurity_cia_triad_svg()
            diagram_title = "The CIA Triad Security Model"
            diagram_caption = "The foundational triad governing security: Confidentiality (privacy), Integrity (trustworthy accuracy), and Availability (resilience)."
        else:
            primary_diagram = _cybersecurity_defense_in_depth_svg()
            diagram_title = "Defense-in-Depth Layered Architecture"
            diagram_caption = "Multiple layered defensive rings ensuring that if one boundary is breached, subsequent controls isolate and protect critical data assets."

        comparison_table = {
            "title": "Threat Vector & Defensive Countermeasure Matrix",
            "headers": ["Threat Category", "Attack Mechanism", "Common Vulnerability", "Defensive Control"],
            "rows": [
                ["Injection (SQLi / Command)", "Unsanitized user inputs in query", "Raw SQL string concatenation", "Prepared statements & ORM parametrization"],
                ["Cross-Site Scripting (XSS)", "Malicious script injected into DOM", "Unescaped reflection of input", "Content Security Policy (CSP) & HTML escaping"],
                ["Authentication Bypass", "Credential stuffing, brute-force", "Weak password policy, no rate limit", "Argon2/bcrypt hashing, MFA, account lockout"],
                ["Data In-Transit Sniffing", "Man-in-the-Middle (MITM) eavesdrop", "Cleartext HTTP / weak TLS cipher", "HSTS headers, TLS 1.3 with forward secrecy"],
            ]
        }

    else:
        primary_diagram = _web_dev_request_response_svg()
        diagram_title = "System Architecture & Processing Flow"
        diagram_caption = "Technical diagram outlining client input, logic execution, and verified output states."

    return {
        "diagram_svg": primary_diagram,
        "diagram_title": diagram_title,
        "diagram_caption": diagram_caption,
        "comparison_table": comparison_table,
    }

