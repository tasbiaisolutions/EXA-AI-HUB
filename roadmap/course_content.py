"""Curated 12-level course content and project review metadata."""


def _project(title, objective, requirements, evaluation, is_active):
    return {
        "title": title.replace("Draft: ", ""),
        "objective": objective,
        "requirements": requirements,
        "evaluation_criteria": evaluation,
        "is_active": is_active,
        "review_reason": "" if is_active else "Project brief is inactive.",
    }


def _level(number, title, description, project_title, project_focus, project_work, project_review, is_active):
    tier = "Beginner" if number <= 4 else "Intermediate" if number <= 8 else "Advanced"
    return {
        "name": f"Level {number}: {title}",
        "description": description,
        "importance": description,
        "tier": tier,
        "coach_level": number,
        "project_json": _project(
            project_title,
            project_focus,
            project_work,
            project_review,
            is_active,
        ),
    }


RESTRUCTURED_CURRICULA = {
    "web_dev": {
        "expert_name": "Senior Full-Stack Web Architect & Mentor",
        "intro": "A 12-level full-stack course from web fundamentals through a deployed, tested capstone. Complete each level project to unlock the next.",
        "levels": [
            _level(1, "Web basics", "DNS, HTTP/HTTPS, client-server communication, and browser developer tools.", "Draft: Web request tracing for a retail site", "A retail engineering team needs a clear map of how its storefront request travels from browser to server.", "Trace a local sample page through DNS lookup, HTTPS request, server response, and browser rendering; record observations from developer tools.", "Accurate request-flow diagram, correct protocol explanations, and reproducible browser evidence.", False),
            _level(2, "HTML", "Semantic tags, forms, input types, and accessibility basics.", "Draft: Accessible application form", "A company needs an accessible customer onboarding form.", "Build a semantic form with suitable input types, labels, keyboard navigation, and clear validation feedback.", "Semantic structure, labels and accessible names, keyboard usability, and form validation.", False),
            _level(3, "CSS", "Selectors, the box model, Flexbox, and Grid.", "Draft: Responsive product catalog", "A commerce team needs a product catalog that works on mobile and desktop.", "Style a catalog with reusable selectors, a consistent box model, Grid or Flexbox layout, and responsive breakpoints.", "Responsive layout, maintainable CSS, and correct use of the requested layout tools.", False),
            _level(4, "JavaScript basics", "Variables, functions, arrays and objects, and DOM basics.", "Responsive landing page", "A product marketing team needs a responsive launch page with interactive navigation and a lead form.", "Build a responsive landing page using semantic HTML, CSS, JavaScript variables/functions, array or object data, and basic DOM interactions.", "Responsive behavior, working DOM interactions, accessible controls, and clean code.", True),
            _level(5, "JavaScript intermediate", "Scope, closures, events, and error handling.", "Draft: Interactive customer support widget", "A SaaS company needs a browser support widget with reliable event handling.", "Build a small widget that uses scoped functions, a closure for private state, event listeners, and user-friendly error handling.", "Correct scope and closure behavior, event handling, and recoverable errors.", False),
            _level(6, "Async JavaScript", "Promises, async/await, Fetch API, and the event loop.", "Draft: Live inventory status panel", "An online retailer needs a client panel that displays inventory from a JSON endpoint.", "Fetch sample inventory data asynchronously, show loading/success/error states, and explain event-loop behavior.", "Correct asynchronous flow, robust response/error handling, and clear UI states.", False),
            _level(7, "Git and GitHub", "Commits, branches, pull requests, and npm basics. Existing Git course content belongs at this level.", "Draft: Team feature delivery workflow", "A product team needs a repeatable workflow for a small feature release.", "Use npm scripts for a sample project, commit incremental changes, create a feature branch, and document a pull request with review notes.", "Useful commit history, branch workflow, clear pull request, and working npm scripts.", False),
            _level(8, "Django backend", "Routing, Django views and templates, and REST APIs with JSON.", "CRUD app", "An operations team needs an internal tool to track service requests.", "Build a Django CRUD application with JSON-friendly REST endpoints, routes, views, templates, and create/read/update/delete behavior.", "Complete CRUD behavior, correct routing and JSON responses, and clear templates.", True),
            _level(9, "Databases", "Relational design, joins, indexes, migrations, and ORM queries.", "Draft: Service request data layer", "An operations team needs a reliable relational data model for service requests.", "Design related tables, add migrations and indexes, write join queries, and implement representative Django ORM queries.", "Sound relational design, correct joins and migrations, justified indexes, and accurate ORM results.", False),
            _level(10, "Auth and security", "Sessions, JWT, password hashing, CSRF, and XSS.", "Draft: Secure internal portal", "A company needs a secure staff portal with authenticated access.", "Implement a local demo login flow with safe password hashing, session handling, CSRF protection, and output escaping; explain JWT tradeoffs.", "Safe authentication practices, CSRF protections, XSS prevention, and clear session/JWT explanation.", False),
            _level(11, "Frontend framework (React)", "React components, state, and API integration.", "Draft: React service-request console", "An operations team needs a component-based console for service requests.", "Build a React interface with reusable components and state that loads and updates records through an API.", "Reusable component design, correct state updates, API integration, and accessible UI.", False),
            _level(12, "Deployment and testing", "Docker basics, environment variables, Render deployment, tests, performance, and a full-stack live capstone.", "Full-stack app deployed live", "A startup needs a production-ready full-stack product that can be demonstrated to stakeholders.", "Design, test, containerize, configure environment variables, deploy on Render, and document a complete full-stack application with a live URL.", "Passing tests, safe configuration, successful live deployment, acceptable performance, and complete project documentation.", True),
        ],
    },
    "data_analytics": {
        "expert_name": "Senior Data Analyst Mentor & Trainer",
        "intro": "A 12-level analyst course progressing from spreadsheet skills through SQL, BI, experimentation, and stakeholder storytelling. Complete each level project to unlock the next.",
        "levels": [
            _level(1, "Excel basics", "Excel formulas, filters, pivot tables, and XLOOKUP.", "Sales sheet cleanup", "A retail finance team needs a clean, trustworthy monthly sales workbook.", "Clean a supplied sales sheet, document data-quality corrections, add formulas and filters, summarize with a pivot table, and use XLOOKUP.", "Correct formulas, transparent cleaning, accurate pivot summary, and clear workbook notes.", True),
            _level(2, "Python basics", "Python variables, loops, functions, lists, and dictionaries.", "Draft: Store operations summary script", "An operations team needs a repeatable summary of daily store activity.", "Write a small Python script that processes sample records using variables, loops, functions, lists, and dictionaries.", "Correct output, appropriate use of core constructs, and readable functions.", False),
            _level(3, "Pandas basics", "Read CSV files, clean nulls, filter rows, and sort data with Pandas.", "Gym renewal analysis", "A fitness company needs to understand which members are likely to renew.", "Load a member CSV, inspect and clean missing values, filter and sort renewal data, and summarize renewal patterns.", "Reproducible CSV workflow, justified null handling, correct filters, and useful findings.", True),
            _level(4, "SQL basics", "SQL SELECT, WHERE, ORDER BY, GROUP BY, and aggregate functions.", "Telecom churn analysis", "A telecom analytics team needs a first churn report from subscriber records.", "Query a sample subscriber database using SELECT, WHERE, ORDER BY, GROUP BY, and aggregates to report churn by customer segment.", "Valid readable SQL, accurate aggregates, and business-relevant churn findings.", True),
            _level(5, "Statistics for analysts", "Mean, median, distributions, outliers, and growth rate.", "Draft: Monthly performance variance report", "A finance team needs to explain variation in monthly performance without overstating the data.", "Analyze a provided monthly dataset using mean, median, distribution summaries, outlier checks, and growth-rate calculations.", "Correct statistical interpretation, transparent outlier treatment, and appropriate business caveats.", False),
            _level(6, "Pandas intermediate", "Groupby, merge, pivot_table, dates, and apply.", "Draft: Subscription revenue cohort workbook", "A subscription company needs a joined monthly view of customer and revenue data.", "Use Pandas groupby, merge, pivot_table, date handling, and apply to build a reproducible analysis.", "Correct joins and date handling, meaningful aggregation, and reproducible transformations.", False),
            _level(7, "SQL joins, subqueries, and CTEs", "Join relational tables and use subqueries and common table expressions.", "Draft: Customer retention query pack", "A customer success team needs reusable SQL for retention reporting across related tables.", "Write documented joins, subqueries, and CTEs against sample customer, subscription, and activity tables.", "Correct join cardinality, readable query structure, and validated results.", False),
            _level(8, "SQL window functions", "ROW_NUMBER, RANK, LAG/LEAD, and running totals.", "Churn analysis in SQL", "A subscription company needs a customer-level churn analysis with cohort and trend details.", "Use SQL window functions, ranking, lag/lead, and running totals to analyze a provided churn dataset.", "Correct partitions/orderings, accurate churn logic, and business-ready result explanations.", True),
            _level(9, "Power BI", "Data models, relationships, and cleaning with Power Query.", "Draft: Executive operations dashboard model", "An operations team needs a maintainable Power BI model for its executive dashboard.", "Clean source data in Power Query, build a relational model, define relationships, and create a focused dashboard.", "Clean transformations, correct relationships, useful visuals, and a coherent model.", False),
            _level(10, "DAX basics", "CALCULATE, filter context, and basic time intelligence.", "Draft: Revenue and retention measures", "A BI team needs reusable measures for revenue and customer retention reporting.", "Create DAX measures using CALCULATE and filter context, plus basic time-intelligence measures, in a sample model.", "Correct measure results, clear filter-context reasoning, and valid time comparisons.", False),
            _level(11, "Time-series and A/B tests", "Trends, seasonality, moving averages, significance, and sample size.", "Draft: Campaign experiment readout", "A growth team needs a defensible experiment readout and trend assessment.", "Analyze a time series for trends and seasonality, calculate moving averages, and assess an A/B test with significance and sample-size caveats.", "Sound trend analysis, appropriate experiment interpretation, and explicit uncertainty.", False),
            _level(12, "Capstone: business metrics dashboard", "Build an end-to-end dashboard with business metrics such as churn, retention, and conversion, then tell the stakeholder story.", "End-to-end business metrics dashboard", "A leadership team needs a decision-ready view of churn, retention, and conversion.", "Deliver an end-to-end analysis, validated metrics, dashboard, and stakeholder narrative with actionable recommendations.", "Metric definitions, reproducible analysis, clear dashboard, and concise evidence-based storytelling.", True),
        ],
    },
    "ai_ml": {
        "expert_name": "Senior AI/ML Engineer & Research Mentor",
        "intro": "A 12-level AI engineering course from Python and classical machine learning to neural networks, LLMs, and a deployed RAG capstone. Complete each level project to unlock the next.",
        "levels": [
            _level(1, "AI/ML foundations", "What AI/ML is, problem types, and Python and NumPy basics.", "Draft: ML problem-framing notebook", "A product analytics team needs to decide whether a business question is a prediction, classification, or clustering problem.", "Write a notebook that explains AI/ML problem types and uses Python and NumPy to inspect a small synthetic dataset.", "Accurate problem framing, correct NumPy operations, and clear assumptions.", False),
            _level(2, "Pandas and ML data preparation", "Pandas data preparation and train/test split for machine learning.", "Draft: Model-ready customer dataset", "A data science team needs a clean, leakage-aware dataset for a baseline model.", "Load and prepare a sample dataset with Pandas, document transformations, and create a reproducible train/test split.", "Reproducible preparation, appropriate split, and no target leakage.", False),
            _level(3, "Linear regression and evaluation", "Fit linear regression and evaluate it with MSE and R-squared.", "House price predictor", "A property analytics team needs a transparent baseline estimate for listing prices.", "Build a linear-regression pipeline from sample property features, evaluate with MSE and R-squared, and explain limitations.", "Correct split and metrics, sound interpretation, and transparent limitations.", True),
            _level(4, "Logistic regression and classification", "Train logistic regression and interpret a confusion matrix, precision, and recall.", "Churn classifier", "A subscription team needs a baseline classifier to prioritize customer-retention outreach.", "Train a logistic-regression churn classifier and report a confusion matrix, precision, and recall with threshold discussion.", "Correct evaluation, appropriate metric tradeoffs, and clear risk of false positives/negatives.", True),
            _level(5, "Decision trees and random forests", "Train and compare decision trees and random forests.", "Draft: Model comparison for service triage", "An operations team needs an interpretable comparison of tree-based models for triaging service requests.", "Train decision-tree and random-forest models on a sample dataset, compare performance, and inspect feature importance responsibly.", "Valid comparison, appropriate evaluation, and cautious feature-importance interpretation.", False),
            _level(6, "Feature engineering and validation", "Feature engineering, cross-validation, and machine-learning pipelines.", "Draft: Reliable model validation pipeline", "An ML team needs a repeatable evaluation pipeline that avoids leakage.", "Create preprocessing and feature-engineering steps inside a pipeline, use cross-validation, and document the evaluation protocol.", "Leakage-safe pipeline, correct cross-validation, and reproducible results.", False),
            _level(7, "Text preprocessing and TF-IDF", "Preprocess text and build a TF-IDF sentiment classifier.", "Draft: Customer feedback sentiment review", "A customer experience team needs to classify feedback themes for manual review.", "Clean a sample text dataset, vectorize with TF-IDF, train a baseline sentiment classifier, and inspect errors.", "Appropriate preprocessing, sound evaluation, and meaningful error analysis.", False),
            _level(8, "Embeddings and clustering", "Embeddings, k-means clustering, and semantic search over documents.", "Semantic search over documents", "A legal operations team needs to find related policy documents using a fixed local sample corpus.", "Create embeddings for a supplied document set, cluster with k-means, and implement semantic retrieval with relevance checks.", "Reproducible local workflow, sensible clustering, and useful retrieval evaluation.", True),
            _level(9, "Neural networks", "Explain perceptrons, activation functions, and backpropagation.", "Draft: Neural network learning notebook", "An applied research team needs a small demonstration of how a neural network learns.", "Build or train a small neural network on a toy dataset and visualize activation and loss changes during learning.", "Correct conceptual explanation, reproducible training, and clear learning diagnostics.", False),
            _level(10, "CNNs for images", "Use convolutional neural networks for image classification.", "Draft: Quality inspection image classifier", "A manufacturing team needs a prototype to classify a labeled sample of product images.", "Prepare a small image dataset, train or fine-tune a CNN, evaluate per-class performance, and document limitations.", "Appropriate split, class-aware evaluation, and transparent dataset/model limitations.", False),
            _level(11, "Transformers and LLMs", "Understand tokens and attention, write grounded prompts, and explain fine-tuning at an introductory level.", "Draft: Grounded internal knowledge assistant", "An internal enablement team needs a safe assistant that answers from an approved knowledge sample.", "Compare tokenization and attention concepts, create grounded prompts over approved sample material, and outline a fine-tuning evaluation plan.", "Correct concepts, source-grounded responses, and responsible evaluation plan.", False),
            _level(12, "AI engineering capstone", "Build and deploy a retrieval-augmented generation application with cited sources.", "Deployed RAG app with cited sources", "A support organization needs a deployed assistant that answers from approved documentation and cites sources.", "Build a retrieval-augmented application over an approved document set, return source citations, test retrieval and answer quality, and deploy it.", "Faithful citations, retrieval evaluation, safe handling of unsupported questions, and successful deployment.", True),
        ],
    },
    "robotics": {
        "expert_name": "Senior Robotics & Embedded Systems Engineer",
        "intro": "A 12-level robotics course from circuits and microcontrollers through control, ROS, navigation, and an integrated robot capstone. Complete each level project to unlock the next.",
        "levels": [
            _level(1, "Electronics basics", "Voltage, current, resistance, Ohm's law, circuits, and breadboarding.", "Draft: Bench circuit measurement log", "A robotics lab needs a safe, documented introduction to simple low-voltage circuits.", "Build simple breadboard circuits with instructor-approved low-voltage components and record voltage/current measurements against Ohm's law.", "Safe setup, correct measurements, and accurate circuit calculations.", False),
            _level(2, "Microcontroller basics", "Arduino/Raspberry Pi setup, GPIO, digital input, and digital output.", "Button-controlled LED sequence", "A robotics lab needs a reliable button-driven status-light prototype.", "Set up an Arduino or Raspberry Pi GPIO example and implement a button-controlled LED sequence with a clear wiring diagram.", "Correct GPIO behavior, safe wiring, clear sequence logic, and reproducible setup.", True),
            _level(3, "PWM, analog input, and sensors", "PWM, analog input, potentiometers, and light-dependent resistors.", "Draft: Light-responsive indicator", "A facilities team needs a simple light-level indicator prototype.", "Read a potentiometer and LDR, demonstrate analog input and PWM output, and document calibration observations.", "Correct sensor readings, appropriate PWM behavior, and documented calibration.", False),
            _level(4, "DC motors and motor drivers", "Drive DC motors with a motor driver and control speed with PWM.", "Motor speed controller", "A warehouse robotics team needs a benchtop controller for adjusting a small test motor.", "Use a suitable motor driver and PWM to control a low-voltage DC motor; record speed-control behavior and safe operating limits.", "Correct driver integration, stable speed control, and explicit electrical safety checks.", True),
            _level(5, "Ultrasonic and IR sensors", "Read ultrasonic and infrared distance/proximity sensors.", "Draft: Local proximity monitor", "A robotics lab needs a local bench demonstration of obstacle-distance sensing.", "Read ultrasonic and IR sensor values, compare their behavior on a controlled local test setup, and log measurements.", "Reliable readings, comparison of sensor limitations, and safe local testing.", False),
            _level(6, "Servo and stepper motors", "Control servo position and stepper motion.", "Draft: Precision actuator test rig", "A prototyping team needs a repeatable actuator test fixture.", "Control a servo and stepper motor in a low-voltage test fixture and document position/step accuracy.", "Correct motor control, repeatable measurements, and safe power handling.", False),
            _level(7, "Obstacle-avoidance logic", "Design state-based control logic for obstacle avoidance.", "Obstacle-avoidance routine", "A warehouse automation team needs a local simulated robot routine for navigating around obstacles.", "Implement a state-based routine using simulated or bench sensor readings and document behavior for clear-path, obstacle, and recovery states.", "Correct state transitions, safe stop/recovery behavior, and repeatable local simulation.", True),
            _level(8, "IMU basics", "Understand accelerometers, gyroscopes, calibration, and sensor orientation.", "Tilt-based balance", "A robotics lab needs a small balancing demonstration using an IMU tilt estimate.", "Read and calibrate an IMU, estimate tilt from accelerometer/gyroscope data, and demonstrate a controlled tilt-based response in simulation or a safe fixture.", "Calibration evidence, sensible sensor fusion discussion, and stable safe response.", True),
            _level(9, "PID control", "Understand PID theory and tune a controller using measured response.", "Draft: Motor response tuning report", "A controls team needs a documented PID tuning experiment for a low-voltage motor.", "Run a controlled simulation or bench experiment, vary PID terms, record step response, and explain stability and tuning tradeoffs.", "Measured response, correct interpretation of PID terms, and safe tuning procedure.", False),
            _level(10, "ROS fundamentals", "Work with ROS nodes, topics, and services.", "Draft: ROS sensor telemetry demo", "A robotics team needs a local ROS demo that publishes sensor telemetry for a consumer node.", "Create local ROS nodes that publish and consume simulated sensor messages and expose a simple service; document commands and message flow.", "Correct node/topic/service behavior, reproducible local setup, and clear message-flow documentation.", False),
            _level(11, "SLAM and navigation", "Explore SLAM, navigation basics, and A* path planning in simulation.", "Draft: Simulated warehouse route planner", "A logistics team needs a simulated route planner for a small warehouse map.", "Use a local simulation/map to explain SLAM and implement or demonstrate A* path planning with obstacle-aware routes.", "Valid local simulation, correct route planning, and clear limitations of the map/localization.", False),
            _level(12, "Robotics capstone", "Integrate sensing, control, and navigation into an obstacle-avoiding robot.", "Integrated obstacle-avoiding robot", "A warehouse automation team needs an integrated prototype that avoids obstacles in a controlled local test area.", "Integrate a microcontroller or ROS stack, sensors, motor control, and obstacle-avoidance behavior; validate only in a controlled local setup.", "Reliable integration, safe behavior, documented test cases, and repeatable local demonstration.", True),
        ],
    },
    "electronics": {
        "expert_name": "Electronics Engineer & Mentor",
        "intro": "A separate 12-level electronics course, progressing from safe circuit fundamentals through measurement, embedded interfaces, and system validation.",
        "levels": [
            _level(1, "Electrical foundations", "Voltage, current, resistance, Ohm's law, and simple LED circuits.", "LED circuit measurement", "A learner needs to understand and measure one safe low-voltage circuit.", "Calculate a current-limiting resistor, assemble one LED circuit in simulation or with a supervised low-voltage kit, and record voltage readings.", "Correct resistor calculation, circuit polarity, and safe measurement setup.", False),
            _level(2, "Circuit paths and rules", "Series and parallel paths, switches, polarity, and Kirchhoff's basic rules.", "Series and parallel comparison", "A small device needs predictable behavior when one component is disconnected.", "Compare a two-resistor series circuit with a parallel circuit and explain how opening one branch changes the path.", "Accurate circuit diagrams, predicted measurements, and explanation of one open-path case.", False),
            _level(3, "Components and datasheets", "Resistors, capacitors, diodes, transistors, ratings, and datasheet limits.", "Component selection card", "A repair bench needs a safe replacement part for a low-voltage indicator.", "Read supplied component markings and a public datasheet excerpt, then select a resistor, diode, and transistor for a bounded example.", "Selections use the stated ratings and include a clear reason for each component.", False),
            _level(4, "Prototyping and schematics", "Breadboard connections, schematic symbols, continuity checks, and safe power limits.", "Breadboard wiring guide", "A training lab needs repeatable wiring notes for a simple sensor circuit.", "Translate a small schematic into a breadboard layout and verify its nodes with continuity mode before applying safe low voltage.", "Layout matches the schematic, rails are checked, and the power limit is stated.", False),
            _level(5, "Measurement instruments", "Multimeter modes, voltage and current measurement, resistance checks, and uncertainty.", "Measurement comparison log", "A service team wants dependable measurements before replacing a board component.", "Measure a known low-voltage source and an unpowered resistor with the correct meter setup; record repeated readings and instrument range.", "Correct modes and probe positions, repeatable readings, and a stated measurement limitation.", False),
            _level(6, "Digital electronics", "Logic levels, pull-up and pull-down resistors, debouncing, and PWM timing.", "Button and dimmer logic", "A product prototype needs a reliable button input and adjustable indicator brightness.", "Sketch a debounced button input and a PWM LED output, then verify expected digital states and duty-cycle behavior in simulation.", "Stable press/release states, correct duty-cycle interpretation, and a safe LED current limit.", False),
            _level(7, "Microcontrollers and GPIO", "Pin modes, GPIO limits, ADC readings, timers, and basic embedded interfaces.", "GPIO interface demo", "A lab fixture needs to read one input and control one low-current output safely.", "Configure one GPIO input and one output in a simulator, document the pin map, and show input-to-output behavior.", "Pin directions and logic states are correct, and the GPIO current limit is respected.", False),
            _level(8, "Sensors and conditioning", "Analog sensors, voltage dividers, ADC scaling, filtering, and calibration.", "Sensor calibration note", "A monitoring device needs stable readings from a low-cost analog sensor.", "Collect a small simulated or public example reading set, map ADC counts to units, and compare raw with simple filtered readings.", "Conversion assumptions are documented, calibration points are shown, and noise limits are explained.", False),
            _level(9, "Actuators and switching", "Transistor and relay drivers, inductive loads, flyback protection, and power separation.", "Low-voltage driver test", "A prototype must switch a small actuator without overloading its controller pin.", "Design or simulate a transistor driver for a bounded low-voltage load and include the correct flyback protection and separate supply path.", "Driver choice matches load current, protection polarity is correct, and controller/load grounds are handled safely.", False),
            _level(10, "Analog signal design", "Op-amp roles, gain, comparators, RC filters, grounding, and noise.", "Signal conditioning worksheet", "A sensor input is too small or noisy for a controller to interpret consistently.", "Calculate a simple amplifier or RC filter from stated values and plot or simulate its expected input/output response.", "Calculation matches the circuit, cutoff or gain is labeled, and one noise trade-off is explained.", False),
            _level(11, "Embedded communication", "UART, I2C, SPI, bus wiring, logic compatibility, and fault diagnosis.", "Interface comparison guide", "A device team needs to choose a suitable board-to-sensor communication link.", "Compare UART, I2C, and SPI for a supplied fictional sensor setup; draw the selected wiring and diagnose one simulated communication fault.", "Choice fits device count and speed, signal levels are compatible, and the fault explanation follows evidence.", False),
            _level(12, "System integration and validation", "Power budgets, schematic review, prototype validation, fault isolation, and documentation.", "Electronics integration dossier", "A small product team needs evidence that its low-voltage sensing prototype is ready for a controlled demo.", "Integrate a sensor, controller, and indicator in simulation or a supervised fixture; document the schematic, power budget, test cases, and one fault found.", "Interfaces and power budget are consistent, tests are repeatable, and limitations and safety controls are clear.", False),
        ],
    },
    "cybersecurity": {
        "expert_name": "Cyber Security Learning Track (Pending Confirmation)",
        "intro": "This defensive, lab-only curriculum is unavailable until the Cyber Security domain is confirmed.",
        "levels": [
            _level(1, "Networking basics", "IP, TCP/UDP, DNS, and ports for defensive network understanding.", "Draft: Local network inventory", "A defensive IT team needs an inventory of a provided local lab network.", "Document supplied local network configuration and protocol roles; do not scan external systems.", "Accurate protocol explanations and strictly local, authorized scope.", False),
            _level(2, "Linux basics", "Command line, permissions, and processes.", "Draft: Linux host baseline", "An IT operations team needs a baseline checklist for a local training VM.", "Inspect permissions and processes on a provided local VM and document secure baseline observations.", "Accurate local observations and safe permission recommendations.", False),
            _level(3, "Security fundamentals", "CIA triad, threat types, and hashing versus encryption.", "Draft: Security awareness briefing", "A security team needs a short briefing for staff on core security concepts.", "Explain confidentiality, integrity, availability, threat categories, and the difference between hashing and encryption.", "Technically accurate distinctions and defensive recommendations.", False),
            _level(4, "Web basics for security", "HTTP, cookies, and sessions from a defensive perspective.", "Draft: Local session configuration review", "A web team needs a configuration review of its own local demo application.", "Review provided local configuration for cookie and session settings and document defensive improvements.", "Correct defensive findings and no testing outside the provided local application.", False),
            _level(5, "OWASP Top 10 part 1", "Injection and broken authentication in a deliberately vulnerable local test app.", "Local vulnerable-app remediation report", "A training team needs a remediation report for a deliberately vulnerable local test application.", "Use only the provided intentionally vulnerable local application; document observed injection/authentication weaknesses and safe remediations without exposing a real service.", "Local-only scope, clear defensive evidence, and actionable remediation.", True),
            _level(6, "OWASP Top 10 part 2", "XSS, CSRF, and security misconfiguration in a local defensive lab.", "Draft: Local web hardening checklist", "A web engineering team needs a defensive checklist for its local training app.", "Review supplied local examples for output encoding, CSRF protection, and secure configuration; document fixes.", "Defensive focus, accurate remediation, and local-only examples.", False),
            _level(7, "Log analysis", "Review authentication logs and identify brute-force indicators defensively.", "Authentication log incident report", "A security operations team needs an incident report based on supplied local authentication logs.", "Analyze provided synthetic/local authentication logs for suspicious patterns and write a timeline and defensive response.", "Correct log interpretation, evidence-based timeline, and defensive response actions.", True),
            _level(8, "Python for security", "Parse local logs and perform simple authorized checks.", "Draft: Local log parsing utility", "A security operations team needs a utility to summarize supplied local logs.", "Write a Python parser for provided local logs and report configured checks without probing external hosts.", "Correct parsing, safe local-only scope, and useful defensive output.", False),
            _level(9, "Wireshark and network scanning", "Analyze supplied packet captures and understand authorized lab scanning.", "Draft: Provided packet-capture analysis", "A network defense team needs a summary of a supplied training packet capture.", "Analyze only a provided packet capture and explain expected lab traffic; keep any scanning within an explicitly provided local lab.", "Accurate traffic interpretation and explicit authorized scope.", False),
            _level(10, "Threat modeling and SIEM basics", "Threat modeling concepts and basic defensive SIEM workflows.", "Draft: Internal service threat model", "An engineering team needs a defensive threat model for an internal service.", "Map assets, trust boundaries, threats, mitigations, and example SIEM alerts for a fictional service.", "Complete threat model, practical mitigations, and useful defensive alert logic.", False),
            _level(11, "Incident response and threat hunting", "Plan defensive incident response and evidence-led threat hunting.", "Draft: Tabletop incident response plan", "A security team needs a tabletop plan for a simulated account-compromise incident.", "Use a fictional tabletop scenario and supplied local logs to define detection, containment, recovery, and lessons learned.", "Clear response phases, evidence handling, and defensive scope.", False),
            _level(12, "Penetration-test workflow and report", "Document an authorized lab-only assessment and remediation report.", "Authorized local lab assessment report", "A security team needs a structured report for a deliberately vulnerable local test application.", "Follow a documentation-only workflow within the provided local lab; report findings, impact, and remediation. Do not target real systems.", "Local-only scope, clear evidence, prioritized remediation, and no real-target instructions.", True),
        ],
    },
}


