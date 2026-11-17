"""
Universal Smart Learning Engine for EXA AI HUB.
Supports all 6 learning domains across exactly 3 stages: Beginner, Intermediate, Advanced.
Implements the complete 8-part pedagogical teaching structure:
  A. Understand
  B. Learn
  C. Examples
  D. Practise
  E. Revise
  F. Quiz
  G. Master
  H. Advance
"""

import re
from typing import Dict, Any, List, Optional


def normalize_stage(stage: str) -> str:
    """Normalize learner stage to strictly one of: Beginner, Intermediate, Advanced."""
    val = (stage or '').strip().casefold()
    if 'adv' in val or any(f'level {i}' in val for i in range(9, 13)):
        return 'Advanced'
    if 'inter' in val or any(f'level {i}' in val for i in range(5, 9)):
        return 'Intermediate'
    return 'Beginner'


class SmartLearningEngine:
    """
    Universal reusable teaching and learning engine for EXA AI HUB.
    Dynamically generates stage-adapted, domain-specific learning modules.
    """

    @classmethod
    def get_stage(cls, level_or_stage: Any) -> str:
        if isinstance(level_or_stage, int):
            if level_or_stage <= 4:
                return 'Beginner'
            elif level_or_stage <= 8:
                return 'Intermediate'
            else:
                return 'Advanced'
        return normalize_stage(str(level_or_stage))

    @classmethod
    def build_lesson(
        cls,
        concept: str,
        guide: Dict[str, Any],
        domain_key: str,
        stage: str = 'Beginner',
        skill_name: str = '',
    ) -> Dict[str, Any]:
        """
        Build the complete 8-part teaching sequence:
        A. Understand -> B. Learn -> C. Examples -> D. Practise -> E. Revise -> F. Quiz -> G. Master -> H. Advance
        """
        stage = normalize_stage(stage)
        definition = guide.get("definition", f"{concept}: foundational concept in {domain_key}.")
        scenario = guide.get("scenario", f"A realistic engineering scenario involving {concept}.")
        example = guide.get("example", f"# Example implementation of {concept}")
        result = guide.get("result", f"Verified output showing {concept} in action.")
        pitfall = guide.get("pitfall", f"Avoid skipping validation when using {concept}.")
        practice = guide.get("practice", f"Apply {concept} to solve a realistic task.")

        # Stage-specific tone and depth
        stage_desc = {
            'Beginner': {
                'prefix': 'Beginner Foundation',
                'depth_text': 'Step-by-step introduction from first principles using clear, approachable terminology.',
                'prereq': 'No advanced prerequisites required. Starts from zero.',
            },
            'Intermediate': {
                'prefix': 'Intermediate Implementation',
                'depth_text': 'Practical engineering implementation, problem-solving, and real-world system behavior.',
                'prereq': 'Basic domain foundations and syntax understanding.',
            },
            'Advanced': {
                'prefix': 'Advanced Production & Architecture',
                'depth_text': 'Industry practices, system architecture, trade-offs, edge cases, and performance optimization.',
                'prereq': 'Solid practical experience with intermediate workflows and core principles.',
            },
        }[stage]

        # Domain-specific terminology and principles
        domain_data = cls._get_domain_enhancements(domain_key, concept, stage)

        # A. Understand
        understand_data = {
            "what_is_it": definition,
            "why_it_matters": (
                f"{concept} is essential because it {domain_data['why_matters']}. "
                f"In {domain_key.replace('_', ' ').title()}, mastering this enables reliable, professional results."
            ),
            "where_it_is_used": scenario,
            "problem_it_solves": domain_data['problem_solved'],
            "prerequisites": stage_desc['prereq'],
        }

        # B. Learn
        learn_data = {
            "detailed_explanation": (
                f"{definition}\n\n"
                f"How it works: {domain_data['how_it_works']}\n\n"
                f"Key Principles:\n{domain_data['key_principles_text']}"
            ),
            "step_by_step": domain_data['step_by_step'],
            "terminology": domain_data['terminology'],
            "how_it_works": domain_data['how_it_works'],
            "key_principles": domain_data['key_principles'],
            "formulas_or_shortcuts": domain_data['formulas_or_shortcuts'],
            "common_mistakes": [pitfall] + domain_data['additional_mistakes'],
        }

        # C. Examples
        examples_data = {
            "simple_example": domain_data['simple_example'],
            "practical_example": example,
            "real_world_application": scenario,
            "expected_outcome": result,
        }

        # D. Practise
        practise_data = {
            "guided_task": {
                "title": f"Guided Exercise: {concept}",
                "objective": f"Follow the step-by-step instructions to implement and verify {concept}.",
                "instructions": domain_data['guided_instructions'],
                "starter_content": domain_data['starter_content'],
                "hints": domain_data['hints'],
                "expected_outcome": result,
            },
            "independent_task": {
                "title": f"Independent Challenge: {concept}",
                "objective": f"Apply {concept} on your own to satisfy realistic requirements without step-by-step guidance.",
                "instructions": practice,
                "evaluation_criteria": [
                    f"Correct application of {concept}",
                    "Evidence-based verification of results",
                    "Proper handling of edge cases or common pitfalls",
                ],
                "expected_outcome": domain_data['independent_outcome'],
            },
            "small_project": domain_data.get('small_project', {
                "title": f"Mini Application for {concept}",
                "description": f"Build a focused working artifact demonstrating {concept} in context.",
            }),
        }

        # E. Revise
        revise_data = {
            "summary": f"{concept} at the {stage} stage: {definition}",
            "important_points": [
                f"Core idea: {definition}",
                f"Working approach: {domain_data['how_it_works']}",
                f"Verification: {result}",
                f"Key pitfall: {pitfall}",
            ],
            "key_terminology": [f"{item['term']}: {item['definition']}" for item in domain_data['terminology']],
            "formulas_and_shortcuts": domain_data['formulas_or_shortcuts'],
            "common_mistakes": [pitfall] + domain_data['additional_mistakes'],
            "targeted_revision_tips": domain_data['revision_tips'],
        }

        # F. Quiz Overview (questions generated adaptively)
        quiz_data = {
            "stage": stage,
            "pass_score_percentage": 80,
            "question_count": 5,
            "types_included": ["Conceptual", "Application", "Analysis & Debugging", "Scenario-based"],
        }

        # G. Master
        master_data = {
            "criteria": f"Score at least 80% (4/5) on the concept quiz and complete the practice exercises.",
            "rubric": [
                "Understands fundamental concept and terminology",
                "Applies concept correctly in code/calculations/scenarios",
                "Verifies results against expected outcomes",
                "Identifies and avoids known pitfalls",
            ],
            "mastery_status": "in_progress",
        }

        # H. Advance
        advance_data = {
            "next_step_advice": f"Review key terminology, complete the 5-question quiz, and proceed to the next concept.",
            "prerequisite_check": "Passed previous required topic quizzes in this level.",
        }

        # Structured lesson sections for UI rendering
        lesson_sections = [
            {"heading": "💡 A. Understand the Concept", "content": f"{understand_data['what_is_it']}\n\nWhy it matters: {understand_data['why_it_matters']}\n\nWhere it is used: {understand_data['where_it_is_used']}"},
            {"heading": "📖 B. Learn Step-by-Step", "content": f"{learn_data['detailed_explanation']}\n\nCommon mistake to avoid: {pitfall}"},
            {"heading": "💻 C. Implementation & Examples", "content": f"Working Example:\n{example}\n\nExpected Result:\n{result}"},
            {"heading": "🛠️ D. Guided & Independent Practice", "content": f"Task: {practise_data['guided_task']['instructions']}\n\nHint: {domain_data['hints'][0] if domain_data['hints'] else 'Check the worked example.'}\n\nExpected Outcome: {result}"},
            {"heading": "🔄 E. Key Revision & Takeaways", "content": "\n".join(f"• {pt}" for pt in revise_data['important_points'])},
        ]

        # Assemble full backward-compatible dictionary
        lesson = {
            "title": concept,
            "stage": stage,
            "domain": domain_key,
            "core_concept": definition,
            "deep_dive": f"Put it to work: {scenario}\n\nTry this:\n{example}\n\nCheck your result:\n{result}",
            "explanation": f"{definition}\n\nPut it to work: {scenario}\n\nTry this:\n{example}\n\nCheck your result:\n{result}",
            "real_world_use_case": scenario,
            "code_example": example,
            "example": example,
            "task": practice,
            "pro_tip": pitfall,
            "thinking_exercise": practice,
            "learning_objectives": [
                f"Explain {concept} clearly in your own words ({stage} stage).",
                f"Implement or apply {concept} to realistic problems.",
                f"Verify results against expected outcomes and avoid common pitfalls.",
            ],
            "lesson_sections": lesson_sections,
            "visual_aids": [],
            "key_points": [definition, result, pitfall],
            "concept_points": [definition, result, pitfall],
            "method_teach": [
                {"step": "Understand", "content": definition},
                {"step": "Apply", "content": example},
                {"step": "Check", "content": result},
            ],
            "mentor_note": f"Try the example, then explain why it works for {concept}.",

            # Rich 8-stage sequence extensions
            "understand": understand_data,
            "learn": learn_data,
            "examples": examples_data,
            "practise": practise_data,
            "revise": revise_data,
            "quiz_info": quiz_data,
            "mastery": master_data,
            "advance": advance_data,
        }

        return lesson

    @classmethod
    def _get_domain_enhancements(cls, domain_key: str, concept: str, stage: str) -> Dict[str, Any]:
        """Provides deep, domain-specific and stage-adapted educational material."""
        norm_concept = concept.casefold()

        # -------------------------------------------------------------
        # 1. DATA ANALYSIS (Special deep Excel coverage as required)
        # -------------------------------------------------------------
        if domain_key == 'data_analytics':
            if any(k in norm_concept for k in ('excel', 'formula', 'cell', 'sheet', 'workbook', 'xlookup', 'pivot', 'filter')):
                if 'xlookup' in norm_concept:
                    return {
                        'why_matters': 'replaces VLOOKUP and INDEX/MATCH with a faster, resilient search that looks left or right without breaking when columns move',
                        'problem_solved': 'Fragile lookups that fail when table columns are inserted or reordered.',
                        'how_it_works': 'Takes a lookup value, searches a lookup array, and returns the corresponding item from a return array with exact match default.',
                        'key_principles': ['Exact match by default', 'Can search left and right', 'Supports native if_not_found fallbacks'],
                        'key_principles_text': '1. Lookup value is the item you search for.\n2. Lookup array is where the item lives.\n3. Return array is where the target answer lives.\n4. If not found handles errors cleanly without nested IFERROR.',
                        'step_by_step': [
                            'Identify the value you want to match in the current table.',
                            'Select the column in the lookup range where that key exists.',
                            'Select the corresponding column from which you want to return data.',
                            'Add a default return message like "Not Found" for unmatched keys.',
                        ],
                        'terminology': [
                            {'term': 'Lookup Value', 'definition': 'The unique key you want to search for (e.g., product code).'},
                            {'term': 'Lookup Array', 'definition': 'The single column or row where Excel searches for the key.'},
                            {'term': 'Return Array', 'definition': 'The single column or row from which the matching data is retrieved.'},
                        ],
                        'formulas_or_shortcuts': [
                            '=XLOOKUP(A2, Products!A:A, Products!C:C, "Missing")',
                            'F4: Lock cell references into absolute $A$2 coordinates',
                            'Ctrl + Space: Select entire column in Excel',
                        ],
                        'additional_mistakes': [
                            'Selecting ranges of mismatched height (e.g. A2:A100 with C2:C50).',
                            'Forgetting to lock table references ($) before copying formulas down.',
                        ],
                        'simple_example': '=XLOOKUP("P101", A2:A10, B2:B10, "Not Found")',
                        'starter_content': 'Lookup Table:\nA2:A5 = [P101, P102, P103, P104]\nB2:B5 = [Apples, Oranges, Bananas, Grapes]\n\nTask Cell C2: Lookup P103',
                        'guided_instructions': 'Write =XLOOKUP("P103", A2:A5, B2:B5, "Missing") and confirm it returns Bananas.',
                        'hints': [
                            'Remember syntax: =XLOOKUP(lookup_value, lookup_range, return_range, [if_not_found])',
                            'Make sure lookup_range and return_range have the exact same number of rows.',
                        ],
                        'independent_outcome': 'Successfully returns the exact product name and handles invalid IDs with a friendly error.',
                        'small_project': {
                            'title': 'Automated Expense Categorizer',
                            'description': 'Use XLOOKUP to automatically map vendor names to budget categories in a monthly expense ledger.',
                        },
                        'revision_tips': 'Remember: XLOOKUP defaults to exact match (unlike VLOOKUP). Always verify that ranges share equal heights.',
                    }
                elif 'pivot' in norm_concept:
                    return {
                        'why_matters': 'allows analysts to slice, aggregate, and summarize millions of rows of transaction data in seconds without writing manual formulas',
                        'problem_solved': 'Manual summation across multiple categorical dimensions which is slow and prone to human calculation errors.',
                        'how_it_works': 'Groups identical values in row and column fields and applies aggregate calculations (Sum, Count, Average) to numerical value fields.',
                        'key_principles': ['Rows group data horizontally', 'Columns group data vertically', 'Values perform numeric aggregations', 'Filters isolate subsets'],
                        'key_principles_text': '1. Clean source data without blank header rows.\n2. Assign categorical fields to Rows or Columns.\n3. Assign numeric metrics to Values.\n4. Refresh the Pivot Table whenever source data changes.',
                        'step_by_step': [
                            'Select the continuous data table with clean header rows.',
                            'Insert -> PivotTable -> Choose New Worksheet.',
                            'Drag Categories to Rows, and Sales Amount to Values.',
                            'Change Value Field Settings to Currency format.',
                        ],
                        'terminology': [
                            {'term': 'Pivot Field', 'definition': 'A column header from your raw data table.'},
                            {'term': 'Value Field Setting', 'definition': 'The aggregate operation applied (SUM, COUNT, AVERAGE).'},
                            {'term': 'Slicer', 'definition': 'A visual interactive filter button connected to your Pivot Table.'},
                        ],
                        'formulas_or_shortcuts': [
                            'Alt + N + V: Insert Pivot Table shortcut',
                            'Alt + F5: Refresh active Pivot Table',
                            'Ctrl + Shift + 4 ($): Format cell as currency',
                        ],
                        'additional_mistakes': [
                            'Source data having blank header cells, which blocks Pivot Table creation.',
                            'Forgetting to refresh the Pivot Table when source rows are updated.',
                        ],
                        'simple_example': 'Drag "Department" to Rows and "Expense Amount" to Values (SUM).',
                        'starter_content': 'Columns: Date, Category, Amount\nRow 1: 2026-01-01, Food, 25.00\nRow 2: 2026-01-02, Transport, 15.00\nRow 3: 2026-01-03, Food, 40.00',
                        'guided_instructions': 'Create a Pivot Table grouping Category in Rows and SUM of Amount in Values. Total for Food should equal $65.00.',
                        'hints': [
                            'Ensure your data table has no blank headers.',
                            'Right-click any value cell to format as Currency.',
                        ],
                        'independent_outcome': 'A clean summary table showing total spend broken down by category and month.',
                        'small_project': {
                            'title': 'Executive Department Spend Breakdown',
                            'description': 'Build an interactive Pivot Table with Slicers analyzing quarterly expenses by department and category.',
                        },
                        'revision_tips': 'Remember: Pivot Tables do not auto-refresh on data change; use Alt+F5 or Refresh All.',
                    }
                else:
                    # General Excel & Formulas (Foundation: Interface, Cells, Rows, Columns, Expense Tracker)
                    return {
                        'why_matters': 'forms the universal foundation of business analytics, spreadsheets, data organization, and financial modeling',
                        'problem_solved': 'Disorganized records, manual arithmetic errors, and lack of systematic tracking.',
                        'how_it_works': 'Organizes data into Workbooks containing Worksheets with a grid of Rows (numbered) and Columns (lettered). Cells store text, numbers, or calculated formulas beginning with "=".',
                        'key_principles': [
                            'Excel Interface: Ribbon, Formula Bar, Name Box, Sheet Tabs',
                            'Grid structure: Columns (A, B, C...) intersect Rows (1, 2, 3...) to create unique Cell addresses (A1, B5)',
                            'Formulas always start with an equals sign (=)',
                            'Relative references (A1) adjust when copied; Absolute references ($A$1) stay locked',
                        ],
                        'key_principles_text': (
                            '1. Excel Interface: The Ribbon contains tools (Home, Insert, Formulas, Data). The Formula Bar displays cell logic.\n'
                            '2. Workbooks & Worksheets: A Workbook is your file (.xlsx); Worksheets are individual sheets inside.\n'
                            '3. Data Entry & Formatting: Text aligns left, numbers align right. Always format currency, dates, and percentages.\n'
                            '4. Essential Formulas: =SUM(A1:A10), =AVERAGE(B1:B10), =COUNT(C1:C10), =IF(D1>100, "High", "Low").\n'
                            '5. Absolute References: Use $ to freeze references (e.g. $A$1) so copying formulas preserves the target cell.'
                        ),
                        'step_by_step': [
                            'Open Excel and explore the Workbook layout, Worksheet tabs, and Ribbon menus.',
                            'Enter column headers in Row 1: Date, Category, Description, Amount.',
                            'Enter data rows and format the Amount column as Currency ($).',
                            'In the total row, type =SUM(D2:D10) or press Alt+= (AutoSum).',
                            'Verify the calculated total against manual summation.',
                        ],
                        'terminology': [
                            {'term': 'Workbook vs Worksheet', 'definition': 'Workbook is the Excel file; Worksheet is a single spreadsheet tab.'},
                            {'term': 'Cell & Address', 'definition': 'Intersection of column and row (e.g. C4 = Column C, Row 4).'},
                            {'term': 'Formula Bar', 'definition': 'Top input area where formula expressions are inspected and edited.'},
                            {'term': 'AutoSum', 'definition': 'Instant formula generator =SUM(...) for contiguous numerical rows or columns.'},
                        ],
                        'formulas_or_shortcuts': [
                            '=SUM(range) — adds all numbers in range',
                            '=AVERAGE(range) — computes mean',
                            'Alt + = (AutoSum) — instantly sums adjacent cells',
                            'Ctrl + Z / Ctrl + Y — Undo / Redo',
                            'Ctrl + Arrow keys — Jump to edge of data region',
                            'F4 — Toggle reference lock (A1 -> $A$1 -> A$1 -> $A1)',
                        ],
                        'additional_mistakes': [
                            'Typing formulas without the leading "=" sign, causing Excel to treat it as plain text.',
                            'Writing hardcoded values inside formulas (e.g., =A1 + 15.50) instead of referencing a separate parameter cell.',
                            'Mixing text and numbers in the same column, breaking =SUM calculations.',
                        ],
                        'simple_example': '=SUM(B2:B10)',
                        'starter_content': 'Expense Tracker Starter:\nDate | Category | Description | Amount\n2026-01-01 | Office | Paper & Pens | 24.50\n2026-01-02 | Software | Cloud Hosting | 50.00\n2026-01-03 | Travel | Train Ticket | 32.00\nTotal: =SUM(D2:D4)',
                        'guided_instructions': 'Enter the 3 expense rows above. In cell D5, write =SUM(D2:D4) and format cell D5 as Currency. Verify it displays $106.50.',
                        'hints': [
                            'Remember to format numerical cells as Currency using the Home Ribbon or Ctrl+Shift+$',
                            'Use the AutoSum shortcut (Alt+=) on cell D5.',
                        ],
                        'independent_outcome': 'A fully functioning Personal Expense Tracker with date, category, amount, running totals, and category sum.',
                        'small_project': {
                            'title': 'Building a Real Monthly Expense Tracker',
                            'description': 'Create an Excel monthly expense workbook with formatted columns (Date, Category, Vendor, Amount), automated totals with =SUM, average daily spend with =AVERAGE, and summary cards.',
                        },
                        'revision_tips': 'Always verify: 1. Formulas start with "=". 2. Cell coordinates match your data range. 3. Numbers are formatted properly.',
                    }

        # -------------------------------------------------------------
        # 2. FULL STACK DEVELOPMENT (web_dev)
        # -------------------------------------------------------------
        if domain_key == 'web_dev':
            return {
                'why_matters': 'powers modern client-server web applications, scalable APIs, and responsive browser interfaces',
                'problem_solved': 'Building reliable, maintainable software accessible to users across browsers and devices.',
                'how_it_works': 'Web clients exchange HTTP/HTTPS request and response messages with backend servers over TCP/IP, rendering DOM nodes and manipulating state.',
                'key_principles': [
                    'Separation of Concerns: Structure (HTML), Presentation (CSS), Behavior (JS), Data & Business Logic (Backend)',
                    'Stateless HTTP: Requests carry needed state or rely on sessions/cookies/tokens',
                    'Idempotent APIs: Safe GETs, validated POST/PUT/DELETE operations',
                ],
                'key_principles_text': (
                    '1. Client-Server Architecture: The browser renders UI and sends requests; the server validates data, queries DB, and returns JSON or HTML.\n'
                    '2. Asynchronous Flow: Non-blocking I/O with Promises and async/await prevents UI freezes.\n'
                    '3. Defense in Depth: Validate inputs on both client and server; sanitize outputs to prevent XSS and SQL injection.'
                ),
                'step_by_step': [
                    'Define the data structure and schema required for the feature.',
                    'Build the backend endpoint / route and test request/response status codes.',
                    'Connect the frontend UI via Fetch API or component state.',
                    'Test error scenarios: missing parameters, network timeouts, invalid inputs.',
                ],
                'terminology': [
                    {'term': 'HTTP Method', 'definition': 'Action verb (GET, POST, PUT, DELETE) indicating intended operation.'},
                    {'term': 'REST API', 'definition': 'Stateless architectural style using standard HTTP conventions and JSON payloads.'},
                    {'term': 'DOM', 'definition': 'Document Object Model: tree representation of HTML elements in memory.'},
                ],
                'formulas_or_shortcuts': [
                    'fetch("/api/data").then(res => res.json())',
                    'Ctrl + Shift + I: Open Browser DevTools',
                    'git checkout -b feature-branch: create clean branch',
                ],
                'additional_mistakes': [
                    'Relying solely on frontend validation; backend endpoints must always re-validate data.',
                    'Mutating state directly rather than creating clean immutable updates.',
                ],
                'simple_example': 'fetch("/api/items").then(r => r.json()).then(console.log);',
                'starter_content': 'async function loadData() {\n  // Fetch items and display them\n}',
                'guided_instructions': 'Implement a GET fetch request with try/catch error handling that logs received JSON records.',
                'hints': [
                    'Check response.ok before parsing response.json()',
                    'Always handle network exceptions in a catch block.',
                ],
                'independent_outcome': 'A fully working, error-handled API integration showing loading, success, and error UI states.',
                'small_project': {
                    'title': 'Mini REST Service & Client Interface',
                    'description': 'Construct a RESTful CRUD endpoint connected to a clean frontend list view with add/delete operations.',
                },
                'revision_tips': 'Review the HTTP status codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 500 (Server Error).',
            }

        # -------------------------------------------------------------
        # 3. AI & MACHINE LEARNING (ai_ml)
        # -------------------------------------------------------------
        if domain_key == 'ai_ml':
            return {
                'why_matters': 'enables systems to learn patterns from historical data to make automated predictions, classifications, and decisions',
                'problem_solved': 'Solving complex pattern recognition problems that are too intricate for static rules or hand-coded logic.',
                'how_it_works': 'Features are extracted from cleaned datasets, fed into parameterized algorithms, optimized via loss minimization, and evaluated on unseen test data.',
                'key_principles': [
                    'Supervised vs Unsupervised: Labeled targets vs discovered structure',
                    'Train/Test Split: Prevent overfitting by keeping test data strictly unseen',
                    'Metric Alignment: Use MSE/MAE for regression; Accuracy, Precision, Recall, F1 for classification',
                ],
                'key_principles_text': (
                    '1. Data Preparation: Clean missing values, scale numeric features, and encode categorical variables.\n'
                    '2. Model Selection: Choose an algorithm suited to problem size and linearity.\n'
                    '3. Training & Validation: Minimize loss function on training split; validate on independent test split.\n'
                    '4. Evaluation: Check confusion matrix and precision/recall trade-offs before deploying.'
                ),
                'step_by_step': [
                    'Inspect dataset shape, distributions, and missing values.',
                    'Split features (X) and target (y) into train and test sets (e.g. 80/20).',
                    'Fit the model on training data using .fit(X_train, y_train).',
                    'Generate predictions on X_test and calculate evaluation metrics.',
                ],
                'terminology': [
                    {'term': 'Overfitting', 'definition': 'Model memorizes training noise and fails to generalize to new test data.'},
                    {'term': 'Loss Function', 'definition': 'Mathematical function quantifying the penalty between prediction and actual target.'},
                    {'term': 'Confusion Matrix', 'definition': 'Table displaying True Positives, False Positives, True Negatives, False Negatives.'},
                ],
                'formulas_or_shortcuts': [
                    'MSE = (1/n) * SUM((y_true - y_pred)^2)',
                    'Accuracy = (TP + TN) / (TP + TN + FP + FN)',
                    'Precision = TP / (TP + FP); Recall = TP / (TP + FN)',
                ],
                'additional_mistakes': [
                    'Data leakage: Scaling or imputing features on the entire dataset before splitting train and test sets.',
                    'Evaluating an imbalanced dataset solely on accuracy.',
                ],
                'simple_example': 'from sklearn.model_selection import train_test_split\nX_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2)',
                'starter_content': 'import numpy as np\n# Prepare features and train simple estimator',
                'guided_instructions': 'Create an 80/20 train/test split, fit a linear estimator, and output the test set Mean Squared Error.',
                'hints': [
                    'Never fit scalers on test data; fit on train, transform on test.',
                    'Check baseline dummy predictions to verify your model genuinely learns.',
                ],
                'independent_outcome': 'A trained model evaluated on holdout data with documented accuracy, precision, and recall.',
                'small_project': {
                    'title': 'Predictive Model Training & Evaluation Pipeline',
                    'description': 'Train a classifier on realistic tabular data, tune hyper-parameters, and report performance with a Confusion Matrix.',
                },
                'revision_tips': 'Keep the golden rule: Test data must remain untouched until final model evaluation.',
            }

        # -------------------------------------------------------------
        # 4. ROBOTICS (robotics)
        # -------------------------------------------------------------
        if domain_key == 'robotics':
            return {
                'why_matters': 'bridges physical mechanics, electronics, microcontrollers, and software to sense the environment and actuate motion safely',
                'problem_solved': 'Automating physical tasks in uncertain real-world environments through feedback loops.',
                'how_it_works': 'Sensors collect analog/digital environmental signals, microcontrollers execute control logic, and actuators convert electrical signals into mechanical motion.',
                'key_principles': [
                    'Sense -> Plan -> Act cycle',
                    'Ohm’s Law: V = I * R and Power = V * I',
                    'PWM (Pulse Width Modulation): Duty cycle modulates speed or servo angle',
                    'Closed-Loop Control: Feedback corrects error between target and measured state',
                ],
                'key_principles_text': (
                    '1. Hardware Safety: Never connect high-current loads directly to microcontroller pins; use motor drivers or transistors.\n'
                    '2. Signal Acquisition: Digital pins read binary 0/1; Analog pins (ADC) read continuous voltage mapped to numerical values.\n'
                    '3. Actuation: PWM controls motor speed by varying the percentage of time power is ON in high-frequency pulses.\n'
                    '4. Feedback: Use encoders or ultrasonic sensors to measure position and prevent collisions.'
                ),
                'step_by_step': [
                    'Design schematic and verify safe voltage/current limits.',
                    'Connect sensor inputs and verify multimeter/serial readings.',
                    'Configure motor driver / H-bridge with external power supply and common ground.',
                    'Implement control loop with boundary safety checks and emergency stop logic.',
                ],
                'terminology': [
                    {'term': 'PWM', 'definition': 'Pulse Width Modulation: fast switching technique to simulate analog output.'},
                    {'term': 'ADC', 'definition': 'Analog to Digital Converter: translates continuous voltage to digital integers.'},
                    {'term': 'H-Bridge', 'definition': 'Circuit topology that allows DC motors to run forwards and backwards.'},
                ],
                'formulas_or_shortcuts': [
                    'V = I * R (Voltage = Current * Resistance)',
                    'Duty Cycle (%) = (Time_ON / Total_Period) * 100',
                    'Common Ground Rule: All power supplies must share a common GND reference.',
                ],
                'additional_mistakes': [
                    'Forgetting to connect micro-controller GND and external motor battery GND.',
                    'Powering high-draw DC motors directly from a 5V/3.3V board regulator.',
                ],
                'simple_example': 'analogWrite(motorPin, 180); // ~70% duty cycle speed',
                'starter_content': '// Setup sensor input and motor driver pins\nvoid setup() {\n  pinMode(trigPin, OUTPUT);\n  pinMode(echoPin, INPUT);\n}',
                'guided_instructions': 'Read ultrasonic sensor distance in cm. If distance < 20 cm, set motor output to 0 (halt).',
                'hints': [
                    'Speed of sound is approximately 0.0343 cm/microsecond.',
                    'Always verify pin polarity before applying battery power.',
                ],
                'independent_outcome': 'A working obstacle avoidance state loop that halts or turns away when nearing boundaries.',
                'small_project': {
                    'title': 'Autonomous Obstacle-Navigating Robot Simulation',
                    'description': 'Construct a complete state-machine loop that reads distance sensors, triggers turn routines, and prevents stall conditions.',
                },
                'revision_tips': 'Always check: 1. Common ground established. 2. Motor driver flyback diode protection. 3. Sensor calibration.',
            }

        # -------------------------------------------------------------
        # 5. ELECTRICAL & ELECTRONICS ENGINEERING (electronics / EEE)
        # -------------------------------------------------------------
        if domain_key == 'electronics':
            return {
                'why_matters': 'forms the fundamental science and engineering of circuits, voltage, current, components, power, and signal conditioning',
                'problem_solved': 'Designing safe, stable electrical paths that deliver power and process signals without component failure or signal degradation.',
                'how_it_works': 'Electromotive force (Voltage) drives charge carriers (Current) through resistive, capacitive, inductive, and semiconductor network paths obeying Kirchhoff’s Laws.',
                'key_principles': [
                    'Ohm’s Law: V = I * R, I = V / R, R = V / I',
                    'Kirchhoff’s Current Law (KCL): Current entering a node equals current exiting it',
                    'Kirchhoff’s Voltage Law (KVL): Sum of voltages around a closed circuit loop equals zero',
                    'Voltage Divider: V_out = V_in * (R2 / (R1 + R2))',
                ],
                'key_principles_text': (
                    '1. Current flows through closed loops with return paths to ground (0V reference).\n'
                    '2. Series circuits share the same current; voltage drops divide across components.\n'
                    '3. Parallel circuits share the same voltage across branches; branch currents add up.\n'
                    '4. Component Ratings: Never exceed power rating P = V * I = I^2 * R, or capacitor breakdown voltages.'
                ),
                'step_by_step': [
                    'Sketch the schematic diagram identifying DC source, switches, resistors, and grounds.',
                    'Calculate expected current using Ohm\'s law: I = (V_supply - V_diode) / R.',
                    'Select component power ratings ensuring P_actual < P_rated * 0.7 for safety margin.',
                    'Assemble on breadboard and verify using multimeter DC voltage and resistance ranges.',
                ],
                'terminology': [
                    {'term': 'Voltage (V)', 'definition': 'Electrical potential difference measured in Volts.'},
                    {'term': 'Current (I)', 'definition': 'Flow rate of electric charge measured in Amperes.'},
                    {'term': 'Resistance (R)', 'definition': 'Opposition to electric current measured in Ohms (Ω).'},
                    {'term': 'Multimeter', 'definition': 'Test tool measuring voltage, current, resistance, and continuity.'},
                ],
                'formulas_or_shortcuts': [
                    'V = I * R | P = V * I | P = I^2 * R',
                    'V_out = V_in * (R2 / (R1 + R2)) (Voltage Divider)',
                    'LED Resistor: R = (V_supply - V_forward) / I_target',
                ],
                'additional_mistakes': [
                    'Connecting an ammeter in parallel with a voltage source (causes high current short-circuit and blows meter fuse).',
                    'Omitting a current-limiting resistor with LEDs, immediately burning them out.',
                ],
                'simple_example': 'R = (9V - 2V) / 0.02A = 350 Ohms (Use nearest standard: 390Ω)',
                'starter_content': 'Supply: 9V DC\nLED Forward Voltage: 2.1V\nTarget Current: 15 mA (0.015 A)\nCalculate: R_limiter',
                'guided_instructions': 'Calculate the required resistor: R = (9 - 2.1) / 0.015 = 460Ω. Choose standard 470Ω and calculate resistor power P = I^2 * R.',
                'hints': [
                    'Convert milliamps to amperes by dividing by 1000 (15 mA = 0.015 A).',
                    'A 1/4 watt resistor handles up to 0.25W. Check that P < 0.25W.',
                ],
                'independent_outcome': 'Accurately designed and verified circuit delivering target current without thermal overload.',
                'small_project': {
                    'title': 'Bench Voltage Divider & Sensor Signal Conditioning Circuit',
                    'description': 'Design a two-resistor voltage divider to scale a 12V automotive signal safely down to 3.3V for microcontroller ADC reading.',
                },
                'revision_tips': 'Measure voltages with meter probes in parallel; measure current by breaking circuit and inserting meter in series.',
            }

        # -------------------------------------------------------------
        # 6. CYBERSECURITY (cybersecurity)
        # -------------------------------------------------------------
        if domain_key == 'cybersecurity':
            return {
                'why_matters': 'protects critical systems, networks, applications, and sensitive data against unauthorized access, compromise, and disruption',
                'problem_solved': 'Defending infrastructure against security vulnerabilities, data breaches, and malicious actors within authorized boundaries.',
                'how_it_works': 'Applies defense-in-depth principles: strong authentication, least privilege access control, encryption in transit and at rest, and continuous audit logging.',
                'key_principles': [
                    'CIA Triad: Confidentiality, Integrity, and Availability',
                    'Principle of Least Privilege: Grant only permissions strictly required for the role',
                    'Defense in Depth: Layered security controls so single failure does not compromise system',
                    'Authorized Scope: Conduct defensive testing exclusively in approved local lab environments',
                ],
                'key_principles_text': (
                    '1. Defensive Scope: All activities must be authorized, defensive, and performed in local virtual sandbox labs.\n'
                    '2. Network Security: Secure ports, inspect packet headers, and block unneeded ingress traffic with firewalls.\n'
                    '3. Application Security: Never trust client input; use parameterized queries, output encoding, and secure session flags.\n'
                    '4. Monitoring: Maintain audit logs for failed logins and anomalous traffic.'
                ),
                'step_by_step': [
                    'Establish isolated local test environment within documented authorized scope.',
                    'Audit open network ports and running services using local defensive tools.',
                    'Identify misconfigurations (default passwords, exposed debug endpoints, missing security headers).',
                    'Implement defensive remediation, re-test to confirm fix, and document findings.',
                ],
                'terminology': [
                    {'term': 'Least Privilege', 'definition': 'Restricting user and process rights to bare minimum required.'},
                    {'term': 'Defense in Depth', 'definition': 'Multiple redundant defensive layers protecting assets.'},
                    {'term': 'OWASP Top 10', 'definition': 'Standard consensus document on critical web application security risks.'},
                ],
                'formulas_or_shortcuts': [
                    'sudo iptables -L -n -v (inspect firewall rules)',
                    'ssh-keygen -t ed25519 (generate strong modern key pair)',
                    'Hash verification: sha256sum file.iso',
                ],
                'additional_mistakes': [
                    'Testing tools against real public domains without written authorization (illegal and unethical).',
                    'Storing plaintext passwords in databases instead of salted cryptographic hashes (e.g. bcrypt/argon2).',
                ],
                'simple_example': 'SELECT * FROM users WHERE username = ?; -- Parameterized query preventing SQL injection',
                'starter_content': '# Audit local SSH configuration for root login\nPermitRootLogin no\nPasswordAuthentication no',
                'guided_instructions': 'Review a local sshd_config file, disable PermitRootLogin, and enforce public key authentication.',
                'hints': [
                    'Look for PermitRootLogin directive in /etc/ssh/sshd_config.',
                    'Always verify you have another working session before restarting SSH service.',
                ],
                'independent_outcome': 'Hardened configuration verified against security checklist without service downtime.',
                'small_project': {
                    'title': 'Local Defensive System Hardening & Security Audit',
                    'description': 'Audit a local test system, close unneeded listening ports, configure firewall rules, and generate an executive remediation report.',
                },
                'revision_tips': 'Golden rule: Always operate strictly inside authorized lab boundaries and prioritize defensive remediation.',
            }

        # Generic Tech Fallback
        return {
            'why_matters': f'provides foundational capability for {concept}',
            'problem_solved': f'Addresses complexity and failure modes in {concept}.',
            'how_it_works': f'Executes systematic processes to achieve predictable outcomes for {concept}.',
            'key_principles': ['Systematic approach', 'Verification of results', 'Continuous improvement'],
            'key_principles_text': '1. Understand requirements.\n2. Implement smallest working solution.\n3. Validate thoroughly.',
            'step_by_step': ['Define goal', 'Implement solution', 'Test outcomes', 'Document results'],
            'terminology': [{'term': concept, 'definition': f'Core topic in {domain_key}.'}],
            'formulas_or_shortcuts': [f'Check {concept} documentation for recommended syntax'],
            'additional_mistakes': ['Skipping testing before production release'],
            'simple_example': f'# Example usage of {concept}',
            'starter_content': f'// Implement {concept}',
            'guided_instructions': f'Implement a small working example of {concept} and verify output.',
            'hints': ['Refer to the core explanation and step-by-step instructions.'],
            'independent_outcome': f'Working verification of {concept}.',
            'small_project': {'title': f'{concept} Implementation Project', 'description': f'Build a practical working implementation of {concept}.'},
            'revision_tips': 'Review the key principles and verify your results before moving to the next level.',
        }

    @classmethod
    def build_quiz_questions(
        cls,
        concept: str,
        guide: Dict[str, Any],
        domain_key: str,
        stage: str = 'Beginner',
    ) -> List[Dict[str, Any]]:
        """
        Generate 5 stage-adapted, authentic quiz questions with thorough explanations.
        Diverse question types: Concept understanding, practical application, code/calc check, scenario analysis.
        """
        stage = normalize_stage(stage)
        definition = guide.get("definition", f"{concept} fundamentals")
        example = guide.get("example", f"implementation of {concept}")
        result = guide.get("result", f"expected outcome for {concept}")
        pitfall = guide.get("pitfall", f"common mistake with {concept}")
        practice = guide.get("practice", f"applying {concept}")

        # Check if guide has a dedicated quiz_factory (e.g. for specialized tests)
        if guide.get("quiz_factory"):
            return guide["quiz_factory"](concept, guide)

        clean_concept = concept.replace("Level ", "").strip()

        # Generate base questions according to stage
        raw_questions = [
            (
                f"What is the primary role and core definition of {clean_concept} in {domain_key.replace('_', ' ').title()}?",
                definition,
                "It is a decorative labeling convention that has no functional impact on results.",
                "It is an obsolete tool that has been completely deprecated in modern practice.",
                "It is a method used exclusively to bypass security and validation checks.",
                f"Correct! {clean_concept} is defined as: {definition}.",
                "conceptual",
            ),
            (
                f"When working practically with {clean_concept}, which implementation step or syntax is correct?",
                example,
                "Skip inspecting source inputs and accept the first generated result blindly.",
                "Change configuration randomly until an error message disappears.",
                "Delete all log files and ignore error warnings during execution.",
                f"Correct! The standard practical implementation is: {example}.",
                "practical",
            ),
            (
                f"After applying {clean_concept}, which measurable result verifies that your work succeeded?",
                result,
                "The process terminates without reading any inputs or producing output.",
                "The output contradicts the underlying source data but looks plausible.",
                "A colleague guesses that the numbers look fine without inspecting evidence.",
                f"Correct! Expected outcome to verify: {result}.",
                "verification",
            ),
            (
                f"Which common pitfall or dangerous mistake should you actively avoid with {clean_concept}?",
                pitfall,
                "Reading error messages when an execution fails.",
                "Writing down notes about how your solution works.",
                "Comparing calculated output against known source records.",
                f"Correct! You must actively avoid this pitfall: {pitfall}.",
                "debugging",
            ),
            (
                f"What is the most effective way to demonstrate that you have mastered {clean_concept}?",
                practice,
                "Memorizing terms by heart without ever testing them on real examples.",
                "Copying someone else's output without understanding the underlying steps.",
                "Claiming mastery without running the code or checking the calculation.",
                f"Correct! True learning requires practical application: {practice}.",
                "application",
            ),
        ]

        # Use positions from guide if provided, else use stage-appropriate distinct positions
        positions = guide.get("quiz_answer_positions", (1, 3, 0, 2, 1))
        letters = "ABCD"

        quiz = []
        for index, ((q_text, correct, dist1, dist2, dist3, explanation, q_type), pos) in enumerate(zip(raw_questions, positions)):
            distractors = [dist1, dist2, dist3]
            # Ensure unique options
            options = []
            for i, opt in enumerate(distractors):
                options.append(opt)
            options.insert(pos % 4, correct)
            # Ensure 4 unique options
            seen = set()
            clean_opts = []
            for opt in options:
                if opt in seen:
                    clean_opts.append(f"{opt} (alternative scenario)")
                else:
                    seen.add(opt)
                    clean_opts.append(opt)

            correct_letter = letters[pos % 4]
            quiz.append({
                "question_text": q_text,
                "option_a": clean_opts[0],
                "option_b": clean_opts[1],
                "option_c": clean_opts[2],
                "option_d": clean_opts[3],
                "correct_answer": correct_letter,
                "answer_key": correct_letter,
                "explanation": explanation,
                "question_type": q_type,
                "difficulty": stage,
            })

        return quiz
