"""Three-Stage Project System for EXA AI HUB by TASBI AI SOLUTIONS.

Provides exactly three properly designed stage-based projects per learning domain:
1. Beginner: Simple mini project, suitable for zero experience, clear objectives, instructions, expected output.
2. Intermediate: Practical project, applying multiple concepts, requirements, implementation steps, expected output.
3. Advanced: Industry-style capstone project, deeper practical knowledge, requirements, implementation guidance, expected output, and evaluation criteria.

Total: 6 Domains × 3 Stages = 18 Stage Projects.
"""

from typing import Dict, Any, List, Optional


STAGE_PROJECTS: Dict[str, Dict[str, Dict[str, Any]]] = {
    # =========================================================================
    # 1. FULL STACK DEVELOPMENT
    # =========================================================================
    "web_dev": {
        "Beginner": {
            "domain": "web_dev",
            "domain_display": "Full Stack Development",
            "stage": "Beginner",
            "stage_label": "Beginner Mini Project",
            "level": 4,
            "title": "Pennywise: Responsive Financial Launch Page & Repayment Calculator",
            "company": "Pennywise",
            "industry": "Personal Finance",
            "what_you_will_build": "An accessible, responsive product launch page with an interactive loan/savings calculator built with semantic HTML5, modern CSS (Flexbox/Grid), and vanilla JavaScript.",
            "what_you_will_learn": [
                "Semantic HTML5 document hierarchy and accessible form inputs with ARIA attributes",
                "Mobile-first responsive CSS layout using Flexbox and CSS Grid breakpoints",
                "Vanilla JavaScript DOM manipulation, event listeners, and numerical input validation",
                "Clean project documentation and GitHub portfolio repository structuring"
            ],
            "objective": "A product marketing team at Pennywise needs an accessible, mobile-first launch page for a financial product with an interactive loan repayment calculator and user lead capture form.",
            "company_context": "Pennywise is a personal finance platform helping everyday earners manage debt. The product marketing team needs a verified, accessible launch page where visitors can calculate estimated loan interest and submit interest in early access.",
            "task": "Build a responsive landing page using semantic HTML5, modern CSS, and vanilla JavaScript. Include a responsive hero section, a working loan repayment calculator that calculates monthly payments upon slider/input changes, an accessible lead capture form with validation, and responsive mobile/desktop navigation.",
            "access_details": "Use synthetic product copy, royalty-free SVG icons, and local browser execution. Do not use external CSS frameworks (Bootstrap/Tailwind) so your fundamental CSS skills are fully visible.",
            "dataset_schema": "loan_calculator_rates.json — product_id (string), tier_name (string), annual_interest_rate (float e.g. 0.075), min_term_months (int: 6), max_term_months (int: 60), min_principal (int: 500), max_principal (int: 25000).",
            "requirements_list": [
                "Semantic HTML5 page structure with header, nav, main, section, and footer elements, achieving valid landmark navigation and zero broken labels.",
                "Mobile-first responsive CSS design using CSS Grid or Flexbox, supporting screen widths from 360px mobile to 1440px desktop without horizontal scroll.",
                "Working interactive loan calculator in vanilla JavaScript that calculates monthly payments dynamically: M = P * [r(1+r)^n] / [(1+r)^n - 1] with input bounds checking."
            ],
            "implementation_steps": [
                "Step 1: Scaffold semantic index.html with appropriate viewport meta tags, landmark elements, and labeled form controls.",
                "Step 2: Create styles.css with design tokens (colors, font hierarchy, spacing), flex layout for navigation, and grid layout for feature cards.",
                "Step 3: Implement calculator.js to attach input event listeners to principal and duration sliders, update DOM display elements, and format currency.",
                "Step 4: Test across mobile and desktop viewport sizes, verify keyboard tab order, and commit to GitHub with a clear README."
            ],
            "expected_output": "A live-accessible webpage with an interactive loan calculator updating instantly on input changes, an accessible contact form with validation feedback, and clean mobile-friendly layout.",
            "tools": "HTML5, CSS3, Vanilla JavaScript (ES6+), Chrome DevTools, Git/GitHub",
            "deadline": "3 to 5 days of steady pacing",
            "submission": {
                "items": [
                    "PDF report with screenshots and architecture notes (max 10 MB)",
                    "GitHub repository link named EXA_Pennywise_LandingPage",
                    "Working live demo URL or short video walkthrough"
                ],
                "live_demo_required": False,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Semantic HTML & Accessibility", "weight": 25},
                    {"name": "Responsive Design & CSS Layout", "weight": 25},
                    {"name": "JavaScript Logic & Interactivity", "weight": 25},
                    {"name": "Documentation & Code Organization", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluation is based on: semantic structure (25%), responsive layout across breakpoints (25%), calculator arithmetic accuracy and DOM interactivity (25%), and code clarity with README documentation (25%). Missing the PDF report caps score at 40.",
            "is_active": True
        },
        "Intermediate": {
            "domain": "web_dev",
            "domain_display": "Full Stack Development",
            "stage": "Intermediate",
            "stage_label": "Intermediate Practical Project",
            "level": 8,
            "title": "NeighborWorks: Property Service Request Full-Stack CRUD Application",
            "company": "NeighborWorks",
            "industry": "Property Management",
            "what_you_will_build": "A complete full-stack web application built in Python and Django featuring relational database models, server-side forms with CSRF protection, RESTful JSON API endpoints, and complete CRUD operations.",
            "what_you_will_learn": [
                "Django MVT (Model-View-Template) architectural pattern and URL routing",
                "Relational data modeling with Django ORM, foreign keys, and migrations",
                "Form validation, security protections (CSRF, XSS prevention), and error handling",
                "RESTful JSON API endpoints supporting Create, Read, Update, and Delete operations"
            ],
            "objective": "NeighborWorks needs an internal property management portal where property managers and tenants can create, track, filter, update, and resolve maintenance service requests.",
            "company_context": "NeighborWorks manages residential complexes. Service requests are currently submitted via unorganized emails. The operations director needs a robust, authenticated internal web portal with searchable ticket statuses and automated priority triage.",
            "task": "Develop a full-stack Django application with relational models for Property, Tenant, and ServiceRequest. Implement views and templates for listing, creating, editing, and deleting requests with status filtering (Pending, In Progress, Resolved). Provide JSON API endpoints for AJAX queries.",
            "access_details": "Starter synthetic tenant and property fixtures are supplied. Use SQLite or PostgreSQL for local development. Follow Django security best practices.",
            "dataset_schema": "properties (id, name, address, units_count); service_requests (id, property_id, title, category, priority: Low/Med/High/Urgent, description, status: Pending/InProgress/Resolved, created_at, resolved_at).",
            "requirements_list": [
                "Relational Django models with foreign keys, data constraints, and migrations for Properties and ServiceRequests.",
                "Complete server-side CRUD workflows with Django ModelForms, CSRF tokens, and user feedback messages.",
                "RESTful JSON API endpoints (GET /api/requests/, POST /api/requests/) returning structured responses and status codes.",
                "Search and filter interface by status and priority with clear empty states and defensive error handling."
            ],
            "implementation_steps": [
                "Step 1: Set up Django app and define models for Property and ServiceRequest with foreign key relationships and status choices.",
                "Step 2: Generate and apply migrations; seed with initial test fixture data.",
                "Step 3: Build views and templates for ticket listing with status badges, detail view, creation form, and update modal.",
                "Step 4: Implement JSON REST endpoints with appropriate HTTP status codes (200, 201, 400, 404).",
                "Step 5: Write unit tests verifying model validation, form errors, and view response codes."
            ],
            "expected_output": "A fully functional full-stack web portal allowing creation, editing, status updating, and filtering of service tickets, backed by relational database persistence.",
            "tools": "Python 3, Django 6+, SQLite/PostgreSQL, HTML5/CSS3, Git",
            "deadline": "1 to 2 weeks of steady progress",
            "submission": {
                "items": [
                    "Comprehensive PDF architecture report with schema diagram (max 10 MB)",
                    "GitHub repository named EXA_NeighborWorks_CRUD",
                    "Working live deployment link or local video walkthrough"
                ],
                "live_demo_required": True,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Data Model & ORM Architecture", "weight": 25},
                    {"name": "CRUD Workflows & View Logic", "weight": 25},
                    {"name": "Security & Form Validation", "weight": 25},
                    {"name": "REST API & Documentation", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on relational schema design (25%), CRUD and filter completeness (25%), CSRF/form security and validation (25%), and REST API quality with tests (25%). Score capped at 40 if report or live link is missing.",
            "is_active": True
        },
        "Advanced": {
            "domain": "web_dev",
            "domain_display": "Full Stack Development",
            "stage": "Advanced",
            "stage_label": "Advanced Industry Project",
            "level": 12,
            "title": "RiverCity Transit: Enterprise Full-Stack Transit Platform Deployed Live",
            "company": "RiverCity Transit",
            "industry": "Public Transportation",
            "what_you_will_build": "An enterprise-grade, containerized full-stack operations platform with role-based authentication, real-time schedule tracking, automated test coverage, and live cloud deployment on Render/Railway.",
            "what_you_will_learn": [
                "Role-based authentication & session security (Admin, Dispatcher, Rider) with password hashing",
                "Advanced relational database schema design with optimized indexes, transactions, and join queries",
                "Docker containerization, environment configuration (.env), and production WSGI/Gunicorn setup",
                "Continuous integration, automated test suites (>80% coverage), and cloud deployment observability"
            ],
            "objective": "RiverCity Transit needs a production-ready transit management platform that coordinates bus routes, live driver status updates, incident reporting, and public arrival tracking.",
            "company_context": "RiverCity Transit operates 45 municipal routes across 3 counties. Stakeholders require an enterprise web portal that provides dispatchers with live status triage, drivers with run sheets, and passengers with timely arrival estimates.",
            "task": "Design, architect, containerize, and deploy a production-ready web platform. Implement role-based access control, relational database schema with PostgreSQL, transaction-safe booking/dispatching, Dockerfile setup, passing test suite, and cloud hosting with HTTPS.",
            "access_details": "Synthetic GTFS route data and vehicle schedules provided. Configure external environment variables for secret keys and database URLs. Never commit secrets to Git.",
            "dataset_schema": "routes (id, route_number, name, origin, destination, is_active); vehicles (id, route_id, vehicle_code, capacity, status); schedule_trips (id, route_id, departure_time, arrival_time); service_alerts (id, route_id, severity, message, active).",
            "requirements_list": [
                "Role-based authentication (RBAC) with secure session handling, CSRF protection, and permission guards for dispatchers vs public riders.",
                "Optimized relational data layer with foreign keys, composite indexes on route and trip times, and transaction atomicity.",
                "Comprehensive automated test suite covering authentication, API endpoints, and critical business rules with passing tests.",
                "Production containerization via Docker and live cloud deployment (Render/Railway/Fly.io) with valid public URL and HTTPS.",
                "Observability and error monitoring, including graceful 404/500 error pages and structured logging."
            ],
            "implementation_steps": [
                "Step 1: System architecture diagram and relational ERD design modeling routes, stops, trips, and alerts.",
                "Step 2: Implement core Django backend with custom user roles, model managers, and query optimization using select_related/prefetch_related.",
                "Step 3: Build interactive responsive frontend with route filtering, schedule board, and incident announcement ticker.",
                "Step 4: Author automated test suite (unit and integration tests) verifying permissions, edge cases, and API responses.",
                "Step 5: Write Dockerfile and docker-compose.yml; configure environment variables and deploy live to cloud provider with HTTPS."
            ],
            "expected_output": "A live-deployed enterprise transit platform with authenticated role management, real-time schedule board, passing automated tests, Docker containerization, and public URL.",
            "tools": "Python 3, Django, PostgreSQL, Docker, Gunicorn, WhiteNoise, Render/Railway, GitHub Actions",
            "deadline": "2 to 3 weeks of thorough engineering",
            "submission": {
                "items": [
                    "Production Architecture & Engineering Dossier in PDF format (max 10 MB)",
                    "GitHub repository with Dockerfile and test suite",
                    "Public live deployment URL with HTTPS",
                    "Optional 3-minute video walkthrough"
                ],
                "live_demo_required": True,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "System Architecture & Security", "weight": 25},
                    {"name": "Data Layer Optimization & Testing", "weight": 25},
                    {"name": "Production Deployment & Docker", "weight": 25},
                    {"name": "UI/UX & Documentation Quality", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on enterprise architecture & RBAC security (25%), database indexing and automated test coverage (25%), verified live deployment with Docker (25%), and UI polish and documentation (25%). Missing live link caps score at 40.",
            "is_active": True
        }
    },

    # =========================================================================
    # 2. AI & MACHINE LEARNING
    # =========================================================================
    "ai_ml": {
        "Beginner": {
            "domain": "ai_ml",
            "domain_display": "AI & Machine Learning",
            "stage": "Beginner",
            "stage_label": "Beginner Mini Project",
            "level": 4,
            "title": "NimbleSub: Subscription Churn Classifier & Exploratory Analysis",
            "company": "NimbleSub",
            "industry": "Subscription Media",
            "what_you_will_build": "An end-to-end exploratory data analysis (EDA) and baseline machine learning pipeline in Python using Pandas and Scikit-Learn that predicts subscriber churn probability.",
            "what_you_will_learn": [
                "Data cleaning, missing value handling, and outlier inspection using Pandas",
                "Feature correlation analysis and visual distribution inspection",
                "Train/test splitting without data leakage and feature scaling with StandardScaler",
                "Fitting a binary classification model (Logistic Regression) and interpreting precision/recall"
            ],
            "objective": "A subscription media platform needs a baseline classifier to identify customers at risk of cancelling their membership based on usage and billing history.",
            "company_context": "NimbleSub streams educational videos. Marketing wants to trigger retention discounts before users cancel, but currently has no predictive signal beyond manual complaints.",
            "task": "Load the supplied subscription dataset, conduct exploratory analysis, clean nulls, engineer feature ratios, train a Scikit-Learn classification model, and evaluate performance using confusion matrix, accuracy, precision, and recall.",
            "access_details": "Synthetic customer usage CSV provided. Run locally in Jupyter Notebook or Python script.",
            "dataset_schema": "subscribers.csv — customer_id (int), tenure_months (int), monthly_fee (float), video_hours_watched (float), support_tickets (int), payment_delay_days (int), churned (0 or 1).",
            "requirements_list": [
                "Complete data cleaning notebook handling null values, inspecting distributions, and plotting correlation heatmaps.",
                "Correct train/test partition (80/20) with feature scaling applied strictly to the training split.",
                "Trained classification model reporting confusion matrix, accuracy (>75%), precision, recall, and top 3 feature importances."
            ],
            "implementation_steps": [
                "Step 1: Ingest dataset with Pandas; inspect summary statistics (.describe()) and missing values.",
                "Step 2: Impute missing numerical features with median and visualize correlations with churn target.",
                "Step 3: Split features (X) and label (y) into train and test sets using train_test_split(random_state=42).",
                "Step 4: Train LogisticRegression and evaluate classification_report and confusion_matrix on test data.",
                "Step 5: Document findings and business recommendations in a structured PDF report."
            ],
            "expected_output": "A reproducible Python notebook and summary report with churn risk scores, confusion matrix visualization, and actionable retention recommendations.",
            "tools": "Python, Pandas, NumPy, Scikit-Learn, Matplotlib, Jupyter",
            "deadline": "3 to 5 days",
            "submission": {
                "items": [
                    "PDF analysis report with charts and confusion matrix (max 10 MB)",
                    "GitHub repository with notebook and clean code",
                    "Model predictions summary table"
                ],
                "live_demo_required": False,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Data Cleaning & EDA Quality", "weight": 25},
                    {"name": "ML Pipeline & Preprocessing", "weight": 25},
                    {"name": "Model Evaluation & Metrics", "weight": 25},
                    {"name": "Business Insights & Interpretation", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on data preprocessing rigor (25%), clean train/test pipeline without leakage (25%), correct metric interpretation (25%), and clarity of business recommendations (25%).",
            "is_active": True
        },
        "Intermediate": {
            "domain": "ai_ml",
            "domain_display": "AI & Machine Learning",
            "stage": "Intermediate",
            "stage_label": "Intermediate Practical Project",
            "level": 8,
            "title": "LexiArchive: Semantic Document Search & Multi-Model NLP Pipeline",
            "company": "LexiArchive",
            "industry": "Legal Tech & Knowledge Management",
            "what_you_will_build": "A semantic document retrieval engine that generates dense text embeddings, indexes document chunks in a vector index, and compares cosine similarity search against traditional BM25 keyword search.",
            "what_you_will_learn": [
                "Text preprocessing, tokenization, and semantic chunking strategies",
                "Generating dense sentence embeddings using Hugging Face Sentence-Transformers",
                "Building vector similarity search (cosine similarity, FAISS or ChromaDB)",
                "Comparative retrieval evaluation (Mean Reciprocal Rank, Recall@K) against keyword baselines"
            ],
            "objective": "A legal research organization needs to search thousands of internal policy documents by semantic intent rather than relying solely on exact keyword matching.",
            "company_context": "LexiArchive maintains legal precedents and policy briefs. Lawyers frequently search by concepts (e.g. 'workplace health liabilities') that miss documents phrased as 'occupational hazard compliance'.",
            "task": "Build an NLP pipeline that ingests a corpus of policy documents, chunks them into semantic paragraphs, generates dense embeddings, builds a vector index, executes semantic query matching, and exposes a clean Python query interface.",
            "access_details": "Synthetic legal and regulatory policy corpus (JSONL) provided. Use open-source sentence-transformers (all-MiniLM-L6-v2) for local embedding generation.",
            "dataset_schema": "legal_docs.jsonl — doc_id (str), title (str), jurisdiction (str), full_text (str), section (str), published_year (int).",
            "requirements_list": [
                "Document chunking pipeline with overlap (e.g. 500 characters with 50 char overlap) and metadata preservation.",
                "Vector embedding generation using a pre-trained transformer model with normalized vectors.",
                "Working similarity search engine returning top-K most relevant chunks with cosine similarity scores.",
                "Comparative benchmark comparing semantic retrieval results against keyword search for 10 test queries."
            ],
            "implementation_steps": [
                "Step 1: Load and clean raw documents; implement recursive character or sentence chunking.",
                "Step 2: Generate vector embeddings using sentence-transformers and build a local vector index.",
                "Step 3: Implement query encoding and cosine similarity search returning ranked results with metadata.",
                "Step 4: Create a side-by-side comparison table showing semantic vs keyword search results for sample queries.",
                "Step 5: Package as a modular Python package with clean docstrings and CLI/web demonstration."
            ],
            "expected_output": "A working semantic search pipeline capable of returning contextually relevant document sections for complex natural language queries.",
            "tools": "Python, Hugging Face Sentence-Transformers, ChromaDB / FAISS, NumPy, Scikit-Learn",
            "deadline": "1 to 2 weeks",
            "submission": {
                "items": [
                    "PDF technical evaluation report with retrieval metrics (max 10 MB)",
                    "GitHub repository with pipeline code and documentation",
                    "Query evaluation results log comparing semantic vs keyword retrieval"
                ],
                "live_demo_required": True,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Chunking & Text Preprocessing", "weight": 25},
                    {"name": "Embedding & Vector Search Implementation", "weight": 25},
                    {"name": "Benchmark Evaluation & Retrieval Metrics", "weight": 25},
                    {"name": "Code Architecture & API Interface", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on text chunking design (25%), vector embedding index implementation (25%), benchmark evaluation comparing against keyword search (25%), and code quality with reproducible tests (25%).",
            "is_active": True
        },
        "Advanced": {
            "domain": "ai_ml",
            "domain_display": "AI & Machine Learning",
            "stage": "Advanced",
            "stage_label": "Advanced Industry Project",
            "level": 12,
            "title": "FieldGuide: Production RAG AI Assistant with Citations & Evaluation Pipeline",
            "company": "FieldGuide",
            "industry": "AgTech & Climate Science",
            "what_you_will_build": "An end-to-end, production-ready Retrieval-Augmented Generation (RAG) assistant with hybrid search, hallucination guardrails, source attribution with clickable citations, and automated evaluation metrics deployed live.",
            "what_you_will_learn": [
                "Production RAG architecture design: hybrid retrieval (dense embeddings + sparse BM25) and re-ranking",
                "Prompt engineering with system guardrails and context window optimization",
                "Automated RAG evaluation using Ragas framework (Faithfulness, Answer Relevance, Context Precision)",
                "Deploying a secure AI API with streaming responses, source citation tracking, and latency profiling"
            ],
            "objective": "An agricultural technology company needs a grounded AI assistant that answers agronomy questions strictly from verified crop manuals, providing verifiable citations while rejecting unsupported queries.",
            "company_context": "FieldGuide supports commercial farm managers with agronomy advice. Generating hallucinated chemical dosages can destroy crops. The system must cite exact manual sections and explicitly decline when information is absent.",
            "task": "Architect, evaluate, and deploy a production RAG application. Implement hybrid retrieval, prompt orchestration with source grounding, hallucination guardrails, an automated evaluation pipeline measuring faithfulness, and a web API interface.",
            "access_details": "Synthetic agronomy manuals and crop protection guides (PDF/Markdown) provided. Use open APIs or local LLM (Ollama/Groq) for generation.",
            "dataset_schema": "manuals/ — guide_id (str), crop (str), topic (pest_control/irrigation/soil), text (str), table_data (str), version (str).",
            "requirements_list": [
                "Hybrid retrieval pipeline combining vector search with keyword filtering and cross-encoder re-ranking.",
                "Grounded prompt template enforcing zero hallucination with explicit inline source citations [Doc X, Sec Y].",
                "Automated evaluation suite testing 20 representative queries and reporting Faithfulness and Context Recall scores.",
                "Production web API (FastAPI or Django) returning streaming responses with structured citation metadata.",
                "Live cloud deployment or containerized demo with reproducible test suite and architecture dossier."
            ],
            "implementation_steps": [
                "Step 1: Ingest agronomy manuals; implement markdown header-aware semantic chunking.",
                "Step 2: Build hybrid retriever and cross-encoder re-ranker to surface top-3 highly relevant passages.",
                "Step 3: Construct system prompt enforcing strict grounding, rejection of unsupported questions, and citation formatting.",
                "Step 4: Author evaluation script using Ragas or custom rubric testing precision, recall, and hallucination rate.",
                "Step 5: Wrap in FastAPI/Django, containerize with Docker, and deploy live with interactive chat UI."
            ],
            "expected_output": "A live, deployed RAG AI assistant that provides grounded, accurate answers backed by verifiable source citations, with automated evaluation scores proving safety.",
            "tools": "Python, LangChain/LlamaIndex, FastAPI/Django, ChromaDB/Pinecone, Docker, Ragas, Cloud Hosting",
            "deadline": "2 to 3 weeks",
            "submission": {
                "items": [
                    "Production Architecture & RAG Evaluation Dossier (max 10 MB)",
                    "GitHub repository with Dockerfile and evaluation scripts",
                    "Working live demo URL or API endpoint",
                    "Automated evaluation benchmark results (Faithfulness & Relevance)"
                ],
                "live_demo_required": True,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Hybrid Retrieval & Reranking Pipeline", "weight": 25},
                    {"name": "Grounding & Hallucination Guardrails", "weight": 25},
                    {"name": "Automated Evaluation & Benchmarks", "weight": 25},
                    {"name": "API Deployment & Engineering Polish", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on hybrid retrieval precision (25%), hallucination defense and citation fidelity (25%), automated benchmark metrics (25%), and live deployment engineering (25%). Missing live link caps score at 40.",
            "is_active": True
        }
    },

    # =========================================================================
    # 3. ROBOTICS
    # =========================================================================
    "robotics": {
        "Beginner": {
            "domain": "robotics",
            "domain_display": "Robotics & Embedded Systems",
            "stage": "Beginner",
            "stage_label": "Beginner Mini Project",
            "level": 4,
            "title": "CrateMover: Closed-Loop DC Motor PWM Speed Controller & Tachometer",
            "company": "CrateMover",
            "industry": "Warehouse Fulfilment",
            "what_you_will_build": "An embedded microcontroller motor control and telemetry system that modulates PWM duty cycle via an H-Bridge driver in response to setpoint inputs and logs optical encoder speed readings.",
            "what_you_will_learn": [
                "Microcontroller GPIO configuration, timer interrupts, and analog-to-digital conversion",
                "Pulse-Width Modulation (PWM) duty cycle calculation and H-Bridge motor direction control",
                "Reading optical rotary encoder pulses to calculate real-time motor RPM",
                "Serial telemetry logging and benchtop debugging techniques"
            ],
            "objective": "A warehouse automation team needs a benchtop motor speed controller that maintains reliable conveyor belt speeds across changing crate weights.",
            "company_context": "CrateMover builds automated sorting conveyors. Motor speeds currently fluctuate when heavy packages enter the belt, causing sorting jams. The team needs an encoder-verified controller.",
            "task": "Program an Arduino or simulated microcontroller circuit to control a DC motor via an H-Bridge (L298N/DRV8833). Read a potentiometer to set target RPM, use timer interrupts to count encoder pulses, calculate actual RPM, and stream real-time telemetry to the serial monitor.",
            "access_details": "Use Wokwi/Tinkercad simulator or physical Arduino/ESP32 hardware. Starter schematic and pinout diagrams provided.",
            "dataset_schema": "telemetry.csv — timestamp_ms (int), target_rpm (int), actual_rpm (int), pwm_duty_cycle (int 0-255), current_draw_ma (float).",
            "requirements_list": [
                "Correct hardware schematic and wiring diagram connecting microcontroller, H-Bridge, DC motor, and encoder.",
                "Non-blocking microcontroller firmware utilizing timer interrupts to calculate motor RPM accurately.",
                "PWM duty cycle control mapping potentiometer inputs (0-1023) smoothly to PWM outputs (0-255) with direction switching."
            ],
            "implementation_steps": [
                "Step 1: Draw circuit schematic including microcontroller, H-Bridge, motor, flyback diode, and encoder connections.",
                "Step 2: Configure digital input with interrupt (attachInterrupt) on encoder channel A to count state transitions.",
                "Step 3: Implement periodic 100ms timer loop to calculate RPM = (pulse_count / pulses_per_rev) * (60000 / dt).",
                "Step 4: Map potentiometer reading to PWM duty cycle and output via analogWrite to motor driver.",
                "Step 5: Log telemetry to serial plotter demonstrating speed response to step changes."
            ],
            "expected_output": "A verified embedded motor control system demonstrating responsive PWM speed adjustment with real-time encoder tachometer telemetry.",
            "tools": "C/C++, Arduino IDE / Wokwi Simulator, L298N/DRV8833, Optical Encoder, Serial Plotter",
            "deadline": "3 to 5 days",
            "submission": {
                "items": [
                    "PDF benchtop report with circuit schematic and RPM response graphs (max 10 MB)",
                    "GitHub repository with microcontroller firmware (.ino/.cpp)",
                    "Wokwi simulation link or short video demo"
                ],
                "live_demo_required": False,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Circuit Schematic & Wiring Rigor", "weight": 25},
                    {"name": "Firmware Design & Interrupt Handling", "weight": 25},
                    {"name": "PWM & Speed Control Accuracy", "weight": 25},
                    {"name": "Telemetry Documentation & Plotting", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on circuit wiring accuracy (25%), non-blocking interrupt firmware (25%), PWM control response (25%), and clear telemetry plotting in the PDF report (25%).",
            "is_active": True
        },
        "Intermediate": {
            "domain": "robotics",
            "domain_display": "Robotics & Embedded Systems",
            "stage": "Intermediate",
            "stage_label": "Intermediate Practical Project",
            "level": 8,
            "title": "Alpine Rescue: Two-Wheeled Self-Balancing Robot with PID Control",
            "company": "Alpine Rescue",
            "industry": "Emergency Response & Search Robotics",
            "what_you_will_build": "A dynamic two-wheeled self-balancing inverted pendulum robot using IMU sensor fusion (accelerometer + gyroscope), a complementary filter for tilt angle estimation, and a tuned PID control loop.",
            "what_you_will_learn": [
                "I2C communication with 6-DOF IMU sensors (MPU6050)",
                "Sensor fusion: combining accelerometer gravity vectors with gyroscope angular velocity via complementary filter",
                "PID control algorithm design: proportional, integral, and derivative gain tuning (Kp, Ki, Kd)",
                "Real-time loop timing and anti-windup protection under dynamic external disturbances"
            ],
            "objective": "A search-and-rescue robotics lab needs a compact, self-balancing two-wheeled robot chassis that maintains upright balance while navigating uneven floor debris.",
            "company_context": "Alpine Rescue develops agile robotic scouts for confined spaces. A two-wheeled inverted pendulum design allows turning in place, but requires microsecond-accurate balance stabilization.",
            "task": "Develop the embedded control firmware for a self-balancing robot. Ingest raw IMU accelerometer and gyroscope readings over I2C, compute clean pitch angle, calculate PID correction outputs, and drive dual motors in real time at a 100Hz loop rate.",
            "access_details": "Use Webots/Gazebo simulation or physical balance robot chassis with MPU6050 and twin geared DC motors.",
            "dataset_schema": "imu_balance_log.csv — timestamp_us (int), raw_pitch_accel (float), raw_gyro_rate (float), fused_angle (float), pid_p (float), pid_i (float), pid_d (float), motor_output (int -255 to 255).",
            "requirements_list": [
                "IMU sensor fusion routine implementing a complementary filter (angle = 0.98 * (angle + gyro*dt) + 0.02 * accel_angle).",
                "Full PID controller implementation with proportional, integral with anti-windup, and derivative terms.",
                "Stable balance demonstration recovering from mild external pushes within +/- 15 degrees of vertical.",
                "Tuning documentation justifying selected Kp, Ki, and Kd values with step-response oscillation plots."
            ],
            "implementation_steps": [
                "Step 1: Interface MPU6050 via I2C, calibrate sensor offsets at rest, and verify angular rate readings.",
                "Step 2: Implement complementary filter to cancel gyroscope drift while filtering high-frequency accelerometer noise.",
                "Step 3: Author PID algorithm: compute error = setpoint - fused_angle; calculate P, I, D terms with motor saturation limits.",
                "Step 4: Tune Kp first until sustained oscillation occurs, then introduce Kd for damping, and Ki for zero steady-state error.",
                "Step 5: Log disturbance recovery and document tuning parameters in a comprehensive engineering report."
            ],
            "expected_output": "A self-balancing robot firmware maintaining stable upright posture, dampening oscillations, and recovering from impulse disturbances.",
            "tools": "C/C++, Arduino/ESP32, MPU6050 IMU, Webots / Gazebo / Physical Rig, PID Tuning Toolkit",
            "deadline": "1 to 2 weeks",
            "submission": {
                "items": [
                    "PDF engineering dossier with PID tuning curves and filter equations (max 10 MB)",
                    "GitHub repository with clean firmware and simulation files",
                    "Video recording or simulation recording demonstrating stable balance"
                ],
                "live_demo_required": True,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "IMU Calibration & Sensor Fusion", "weight": 25},
                    {"name": "PID Algorithm & Anti-Windup Design", "weight": 25},
                    {"name": "Dynamic Balance & Disturbance Recovery", "weight": 25},
                    {"name": "Engineering Dossier & Tuning Rigor", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on sensor fusion math (25%), PID implementation and anti-windup (25%), physical balance stability under disturbance (25%), and documentation of the tuning methodology (25%).",
            "is_active": True
        },
        "Advanced": {
            "domain": "robotics",
            "domain_display": "Robotics & Embedded Systems",
            "stage": "Advanced",
            "stage_label": "Advanced Industry Project",
            "level": 12,
            "title": "Lighthouse Foods: Autonomous Mobile Robot with ROS 2 & LiDAR Navigation",
            "company": "Lighthouse Foods",
            "industry": "Industrial Food Logistics",
            "what_you_will_build": "A complete ROS 2 Autonomous Mobile Robot (AMR) software stack in simulation featuring 2D LiDAR SLAM mapping, Nav2 costmaps, global/local path planning, dynamic obstacle avoidance, and mission dispatching.",
            "what_you_will_learn": [
                "ROS 2 (Humble/Iron) architecture: nodes, topics, publishers, subscribers, action servers, and TF2 transforms",
                "2D Simultaneous Localization and Mapping (SLAM) with Cartographer/slam_toolbox",
                "Nav2 navigation stack configuration: global planners (NavFn/A*), local controllers (DWB/TEB), and costmaps",
                "Autonomous mission dispatching, dynamic obstacle avoidance, and recovery behavior trees"
            ],
            "objective": "A food processing warehouse needs an autonomous mobile robot (AMR) to transport ingredients between cold storage and processing bays while dodging workers and mobile equipment.",
            "company_context": "Lighthouse Foods operates a 50,000 sq ft processing plant. Forklift accidents prompted a mandate to transition internal material transport to automated guided mobile robots with certified safety navigation.",
            "task": "Develop and document a ROS 2 autonomous navigation package for a differential-drive robot in Gazebo simulation. Generate an accurate 2D floorplan using SLAM, configure the Nav2 stack, implement autonomous waypoint navigation, and demonstrate dynamic obstacle avoidance.",
            "access_details": "Gazebo warehouse world model and URDF/Xacro differential robot description supplied. Run in Ubuntu / ROS 2 Humble or Docker container.",
            "dataset_schema": "ros2_topics: /scan (sensor_msgs/LaserScan), /odom (nav_msgs/Odometry), /cmd_vel (geometry_msgs/Twist), /map (nav_msgs/OccupancyGrid), /tf (tf2_msgs/TFMessage).",
            "requirements_list": [
                "URDF/Xacro robot model with proper kinematics, collision geometries, inertial tags, and LiDAR sensor plugin.",
                "Generated 2D occupancy grid map of the warehouse environment using slam_toolbox or Cartographer.",
                "Nav2 navigation stack configuration with tuned global (A*) and local (DWB) trajectory planners.",
                "Autonomous multi-waypoint navigation demo successfully avoiding unexpected obstacles placed in its path.",
                "Comprehensive architecture dossier detailing TF tree, node communication graph, and safety recovery behaviors."
            ],
            "implementation_steps": [
                "Step 1: Set up ROS 2 workspace, verify URDF model in RViz2, and check TF transforms (odom ➔ base_link ➔ laser_frame).",
                "Step 2: Launch Gazebo warehouse simulation; teleoperate robot while running slam_toolbox to generate warehouse.yaml map.",
                "Step 3: Configure Nav2 parameter file (nav2_params.yaml) tuning inflation layers, footprint, and max velocity limits.",
                "Step 4: Test 2D Nav Goal in RViz; author Python mission script using BasicNavigator API to navigate between 4 waypoints.",
                "Step 5: Introduce dynamic obstacle along planned path; verify local planner avoids obstacle without collisions.",
                "Step 6: Document complete system architecture, ROS graph, and performance logs in final engineering dossier."
            ],
            "expected_output": "A fully functional ROS 2 AMR navigation stack driving an autonomous robot between designated warehouse waypoints with dynamic obstacle avoidance in Gazebo.",
            "tools": "ROS 2 (Humble), Gazebo, RViz2, Nav2, slam_toolbox, Python, C++, Docker",
            "deadline": "2 to 3 weeks",
            "submission": {
                "items": [
                    "Complete ROS 2 AMR Architecture Dossier with TF tree and maps (max 10 MB)",
                    "GitHub repository with ROS 2 launch files, configurations, and nodes",
                    "Video recording showing SLAM mapping and autonomous waypoint navigation with obstacle avoidance",
                    "Nav2 configuration file and generated occupancy map (.yaml + .pgm)"
                ],
                "live_demo_required": True,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "ROS 2 Architecture & TF Kinematics", "weight": 25},
                    {"name": "SLAM Mapping & Occupancy Grid Quality", "weight": 25},
                    {"name": "Nav2 Path Planning & Obstacle Avoidance", "weight": 25},
                    {"name": "Engineering Dossier & Mission Autonomy", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on clean ROS 2 TF transform hierarchy (25%), SLAM map resolution (25%), smooth path planning and collision-free obstacle avoidance (25%), and documentation completeness (25%). Missing video demo caps score at 40.",
            "is_active": True
        }
    },

    # =========================================================================
    # 4. DATA ANALYSIS
    # =========================================================================
    "data_analytics": {
        "Beginner": {
            "domain": "data_analytics",
            "domain_display": "Data Analysis",
            "stage": "Beginner",
            "stage_label": "Beginner Mini Project",
            "level": 4,
            "title": "SkyParcel: Logistics Delivery Performance & Telecom Churn Audit",
            "company": "SkyParcel",
            "industry": "Logistics & Supply Chain",
            "what_you_will_build": "A comprehensive data cleaning, exploratory analysis, and executive summary workbook in Excel / Python that audits delivery delays and customer churn patterns across regional hubs.",
            "what_you_will_learn": [
                "Detecting and remediating data quality flaws: missing entries, duplicated keys, inconsistent date formatting",
                "Summarizing multi-variable datasets with Pivot Tables, XLOOKUP, and aggregate metrics",
                "Formulating business hypotheses and validating them with statistical summaries",
                "Designing clean visual charts (histograms, bar comparisons) with professional executive annotations"
            ],
            "objective": "A national parcel logistics company needs an operational data audit to pinpoint which distribution hubs are driving delivery SLA breaches and subscriber cancellations.",
            "company_context": "SkyParcel handles 100,000 packages daily. Customer satisfaction dropped by 18% last quarter. The COO needs an unambiguous audit tracing package delays to carrier routes and hub congestion.",
            "task": "Clean a provided raw logistics and delivery dataset, calculate on-time delivery percentages by hub, analyze customer churn by delivery delay tier, build pivot table summaries, and write an executive briefing memo.",
            "access_details": "Synthetic raw logistics workbook (.csv/.xlsx) supplied with intentional dirty data (dates, nulls, casing).",
            "dataset_schema": "shipments.csv — tracking_id (str), ship_date (date), delivery_date (date), hub_origin (str), carrier (str), status (Delivered/Delayed/Lost), package_weight_kg (float), customer_churned (bool).",
            "requirements_list": [
                "Documented data cleaning log correcting invalid dates, missing hubs, and duplicate tracking IDs.",
                "Pivot table summaries calculating on-time delivery rates, average delay hours by hub, and churn correlation.",
                "Executive summary memo with 3 clear data-backed recommendations to resolve logistics bottlenecks."
            ],
            "implementation_steps": [
                "Step 1: Open raw dataset; identify missing values, corrupted dates, and duplicate records.",
                "Step 2: Clean data using Excel formulas (TRIM, IF, DATEDIF, XLOOKUP) or Python Pandas (dropna, fillna).",
                "Step 3: Create pivot tables aggregating delivery status by regional hub and carrier.",
                "Step 4: Compute correlation between delivery delays (>48 hours) and customer cancellation rates.",
                "Step 5: Format findings into an executive report with clean charts and actionable recommendations."
            ],
            "expected_output": "A cleaned master dataset workbook and executive report pinpointing the exact hubs responsible for delivery bottlenecks and customer churn.",
            "tools": "Microsoft Excel / Google Sheets, Python (Pandas/Matplotlib optional), PowerPoint/Word",
            "deadline": "3 to 5 days",
            "submission": {
                "items": [
                    "PDF executive report with data charts and recommendations (max 10 MB)",
                    "Cleaned data workbook (.xlsx or .csv) with formulas intact",
                    "Data cleaning methodology log"
                ],
                "live_demo_required": False,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Data Cleaning & Quality Audit", "weight": 25},
                    {"name": "Aggregation & Formula Correctness", "weight": 25},
                    {"name": "Visualization Polish & Chart Selection", "weight": 25},
                    {"name": "Business Insight & Recommendations", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on data cleaning thoroughness (25%), correct formula and pivot summaries (25%), chart readability and formatting (25%), and practical business utility of insights (25%).",
            "is_active": True
        },
        "Intermediate": {
            "domain": "data_analytics",
            "domain_display": "Data Analysis",
            "stage": "Intermediate",
            "stage_label": "Intermediate Practical Project",
            "level": 8,
            "title": "Aster Hotels: SQL Multi-Table Revenue & Customer Cohort Analysis",
            "company": "Aster Hotels",
            "industry": "Hospitality & Tourism",
            "what_you_will_build": "An advanced SQL analytical query pack over a normalized relational hotel database that computes RevPAR, customer lifetime value, multi-table booking trends, and monthly cohort retention rates.",
            "what_you_will_learn": [
                "Complex relational SQL queries: multi-table INNER and LEFT JOINs, subqueries, and Common Table Expressions (CTEs)",
                "Advanced window functions: ROW_NUMBER(), RANK(), LAG(), LEAD(), and rolling 30-day moving averages",
                "Cohort analysis: grouping customers by acquisition month and tracking repeat booking retention matrices",
                "Authoring clean, production-grade SQL with comments, CTE naming conventions, and query execution planning"
            ],
            "objective": "A boutique hotel chain needs a comprehensive SQL analytical suite to assess booking channel profitability, repeat guest retention cohorts, and cancellation trends across properties.",
            "company_context": "Aster Hotels operates 12 boutique locations. Heavy reliance on online travel agencies (OTAs) incurs high commissions. Leadership wants to analyze direct booking customer cohorts and retention.",
            "task": "Write modular SQL queries analyzing a normalized schema of guests, bookings, rooms, and payments. Compute Revenue per Available Room (RevPAR), 30-day rolling revenue trends using window functions, and construct a customer cohort retention matrix.",
            "access_details": "SQLite / PostgreSQL database file provided with 50,000 synthetic booking records across 5 normalized tables.",
            "dataset_schema": "guests (guest_id, signup_date, country); hotels (hotel_id, name, city, rooms_count); rooms (room_id, hotel_id, room_type, base_price); bookings (booking_id, guest_id, hotel_id, room_id, check_in, check_out, status, channel: Direct/OTA); payments (payment_id, booking_id, amount, paid_at).",
            "requirements_list": [
                "Syntactically valid SQL query scripts utilizing CTEs, multi-table JOINs, and aggregate functions.",
                "Window functions calculating running revenue totals, previous booking comparisons (LAG), and guest visit rank.",
                "SQL-generated cohort retention matrix tracking repeat bookings over 12 months following guest acquisition.",
                "Executive analytical memo summarizing high-value guest segments and direct booking strategies."
            ],
            "implementation_steps": [
                "Step 1: Inspect database schema, verify primary and foreign key constraints, and check indexing.",
                "Step 2: Author CTE-based queries computing total revenue, ADR (Average Daily Rate), and occupancy rate by property.",
                "Step 3: Implement window functions: calculate 30-day rolling booking revenue and delta vs prior period using LAG.",
                "Step 4: Build cohort retention query: group guests by first booking month and calculate % returning in months 1 through 6.",
                "Step 5: Export results and compile a clean presentation report explaining findings to executive stakeholders."
            ],
            "expected_output": "A documented SQL query library with verified query outputs, cohort retention tables, and an executive briefing on guest channel profitability.",
            "tools": "SQL (PostgreSQL / SQLite / MySQL), DBeaver / pgAdmin, Python / Excel for visualization",
            "deadline": "1 to 2 weeks",
            "submission": {
                "items": [
                    "PDF analytical report with query outputs and cohort visualizations (max 10 MB)",
                    "GitHub repository with raw .sql scripts, comments, and schemas",
                    "Query output CSV data files"
                ],
                "live_demo_required": True,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "SQL Query Structure & CTE Design", "weight": 25},
                    {"name": "Window Functions & Analytical Logic", "weight": 25},
                    {"name": "Cohort Retention Matrix Accuracy", "weight": 25},
                    {"name": "Executive Storytelling & Insights", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on SQL syntax cleanliness and CTE readability (25%), correct window function math (25%), accurate cohort matrix generation (25%), and clarity of business recommendations (25%).",
            "is_active": True
        },
        "Advanced": {
            "domain": "data_analytics",
            "domain_display": "Data Analysis",
            "stage": "Advanced",
            "stage_label": "Advanced Industry Project",
            "level": 12,
            "title": "Sunrise Mutual: End-to-End Enterprise BI Dashboard & Metric Model",
            "company": "Sunrise Mutual",
            "industry": "Insurance & Risk Management",
            "what_you_will_build": "An enterprise Business Intelligence (BI) data model and interactive dashboard tracking policyholder retention, loss ratios, regional risk factors, and predictive claims forecasting.",
            "what_you_will_learn": [
                "Dimensional data modeling: designing Star Schema fact and dimension tables for enterprise BI reporting",
                "Automated ETL pipeline scripting in Python to clean, validate, and load incremental transactional data",
                "Interactive BI dashboard design (Power BI / Tableau / Streamlit) with drill-down filters and KPI cards",
                "Statistical hypothesis testing and executive decision-readout storytelling for leadership"
            ],
            "objective": "An insurance carrier needs an end-to-end executive BI platform to analyze underwriting risk, policy renewal decay, and regional claim loss ratios across automotive and property portfolios.",
            "company_context": "Sunrise Mutual underwrites personal lines. Regional claim spikes eroded margins in two states. Underwriters and senior leadership lack an integrated, drillable view comparing claim severity against premium revenue.",
            "task": "Design a dimensional star schema, build a Python ETL pipeline ingesting policy and claims records, model key insurance metrics (Loss Ratio, Retention Rate, Claim Frequency), and deploy an interactive BI dashboard.",
            "access_details": "Three years of historical policy, claim, and customer risk data supplied in relational CSVs.",
            "dataset_schema": "fact_claims (claim_id, policy_id, date_id, claim_amount, status); fact_policies (policy_id, customer_id, date_id, product_id, premium, is_active, renewed); dim_customers (customer_id, credit_tier, age, region); dim_products (product_id, line_of_business); dim_date (date_id, date, month, quarter, year).",
            "requirements_list": [
                "Documented dimensional data model (Star Schema) with entity-relationship diagram (ERD) and surrogate keys.",
                "Automated Python ETL pipeline with data quality assertions (schema validation, zero duplicate facts).",
                "Interactive multi-page BI dashboard (Streamlit, Power BI, or Tableau) with dynamic filtering by line of business and region.",
                "Executive decision briefing slide deck with statistical hypothesis readout evaluating claims variance."
            ],
            "implementation_steps": [
                "Step 1: Architect star schema: define fact_policies, fact_claims, and associated dimension tables.",
                "Step 2: Write Python ETL pipeline (etl_pipeline.py) performing validation, joins, and database loading.",
                "Step 3: Define DAX / SQL measures: Loss Ratio = SUM(claim_amount)/SUM(premium), Policy Retention %, Claim Severity.",
                "Step 4: Build interactive dashboard with executive KPI summary, regional risk heatmap, and loss ratio drill-downs.",
                "Step 5: Conduct hypothesis test (two-sample t-test) evaluating if regional policy pricing significantly impacts retention.",
                "Step 6: Synthesize conclusions into an executive report with interactive dashboard link."
            ],
            "expected_output": "A production-quality BI dashboard and automated data pipeline providing executives with actionable, drillable visibility into insurance risk and revenue retention.",
            "tools": "Python, SQL, Power BI / Tableau / Streamlit, Star Schema, Git",
            "deadline": "2 to 3 weeks",
            "submission": {
                "items": [
                    "Executive BI Architecture Dossier with ERD and metric definitions (max 10 MB)",
                    "GitHub repository with ETL pipeline code and data model schemas",
                    "Public interactive dashboard link (Power BI / Tableau Public / Streamlit Cloud)",
                    "Video walkthrough explaining key dashboard insights"
                ],
                "live_demo_required": True,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Dimensional Data Modeling & Star Schema", "weight": 25},
                    {"name": "ETL Pipeline & Data Validation Rigor", "weight": 25},
                    {"name": "Dashboard UX & Interactive KPI Drilldown", "weight": 25},
                    {"name": "Statistical Analysis & Executive Readout", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on dimensional model soundness (25%), reproducible ETL scripts (25%), dashboard interactivity and clarity (25%), and executive communication polish (25%). Missing live link caps score at 40.",
            "is_active": True
        }
    },

    # =========================================================================
    # 5. ELECTRICAL & ELECTRONICS ENGINEERING (EEE)
    # =========================================================================
    "electronics": {
        "Beginner": {
            "domain": "electronics",
            "domain_display": "Electrical & Electronics Engineering",
            "stage": "Beginner",
            "stage_label": "Beginner Mini Project",
            "level": 4,
            "title": "Brightwell Lighting: Dual-Rail Regulated DC Power Supply & Breadboard Rig",
            "company": "Brightwell Lighting",
            "industry": "Commercial Lighting & Electronics",
            "what_you_will_build": "A benchtop breadboarded dual-rail DC power supply (+5V and +3.3V) with linear regulators (LM7805/LM1117), reverse-polarity diode protection, capacitor ripple filtering, and multimeter test verification.",
            "what_you_will_learn": [
                "Reading schematic symbols and mapping circuit diagrams to breadboard layouts",
                "Ohm's Law (V=IR), resistor color codes, and LED current-limiting calculations",
                "Linear voltage regulation and decoupling capacitor selection to suppress supply noise",
                "Safe laboratory multimeter practices: measuring DC voltage drops and branch currents"
            ],
            "objective": "A lighting engineering lab needs clean, repeatable bench power supplies (+5V logic, +3.3V microcontroller) from an external 9V-12V DC wall adapter with visual power indicators.",
            "company_context": "Brightwell Lighting prototypes IoT smart-switch fixtures. Junior lab technicians frequently fry sensitive 3.3V microcontrollers by plugging them directly into unregulated 12V supplies.",
            "task": "Design, calculate, breadboard, and measure a dual-rail regulated power supply circuit. Calculate current-limiting resistor values for power indicator LEDs, add decoupling capacitors to prevent regulator oscillation, and verify output voltages across varying load resistances.",
            "access_details": "Use physical components (breadboard, LM7805, LM1117, 10uF/0.1uF caps, LEDs, multimeter) or Tinkercad Circuits / CircuitLab simulator.",
            "dataset_schema": "measurement_log.csv — test_point (str), input_voltage_v (float), output_voltage_v (float), load_resistance_ohms (float), measured_current_ma (float), ripple_peak_mv (float).",
            "requirements_list": [
                "Complete schematic diagram with component designators, values, and polarity markings.",
                "Accurate current-limiting calculations for indicator LEDs ensuring forward current < 15mA.",
                "Breadboarded circuit with clean color-coded wiring (Red=5V, Orange=3.3V, Black=GND).",
                "Multimeter verification table proving stable 5.0V (+/-0.1V) and 3.3V (+/-0.08V) outputs under load."
            ],
            "implementation_steps": [
                "Step 1: Calculate LED current-limiting resistor: R = (V_rail - V_forward) / I_desired; select standard E12 resistor.",
                "Step 2: Draw full schematic including input protection diode (1N4001), LM7805, LM1117, input/output caps, and LEDs.",
                "Step 3: Wire circuit on breadboard following color-coded rail conventions and short wire jumpers.",
                "Step 4: Power with 9V DC; measure and record voltages at Vin, 5V rail, 3.3V rail, and across load resistors.",
                "Step 5: Photograph or screenshot bench setup and compile a clean lab measurement report."
            ],
            "expected_output": "A stable dual-rail breadboard power supply providing clean +5V and +3.3V rails with verified multimeter measurements and documentation.",
            "tools": "Breadboard, Multimeter (DMM), LM7805, LM1117, Resistors, Capacitors, Tinkercad / CircuitLab",
            "deadline": "3 to 5 days",
            "submission": {
                "items": [
                    "PDF lab report with schematic, calculations, and multimeter log (max 10 MB)",
                    "High-resolution photograph or simulator link of the wired breadboard",
                    "Voltage verification table"
                ],
                "live_demo_required": False,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Schematic Design & Component Sizing", "weight": 25},
                    {"name": "Mathematical Calculations (Ohm's Law)", "weight": 25},
                    {"name": "Breadboard Layout & Wiring Hygiene", "weight": 25},
                    {"name": "Multimeter Measurement & Lab Notes", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on schematic correctness (25%), mathematical calculations for LEDs and regulators (25%), wiring hygiene and safety (25%), and lab measurement rigor in the report (25%).",
            "is_active": True
        },
        "Intermediate": {
            "domain": "electronics",
            "domain_display": "Electrical & Electronics Engineering",
            "stage": "Intermediate",
            "stage_label": "Intermediate Practical Project",
            "level": 8,
            "title": "FieldSense: Precision Analog Sensor Conditioning & Microcontroller ADC Module",
            "company": "FieldSense",
            "industry": "Agricultural Technology & Instrumentation",
            "what_you_will_build": "An analog sensor front-end (AFE) circuit using an Operational Amplifier (Op-Amp) in an active conditioning configuration, an active low-pass RC filter to reject 50Hz/60Hz line noise, and calibrated ADC digitization.",
            "what_you_will_learn": [
                "Operational amplifier topologies: buffer (voltage follower), inverting, and non-inverting amplifier design",
                "Analog active filter design: calculating cutoff frequencies (fc = 1 / 2*pi*R*C) for anti-aliasing noise rejection",
                "Sensor transfer functions, calibration curves, and Wheatstone bridge interfacing",
                "Analog-to-Digital Converter (ADC) quantization, reference voltages, and scaling in firmware"
            ],
            "objective": "An ag-tech telemetry device requires clean, amplified readings from a high-impedance resistive soil/temperature sensor whose raw output is noisy and spans only a few millivolts.",
            "company_context": "FieldSense produces smart agricultural soil probes. In the field, raw sensor cables pick up severe 50Hz/60Hz AC noise from irrigation pumps, corrupting microcontroller ADC readings.",
            "task": "Design, simulate, and verify an analog signal conditioning front-end using an Op-Amp (LM358/LM324). Condition the sensor signal through a non-inverting amplifier with gain = 10, pass through a low-pass filter (fc = 15Hz), and digitize using a microcontroller ADC.",
            "access_details": "Use SPICE simulator (LTspice / Falstad) or physical hardware. Sensor datasheet and transfer curve supplied.",
            "dataset_schema": "sensor_calibration.csv — temperature_c (float), raw_sensor_mv (float), opamp_output_v (float), adc_reading_10bit (int), error_percentage (float).",
            "requirements_list": [
                "Op-Amp gain calculations and circuit schematic with feedback resistor sizing (Rf and Rin) for desired gain.",
                "Active RC low-pass filter calculation suppressing frequencies above 15Hz by at least -20dB/decade.",
                "SPICE simulation frequency response (Bode plot) showing gain and phase margins.",
                "Calibration curve mapping digitized ADC integer readings back to physical engineering units (e.g. °C)."
            ],
            "implementation_steps": [
                "Step 1: Calculate non-inverting gain: Av = 1 + (Rf / Rin); select precision 1% resistors.",
                "Step 2: Calculate RC filter cutoff: C = 1 / (2 * pi * R * 15Hz); size standard capacitor values.",
                "Step 3: Run AC sweep simulation in LTspice/Falstad; verify gain is constant in passband and attenuates 60Hz noise.",
                "Step 4: Wire circuit on breadboard or prototype board; inject millivolt signals and verify amplified output.",
                "Step 5: Write microcontroller code to read ADC, average 16 samples, and print calibrated physical values to serial monitor."
            ],
            "expected_output": "A noise-filtered, amplified analog front-end circuit providing stable, calibrated sensor measurements to a microcontroller.",
            "tools": "LTspice / Falstad, Op-Amp (LM358), Passive Components, Multimeter/Oscilloscope, Microcontroller",
            "deadline": "1 to 2 weeks",
            "submission": {
                "items": [
                    "PDF engineering report with SPICE Bode plots and math derivations (max 10 MB)",
                    "LTspice schematic file (.asc) or simulator link",
                    "Calibration curve graph and ADC conversion code"
                ],
                "live_demo_required": True,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Op-Amp Amplifier Math & Circuit Design", "weight": 25},
                    {"name": "Filter Design & Noise Suppression", "weight": 25},
                    {"name": "SPICE Simulation Verification", "weight": 25},
                    {"name": "Sensor Calibration & ADC Code", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on Op-Amp gain calculations (25%), filter cutoff math (25%), SPICE simulation Bode plot evidence (25%), and accuracy of ADC calibration (25%).",
            "is_active": True
        },
        "Advanced": {
            "domain": "electronics",
            "domain_display": "Electrical & Electronics Engineering",
            "stage": "Advanced",
            "stage_label": "Advanced Industry Project",
            "level": 12,
            "title": "CircuitNest: Mixed-Signal IoT Hardware Dossier with 2-Layer PCB Design",
            "company": "CircuitNest",
            "industry": "Commercial IoT Prototyping",
            "what_you_will_build": "A complete industrial mixed-signal IoT hardware engineering dossier including KiCad schematic capture, micro-controller interfacing, I2C/SPI bus routing, 2-layer PCB layout with ground planes, Bill of Materials (BOM), and manufacturing Gerbers.",
            "what_you_will_learn": [
                "Professional schematic capture following industry hierarchical block conventions in KiCad/EasyEDA",
                "High-speed and mixed-signal PCB layout rules: continuous ground planes, star grounding, and decoupling loop minimization",
                "Component selection, package footprints (SMD 0805, QFN), thermal dissipation, and Bill of Materials (BOM) sourcing",
                "Design for Manufacturing (DFM): generating standard Gerber X2 and drill files ready for factory fabrication"
            ],
            "objective": "A commercial prototyping team needs a production-ready, manufactured 2-layer PCB design for a wireless environmental telemetry node with solar battery management.",
            "company_context": "CircuitNest delivers turn-key IoT hardware. A client commissioned 500 remote environmental monitoring units. The prototype breadboard is complete; now an industry-standard PCB must be designed for volume assembly.",
            "task": "Design, route, verify, and export a complete 2-layer printed circuit board (PCB) in KiCad for an IoT node (ESP32/STM32 base) with power regulation, battery charger IC, I2C environmental sensor, and status LEDs. Deliver schematic, PCB layout, 3D render, BOM, and Gerbers.",
            "access_details": "Component datasheets, library footprints, and target enclosure mechanical constraints provided. Use free open-source KiCad 7/8.",
            "dataset_schema": "bom.csv — item (int), designator (str), quantity (int), manufacturer (str), part_number (str), description (str), package (str), unit_cost (float).",
            "requirements_list": [
                "Complete electrical schematic in KiCad with proper power net labels, decoupling capacitors at every IC pin, and test points.",
                "Two-layer PCB layout adhering to strict DFM rules (min 6 mil trace/space, thermal reliefs, continuous bottom ground plane).",
                "Clean Design Rule Check (DRC) report with zero unconnected nets and zero design rule violations.",
                "Exported production manufacturing package: RS-274X/X2 Gerbers, Excellon drill files, and formatted Bill of Materials (BOM).",
                "Hardware engineering dossier covering power budget, trace impedance, decoupling strategy, and 3D board visualizations."
            ],
            "implementation_steps": [
                "Step 1: Create KiCad project; draft schematic modules (Power/LDO, Microcontroller, Sensors, Connectors).",
                "Step 2: Assign accurate footprints (SMD 0805 for passives, standard QFP/QFN for ICs) and verify pinouts.",
                "Step 3: Define board edge outline to fit enclosure constraints; place decoupling capacitors as close to IC power pins as possible.",
                "Step 4: Route top layer signal traces; pour solid copper ground plane on bottom layer; connect grounds via thermal relief vias.",
                "Step 5: Run KiCad DRC; resolve all clearance and unrouted net warnings.",
                "Step 6: Export Gerbers, drill files, BOM spreadsheet, and 3D ray-traced board render for the engineering dossier."
            ],
            "expected_output": "A complete, manufacturing-ready PCB design package with verified schematic, DRC-cleared layout, 3D renderings, and production Gerber files.",
            "tools": "KiCad / EasyEDA, Gerber Viewer, SPICE, Component Datasheets",
            "deadline": "2 to 3 weeks",
            "submission": {
                "items": [
                    "Complete Hardware Engineering Dossier in PDF format with 3D renders (max 10 MB)",
                    "GitHub repository with KiCad schematic (.kicad_sch) and PCB (.kicad_pcb) files",
                    "Zipped production Gerber package and drill files",
                    "Costed Bill of Materials (BOM) spreadsheet"
                ],
                "live_demo_required": True,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Schematic Completeness & Decoupling", "weight": 25},
                    {"name": "PCB Layout, Ground Planes & DFM", "weight": 25},
                    {"name": "DRC Clearance & Gerber Package", "weight": 25},
                    {"name": "Engineering Dossier & BOM Quality", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on schematic electrical design (25%), PCB trace routing and ground plane integrity (25%), clean DRC and valid Gerbers (25%), and Bill of Materials sourcing completeness (25%). Missing Gerber package caps score at 40.",
            "is_active": True
        }
    },

    # =========================================================================
    # 6. CYBERSECURITY
    # =========================================================================
    "cybersecurity": {
        "Beginner": {
            "domain": "cybersecurity",
            "domain_display": "Cybersecurity & Information Security",
            "stage": "Beginner",
            "stage_label": "Beginner Mini Project",
            "level": 4,
            "title": "FortressLab: Defensive Security Configuration Audit & Hardening Benchmark",
            "company": "FortressLab",
            "industry": "Corporate Information Security",
            "what_you_will_build": "A comprehensive defensive security configuration audit, vulnerability assessment, and remediation runbook for a simulated corporate web application and host server, evaluating baseline compliance against CIS Benchmarks.",
            "what_you_will_learn": [
                "Applying the CIA Triad (Confidentiality, Integrity, Availability) to system architectures",
                "Auditing web server HTTP security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options)",
                "Identifying common security misconfigurations: weak cipher suites, default credentials, verbose error leaks",
                "Authoring defensive remediation runbooks with risk prioritization (CVSS severity scoring)"
            ],
            "objective": "A security operations team needs an audit and hardening assessment of a newly provisioned internal web portal before it is authorized for corporate production use.",
            "company_context": "FortressLab manages defensive security posture for mid-market enterprises. An internal portal was deployed with default server configurations, potentially exposing sensitive employee data.",
            "task": "Perform a defensive configuration audit on a supplied local server configuration and HTTP response headers. Identify missing headers, weak cookie flags (HttpOnly, Secure, SameSite), open unnecessary services, and write step-by-step remediation commands.",
            "access_details": "Defensive, authorized local inspection only. Simulated Nginx/Apache configuration files, SSL scan reports, and HTTP headers provided. Do not probe external networks.",
            "dataset_schema": "audit_targets/ — nginx.conf (server block), http_headers.txt (curl -I sample response), cipher_suite_audit.txt (SSL Labs output), users_auth_policy.json (password policy rules).",
            "requirements_list": [
                "Complete audit matrix analyzing 10 security controls against the CIS Benchmark and OWASP Top 10.",
                "Analysis of HTTP response headers identifying missing security flags (CSP, HSTS, X-Content-Type-Options, Referrer-Policy).",
                "Remediation configuration snippet providing a hardened nginx.conf / web.config with verified secure defaults.",
                "Executive security advisory memo explaining the business impact of each vulnerability found."
            ],
            "implementation_steps": [
                "Step 1: Inspect supplied web server configuration and curl response headers; check cookie flags and header directives.",
                "Step 2: Compare existing configuration against OWASP Secure Headers Project and CIS Benchmarks.",
                "Step 3: Document each finding with severity rating (High, Medium, Low) and CVE/CWE reference.",
                "Step 4: Author the hardened configuration replacement with comments explaining why each directive was added.",
                "Step 5: Verify the hardened configuration in a local environment and compile the executive audit report."
            ],
            "expected_output": "A formal defensive security assessment report with identified vulnerabilities, CVSS risk ratings, and hardened configuration files ready for deployment.",
            "tools": "curl, Wireshark, Nginx/Apache configuration, OWASP ZAP (local passive scan), Python",
            "deadline": "3 to 5 days",
            "submission": {
                "items": [
                    "PDF security assessment and hardening report (max 10 MB)",
                    "GitHub repository with hardened configuration files and audit scripts",
                    "Before-and-after HTTP header verification diff"
                ],
                "live_demo_required": False,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Vulnerability Identification & Scope", "weight": 25},
                    {"name": "Security Control & CIS Benchmark Rigor", "weight": 25},
                    {"name": "Hardened Remediation Configuration", "weight": 25},
                    {"name": "Executive Communication & Risk Advisory", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on thoroughness of vulnerability detection (25%), accurate CIS benchmark mapping (25%), correctness of the hardened configuration (25%), and clarity of executive risk communication (25%).",
            "is_active": True
        },
        "Intermediate": {
            "domain": "cybersecurity",
            "domain_display": "Cybersecurity & Information Security",
            "stage": "Intermediate",
            "stage_label": "Intermediate Practical Project",
            "level": 8,
            "title": "SentinelLog: Automated Security Operations Log Parser & SIEM Incident Detector",
            "company": "SentinelLog",
            "industry": "Security Operations (SOC) & Threat Detection",
            "what_you_will_build": "A Python-based security operations utility that parses heterogeneous server logs (web server access logs, Linux auth.log, firewall logs), detects attack patterns (brute-force attacks, SQL injection attempts, directory traversal), and generates structured JSON incident alerts.",
            "what_you_will_learn": [
                "Log normalization, regular expression pattern matching for security threats, and timestamp alignment",
                "Detecting automated brute-force attacks via sliding time-window thresholding (e.g. >10 failed logins in 60s)",
                "Identifying web application attack signatures (SQLi quotes, directory traversal ../, XSS tags) in URL parameters",
                "Structuring SIEM-compatible incident alert payloads (CEF / JSON format) with threat severity tagging"
            ],
            "objective": "A security operations center (SOC) needs an automated log parser to process massive authentication and web logs, surface confirmed attack incidents, and reduce analyst alert fatigue.",
            "company_context": "SentinelLog provides managed detection and response (MDR). Analysts manually review thousands of log lines daily. An automated parsing and threat detection engine is required to triage attacks in real time.",
            "task": "Write a modular Python security tool that ingests sample access logs and auth.log files, normalizes timestamps, flags malicious indicators of compromise (IOCs), calculates attack frequency per IP address, and outputs a formatted incident report.",
            "access_details": "Synthetic, authorized lab logs provided containing both normal user activity and simulated attacks (brute force, traversal, injection).",
            "dataset_schema": "logs/ — access.log (Combined Log Format: ip, timestamp, request, status, user_agent); auth.log (timestamp, host, process: sshd, message: Failed password for invalid user).",
            "requirements_list": [
                "Robust Python log ingestion script handling timestamp parsing, malformed lines, and regex normalization.",
                "Detection rule for brute-force SSH attacks tracking failed attempts per IP within configurable time windows.",
                "Detection rule for web attacks identifying directory traversal ('..%2F') and SQL injection payloads.",
                "Exported JSON SIEM incident summary report identifying attacker IPs, targeted accounts, timestamps, and recommended firewall blocklist."
            ],
            "implementation_steps": [
                "Step 1: Write regex parsers for Apache/Nginx Combined Log format and Linux syslog/auth.log format.",
                "Step 2: Implement sliding time-window aggregator using Python collections (defaultdict, deque) to detect frequency bursts.",
                "Step 3: Define pattern matching rules for SQLi indicators ('UNION SELECT', 'OR 1=1') and directory traversal.",
                "Step 4: Output structured JSON alerts containing alert_id, severity, rule_name, source_ip, target_endpoint, and raw_log_excerpt.",
                "Step 5: Document detection rules, false-positive mitigation strategies, and test coverage in a technical report."
            ],
            "expected_output": "A reproducible Python security log detection utility that accurately flags simulated attacks and outputs structured incident response alerts.",
            "tools": "Python 3, Regex, Linux / Bash, JSON, PyTest",
            "deadline": "1 to 2 weeks",
            "submission": {
                "items": [
                    "PDF SOC incident analysis report with threat detection metrics (max 10 MB)",
                    "GitHub repository with Python parser, detection rules, and unit tests",
                    "Generated JSON incident alerts file from the test dataset"
                ],
                "live_demo_required": True,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "Log Parsing & Data Normalization", "weight": 25},
                    {"name": "Threat Detection Rules & Pattern Matching", "weight": 25},
                    {"name": "False Positive Control & Time Windowing", "weight": 25},
                    {"name": "Alert Formatting & SOC Documentation", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on log parsing robustness (25%), detection accuracy for brute force and web attacks (25%), time-window sliding logic (25%), and SIEM alert formatting polish (25%).",
            "is_active": True
        },
        "Advanced": {
            "domain": "cybersecurity",
            "domain_display": "Cybersecurity & Information Security",
            "stage": "Advanced",
            "stage_label": "Advanced Industry Project",
            "level": 12,
            "title": "AegisOps: Enterprise Threat Model, Defense-in-Depth Architecture & Tabletop IR Plan",
            "company": "AegisOps",
            "industry": "Healthcare & Financial Cyber Defense",
            "what_you_will_build": "An enterprise security architecture and incident response dossier for a critical healthcare/fintech web application featuring STRIDE threat modeling, network segmentation architecture, Role-Based Access Control (RBAC), and an Incident Response Playbook for a simulated ransomware/data breach.",
            "what_you_will_learn": [
                "Threat modeling using the Microsoft STRIDE framework and MITRE ATT&CK enterprise matrix",
                "Architecting Defense-in-Depth network boundaries: DMZ, Web Application Firewall (WAF), Zero Trust microsegmentation, and mTLS",
                "Designing identity, authentication, and authorization controls (least privilege, RBAC, OAuth2 / OIDC flows)",
                "Authoring an enterprise Incident Response (IR) Playbook compliant with NIST SP 800-61 (Preparation, Detection, Containment, Eradication, Recovery)"
            ],
            "objective": "A healthcare fintech platform processing sensitive patient billing records needs a complete defensive threat model, architectural hardening blueprint, and incident response playbook ahead of regulatory compliance audit.",
            "company_context": "AegisOps protects sensitive electronic health records (EHR) and payment data. Regulatory bodies mandate a formal STRIDE threat model and verified Incident Response Plan before the platform can go live.",
            "task": "Develop an enterprise-grade cyber defense dossier. Perform a comprehensive STRIDE threat model on the application architecture, design a defense-in-depth network topology with network diagrams, design an RBAC permission matrix, and author an Incident Response Playbook for a simulated breach scenario.",
            "access_details": "System architecture specifications, data flow diagrams (DFD), and regulatory requirements provided. Authorized defensive documentation and planning workflow.",
            "dataset_schema": "threat_model_assets/ — system_dfd.png (data flow diagram), api_endpoints.json, user_roles.csv (Admin, Doctor, Patient, BillingClerk), compliance_checklist.csv.",
            "requirements_list": [
                "STRIDE threat model analyzing all data flows, identifying at least 6 distinct threats with MITRE ATT&CK mappings and mitigations.",
                "Defense-in-depth network architecture diagram illustrating edge firewalls, DMZ, WAF, application cluster, and encrypted database tier.",
                "Granular Role-Based Access Control (RBAC) permission matrix enforcing the principle of least privilege across 4 user roles.",
                "Comprehensive Incident Response (IR) Playbook covering containment, evidence preservation, stakeholder communication, and root-cause eradication."
            ],
            "implementation_steps": [
                "Step 1: Deconstruct system architecture into Level-0 and Level-1 Data Flow Diagrams (DFDs) identifying trust boundaries.",
                "Step 2: Apply STRIDE methodology to each element (Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege).",
                "Step 3: Design network segmentation: define subnets, firewall rules, TLS 1.3 termination, and zero-trust API gateway policies.",
                "Step 4: Formulate RBAC access control matrix defining create/read/update/delete permissions for each role.",
                "Step 5: Write Incident Response Playbook following NIST SP 800-61 covering a simulated credential stuffing & data exfiltration incident.",
                "Step 6: Compile all diagrams, threat matrices, and playbooks into a formal Enterprise Security Dossier."
            ],
            "expected_output": "A comprehensive enterprise cybersecurity dossier containing a STRIDE threat model, network defense architecture diagrams, RBAC matrix, and NIST-aligned Incident Response Playbook.",
            "tools": "STRIDE, MITRE ATT&CK Navigator, Draw.io / Lucidchart, NIST SP 800-61, Python for automated policy checks",
            "deadline": "2 to 3 weeks",
            "submission": {
                "items": [
                    "Enterprise Cyber Defense & Threat Model Dossier in PDF format (max 10 MB)",
                    "GitHub repository with architecture diagrams, threat matrices, and policy files",
                    "Tabletop Incident Response scenario simulation readout",
                    "Executive risk briefing presentation"
                ],
                "live_demo_required": True,
                "pdf_required": True,
            },
            "scoring": {
                "criteria": [
                    {"name": "STRIDE Threat Modeling & MITRE Mapping", "weight": 25},
                    {"name": "Defense-in-Depth Network Architecture", "weight": 25},
                    {"name": "Access Control & Least Privilege Rigor", "weight": 25},
                    {"name": "NIST Incident Response Playbook Polish", "weight": 25}
                ],
                "pass_score": 60,
                "missing_required_evidence_cap": 40
            },
            "evaluation_criteria": "Evaluated on thoroughness of the STRIDE threat model (25%), robustness of defense-in-depth architecture diagrams (25%), precision of the RBAC matrix (25%), and practical completeness of the NIST Incident Response Playbook (25%).",
            "is_active": True
        }
    }
}


def get_stage_project(domain_key: str, stage: str) -> Optional[Dict[str, Any]]:
    """Retrieves the stage project for a given domain and stage ('Beginner', 'Intermediate', 'Advanced')."""
    dk = (domain_key or '').lower()
    # Normalize domain keys
    if 'web' in dk or 'full' in dk or 'front' in dk or 'back' in dk or 'django' in dk:
        dk = 'web_dev'
    elif 'ai' in dk or 'ml' in dk or 'machine' in dk:
        dk = 'ai_ml'
    elif 'robot' in dk:
        dk = 'robotics'
    elif 'data' in dk or 'anal' in dk or 'sql' in dk:
        dk = 'data_analytics'
    elif 'electr' in dk or 'circuit' in dk or 'eee' in dk or 'hardware' in dk:
        dk = 'electronics'
    elif 'cyber' in dk or 'security' in dk or 'infosec' in dk:
        dk = 'cybersecurity'
    else:
        dk = 'web_dev'

    stage_norm = (stage or 'Beginner').capitalize()
    if stage_norm not in ('Beginner', 'Intermediate', 'Advanced'):
        stage_norm = 'Beginner'

    return STAGE_PROJECTS.get(dk, {}).get(stage_norm)


def get_all_stage_projects_for_domain(domain_key: str) -> List[Dict[str, Any]]:
    """Returns the three stage projects (Beginner, Intermediate, Advanced) for a domain."""
    dk = (domain_key or '').lower()
    if 'web' in dk or 'full' in dk or 'front' in dk or 'back' in dk or 'django' in dk:
        dk = 'web_dev'
    elif 'ai' in dk or 'ml' in dk or 'machine' in dk:
        dk = 'ai_ml'
    elif 'robot' in dk:
        dk = 'robotics'
    elif 'data' in dk or 'anal' in dk or 'sql' in dk:
        dk = 'data_analytics'
    elif 'electr' in dk or 'circuit' in dk or 'eee' in dk or 'hardware' in dk:
        dk = 'electronics'
    elif 'cyber' in dk or 'security' in dk or 'infosec' in dk:
        dk = 'cybersecurity'
    else:
        dk = 'web_dev'

    domain_data = STAGE_PROJECTS.get(dk, {})
    return [
        domain_data.get('Beginner'),
        domain_data.get('Intermediate'),
        domain_data.get('Advanced')
    ]



def get_stage_nodes_for_goal(goal, stage: str):
    """
    Returns the list of SkillNode objects belonging to the specified stage
    for a given UserGoal.
    Beginner: coach_level/order 1..4 (or tier='Beginner')
    Intermediate: coach_level/order 5..8 (or tier='Intermediate')
    Advanced: coach_level/order 9..12 (or tier='Advanced')
    """
    stage_ranges = {
        'Beginner': (1, 4),
        'Intermediate': (5, 8),
        'Advanced': (9, 12),
    }
    first_lvl, last_lvl = stage_ranges.get(stage, (1, 4))
    all_nodes = list(goal.skill_nodes.all().order_by('order'))
    nodes = [n for n in all_nodes if first_lvl <= (n.coach_level or n.order) <= last_lvl]
    if not nodes:
        nodes = [n for n in all_nodes if (n.tier or '').capitalize() == stage]
    if not nodes:
        if (goal.chosen_tier or '').capitalize() == stage or stage == 'Beginner':
            nodes = all_nodes
    return nodes


def get_stage_learning_progress(goal, stage: str) -> Dict[str, Any]:
    """
    Computes lesson/quiz completion progress for a stage.
    """
    nodes = get_stage_nodes_for_goal(goal, stage)
    total_nodes = len(nodes)
    completed_nodes = [n for n in nodes if n.status == 'completed']
    completed_count = len(completed_nodes)
    pending_nodes = [n for n in nodes if n.status != 'completed']
    all_completed = (total_nodes > 0 and completed_count == total_nodes)
    
    return {
        'stage': stage,
        'total_nodes': total_nodes,
        'completed_count': completed_count,
        'completed_nodes': completed_nodes,
        'pending_nodes': pending_nodes,
        'all_lessons_completed': all_completed,
        'progress_pct': int((completed_count / total_nodes) * 100) if total_nodes else 0,
    }


def is_stage_project_completed(goal, stage: str):
    """
    Returns (is_completed, score) for a stage project.
    """
    from .models import Project
    p = Project.objects.filter(
        goal=goal,
        level__icontains=stage,
        status='Completed'
    ).order_by('-score').first()
    
    if not p:
        p = Project.objects.filter(
            goal=goal,
            title__icontains=stage,
            status='Completed'
        ).order_by('-score').first()
        
    if p:
        return True, p.score
    return False, 0


def is_stage_project_unlocked(goal, stage: str) -> bool:
    """
    A stage project is UNLOCKED only after the learner completes all required lessons
    and quizzes for that stage.
    
    Beginner: All Beginner lessons completed.
    Intermediate:
      - If enrolled as Beginner: Beginner stage project must be completed AND Intermediate lessons completed.
      - If enrolled as Intermediate: Intermediate lessons completed.
    Advanced:
      - Previous stage project completed AND Advanced lessons completed.
    """
    # ---- TEMPORARY TESTING OVERRIDE - remove after QA ----
    return True
    # ---- END TESTING OVERRIDE ----
    stage_prog = get_stage_learning_progress(goal, stage)
    if not stage_prog['all_lessons_completed']:
        return False
    
    chosen = (goal.chosen_tier or 'Beginner').capitalize()
    
    if stage == 'Beginner':
        return True
    elif stage == 'Intermediate':
        if chosen in ('Intermediate', 'Advanced'):
            return True
        beg_completed, _ = is_stage_project_completed(goal, 'Beginner')
        return beg_completed
    elif stage == 'Advanced':
        if chosen == 'Advanced':
            return True
        mid_completed, _ = is_stage_project_completed(goal, 'Intermediate')
        return mid_completed
    return False


def get_stage_summary_for_dashboard(goal, domain_key: str) -> List[Dict[str, Any]]:
    """
    Builds the 3-stage project indicators for the dashboard.
    At the beginning of a roadmap, actual project details are hidden;
    only stage indicators with locked/unlocked/completed status are shown.
    """
    summaries = []
    for s in ('Beginner', 'Intermediate', 'Advanced'):
        prog = get_stage_learning_progress(goal, s)
        is_comp, score = is_stage_project_completed(goal, s)
        is_unlk = is_comp or is_stage_project_unlocked(goal, s)
        raw_p = get_stage_project(domain_key, s) or {}
        
        if is_comp:
            status_label = 'Completed'
            badge_class = 'badge-completed'
            display_title = raw_p.get('title', f"{s} Stage Project")
            display_desc = raw_p.get('what_you_will_build', '')
        elif is_unlk:
            status_label = 'Unlocked'
            badge_class = 'badge-unlocked'
            display_title = raw_p.get('title', f"{s} Stage Project")
            display_desc = raw_p.get('what_you_will_build', '')
        else:
            status_label = 'Locked'
            badge_class = 'badge-locked'
            display_title = f"{s} Project"
            display_desc = f"Complete all {s} stage lessons and topic quizzes to unlock this portfolio project."
        
        summaries.append({
            'stage': s,
            'is_unlocked': is_unlk,
            'is_completed': is_comp,
            'score': score,
            'status_label': status_label,
            'badge_class': badge_class,
            'completed_lessons': prog['completed_count'],
            'total_lessons': prog['total_nodes'],
            'pending_nodes': prog['pending_nodes'],
            'progress_percent': prog['progress_pct'],
            'display_title': display_title,
            'display_description': display_desc,
            'raw_project': raw_p,
        })
    return summaries