LEVEL_CONCEPTS = {
    "web_dev": [
        ["DNS resolution", "HTTP and HTTPS", "Client-server requests and responses", "Browser developer tools"],
        ["Semantic HTML tags", "Forms and labels", "HTML input types", "Accessibility basics"],
        ["CSS selectors", "CSS box model", "Flexbox layout", "CSS Grid layout"],
        ["JavaScript variables", "Functions", "Arrays and objects", "DOM basics"],
        ["Scope", "Closures", "Browser events", "Error handling"],
        ["Promises", "async/await", "Fetch API", "JavaScript event loop"],
        ["Git commits", "Branches", "Pull requests", "npm basics"],
        ["Django URL routing", "Django views", "Django templates", "REST APIs with JSON"],
        ["Relational database design", "SQL joins", "Database indexes", "Schema migrations"],
        ["Sessions", "JWT", "Password hashing", "CSRF protection", "XSS prevention"],
        ["React components", "React state", "API integration"],
        ["Docker basics", "Environment variables", "Render deployment", "Automated tests"],
    ],
    "data_analytics": [
        ["Excel formulas", "Filters", "Pivot tables", "XLOOKUP"],
        ["Python variables", "Loops", "Functions", "Lists and dictionaries"],
        ["Read CSV with Pandas", "Clean null values", "Filter rows", "Sort data"],
        ["SQL SELECT", "WHERE and ORDER BY", "GROUP BY", "Aggregate functions"],
        ["Mean and median", "Distributions", "Outliers", "Growth rate"],
        ["Pandas groupby", "Merge dataframes", "pivot_table", "Dates and apply"],
        ["SQL joins", "Subqueries", "Common table expressions"],
        ["ROW_NUMBER and RANK", "LAG and LEAD", "Running totals"],
        ["Power BI data model", "Table relationships", "Power Query cleaning"],
        ["DAX CALCULATE", "Filter context", "Basic time intelligence"],
        ["Time-series trends", "Seasonality", "Moving averages", "Statistical significance and sample size"],
        ["Churn metrics", "Retention metrics", "Conversion metrics", "Dashboard design", "Stakeholder storytelling"],
    ],
    "ai_ml": [
        ["What AI and ML are", "ML problem types", "Python basics", "NumPy arrays"],
        ["Pandas data preparation", "Handle missing values", "Feature and target selection", "Train/test split"],
        ["Linear regression", "Model fitting", "Mean squared error", "R-squared"],
        ["Logistic regression", "Confusion matrix", "Precision", "Recall"],
        ["Decision trees", "Tree splitting", "Random forests", "Model comparison"],
        ["Feature engineering", "Cross-validation", "Preprocessing pipelines"],
        ["Text preprocessing", "Tokenization", "TF-IDF vectors", "Sentiment classification"],
        ["Text embeddings", "K-means clustering", "Similarity search", "Document semantic search"],
        ["Perceptrons", "Neural network layers", "Activation functions", "Backpropagation"],
        ["Image tensors", "Convolution filters", "Pooling", "CNN image classification"],
        ["LLM tokens", "Attention basics", "Grounded prompting", "Fine-tuning introduction"],
        ["Document ingestion", "RAG chunking and retrieval", "Cited source answers", "Deployment and evaluation"],
    ],
    "robotics": [
        ["Voltage", "Current", "Resistance and Ohm's law", "LED circuit", "Breadboard", "Multimeter use"],
        ["Arduino or Raspberry Pi setup", "GPIO pins", "Digital input", "Digital output"],
        ["PWM output", "Analog input", "Potentiometer readings", "LDR sensor readings"],
        ["DC motors", "Motor drivers", "PWM speed control", "Motor safety"],
        ["Ultrasonic distance sensing", "IR proximity sensing", "Sensor readings", "Sensor limitations"],
        ["Servo positioning", "Stepper motor steps", "Actuator control"],
        ["Obstacle detection states", "State-based control", "Avoidance decisions", "Recovery behavior"],
        ["Accelerometer data", "Gyroscope data", "IMU orientation", "Calibration"],
        ["PID control loop", "Proportional response", "Integral and derivative terms", "Controller tuning"],
        ["ROS nodes", "ROS topics", "ROS services", "Message flow"],
        ["SLAM concepts", "Map and localization basics", "A* path planning", "Obstacle-aware routes"],
        ["Sensor integration", "Motor control integration", "Obstacle-avoidance behavior", "End-to-end robot testing"],
    ],
    "electronics": [
        ["Voltage", "Current", "Resistance and Ohm's law", "LED circuits"],
        ["Series circuits", "Parallel circuits", "Open and closed paths", "Circuit polarity"],
        ["Resistor ratings", "Capacitors", "Diodes", "Transistors as switches"],
        ["Breadboard rows and rails", "Schematic symbols", "Continuity checks", "Safe power limits"],
        ["Multimeter controls", "DC voltage measurement", "Current measurement", "Resistance measurement"],
        ["Logic levels", "Pull-up and pull-down inputs", "Switch debouncing", "PWM signals"],
        ["Microcontroller pins", "GPIO output", "Digital button input", "ADC conversion"],
        ["Voltage dividers", "Analog sensors", "Signal filtering", "Sensor calibration"],
        ["Transistor drivers", "Relay switching", "Flyback diodes", "Separate load power"],
        ["Op-amp basics", "Amplifier gain", "RC filters", "Noise and grounding"],
        ["UART communication", "I2C bus", "SPI bus", "Logic-level compatibility"],
        ["Power budgeting", "Schematic review", "Prototype test plans", "Fault isolation"],
    ],
    "cybersecurity": [
        ["IP addressing", "TCP and UDP", "DNS", "Network ports"],
        ["Linux command line", "File permissions", "Process basics", "Safe local administration"],
        ["Confidentiality, integrity, availability", "Threat types", "Hashing", "Encryption"],
        ["HTTP requests and responses", "Cookies", "Sessions", "Secure web configuration"],
        ["Injection risk concepts", "Broken authentication concepts", "Local vulnerable test app", "Defensive remediation"],
        ["Cross-site scripting prevention", "CSRF protection", "Security misconfiguration", "Secure configuration review"],
        ["Authentication log fields", "Failed-login patterns", "Brute-force indicators", "Incident report timeline"],
        ["Python log parsing", "Structured event data", "Local-only port-check concepts", "Defensive output"],
        ["Wireshark interface basics", "Provided packet capture", "Protocol filtering", "Authorized local scanning concepts"],
        ["Asset and trust-boundary mapping", "Threat modeling", "SIEM event basics", "Defensive alert rules"],
        ["Incident triage", "Evidence handling", "Threat-hunting from supplied logs", "Containment and recovery"],
        ["Authorized lab scope", "Assessment planning", "Findings and risk ratings", "Remediation report"],
    ],
}

