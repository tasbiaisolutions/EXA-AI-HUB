import json
import random
import re
from typing import Dict, Any, List
from .course_content import RESTRUCTURED_CURRICULA
from .course_teaching import build_course_lesson, build_course_quiz, get_course_guide

# =============================================================================
# DOMAIN DETECTION — Single source of truth
# =============================================================================

def detect_domain(domain: str, goal: str, skill_name: str = "") -> str:
    """
    Determine which curriculum branch to use.
    Prioritizes explicit user goal choices over fallback domain defaults.
    """
    goal_lower = (goal or "").lower()
    domain_lower = (domain or "").lower()
    combined = f"{domain_lower} {goal_lower} {(skill_name or '').lower()}"

    domain_aliases = {
        "web_dev": "web_dev",
        "data_analytics": "data_analytics",
        "ai_ml": "ai_ml",
        "robotics": "robotics",
        "electronics": "electronics",
        "electrocics": "electronics",
        "electrocics engineering": "electronics",
        "eee": "electronics",
        "electrical": "electronics",
        "electrician": "electronics",
        "electrical and electroncial": "electronics",
        "electrical and electroncial engineering": "electronics",
        "electrical & electronics": "electronics",
        "electrical and electronics": "electronics",
        "electronics engineering": "electronics",
        "electrical engineering": "electronics",
        "electrical and electronics engineering": "electronics",
        "cybersecurity": "cybersecurity",
    }
    if domain_lower.strip() in domain_aliases:
        return domain_aliases[domain_lower.strip()]

    # 1. Explicit goal keyword matches (highest priority)
    if any(w in goal_lower for w in ["fullstack", "full stack", "full-stack", "web dev", "web development", "frontend", "front-end", "backend", "back-end"]):
        return "web_dev"
    if any(w in goal_lower for w in ["data analyst", "data analytics", "business intelligence", "power bi", "tableau"]):
        return "data_analytics"
    if any(w in goal_lower for w in ["ui/ux", "ui ux", "ux designer", "ui designer", "product design", "figma"]):
        return "ui_ux"
    if any(w in goal_lower for w in ["cybersecurity", "cyber security", "ethical hack", "penetration test", "infosec", "network security"]):
        return "cybersecurity"
    if any(w in goal_lower for w in ["cloud", "devops", "aws", "azure", "gcp", "docker", "kubernetes"]):
        return "cloud_devops"
    if any(w in goal_lower for w in ["machine learning", "deep learning", "artificial intelligence", "ai/ml", "generative ai"]):
        return "ai_ml"
    if any(term in goal_lower for term in ("electronics", "electrocics")) and not any(w in goal_lower for w in ("robotics", "robot engineer", "robot developer")):
        return "electronics"
    if "robotics" in goal_lower or "robot" in goal_lower:
        return "robotics"

    # 2. Combined keyword matches
    if any(w in combined for w in ["fullstack", "full stack", "full-stack", "web dev", "web development", "frontend", "front-end", "backend", "back-end", "html", "css", "react", "vue", "angular", "node.js", "nodejs", "django web", "flask web", "rest api", "graphql"]):
        return "web_dev"
    if any(w in combined for w in ["robotics", "robot", "embedded", "arduino", "raspberry", "iot", "microcontroller", "firmware", "rtos"]):
        return "robotics"
    if any(w in combined for w in ["ui/ux", "ui ux", "ux designer", "ui designer", "product design", "figma", "user experience", "user interface"]):
        return "ui_ux"
    if any(w in combined for w in ["cybersecurity", "cyber security", "ethical hack", "penetration test", "network security", "infosec", "ctf", "kali", "nmap", "wireshark"]):
        return "cybersecurity"
    if any(w in combined for w in ["machine learning", "ml ", " ml", "deep learning", "neural network", "artificial intelligence", " ai ", "ai/ml", "tensorflow", "pytorch", "scikit", "nlp ", "computer vision", "llm", "generative ai"]):
        return "ai_ml"
    if any(w in combined for w in ["cloud", "devops", "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "terraform", "ansible", "jenkins", "deployment pipeline"]):
        return "cloud_devops"
    if any(w in combined for w in ["data analyst", "data analytics", "business intelligence", "power bi", "tableau", "excel analyst", "data analysis", "analytics engineer"]):
        return "data_analytics"
    if any(w in combined for w in ["javascript", "typescript", "js ", " js", "ecmascript", "node js", "deno", "bun "]):
        return "javascript"
    if any(w in combined for w in ["data structure", "data structures", "dsa", "leetcode", "competitive programming", "binary tree", "graph theory", "dynamic programming"]):
        return "dsa"
    if any(w in combined for w in ["sql", "database", "mysql", "postgresql", "sqlite", "mongodb", "nosql", "redis", "db design", "relational"]):
        return "sql_databases"
    if any(w in combined for w in ["python programming", "learn python", "python developer", "python engineer", "python basics", "python course", "python scripting", "python for beginners", "python"]):
        return "python"
    if any(w in combined for w in ["mobile", "android", "ios", "swift", "kotlin", "flutter", "react native"]):
        return "mobile_dev"
    if any(w in combined for w in ["software engineer", "software development", "git", "testing", "agile", "scrum", "system design", "clean code", "design pattern"]):
        return "software_engineering"

    # Default to custom synthesis for any uncatalogued domain or career goal
    return "custom"


def synthesize_custom_roadmap(goal: str, domain: str, level: str, skills: str) -> Dict[str, Any]:
    """Dynamically construct a tailored 6-stage roadmap for any career goal or domain."""
    raw_title = goal.strip() if (goal and goal.strip()) else ((domain or "").strip() if (domain and domain.strip()) else "Modern Engineering")
    clean_title = raw_title
    for prefix in ["i want to become a ", "i want to learn ", "i want to be a ", "become a ", "become an ", "learn "]:
        if clean_title.lower().startswith(prefix):
            clean_title = clean_title[len(prefix):]
    clean_title = clean_title.strip().title()
    if not clean_title:
        clean_title = "Applied Technology"

    return {
        "expert_agent_name": f"{clean_title} Principal Specialist & Mentor",
        "expert_agent_intro": f"Let's build your {clean_title} skills one practical step at a time.",
        "skill_nodes": [
            {
                "name": f"Level 1: {clean_title} Foundations & Core Principles",
                "description": f"Fundamental concepts, core terminology, environment setup, and essential mental models for {clean_title}.",
                "importance": f"Builds the necessary conceptual foundation required before tackling practical workflows in {clean_title}."
            },
            {
                "name": f"Level 2: Essential Tooling, Syntax & Core Workflows",
                "description": f"Hands-on syntax, core tools, and standard workflows used daily by {clean_title} practitioners.",
                "importance": f"Translates theoretical knowledge of {clean_title} into practical, working capability."
            },
            {
                "name": f"Level 3: Architecture, Integration & Practical Application",
                "description": f"Structuring systems, handling data flow, integrating modules, and building realistic {clean_title} features.",
                "importance": "Enables building modular, maintainable, and scalable systems."
            },
            {
                "name": f"Level 4: Advanced Patterns, Performance & Reliability",
                "description": f"Handling complex edge cases, debugging tricky failure modes, and optimizing {clean_title} workflows.",
                "importance": "Separates junior learners from production-ready practitioners."
            },
            {
                "name": f"Level 5: Industry Best Practices, Security & Collaboration",
                "description": f"Testing methodologies, security hardening, automated pipelines, code quality standards, and team collaboration in {clean_title}.",
                "importance": "Prepares you to deliver reliable, enterprise-grade deliverables in a professional setting."
            },
            {
                "name": f"Level 6: {clean_title} Capstone Portfolio Project",
                "description": f"Design, build, and ship a comprehensive, end-to-end practical project demonstrating your mastery of {clean_title}.",
                "importance": "Provides concrete, employer-ready proof of capability."
            }
        ]
    }


# =============================================================================
# CURRICULUM DEFINITIONS
# =============================================================================

CURRICULA = {

    "python": {
        "expert_name": "Senior Python Engineer & Mentor",
        "intro": "Welcome to the complete Python Programming track! I'm your personal Python mentor. We'll build from zero to writing clean, production-quality Python — variables and loops all the way to OOP, file handling, APIs, and real projects.",
        "levels": [
            {
                "name": "Level 1: Python Foundations",
                "description": "Python syntax, variables, data types, input/output, conditionals, loops, and writing your first scripts.",
                "importance": "Every Python program — from scripts to machine learning models — is built on these fundamentals."
            },
            {
                "name": "Level 2: Functions, Modules & Data Structures",
                "description": "Defining and calling functions, scope, lambda, lists, tuples, dictionaries, sets, list comprehensions, and working with Python's standard library.",
                "importance": "Functions and data structures are the backbone of every real Python program."
            },
            {
                "name": "Level 3: Object-Oriented Python & File Handling",
                "description": "Classes, objects, inheritance, encapsulation, polymorphism, magic methods, file I/O, JSON, CSV, and exception handling.",
                "importance": "OOP lets you build maintainable, scalable software. File I/O connects your programs to the real world."
            },
            {
                "name": "Level 4: Advanced Python & Ecosystem",
                "description": "Decorators, generators, context managers, async/await, virtual environments, pip, testing with pytest, and working with external APIs.",
                "importance": "Advanced Python patterns are used in every professional codebase — from web apps to data pipelines."
            },
            {
                "name": "Level 5: Python Capstone Project",
                "description": "Build a complete, working Python application — CLI tool, REST API wrapper, automation script, or data pipeline — with clean code, tests, and documentation.",
                "importance": "Proves you can take Python from concept to a shipped, real-world product."
            }
        ]
    },

    "web_dev": {
        "expert_name": "Senior Full-Stack Web Architect & Mentor",
        "intro": "Welcome to the complete Full-Stack Web Development track! I am your personal mentor. We will journey through every layer of modern web engineering — from web fundamentals and semantic HTML to CSS, JavaScript, Git, React, backend APIs, databases, authentication, CI/CD, and portfolio projects.",
        "levels": [
            {
                "name": "Level 1: Web Fundamentals",
                "description": "How the web works: DNS, HTTP/HTTPS protocols, client-server architecture, browser rendering lifecycle, and developer tools.",
                "importance": "The foundational mental model for all frontend and backend communication."
            },
            {
                "name": "Level 2: HTML & Semantic Structure",
                "description": "Document structure, semantic HTML5 elements, forms, input types, client validation, multimedia, and web accessibility (a11y).",
                "importance": "The structural backbone of every web application, critical for accessibility and search engine indexing."
            },
            {
                "name": "Level 3: CSS & Modern Responsive Design",
                "description": "CSS selectors, box model, Flexbox layouts, CSS Grid, media queries, mobile-first design, and custom properties.",
                "importance": "Enables you to build responsive, visually engaging user interfaces across mobile and desktop devices."
            },
            {
                "name": "Level 4: JavaScript Core & Asynchronous Logic",
                "description": "Variables, data types, functions, scope, closures, DOM manipulation, event loop, Promises, async/await, and Fetch API.",
                "importance": "The core programming language of the web that drives interactivity and asynchronous client applications."
            },
            {
                "name": "Level 5: Git & GitHub Version Control",
                "description": "Git repositories, commits, branching strategies, merge conflicts, pull requests, and collaborative developer workflows on GitHub.",
                "importance": "Essential industry collaboration skill required by every professional engineering team."
            },
            {
                "name": "Level 6: Frontend Framework (React)",
                "description": "Component architecture, JSX, props, state, hooks (useState, useEffect), client routing (React Router), and Context API.",
                "importance": "The industry standard for building scalable, high-performance interactive single-page web applications."
            },
            {
                "name": "Level 7: Backend Development & Server Architecture",
                "description": "Server runtimes (Node.js/Express or Python/Django), routing, middleware, controllers, error handling, and business logic.",
                "importance": "The engine where server-side logic, business workflows, and data processing safely execute."
            },
            {
                "name": "Level 8: Databases & SQL",
                "description": "Relational schema design, normalization, SQL queries (SELECT, JOIN, GROUP BY), indexing, transactions, and ORM integration.",
                "importance": "Every production web application relies on robust, consistent data modeling and persistence."
            },
            {
                "name": "Level 9: API Development & REST Integration",
                "description": "RESTful API design constraints, HTTP status codes, JSON serialization, query parameters, pagination, and API consumption.",
                "importance": "Enables seamless data exchange between client applications, external services, and backend databases."
            },
            {
                "name": "Level 10: Authentication & Security Fundamentals",
                "description": "User authentication, password hashing (bcrypt), session cookies, stateless JWT tokens, CORS, CSRF, and OWASP Top 10 defense.",
                "importance": "Protects user data, prevents malicious exploits, and ensures production security compliance."
            },
            {
                "name": "Level 11: Testing & Deployment (CI/CD)",
                "description": "Unit testing, integration testing, Docker containers, automated CI/CD pipelines, and cloud platform deployment.",
                "importance": "Ensures code quality, prevents regressions, and enables automated zero-downtime shipping to production."
            },
            {
                "name": "Level 12: Full-Stack Capstone Portfolio Projects",
                "description": "End-to-end full-stack projects integrating frontend, backend, database, authentication, testing, and live production deployment.",
                "importance": "Provides concrete, employer-ready proof of your ability to ship complete production web software."
            }
        ]
    },

    "javascript": {
        "expert_name": "Senior JavaScript & TypeScript Engineer",
        "intro": "Welcome to the JavaScript Mastery track! From variables and functions to asynchronous patterns, TypeScript, Node.js, and modern frameworks — we'll cover the full language deeply.",
        "levels": [
            {
                "name": "Level 1: JavaScript Core Language",
                "description": "Variables (var/let/const), data types, operators, control flow, functions, scope, closures, and the event loop.",
                "importance": "The language fundamentals everything in the JS ecosystem is built on."
            },
            {
                "name": "Level 2: ES6+ Modern JavaScript",
                "description": "Arrow functions, destructuring, spread/rest, template literals, modules (import/export), Promises, async/await, and iterators.",
                "importance": "Modern JS syntax is used in every professional frontend and backend JavaScript project."
            },
            {
                "name": "Level 3: DOM, Browser APIs & Async Patterns",
                "description": "DOM manipulation, events, fetch API, localStorage, Web Workers, error handling, and advanced async patterns.",
                "importance": "Required for building interactive, performant web UIs."
            },
            {
                "name": "Level 4: TypeScript & Node.js",
                "description": "TypeScript types, interfaces, generics, Node.js runtime, npm ecosystem, Express APIs, and working with databases.",
                "importance": "TypeScript catches bugs at compile time. Node.js takes JavaScript server-side."
            },
            {
                "name": "Level 5: JavaScript Capstone Project",
                "description": "Build a complete JavaScript application — REST API, CLI tool, or interactive web app — with TypeScript, tests, and deployment.",
                "importance": "Demonstrates professional JavaScript engineering capability."
            }
        ]
    },

    "data_analytics": {
        "expert_name": "Senior Data Analyst Mentor & Trainer",
        "intro": "Build confidence with data, one useful skill and real-world project at a time.",
        "levels": [
            {
                "name": "Level 1: Data Analyst Foundations",
                "description": "How analysts solve business problems, structured vs unstructured data, records & fields, KPIs, metrics vs dimensions, and the analytical lifecycle.",
                "importance": "The core mental model for every analysis you will ever do."
            },
            {
                "name": "Level 2: Microsoft Excel: Beginner to Advanced",
                "description": "Formulas ($A$1 references, SUM, AVERAGE, COUNTIFS, SUMIFS, XLOOKUP, INDEX/MATCH), data cleaning, PivotTables, slicers & KPI dashboards.",
                "importance": "The daily workhorse tool of every business data analyst."
            },
            {
                "name": "Level 3: Statistics & Analytical Thinking",
                "description": "Mean, median, mode, variance, standard deviation, distributions, outliers, correlation vs causation, and A/B testing.",
                "importance": "Separates basic number-crunchers from true analytical thinkers."
            },
            {
                "name": "Level 4: SQL: Beginner to Advanced",
                "description": "Relational schemas, SELECT, WHERE, GROUP BY, HAVING, multi-table JOINs, CTEs, and Window Functions.",
                "importance": "The universal standard for extracting and querying company data."
            },
            {
                "name": "Level 5: Data Visualization & Power BI",
                "description": "Visual storytelling, chart selection, Power Query, Star Schema modeling, DAX measures, and executive interactive dashboards.",
                "importance": "How you present findings to senior leaders who don't read raw data."
            },
            {
                "name": "Level 6: Python for Data Analysis",
                "description": "Jupyter, Pandas DataFrames, NumPy, data cleaning, EDA, and Matplotlib/Seaborn visualization.",
                "importance": "Automates massive datasets and unlocks advanced analytics."
            },
            {
                "name": "Level 7: Business Analysis & Communication",
                "description": "Translating business questions into KPIs, churn rate, CAC, retention cohorts, and evidence-based recommendations.",
                "importance": "Turns data into actual profit, cost savings, and strategic decisions."
            },
            {
                "name": "Level 8: Professional Portfolio & Capstone",
                "description": "End-to-end multi-tool analytics portfolio project, interview prep, and resume packaging.",
                "importance": "Proves job-readiness to hiring managers and recruiters."
            }
        ]
    },

    "ai_ml": {
        "expert_name": "Senior AI/ML Engineer & Research Mentor",
        "intro": "Welcome to the AI & Machine Learning track! From maths foundations and classical ML to deep learning, NLP, and deploying production AI systems — this is your complete roadmap.",
        "levels": [
            {
                "name": "Level 1: AI/ML Foundations & Mathematics",
                "description": "What AI/ML is, supervised vs unsupervised learning, linear algebra essentials (vectors, matrices), calculus intuition (gradients), probability basics, and the ML workflow.",
                "importance": "Every ML algorithm is math in disguise — understanding these foundations prevents you from using models blindly."
            },
            {
                "name": "Level 2: Classical Machine Learning",
                "description": "Linear regression, logistic regression, decision trees, random forests, SVMs, k-means clustering, model evaluation (precision, recall, F1, AUC), and scikit-learn.",
                "importance": "Classical ML still solves most real business problems faster and more interpretably than deep learning."
            },
            {
                "name": "Level 3: Deep Learning & Neural Networks",
                "description": "Perceptrons, activation functions, backpropagation, CNNs for vision, RNNs/LSTMs, batch normalization, dropout, and TensorFlow/PyTorch implementation.",
                "importance": "Deep learning powers image recognition, speech, NLP, and recommendation systems."
            },
            {
                "name": "Level 4: NLP & Large Language Models",
                "description": "Text preprocessing, embeddings, transformers architecture, fine-tuning pre-trained models (BERT, GPT), prompt engineering, RAG, and LangChain.",
                "importance": "NLP and LLMs are the fastest-growing area in AI engineering."
            },
            {
                "name": "Level 5: ML Engineering & Production AI",
                "description": "MLOps, model serving (FastAPI, Docker), feature stores, model monitoring, A/B testing ML models, and responsible AI principles.",
                "importance": "A model only creates value when it's reliably running in production."
            }
        ]
    },

    "dsa": {
        "expert_name": "Senior Software Engineer & DSA Interview Coach",
        "intro": "Welcome to the Data Structures & Algorithms track! Master the patterns that top tech companies test in interviews — arrays, trees, graphs, dynamic programming — with clear explanations and practice.",
        "levels": [
            {
                "name": "Level 1: Arrays, Strings & Basic Complexity",
                "description": "Big-O notation, arrays, strings, two-pointer technique, sliding window, hash maps, and solving linear-time problems.",
                "importance": "Arrays and strings are in over 60% of coding interview problems."
            },
            {
                "name": "Level 2: Linked Lists, Stacks & Queues",
                "description": "Singly/doubly linked lists, fast/slow pointers, stacks (LIFO), queues (FIFO), monotonic stacks, and deque patterns.",
                "importance": "Classic data structures tested heavily in FAANG-level interviews."
            },
            {
                "name": "Level 3: Trees & Recursion",
                "description": "Binary trees, BSTs, tree traversals (DFS/BFS), recursion patterns, backtracking, tries, and heap/priority queues.",
                "importance": "Tree problems combine recursion, algorithmic thinking, and real system design concepts."
            },
            {
                "name": "Level 4: Graphs & Advanced Algorithms",
                "description": "Graph representations, BFS/DFS, Dijkstra's, topological sort, union-find, dynamic programming (memoization & tabulation).",
                "importance": "Graphs model real-world systems — social networks, maps, dependency resolution."
            },
            {
                "name": "Level 5: Interview Mastery & Problem Patterns",
                "description": "Solving 50+ problems by pattern, mock interview simulation, system design basics, and building a problem-solving portfolio.",
                "importance": "Pattern recognition — not memorization — is what gets you through top-tier tech interviews."
            }
        ]
    },

    "sql_databases": {
        "expert_name": "Senior Database Engineer & SQL Mentor",
        "intro": "Welcome to the SQL & Databases track! From writing your first SELECT query to designing scalable database schemas and optimising production queries — this track covers it all.",
        "levels": [
            {
                "name": "Level 1: SQL Fundamentals",
                "description": "Relational model, tables, primary/foreign keys, SELECT, WHERE, ORDER BY, LIMIT, INSERT, UPDATE, DELETE.",
                "importance": "SQL is the universal language of data — every developer and analyst needs it."
            },
            {
                "name": "Level 2: Aggregations, Joins & Subqueries",
                "description": "GROUP BY, HAVING, INNER/LEFT/RIGHT JOINs, self-joins, subqueries, and NULL handling.",
                "importance": "Real-world queries almost always join multiple tables and aggregate results."
            },
            {
                "name": "Level 3: Advanced SQL",
                "description": "CTEs (WITH), window functions (ROW_NUMBER, RANK, LAG, LEAD), stored procedures, transactions, and indexing strategy.",
                "importance": "Advanced SQL unlocks analytics-grade queries and production performance optimisation."
            },
            {
                "name": "Level 4: Database Design & Optimisation",
                "description": "Normalisation (1NF–3NF), ER diagrams, query execution plans (EXPLAIN), index types, partitioning, and replication basics.",
                "importance": "Bad schema design creates technical debt that costs teams months to fix."
            },
            {
                "name": "Level 5: Database Capstone",
                "description": "Design, build, populate and query a complete relational database for a real business scenario with full documentation.",
                "importance": "Proves end-to-end database engineering competence."
            }
        ]
    },

    "cloud_devops": {
        "expert_name": "Senior Cloud & DevOps Engineer Mentor",
        "intro": "Welcome to the Cloud & DevOps track! From Linux and networking basics to AWS/GCP, Docker, Kubernetes, CI/CD pipelines, and infrastructure as code — build the skills that keep modern software running.",
        "levels": [
            {
                "name": "Level 1: Linux, Networking & Cloud Fundamentals",
                "description": "Linux CLI, bash scripting, TCP/IP, DNS, HTTP, cloud computing concepts, and navigating AWS/GCP/Azure consoles.",
                "importance": "Every cloud and DevOps role starts with solid Linux and networking foundations."
            },
            {
                "name": "Level 2: Containerisation with Docker",
                "description": "Container vs VM, Dockerfile authoring, image builds, volumes, networks, Docker Compose, and container best practices.",
                "importance": "Docker is the foundation of modern software deployment — it's required in almost every engineering job."
            },
            {
                "name": "Level 3: CI/CD Pipelines & Automation",
                "description": "Git workflows, GitHub Actions, automated testing in pipelines, artifact builds, deployment automation, and secrets management.",
                "importance": "CI/CD eliminates manual deployments and lets teams ship confidently multiple times a day."
            },
            {
                "name": "Level 4: Kubernetes & Cloud Infrastructure",
                "description": "Kubernetes pods, services, deployments, Helm charts, AWS EC2/S3/RDS, IAM, Terraform infrastructure as code.",
                "importance": "Kubernetes orchestrates containers at scale — it's the production standard for cloud-native apps."
            },
            {
                "name": "Level 5: DevOps Capstone Project",
                "description": "Deploy a complete application with Docker, CI/CD, Kubernetes, monitoring (Prometheus/Grafana), and infrastructure as code.",
                "importance": "Demonstrates full DevOps engineering capability in a real-world scenario."
            }
        ]
    },

    "software_engineering": {
        "expert_name": "Senior Software Engineer & Technical Mentor",
        "intro": "Welcome to the Software Engineering track! Beyond just writing code — we'll cover clean code principles, design patterns, system design, testing, Git workflows, and how to work like a professional engineer.",
        "levels": [
            {
                "name": "Level 1: Clean Code & Git Mastery",
                "description": "Naming conventions, functions, comments, code smells, refactoring, Git branching strategies, pull requests, and code review etiquette.",
                "importance": "Clean, versioned code is the baseline expectation at every professional software company."
            },
            {
                "name": "Level 2: Software Design Principles",
                "description": "SOLID principles, DRY/KISS/YAGNI, coupling vs cohesion, layered architecture, dependency injection, and interface design.",
                "importance": "These principles determine whether your codebase grows cleanly or collapses under its own complexity."
            },
            {
                "name": "Level 3: Design Patterns",
                "description": "Creational (Factory, Singleton, Builder), Structural (Adapter, Decorator, Facade), and Behavioural (Observer, Strategy, Command) patterns with real examples.",
                "importance": "Design patterns are a shared vocabulary for solving recurring architectural problems."
            },
            {
                "name": "Level 4: Testing, APIs & System Design",
                "description": "Unit/integration/e2e testing, TDD, REST API design, OpenAPI specs, basic system design (load balancing, caching, databases, queues).",
                "importance": "Tested, well-designed systems are what distinguishes senior from junior engineers."
            },
            {
                "name": "Level 5: Engineering Capstone",
                "description": "Design, build, test, and document a production-quality system — with architecture decision records, full test suite, and deployment.",
                "importance": "Proves senior-level software engineering thinking and execution."
            }
        ]
    },

    "mobile_dev": {
        "expert_name": "Senior Mobile Developer & Mentor",
        "intro": "Welcome to the Mobile Development track! From UI components and navigation to state management, APIs, and publishing to the App Store and Play Store.",
        "levels": [
            {"name": "Level 1: Mobile Fundamentals & UI Basics", "description": "Mobile app architecture, layouts, navigation, components, and user input handling.", "importance": "Every mobile feature starts with understanding how mobile UIs work."},
            {"name": "Level 2: State Management & Data", "description": "Local state, global state (Redux/Provider/Riverpod), async data fetching, REST APIs, and local storage.", "importance": "Apps without proper state management break at scale."},
            {"name": "Level 3: Advanced UI & Animations", "description": "Custom animations, transitions, gestures, accessibility, and responsive layouts.", "importance": "Great mobile UX requires fluid, accessible interactions."},
            {"name": "Level 4: Native Features & Testing", "description": "Camera, GPS, push notifications, background tasks, unit tests, and widget tests.", "importance": "Native integration and testing separate hobby projects from professional apps."},
            {"name": "Level 5: Mobile Capstone & Deployment", "description": "Build, test, and publish a complete app to App Store/Play Store with CI/CD.", "importance": "A shipped, published app is the most powerful portfolio piece a mobile developer can have."}
        ]
    },

    "robotics": {
        "expert_name": "Senior Robotics & Embedded Systems Engineer",
        "intro": "Welcome to the Robotics & Embedded Systems track! From electronics fundamentals and microcontrollers to sensors, actuators, control systems, and autonomous robot programming.",
        "levels": [
            {"name": "Level 1: Electronics & Robotics Fundamentals", "description": "Voltage, current, resistance, Ohm's law, circuits, breadboarding, and how microcontrollers work.", "importance": "Every robot is built on basic electronics — without this, nothing else makes sense."},
            {"name": "Level 2: Microcontrollers & Programming", "description": "Arduino/Raspberry Pi setup, GPIO pins, digital/analog I/O, PWM, and embedded C/Python scripting.", "importance": "Microcontrollers are the brain of every embedded system and robot."},
            {"name": "Level 3: Sensors, Actuators & Control", "description": "Ultrasonic, IR, IMU sensors, servo/DC/stepper motors, PID control, and basic feedback loops.", "importance": "Sensors let robots perceive; actuators let them act; control systems make them precise."},
            {"name": "Level 4: Robot Operating System (ROS) & Navigation", "description": "ROS fundamentals, nodes, topics, SLAM, path planning, and simulating robots in Gazebo.", "importance": "ROS is the standard framework for building professional robotic systems."},
            {"name": "Level 5: Robotics Capstone Project", "description": "Design, build, and program a complete autonomous robot or simulation with sensors, control, and navigation.", "importance": "A working robot project is the ultimate proof of robotics engineering skill."}
        ]
    },

    "general_tech": {
        "expert_name": "Technology Expert & Mentor",
        "intro": "Welcome! I'm your personal technology mentor. We'll build genuine, structured competence in your chosen area — one concept at a time, with hands-on practice and real projects.",
        "levels": [
            {"name": "Level 1: Core Foundations", "description": "Fundamental concepts, mental models, and how the technology works from the ground up.", "importance": "Strong foundations make everything that comes next faster and easier."},
            {"name": "Level 2: Tools, Syntax & First Programs", "description": "Setting up a working environment, learning core syntax, and writing your first functional programs.", "importance": "Practical hands-on experience from day one."},
            {"name": "Level 3: Intermediate Patterns & Real Projects", "description": "Handling edge cases, using libraries, and building real projects that solve actual problems.", "importance": "Moves you from tutorial-following to independent building."},
            {"name": "Level 4: Advanced Techniques & Architecture", "description": "Designing robust, modular systems, performance optimisation, and best practices.", "importance": "Required for production-grade, professional work."},
            {"name": "Level 5: Capstone & Portfolio Project", "description": "Build a complete, polished project showcasing end-to-end mastery.", "importance": "Demonstrates job-readiness to employers."}
        ]
    },

    "ui_ux": {
        "expert_name": "Principal UI/UX Designer & Product Design Mentor",
        "intro": "Welcome to the UI/UX Product Design track! I will guide you through user research, wireframing, typography, design systems, Figma interactive prototyping, and portfolio case studies.",
        "levels": [
            {
                "name": "Level 1: Design Thinking & UX Research",
                "description": "User interviews, empathy mapping, personas, journey maps, problem statements, and qualitative research.",
                "importance": "Great design starts with understanding the user's real problem before touching Figma."
            },
            {
                "name": "Level 2: Information Architecture & Wireframing",
                "description": "Site mapping, user flows, content hierarchy, low-fidelity sketching, and digital wireframing.",
                "importance": "Creates clear, intuitive navigation and structure for users."
            },
            {
                "name": "Level 3: Visual Design Principles, Typography & Color",
                "description": "Visual hierarchy, typography scales, 8pt spacing grids, accessible color palettes (WCAG), and modern UI aesthetics.",
                "importance": "Turns wireframes into polished, accessible, and delightful interfaces."
            },
            {
                "name": "Level 4: Figma Mastery & Interactive Prototyping",
                "description": "Auto Layout, component variants, smart animate, micro-interactions, and high-fidelity clickable prototypes.",
                "importance": "Brings static mockups to life for usability testing and stakeholder validation."
            },
            {
                "name": "Level 5: Design Systems & Developer Handoff",
                "description": "Design tokens, shared component libraries, documentation, accessibility compliance, and design-to-code handoff.",
                "importance": "Ensures design consistency across large multi-disciplinary product teams."
            },
            {
                "name": "Level 6: UI/UX Capstone Portfolio Case Study",
                "description": "Complete end-to-end product design case study: from initial user research to a polished, tested, interactive prototype.",
                "importance": "The definitive portfolio asset that gets you hired as a product designer."
            }
        ]
    }
}


# =============================================================================
# Replace the legacy course outlines with the reviewed 12-level course maps.
CURRICULA.update(RESTRUCTURED_CURRICULA)


# SKILL MAP CONCEPTS — per domain, per level
# =============================================================================

SKILL_MAPS = {

    "python": {
        "level 1": [
            {"name": "What is Python & Why It's Used Everywhere", "description": "Python's history, use cases (web, AI, automation, data), and installing Python + VS Code.", "estimated_time": "10 min"},
            {"name": "Variables, Data Types & Type Checking", "description": "int, float, str, bool, NoneType, type(), and dynamic typing.", "estimated_time": "15 min"},
            {"name": "String Operations & Formatting", "description": "String methods, slicing, f-strings, and .format().", "estimated_time": "15 min"},
            {"name": "Conditionals: if, elif, else", "description": "Boolean logic, comparison operators, and writing decision-making code.", "estimated_time": "15 min"},
            {"name": "Loops: for & while", "description": "Iterating over ranges, lists, and strings; break, continue, and loop patterns.", "estimated_time": "20 min"},
        ],
        "level 2": [
            {"name": "Defining & Calling Functions", "description": "def, parameters, return values, default arguments, and *args/**kwargs.", "estimated_time": "20 min"},
            {"name": "Lists: Creation, Indexing & Methods", "description": "append, insert, pop, slicing, and list comprehensions.", "estimated_time": "20 min"},
            {"name": "Dictionaries & Sets", "description": "Key-value pairs, dict methods, sets, and when to use each.", "estimated_time": "20 min"},
            {"name": "Modules & Importing", "description": "import, from...import, stdlib modules (os, math, random, datetime).", "estimated_time": "15 min"},
            {"name": "Lambda Functions & Map/Filter", "description": "Anonymous functions, map(), filter(), and functional patterns.", "estimated_time": "15 min"},
        ],
        "level 3": [
            {"name": "Classes & Objects", "description": "class keyword, __init__, instance methods, self, and creating objects.", "estimated_time": "25 min"},
            {"name": "Inheritance & Polymorphism", "description": "super(), method overriding, and writing clean class hierarchies.", "estimated_time": "20 min"},
            {"name": "Exception Handling", "description": "try/except/finally, raising exceptions, and custom exception classes.", "estimated_time": "20 min"},
            {"name": "File I/O & JSON", "description": "Reading/writing text files, working with JSON (json.load/dump).", "estimated_time": "20 min"},
            {"name": "Magic Methods & Dunder Protocol", "description": "__str__, __repr__, __len__, __eq__, and operator overloading.", "estimated_time": "15 min"},
        ],
        "level 4": [
            {"name": "Decorators", "description": "Function decorators, @wraps, and practical use cases (logging, timing).", "estimated_time": "20 min"},
            {"name": "Generators & Iterators", "description": "yield, generator expressions, and memory-efficient iteration.", "estimated_time": "20 min"},
            {"name": "Async Programming with asyncio", "description": "async def, await, event loop, and async HTTP requests.", "estimated_time": "25 min"},
            {"name": "Testing with pytest", "description": "Writing unit tests, fixtures, parametrize, and test coverage.", "estimated_time": "25 min"},
            {"name": "Virtual Environments & pip", "description": "venv, requirements.txt, pyproject.toml, and dependency management.", "estimated_time": "15 min"},
        ],
    },

    "web_dev": {
        "level 1": [
            {"name": "HTML Document Structure & Semantic Elements", "description": "DOCTYPE, head/body, semantic tags (header, nav, main, article, footer).", "estimated_time": "15 min"},
            {"name": "CSS Selectors, Specificity & the Box Model", "description": "Selectors, classes, IDs, margin/padding/border, and display types.", "estimated_time": "20 min"},
            {"name": "Flexbox Layout", "description": "flex container/item, justify-content, align-items, flex-wrap, and gap.", "estimated_time": "20 min"},
            {"name": "CSS Grid Layout", "description": "Grid container, template-columns/rows, areas, and responsive grids.", "estimated_time": "20 min"},
            {"name": "Responsive Design & Media Queries", "description": "Mobile-first design, breakpoints, viewport meta tag, and fluid typography.", "estimated_time": "20 min"},
        ],
        "level 2": [
            {"name": "JavaScript DOM Manipulation", "description": "querySelector, createElement, innerHTML, classList, and event listeners.", "estimated_time": "20 min"},
            {"name": "Events & User Interaction", "description": "click, submit, input events, event delegation, and preventing defaults.", "estimated_time": "20 min"},
            {"name": "Fetch API & REST Consumption", "description": "fetch(), async/await, handling JSON responses, and displaying API data.", "estimated_time": "25 min"},
            {"name": "Local Storage & Session Storage", "description": "Storing, reading, and deleting browser-side data with Web Storage API.", "estimated_time": "15 min"},
            {"name": "Form Validation & UX Feedback", "description": "HTML5 validation, custom validation with JS, and feedback patterns.", "estimated_time": "15 min"},
        ],
        "level 3": [
            {"name": "React Components & JSX", "description": "Functional components, JSX syntax, props, and component composition.", "estimated_time": "25 min"},
            {"name": "State & the useState Hook", "description": "Managing dynamic data inside components with useState.", "estimated_time": "20 min"},
            {"name": "useEffect & Side Effects", "description": "Fetching data on mount, cleanup functions, and dependency arrays.", "estimated_time": "20 min"},
            {"name": "React Router — Navigation & URL Params", "description": "BrowserRouter, Route, Link, useParams, and nested routes.", "estimated_time": "20 min"},
            {"name": "Context API & Global State", "description": "createContext, useContext, and avoiding prop-drilling.", "estimated_time": "20 min"},
        ],
        "level 4": [
            {"name": "Node.js Runtime & npm Ecosystem", "description": "How Node.js works, the event loop, npm packages, and package.json.", "estimated_time": "20 min"},
            {"name": "Express.js REST APIs", "description": "Routes, middleware, request/response, error handling, and JSON APIs.", "estimated_time": "25 min"},
            {"name": "Authentication — JWT & Sessions", "description": "JWT tokens, signing/verifying, session cookies, and security best practices.", "estimated_time": "25 min"},
            {"name": "Database Integration (PostgreSQL/SQLite)", "description": "SQL queries from Node, ORMs (Prisma/Sequelize), and migrations.", "estimated_time": "25 min"},
            {"name": "API Security & Rate Limiting", "description": "CORS, helmet, rate-limiting, input validation, and SQL injection prevention.", "estimated_time": "20 min"},
        ],
    },

    "javascript": {
        "level 1": [
            {"name": "Variables: var, let, const & Scope", "description": "Differences between var/let/const, hoisting, block scope, and TDZ.", "estimated_time": "15 min"},
            {"name": "Data Types & Type Coercion", "description": "Primitive types, typeof, == vs ===, and implicit type conversion.", "estimated_time": "15 min"},
            {"name": "Functions & Closures", "description": "Function declarations vs expressions, closures, and the scope chain.", "estimated_time": "20 min"},
            {"name": "The Event Loop & Call Stack", "description": "How JavaScript runs single-threaded, the call stack, and async queue.", "estimated_time": "20 min"},
            {"name": "Objects & Prototypal Inheritance", "description": "Object literals, this keyword, prototype chain, and Object methods.", "estimated_time": "20 min"},
        ],
        "level 2": [
            {"name": "Arrow Functions & Lexical this", "description": "Arrow syntax, lexical this binding, and when NOT to use arrow functions.", "estimated_time": "15 min"},
            {"name": "Destructuring, Spread & Rest", "description": "Array/object destructuring, spread operator, and rest parameters.", "estimated_time": "15 min"},
            {"name": "Promises & Async/Await", "description": "Promise chain, .then/.catch, async functions, and error handling.", "estimated_time": "20 min"},
            {"name": "ES Modules: import & export", "description": "Named/default exports, module resolution, and circular dependencies.", "estimated_time": "15 min"},
            {"name": "Array Methods: map, filter, reduce", "description": "Functional array transformation patterns with real examples.", "estimated_time": "20 min"},
        ],
    },

    "data_analytics": {
        "level 1": [
            {"name": "What Data Analysis Is & Solving Business Problems", "description": "How analysts convert raw questions into measurable insights.", "estimated_time": "12 min"},
            {"name": "Structured vs Unstructured & Quantitative vs Qualitative Data", "description": "Differentiating tables and numbers from text and logs.", "estimated_time": "12 min"},
            {"name": "Rows, Columns, Records, Fields & Relational Tables", "description": "Mastering tabular anatomy and relational schemas.", "estimated_time": "15 min"},
            {"name": "KPIs, Metrics, Dimensions & Business Questions", "description": "Distinguishing measurable numbers from sliceable attributes.", "estimated_time": "15 min"},
            {"name": "The End-to-End Data Analysis Lifecycle & Ethics", "description": "From ingestion and cleaning to storytelling and privacy.", "estimated_time": "15 min"},
        ],
        "level 2": [
            {"name": "Workbooks, Cell Ranges & Absolute References ($A$1)", "description": "Grid navigation, data types, and locking cell references.", "estimated_time": "15 min"},
            {"name": "Core Formulas: SUM, AVERAGE, COUNT, MIN, MAX", "description": "Essential aggregation building blocks.", "estimated_time": "12 min"},
            {"name": "Logical Formulas: IF, IFS, AND, OR, IFERROR", "description": "Branching calculation logic and error catching.", "estimated_time": "15 min"},
            {"name": "Multi-Condition Analytics: SUMIFS, COUNTIFS, AVERAGEIFS", "description": "Segment calculations with multiple criteria.", "estimated_time": "15 min"},
            {"name": "Text Cleaning: TRIM, LEFT, RIGHT, MID, CONCAT", "description": "Cleaning messy data entries and reformatting strings.", "estimated_time": "15 min"},
            {"name": "Advanced Lookups: XLOOKUP & INDEX/MATCH", "description": "Connecting datasets across tabs without breakage.", "estimated_time": "18 min"},
            {"name": "Pivot Tables, Slicers & Interactive Dashboards", "description": "Grouping thousands of rows into dynamic cross-tabs.", "estimated_time": "20 min"},
        ],
        "level 3": [
            {"name": "Measures of Central Tendency: Mean, Median, Mode", "description": "Why the median protects you from outlier distortions.", "estimated_time": "15 min"},
            {"name": "Variance, Standard Deviation & Spread", "description": "Measuring consistency, risk, and volatility.", "estimated_time": "15 min"},
            {"name": "Distributions, Outliers & Normal Curves", "description": "Detecting anomalies and 3-sigma thresholds.", "estimated_time": "15 min"},
            {"name": "Correlation vs Causation", "description": "Confounders, spurious correlations, and ethical reporting.", "estimated_time": "15 min"},
            {"name": "A/B Testing & Hypothesis Testing", "description": "P-values, control vs variant, and statistical significance.", "estimated_time": "18 min"},
        ],
        "level 4": [
            {"name": "Relational Tables, Primary & Foreign Keys", "description": "How databases structure one-to-many records.", "estimated_time": "15 min"},
            {"name": "Core Queries: SELECT, FROM, WHERE, ORDER BY", "description": "Extracting clean slices of data with filters.", "estimated_time": "15 min"},
            {"name": "Aggregations: GROUP BY & HAVING", "description": "Sums, counts, and averages per segment.", "estimated_time": "15 min"},
            {"name": "Multi-Table JOINs: INNER, LEFT, RIGHT", "description": "Combining tables into unified result sets.", "estimated_time": "18 min"},
            {"name": "CASE WHEN & NULL Handling (COALESCE)", "description": "Custom business flags and preventing NULL bugs.", "estimated_time": "15 min"},
            {"name": "CTEs & Window Functions (ROW_NUMBER, RANK, LAG)", "description": "Running totals, ranking, and cohort analytics.", "estimated_time": "20 min"},
        ],
    },

    "ai_ml": {
        "level 1": [
            {"name": "What is AI vs ML vs Deep Learning?", "description": "The hierarchy: AI → ML → DL and where each applies.", "estimated_time": "15 min"},
            {"name": "Supervised vs Unsupervised vs Reinforcement Learning", "description": "Types of learning problems with real-world examples.", "estimated_time": "15 min"},
            {"name": "Vectors, Matrices & Linear Algebra Essentials", "description": "Dot products, matrix multiplication, and why they matter in ML.", "estimated_time": "20 min"},
            {"name": "Probability Fundamentals for ML", "description": "Probability, conditional probability, Bayes' theorem, and distributions.", "estimated_time": "20 min"},
            {"name": "The ML Workflow: Data → Model → Evaluate → Deploy", "description": "End-to-end pipeline from raw data to production prediction.", "estimated_time": "15 min"},
        ],
        "level 2": [
            {"name": "Linear Regression — Prediction with Numbers", "description": "Cost function, gradient descent, and fitting a line to data.", "estimated_time": "25 min"},
            {"name": "Logistic Regression — Binary Classification", "description": "Sigmoid function, decision boundary, and log loss.", "estimated_time": "20 min"},
            {"name": "Decision Trees & Random Forests", "description": "Entropy, information gain, bagging, and feature importance.", "estimated_time": "25 min"},
            {"name": "Model Evaluation: Accuracy, Precision, Recall, F1, AUC", "description": "Choosing the right metric for your problem type.", "estimated_time": "20 min"},
            {"name": "Scikit-Learn Pipeline Pattern", "description": "fit/predict API, train-test split, cross-validation, and grid search.", "estimated_time": "25 min"},
        ],
        "level 3": [
            {"name": "Neural Network Architecture & Forward Pass", "description": "Layers, neurons, weights, biases, and computing predictions.", "estimated_time": "25 min"},
            {"name": "Backpropagation & Gradient Descent", "description": "How neural networks learn from error signals.", "estimated_time": "25 min"},
            {"name": "Convolutional Neural Networks (CNNs)", "description": "Filters, feature maps, pooling, and image classification.", "estimated_time": "25 min"},
            {"name": "Recurrent Networks & LSTMs", "description": "Sequence modelling, vanishing gradients, and LSTM gates.", "estimated_time": "25 min"},
            {"name": "Regularisation: Dropout, BatchNorm & Early Stopping", "description": "Preventing overfitting in deep networks.", "estimated_time": "20 min"},
        ],
    },

    "cybersecurity": {
        "level 1": [
            {"name": "Networking Layers for Defenders", "description": "Understand network layers and how defenders categorize supplied local logs.", "estimated_time": "20 min"},
            {"name": "TCP/IP, Ports & Protocols (HTTP, DNS, FTP, SSH)", "description": "How data travels across the internet and what each protocol does.", "estimated_time": "20 min"},
            {"name": "IP Addressing & Subnetting", "description": "IPv4/IPv6, CIDR notation, subnetting, and NAT.", "estimated_time": "20 min"},
            {"name": "Firewalls, VPNs & Network Security Devices", "description": "Stateful inspection, ACLs, VPN tunnels, and proxy servers.", "estimated_time": "15 min"},
            {"name": "The CIA Triad: Confidentiality, Integrity, Availability", "description": "Core defensive security principles and how controls support each.", "estimated_time": "15 min"},
        ],
        "level 2": [
            {"name": "Linux File System & Permissions", "description": "File hierarchy, chmod, chown, SUID/SGID, and sticky bit.", "estimated_time": "20 min"},
            {"name": "Defensive Log Review", "description": "Review supplied local logs and identify events for the approved incident playbook.", "estimated_time": "25 min"},
            {"name": "Process Management & Log Analysis", "description": "Review supplied local process and event summaries for defensive monitoring.", "estimated_time": "20 min"},
            {"name": "SSH, Key Management & Hardening", "description": "SSH key pairs, config hardening, port forwarding, and fail2ban.", "estimated_time": "20 min"},
            {"name": "Provided Packet Capture Review", "description": "Interpret only a supplied local training packet capture.", "estimated_time": "25 min"},
        ],
        "level 3": [
            {"name": "Threat Modeling & Defensive Review", "description": "Map assets, trust boundaries, risks, and mitigations for a fictional system.", "estimated_time": "25 min"},
            {"name": "Security Finding Remediation", "description": "Review findings supplied from a local training app and prioritize safe fixes.", "estimated_time": "25 min"},
            {"name": "OWASP Risks & Secure Coding", "description": "Recognize common web risks and apply preventive coding controls.", "estimated_time": "30 min"},
            {"name": "Local Lab Configuration Review", "description": "Review a deliberately vulnerable local app configuration and document remediations.", "estimated_time": "30 min"},
            {"name": "Incident Response & Recovery", "description": "Use supplied local logs to document detection, containment, and recovery.", "estimated_time": "25 min"},
        ],
    },

    "dsa": {
        "level 1": [
            {"name": "Big-O Notation & Time/Space Complexity", "description": "O(1), O(n), O(n²), O(log n) with real algorithm examples.", "estimated_time": "20 min"},
            {"name": "Arrays — Operations & the Two-Pointer Pattern", "description": "Indexing, searching, two-pointer technique, and sliding window.", "estimated_time": "25 min"},
            {"name": "Hash Maps & Sets — O(1) Lookups", "description": "Hash function, collision resolution, and frequency counting patterns.", "estimated_time": "25 min"},
            {"name": "Strings — Manipulation & Pattern Matching", "description": "Reverse, palindrome check, anagram detection, and substring problems.", "estimated_time": "20 min"},
            {"name": "Sorting Algorithms — Bubble, Merge, Quick Sort", "description": "Comparison-based sorts with time complexity analysis.", "estimated_time": "25 min"},
        ],
        "level 2": [
            {"name": "Linked Lists — Singly & Doubly", "description": "Node structure, traversal, insertion/deletion, and reversing.", "estimated_time": "25 min"},
            {"name": "Fast & Slow Pointer — Cycle Detection", "description": "Floyd's algorithm and finding the midpoint.", "estimated_time": "20 min"},
            {"name": "Stacks — LIFO & Monotonic Stack Pattern", "description": "Call stack simulation, balanced parentheses, and next greater element.", "estimated_time": "25 min"},
            {"name": "Queues, Deques & BFS Foundation", "description": "FIFO queue, deque, and breadth-first search pattern.", "estimated_time": "25 min"},
        ],
    },

    "sql_databases": {
        "level 1": [
            {"name": "Relational Model: Tables, Rows & Columns", "description": "What a relational database is and how data is organised.", "estimated_time": "15 min"},
            {"name": "SELECT Queries — Retrieving Data", "description": "SELECT, FROM, WHERE, ORDER BY, LIMIT, and column aliasing.", "estimated_time": "15 min"},
            {"name": "Filtering: WHERE Clause & Boolean Logic", "description": "AND, OR, NOT, IN, BETWEEN, LIKE, and IS NULL.", "estimated_time": "15 min"},
            {"name": "INSERT, UPDATE & DELETE — Modifying Data", "description": "Adding rows, updating values, and deleting records safely.", "estimated_time": "15 min"},
            {"name": "Primary Keys, Foreign Keys & Constraints", "description": "Data integrity, referential integrity, and UNIQUE constraints.", "estimated_time": "15 min"},
        ],
        "level 2": [
            {"name": "Aggregate Functions: SUM, COUNT, AVG, MIN, MAX", "description": "Summarising data across groups of rows.", "estimated_time": "15 min"},
            {"name": "GROUP BY & HAVING", "description": "Grouping rows, post-aggregation filtering, and common mistakes.", "estimated_time": "15 min"},
            {"name": "INNER JOIN — Matching Rows Across Tables", "description": "Combining related tables on foreign keys.", "estimated_time": "20 min"},
            {"name": "LEFT JOIN, RIGHT JOIN & FULL OUTER JOIN", "description": "Preserving unmatched rows and handling NULLs.", "estimated_time": "20 min"},
            {"name": "Subqueries & Correlated Subqueries", "description": "Nested queries, IN/EXISTS, and when to use joins instead.", "estimated_time": "20 min"},
        ],
    },

    "cloud_devops": {
        "level 1": [
            {"name": "Cloud Computing Fundamentals (IaaS, PaaS, SaaS)", "description": "What the cloud is, why companies use it, and the 3 service models.", "estimated_time": "15 min"},
            {"name": "Linux Command Line Essentials", "description": "Navigation, file management, permissions, and essential commands.", "estimated_time": "20 min"},
            {"name": "Bash Scripting for Automation", "description": "Variables, conditionals, loops, and writing automation scripts.", "estimated_time": "25 min"},
            {"name": "Networking for DevOps: DNS, HTTP, Ports", "description": "How services communicate and what engineers must know.", "estimated_time": "20 min"},
            {"name": "AWS Core Services: EC2, S3, IAM, VPC", "description": "Launching instances, storing files, managing users, and networking.", "estimated_time": "25 min"},
        ],
        "level 2": [
            {"name": "What is Docker & Why Containers?", "description": "Container vs VM, Docker architecture, and key benefits.", "estimated_time": "15 min"},
            {"name": "Writing Dockerfiles", "description": "FROM, RUN, COPY, EXPOSE, CMD, and best practices for small images.", "estimated_time": "25 min"},
            {"name": "Docker Compose — Multi-Container Apps", "description": "services, volumes, networks, and docker-compose.yml syntax.", "estimated_time": "25 min"},
            {"name": "Container Registries: Docker Hub & ECR", "description": "Pushing, pulling, and tagging images for deployment.", "estimated_time": "15 min"},
        ],
    },

    "software_engineering": {
        "level 1": [
            {"name": "Git Fundamentals — Commits, Branches & Merging", "description": "init, add, commit, push, pull, branch, merge, and resolving conflicts.", "estimated_time": "20 min"},
            {"name": "Git Workflows — GitHub Flow & Feature Branches", "description": "Pull requests, code review, branch naming, and trunk-based development.", "estimated_time": "20 min"},
            {"name": "Naming Things Right — Clean Code Principles", "description": "Meaningful names, small functions, avoiding magic numbers, and comments.", "estimated_time": "20 min"},
            {"name": "Code Smells & Refactoring", "description": "Long methods, duplicated code, and systematic refactoring techniques.", "estimated_time": "20 min"},
            {"name": "Reading & Understanding Existing Codebases", "description": "How to navigate unfamiliar code, trace bugs, and make safe changes.", "estimated_time": "20 min"},
        ],
        "level 2": [
            {"name": "SOLID Principles", "description": "Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion.", "estimated_time": "30 min"},
            {"name": "DRY, KISS & YAGNI", "description": "Don't Repeat Yourself, Keep It Simple, and avoiding over-engineering.", "estimated_time": "15 min"},
            {"name": "Coupling & Cohesion", "description": "Why low coupling and high cohesion lead to maintainable systems.", "estimated_time": "20 min"},
            {"name": "Dependency Injection", "description": "Constructor injection, inversion of control, and testability.", "estimated_time": "20 min"},
        ],
    },
    "python": {
        "level 5": [
            {"name": "Advanced Metaprogramming & Decorators", "description": "Creating higher-order functions, class decorators, and runtime code generation.", "estimated_time": "25 min"},
            {"name": "Concurrency with threading & multiprocessing", "description": "Thread pools, process pools, GIL considerations, and inter-process communication.", "estimated_time": "30 min"},
            {"name": "AsyncIO Advanced Patterns", "description": "Custom event loops, async generators, and performance tuning.", "estimated_time": "25 min"},
            {"name": "Packaging & Distribution", "description": "Building wheels, using setuptools, and publishing to PyPI.", "estimated_time": "20 min"},
            {"name": "Security Best Practices", "description": "Input sanitisation, secrets management, and protecting against injection attacks.", "estimated_time": "20 min"}
        ]
    },
}


def get_skill_map_concepts(skill_name: str, domain_key: str, level: str) -> list:
    """Return concept list for a given domain and level, prioritizing the skill name."""
    sn = (skill_name or "").lower()

    if domain_key in RESTRUCTURED_CURRICULA:
        import re

        level_match = re.search(r"\blevel\s+(\d+)\b", sn)
        if level_match:
            course_level = int(level_match.group(1))
            levels = RESTRUCTURED_CURRICULA[domain_key]["levels"]
            if 1 <= course_level <= len(levels):
                level_data = levels[course_level - 1]
                return [
                    {
                        "name": topic,
                        "description": f"Learn and practice {topic.lower()} as part of {level_data['name']}.",
                        "estimated_time": "15 min",
                    }
                    for topic in level_data["concepts"]
                ]

    # 1. Match by specific skill keywords across all domains
    if "web fundamentals" in sn or "how the web works" in sn:
        return [
            {"name": "How the Internet & Web Works (DNS, HTTP/HTTPS)", "description": "Domain resolution, client-server model, and data packets.", "estimated_time": "15 min"},
            {"name": "Client-Server Architecture & Request-Response", "description": "How browsers communicate with web servers via HTTP.", "estimated_time": "15 min"},
            {"name": "Browser Rendering & Critical Rendering Path", "description": "DOM, CSSOM, render tree, layout, and paint cycle.", "estimated_time": "15 min"},
            {"name": "Developer Tools & Network Inspection", "description": "Inspecting elements, console logging, network waterfall.", "estimated_time": "15 min"},
        ]
    if "html" in sn:
        return [
            {"name": "Introduction to HTML & Document Structure", "description": "DOCTYPE, html, head, body, and basic document tags.", "estimated_time": "15 min"},
            {"name": "Semantic HTML5 Tags & Structural Layout", "description": "header, nav, main, section, article, aside, footer.", "estimated_time": "15 min"},
            {"name": "Headings, Paragraphs, Links & Media Elements", "description": "h1-h6 hierarchy, p tags, img with alt, and a tags.", "estimated_time": "15 min"},
            {"name": "HTML Forms, Inputs & Client Validation", "description": "form, input types, labels, required attributes, submit.", "estimated_time": "20 min"},
            {"name": "Accessibility (a11y), ARIA Roles & SEO", "description": "Screen readers, semantic landmark roles, and meta SEO tags.", "estimated_time": "15 min"},
        ]
    if "css" in sn:
        return [
            {"name": "CSS Selectors, Specificity & The Cascade", "description": "Classes, IDs, element selectors, and specificity rules.", "estimated_time": "15 min"},
            {"name": "The CSS Box Model: Margin, Border, Padding", "description": "Content box vs border box, sizing, and spacing calculations.", "estimated_time": "15 min"},
            {"name": "Flexbox Layout & Alignment", "description": "justify-content, align-items, flex-direction, and flex-wrap.", "estimated_time": "20 min"},
            {"name": "CSS Grid: 2D Layouts & Responsive Grids", "description": "grid-template-columns, fr units, repeat, and gap.", "estimated_time": "20 min"},
            {"name": "Media Queries & Mobile-First Responsive Design", "description": "Breakpoints, fluid typography, and responsive container queries.", "estimated_time": "20 min"},
        ]
    if "javascript" in sn or "js " in sn or sn.endswith(" js"):
        return [
            {"name": "Variables (let, const), Types & Operators", "description": "Primitive types, type coercion, arithmetic and logical operators.", "estimated_time": "15 min"},
            {"name": "Functions, Scope, Closures & Arrow Syntax", "description": "Function declarations, parameters, lexical scope, and closures.", "estimated_time": "20 min"},
            {"name": "DOM Manipulation & Event Handling", "description": "querySelector, addEventListener, bubbling, and dynamic DOM updates.", "estimated_time": "20 min"},
            {"name": "Asynchronous JavaScript & Promises", "description": "The event loop, callback hell, and Promise chaining (.then/.catch).", "estimated_time": "20 min"},
            {"name": "Async/Await, Fetch API & JSON Handling", "description": "Modern async/await syntax, calling REST endpoints, and parsing JSON.", "estimated_time": "25 min"},
        ]
    if "git" in sn or "github" in sn:
        return [
            {"name": "Version Control Basics & Git Repositories", "description": "git init, git clone, tracking files, and .gitignore.", "estimated_time": "15 min"},
            {"name": "Staging, Committing & Viewing History", "description": "git add, git commit -m, git status, and git log --oneline.", "estimated_time": "15 min"},
            {"name": "Git Branching Strategies & Feature Branches", "description": "git branch, git checkout, git switch, and isolated feature work.", "estimated_time": "20 min"},
            {"name": "Merging, Rebasing & Resolving Merge Conflicts", "description": "Fast-forward merges, merge commits, rebase, and conflict markers.", "estimated_time": "25 min"},
            {"name": "Remote Repositories & GitHub Collaboration", "description": "git remote, git push, git pull, pull requests, and code review.", "estimated_time": "20 min"},
        ]
    if "react" in sn or "frontend framework" in sn:
        return [
            {"name": "React Components & JSX Syntax", "description": "Functional components, JSX rules, and component composition.", "estimated_time": "20 min"},
            {"name": "State Management with the useState Hook", "description": "Component state, immutable updates, and reactive re-renders.", "estimated_time": "20 min"},
            {"name": "Side Effects & Lifecycle with useEffect", "description": "API fetching, event listeners, cleanup, and dependency arrays.", "estimated_time": "25 min"},
            {"name": "Client Routing with React Router", "description": "BrowserRouter, Routes, Route, Link, and useParams.", "estimated_time": "20 min"},
            {"name": "Global State with Context API", "description": "createContext, Provider, useContext, and avoiding prop drilling.", "estimated_time": "20 min"},
        ]
    if "backend" in sn or "server architecture" in sn:
        return [
            {"name": "Server Architecture & Node/Django Runtimes", "description": "Event-driven vs threaded servers, event loop, and runtime setup.", "estimated_time": "20 min"},
            {"name": "Routing, Endpoints & Request/Response Lifecycle", "description": "Handling GET, POST, PUT, DELETE, and URL parameters.", "estimated_time": "20 min"},
            {"name": "Middleware Architecture & Request Validation", "description": "Chaining middleware, body parsing, CORS, and logging.", "estimated_time": "20 min"},
            {"name": "Controller-Service Layer Architecture", "description": "Separating business logic, controllers, and database access.", "estimated_time": "25 min"},
            {"name": "Error Handling, Status Codes & Server Logging", "description": "Centralized error middleware, logging, and graceful shutdowns.", "estimated_time": "20 min"},
        ]
    if "database" in sn or "sql" in sn:
        return [
            {"name": "Relational Tables, Data Types & Primary Keys", "description": "Designing normalized tables and defining constraints.", "estimated_time": "15 min"},
            {"name": "SELECT Queries, Filtering (WHERE) & Sorting", "description": "Extracting clean data with conditions and ordering.", "estimated_time": "15 min"},
            {"name": "Aggregations & Grouping (GROUP BY, HAVING)", "description": "COUNT, SUM, AVG, MIN, MAX grouped by categories.", "estimated_time": "15 min"},
            {"name": "Relational Joins: INNER, LEFT & RIGHT JOIN", "description": "Connecting related tables through foreign key relationships.", "estimated_time": "20 min"},
            {"name": "Database Indexes, Transactions (ACID) & ORM Basics", "description": "Query performance, B-Trees, transaction safety, and ORM models.", "estimated_time": "20 min"},
        ]
    if "api" in sn or "rest" in sn:
        return [
            {"name": "REST Architecture Principles & Resource Design", "description": "Statelessness, resource URIs, and standard HTTP verbs.", "estimated_time": "15 min"},
            {"name": "HTTP Status Codes & Response Formatting", "description": "200 OK, 201 Created, 400 Bad Request, 401/403, 404, 500.", "estimated_time": "15 min"},
            {"name": "JSON Serialization, Query Params & Pagination", "description": "Payload formatting, limit/offset, page/pageSize, and sorting.", "estimated_time": "20 min"},
            {"name": "API Documentation with OpenAPI / Swagger", "description": "Defining endpoints, schemas, request bodies, and test clients.", "estimated_time": "15 min"},
            {"name": "Consuming APIs & Error Resilience", "description": "Retries, timeouts, error boundary fallbacks, and caching.", "estimated_time": "20 min"},
        ]
    if "auth" in sn or "security" in sn:
        return [
            {"name": "Authentication vs Authorization & Password Hashing", "description": "Hashing with bcrypt/argon2, salt, and password storage.", "estimated_time": "20 min"},
            {"name": "Stateless JWT Tokens vs Stateful Sessions", "description": "JWT structure (header.payload.signature), expiration, and cookies.", "estimated_time": "25 min"},
            {"name": "CORS (Cross-Origin Resource Sharing) & CSRF", "description": "Origin headers, preflight OPTIONS, and CSRF token defenses.", "estimated_time": "20 min"},
            {"name": "Preventing OWASP Top 10: SQLi, XSS & IDOR", "description": "Parameterized queries, output escaping, and authorization checks.", "estimated_time": "25 min"},
            {"name": "Role-Based Access Control (RBAC) & Route Guards", "description": "Admin, user, guest permissions, and protected API routes.", "estimated_time": "20 min"},
        ]
    if "test" in sn or "deploy" in sn or "ci/cd" in sn:
        return [
            {"name": "Unit Testing & Test-Driven Development (TDD)", "description": "Writing tests, assertions, mocks, and test runners.", "estimated_time": "20 min"},
            {"name": "Integration Testing & API Endpoint Tests", "description": "Testing full request/response flows against a test database.", "estimated_time": "25 min"},
            {"name": "Containerizing Applications with Docker", "description": "Writing Dockerfiles, layers, multi-stage builds, and compose.", "estimated_time": "25 min"},
            {"name": "Automated CI/CD Pipelines (GitHub Actions)", "description": "Workflows, automated test runs on push, and build checks.", "estimated_time": "20 min"},
            {"name": "Cloud Deployment, HTTPS & Production Monitoring", "description": "Deploying to cloud hosts, environment secrets, and uptime logs.", "estimated_time": "20 min"},
        ]
    if "portfolio" in sn or "capstone" in sn:
        return [
            {"name": "System Architecture & Data Modeling Plan", "description": "Drafting user stories, wireframes, and database ERD diagram.", "estimated_time": "20 min"},
            {"name": "Backend REST API & Database Implementation", "description": "Building CRUD endpoints, auth, and database persistence.", "estimated_time": "30 min"},
            {"name": "Responsive Frontend UI & State Integration", "description": "Connecting UI components to backend endpoints with feedback.", "estimated_time": "30 min"},
            {"name": "Testing, Edge Case Hardening & Bug Fixing", "description": "Verifying input validation, responsive layouts, and error states.", "estimated_time": "25 min"},
            {"name": "Live Production Deployment & Portfolio Presentation", "description": "Deploying live with custom domain, README, and video demo.", "estimated_time": "25 min"},
        ]
    if "ui" in sn or "ux" in sn or "figma" in sn or "design" in sn:
        return [
            {"name": "User Research, Personas & Problem Framing", "description": "Empathy mapping, user interviews, and defining design goals.", "estimated_time": "20 min"},
            {"name": "Information Architecture, User Flows & Wireframes", "description": "Site mapping, low-fi wireframing, and content hierarchy.", "estimated_time": "20 min"},
            {"name": "Visual Design Systems: Typography, Grids & Color", "description": "8pt grid system, font pairings, contrast, and component styling.", "estimated_time": "20 min"},
            {"name": "Interactive Prototyping & Figma Components", "description": "Auto Layout, component variants, and interactive prototype flows.", "estimated_time": "25 min"},
            {"name": "Usability Testing & Design System Handoff", "description": "User test sessions, feedback iteration, and developer handoff specs.", "estimated_time": "20 min"},
        ]

# 2. Check predefined domain_map by level
    level_lower = level.lower()
    # Map textual level descriptors to skill map keys.
    if "1" in level_lower or "beginner" in level_lower or "foundation" in level_lower:
        level_key = "level 1"
    elif "2" in level_lower or "level 2" in level_lower or "intermediate" in level_lower:
        level_key = "level 2"
    elif "3" in level_lower or "level 3" in level_lower:
        level_key = "level 3"
    elif "4" in level_lower or "level 4" in level_lower:
        level_key = "level 4"
    elif "5" in level_lower or "advanced" in level_lower or "level 5" in level_lower:
        level_key = "level 5"
    else:
        import re
        match = re.search(r"\d+", level_lower)
        level_key = f"level {match.group(0)}" if match else "level 1"

    domain_map = SKILL_MAPS.get(domain_key, {})
    # Build cumulative concepts up to requested level
    level_order = ["level 1", "level 2", "level 3", "level 4", "level 5"]
    try:
        target_index = level_order.index(level_key) + 1
    except ValueError:
        target_index = 1
    concepts = []
    for lk in level_order[:target_index]:
        concepts.extend(domain_map.get(lk, []))

    # Special handling for data_analytics – map to appropriate granular levels
    if not concepts and domain_key == "data_analytics":
        # approximate mapping: beginner->level 1, intermediate->level 3, advanced->level 5
        level_map = {"level 1": 1, "level 2": 3, "level 3": 5, "level 4": 6, "level 5": 8}
        target_lvl = level_map.get(level_key, 1)
        concepts = []
        for i in range(1, target_lvl + 1):
            lvl_key = f"level {i}"
            concepts.extend(domain_map.get(lvl_key, []))

    # If still missing, fallback to highest defined level for the domain
    if not concepts:
        available_levels = [k for k in domain_map.keys() if k.startswith("level")]
        if available_levels:
            max_level = max(available_levels, key=lambda k: int(k.split()[1]))
            concepts = domain_map.get(max_level, [])

    if concepts:
        return concepts

    # 3. Dynamic generic fallback tailored to skill_name
    return [
        {"name": f"Core Foundations of {skill_name}", "description": f"Fundamental concepts, principles, and mental model of {skill_name}.", "estimated_time": "15 min"},
        {"name": f"Essential Tools & Core Syntax for {skill_name}", "description": f"Setting up the working environment and executing your first workflows in {skill_name}.", "estimated_time": "15 min"},
        {"name": f"Practical Patterns & System Architecture in {skill_name}", "description": f"Handling real inputs, edge cases, and industry patterns in {skill_name}.", "estimated_time": "20 min"},
        {"name": f"Testing, Best Practices & Production Delivery in {skill_name}", "description": f"Validating outputs, handling failures, and writing maintainable {skill_name} deliverables.", "estimated_time": "20 min"},
    ]


# =============================================================================
# LESSON CONTENT — per domain, per concept type
# =============================================================================

def generate_lesson_for_domain(concept_name: str, skill_name: str, domain_key: str, level: str) -> Dict[str, Any]:
    """Generate a rich lesson for a concept based on the detected domain."""
    cn = concept_name.lower()
    sn = skill_name.lower()
    course_guide = get_course_guide(domain_key, skill_name, concept_name)
    # #region agent log
    try:
        with open(r"c:\Users\THOUSEEQ\Downloads\TA JNR AI\debug-13ca71.log", "a", encoding="utf-8") as _f:
            _f.write(json.dumps({
                "sessionId": "13ca71",
                "runId": "pre-fix",
                "hypothesisId": "A",
                "location": "ai_service.py:generate_lesson_for_domain",
                "message": "lesson domain and guide",
                "data": {
                    "concept_name": concept_name,
                    "skill_name": skill_name,
                    "domain_key": domain_key,
                    "level": level,
                    "used_course_guide": bool(course_guide),
                },
                "timestamp": int(__import__("time").time() * 1000),
            }) + "\n")
    except Exception:
        pass
    # #endregion
    if course_guide:
        return enrich_lesson_for_learning(build_course_lesson(concept_name, course_guide), domain_key, level)

    if domain_key == "python":
        base = _python_lesson(concept_name, cn, skill_name, level)
    elif domain_key == "web_dev":
        base = _web_dev_lesson(concept_name, cn, skill_name, level)
    elif domain_key == "javascript":
        base = _javascript_lesson(concept_name, cn, skill_name, level)
    elif domain_key == "data_analytics":
        base = _data_analytics_lesson(concept_name, cn, skill_name, level)
    elif domain_key == "ai_ml":
        base = _ai_ml_lesson(concept_name, cn, skill_name, level)
    elif domain_key == "cybersecurity":
        base = _cybersecurity_lesson(concept_name, cn, skill_name, level)
    elif domain_key == "dsa":
        base = _dsa_lesson(concept_name, cn, skill_name, level)
    elif domain_key == "sql_databases":
        base = _sql_lesson(concept_name, cn, skill_name, level)
    elif domain_key == "cloud_devops":
        base = _cloud_devops_lesson(concept_name, cn, skill_name, level)
    elif domain_key == "software_engineering":
        base = _software_engineering_lesson(concept_name, cn, skill_name, level)
    else:
        base = _general_tech_lesson(concept_name, skill_name, level)

    # Augment lesson with level‑specific deeper content
    return enrich_lesson_for_learning(_augment_lesson_for_level(base, level), domain_key, level)


def _teaching_level(level: str) -> str:
    value = (level or '').casefold()
    if 'advanced' in value or any(f'level {number}' in value for number in range(9, 13)):
        return 'advanced'
    if 'intermediate' in value or any(f'level {number}' in value for number in range(5, 9)):
        return 'intermediate'
    return 'beginner'


def enrich_lesson_for_learning(lesson: Dict[str, Any], domain_key: str, level: str) -> Dict[str, Any]:
    """Apply the platform lesson contract without replacing domain-authored material.

    This is intentionally a content adapter: curated guides retain their precise
    examples, while every generated or custom-domain lesson gains the same
    teach -> practise -> demonstrate structure.
    """
    lesson = dict(lesson)
    title = lesson.get('title', 'this concept')
    depth = _teaching_level(level)
    is_code = domain_key in {'python', 'web_dev', 'javascript', 'ai_ml', 'dsa', 'sql_databases', 'cloud_devops', 'software_engineering'}
    is_lab = domain_key in {'electronics', 'robotics'}
    implementation_label = 'runnable implementation' if is_code else ('safe lab workflow' if is_lab else 'practical workflow')
    existing_sections = lesson.get('lesson_sections', [])
    existing_mistake = lesson.get('pro_tip', 'Skipping checks or assumptions can make a plausible result unreliable.')
    output = lesson.get('expected_output') or lesson.get('result') or (
        'The result should match the stated inputs and be explainable step by step. Compare it with the expected behaviour before moving on.'
    )
    practice = lesson.get('thinking_exercise') or lesson.get('task') or f'Apply {title} to one small, realistic problem and explain your choices.'
    level_guidance = {
        'beginner': 'Start with the supplied example. Change one input at a time and explain the change in plain language.',
        'intermediate': 'Adapt the example to a new realistic constraint, then justify the design or calculation choices.',
        'advanced': 'Compare two viable approaches, state the trade-offs, and defend the approach you would use in production.',
    }[depth]
    lesson.update({
        'teaching_level': depth,
        'what_and_why': lesson.get('core_concept', ''),
        'expected_output': output,
        'common_mistakes': [existing_mistake],
        'implementation_type': implementation_label,
        'guided_practice': [
            {'difficulty': 'guided', 'prompt': practice, 'hint': 'Use the worked example as a starting point; identify the input, action, and result.'},
            {'difficulty': 'applied', 'prompt': level_guidance, 'hint': 'Make one deliberate choice and explain why it fits the scenario.'},
        ],
        'knowledge_check': [
            f'What problem does {title} solve, and why is it useful here?',
            f'What would you check in the output to know the approach worked?',
        ],
        'mastery_task': {
            'prompt': f'Independently apply {title} to a small domain-relevant scenario. Include your approach, the {implementation_label}, the expected result, and one check or limitation.',
            'rubric': ['Correct use of the concept', 'Reasoned steps or implementation', 'Interpretation of the expected result', 'A validation step, limitation, or trade-off'],
            'minimum_evidence': 3,
        },
    })
    contract_sections = [
        {'heading': 'What it is and why it matters', 'content': lesson['what_and_why']},
        {'heading': 'How it works', 'content': lesson.get('deep_dive', lesson['what_and_why'])},
        {'heading': 'Where you will use it', 'content': lesson.get('real_world_use_case', '')},
        {'heading': f'Practical {implementation_label}', 'content': lesson.get('code_example', '')},
        {'heading': 'Expected result and interpretation', 'content': output},
        {'heading': 'Common mistake to avoid', 'content': existing_mistake},
    ]
    # Keep authored sections first when they already provide richer domain detail.
    lesson['lesson_sections'] = existing_sections or contract_sections
    return lesson


def evaluate_mastery_response(response: str, lesson: Dict[str, Any]) -> Dict[str, Any]:
    """Score written/code/workflow evidence conservatively; never claim unverified execution."""
    text = (response or '').strip()
    if len(text) < 80:
        return {'score': 0, 'is_mastered': False, 'feedback': 'Add enough evidence to show your approach, expected result, and how you would check it.', 'evidence': {'length': len(text), 'criteria_met': 0}}
    markers = {
        'approach': ('step', 'first', 'then', 'use', 'implement', 'calculate', 'connect', 'configure'),
        'result': ('output', 'result', 'expect', 'shows', 'returns', 'measure'),
        'validation': ('check', 'test', 'verify', 'validate', 'compare', 'limit', 'trade-off', 'error'),
        'concept': tuple(word for word in re.findall(r'[a-zA-Z]{4,}', lesson.get('title', '').casefold())),
    }
    met = {name: any(marker in text.casefold() for marker in words) for name, words in markers.items() if words}
    score = sum(met.values()) * 25
    mastered = score >= 75
    missing = [name.replace('_', ' ') for name, value in met.items() if not value]
    feedback = ('Your response demonstrates independent application. Keep the same validation habit in larger work.' if mastered
                else 'Strengthen this response by adding: ' + ', '.join(missing) + '. Use the hint and try again.')
    return {'score': score, 'is_mastered': mastered, 'feedback': feedback, 'evidence': {'criteria_met': sum(met.values()), 'criteria': met}}


def _make_lesson(
    title,
    core,
    deep,
    usecase,
    code,
    pro_tip,
    exercise
):
    """
    Standardized EXA AI lesson structure.

    Keeps existing fields for backward compatibility while adding
    structured teaching sections for deeper concept learning.
    """

    return {
        "title": title,

        # Core teaching content
        "core_concept": core,
        "deep_dive": deep,
        "explanation": f"{core}\n\n{deep}",

        # Practical understanding
        "real_world_use_case": usecase,
        "code_example": code,
        "example": code,

        # Additional learning support
        "pro_tip": pro_tip,
        "thinking_exercise": exercise,

        # New structured lesson sections
        "learning_objectives": [
            f"Explain the core principle of {title}.",
            f"Describe how {title} works.",
            f"Connect {title} to a real-world application.",
            f"Apply {title} in a practical exercise.",
        ],

        "lesson_sections": [
            {
                "heading": "1. Core Principle",
                "content": core,
            },
            {
                "heading": "2. Detailed Explanation",
                "content": deep,
            },
            {
                "heading": "3. Real-World Application",
                "content": usecase,
            },
            {
                "heading": "4. Practical Example",
                "content": code,
            },
            {
                "heading": "5. Expert Tip",
                "content": pro_tip,
            },
            {
                "heading": "6. Independent Practice",
                "content": exercise,
            },
        ],

        # Visuals can be populated by domain-specific lesson generators.
        # Do not invent image URLs or display unrelated images.
        "visual_aids": [],

        "key_points": [
            f"Understand the core principle behind {title}.",
            "Know why the concept works, not just how to use it.",
            "Connect the explanation to real-world applications.",
            "Complete the practical exercise before attempting mastery checks.",
        ],

        "mentor_note": (
            f"Take your time with {title}. "
            "Understand each section, study the practical example, "
            "and complete the exercise before testing your understanding."
        ),
    }

def _augment_lesson_for_level(lesson: Dict[str, Any], level: str) -> Dict[str, Any]:
    """Add intermediate or advanced enrichments without touching Level 1 lessons.

    The existing lesson dict already contains core fields. For intermediate
    (Level 2‑3) we add a richer exercise set. For advanced (Level 4‑5) we add
    a scenario‑based assessment, a capstone project brief, and detailed feedback
    guidance. This preserves backward compatibility – callers that only expect
    the original keys continue to work.
    """
    lvl = level.lower()
    # Intermediate enrichment
    if "level 2" in lvl or "level 3" in lvl:
        lesson["intermediate_exercises"] = [
            {
                "title": f"Apply {lesson.get('title', 'the concept')} in a real‑world scenario",
                "description": "Create a small project or script that solves a concrete problem using the concept.",
                "hint": "Break the problem into sub‑tasks that map directly to the concept's core steps."
            }
        ]
    # Advanced enrichment
    if "level 4" in lvl or "level 5" in lvl:
        lesson["scenario_assessment"] = {
            "description": "Given a realistic use‑case, answer comprehension questions and outline how the concept would be applied.",
            "questions": [
                f"What trade‑offs does {lesson.get('title', 'the concept')} introduce in this scenario?",
                f"How would you modify the implementation to handle edge‑case X?",
                f"Explain performance considerations when scaling this solution."
            ]
        }
        lesson["advanced_project_brief"] = {
            "title": f"Capstone: Build a mini‑application using {lesson.get('title', 'the concept')}",
            "outline": "Define requirements, design architecture, implement, test, and document the solution.",
            "evaluation_criteria": ["Correctness", "Code quality", "Scalability", "Documentation"]
        }
        lesson["detailed_feedback"] = "Provide a peer‑review checklist focusing on correctness, edge‑case handling, performance, and adherence to best practices."
    return lesson


def _python_lesson(concept_name, cn, skill_name, level):
    if "variable" in cn or "data type" in cn:
        return _make_lesson(
            concept_name,
            "Variables are named containers that store values in memory. Python is dynamically typed — the type is inferred at runtime, not declared explicitly.",
            "How Python variables work:\n\n1. Assignment: name = value creates a binding in the current scope.\n2. Dynamic typing: x = 5 makes x an int; x = 'hello' then makes it a str — same variable, new type.\n3. type() lets you inspect the type at any time.\n4. Python uses reference semantics — variables point to objects, not memory slots.",
            "In data pipelines and web backends, clean variable naming and type awareness prevents the most common bugs — passing a string where a number is expected, for example.",
            '# Python variable basics\nname = "EXA"\nage = 25\nheight = 1.75\nis_active = True\nnothing = None\n\nprint(type(name))    # <class \'str\'>\nprint(type(age))     # <class \'int\'>\nprint(type(height))  # <class \'float\'>\n\n# f-string formatting\nprint(f"Hello, {name}! You are {age} years old.")',
            "Use UPPERCASE_NAMES for constants (e.g. MAX_RETRIES = 3) and snake_case for all variable names. Python convention (PEP 8) is strict about this in professional codebases.",
            "What happens if you write `x = 5` then `x = x + '3'`? Try to predict the error type and why it occurs before running it."
        )
    elif "loop" in cn or "for" in cn or "while" in cn:
        return _make_lesson(
            concept_name,
            "Loops let you execute a block of code repeatedly. `for` loops iterate over sequences; `while` loops run as long as a condition is True.",
            "Python loop mechanics:\n\n1. for item in iterable: — works with any iterable (list, range, string, dict, file).\n2. range(start, stop, step) — generates a sequence of integers without creating a list in memory.\n3. while condition: — checks condition before each iteration; use when you don't know the count in advance.\n4. break exits immediately; continue skips to the next iteration.\n5. for...else — the else block runs only if the loop completed without a break.",
            "Web scrapers loop through 10,000 HTML elements; ETL pipelines loop through millions of CSV rows; game engines loop 60 times per second updating each entity on screen.",
            '# for loop over a list\nfruits = ["apple", "banana", "cherry"]\nfor fruit in fruits:\n    print(f"I like {fruit}")\n\n# range loop\nfor i in range(1, 6):  # 1 to 5 inclusive\n    print(f"Count: {i}")\n\n# while loop\ncount = 0\nwhile count < 3:\n    print(f"Attempt {count + 1}")\n    count += 1\n\n# Loop with break\nfor num in range(10):\n    if num == 5:\n        break\n    print(num)  # Prints 0 to 4',
            "Prefer `for` over `while` whenever you know the collection or range in advance — it's less likely to produce infinite loops.",
            "Write a loop that prints only the even numbers from 1 to 20. Then write another that stops as soon as it hits a number divisible by 7."
        )
    elif "function" in cn or "def" in cn:
        return _make_lesson(
            concept_name,
            "Functions let you package reusable logic under a name. Instead of repeating code, you call the function. Python functions are first-class objects — they can be passed as arguments and returned from other functions.",
            "Python function anatomy:\n\n1. def function_name(parameters): defines the function.\n2. Parameters are local variables inside the function.\n3. return sends a value back to the caller (None if omitted).\n4. Default parameters allow optional arguments: def greet(name='World').\n5. *args collects extra positional arguments; **kwargs collects extra keyword arguments.\n6. Scope: variables inside a function are local unless declared global.",
            "Every Django view is a Python function. Every pytest test is a function. Every Flask route handler is a function. Functions are the primary unit of logic in all Python codebases.",
            'def calculate_area(length, width, unit="cm"):\n    """Calculate rectangle area. Returns area and unit string."""\n    if length <= 0 or width <= 0:\n        raise ValueError("Dimensions must be positive")\n    area = length * width\n    return area, unit\n\n# Call with positional args\nresult, unit = calculate_area(5, 3)\nprint(f"Area: {result} {unit}²")  # Area: 15 cm²\n\n# Call with keyword args\nresult, unit = calculate_area(width=4, length=6, unit="m")\nprint(f"Area: {result} {unit}²")  # Area: 24 m²\n\n# Function as a value\ndef apply(func, value):\n    return func(value)\n\nprint(apply(len, "Python"))  # 6',
            "Keep functions short — if a function is longer than ~15 lines, it's probably doing too many things. The Single Responsibility Principle applies to functions too.",
            "Write a function that takes a list of numbers and returns a tuple of (minimum, maximum, average). Handle the case where the list is empty."
        )
    elif "class" in cn or "object" in cn or "oop" in cn:
        return _make_lesson(
            concept_name,
            "A class is a blueprint for creating objects. Objects bundle data (attributes) and behaviour (methods) together. OOP makes large codebases manageable by modelling real-world entities.",
            "Python class essentials:\n\n1. class MyClass: defines the blueprint.\n2. __init__(self, ...) is the constructor — runs when you create an instance.\n3. self refers to the specific object being operated on.\n4. Instance attributes belong to the object; class attributes are shared.\n5. Methods are functions inside a class that receive self as the first argument.\n6. __str__ controls what print(obj) shows.",
            "Django's ORM — every database table is a class. Each row is an object. Flask-SQLAlchemy, FastAPI Pydantic models, and Python's argparse all use classes heavily.",
            'class BankAccount:\n    """Represents a simple bank account."""\n    \n    bank_name = "EXA Bank"  # Class attribute\n    \n    def __init__(self, owner, balance=0):\n        self.owner = owner        # Instance attribute\n        self.balance = balance\n    \n    def deposit(self, amount):\n        if amount <= 0:\n            raise ValueError("Deposit must be positive")\n        self.balance += amount\n        return self.balance\n    \n    def withdraw(self, amount):\n        if amount > self.balance:\n            raise ValueError("Insufficient funds")\n        self.balance -= amount\n        return self.balance\n    \n    def __str__(self):\n        return f"Account({self.owner}): £{self.balance:.2f}"\n\n# Usage\naccount = BankAccount("Alice", 100)\naccount.deposit(50)\nprint(account)  # Account(Alice): £150.00',
            "Always validate data in __init__ — if a BankAccount can't have a negative balance, enforce it at creation time, not later.",
            "Add a `transfer(amount, target_account)` method to BankAccount. It should deduct from self and add to target_account atomically — what guard checks do you need?"
        )
    else:
        return _make_lesson(
            concept_name,
            f"{concept_name} is a core Python technique that makes your code more efficient, readable, and Pythonic.",
            f"How {concept_name} works in Python:\n\n1. Understand the purpose — why does Python provide this feature?\n2. Study the syntax — Python prioritises readability.\n3. See the common patterns — how do professional Python developers use this daily?\n4. Identify the edge cases — what inputs can cause unexpected results?",
            f"Production Python engineers use {concept_name} in web frameworks (Django, FastAPI), data pipelines (Pandas, PySpark), and automation scripts every day.",
            f'# {concept_name} in Python\n# Study this pattern carefully\n\ndef example_function(data):\n    """Demonstrates {concept_name}."""\n    if not data:\n        return None\n    result = [item for item in data if item is not None]\n    return result\n\n# Test it\nprint(example_function([1, None, 2, None, 3]))  # [1, 2, 3]',
            "Always test your code with edge cases: empty list, None, single element, and very large inputs.",
            f"In your own words, explain what {concept_name} does and when you'd use it instead of the alternatives."
        )


def _web_dev_lesson(concept_name, cn, skill_name, level):
    if "html" in cn or "semantic" in cn or "document" in cn:
        return _make_lesson(
            concept_name,
            "HTML (HyperText Markup Language) is the skeleton of every web page. It defines the content and structure using nested tags. Semantic HTML uses tags that describe the meaning of content, not just how it looks.",
            "HTML structure essentials:\n\n1. <!DOCTYPE html> tells the browser this is HTML5.\n2. <head> contains metadata (title, meta tags, CSS links) — not visible on page.\n3. <body> contains all visible content.\n4. Semantic tags (header, nav, main, article, section, footer, aside) help screen readers, SEO, and code readability.\n5. Block elements (div, p, h1-h6) take full width. Inline elements (span, a, strong) flow with text.",
            "Google's search ranking algorithm reads your HTML semantics. Screen readers for visually impaired users depend on correct semantic tags. Every professional web developer writes semantic HTML.",
            '<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <title>EXA Learning Platform</title>\n</head>\n<body>\n  <header>\n    <nav>\n      <a href="/">Home</a>\n      <a href="/courses">Courses</a>\n    </nav>\n  </header>\n  \n  <main>\n    <article>\n      <h1>Welcome to EXA</h1>\n      <p>Learn deeply. Prove your skills.</p>\n    </article>\n    \n    <section>\n      <h2>Featured Courses</h2>\n      <!-- course cards go here -->\n    </section>\n  </main>\n  \n  <footer>\n    <p>&copy; 2026 EXA AI. Built by Tasbi AI Technologies.</p>\n  </footer>\n</body>\n</html>',
            "Never use <div> when a semantic alternative exists. Use <button> for clickable actions (not <div onclick=...>). Screen readers and SEO tools will thank you.",
            "Look at any major website's HTML source (Ctrl+U). Can you identify which semantic elements they use? Do they use <header>, <main>, <footer>?"
        )
    elif "css" in cn or "flexbox" in cn or "grid" in cn or "box model" in cn:
        return _make_lesson(
            concept_name,
            "CSS (Cascading Style Sheets) controls how HTML elements look and are laid out. Flexbox is a 1-dimensional layout system (rows or columns). CSS Grid is 2-dimensional (rows AND columns simultaneously).",
            "Flexbox key concepts:\n\n1. display: flex on the container activates Flexbox.\n2. flex-direction: row (default) or column.\n3. justify-content: aligns items along the main axis (left-right in row).\n4. align-items: aligns items along the cross axis (top-bottom in row).\n5. flex-wrap: wrap lets items move to the next line instead of overflowing.\n6. gap: adds space between items without margin hacks.",
            "Every modern website layout uses Flexbox or Grid. Navigation bars, card grids, hero sections, footers — all built with these two systems.",
            '.container {\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n  align-items: center;\n  flex-wrap: wrap;\n  gap: 16px;\n  padding: 20px;\n}\n\n.card {\n  flex: 1 1 280px;  /* grow, shrink, min-width */\n  background: #fff;\n  border-radius: 8px;\n  padding: 20px;\n  box-shadow: 0 2px 8px rgba(0,0,0,0.1);\n}\n\n/* CSS Grid for a 3-column layout */\n.grid-layout {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  gap: 24px;\n}\n\n/* Responsive: stack on mobile */\n@media (max-width: 768px) {\n  .grid-layout {\n    grid-template-columns: 1fr;\n  }\n}',
            "Use Flexbox for navigation bars, card rows, and button groups. Use Grid for full page layouts and complex 2D arrangements.",
            "Without looking at documentation, explain: what does `justify-content: space-between` do, and how would you centre an item both horizontally and vertically with Flexbox?"
        )
    elif "react" in cn or "component" in cn or "jsx" in cn:
        return _make_lesson(
            concept_name,
            "React is a JavaScript library for building user interfaces from components. A component is a reusable, self-contained piece of UI that manages its own logic and appearance. JSX is HTML-like syntax that compiles to JavaScript function calls.",
            "React component anatomy:\n\n1. A functional component is a JavaScript function that returns JSX.\n2. Props (properties) let parent components pass data to children — like HTML attributes.\n3. JSX must have a single root element (or use <> fragments).\n4. JavaScript expressions in JSX must be wrapped in {}.\n5. Components are composed — big UIs are trees of small components.",
            "Facebook, Instagram, Airbnb, and Netflix all use React. The component model makes it possible for teams of 100+ engineers to work on the same UI without conflicts.",
            '// A reusable CourseCard component\nfunction CourseCard({ title, level, duration, onEnroll }) {\n  return (\n    <div className="course-card">\n      <h3>{title}</h3>\n      <div className="meta">\n        <span className="badge">{level}</span>\n        <span>{duration}</span>\n      </div>\n      <button \n        onClick={onEnroll}\n        className="btn-primary"\n      >\n        Enroll Now\n      </button>\n    </div>\n  );\n}\n\n// Usage in parent component\nfunction CourseList() {\n  const courses = [\n    { id: 1, title: "Python Mastery", level: "Beginner", duration: "8 weeks" },\n    { id: 2, title: "React Complete", level: "Intermediate", duration: "10 weeks" },\n  ];\n\n  return (\n    <div className="course-list">\n      {courses.map(course => (\n        <CourseCard\n          key={course.id}\n          title={course.title}\n          level={course.level}\n          duration={course.duration}\n          onEnroll={() => console.log(`Enrolling in ${course.title}`)}\n        />\n      ))}\n    </div>\n  );\n}',
            "Each component should do one thing well. If a component's JSX is longer than ~30 lines, it probably needs to be split into smaller components.",
            "What would happen if you removed the `key` prop from the `.map()` call? Why does React need keys when rendering lists?"
        )
    else:
        return _make_lesson(
            concept_name,
            f"{concept_name} is a Python concept. To understand it properly, first identify the problem it solves, the inputs it accepts, the result it produces, and how it behaves in different situations.",
            f"Learn {concept_name} step by step:\n\n"
            f"1. PURPOSE: Identify what problem {concept_name} solves in Python.\n\n"
            f"2. PRINCIPLE: Understand the underlying idea before memorising syntax.\n\n"
            f"3. SYNTAX: Study the correct Python syntax and the role of each part.\n\n"
            f"4. EXECUTION: Trace how Python evaluates the code and produces its result.\n\n"
            f"5. EDGE CASES: Consider empty inputs, invalid values, and unexpected situations.\n\n"
            f"6. APPLICATION: Apply {concept_name} in a small Python program and explain why your solution works.\n\n"
            "Important: These are learning steps, not a substitute for a concept-specific explanation. "
            "Use the examples and documentation relevant to the exact concept.",
            f"Practice {concept_name} in a small Python project. For example, if the concept relates to data processing, test it with realistic data and verify the output.",
            f"# Practice: {concept_name}\n"
            "# Replace this outline with a concept-specific example.\n"
            "# 1. Define the problem.\n"
            "# 2. Write a small Python solution.\n"
            "# 3. Test normal and edge-case inputs.\n"
            "# 4. Explain why the solution works.",
            f"Before using {concept_name} in production, understand its limitations, test edge cases, and follow the relevant Python conventions.",
            f"Create a small working example of {concept_name}. Explain each line, predict the output before running it, and test at least two edge cases."
        )


def _javascript_lesson(concept_name, cn, skill_name, level):
    if "variable" in cn or "let" in cn or "const" in cn or "scope" in cn:
        return _make_lesson(
            concept_name,
            "JavaScript has three ways to declare variables: `var` (old, function-scoped, avoid), `let` (block-scoped, reassignable), and `const` (block-scoped, cannot be reassigned). Understanding scope determines whether your variable is accessible where you need it.",
            "Scope and declaration rules:\n\n1. var is function-scoped and hoisted — it exists throughout the function, even before its declaration line.\n2. let and const are block-scoped — they only exist inside the { } block they're declared in.\n3. const does NOT mean immutable — you can still modify object properties and array elements.\n4. The Temporal Dead Zone (TDZ) is the time between entering a block and the let/const declaration — accessing in TDZ throws a ReferenceError.\n5. Closures capture variables from their outer scope.",
            "Every JavaScript bug involving 'variable is undefined' or 'variable not accessible' traces back to scope. Understanding this prevents hours of debugging.",
            '// var vs let vs const\nvar oldStyle = "avoid this";\nlet mutableValue = 0;\nconst CONSTANT = 42;\n\n// Block scope demonstration\nif (true) {\n  let blockScoped = "only here";\n  var functionScoped = "leaks out";\n  console.log(blockScoped);     // ✅ works\n}\n// console.log(blockScoped);   // ❌ ReferenceError\nconsole.log(functionScoped);   // ✅ "leaks out" — unexpected!\n\n// const with objects\nconst user = { name: "Alice" };\nuser.name = "Bob";             // ✅ allowed — modifying property\n// user = { name: "Charlie" }; // ❌ TypeError — cannot reassign\n\n// Closure example\nfunction makeCounter() {\n  let count = 0;          // captured in closure\n  return () => ++count;   // arrow fn remembers count\n}\nconst counter = makeCounter();\nconsole.log(counter()); // 1\nconsole.log(counter()); // 2',
            "Default to const. Use let only when you need to reassign. Never use var in modern JavaScript.",
            "Predict the output of this code: `for (var i = 0; i < 3; i++) { setTimeout(() => console.log(i), 100); }` — then explain why it outputs what it does."
        )
    elif "async" in cn or "promise" in cn or "await" in cn or "event loop" in cn:
        return _make_lesson(
            concept_name,
            "JavaScript is single-threaded — only one thing runs at a time. Async programming lets long-running tasks (network requests, timers) run 'in the background' without freezing the browser. Promises represent a future value; async/await is syntactic sugar over Promises.",
            "The JavaScript async model:\n\n1. The Call Stack executes synchronous code.\n2. Web APIs (setTimeout, fetch) handle async operations outside the stack.\n3. The Callback Queue holds completed async callbacks.\n4. The Event Loop moves callbacks to the Call Stack when it's empty.\n5. Promises have three states: pending, fulfilled, rejected.\n6. async functions always return a Promise.\n7. await pauses execution inside the async function until the Promise settles.",
            "Every API call, database query, and file read in Node.js is asynchronous. Understanding async prevents the #1 JavaScript mistake: assuming data is available before the async operation completes.",
            '// Promise-based fetch\nfunction fetchUser(userId) {\n  return fetch(`/api/users/${userId}`)\n    .then(response => {\n      if (!response.ok) throw new Error(`HTTP ${response.status}`);\n      return response.json();\n    })\n    .catch(error => console.error("Fetch failed:", error));\n}\n\n// Same thing with async/await (cleaner)\nasync function getUser(userId) {\n  try {\n    const response = await fetch(`/api/users/${userId}`);\n    if (!response.ok) throw new Error(`HTTP ${response.status}`);\n    const user = await response.json();\n    return user;\n  } catch (error) {\n    console.error("Failed to get user:", error);\n    return null;\n  }\n}\n\n// Parallel requests (much faster than sequential)\nasync function getDashboard(userId) {\n  const [user, posts, notifications] = await Promise.all([\n    getUser(userId),\n    fetchPosts(userId),\n    fetchNotifications(userId),\n  ]);\n  return { user, posts, notifications };\n}',
            "Use Promise.all() when requests are independent — it runs them in parallel and can be 3x faster than awaiting each one sequentially.",
            "What is the difference between `await Promise.all([a(), b()])` and `await a(); await b();`? When would you choose each?"
        )
    else:
        return _make_lesson(
            concept_name,
            f"{concept_name} is a key JavaScript concept used in modern web and server-side development.",
            f"Key points about {concept_name}:\n\n1. Understand what problem it solves.\n2. Know the syntax and common patterns.\n3. Identify edge cases and common mistakes.\n4. See how it fits into larger JavaScript applications.",
            f"JavaScript developers use {concept_name} in React applications, Node.js services, and browser-side scripting daily.",
            f'// {concept_name} example\nconst result = [1, 2, 3].map(n => n * 2);\nconsole.log(result); // [2, 4, 6]',
            "Always handle errors explicitly — unhandled Promise rejections and uncaught TypeErrors are the most common JavaScript production bugs.",
            f"Can you write a small code snippet that demonstrates {concept_name} in a realistic scenario?"
        )


def _data_analytics_lesson(concept_name, cn, skill_name, level):
    if "sql" in cn or "select" in cn or "join" in cn or "query" in cn or "group by" in cn:
        core = f"{concept_name} is the bridge between raw corporate databases and decision-making. SQL lets you retrieve exact rows from millions of records efficiently."
        deep = "How SQL queries execute:\n\n1. FROM — database identifies which table to read.\n2. WHERE — filters rows BEFORE any calculation.\n3. GROUP BY — groups filtered rows into buckets.\n4. HAVING — filters groups AFTER aggregation.\n5. SELECT — computes the final output columns.\n6. ORDER BY — sorts the result set.\n7. LIMIT — returns only the first N rows."
        usecase = "Data analysts at Spotify run SQL daily to find how many users streamed a new artist or which playlists have the highest 30-day retention."
        code = "-- Monthly revenue by customer segment\nSELECT \n    DATE_TRUNC('month', order_date) AS order_month,\n    customer_segment,\n    COUNT(DISTINCT customer_id) AS active_customers,\n    ROUND(SUM(order_amount), 2)   AS total_revenue\nFROM ecommerce_sales\nWHERE status = 'completed'\n  AND order_date >= '2026-01-01'\nGROUP BY 1, 2\nHAVING SUM(order_amount) > 1000\nORDER BY order_month DESC, total_revenue DESC;"
        tip = "Always filter with WHERE before aggregating with GROUP BY — filtering early can cut data volume by 90%, preventing server timeouts."
        exercise = "Your manager asks: 'Which 3 cities generated the most revenue last month?' List the SQL clauses you need and the correct order."
    elif "excel" in cn or "formula" in cn or "pivot" in cn or "xlookup" in cn:
        core = f"{concept_name} in modern data analytics means dynamic formulas, lookups, and PivotTable dashboards that non-technical leaders can interact with."
        deep = "Excel model best practices:\n\n1. Keep raw data separate from formula sheets.\n2. Use XLOOKUP instead of VLOOKUP — it doesn't break on column inserts.\n3. SUMIFS/COUNTIFS handle multiple criteria cleanly.\n4. PivotTables group 100,000+ rows into dynamic cross-tabs instantly.\n5. Use Tables (Ctrl+T) so formulas auto-extend to new rows."
        usecase = "Sales Operations teams build Excel dashboards where changing a single conversion rate recalculates Q4 projections across 10 regional offices in real-time."
        code = '=XLOOKUP(A2, Products!A:A, Products!D:D, "Not Found", 0)\n=SUMIFS(Sales!E:E, Sales!B:B, "Enterprise", Sales!C:C, ">=2026-01-01")\n=AVERAGEIFS(Margins!D:D, Margins!A:A, "Data Analytics")'
        tip = "Use F4 to toggle between A1, $A$1, $A1, A$1 references. Freeze the row, column, or both depending on which direction you'll drag the formula."
        exercise = "What is the difference between a PivotTable summary and a SUMIFS formula? When is a PivotTable faster for a manager?"
    elif "python" in cn or "pandas" in cn or "dataframe" in cn:
        core = f"{concept_name} lets data analysts automate repetitive cleaning, merge CSV files, and transform messy data into analysis-ready DataFrames."
        deep = "The standard Pandas analysis pipeline:\n\n1. Load: pd.read_csv() or pd.read_excel()\n2. Inspect: df.info(), df.describe(), df.isnull().sum()\n3. Clean: fillna(), dropna(), str.strip()\n4. Transform: groupby(), merge(), pivot_table()\n5. Visualise: df.plot(), seaborn charts"
        usecase = "Financial analysts use Python/Pandas to reconcile 500,000 credit card transactions nightly, flagging fraud anomalies and saving 8 hours of manual Excel work."
        code = "import pandas as pd\n\n# Load and inspect\ndf = pd.read_csv('sales_data.csv')\nprint(df.info())\nprint(df.isnull().sum())\n\n# Clean: fill missing revenue with category median\ndf['revenue'] = df.groupby('segment')['revenue'].transform(\n    lambda x: x.fillna(x.median())\n)\n\n# Aggregate by segment\nsummary = df.groupby('segment').agg(\n    customers=('customer_id', 'nunique'),\n    revenue=('revenue', 'sum'),\n    avg_order=('revenue', 'mean')\n).reset_index()\n\nprint(summary.sort_values('revenue', ascending=False))"
        tip = "Avoid Python for loops on DataFrames — vectorised operations are up to 100× faster because they run in compiled C."
        exercise = "Why is it dangerous to simply delete all rows with missing values instead of investigating why they are empty?"
    else:
        core = f"Let's master {concept_name} in Data Analytics. This enables you to structure, analyse, and communicate findings clearly."
        deep = f"How {concept_name} works in practice:\n\n1. Break the business question into measurable data steps.\n2. Identify the right data sources and validate quality.\n3. Apply the analytical technique with appropriate tools.\n4. Validate results against known benchmarks.\n5. Translate findings into clear stakeholder communication."
        usecase = f"Product and finance teams rely on {concept_name} to make evidence-based decisions instead of gut-feel guesses."
        code = f"-- Analytical approach for {concept_name}\nSELECT \n    metric_category,\n    COUNT(*) AS total_events,\n    AVG(value) AS avg_value\nFROM analytics_table\nGROUP BY metric_category\nORDER BY total_events DESC;"
        tip = "The 80/20 rule: master the 5 most common patterns first — they solve 80% of daily analytical tasks."
        exercise = f"How would you explain the business value of {concept_name} to a non-technical manager?"
    return _make_lesson(concept_name, core, deep, usecase, code, tip, exercise)


def _ai_ml_lesson(concept_name, cn, skill_name, level):
    if "linear regression" in cn or "regression" in cn:
        return _make_lesson(
            concept_name,
            "Linear regression finds the best-fit straight line through data points to predict a continuous output value. It models the relationship y = mx + b, where m is slope and b is intercept.",
            "How linear regression works:\n\n1. Define a cost function — Mean Squared Error (MSE) measures how wrong predictions are.\n2. Gradient descent iteratively adjusts weights (m, b) to minimise MSE.\n3. The learning rate controls how big each adjustment step is.\n4. Regularisation (Ridge/Lasso) adds a penalty for large weights to prevent overfitting.\n5. Evaluate with R² score (1.0 = perfect fit) and RMSE.",
            "Real estate price prediction, sales forecasting, energy consumption modelling — linear regression is the first model to try on any prediction problem before reaching for complex ones.",
            'from sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_squared_error, r2_score\nimport numpy as np\n\n# Dummy dataset: house size vs price\nX = np.array([[500],[750],[1000],[1250],[1500]])\ny = np.array([150000, 200000, 260000, 310000, 380000])\n\n# Split and train\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\n\n# Evaluate\ny_pred = model.predict(X_test)\nprint(f"R² Score: {r2_score(y_test, y_pred):.3f}")\nprint(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")\nprint(f"Predicted price for 900 sqft: £{model.predict([[900]])[0]:,.0f}")',
            "Always check the R² score AND plot your residuals. A high R² can still mask systematic errors if the relationship is not truly linear.",
            "If you trained a linear regression model to predict salary from years of experience, what R² score would you consider acceptable, and why?"
        )
    elif "neural network" in cn or "deep learning" in cn or "backpropagation" in cn:
        return _make_lesson(
            concept_name,
            "A neural network is a layered system of connected mathematical functions (neurons) that learns patterns from data. Each layer transforms the input progressively, and the network learns by adjusting connection weights through backpropagation.",
            "Neural network mechanics:\n\n1. Input layer — receives raw features (pixel values, word embeddings, numbers).\n2. Hidden layers — apply linear transformation (weights × inputs + bias) then activation function (ReLU, sigmoid).\n3. Output layer — produces predictions.\n4. Loss function — measures how wrong predictions are.\n5. Backpropagation — computes gradients of the loss w.r.t. each weight using chain rule.\n6. Gradient descent — updates weights to reduce loss.",
            "Neural networks power image recognition (Google Photos), speech synthesis (Amazon Alexa), fraud detection (Visa), and product recommendations (Netflix).",
            'import torch\nimport torch.nn as nn\n\n# Simple feedforward network\nclass SimpleNet(nn.Module):\n    def __init__(self, input_size, hidden_size, output_size):\n        super().__init__()\n        self.network = nn.Sequential(\n            nn.Linear(input_size, hidden_size),\n            nn.ReLU(),\n            nn.Dropout(0.3),\n            nn.Linear(hidden_size, output_size)\n        )\n    \n    def forward(self, x):\n        return self.network(x)\n\n# Instantiate and inspect\nmodel = SimpleNet(input_size=10, hidden_size=64, output_size=2)\nprint(model)\nprint(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")',
            "Always start with a small network and add layers only if underfitting. More parameters = more risk of overfitting on small datasets.",
            "What is the purpose of an activation function like ReLU? What would happen if every layer was purely linear (no activation)?"
        )
    else:
        return _make_lesson(
            concept_name,
            f"{concept_name} is a fundamental AI/ML concept that enables machines to learn patterns from data and make predictions or decisions.",
            f"Key aspects of {concept_name}:\n\n1. Mathematical foundation — what equations underpin this technique.\n2. Training process — how the algorithm learns from labelled or unlabelled data.\n3. Evaluation — how we measure whether the model is working correctly.\n4. Practical limitations — when this technique works well, and when it fails.",
            f"AI/ML engineers use {concept_name} in recommendation systems, computer vision, NLP, and predictive analytics at companies like Google, Meta, and Amazon.",
            f'# {concept_name} with scikit-learn\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import classification_report\n\n# Standard ML pipeline\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42\n)\n\n# Model fitting and evaluation\nmodel.fit(X_train, y_train)\ny_pred = model.predict(X_test)\nprint(classification_report(y_test, y_pred))',
            "Never evaluate your model on training data — always use a held-out test set or cross-validation to get an honest performance estimate.",
            f"What metric would you use to evaluate {concept_name} on an imbalanced dataset (99% negative, 1% positive) and why?"
        )


def _cybersecurity_lesson(concept_name, cn, skill_name, level):
    return _make_lesson(
        concept_name,
        f"{concept_name} is studied here to improve defensive monitoring and safe configuration in systems you own or in a supplied local training lab.",
        "Use a defense-first workflow: identify the asset and expected behavior, review supplied local configuration or synthetic logs, document a risk, apply a safe mitigation, and verify the result in the same lab. Keep evidence limited to the provided materials.",
        "Security and operations teams use this process to reduce risk, detect incidents, and verify that remediations work without affecting external systems.",
        "Example defensive record:\n"
        "sample_event = {'source': 'local-training-log', 'event': 'repeated failed login', 'count': 8}\n"
        "if sample_event['count'] > 5:\n"
        "    print('Review the local account logs and apply the incident playbook')",
        "Work only with deliberately vulnerable applications, synthetic/local logs, or systems you own and are authorized to administer. Do not test real third-party systems.",
        f"Given a supplied local log excerpt related to {concept_name}, identify one defensive signal, one safe mitigation, and how you would verify the change without contacting an external system."
    )


def _dsa_lesson(concept_name, cn, skill_name, level):
    if "big-o" in cn or "complexity" in cn or "time" in cn:
        return _make_lesson(
            concept_name,
            "Big-O notation describes how an algorithm's runtime or space usage grows as the input size (n) grows. It lets us compare algorithms objectively, regardless of hardware.",
            "Key complexity classes:\n\n1. O(1) — Constant: array index lookup. Always the same speed.\n2. O(log n) — Logarithmic: binary search. Doubles input = 1 extra step.\n3. O(n) — Linear: scanning an array. 2× input = 2× time.\n4. O(n log n) — Linearithmic: merge sort. Most efficient comparison sort.\n5. O(n²) — Quadratic: nested loops. 2× input = 4× time. Avoid at scale.\n6. O(2ⁿ) — Exponential: recursive subsets. Unusable for n > 30.",
            "At Google, a function called 1 billion times per day with O(n²) complexity vs O(n) can mean millions of dollars in server costs. Big-O is the language of system design interviews.",
            '# O(n²) — Brute force: all pairs\ndef find_pair_brute(nums, target):\n    for i in range(len(nums)):          # O(n)\n        for j in range(i+1, len(nums)): # O(n)\n            if nums[i] + nums[j] == target:\n                return [i, j]\n    return []\n\n# O(n) — Hash map: one pass\ndef find_pair_optimal(nums, target):\n    seen = {}  # value → index\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]  # O(1) lookup\n        seen[num] = i\n    return []\n\n# Test both\nnums = [2, 7, 11, 15]\nprint(find_pair_brute(nums, 9))    # [0, 1]\nprint(find_pair_optimal(nums, 9))  # [0, 1] — but O(n) not O(n²)',
            "In interviews, always state your solution's time and space complexity before coding. It shows you think like a professional engineer, not just a tutorial follower.",
            "An algorithm takes 1 second for n=1000. Estimate how long it takes for n=2000 if it's O(n), O(n²), and O(log n). Show your working."
        )
    elif "array" in cn or "two pointer" in cn or "sliding window" in cn:
        return _make_lesson(
            concept_name,
            "Arrays are the most fundamental data structure — contiguous blocks of memory holding elements of the same type. Two-pointer and sliding window are algorithmic patterns that solve many array problems in O(n) instead of O(n²).",
            "Two-pointer technique:\n\n1. Start two pointers at opposite ends (or both at start for fast/slow).\n2. Move them toward each other based on conditions.\n3. Eliminates the inner loop → O(n) instead of O(n²).\n\nSliding window technique:\n1. Maintain a window [left, right] over the array.\n2. Expand right to grow the window.\n3. Shrink left when the window violates a constraint.\n4. Track the optimum (max, min, etc.) as you slide.",
            "Two-pointer problems appear in ~30% of array interview questions. Sliding window is used in real systems for network packet buffering, text search algorithms, and stream processing.",
            '# Two Pointers: check if sorted array has pair summing to target\ndef has_pair_with_sum(arr, target):\n    left, right = 0, len(arr) - 1\n    while left < right:\n        current_sum = arr[left] + arr[right]\n        if current_sum == target:\n            return True\n        elif current_sum < target:\n            left += 1   # need bigger number\n        else:\n            right -= 1  # need smaller number\n    return False\n\n# Sliding Window: max sum of k consecutive elements\ndef max_subarray_sum(arr, k):\n    if len(arr) < k:\n        return 0\n    window_sum = sum(arr[:k])  # initial window\n    max_sum = window_sum\n    for i in range(k, len(arr)):\n        window_sum += arr[i] - arr[i - k]  # slide!\n        max_sum = max(max_sum, window_sum)\n    return max_sum\n\nprint(has_pair_with_sum([1, 3, 5, 7, 9], 12))  # True (3+9)\nprint(max_subarray_sum([2, 1, 5, 1, 3, 2], 3))  # 9 (5+1+3)',
            "When you see 'find pair', 'find subarray', 'longest/shortest window' in a problem — think two-pointer or sliding window before writing nested loops.",
            "Can you solve 'find longest substring without repeating characters' using the sliding window pattern? Sketch the approach in pseudocode."
        )
    else:
        return _make_lesson(
            concept_name,
            f"{concept_name} is a fundamental data structures and algorithms topic tested in coding interviews at every major tech company.",
            f"Key aspects of {concept_name}:\n\n1. Understand the data structure or algorithm from first principles.\n2. Know the time and space complexity.\n3. Identify which problem patterns it solves best.\n4. Practice implementing it from scratch, not from memory.",
            f"FAANG companies (Google, Meta, Amazon, Apple, Netflix) regularly ask {concept_name} questions in technical interviews.",
            f'# {concept_name} implementation\ndef solve(nums):\n    # Think: what\'s the simplest correct solution first?\n    # Then optimise if needed\n    result = []\n    for i, num in enumerate(nums):\n        result.append(num)\n    return result\n\nprint(solve([1, 2, 3, 4, 5]))',
            "Always clarify constraints before coding in an interview: input size, value range, can input be empty or contain duplicates?",
            f"What is the time complexity of your approach to {concept_name}? Can you think of a more efficient solution?"
        )


def _sql_lesson(concept_name, cn, skill_name, level):
    if "select" in cn or "where" in cn or "query" in cn:
        return _make_lesson(
            concept_name,
            "SELECT is the SQL command for retrieving data. WHERE filters rows. Together they form the basis of 80% of all SQL queries written in real analytics and application work.",
            "SQL query execution order:\n\n1. FROM — choose the table.\n2. WHERE — filter rows (runs BEFORE SELECT!).\n3. SELECT — pick and compute columns.\n4. ORDER BY — sort the result.\n5. LIMIT — cap the number of rows returned.\n\nKey WHERE operators: =, !=, >, <, >=, <=, BETWEEN, IN, LIKE, IS NULL",
            "Every web application reads data from a database using SELECT queries. Every dashboard fetches data with filtered queries. SQL is the universal data retrieval language.",
            "-- Basic SELECT with WHERE\nSELECT \n    first_name,\n    last_name,\n    email,\n    created_at\nFROM users\nWHERE active = true\n  AND created_at >= '2026-01-01'\nORDER BY created_at DESC\nLIMIT 10;\n\n-- Pattern matching\nSELECT * FROM products\nWHERE name LIKE '%laptop%'   -- contains 'laptop'\n  AND price BETWEEN 500 AND 2000;\n\n-- NULL handling\nSELECT * FROM orders\nWHERE shipped_at IS NULL;  -- pending orders",
            "NULL is not zero and not empty string — it means 'unknown'. Always use IS NULL / IS NOT NULL, never = NULL.",
            "Write a query that returns all users who signed up in the last 30 days and have verified their email. What columns would you include?"
        )
    elif "join" in cn:
        return _make_lesson(
            concept_name,
            "JOINs combine rows from two or more tables based on a related column (usually a foreign key). They are the most powerful and most misunderstood feature of SQL.",
            "JOIN types:\n\n1. INNER JOIN — returns only rows that have a match in BOTH tables.\n2. LEFT JOIN — returns ALL rows from the left table; NULLs for non-matching right rows.\n3. RIGHT JOIN — opposite of LEFT JOIN (rarely used; swap table order and use LEFT instead).\n4. FULL OUTER JOIN — all rows from both tables, NULLs where no match.\n5. CROSS JOIN — every combination of rows (cartesian product — usually a mistake!).",
            "Every relational database application uses JOINs. Reporting tools, dashboards, and APIs all combine data from multiple tables constantly.",
            "-- INNER JOIN: customers with at least one order\nSELECT \n    c.customer_name,\n    COUNT(o.order_id) AS order_count,\n    SUM(o.total_amount) AS lifetime_value\nFROM customers c\nINNER JOIN orders o ON c.customer_id = o.customer_id\nGROUP BY c.customer_id, c.customer_name\nORDER BY lifetime_value DESC;\n\n-- LEFT JOIN: ALL customers, even those with no orders\nSELECT \n    c.customer_name,\n    COALESCE(COUNT(o.order_id), 0) AS order_count\nFROM customers c\nLEFT JOIN orders o ON c.customer_id = o.customer_id\nGROUP BY c.customer_id, c.customer_name;",
            "Use LEFT JOIN when you want to preserve all rows from one table regardless of matches. A missing row becomes NULL — always handle that with COALESCE or IS NULL filters.",
            "Your manager asks: 'Show me all products that have NEVER been ordered.' Which type of JOIN would you use, and what WHERE condition would you add?"
        )
    else:
        return _make_lesson(
            concept_name,
            f"{concept_name} is a key SQL and database concept used in application development, data analytics, and system design.",
            f"How {concept_name} works:\n\n1. Understand the database operation being performed.\n2. Learn the syntax and required clauses.\n3. Practice with realistic data scenarios.\n4. Identify performance considerations.",
            f"Database engineers and data analysts use {concept_name} in production systems handling millions of records daily.",
            f"-- {concept_name} example\nSELECT column1, column2\nFROM table_name\nWHERE condition = true\nORDER BY column1;",
            "Always test SQL changes on a development database first. A wrong UPDATE or DELETE without a WHERE clause can affect every row in the table.",
            f"How would you test your {concept_name} query to ensure it's returning the correct results before running it in production?"
        )


def _cloud_devops_lesson(concept_name, cn, skill_name, level):
    if "docker" in cn or "container" in cn or "dockerfile" in cn:
        return _make_lesson(
            concept_name,
            "Docker packages an application and all its dependencies into a container — a lightweight, isolated environment that runs identically on any machine. 'Works on my machine' becomes 'works everywhere'.",
            "Docker core concepts:\n\n1. Image — read-only blueprint (built from a Dockerfile).\n2. Container — running instance of an image.\n3. Dockerfile — script of instructions to build an image.\n4. Registry — storage for images (Docker Hub, ECR, GCR).\n5. Volume — persistent storage that survives container restarts.\n6. Network — how containers communicate with each other.",
            "Every major tech company — Netflix, Spotify, Airbnb — runs their production services in Docker containers. It's required knowledge for any DevOps or backend engineering role.",
            '# Dockerfile for a Python web app\nFROM python:3.12-slim\n\n# Set working directory\nWORKDIR /app\n\n# Copy dependency file first (layer caching optimisation)\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\n# Copy application code\nCOPY . .\n\n# Create non-root user (security best practice)\nRUN useradd --create-home appuser\nUSER appuser\n\n# Expose port and run\nEXPOSE 8000\nCMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]\n\n# Build and run:\n# docker build -t my-app .\n# docker run -p 8000:8000 my-app',
            "Always use a specific image tag (python:3.12-slim) not `latest` — `latest` changes without warning and breaks reproducible builds.",
            "What is the difference between a Docker image and a Docker container? What happens to data written inside a container when it stops?"
        )
    else:
        return _make_lesson(
            concept_name,
            f"{concept_name} is a core Cloud/DevOps skill used to build, deploy, and operate reliable software infrastructure.",
            f"Key aspects of {concept_name}:\n\n1. Purpose — what problem does this tool or technique solve?\n2. Core commands — the essential CLI or configuration.\n3. Production patterns — how professional teams use this at scale.\n4. Common pitfalls — mistakes to avoid.",
            f"DevOps engineers use {concept_name} at companies like Netflix, Cloudflare, and Stripe to deploy hundreds of times per day with zero downtime.",
            f"# {concept_name} command reference\n# Always refer to official documentation for your specific version\necho 'Practice in a safe lab environment'",
            "Infrastructure changes can take down production services. Always test in a staging environment first and have a rollback plan.",
            f"How would {concept_name} improve reliability or deployment speed for a team shipping code multiple times per day?"
        )


def _software_engineering_lesson(concept_name, cn, skill_name, level):
    if "git" in cn or "branch" in cn or "commit" in cn:
        return _make_lesson(
            concept_name,
            "Git is the industry-standard version control system. Every professional software team uses Git to track changes, collaborate safely, and deploy code. A commit is a saved snapshot; a branch is an independent line of development.",
            "Essential Git workflow:\n\n1. git init / git clone — start a repo.\n2. git add . — stage changes.\n3. git commit -m 'message' — save snapshot.\n4. git branch feature/name — create isolated work.\n5. git checkout / git switch — move between branches.\n6. git merge / git rebase — combine branches.\n7. git pull / git push — sync with remote.\n8. git log --oneline — see history at a glance.",
            "Every open-source project and every professional software team uses Git daily. A GitHub profile with clean commits is increasingly a hiring signal for junior developers.",
            '# Professional Git workflow\n\n# Start a new feature\ngit checkout -b feature/user-authentication\n\n# Make changes, then stage and commit\ngit add src/auth/\ngit commit -m "feat: add JWT authentication middleware"\n\n# Push branch to remote\ngit push origin feature/user-authentication\n\n# Interactive rebase to clean up commits before PR\ngit rebase -i HEAD~3\n\n# After PR is merged, clean up\ngit checkout main\ngit pull origin main\ngit branch -d feature/user-authentication\n\n# Helpful aliases in ~/.gitconfig\n[alias]\n    lg = log --oneline --graph --all --decorate\n    st = status -s',
            "Write commit messages in the imperative present tense: 'Add login form' not 'Added login form'. Use conventional commits (feat:, fix:, docs:) for professional repos.",
            "What is the difference between `git merge` and `git rebase`? When would you prefer each approach, and what risks does rebase carry on a shared branch?"
        )
    elif "solid" in cn or "principle" in cn or "clean code" in cn:
        return _make_lesson(
            concept_name,
            "SOLID is a set of 5 principles for writing object-oriented code that is easy to understand, modify, and extend. Violating them leads to 'spaghetti code' that becomes impossible to change without breaking things.",
            "The 5 SOLID principles:\n\n1. Single Responsibility (SRP) — a class does one thing. God classes that do everything are the #1 cause of bugs.\n2. Open/Closed (OCP) — open for extension, closed for modification. Add behaviour by adding code, not changing existing code.\n3. Liskov Substitution (LSP) — subclasses must be usable wherever the parent class is expected.\n4. Interface Segregation (ISP) — don't force classes to implement interfaces they don't use.\n5. Dependency Inversion (DIP) — depend on abstractions (interfaces), not concrete implementations.",
            "SOLID principles are the difference between codebases that scale to 50 engineers and those that become unmaintainable after 3 months. Senior engineers are hired partly for knowing and applying these.",
            '# SRP Violation — one class doing too much\nclass UserManager:\n    def create_user(self): ...\n    def send_email(self): ...      # ← email is a different responsibility\n    def generate_report(self): ... # ← reporting is a different responsibility\n\n# SRP Fixed — each class has one job\nclass UserRepository:\n    def create_user(self, data): ...\n\nclass EmailService:\n    def send_welcome_email(self, user): ...\n\nclass UserReportGenerator:\n    def generate(self, users): ...\n\n# DIP — depend on abstractions, not concretions\nfrom abc import ABC, abstractmethod\n\nclass NotificationService(ABC):\n    @abstractmethod\n    def notify(self, message: str): ...\n\nclass EmailNotification(NotificationService):\n    def notify(self, message): ...\n\nclass SMSNotification(NotificationService):\n    def notify(self, message): ...\n\n# OrderProcessor depends on the abstraction\nclass OrderProcessor:\n    def __init__(self, notifier: NotificationService):\n        self.notifier = notifier  # inject any implementation!',
            "SRP is the most impactful principle to apply first. If you can't describe what a class does in one sentence without the word 'and', it's violating SRP.",
            "Find a class or function in a project you've worked on that violates SRP. What single responsibility should it have, and what should be extracted?"
        )
    else:
        return _make_lesson(
            concept_name,
            f"{concept_name} is a software engineering best practice that helps teams write more maintainable, reliable, and scalable code.",
            f"Key aspects of {concept_name}:\n\n1. The problem it solves — what goes wrong without it.\n2. The principle or pattern — the core idea.\n3. Practical application — how professional teams apply it.\n4. Common misapplication — how to avoid over-engineering.",
            f"Senior software engineers are expected to know and apply {concept_name} in code reviews, architecture discussions, and day-to-day development.",
            f'# {concept_name} example\n# Clean, intentional code communicates meaning\ndef calculate_total_price(items, discount_rate=0.0):\n    """Calculate total price with optional discount.\n    \n    Args:\n        items: List of (price, quantity) tuples\n        discount_rate: Decimal discount (0.0 to 1.0)\n    Returns:\n        Total price after discount\n    """\n    subtotal = sum(price * qty for price, qty in items)\n    return subtotal * (1 - discount_rate)',
            "The best code is the simplest code that correctly solves the problem. Resist the urge to add complexity 'for the future' — YAGNI (You Aren't Gonna Need It).",
            f"How would you explain {concept_name} to a junior developer joining your team? What example would you use?"
        )


def _general_tech_lesson(concept_name, skill_name, level):
    return _make_lesson(
        concept_name,
        f"{concept_name} is a foundational concept in {skill_name}. Understanding it deeply gives you the mental model needed to build real applications.",
        f"How {concept_name} works:\n\n1. Core purpose — what problem does it solve?\n2. Underlying mechanism — how it actually works under the hood.\n3. Common usage patterns — how professionals use it daily.\n4. Edge cases — where it fails or behaves unexpectedly.",
        f"Professional {skill_name} developers use {concept_name} in production systems handling real users and real data every day.",
        f'# {concept_name} implementation example\ndef example_implementation(data):\n    """Demonstrates {concept_name} pattern."""\n    if not data:\n        return None\n    \n    # Process the data\n    result = [item for item in data if item is not None]\n    return result\n\n# Always test edge cases\nprint(example_implementation([]))         # None\nprint(example_implementation([1, None, 2])) # [1, 2]',
        "Always validate your understanding by implementing from scratch, not copying. Building from memory reveals exactly what you know vs what you've just memorised.",
        f"Can you explain {concept_name} in your own words as if teaching it to someone who has never seen it before?"
    )


# =============================================================================
# QUIZ QUESTIONS — per domain
# =============================================================================

def generate_quiz_for_domain(concept_name: str, skill_name: str, domain_key: str, level: str) -> List[Dict[str, Any]]:
    """Return 5 domain-specific MCQ questions for a concept."""
    cn = concept_name.lower()
    course_guide = get_course_guide(domain_key, skill_name, concept_name)
    if course_guide:
        return build_course_quiz(concept_name, course_guide)

    if domain_key == "python":
        return _python_quiz(concept_name, cn, skill_name, level)
    elif domain_key == "web_dev":
        return _web_dev_quiz(concept_name, cn, skill_name, level)
    elif domain_key == "javascript":
        return _javascript_quiz(concept_name, cn, skill_name, level)
    elif domain_key == "data_analytics":
        return _data_analytics_quiz(concept_name, cn, skill_name, level)
    elif domain_key == "ai_ml":
        return _ai_ml_quiz(concept_name, cn, skill_name, level)
    elif domain_key == "cybersecurity":
        return _cybersecurity_quiz(concept_name, cn, skill_name, level)
    elif domain_key == "dsa":
        return _dsa_quiz(concept_name, cn, skill_name, level)
    elif domain_key == "sql_databases":
        return _sql_quiz(concept_name, cn, skill_name, level)
    else:
        return _general_quiz(concept_name, skill_name, level)


def _python_quiz(concept_name, cn, skill_name, level):
    if "variable" in cn or "data type" in cn:
        return [
            {"question_text": "What does `type(3.14)` return in Python?", "option_a": "<class 'int'>", "option_b": "<class 'float'>", "option_c": "<class 'double'>", "option_d": "<class 'decimal'>", "correct_answer": "B", "explanation": "3.14 is a floating-point number, so type() returns <class 'float'>. Python has no 'double' type — floats are always 64-bit."},
            {"question_text": "Which statement correctly assigns and uses an f-string?", "option_a": "name = 'EXA' | print('Hello ' + name)", "option_b": "name = 'EXA' | print(f'Hello {name}')", "option_c": "name = 'EXA' | print('Hello %name')", "option_d": "name = 'EXA' | print('Hello' + {name})", "correct_answer": "B", "explanation": "f-strings use f'...' prefix with variables inside {}. They're the modern, readable way to format strings in Python 3.6+."},
            {"question_text": "What happens when you assign `x = 5` then `x = 'hello'`?", "option_a": "A TypeError is raised — you can't change types", "option_b": "x is now 'hello' — Python is dynamically typed", "option_c": "x holds both values", "option_d": "Python converts 'hello' to 5", "correct_answer": "B", "explanation": "Python is dynamically typed — a variable can be rebound to any type at any time. x just points to the new 'hello' string object."},
            {"question_text": "What is the correct way to check if a variable `val` is None?", "option_a": "if val == None:", "option_b": "if val = None:", "option_c": "if val is None:", "option_d": "if val.isNone():", "correct_answer": "C", "explanation": "Use `is None` (identity check) not `== None` (equality check). None is a singleton in Python, so identity comparison is always correct and slightly faster."},
            {"question_text": "What naming convention does PEP 8 recommend for Python variables?", "option_a": "camelCase (myVariable)", "option_b": "PascalCase (MyVariable)", "option_c": "snake_case (my_variable)", "option_d": "UPPER_CASE (MY_VARIABLE)", "correct_answer": "C", "explanation": "PEP 8 (Python style guide) requires snake_case for variable and function names. UPPER_CASE is for constants; PascalCase is for class names."},
        ]
    elif "loop" in cn or "for" in cn or "while" in cn:
        return [
            {"question_text": "What does `range(1, 6)` produce?", "option_a": "1, 2, 3, 4, 5, 6", "option_b": "1, 2, 3, 4, 5", "option_c": "0, 1, 2, 3, 4, 5", "option_d": "0, 1, 2, 3, 4", "correct_answer": "B", "explanation": "range(start, stop) generates numbers from start UP TO BUT NOT INCLUDING stop. range(1, 6) gives 1, 2, 3, 4, 5."},
            {"question_text": "What does `break` do inside a loop?", "option_a": "Skips to the next iteration", "option_b": "Pauses execution for 1 second", "option_c": "Exits the entire loop immediately", "option_d": "Exits the function", "correct_answer": "C", "explanation": "`break` immediately terminates the enclosing loop. `continue` skips to the next iteration. They're different — break exits; continue skips."},
            {"question_text": "How many times does this loop print? `for i in range(0, 10, 2): print(i)`", "option_a": "10", "option_b": "5", "option_c": "4", "option_d": "6", "correct_answer": "B", "explanation": "range(0, 10, 2) with step 2 generates: 0, 2, 4, 6, 8 — that's 5 values. Step controls how much i increments each iteration."},
            {"question_text": "What is the risk of a `while` loop compared to a `for` loop?", "option_a": "while loops are always slower", "option_b": "while loops can run forever if the condition never becomes False", "option_c": "while loops can't iterate over lists", "option_d": "while loops always run at least once", "correct_answer": "B", "explanation": "An infinite loop occurs when the while condition never becomes False (e.g., forgetting to increment a counter). for loops over a finite iterable always terminate naturally."},
            {"question_text": "Which loop is better when you know exactly how many iterations you need?", "option_a": "while loop", "option_b": "do-while loop", "option_c": "for loop with range()", "option_d": "recursive function", "correct_answer": "C", "explanation": "`for i in range(n)` is the Pythonic choice when the count is known. while loops are better when you iterate until a condition changes, not a fixed count."},
        ]
    else:
        return _general_quiz(concept_name, skill_name, "python")


def _web_dev_quiz(concept_name, cn, skill_name, level):
    if "html" in cn or "semantic" in cn:
        return [
            {"question_text": "Which HTML element is semantically correct for the main navigation menu?", "option_a": "<div class='nav'>", "option_b": "<nav>", "option_c": "<menu>", "option_d": "<header>", "correct_answer": "B", "explanation": "<nav> is the semantic HTML5 element for navigation menus. It tells browsers, screen readers, and search engines 'this is navigation', unlike a generic <div>."},
            {"question_text": "What does the `<head>` element contain?", "option_a": "The visible page content", "option_b": "The page header with logo and navigation", "option_c": "Metadata — title, CSS links, meta tags, scripts", "option_d": "Only the page title", "correct_answer": "C", "explanation": "<head> contains metadata not shown on the page itself: title, meta tags, CSS stylesheet links, fonts, and script tags. The visible content goes inside <body>."},
            {"question_text": "Why should you use `<button>` instead of `<div onclick='...'>` for clickable actions?", "option_a": "Buttons are faster", "option_b": "Buttons are keyboard-accessible, focusable, and screen-reader-friendly by default", "option_c": "Divs don't support click events", "option_d": "There is no difference", "correct_answer": "B", "explanation": "Native <button> elements are keyboard accessible (Tab, Enter, Space), focusable, and correctly announced by screen readers. A clickable <div> requires extra ARIA attributes to achieve the same accessibility."},
            {"question_text": "What is the correct DOCTYPE declaration for HTML5?", "option_a": "<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01//EN'>", "option_b": "<!DOCTYPE html5>", "option_c": "<!DOCTYPE html>", "option_d": "<html version='5'>", "correct_answer": "C", "explanation": "HTML5 uses the simplified `<!DOCTYPE html>` declaration. Older HTML versions had long DOCTYPE strings referencing DTD files — HTML5 simplified this significantly."},
            {"question_text": "Which element should wrap the primary content of a page (not repeated headers/footers)?", "option_a": "<section>", "option_b": "<article>", "option_c": "<main>", "option_d": "<div id='content'>", "correct_answer": "C", "explanation": "<main> represents the primary, unique content of the document — there should be only one per page. Screen readers use it to skip directly to the main content."},
        ]
    elif "css" in cn or "flexbox" in cn or "grid" in cn:
        return [
            {"question_text": "Which CSS property activates Flexbox on a container?", "option_a": "position: flex", "option_b": "display: flex", "option_c": "flex: true", "option_d": "layout: flexbox", "correct_answer": "B", "explanation": "`display: flex` on the container element activates Flexbox. All direct children automatically become flex items."},
            {"question_text": "What does `justify-content: space-between` do in a flex row?", "option_a": "Centres all items in the middle", "option_b": "Puts equal space between items, with none at the edges", "option_c": "Puts equal space around every item including edges", "option_d": "Stacks items vertically", "correct_answer": "B", "explanation": "space-between distributes items with equal gaps BETWEEN them, but NO gap at the start and end edges. space-around adds half-gaps at the edges too."},
            {"question_text": "How do you create a 3-column equal-width grid with CSS Grid?", "option_a": "grid-columns: 3", "option_b": "grid-template-columns: 33% 33% 33%", "option_c": "grid-template-columns: repeat(3, 1fr)", "option_d": "columns: 3", "correct_answer": "C", "explanation": "`repeat(3, 1fr)` creates 3 columns each taking 1 fraction of available space — they're always equal-width. It also handles gaps correctly, unlike 33.33%."},
            {"question_text": "What does `flex: 1 1 280px` mean?", "option_a": "Fixed width of 280px, cannot shrink or grow", "option_b": "Grow if space available, shrink if needed, minimum/basis of 280px", "option_c": "Height is 280px, weight is 1", "option_d": "Margin of 280px", "correct_answer": "B", "explanation": "flex: grow shrink basis. So flex: 1 1 280px means: can grow (1), can shrink (1), starting width is 280px. This creates responsive cards that wrap nicely."},
            {"question_text": "Which CSS unit is best for creating a truly responsive layout that adapts to the parent container?", "option_a": "px (pixels)", "option_b": "pt (points)", "option_c": "% or fr (fractional units)", "option_d": "cm (centimetres)", "correct_answer": "C", "explanation": "% and fr are relative units. fr (fraction) is specific to CSS Grid and divides available space proportionally. Fixed units like px don't adapt when the parent changes size."},
        ]
    else:
        return _general_quiz(concept_name, skill_name, "web_dev")


def _javascript_quiz(concept_name, cn, skill_name, level):
    if "variable" in cn or "let" in cn or "const" in cn or "scope" in cn:
        return [
            {"question_text": "What is the key difference between `let` and `var` in JavaScript?", "option_a": "let is faster than var", "option_b": "let is block-scoped; var is function-scoped and hoisted", "option_c": "var is newer and replaces let", "option_d": "There is no difference in modern JS", "correct_answer": "B", "explanation": "`let` is block-scoped — only exists inside the { } it's declared in. `var` is function-scoped and gets hoisted to the top of the function, causing subtle bugs."},
            {"question_text": "Can you modify the properties of a `const` object?", "option_a": "No — const makes everything immutable", "option_b": "Yes — const only prevents reassignment of the variable, not mutation of the object", "option_c": "Only in strict mode", "option_d": "Only if you use Object.freeze() first", "correct_answer": "B", "explanation": "`const` prevents reassigning the variable binding (user = {...} would throw), but you can still modify object properties (user.name = 'Bob' is fine). Use Object.freeze() for true immutability."},
            {"question_text": "What is the Temporal Dead Zone (TDZ) in JavaScript?", "option_a": "A memory leak caused by let variables", "option_b": "The time between entering a block and when let/const is declared — accessing causes ReferenceError", "option_c": "Variables that are never used", "option_d": "Async code that hasn't resolved yet", "correct_answer": "B", "explanation": "let and const exist in TDZ from the start of the block until their declaration line. Accessing them before declaration throws ReferenceError — unlike var which returns undefined."},
            {"question_text": "What does a closure 'close over'?", "option_a": "A function that doesn't return anything", "option_b": "The outer scope's variables, preserving them even after the outer function exits", "option_c": "A function with no parameters", "option_d": "A try/catch block", "correct_answer": "B", "explanation": "A closure is a function that 'remembers' variables from its outer scope. Even after the outer function returns, the inner function still has access to those captured variables."},
            {"question_text": "Why should you prefer `const` over `let` as a default?", "option_a": "const is faster at runtime", "option_b": "It signals the variable won't be reassigned, improving code readability and preventing accidental reassignment", "option_c": "const uses less memory", "option_d": "const allows block scope like let does not", "correct_answer": "B", "explanation": "Using const by default communicates intent — this binding won't change. It also prevents accidental reassignment bugs. Use let only when you specifically need to reassign."},
        ]
    elif "async" in cn or "promise" in cn or "await" in cn:
        return [
            {"question_text": "What does an `async` function always return?", "option_a": "A string value", "option_b": "A Promise", "option_c": "undefined", "option_d": "A callback function", "correct_answer": "B", "explanation": "An async function always returns a Promise, even if you `return 42` — it wraps the value as `Promise.resolve(42)`. This is why you can await async functions."},
            {"question_text": "What does `await` do inside an async function?", "option_a": "Pauses the entire JavaScript engine", "option_b": "Pauses execution of the async function until the Promise resolves", "option_c": "Converts a callback to a Promise", "option_d": "Creates a new thread", "correct_answer": "B", "explanation": "`await` pauses only the current async function, allowing the event loop to handle other work. The engine is NOT blocked — other callbacks can still run while waiting."},
            {"question_text": "How do you run two async operations in PARALLEL (not one after the other)?", "option_a": "await task1(); await task2();", "option_b": "Promise.all([task1(), task2()])", "option_c": "async task1() && async task2()", "option_d": "parallel(task1, task2)", "correct_answer": "B", "explanation": "`await task1(); await task2()` is SEQUENTIAL — task2 doesn't start until task1 finishes. `Promise.all([task1(), task2()])` starts both simultaneously and waits for both."},
            {"question_text": "What happens if a rejected Promise is not caught with `.catch()` or `try/catch`?", "option_a": "Nothing — JavaScript ignores it", "option_b": "The function returns undefined", "option_c": "An UnhandledPromiseRejection warning or error is thrown", "option_d": "The promise automatically retries", "correct_answer": "C", "explanation": "Unhandled Promise rejections cause UnhandledPromiseRejectionWarning in Node.js (and crash the process in newer versions). Always wrap async calls in try/catch."},
            {"question_text": "Which is the correct way to handle errors in an async/await function?", "option_a": "async function get() { result = await fetch(url).error(handleError) }", "option_b": "async function get() { try { return await fetch(url) } catch(e) { handleError(e) } }", "option_c": "async function get() { await fetch(url) catch(e) {} }", "option_d": "async function get() { return await fetch(url) ?? null }", "correct_answer": "B", "explanation": "Use try/catch inside async functions for error handling. The catch block receives the rejection reason (error). This is the standard, readable pattern for async error handling."},
        ]
    else:
        return _general_quiz(concept_name, skill_name, "javascript")


def _data_analytics_quiz(concept_name, cn, skill_name, level):
    if "sql" in cn or "select" in cn or "join" in cn or "group by" in cn:
        return [
            {"question_text": "In what order does SQL actually execute: SELECT, FROM, WHERE, GROUP BY?", "option_a": "SELECT → FROM → WHERE → GROUP BY", "option_b": "FROM → WHERE → GROUP BY → SELECT", "option_c": "WHERE → FROM → SELECT → GROUP BY", "option_d": "GROUP BY → WHERE → FROM → SELECT", "correct_answer": "B", "explanation": "SQL execution order: FROM (identify tables) → WHERE (filter rows) → GROUP BY (group filtered rows) → HAVING (filter groups) → SELECT (compute columns) → ORDER BY → LIMIT."},
            {"question_text": "What is the difference between WHERE and HAVING?", "option_a": "They are identical — HAVING is just an alias for WHERE", "option_b": "WHERE filters rows before aggregation; HAVING filters groups after aggregation", "option_c": "HAVING filters rows; WHERE filters columns", "option_d": "WHERE only works with text; HAVING only works with numbers", "correct_answer": "B", "explanation": "WHERE filters individual rows BEFORE GROUP BY aggregates them. HAVING filters the aggregated results AFTER GROUP BY. You cannot use WHERE SUM(amount) > 1000 — that requires HAVING."},
            {"question_text": "Which JOIN type returns ALL rows from the left table even when there's no match in the right table?", "option_a": "INNER JOIN", "option_b": "CROSS JOIN", "option_c": "LEFT JOIN", "option_d": "FULL JOIN", "correct_answer": "C", "explanation": "LEFT JOIN returns all rows from the left table; rows with no match in the right table get NULL for all right-table columns. INNER JOIN only returns matched rows."},
            {"question_text": "What does NULL represent in SQL?", "option_a": "Zero (0)", "option_b": "An empty string", "option_c": "Unknown or missing value", "option_d": "False", "correct_answer": "C", "explanation": "NULL means 'unknown' or 'absent' — it is NOT zero, not empty string, not false. This is why you use IS NULL / IS NOT NULL, not = NULL (which always returns unknown, never true)."},
            {"question_text": "A window function like ROW_NUMBER() OVER (PARTITION BY ...) differs from GROUP BY because:", "option_a": "Window functions are slower than GROUP BY", "option_b": "Window functions calculate across rows without collapsing them into groups", "option_c": "Window functions only work on numeric columns", "option_d": "There is no difference", "correct_answer": "B", "explanation": "GROUP BY collapses rows into one row per group. Window functions (ROW_NUMBER, RANK, LAG) calculate across related rows but KEEP every original row in the result set."},
        ]
    elif "excel" in cn or "xlookup" in cn or "sumifs" in cn:
        return [
            {"question_text": "Why is XLOOKUP better than VLOOKUP for most use cases?", "option_a": "XLOOKUP is faster to type", "option_b": "XLOOKUP doesn't break when columns are inserted, supports exact match by default, and can search left", "option_c": "XLOOKUP works on Mac; VLOOKUP only works on Windows", "option_d": "XLOOKUP can search multiple sheets simultaneously", "correct_answer": "B", "explanation": "VLOOKUP needs a column number that breaks when you insert columns. XLOOKUP uses column references so it's robust to structural changes. It also defaults to exact match and can search left (VLOOKUP can only search right)."},
            {"question_text": "In SUMIFS, which argument comes FIRST?", "option_a": "The criteria range", "option_b": "The criteria value", "option_c": "The sum range (the column to add up)", "option_d": "The conditions", "correct_answer": "C", "explanation": "SUMIFS(sum_range, criteria_range1, criteria1, ...) — the column you want to sum comes FIRST. This is opposite to SUMIF (singular) which has sum_range LAST. This is the most common SUMIFS mistake."},
            {"question_text": "What does $A$1 (absolute reference) do when you copy a formula to another cell?", "option_a": "The reference shifts relative to the new cell position", "option_b": "The reference stays locked on cell A1 regardless of where you paste", "option_c": "The formula becomes read-only", "option_d": "Excel asks if you want to update the reference", "correct_answer": "B", "explanation": "$ signs freeze the reference. $A$1 always refers to A1 no matter where the formula is copied. A1 (relative) would shift — if you copy from B2 to C3, A1 becomes B2."},
            {"question_text": "A PivotTable is better than SUMIFS for which scenario?", "option_a": "When you need one specific calculated value", "option_b": "When you need to explore and slice data interactively across multiple dimensions", "option_c": "When the dataset has fewer than 100 rows", "option_d": "When you need to use the result in another formula", "correct_answer": "B", "explanation": "PivotTables excel at interactive exploration — drag fields, add slicers, change breakdowns instantly. SUMIFS is better when you need specific calculated values embedded in other formulas."},
            {"question_text": "What does IFERROR(XLOOKUP(A2, D:D, E:E), 'Not Found') do?", "option_a": "Searches for A2 in column E and returns D — in reverse", "option_b": "Searches for A2 in column D, returns the corresponding value from E, returns 'Not Found' if no match", "option_c": "Returns an error if A2 is not in column D", "option_d": "Checks if A2 equals 'Not Found'", "correct_answer": "B", "explanation": "XLOOKUP(lookup, search_range, return_range) finds the value. IFERROR wraps it to return 'Not Found' instead of an #N/A error when no match exists — essential for clean dashboards."},
        ]
    else:
        return _general_quiz(concept_name, skill_name, "data_analytics")


def _ai_ml_quiz(concept_name, cn, skill_name, level):
    if "regression" in cn or "linear" in cn:
        return [
            {"question_text": "What does the R² score measure in linear regression?", "option_a": "The slope of the regression line", "option_b": "The proportion of variance in y explained by the model (1.0 = perfect)", "option_c": "The number of correct predictions", "option_d": "The training speed", "correct_answer": "B", "explanation": "R² (coefficient of determination) measures how much variance in the target variable the model explains. R² = 1.0 means perfect prediction. R² = 0 means the model is no better than predicting the mean."},
            {"question_text": "What does gradient descent minimise in linear regression?", "option_a": "The number of features", "option_b": "The mean squared error (MSE) between predictions and actual values", "option_c": "The learning rate", "option_d": "The number of training epochs", "correct_answer": "B", "explanation": "Gradient descent iteratively adjusts model weights to minimise the Mean Squared Error (MSE) — the average squared difference between predicted and actual values."},
            {"question_text": "What is overfitting in machine learning?", "option_a": "The model is too simple to capture patterns in the data", "option_b": "The model learns the training data so well it fails on new, unseen data", "option_c": "The model takes too long to train", "option_d": "The model has too few features", "correct_answer": "B", "explanation": "Overfitting = model memorises training noise instead of learning generalisable patterns. It scores high on training data but poorly on test data. Fix with more data, regularisation, or simpler models."},
            {"question_text": "Why do we split data into training and test sets?", "option_a": "To speed up training", "option_b": "To get an honest estimate of model performance on unseen data", "option_c": "Because more data makes training slower", "option_d": "Test sets are required by scikit-learn", "correct_answer": "B", "explanation": "Evaluating on training data is cheating — the model has already seen that data. The test set simulates new, unseen data and gives an honest estimate of real-world performance."},
            {"question_text": "Which metric is best for evaluating a model on a severely imbalanced classification dataset (99% class A, 1% class B)?", "option_a": "Accuracy", "option_b": "Precision, Recall, and F1-Score", "option_c": "R² Score", "option_d": "Mean Absolute Error", "correct_answer": "B", "explanation": "A model that always predicts class A achieves 99% accuracy but is completely useless for class B. Precision, Recall, and F1 measure performance specifically on the minority class — much more informative."},
        ]
    else:
        return _general_quiz(concept_name, skill_name, "ai_ml")


def _cybersecurity_quiz(concept_name, cn, skill_name, level):
    return [
        {"question_text": "What should analysts use to practice security procedures?", "option_a": "Any publicly reachable system", "option_b": "A supplied local lab or synthetic dataset", "option_c": "A coworker's personal device", "option_d": "An unapproved production service", "correct_answer": "B", "explanation": "Security practice must stay in a deliberately vulnerable local lab, supplied synthetic data, or systems the learner owns and is authorized to administer."},
        {"question_text": "What is the primary purpose of parameterized database queries?", "option_a": "To separate user data from query instructions", "option_b": "To expose database errors to users", "option_c": "To store passwords in plain text", "option_d": "To disable access checks", "correct_answer": "A", "explanation": "Parameterized queries keep data separate from query structure and are a core defensive coding practice."},
        {"question_text": "Which control helps browsers restrict where scripts may load from?", "option_a": "Content Security Policy", "option_b": "A larger image cache", "option_c": "A verbose error page", "option_d": "An unencrypted cookie", "correct_answer": "A", "explanation": "A carefully configured Content Security Policy is a defense-in-depth control that can reduce script injection impact."},
        {"question_text": "What is a safe first response to repeated failed logins in supplied local logs?", "option_a": "Ignore the events", "option_b": "Review the timeline and follow the approved incident playbook", "option_c": "Attempt access to the source system", "option_d": "Publish the log publicly", "correct_answer": "B", "explanation": "Analysts should preserve evidence, assess the supplied logs, and follow approved defensive response procedures."},
        {"question_text": "What does the CIA triad represent?", "option_a": "Confidentiality, Integrity, Availability", "option_b": "Compliance, Inspection, Authorization", "option_c": "Cookies, Identity, Access", "option_d": "Containment, Investigation, Analysis", "correct_answer": "A", "explanation": "Confidentiality, Integrity, and Availability are foundational security objectives used to assess defensive controls."},
    ]


def _dsa_quiz(concept_name, cn, skill_name, level):
    if "big-o" in cn or "complexity" in cn:
        return [
            {"question_text": "What is the time complexity of looking up an element in a Python dictionary?", "option_a": "O(n)", "option_b": "O(log n)", "option_c": "O(1) on average", "option_d": "O(n²)", "correct_answer": "C", "explanation": "Hash maps (Python dicts) provide O(1) average lookup because they use a hash function to compute the array index directly. Worst case is O(n) on hash collisions, but rare in practice."},
            {"question_text": "An algorithm processes 1,000 elements in 1ms. At O(n²), how long for 10,000 elements?", "option_a": "10ms", "option_b": "100ms", "option_c": "1,000ms", "option_d": "10,000ms", "correct_answer": "B", "explanation": "O(n²): 10× input = 100× time. 1,000 → 1ms; 10,000 → 1ms × (10,000/1,000)² = 100ms. This is why O(n²) algorithms become unusable on large inputs."},
            {"question_text": "What is the time complexity of binary search on a sorted array?", "option_a": "O(n)", "option_b": "O(n²)", "option_c": "O(log n)", "option_d": "O(1)", "correct_answer": "C", "explanation": "Binary search halves the search space each step. For 1,000,000 elements, it takes at most log₂(1,000,000) ≈ 20 steps. That's why sorted data + binary search is incredibly efficient."},
            {"question_text": "Why is O(n log n) considered optimal for comparison-based sorting algorithms?", "option_a": "It's not — O(n) sorting always exists", "option_b": "It's a theoretical lower bound proven by information theory", "option_c": "Sorting algorithms can't be faster than O(n²)", "option_d": "Only because hardware limitations", "correct_answer": "B", "explanation": "Information theory proves any comparison-based sort must make at least O(n log n) comparisons in the worst case. Merge sort and heap sort achieve this. Counting sort bypasses comparisons and can do O(n) — but requires specific constraints."},
            {"question_text": "Which data structure provides O(1) push and pop from the same end?", "option_a": "Queue", "option_b": "Stack", "option_c": "Linked List (from middle)", "option_d": "Binary Tree", "correct_answer": "B", "explanation": "A Stack (LIFO — Last In, First Out) provides O(1) push (add) and pop (remove) from the top. A Queue (FIFO) provides O(1) enqueue and dequeue but from opposite ends."},
        ]
    else:
        return _general_quiz(concept_name, skill_name, "dsa")


def _sql_quiz(concept_name, cn, skill_name, level):
    if "select" in cn or "where" in cn or "query" in cn:
        return [
            {"question_text": "What does `SELECT *` return?", "option_a": "Only the first row of the table", "option_b": "All columns from all rows (matching WHERE clause if present)", "option_c": "Only unique rows", "option_d": "The count of all rows", "correct_answer": "B", "explanation": "SELECT * retrieves all columns. In production, it's usually better to select specific columns — it's faster, more readable, and won't break if the table schema changes."},
            {"question_text": "How do you check if a value IS missing (NULL) in SQL?", "option_a": "WHERE column = NULL", "option_b": "WHERE column == NULL", "option_c": "WHERE column IS NULL", "option_d": "WHERE column = 'NULL'", "correct_answer": "C", "explanation": "NULL cannot be compared with = because NULL = NULL is NULL (unknown), not TRUE. Always use IS NULL or IS NOT NULL."},
            {"question_text": "What does ORDER BY column DESC do?", "option_a": "Sorts alphabetically A–Z", "option_b": "Sorts from largest/latest to smallest/earliest", "option_c": "Groups rows by the column", "option_d": "Removes duplicate values", "correct_answer": "B", "explanation": "DESC (descending) sorts from highest to lowest — for numbers: 9,8,7...; for dates: most recent first; for text: Z–A. ASC (default) sorts lowest to highest."},
            {"question_text": "What is the purpose of LIMIT in a SELECT query?", "option_a": "Limits the number of columns returned", "option_b": "Limits the maximum value in a column", "option_c": "Restricts how many rows are returned in the result", "option_d": "Prevents updates to the queried table", "correct_answer": "C", "explanation": "LIMIT N returns only the first N rows of the result set. Essential for pagination (LIMIT 20 OFFSET 40), testing queries on large tables, and 'top N' reports."},
            {"question_text": "In SQL, what is a primary key?", "option_a": "The most important column for business analysis", "option_b": "A unique, non-null identifier for each row in a table", "option_c": "The first column in the table", "option_d": "A column used in JOIN conditions", "correct_answer": "B", "explanation": "A primary key uniquely identifies each row — it must be unique and cannot be NULL. It's often an auto-incrementing integer (id). Foreign keys in other tables reference it to create relationships."},
        ]
    else:
        return _general_quiz(concept_name, skill_name, "sql_databases")


def _general_quiz(concept_name, skill_name, domain_key="general"):
    return [
        {"question_text": f"What is the primary purpose of {concept_name}?", "option_a": "To add complexity to the codebase", "option_b": f"To solve a specific, well-defined problem in {skill_name}", "option_c": "To slow down execution", "option_d": "It has no specific purpose", "correct_answer": "B", "explanation": f"Every concept in {skill_name} exists to solve a specific problem. {concept_name} is no exception — always ask 'what problem does this solve?' before learning the syntax."},
        {"question_text": f"What is the best first step when learning {concept_name}?", "option_a": "Memorise all syntax and edge cases immediately", "option_b": "Build a complex project right away", "option_c": "Understand the 'why' and practise with simple examples", "option_d": "Skip it and go straight to advanced topics", "correct_answer": "C", "explanation": "Always start with why the concept exists and what problem it solves. Simple examples build the mental model before you tackle complex use cases."},
        {"question_text": f"Which is a common mistake beginners make with {concept_name}?", "option_a": "Asking for help when stuck", "option_b": "Reading the official documentation", "option_c": "Trying too many approaches at once before mastering one", "option_d": "Writing simple test cases", "correct_answer": "C", "explanation": "Jumping between approaches before mastering one is the most common beginner mistake. Focus, master one approach fully, then explore alternatives."},
        {"question_text": f"How does {concept_name} connect to the broader skill of {skill_name}?", "option_a": "It doesn't — they are completely unrelated", "option_b": f"It is a foundational building block that other {skill_name} concepts depend on", "option_c": "It is only used in advanced scenarios", "option_d": "It replaces everything else in the skill", "correct_answer": "B", "explanation": f"Foundational concepts in {skill_name} are prerequisites for everything else. Understanding {concept_name} deeply makes every subsequent concept easier to learn and apply."},
        {"question_text": f"What is the most effective way to verify you have truly understood {concept_name}?", "option_a": "Re-reading the lesson text multiple times", "option_b": "Watching a video explanation", "option_c": "Implementing it from scratch without looking at reference code", "option_d": "Memorising the example code", "correct_answer": "C", "explanation": "Real understanding means you can implement from scratch. If you can't build it without looking at notes, you've memorised rather than understood. Build → break → fix → understand."},
    ]


# =============================================================================
# MAIN ORCHESTRATOR CLASS
# =============================================================================

class EXAOrchestrator:
    """
    EXA Orchestrator — Domain-aware learning engine.
    Generates curricula, skill maps, lessons, quizzes, and mentor responses
    tailored to the user's actual selected domain and skill.
    """

    # ------------------------------------------------------------------
    # GOAL ANALYSIS & CURRICULUM GENERATION
    # ------------------------------------------------------------------

    @classmethod
    def analyze_goal_and_skills(cls, goal: str, level: str, domain: str, skills: str) -> Dict[str, Any]:
        """Generate a domain-appropriate course curriculum and Expert Mentor."""
        domain_key = detect_domain(domain, goal)
        print(f"DEBUG: domain={domain!r}, goal={goal!r}, detected={domain_key!r}")

        if domain_key in CURRICULA:
            curriculum = CURRICULA[domain_key]
            return {
                "expert_agent_name": curriculum["expert_name"],
                "expert_agent_intro": curriculum["intro"],
                "skill_nodes": curriculum["levels"]
            }
        else:
            return synthesize_custom_roadmap(goal, domain, level, skills)

    # ------------------------------------------------------------------
    # INITIAL ASSESSMENT
    # ------------------------------------------------------------------

    @classmethod
    def generate_initial_assessment(cls, skill_name: str, domain: str, level: str) -> Dict[str, Any]:
        """Generate initial diagnostic questions before teaching begins."""
        level_lower = level.lower()

        if "beginner" in level_lower or "not sure" in level_lower:
            questions = [
                {
                    "question": f"What is your current experience with {skill_name}?",
                    "prompt": f"What is your current experience with {skill_name}?",
                    "topic": "Current Familiarity",
                    "options": [
                        "Complete beginner — I've never used this before",
                        "I've read about it or seen basic tutorials",
                        "I've written a few simple programs or scripts",
                        "I understand the basics and want to build real projects"
                    ],
                    "type": "choice"
                },
                {
                    "question": f"What is your main priority while learning {skill_name}?",
                    "prompt": f"What is your main priority while learning {skill_name}?",
                    "topic": "Learning Goal",
                    "options": [
                        "Understand the core concepts step-by-step",
                        "See practical, real-world examples immediately",
                        "Learn best practices and avoid common mistakes",
                        "Prepare for technical interviews and portfolio projects"
                    ],
                    "type": "choice"
                },
                {
                    "question": "How do you best understand new technical concepts?",
                    "prompt": "How do you best understand new technical concepts?",
                    "topic": "Learning Style",
                    "options": [
                        "Step-by-step explanation with clear examples",
                        "Working code to read and modify",
                        "Real-world analogies and use cases",
                        "Exercises and quizzes to test understanding"
                    ],
                    "type": "choice"
                }
            ]
        elif "intermediate" in level_lower:
            questions = [
                {
                    "question": f"Rate your practical comfort level with {skill_name}:",
                    "prompt": f"Rate your practical comfort level with {skill_name}:",
                    "topic": "Practical Level",
                    "options": [
                        "I know syntax but get stuck when building real features",
                        "I can build features but frequently look things up",
                        "Comfortable with standard workflows; want to master patterns",
                        "Advanced practitioner wanting to polish edge cases and scale"
                    ],
                    "type": "choice"
                },
                {
                    "question": f"What is your biggest challenge with {skill_name}?",
                    "prompt": f"What is your biggest challenge with {skill_name}?",
                    "topic": "Main Challenge",
                    "options": [
                        "Structuring clean, maintainable, modular code",
                        "Debugging complex or unexpected behaviour",
                        "Integrating with external libraries, APIs, and services",
                        "Performance optimisation and handling edge cases at scale"
                    ],
                    "type": "choice"
                },
                {
                    "question": f"How do you prefer to deepen your {skill_name} knowledge?",
                    "prompt": f"How do you prefer to deepen your {skill_name} knowledge?",
                    "topic": "Learning Preference",
                    "options": [
                        "Deep architectural breakdowns with code walkthroughs",
                        "Short quizzes testing edge cases and tricky scenarios",
                        "Comparing bad patterns vs clean production-grade patterns",
                        "Hands-on project challenges with real requirements"
                    ],
                    "type": "choice"
                }
            ]
        else:
            questions = [
                {
                    "question": f"Which aspect of {skill_name} is your primary focus?",
                    "prompt": f"Which aspect of {skill_name} is your primary focus?",
                    "topic": "Advanced Focus",
                    "options": [
                        "High-throughput architecture and distributed systems design",
                        "Security hardening, authentication, and compliance",
                        "Performance profiling, optimisation, and low-latency systems",
                        "Team leadership, design patterns, and engineering excellence"
                    ],
                    "type": "choice"
                },
                {
                    "question": f"What is your production experience with {skill_name}?",
                    "prompt": f"What is your production experience with {skill_name}?",
                    "topic": "Production Experience",
                    "options": [
                        "Personal projects and small proofs of concept",
                        "Contributed to 1–2 small production features",
                        "Regularly maintaining medium-to-large production systems",
                        "Senior engineer designing high-scale enterprise systems"
                    ],
                    "type": "choice"
                },
                {
                    "question": f"What is your target outcome for mastering {skill_name}?",
                    "prompt": f"What is your target outcome for mastering {skill_name}?",
                    "topic": "Target Outcome",
                    "options": [
                        "Crack Senior/Staff Engineer technical interviews",
                        "Lead system design and architectural decisions in my team",
                        "Build and ship my own scalable product or service",
                        "Deep specialisation, research, and architectural mastery"
                    ],
                    "type": "choice"
                }
            ]

        return {
            "questions": questions,
            "mentor_intro": f"Let's start with a few quick questions about {skill_name}. No grades—just a way to focus on what matters to you."
        }

    # ------------------------------------------------------------------
    # SKILL MAP
    # ------------------------------------------------------------------

    @classmethod
    def generate_skill_map(cls, skill_name: str, domain: str, level: str, assessment_answers: list) -> Dict[str, Any]:
        """Generate a concept map for the skill based on domain and level."""
        domain_key = detect_domain(domain, "", skill_name)
        concepts = get_skill_map_concepts(skill_name, domain_key, level)

        return {
            "concepts": concepts,
            "summary": f"Your personalised learning map for {skill_name} has {len(concepts)} focused concepts. We'll master them one at a time — explanation, code practice, and a 5-question quiz for each.",
            "mentor_message": f"Take your time with {skill_name}. Ask questions as you go—steady progress beats rushing. 💪"
        }

    # ------------------------------------------------------------------
    # CONCEPT LESSON
    # ------------------------------------------------------------------

    @classmethod
    def generate_concept_lesson(cls, concept_name: str, skill_name: str, domain: str, level: str) -> Dict[str, Any]:
        """Generate a thorough, domain-specific lesson for a single concept."""
        domain_key = detect_domain(domain, "", skill_name)
        return generate_lesson_for_domain(concept_name, skill_name, domain_key, level)

    # ------------------------------------------------------------------
    # QUIZ QUESTIONS
    # ------------------------------------------------------------------

    @classmethod
    def generate_quiz_questions(cls, concept_name: str, skill_name: str, domain: str, level: str) -> List[Dict[str, Any]]:
        """Generate 5 domain-specific MCQ questions for a concept."""
        domain_key = detect_domain(domain, "", skill_name)
        return generate_quiz_for_domain(concept_name, skill_name, domain_key, level)

    # ------------------------------------------------------------------
    # QUIZ EVALUATION
    # ------------------------------------------------------------------

    @classmethod
    def evaluate_quiz(cls, questions_data: list, user_answers: list) -> Dict[str, Any]:
        """Evaluate quiz answers. Pass threshold: 4/5 (80%)."""
        score = 0
        feedback = []
        total = len(questions_data)

        for i, q in enumerate(questions_data):
            user_answer = user_answers[i] if i < len(user_answers) else ''
            is_correct = user_answer.upper() == q.get('correct_answer', '').upper()
            if is_correct:
                score += 1
            feedback.append({
                "question_num": i + 1,
                "question_text": q.get('question_text', ''),
                "user_answer": user_answer.upper(),
                "correct_answer": q.get('correct_answer', ''),
                "is_correct": is_correct,
                "explanation": q.get('explanation', ''),
                "user_option_text": q.get(f'option_{user_answer.lower()}', '') if user_answer else '',
                "correct_option_text": q.get(f'option_{q.get("correct_answer", "a").lower()}', ''),
            })

        # Pass at 80% (4/5) — not requiring a perfect 5/5
        is_passed = score >= max(1, round(total * 0.8))

        return {
            "score": score,
            "total": total,
            "is_passed": is_passed,
            "feedback": feedback,
        }

    # ------------------------------------------------------------------
    # APPLAUSE MESSAGE
    # ------------------------------------------------------------------

    @classmethod
    def generate_applause_message(cls, skill_name: str, concept_name: str, score: int) -> str:
        msgs = [
            f"🎉 Excellent! {score}/5 on {concept_name}! Your understanding is solid — that's what mastery looks like.",
            f"🏆 Great work! You passed {concept_name} with {score}/5. You're building real, lasting knowledge.",
            f"⭐ Well done! {score}/5 on {concept_name}! Each concept you master makes the next one easier.",
            f"💪 Solid pass! {score}/5 on {concept_name}. You're proving your competence one step at a time.",
            f"🌟 Passed! {score}/5 on {concept_name}. Understanding > memorisation — and you've shown you understand.",
        ]
        return random.choice(msgs)

    # ------------------------------------------------------------------
    # REVIEW FEEDBACK
    # ------------------------------------------------------------------

    @classmethod
    def generate_review_feedback(cls, wrong_questions: list, concept_name: str, skill_name: str, score: int, total: int) -> Dict[str, Any]:
        """Generate targeted feedback for missed quiz questions."""
        weak_areas = []
        for q in wrong_questions:
            weak_areas.append({
                "question": q.get("question_text", ""),
                "your_answer": q.get("user_option_text", ""),
                "correct_answer": q.get("correct_option_text", ""),
                "explanation": q.get("explanation", ""),
                "improvement_tip": f"Re-read the explanation and ask yourself: WHY is '{q.get('correct_option_text', '')}' correct? Understanding the reason, not memorising the answer, is what builds lasting knowledge."
            })

        if score >= 4:
            encouragement = f"You scored {score}/{total} — really close! Just one concept to sharpen. Review it quickly and you'll ace the retake."
            tone = "almost_perfect"
        elif score >= 3:
            encouragement = f"You got {score}/{total} — solid foundation! You understand the core idea, and there are a few details to reinforce. Let's go through them together."
            tone = "good_effort"
        elif score >= 2:
            encouragement = f"You got {score}/{total}. No worries — this is how learning works. Review the explanations below carefully; I'll walk you through each one."
            tone = "encouraging"
        else:
            encouragement = f"You scored {score}/{total}. That's okay — every expert started exactly where you are. Let me explain this concept differently. A fresh angle often makes everything click."
            tone = "supportive"

        return {
            "score": score,
            "total": total,
            "weak_areas": weak_areas,
            "encouragement": encouragement,
            "tone": tone,
            "mentor_advice": f"Focus on the {len(weak_areas)} question(s) you missed. Read the explanations carefully. When you feel ready, take the quiz again — there's no time limit. 🌱",
            "reteach_summary": f"Let me re-explain the parts of {concept_name} that need more work. The key is understanding WHY each correct answer is right, not just memorising the letter."
        }

    # ------------------------------------------------------------------
    # LEGACY: LEARNING SESSION (backward compatibility)
    # ------------------------------------------------------------------

    @classmethod
    def generate_learning_session(cls, skill_name: str, domain: str, level: str) -> Dict[str, Any]:
        """Legacy method — generates a basic learning session."""
        lesson = cls.generate_concept_lesson(skill_name, skill_name, domain, level)
        return {
            "concept": lesson.get("core_concept", ""),
            "why_it_matters": lesson.get("real_world_use_case", ""),
            "example": lesson.get("code_example", ""),
            "quick_tip": lesson.get("pro_tip", ""),
            "practice_prompt": lesson.get("thinking_exercise", ""),
        }

    # ------------------------------------------------------------------
    # PRACTICE EVALUATION
    # ------------------------------------------------------------------

    @classmethod
    def evaluate_practice(cls, answer: str, context: str) -> Dict[str, Any]:
        """Evaluate a practice submission."""
        if len((answer or "").strip()) > 10:
            return {
                "success": True,
                "feedback": "Good attempt! You've demonstrated an understanding of the concept. Review the explanation to refine your answer.",
                "weakness_detected": False,
                "next_action": "Proceed to the quiz to test your knowledge."
            }
        return {
            "success": False,
            "feedback": "Please provide a more complete answer — explain your thinking, write the code, or describe the approach in detail.",
            "weakness_detected": True,
            "next_action": "Review the concept and try again with a more complete response."
        }

    # ------------------------------------------------------------------
    # PROJECT GENERATION
    # ------------------------------------------------------------------

    @classmethod
    def generate_project(cls, goal: str, level: str, skill_name: str = "") -> Dict[str, Any]:
        """Generate a domain-appropriate capstone project."""
        domain_key = detect_domain("", goal, skill_name)
        sn = skill_name.lower()
        lv = level.lower()

        if domain_key == "python":
            if "1" in sn or "foundation" in sn:
                return {"title": "Python Foundations Project: Command-Line Task Manager", "objective": "Build a fully working command-line task manager in Python that allows users to add tasks, mark them complete, list all tasks, and save/load tasks from a JSON file.", "requirements": "Milestone 1: Accept user input via input(), store tasks in a list of dictionaries.\nMilestone 2: Implement save (json.dump) and load (json.load) to persist tasks between runs.\nMilestone 3: Implement add, list, complete, and delete commands with clear error handling.", "evaluation_criteria": "1. All commands work correctly without crashing.\n2. Tasks persist to file and load correctly on restart.\n3. Edge cases handled (empty list, invalid input, missing file)."}
            else:
                return {"title": "Python Advanced Project: REST API Client & Data Pipeline", "objective": "Build a Python application that fetches data from a public REST API, processes it with Pandas, and generates a clean summary report saved as CSV.", "requirements": "Milestone 1: Fetch data using requests or httpx with error handling and retries.\nMilestone 2: Parse JSON response into a Pandas DataFrame; clean and transform.\nMilestone 3: Generate summary statistics and save to CSV with proper column headers.", "evaluation_criteria": "1. API requests handle errors (timeouts, HTTP errors) gracefully.\n2. Pandas operations are vectorised (no row-by-row loops).\n3. Output CSV is clean, correctly typed, and documented."}

        elif domain_key == "web_dev":
            return {"title": "Full-Stack Web App: Personal Portfolio with Contact Form API", "objective": "Build and deploy a responsive personal portfolio website with HTML/CSS/JS frontend, a Node.js/Express backend API for contact form submissions, and a SQLite database.", "requirements": "Milestone 1 (Frontend): Responsive HTML/CSS portfolio with sections for About, Projects, Skills. Mobile-first design with Flexbox/Grid.\nMilestone 2 (Backend): Express API endpoint POST /contact that validates and stores form submissions in SQLite.\nMilestone 3 (Deployment): Deploy frontend to Netlify/Vercel; backend to Render. Configure CORS and environment variables.", "evaluation_criteria": "1. Layout is fully responsive from 320px to 1440px.\n2. API validates input (name, email required) and returns proper status codes.\n3. Successfully deployed and accessible via public URLs."}

        elif domain_key == "data_analytics":
            if "level 1" in sn or "foundation" in sn:
                return {"title": "Level 1: Small Business Retail Data Audit & KPI Framework", "objective": "Audit retail transaction data, identify quality issues, define 4 KPIs, and write an executive summary.", "requirements": "Milestone 1: Audit rows for missing IDs, negative prices, duplicates.\nMilestone 2: Define Net Revenue, Gross Margin %, Average Basket Size, Repeat Rate.\nMilestone 3: Write a 3-paragraph executive summary.", "evaluation_criteria": "1. Data quality issues comprehensively identified.\n2. KPI definitions are mathematically correct.\n3. Executive summary is clear and jargon-free."}
            elif "sql" in sn or "level 4" in sn:
                return {"title": "Level 4: SaaS Retention & Cohort Analysis in SQL", "objective": "Write relational SQL across subscriptions, users, and billing tables. Compute monthly actives, churn, and running revenue.", "requirements": "Milestone 1: INNER + LEFT JOINs combining user profiles with invoice logs.\nMilestone 2: GROUP BY/HAVING for enterprise accounts > $5,000 ARR.\nMilestone 3: CTE + Window Functions for running revenue and churn identification.", "evaluation_criteria": "1. All queries are syntactically valid and correctly formatted.\n2. JOIN logic is accurate — no Cartesian products.\n3. Window functions applied correctly."}
            else:
                return {"title": "Data Analytics Capstone: End-to-End Business Analysis Project", "objective": "Combine SQL, Excel/Python, and storytelling to produce a complete analytics deliverable for a simulated business problem.", "requirements": "Milestone 1: SQL data extraction with multi-table JOINs.\nMilestone 2: Python or Excel analysis with visualisations.\nMilestone 3: Executive presentation with findings and recommendations.", "evaluation_criteria": "1. Multi-tool integration demonstrated.\n2. Findings are data-supported and quantified.\n3. Recommendations are actionable and clearly presented."}

        elif domain_key == "ai_ml":
            return {"title": "ML Project: End-to-End Customer Churn Prediction", "objective": "Build a complete binary classification pipeline to predict customer churn: data cleaning, feature engineering, model training, evaluation, and a brief model card.", "requirements": "Milestone 1: Load dataset, handle missing values, encode categoricals, split train/test.\nMilestone 2: Train at least 2 models (Logistic Regression + Random Forest), tune hyperparameters.\nMilestone 3: Evaluate with precision, recall, F1, ROC-AUC. Write a model card documenting performance and limitations.", "evaluation_criteria": "1. Data pipeline handles edge cases (missing values, unseen categories).\n2. Model evaluation uses appropriate metrics (not just accuracy).\n3. Model card honestly documents capabilities and limitations."}

        elif domain_key == "cybersecurity":
            return {
                "title": "Defensive Security Lab: Local Findings and Remediation Report",
                "objective": "Review a deliberately vulnerable local training application or supplied synthetic logs, document defensive findings, and recommend safe remediations.",
                "requirements": "Milestone 1: Use only the supplied local lab, local logs, or provided packet capture.\nMilestone 2: Describe observed risks at a high level and apply or propose defensive fixes.\nMilestone 3: Record evidence, remediation priorities, and verification steps without contacting external systems.",
                "evaluation_criteria": "1. Work remains within supplied local/authorized materials.\n2. Findings are evidence-based and framed defensively.\n3. Remediations are practical, prioritized, and verified safely."
            }

        elif domain_key == "dsa":
            return {"title": "DSA Project: Implement & Benchmark Core Data Structures", "objective": "Implement a LinkedList, Stack, Queue, and Binary Search Tree from scratch in Python. Add unit tests and a benchmark comparing performance against Python builtins.", "requirements": "Milestone 1: Implement each structure with core operations (insert, delete, search, traverse).\nMilestone 2: Write pytest unit tests with edge cases (empty structure, single element, duplicates).\nMilestone 3: Benchmark insert and search operations at 1k, 10k, 100k elements. Plot results.", "evaluation_criteria": "1. All structures handle edge cases without errors.\n2. Test suite covers normal, edge, and error cases.\n3. Benchmark analysis correctly identifies time complexity from results."}

        elif domain_key == "robotics":
            return {
                "title": "Autonomous Mobile Robot Navigation & Obstacle Avoidance Project",
                "objective": "Build and simulate an autonomous robot system in Python/ROS 2 that reads sensor data, maps an environment, and navigates between waypoints while avoiding obstacles.",
                "requirements": "Milestone 1: Create a simulation world and robot model with LiDAR and wheel odometry sensors.\nMilestone 2: Implement a ROS 2 node that subscribes to /scan and publishes /cmd_vel velocity commands.\nMilestone 3: Implement an obstacle avoidance algorithm (state machine or potential fields) to navigate to the goal safely.",
                "evaluation_criteria": "1. Robot successfully reaches the target waypoint without collisions.\n2. ROS 2 node architecture is clean with separate publisher and subscriber callbacks.\n3. Odometry and sensor transform (TF2) tree is correctly defined."
            }

        elif domain_key == "ui_ux":
            return {
                "title": "UI/UX Capstone: End-to-End Product Design Case Study",
                "objective": "Design a complete digital product from initial user research and wireframing to an interactive, accessible Figma prototype with design system specifications.",
                "requirements": "Milestone 1: User research synthesis, problem statement, user personas, and information architecture flow.\nMilestone 2: Low-to-mid fidelity wireframes and user journey validation.\nMilestone 3: High-fidelity interactive prototype with reusable component design tokens and WCAG AA contrast compliance.",
                "evaluation_criteria": "1. Comprehensive design rationale backed by user research.\n2. Design system demonstrates consistent typography, 8pt grid, and accessible components.\n3. Prototype is interactive with realistic micro-animations and developer specs."
            }

        else:
            lvl_word = "Beginner" if ("beginner" in lv or "1" in lv) else "Professional"
            return {
                "title": f"{goal.title()} — {lvl_word} Capstone Project",
                "objective": f"Build a complete, working project that demonstrates your end-to-end mastery of {goal}.",
                "requirements": "Milestone 1: Project architecture, setup, and core feature implementation.\nMilestone 2: Error handling, edge cases, and input validation.\nMilestone 3: Testing, documentation, and a working demonstration.",
                "evaluation_criteria": "1. Project runs correctly without uncaught errors.\n2. Core requirements are fully implemented.\n3. Code is clean, readable, and documented."
            }

    # ------------------------------------------------------------------
    # PROJECT EVALUATION
    # ------------------------------------------------------------------

    @classmethod
    def evaluate_project_submission(cls, submission_text: str, goal: str, domain: str, level: str) -> Dict[str, Any]:
        """Evaluate a project submission with honest rubric-based feedback."""
        text = (submission_text or "").strip()
        word_count = len(text.split())

        if word_count < 15:
            return {
                "is_passed": False,
                "score": 40,
                "feedback": "Your submission is too brief to evaluate fairly. Please paste your actual code, SQL queries, analysis steps, or a detailed description of what you built for each milestone.",
                "strengths": ["Attempt submitted — good start!"],
                "improvements": ["Include the actual code or queries you wrote", "Describe your approach for each milestone", "Explain what you found or built and any challenges you overcame"],
                "next_action": "Expand your submission with your actual work and resubmit."
            }

        has_code = any(k in text for k in ["def ", "class ", "import ", "SELECT ", "function ", "const ", "<html", "docker", "kubectl"])
        has_analysis = any(k in text.lower() for k in ["found", "result", "analysis", "shows", "indicates", "recommend", "milestone"])
        has_link = "http" in text.lower() or "github" in text.lower()
        has_pdf = ".pdf" in text.lower() or "pdf report" in text.lower()
        level_match = re.search(r"(?:level\s*)?(\d+)", level or "", re.IGNORECASE)
        level_number = int(level_match.group(1)) if level_match else 1
        live_demo_required = level_number >= 5
        has_live_link = "http" in text.lower() and any(
            marker in text.lower() for marker in ("live", "demo", "render", "vercel", "netlify")
        )

        score = 75
        strengths = ["Submitted a substantive response"]
        improvements = ["Consider adding more detail about your decision-making process"]

        if has_code:
            score += 10
            strengths.append("Included actual code or queries — good evidence of implementation")
        if has_analysis:
            score += 5
            strengths.append("Demonstrates analytical thinking and milestone completion")
        if has_link:
            score += 5
            strengths.append("Provided a link to your work — excellent for portfolio visibility")

        score = min(score, 97)
        missing_evidence = not has_pdf or (live_demo_required and not has_live_link)
        if missing_evidence:
            score = min(score, 40)
            improvements.append(
                "Submit the PDF report" + (" and the required live-demo link" if live_demo_required else "")
                + "; missing required evidence caps the score at 40."
            )
        is_passed = score >= 60

        return {
            "is_passed": is_passed,
            "score": score,
            "feedback": f"Your project submission demonstrates {'solid' if score >= 85 else 'adequate'} understanding of the concepts covered. {'Your code and methodology are clear.' if has_code else 'Adding your actual code or queries would strengthen the evaluation.'}",
            "strengths": strengths,
            "improvements": improvements + (["Add automated tests or validation to show your code handles edge cases"] if score < 90 else []),
            "next_action": "Project passed! Your next level is now unlocked." if is_passed else "Review the feedback, revise your submission, and resubmit."
        }

    # ------------------------------------------------------------------
    # AI MENTOR CHAT
    # ------------------------------------------------------------------

    @classmethod
    def respond_to_learner_query(
        cls,
        query: str,
        goal: str = "",
        domain: str = "",
        level: str = "",
        current_skill_name: str = "",
        current_concept_name: str = "",
        context_mode: str = "general"
    ) -> str:
        """Respond to learner questions with domain-aware, personalised guidance."""
        q = (query or "").strip()
        q_lower = q.lower()
        context_info = current_concept_name or current_skill_name or goal or "your current topic"
        domain_key = detect_domain(domain, goal, current_skill_name)

        # 1. Quiz/assessment mode — give conceptual clues only
        if context_mode == "quiz" or any(w in q_lower for w in ["what is the answer", "tell me the answer", "correct option", "give me option", "which letter"]):
            return (
                f"🎯 **Assessment Guidance**\n\n"
                f"I want you to experience the satisfaction of working this out yourself! I won't reveal the answer letter, but here's a conceptual clue:\n\n"
                f"💡 **Think about:** What is the *purpose* of the thing being asked about? What problem does it solve? Eliminate options that don't fit that purpose.\n\n"
                f"Re-read the lesson on **{context_info}** and look for the option that most accurately describes what we learned. You've got this! 💪"
            )

        # 2. Domain-specific responses
        if domain_key == "python":
            if any(w in q_lower for w in ["error", "exception", "traceback", "bug", "debug"]):
                return (
                    f"🐍 **Debugging Python Errors**\n\n"
                    f"**Step 1 — Read the traceback bottom-up.** The last line tells you the error type and message. The lines above show exactly where it happened.\n\n"
                    f"**Common Python errors:**\n"
                    f"- `NameError` — variable used before being defined\n"
                    f"- `TypeError` — wrong type (e.g., adding str + int)\n"
                    f"- `IndexError` — list index out of range\n"
                    f"- `KeyError` — dictionary key doesn't exist\n"
                    f"- `AttributeError` — calling method that doesn't exist on the object\n\n"
                    f"**Step 2 — Add `print()` statements** at each step to see what values actually are vs what you expect.\n\n"
                    f"**Step 3** — Can you paste the exact error message? I'll help you trace the root cause! 🔍"
                )
            elif any(w in q_lower for w in ["list", "dictionary", "dict", "tuple", "set"]):
                return (
                    f"🐍 **Python Data Structures Quick Reference**\n\n"
                    f"- **list** `[]` — ordered, mutable, allows duplicates. Use for sequences.\n"
                    f"- **tuple** `()` — ordered, IMMUTABLE, allows duplicates. Use for fixed data (coordinates, RGB).\n"
                    f"- **dict** `{{}}` — key-value pairs, O(1) lookup. Use when you need to look up by name.\n"
                    f"- **set** `{{}}` — unordered, no duplicates, O(1) membership test. Use for uniqueness checks.\n\n"
                    f"**Choosing the right one:**\n"
                    f"'I need to store a sequence and change it' → list\n"
                    f"'I need to look up data by a name/ID' → dict\n"
                    f"'I need only unique values' → set\n"
                    f"'I need fixed, unchangeable data' → tuple\n\n"
                    f"What specifically are you working with in **{context_info}**? I can give a more targeted example!"
                )

        if domain_key == "cybersecurity":
            if any(w in q_lower for w in ["hack", "exploit", "attack", "break into"]):
                return (
                    f"🔐 **Ethical Hacking Guidance**\n\n"
                    f"Great question about offensive security! Remember: **only test systems you own or have explicit written permission to test.** Unauthorised access is illegal everywhere.\n\n"
                    f"For your learning in **{context_info}**, practise on:\n"
                    f"- **DVWA** (Damn Vulnerable Web Application) — runs locally\n"
                    f"- **HackTheBox** — legal CTF challenges\n"
                    f"- **TryHackMe** — guided ethical hacking labs\n"
                    f"- **VulnHub** — downloadable vulnerable VMs\n\n"
                    f"What specific technique or vulnerability are you trying to understand? I'll explain the concept and a safe way to practise it! 🛡️"
                )

        if domain_key == "data_analytics":
            if any(w in q_lower for w in ["xlookup", "vlookup", "index match", "lookup"]):
                return (
                    f"📊 **Excel Lookups Explained**\n\n"
                    f"**XLOOKUP** (modern, recommended):\n"
                    f"`=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found])`\n\n"
                    f"**Example:** Find the price for product in A2, searching column D, returning column E:\n"
                    f"`=XLOOKUP(A2, D:D, E:E, \"Not Found\")`\n\n"
                    f"**Why XLOOKUP beats VLOOKUP:**\n"
                    f"✅ Doesn't break when you insert columns\n"
                    f"✅ Exact match by default (no FALSE parameter needed)\n"
                    f"✅ Can search left-to-right OR right-to-left\n"
                    f"✅ Returns a custom message when not found\n\n"
                    f"Still using VLOOKUP? Type `=XLOOKUP(` and press Tab — Excel will guide you through each argument! 📌"
                )
            if any(w in q_lower for w in ["join", "left join", "inner join", "sql join"]):
                return (
                    f"🗄️ **SQL JOINs — Quick Guide**\n\n"
                    f"**INNER JOIN** — Only rows that match in BOTH tables:\n"
                    f"```sql\nSELECT c.name, o.total\nFROM customers c\nINNER JOIN orders o ON c.id = o.customer_id;\n```\n\n"
                    f"**LEFT JOIN** — ALL rows from left table; NULL for unmatched right:\n"
                    f"```sql\nSELECT c.name, o.total\nFROM customers c\nLEFT JOIN orders o ON c.id = o.customer_id;\n-- Customers with no orders appear with NULL total\n```\n\n"
                    f"**Pro tip:** Use LEFT JOIN + WHERE right_table.id IS NULL to find rows with NO match — 'customers who never ordered'.\n\n"
                    f"Which type of JOIN are you trying to use in **{context_info}**?"
                )

        if domain_key == "ai_ml":
            if any(w in q_lower for w in ["overfitting", "underfitting", "bias", "variance"]):
                return (
                    f"🤖 **Overfitting vs Underfitting**\n\n"
                    f"**Overfitting** — model too complex, memorises training data, fails on new data.\n"
                    f"- Symptom: High training accuracy, low test accuracy.\n"
                    f"- Fix: More data, regularisation (L1/L2), dropout, simpler model, cross-validation.\n\n"
                    f"**Underfitting** — model too simple, can't capture patterns.\n"
                    f"- Symptom: Low accuracy on BOTH training and test sets.\n"
                    f"- Fix: More features, more complex model, train longer, remove regularisation.\n\n"
                    f"**The Bias-Variance Tradeoff:**\n"
                    f"- High bias = underfitting (model is too simple)\n"
                    f"- High variance = overfitting (model is too sensitive to training data)\n"
                    f"- Goal: Find the sweet spot — generalises well to new data.\n\n"
                    f"Are you seeing overfitting or underfitting in **{context_info}**? Tell me your train vs test accuracy and I'll help diagnose! 📊"
                )

        # 3. General simplification request
        if any(w in q_lower for w in ["simple", "simpler", "confused", "don't understand", "eli5", "explain again"]):
            return (
                f"🤝 **Let me explain {context_info} differently!**\n\n"
                f"Don't worry — feeling confused at first is completely normal and part of learning. Let me try a different angle:\n\n"
                f"**Think of it this way:** Every concept in programming or technology exists because someone had a problem and needed a systematic solution. Ask yourself — what problem does {context_info} solve?\n\n"
                f"**One small step:** Instead of reading the whole lesson, pick just the first key point and try to explain it back to me in your own words. That's where real understanding begins.\n\n"
                f"Which specific sentence or part of the lesson felt confusing? Tell me and I'll explain it with a fresh everyday analogy! 😊"
            )

        # 4. Domain-aware general fallback
        domain_names = {
            "python": "Python Programming",
            "web_dev": "Web Development",
            "javascript": "JavaScript",
            "data_analytics": "Data Analytics",
            "ai_ml": "AI & Machine Learning",
            "electronics": "Electronics Engineering",
            "cybersecurity": "Cybersecurity",
            "dsa": "Data Structures & Algorithms",
            "sql_databases": "SQL & Databases",
            "cloud_devops": "Cloud & DevOps",
            "software_engineering": "Software Engineering",
        }
        domain_display = domain_names.get(domain_key, goal or "your chosen field")

        return (
            f"👋 **Let's work through {domain_display} together**\n\n"
            f"You asked: *\"{q}\"*\n\n"
            f"**How this relates to {context_info}:**\n\n"
            f"Every question is a great sign — it means you're actively processing, not just passively reading. Here's how I'd approach this:\n\n"
            f"1. **Root concept:** What is the fundamental idea behind {context_info}?\n"
            f"2. **Real-world anchor:** Where have you seen this used in actual {domain_display} projects?\n"
            f"3. **Practice step:** Can you write even 5 lines of code or a brief explanation in your own words?\n\n"
            f"If you're stuck on a specific error message, paste it here and I'll help you trace it! If you want a simpler explanation of any part of the lesson, just ask and I'll try a different analogy. 🚀"
        )

    # ------------------------------------------------------------------
    # CONCEPT OVERVIEW (for overview page)
    # ------------------------------------------------------------------

    @classmethod
    def generate_concept_overview(cls, skill_name: str, domain: str, level: str) -> Dict[str, Any]:
        """Generate an overview for the concept_overview page."""
        return cls.generate_concept_lesson(
            concept_name=f"Overview of {skill_name}",
            skill_name=skill_name,
            domain=domain,
            level=level
        )