for _domain, _levels in RESTRUCTURED_CURRICULA.items():
    for _index, _level_data in enumerate(_levels["levels"]):
        _level_data["concepts"] = LEVEL_CONCEPTS[_domain][_index]

for _cyber_level in RESTRUCTURED_CURRICULA["cybersecurity"]["levels"]:
    _cyber_project = _cyber_level["project_json"]
    _cyber_project["objective"] = (
        "Defensive, authorized local-lab only. " + _cyber_project["objective"]
    )
    _cyber_project["requirements"] += (
        "\nUse only supplied local labs, synthetic/local logs, or provided captures. "
        "Do not target real or third-party systems."
    )


# Build Lab briefs are deliberately kept as metadata on the existing projects so the
# lesson, quiz, runner, tier routing, and unlock models do not need to change.
_BUILD_LAB_COMPANIES = {
    "data_analytics": [
        ("Northstar Grocers", "grocery retail"), ("BrightPath Tutors", "edtech"),
        ("Harborline Clinics", "healthcare"), ("SkyParcel", "logistics"),
        ("Cedar Bank", "banking"), ("PeakFit Studios", "fitness"),
        ("Lumen Mobile", "telecommunications"), ("Aster Hotels", "hospitality"),
        ("ForgeWorks", "manufacturing"), ("CivicGrid", "utilities"),
        ("GreenCart", "e-commerce"), ("Sunrise Mutual", "insurance"),
    ],
    "ai_ml": [
        ("Willow Homes", "real estate"), ("MediRoute", "pharmacy"),
        ("Atlas Lending", "consumer lending"), ("NimbleSub", "subscription media"),
        ("QuarryOps", "mining"), ("FreshFleet", "food delivery"),
        ("Kindred Care", "elder care"), ("LexiArchive", "legal services"),
        ("Tide Energy", "renewable energy"), ("Orbit Assembly", "electronics manufacturing"),
        ("CampusBridge", "higher education"), ("FieldGuide", "agriculture"),
    ],
    "web_dev": [
        ("Maple Market", "specialty retail"), ("CareLink", "patient scheduling"),
        ("TrailStay", "travel"), ("Pennywise", "personal finance"),
        ("PulseDesk", "SaaS customer support"), ("Stockroom", "warehouse operations"),
        ("MintPress", "digital publishing"), ("NeighborWorks", "property management"),
        ("Cobalt Motors", "automotive"), ("BeaconPay", "payments"),
        ("StageDoor", "event ticketing"), ("RiverCity Transit", "public transport"),
    ],
    "robotics": [
        ("VoltCraft", "consumer electronics"), ("SproutLab", "urban farming"),
        ("AquaSense", "water treatment"), ("CrateMover", "fulfilment"),
        ("SafeHarbor", "port operations"), ("StoneMill", "construction"),
        ("KiteRail", "rail maintenance"), ("Alpine Rescue", "emergency response"),
        ("NovaFab", "aerospace"), ("CurePack", "medical devices"),
        ("TerraHaul", "waste management"), ("Lighthouse Foods", "food processing"),
    ],
    "electronics": [
        ("TeraCircuits", "consumer electronics"), ("VitalLoop", "medical devices"),
        ("GridPilot", "renewable energy"), ("Brightwell Lighting", "commercial lighting"),
        ("LabCraft Learning", "education laboratories"), ("ClearWave Instruments", "test equipment"),
        ("NovaBoard", "embedded computing"), ("FieldSense", "agriculture technology"),
        ("AeroRelay", "aircraft systems"), ("QuietSignal Audio", "audio equipment"),
        ("GaugeLink", "industrial monitoring"), ("CircuitNest", "product prototyping"),
    ],
}


def _build_lab_schema(domain, level):
    schemas = {
        "data_analytics": [
            "sales.csv — order_id (integer, unique), order_date (date), store (string), product (string), units (integer), unit_price (decimal); synthetic sales rows.",
            "daily_sales.csv — sale_id (integer), sale_date (date), item (string), quantity (integer), price (decimal); synthetic practice rows.",
            "members.csv — member_id (integer, unique), join_date (date), plan (string), visits (integer), renewed (boolean); synthetic member records.",
            "subscribers.csv — customer_id (integer), plan (string), tenure_months (integer), monthly_fee (decimal), churned (boolean); synthetic subscriber records.",
            "monthly_performance.csv — month (date), store (string), revenue (decimal), target (decimal), returns (integer); synthetic monthly results.",
            "customers.csv — customer_id (integer), signup_date (date), plan (string); payments.csv — customer_id (integer), paid_at (date), amount (decimal), status (string); synthetic linked tables.",
            "customers.csv — customer_id (integer), segment (string); subscriptions.csv — customer_id (integer), start_date (date), end_date (date), plan (string); activity.csv — customer_id (integer), activity_date (date), event (string); synthetic linked tables.",
            "monthly_churn.csv — customer_id (integer), month (date), plan (string), active (boolean), churned (boolean); synthetic cohort rows.",
            "orders.csv — order_id (integer), order_date (date), product_id (integer), store_id (integer), revenue (decimal); products.csv — product_id (integer), category (string); stores.csv — store_id (integer), region (string); synthetic star-schema sample.",
            "daily_revenue.csv — day (date), region (string), revenue (decimal), customers (integer), refunds (integer); synthetic BI measures.",
            "experiment.csv — participant_id (integer), variant (string), assigned_at (date), converted (boolean); synthetic A/B test and trend observations.",
            "customer_month.csv — customer_id (integer), month (date), active (boolean), spend (decimal), channel (string); synthetic capstone metrics.",
        ],
        "ai_ml": [
            "problem_samples.csv — sample_id (integer), feature_a (float), feature_b (float), target (float); small synthetic regression examples.",
            "customer_features.csv — customer_id (integer), tenure (integer), visits (integer), plan (string), target (integer); synthetic train/test rows.",
            "homes.csv — home_id (integer), area_sqft (float), bedrooms (integer), age_years (integer), price (decimal); synthetic regression data.",
            "churn.csv — customer_id (integer), tenure_months (integer), monthly_fee (decimal), support_calls (integer), churned (boolean); synthetic classification data.",
            "service_requests.csv — request_id (integer), category (string), wait_minutes (float, some missing), priority (string), resolved (boolean); intentionally imperfect synthetic rows.",
            "customer_history.csv — customer_id (integer), event_date (date), event (string), value (decimal, occasional nulls); synthetic time-based features.",
            "reviews.csv — review_id (integer), review_text (string), sentiment (string); short synthetic/public text sample with labels.",
            "policy_docs.jsonl — doc_id (string), title (string), text (string), topic (string); small approved synthetic document corpus.",
            "image_manifest.csv — image_path (string), class_label (string), split (string); toy image files or generated diagrams.",
            "inspection_manifest.csv — image_path (string), defect_class (string), split (string); synthetic sample images and labels.",
            "approved_docs.jsonl — source_id (string), section (string), text (string); fictional policy text for grounded assistant evaluation.",
            "knowledge_docs.jsonl — doc_id (string), topic (string), text (string), expected_answer (string); synthetic documents and evaluation questions.",
        ],
        "web_dev": [
            "starter/ — index.html (HTML page), styles.css (CSS), app.js (JavaScript); browser tools provide local request/response evidence.",
            "starter/ — index.html, form.js, styles.css; fields.json contains field_id (string), label (string), input_type (string), required (boolean).",
            "products.json — product_id (integer), name (string), category (string), price (decimal), image_url (string); sample catalog items.",
            "landing-config.json — headline (string), features (array), CTA (string), lead_fields (array); sample launch-page content.",
            "support_threads.json — ticket_id (integer), subject (string), status (string), message (string); local mock support records.",
            "inventory.json — sku (string), product_name (string), quantity (integer), updated_at (datetime); sample async API response.",
            "starter repository — package.json (scripts/dependencies), README.md, and sample feature files; no customer data or external credentials.",
            "service_requests table — id (integer), title (string), status (string), created_at (datetime), assignee (string); local sample database.",
            "requests table — request_id (integer), customer_id (integer), status (string), created_at (datetime); customers table — id (integer), name (string).",
            "staff_users.json — user_id (integer), username (string), role (string); fake local accounts only, no real credentials.",
            "requests.json — id (integer), title (string), status (string), updated_at (datetime); local mock API records.",
            "starter/ — frontend source, backend routes, tests, Dockerfile, and sample environment file with placeholder values only.",
        ],
        "robotics": [
            "Low-voltage kit manifest — part_id (string), part_name (string), rated_value (string), quantity (integer). Use a breadboard, 5 V supply, LED, 330 Ω resistor, and multimeter; simulation is acceptable.",
            "button_led.json — pin (integer), input_mode (string), pressed_state (string), expected_led (boolean); simulated GPIO wiring and expected states.",
            "sensor_readings.csv — timestamp (integer), light_level (integer), knob_position (integer), pwm_output (integer); synthetic/simulated sensor readings.",
            "motor_trials.csv — trial_id (integer), pwm_command (integer), direction (string), measured_speed (float), safe_stop (boolean); low-voltage or simulated tests.",
            "distance_trials.csv — timestamp (integer), sensor (string), distance_cm (float), surface (string); synthetic/local ultrasonic and IR readings.",
            "actuator_trials.csv — actuator (string), command (integer), measured_position (float), repeat (integer); simulation or safe low-voltage fixture data.",
            "state_log.csv — step (integer), front_clear (boolean), robot_state (string), action (string), recovery_ok (boolean); simulated obstacle cases.",
            "imu.csv — timestamp (datetime), accel_x/y/z (float), gyro_x/y/z (float), known_tilt_deg (float); simulated or locally recorded readings.",
            "step_response.csv — time_ms (integer), target_speed (float), measured_speed (float), kp/ki/kd (float); simulated controller trials.",
            "ros_messages.jsonl — timestamp (datetime), topic (string), message_type (string), payload (object); local ROS simulation messages.",
            "map.csv — x (integer), y (integer), blocked (boolean), start (boolean), goal (boolean); small simulated grid map.",
            "robot_runs.csv — run_id (integer), scenario (string), obstacle_detected (boolean), stop_safe (boolean), route_complete (boolean); controlled simulation logs.",
        ],
    }
    schemas["electronics"] = [
        "parts.csv — part_id (string), name (string), value (string), voltage_limit (float), quantity (integer); synthetic low-voltage kit inventory.",
        "branches.csv — branch_id (string), component (string), value (float), connection (series/parallel); synthetic circuit cases.",
        "components.csv — part_id (string), type (string), rating (string), datasheet_url (string); fictional parts with public datasheet references.",
        "breadboard_map.json — hole_id (string), node_id (string), rail_segment (string); simulated board connections and component endpoints.",
        "meter_trials.csv — trial_id (integer), mode (string), range (string), expected (float), measured (float); synthetic low-voltage readings.",
        "logic_trials.csv — input_state (boolean), raw_edges (integer), debounce_ms (integer), accepted_edges (integer), pwm_duty (integer); simulated results.",
        "gpio_map.csv — pin (integer), direction (string), logic_voltage (float), current_ma (float), expected_state (string); simulated controller I/O.",
        "sensor.csv — raw_count (integer), reference_value (float), timestamp_ms (integer), condition (string); synthetic calibration readings.",
        "load_trials.csv — load_id (string), voltage (float), current_ma (float), driver (string), protection (string); simulated low-voltage loads.",
        "signal_cases.csv — input_v (float), gain (float), cutoff_hz (float), output_v (float), noise_pp (float); simulated analog circuits.",
        "bus_log.csv — protocol (string), address (string), tx (string), rx (string), voltage_level (float), status (string); synthetic interface traces.",
        "system_tests.csv — test_id (string), input (string), expected (string), observed (string), pass (boolean), fault_note (string); controlled integration data.",
    ]
    return schemas[domain][level - 1]


def _build_lab_project(domain, level, lesson_name, base_project, company, industry):
    """Create consistent, auditable briefs while retaining the existing project fields."""
    tier = "Beginner" if level <= 4 else "Intermediate" if level <= 8 else "Advanced"
    count = {"Beginner": 3, "Intermediate": 4, "Advanced": 5}[tier]
    schema = _build_lab_schema(domain, level)
    focus = base_project["title"].replace("Draft: ", "")
    level_task = base_project.get("requirements", "Complete the project using the skills taught in this level.").strip()
    level_one_tasks = {
        "data_analytics": "Use the small sales sheet to calculate total revenue and identify the top-selling product.",
        "ai_ml": "Use the tiny synthetic dataset to identify the prediction target and calculate a simple baseline result.",
        "web_dev": "Open the supplied local page, trace one browser request, and draw a short browser-to-server flow diagram.",
        "robotics": "Build one LED and resistor circuit on a breadboard, then record the supply and LED voltage in a simulator or safe low-voltage setup.",
        "electronics": "Use the small parts manifest to calculate a safe LED resistor and record the expected circuit voltage in a simulator or supervised low-voltage setup.",
    }
    if level == 1:
        level_task = level_one_tasks[domain]
    context = (
        f"{company} is a fictional {industry} company. {base_project.get('objective', '').strip()} "
        "Your findings should help the team choose a practical next step and explain its likely business value."
    )
    access = (
        f"Starter files are provided as a local download for {company}'s fictional scenario. "
        "Use the documented fields below, free tools, and no private data. The build window is two days."
    )
    lesson_topic = lesson_name.split(": ", 1)[-1]
    task = f"Level {level} — {lesson_topic}. {level_task}"
    deadline = "Deadline: submit within two calendar days of receiving the starter repository."
    tool_guidance = {
        "data_analytics": (
            "Excel or Google Sheets" if level == 1 else
            "Python and a notebook" if level == 2 else
            "Python, Pandas, and a notebook" if level == 3 else
            "SQLite and a SQL editor" if level == 4 else
            "SQL, Python/Pandas, and the BI tool named in this level"
        ),
        "ai_ml": "Python and Jupyter; use NumPy for the starter exercise and add only the library taught in this level.",
        "web_dev": (
            "A browser and developer tools" if level == 1 else
            "The HTML, CSS, or JavaScript feature taught in this level, plus a browser" if level <= 4 else
            "The framework and tools named in this level, GitHub, and free hosting only when the level requires deployment"
        ),
        "robotics": (
            "A circuit simulator or supervised low-voltage kit, a breadboard, LED, resistor, and multimeter" if level == 1 else
            "A simulator or supervised low-voltage kit and the components named in this level"
        ),
        "electronics": "A circuit simulator, a multimeter for low-voltage measurements, and the components named in this level; use public datasheets and synthetic examples.",
    }
    tools = f"Tools: {tool_guidance[domain]} Use free tools and synthetic data only."
    if domain == "robotics":
        tools += " Never connect circuits to mains power."
    elif domain == "electronics":
        tools += " Keep all physical work low-voltage; simulation is acceptable."
    report_readme = (
        "Write a README with setup, method, and numeric results. Include a PDF with the business problem, approach, findings, "
        "limitations, and a recommendation."
    )
    requirements = [
        "Complete the task above using the supplied starter material and keep the scope appropriate to this level.",
        f"Show two measured findings or checks. {report_readme}",
        "Publish a GitHub repository named EXA_ProjectName and submit the PDF plus a short screen recording.",
    ]
    if tier == "Intermediate":
        requirements = [
            "Complete the task above with the supplied real-style files and document the key transformations.",
            "Handle missing, inconsistent, or invalid inputs and show one edge-case check.",
            f"{report_readme} Keep the analysis or app method easy to reproduce.",
            "Publish EXA_ProjectName on GitHub, deploy a live demo, and include both links with your PDF.",
        ]
    elif tier == "Advanced":
        requirements = [
            "Complete the task above with a realistic but bounded data or user scope.",
            "Validate the result and report one relevant quality, performance, or error measure.",
            "Address one company constraint (cost, latency, accessibility, safety, or privacy) and explain the trade-off.",
            f"{report_readme} Add a short PDF monitoring/evaluation section naming a metric, threshold, review cadence, and owner.",
            "Publish EXA_ProjectName on GitHub, deploy a live demo, and include both links with your PDF.",
        ]
    weights = ([34, 33, 33] if count == 3 else [25, 25, 25, 25] if count == 4 else [20] * 5)
    evidence = [
        {"id": f"R{index + 1}", "requirement": requirement, "evidence_type":
         ("github_repo" if index == 0 else "pdf_report" if index == 1 else "live_demo" if tier != "Beginner" and index == 2 else "screen_recording"),
         "weight": weights[index]}
        for index, requirement in enumerate(requirements)
    ]
    result = dict(base_project)
    result.update({
        "title": f"{company}: {focus}",
        "objective": context,
        "company": company,
        "industry": industry,
        "tier": tier,
        "domain": domain,
        "level": level,
        "company_context": context,
        "access_details": access,
        "dataset_schema": schema,
        "requirements_list": requirements,
        "task": task,
        "level_task": level_task,
        "deadline": deadline,
        "tools": tools,
        "requirements": "\n".join(f"{i + 1}. {item}" for i, item in enumerate(requirements)) + f"\n\n{access}\n{task}\n{deadline}\n{tools}",
        "requirement_evidence": evidence,
        "submission": {
            "items": ["PDF report (max 10 MB)", "GitHub repo named EXA_ProjectName", "screen recording" if tier == "Beginner" else "live demo", "optional video (max 5 min)"],
            "live_demo_required": tier != "Beginner",
            "pdf_required": True,
        },
        "scoring": {
            "criteria": [{"name": name, "weight": 25} for name in ("Business fit", "Technical quality", "Evidence and results", "Communication")],
            "pass_score": 60,
            "missing_required_evidence_cap": 40,
        },
        "quality_gate": {
            "status": "passed",
            "attempts": 1,
            "checks": ["tier requirement count", "unique company and industry", "documented schema", "tier submission rules"],
            "log": "Build Lab quality gate passed on first generation.",
        },
        "evaluation_criteria": "Business fit (25), technical quality (25), evidence and results (25), communication (25). Score is the sum; missing the PDF or required live link caps the score at 40.",
        "is_active": True,
        "review_reason": "",
    })
    return result


def _build_lab_quality_errors(brief, domain, level, seen_companies, seen_industries):
    expected_count = {"Beginner": 3, "Intermediate": 4, "Advanced": 5}[brief["tier"]]
    errors = []
    if brief.get("domain") != domain or brief.get("level") != level:
        errors.append("domain or level mapping")
    if len(brief.get("requirements_list", [])) != expected_count:
        errors.append("tier requirement count")
    if sum(item.get("weight", 0) for item in brief.get("requirement_evidence", [])) != 100:
        errors.append("evidence weights")
    if sum(item.get("weight", 0) for item in brief.get("scoring", {}).get("criteria", [])) != 100:
        errors.append("scoring weights")
    if brief.get("company") in seen_companies or brief.get("industry") in seen_industries:
        errors.append("unique company or industry")
    if not all(brief.get(key) for key in ("company_context", "access_details", "task", "deadline", "tools", "dataset_schema")):
        errors.append("required brief context")
    return errors


for _domain in ("data_analytics", "ai_ml", "web_dev", "robotics", "electronics"):
    _seen_companies, _seen_industries = set(), set()
    for _index, _level_data in enumerate(RESTRUCTURED_CURRICULA[_domain]["levels"]):
        _company, _industry = _BUILD_LAB_COMPANIES[_domain][_index]
        _candidate = _build_lab_project(
            _domain, _index + 1, _level_data["name"], _level_data["project_json"], _company, _industry
        )
        _errors = _build_lab_quality_errors(
            _candidate, _domain, _index + 1, _seen_companies, _seen_industries
        )
        if _errors:
            _candidate = _build_lab_project(
                _domain, _index + 1, _level_data["name"], _level_data["project_json"], _company, _industry
            )
            _errors = _build_lab_quality_errors(
                _candidate, _domain, _index + 1, _seen_companies, _seen_industries
            )
        if _errors:
            _candidate["is_active"] = False
            _candidate["review_reason"] = "Build Lab quality gate failed."
            _candidate["quality_gate"] = {
                "status": "failed",
                "attempts": 2,
                "log": "Build Lab quality gate failed after regeneration: " + ", ".join(_errors),
            }
        else:
            _seen_companies.add(_company)
            _seen_industries.add(_industry)
        _level_data["project_json"] = _candidate

# Cyber Security is intentionally held for owner review; it must never become an
# active Build Lab brief during the refresh.
for _cyber_level in RESTRUCTURED_CURRICULA["cybersecurity"]["levels"]:
    _cyber_level["project_json"]["is_active"] = False
    _cyber_level["project_json"]["review_reason"] = "Cyber Security Build Lab briefs are pending owner review."
    _cyber_level["project_json"]["quality_gate"] = {
        "status": "inactive",
        "attempts": 0,
        "log": "Held inactive by the Cyber Security safety/owner-review policy.",
    }
