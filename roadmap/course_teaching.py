"""Topic-specific lesson and quiz material for the curated curricula."""



from .course_content import LEVEL_CONCEPTS





def _guide(

    concept,

    definition,

    scenario,

    example,

    result,

    pitfall,

    practice,

    **extras,

):

    guide = {

        "definition": f"{concept}: {definition}",

        "scenario": scenario,

        "example": example,

        "result": result,

        "pitfall": pitfall,

        "practice": practice,

    }

    guide.update(extras)

    return guide





def _match(concept, rules):

    normalized = concept.casefold()

    for words, guide in rules:

        if any(word in normalized for word in words):

            return guide(concept)

    return None





def get_course_guide(domain, skill_name, concept):

    """Return a focused guide when the concept belongs to a curated course."""

    level = _level_number(skill_name)

    rules = _COURSE_RULES.get(domain, {}).get(level, ())

    matched = _match(concept, rules)

    if matched:

        matched["domain"] = domain

        matched["tier"] = "Beginner" if (level or 1) <= 4 else "Intermediate" if (level or 1) <= 8 else "Advanced"

        matched["level"] = level

    if matched:
        matched["domain"] = domain
        matched["tier"] = "Beginner" if (level or 1) <= 4 else "Intermediate" if (level or 1) <= 8 else "Advanced"
        matched["level"] = level
    # #region agent log

    import json, time

    try:

        with open(r"c:\Users\THOUSEEQ\Downloads\TA JNR AI\debug-13ca71.log", "a", encoding="utf-8") as _f:

            _f.write(json.dumps({

                "sessionId": "13ca71",

                "runId": "pre-fix",

                "hypothesisId": "B",

                "location": "course_teaching.py:get_course_guide",

                "message": "course guide lookup",

                "data": {

                    "domain": domain,

                    "skill_name": skill_name,

                    "concept": concept,

                    "level": level,

                    "rule_count": len(rules) if rules else 0,

                    "matched": bool(matched),

                    "has_example": bool((matched or {}).get("example")),

                },

                "timestamp": int(time.time() * 1000),

            }) + "\n")

    except Exception:

        pass

    # #endregion

    return matched





def build_course_lesson(concept, guide, domain_key=None, stage=None):

    from .smart_learning_engine import SmartLearningEngine

    domain = domain_key or guide.get("domain", "web_dev")

    tier = stage or guide.get("tier", "Beginner")

    return SmartLearningEngine.build_lesson(concept, guide, domain, tier)





def build_course_quiz(concept, guide, domain_key=None, stage=None):

    from .smart_learning_engine import SmartLearningEngine

    domain = domain_key or guide.get("domain", "web_dev")

    tier = stage or guide.get("tier", "Beginner")

    return SmartLearningEngine.build_quiz_questions(concept, guide, domain, tier)





def _electronics_quiz(concept, guide):

    """Topic-specific Level 1 robotics checks; metadata is not shown to learners."""

    correct = [guide["definition"], guide["example"], guide["result"], guide["pitfall"]]

    prompts = [

        f"{concept}: which statement gives the correct core idea?",

        f"{concept}: which step is appropriate in the supplied bench example?",

        f"True or false â€” {concept} should be checked against the stated expected result.",

        f"{concept}: which safety or setup mistake must be avoided?",

    ]

    options = [

        [correct[0], "It is only a decorative label on a circuit diagram.", "It removes the need for a return path.", "It is interchangeable with every other electronics quantity."],

        [correct[1], "Connect the component directly to an unknown power source.", "Skip measurement and estimate the outcome by eye.", "Reverse every connection to see what happens."],

        ["True", "False", "Only when no meter is available", "Only for AC circuits"],

        [correct[3], "Label parts after powering the circuit.", "Assume all LEDs and resistors have identical limits.", "Ignore polarity because low voltage is always harmless."],

    ]

    answers = ["A", "A", "A", "A"]

    return [

        {

            "question_text": prompt,

            "option_a": choices[0], "option_b": choices[1], "option_c": choices[2], "option_d": choices[3],

            "correct_answer": answer, "answer_key": answer,

            "question_type": "true_false" if index == 2 else "multiple_choice",

            "explanation": correct[index],

        }

        for index, (prompt, choices, answer) in enumerate(zip(prompts, options, answers))

    ]

def _level_number(skill_name):

    import re



    match = re.search(r"\blevel\s+(\d+)\b", skill_name or "", re.IGNORECASE)

    return int(match.group(1)) if match else None





def _data_rules():

    return {

        1: [

            (("xlookup",), lambda c: _guide(

                c, "a modern lookup formula that searches a range or array and returns corresponding items from another range with exact match default.",

                "A finance analyst needs to match product codes to standard item names across separate tables.",

                '=XLOOKUP(A2, ProductIDs, ProductNames, "Not found")',

                "The lookup returns the matching product name, or the fallback text when there is no match.",

                "Check that lookup ranges have identical height; mismatched ranges cause formula errors.",

                "Use a small sample with one matching and one missing ID, then confirm both outputs.",

            )),

            (("pivot",), lambda c: _guide(

                c, "an interactive spreadsheet tool that groups, aggregates, and summarizes tabular records without writing complex manual formulas.",

                "A business manager needs a breakdown of monthly expenses grouped by department and category.",

                '# Insert PivotTable -> Rows: Category, Values: SUM of Amount, Slicer: Month',

                "The Pivot Table displays aggregated totals per category and updates instantly when refreshed.",

                "Ensure source data has no blank column headers, and refresh the Pivot Table after source updates.",

                "Create a Pivot Table grouping expenses by category, format values as Currency, and check the grand total.",

            )),

            (("filter",), lambda c: _guide(

                c, "a spreadsheet feature that displays only the rows meeting specified criteria while hiding the rest.",

                "An auditor needs to review all transaction records where expense amount exceeds $500.",

                '# Data Ribbon -> Filter -> Amount Column Dropdown -> Number Filters -> Greater Than 500',

                "Only transactions exceeding $500 are visible, allowing focused inspection without deleting other rows.",

                "Remember that hidden rows are still present; verify whether downstream formulas include or exclude filtered rows.",

                "Apply a filter for high-value expenses, note the visible row count, and clear the filter when done.",

            )),

            (("formula", "excel"), lambda c: _guide(

                c, "the foundational spreadsheet environment and calculation engine organizing data in workbooks, worksheets, rows, columns, and cells.",

                "A personal finance learner is building a monthly expense tracker with date, category, and expense amounts.",

                '=SUM(D2:D10)  # AutoSum calculating total monthly expenses across rows 2 to 10',

                "Cell D11 displays the formatted currency sum of all expense rows, updating dynamically when values change.",

                "Formulas must always start with an equals sign (=); text typed without = will not calculate.",

                "Build an expense tracker with Date, Category, Description, and Amount columns, and calculate total spend with =SUM.",

            )),

        ],

        2: [

            (("variable", "loop", "function", "list", "dictionary", "python"), lambda c: _guide(

                c, "a Python building block for storing, repeating, or organizing analysis steps.",

                "A team receives daily sales and wants a repeatable total instead of manual addition.",

                "sales = [12, 18, 10]\nweekly_total = sum(sales)\nprint(weekly_total)",

                "The total is 40; the list keeps the values together and sum adds them.",

                "Watch data types and empty inputs; valid-looking text can fail arithmetic.",

                "Change one sale, predict the new total, and check your prediction.",

            )),

        ],

        3: [

            (("csv", "null", "missing", "filter", "sort", "pandas"), lambda c: _guide(

                c, "a Pandas step for loading, checking, cleaning, or selecting rows in a table.",

                "A gym wants to compare renewal rates without letting missing membership data distort the result.",

                "import pandas as pd\ndf = pd.read_csv('members.csv')\ndf['renewed'].value_counts(dropna=False)",

                "The count includes missing renewal values, making data gaps visible before filtering.",

                "Do not drop nulls automatically; first check whether missingness is concentrated in a group.",

                "Count missing values by column and explain which records you would keep or exclude.",

            )),

        ],

        4: [

            (("select", "where", "order by", "group by", "aggregate", "sql basics"), lambda c: _guide(

                c, "a SQL clause or aggregate for selecting, filtering, sorting, or summarising rows.",

                "A telecom team wants churn counts by plan, using only active customer records.",

                "SELECT plan, COUNT(*) AS customers\nFROM subscribers\nWHERE status = 'active'\nGROUP BY plan\nORDER BY customers DESC;",

                "Each active plan appears once, sorted from the largest customer count to the smallest.",

                "Filter rows with WHERE before grouping; use HAVING only to filter aggregated groups.",

                "Add a churn condition and verify the total grouped count against the filtered row count.",

            )),

        ],

        5: [

            (("outlier",), lambda c: _guide(

                c, "an observation far from the overall pattern that may be an error or a meaningful rare event.",

                "A retailer sees one unusually large order and needs to know whether it is a data-entry issue or a genuine bulk purchase.",

                "q1 = df['amount'].quantile(.25)\nq3 = df['amount'].quantile(.75)\niqr = q3 - q1\noutliers = df[(df.amount < q1 - 1.5*iqr) | (df.amount > q3 + 1.5*iqr)]",

                "The IQR rule flags values outside the lower and upper fences for investigation; it does not prove they are errors.",

                "Do not delete flagged rows automatically. Check units, source records, and business context first.",

                "Compare the median and mean before and after reviewing the flagged order. Explain what changed and why.",

            )),

            (("mean", "median", "distribution", "growth rate", "growth"), lambda c: _guide(

                c, "a statistical summary that describes a typical value, spread, shape, or change over time.",

                "A manager compares typical order value across stores where a few very large orders may skew the average.",

                "median = df['order_value'].median()\nmean = df['order_value'].mean()\nprint({'median': median, 'mean': mean})",

                "A large gap between mean and median can signal skew or extreme values worth investigating.",

                "A single summary number can hide skew, small sample sizes, or different customer groups.",

                "Choose a summary that fits the data shape and explain what information it leaves out.",

            )),

        ],

        6: [

            (("groupby", "merge", "pivot_table", "dates", "apply"), lambda c: _guide(

                c, "a Pandas operation for combining, grouping, reshaping, or transforming tabular data.",

                "A subscription team combines customer records with monthly payments to compare revenue by cohort.",

                "monthly = payments.groupby('cohort', as_index=False)['revenue'].sum()",

                "The output has one row per cohort and a revenue total for each group.",

                "Check join keys and row counts after a merge; duplicate keys can multiply rows.",

                "Compare record counts before and after the operation and explain any change.",

            )),

        ],

        7: [

            (("join", "subquer", "cte", "common table expression"), lambda c: _guide(

                c, "a SQL technique for combining related tables or organizing a multi-step query.",

                "A customer success team needs customers and their latest subscription activity in one result.",

                "WITH latest AS (\n  SELECT customer_id, MAX(activity_date) AS last_seen\n  FROM activity GROUP BY customer_id\n)\nSELECT c.customer_id, latest.last_seen\nFROM customers c LEFT JOIN latest USING (customer_id);",

                "Every customer remains in the result; customers with no activity have a NULL last_seen.",

                "Check join cardinality and preserve unmatched customers when the question asks for all customers.",

                "Reconcile the output row count to the customer table and inspect customers with no activity.",

            )),

        ],

        8: [

            (("row_number", "rank", "lag", "lead", "running total", "window"), lambda c: _guide(

                c, "a SQL calculation across related rows that keeps each row in the result.",

                "A retention analyst needs to compare each month's churn with the previous month.",

                "LAG(churned_customers) OVER (PARTITION BY plan ORDER BY month)",

                "Each row keeps its month and receives the prior month's churn value for the same plan.",

                "Choose the correct PARTITION BY and ORDER BY; otherwise comparisons cross groups or time order.",

                "Check the first row in each partition and explain why its previous-month value is NULL.",

            )),

        ],

        9: [

            (("power bi", "power query", "relationship", "data model"), lambda c: _guide(

                c, "a Power BI modeling or preparation step that shapes clean tables and their relationships.",

                "A reporting team combines orders and products without duplicating product totals.",

                "Create a one-to-many relationship from Products[ProductID] to Orders[ProductID].",

                "Product attributes filter matching order rows while each product remains a single dimension record.",

                "Avoid many-to-many relationships unless the data model truly requires them; verify key uniqueness.",

                "Test one product filter and confirm only its orders and totals appear.",

            )),

        ],

        10: [

            (("calculate", "filter context", "time intelligence", "dax"), lambda c: _guide(

                c, "a DAX measure evaluated under the report's current filters and relationships.",

                "A sales manager selects one region and needs revenue for that selection, not the whole company.",

                "Regional Revenue = CALCULATE(SUM(Sales[Revenue]), Sales[Status] = \"Complete\")",

                "The measure totals completed sales while respecting the report's region filter.",

                "Know which filters CALCULATE adds or replaces; a measure can look right on a total and wrong by segment.",

                "Compare the card total with the sum of visible regions and explain any difference.",

            )),

        ],

        11: [

            (("time-series", "seasonality", "moving average", "a/b", "significance", "sample size"), lambda c: _guide(

                c, "a method for distinguishing a real pattern from ordinary variation in time-based or experiment data.",

                "A product team tests a new signup page and wants to avoid calling a small random lift a win.",

                "lift = (variant_rate - control_rate) / control_rate",

                "The relative lift describes the observed change; significance and sample size are still needed to judge confidence.",

                "Do not stop an experiment early just because one interim result looks favorable.",

                "Report the effect size, sample size, uncertainty, and decision rule together.",

            )),

        ],

        12: [

            (("churn", "retention", "conversion", "dashboard", "storytelling", "capstone"), lambda c: _guide(

                c, "a business metric and dashboard practice for turning validated data into a decision.",

                "Leadership wants to know whether customer retention improved after a service change.",

                "retention_rate = returning_customers / eligible_customers",

                "The rate is meaningful only when the eligible cohort and time window are clearly defined.",

                "Do not mix denominators or time windows when comparing metrics between periods.",

                "Define the metric, show its trend, and recommend one action supported by the evidence.",

            )),

        ],

    }





def _ai_rules():

    return {

        1: [(("ai", "ml", "problem", "numpy", "python"), lambda c: _guide(

            c, "a building block for framing a problem and representing data for a machine-learning task.",

            "A delivery company wants to estimate arrival time from route and traffic data.",

            "import numpy as np\ntravel_minutes = np.array([32, 45, 28])\nprint(travel_minutes.mean())",

            "The mean is 35 minutes; choosing a prediction task depends on having a numeric target such as arrival time.",

            "Do not choose a model before defining the target and what decision the prediction will support.",

            "State the input, target, and useful evaluation measure for a concrete prediction problem.",

        ))],

        2: [(("pandas", "data prep", "missing", "train/test", "split", "feature", "target"), lambda c: _guide(

            c, "a preparation step that creates clean features and a fair holdout set for evaluation.",

            "A churn team needs to test whether a model works on customers it did not train on.",

            "from sklearn.model_selection import train_test_split\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)",

            "Training data fits the model; the held-out test set estimates performance on unseen examples.",

            "Do not fit preprocessing on the full dataset before splitting; that leaks test information.",

            "Identify one feature that could leak the answer and remove it before evaluating.",

        ))],

        3: [(("linear regression", "mse", "mean squared error", "r-squared", "r²", "model fitting", "fit"), lambda c: _guide(

            c, "a model for predicting a continuous value by fitting a relationship between features and a target.",

            "A housing team predicts sale price from floor area and compares predictions with known sale prices.",

            "from sklearn.metrics import mean_squared_error, r2_score\nprint(mean_squared_error(y_test, y_pred), r2_score(y_test, y_pred))",

            "MSE measures squared prediction error; R² compares improvement with predicting the target mean.",

            "A high R² alone does not prove the model generalizes; inspect holdout errors and residual patterns.",

            "Compare the model with a mean-price baseline and explain whether it improves predictions.",

        ))],

        4: [(("logistic", "confusion", "precision", "recall", "classifier"), lambda c: _guide(

            c, "a classification method evaluated by how its predicted classes compare with actual outcomes.",

            "A churn team flags customers at risk, and wants to understand missed churners versus false alerts.",

            "from sklearn.metrics import confusion_matrix, precision_score, recall_score\nprint(confusion_matrix(y_test, y_pred))",

            "The confusion matrix counts true positives, false positives, true negatives, and false negatives.",

            "Accuracy can hide poor performance when one class is rare; choose metrics tied to the business cost.",

            "Explain whether missing a churner or contacting a retained customer is more costly, then choose a metric.",

        ))],

        5: [(("tree", "forest", "random", "comparison"), lambda c: _guide(

            c, "a tree-based model that splits records into groups; a random forest combines many trees.",

            "An insurer wants understandable rules for grouping claims by risk factors.",

            "from sklearn.ensemble import RandomForestClassifier\nmodel = RandomForestClassifier(n_estimators=100, random_state=42)",

            "The forest combines predictions from many trees, reducing dependence on one particular split.",

            "Deep trees can memorize training examples; compare training and validation performance.",

            "Compare a shallow tree with a forest and note the trade-off between readability and stability.",

        ))],

        6: [(("feature", "cross-validation", "pipeline"), lambda c: _guide(

            c, "a repeatable way to prepare inputs and test model choices without leaking information.",

            "A team compares models while scaling numeric columns and encoding categories.",

            "from sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\npipe = make_pipeline(StandardScaler(), LogisticRegression())",

            "The pipeline fits preprocessing within each training fold and applies it consistently to validation data.",

            "Preprocessing the full dataset before cross-validation leaks information into validation folds.",

            "Place one preprocessing step inside a pipeline and explain why the validation fold must stay unseen.",

        ))],

        7: [(("text", "tf-idf", "sentiment", "token"), lambda c: _guide(

            c, "a text-processing step that turns written feedback into features a classifier can use.",

            "A support team labels customer comments as positive or negative.",

            "from sklearn.feature_extraction.text import TfidfVectorizer\nX = TfidfVectorizer().fit_transform(comments)",

            "Common but uninformative terms receive less weight than terms that distinguish comments.",

            "Fit the vectorizer on training text only; fitting on all text leaks vocabulary information.",

            "Inspect the most informative terms and check whether they reflect sentiment rather than data leakage.",

        ))],

        8: [(("embedding", "cluster", "k-means", "semantic", "search"), lambda c: _guide(

            c, "a way to represent text by meaning and compare or group similar documents.",

            "A support team wants relevant help articles for a customer's question, even when wording differs.",

            "similarity = query_embedding @ document_embedding.T",

            "Higher similarity scores indicate closer vector direction; results still need relevance checks.",

            "Semantic similarity is not proof that a document answers the question; inspect retrieved passages.",

            "Compare results for two differently worded queries that express the same intent.",

        ))],

        9: [(("neural", "perceptron", "activation", "backpropagation"), lambda c: _guide(

            c, "a trainable network of weighted layers that learns representations by reducing a loss.",

            "An image classifier adjusts its weights after comparing a predicted label with the correct label.",

            "loss.backward()\noptimizer.step()\noptimizer.zero_grad()",

            "Backpropagation computes gradients; the optimizer uses them to update weights.",

            "Without nonlinear activations, stacked linear layers still behave like one linear transformation.",

            "Explain what changes after one training step and how the loss indicates whether it helped.",

        ))],

        10: [(("cnn", "convolution", "image", "pooling"), lambda c: _guide(

            c, "an image model that uses local filters to detect spatial patterns such as edges and textures.",

            "A quality-control team classifies product photos while preserving nearby-pixel relationships.",

            "features = conv_layer(image_batch)\npooled = pool_layer(features)",

            "Convolution creates feature maps; pooling can reduce their spatial size while retaining strong signals.",

            "Flattening images immediately can discard useful spatial structure and create too many parameters.",

            "Trace how one small filter responds to a simple edge in an image patch.",

        ))],

        11: [(("transformer", "llm", "token", "attention", "prompt", "fine-tun"), lambda c: _guide(

            c, "a language-model technique that processes token sequences and uses context to represent relationships.",

            "A support assistant must answer from a long product policy without inventing details.",

            "prompt = \"Use only the supplied policy. If the answer is absent, say so.\\n\\n\" + policy_text",

            "Clear context and constraints make the task more focused, but the answer still needs checking.",

            "A confident answer is not evidence; verify claims against the supplied source.",

            "Mark each sentence in a response that is supported by the source and flag any unsupported claim.",

        ))],

        12: [(("rag", "retrieval", "cited", "capstone", "document", "deployment", "evaluation"), lambda c: _guide(

            c, "a system that retrieves relevant source passages and uses them to support a generated answer.",

            "A company handbook assistant must answer employee questions with traceable citations.",

            "for chunk in retrieve(question, handbook_chunks):\n    print(chunk.source, chunk.text)",

            "A useful answer cites passages that directly support each claim and can abstain when evidence is missing.",

            "Do not treat retrieval as verification; irrelevant or incomplete passages can still produce incorrect answers.",

            "Test a question answerable from the handbook and one deliberately not covered by it.",

        ))],

    }





def _electronics_rules():

    """Curated topic-by-topic teaching notes for the standalone Electronics track."""

    facts = {

        "Voltage": ("electric potential difference between two points, measured in volts", "Measure across a 5 V source: red probe to +5 V and black probe to GND.", "A healthy source reads close to 5 V across its rails.", "Placing a voltmeter in series can interrupt the circuit or cause a short.", "Measure a low-voltage source and label the two points used."),

        "Current": ("the rate of charge flow through a complete path, measured in amperes", "Open the LED branch and insert the meter in series on its mA range.", "The meter reports the current flowing in that branch.", "An ammeter placed directly across a supply can short it.", "Draw where an ammeter must sit in one LED branch."),

        "Resistance and Ohm's law": ("opposition to current flow, related by V = I × R", "R = (5 - 2) / 0.01  # 300 ohms for a 2 V LED at 10 mA from 5 V", "The calculated series resistor is 300 ohms or the next suitable higher standard value.", "Using milliamps as amps in the equation produces a value 1,000 times too large.", "Calculate the resistor for a 5 V source, 2 V LED, and 10 mA target."),

        "LED circuits": ("a polarized diode circuit that needs a current-limiting resistor and a complete return path", "+5 V -> 330 ohm resistor -> LED anode; LED cathode -> GND", "The LED lights when forward biased in a complete circuit with a suitable resistor.", "Connecting an LED directly to a supply can exceed its current limit.", "Sketch the safe series path and mark the LED anode and cathode."),

        "Series circuits": ("a circuit path where the same current passes through each component in sequence", "R_total = R1 + R2\nI = supply_voltage / R_total", "Adding a component in series increases total resistance and lowers current for a fixed supply.", "A break at any series connection opens the whole path.", "Predict the current change after adding a second series resistor."),

        "Parallel circuits": ("a circuit with multiple branches connected across the same two nodes", "V_branch1 = V_branch2 = supply_voltage", "Each ideal branch sees the supply voltage, while source current is the sum of branch currents.", "Adding branches can exceed the source current limit.", "Draw two parallel LED branches and label their shared nodes."),

        "Open and closed paths": ("a closed conductive loop that allows current to flow from a source and back", "switch_closed = True  # complete path\nswitch_closed = False  # open path", "An open switch stops branch current; a closed switch completes the path.", "A diagram can look closed while a breadboard row or return wire is disconnected.", "Mark one likely open point in a simple lamp circuit and predict the result."),

        "Circuit polarity": ("the assigned positive and negative orientation of a source and polarized components", "Connect the LED anode toward the positive supply through a resistor; its cathode returns to ground.", "Correct polarity forward-biases the LED; reversed polarity usually leaves it off.", "Do not rely on wire color alone; verify the actual terminals and component marking.", "Label source polarity and the LED anode/cathode on a diagram."),

        "Resistor ratings": ("limits on resistance value, tolerance, and heat dissipation for a resistor", "P = I ** 2 * R  # estimate resistor dissipation", "A selected resistor must meet both the required resistance and power rating.", "A correct ohm value can still overheat if its power rating is too low.", "Compare calculated resistor power with the rating on a supplied datasheet."),

        "Capacitors": ("components that store charge in an electric field and oppose rapid voltage changes", "tau_seconds = resistance_ohms * capacitance_farads", "An RC circuit reaches about 63 percent of its final step voltage after one time constant.", "Electrolytic capacitors are polarized and must not exceed their voltage rating.", "Estimate the time constant for a 10 kOhm resistor and 100 microfarad capacitor."),

        "Diodes": ("semiconductor components that conduct readily in one direction when forward biased", "forward_biased = (anode_voltage > cathode_voltage)", "A forward-biased diode conducts after its forward-voltage drop; reverse bias blocks ordinary current.", "A diode's current and reverse-voltage limits still matter in low-voltage circuits.", "Identify anode and cathode, then predict the result for each polarity."),

        "Transistors as switches": ("semiconductor devices that use a small control signal to switch a larger load current", "if base_or_gate_is_driven: load_path = 'on'", "A correctly driven transistor switches the load while keeping load current out of the logic pin.", "A base resistor or suitable gate drive may be required; check the part's limits.", "Label control, load, and ground connections for a low-side switch."),

        "Breadboard rows and rails": ("internal conductive strips that connect specific hole groups for solderless prototypes", "Use a continuity check to map one five-hole row and each power-rail segment.", "Holes in one terminal row share a node; the center gap separates the two sides.", "Power rails may be split and not connected end to end.", "Mark two connected holes and one unconnected rail segment on a layout."),

        "Schematic symbols": ("standard marks that describe components and electrical connections in a circuit diagram", "VCC -- resistor -- LED -- GND", "A schematic communicates electrical connectivity regardless of the physical placement of parts.", "Crossing wires are not always connected unless a junction is shown.", "Redraw a simple LED circuit using labeled supply, resistor, diode, and ground symbols."),

        "Continuity checks": ("a low-resistance test used to find whether two unpowered points are electrically connected", "power_off(); meter.set_mode('continuity'); check(point_a, point_b)", "A beep or low reading indicates a conductive path between the probe points.", "Never use continuity mode on an energized circuit.", "Check whether two breadboard holes belong to the same internal node."),

        "Safe power limits": ("voltage, current, and energy boundaries that keep components and people safe", "supply_limit = min(component_voltage_limits)", "The circuit stays within the lowest relevant component and supply limit.", "A low voltage does not make a short circuit or overheated component harmless.", "List the supply and component limits before powering a practice circuit."),

        "Multimeter controls": ("the selector, input jacks, and range that configure a meter for a measurement", "black_lead = 'COM'; red_lead = 'V/ohm'; mode = 'DC volts'", "The meter is ready for voltage only when its lead sockets and dial match that measurement.", "Leaving the red lead in the current jack can create a short during a voltage check.", "Choose the correct jack, mode, and range for measuring a battery."),

        "DC voltage measurement": ("a parallel measurement of the potential difference in a direct-current circuit", "meter.connect_across(source_positive, source_ground)", "A correctly connected meter displays the source voltage and probe polarity.", "Never place a voltage meter in series as the normal measurement method.", "Record a source voltage and state where each probe touched."),

        "Current measurement": ("a series measurement of charge flow through a circuit branch", "open_branch(); meter.insert_in_series(); select_mA_range()", "The reading is the current through the opened branch after the meter completes its path.", "Starting on an unsuitable low range or wrong jack can damage a meter fuse.", "Describe how to safely measure current in an LED branch."),

        "Resistance measurement": ("a measurement of opposition to current on an unpowered, isolated component or path", "power_off(); isolate_component(); resistance = meter.measure_ohms()", "The meter reports an ohm value without external circuit power affecting the test.", "Parallel paths can make an in-circuit resistance reading misleading.", "Explain why a resistor may need one lead lifted before measuring it."),

        "Logic levels": ("voltage ranges interpreted by a digital input as logic low or logic high", "logic_high_threshold = board_datasheet['VIH_min']", "A valid high input meets the receiving device's minimum VIH requirement.", "A 5 V output can damage a 3.3 V-only input.", "Compare the output-high voltage with the input's published VIH range."),

        "Pull-up and pull-down inputs": ("resistors that hold a digital input at a defined state when no active driver is connected", "button_pressed = (digital_read(pin) == LOW)  # pull-up wiring", "An open button has a stable default state instead of a floating reading.", "A floating input can change state from electrical noise.", "Draw a pull-up button input and label the idle and pressed voltages."),

        "Switch debouncing": ("filtering rapid electrical transitions caused by a mechanical contact bouncing", "if now_ms - last_change_ms > debounce_ms: accept_state()", "One physical press is treated as one clean state change.", "A long delay can make the controls feel unresponsive.", "Choose a short debounce interval and compare raw and filtered transitions."),

        "PWM signals": ("digital pulses whose duty cycle controls average delivered power over time", "duty_percent = on_time / period * 100", "A higher duty cycle raises LED brightness while the digital output still switches on and off.", "PWM is not the same as a steady analog voltage.", "Calculate the duty cycle for a signal on for 3 ms in a 10 ms period."),

        "Microcontroller pins": ("physical or logical terminals that connect a controller to external signals", "pin_mode(5, INPUT); pin_mode(9, OUTPUT)", "Each pin is configured for its intended direction and supported function.", "A pin's current and voltage ratings are limited; it cannot power every load.", "Label the input and output pins on a small board diagram."),

        "GPIO output": ("a general-purpose digital pin configured to drive a logic-level output", "digital_write(9, HIGH)", "The pin reaches its documented high logic level when set HIGH.", "Do not connect a motor or high-current load directly to GPIO.", "Write a short output-state sequence for an LED with a series resistor."),

        "Digital button input": ("a controller input that reads one of two defined logic states from a switch", "pressed = digital_read(button_pin) == LOW", "The read value changes predictably between idle and pressed states.", "Unbiased or poorly wired inputs can float and produce random values.", "Record the expected reading for an open and a pressed button."),

        "ADC conversion": ("conversion of an analog input voltage into a finite digital count", "volts = adc_count * reference_volts / (2**resolution_bits - 1)", "The count scales with the input between ground and the ADC reference voltage.", "A reference mismatch or voltage above the input limit makes the conversion unreliable or unsafe.", "Convert one ADC count to volts using a stated resolution and reference."),

        "Voltage dividers": ("two series resistors that create a lower voltage from a known input", "v_out = v_in * r_bottom / (r_top + r_bottom)", "The output follows the resistor ratio when the load does not significantly affect it.", "A low-resistance load can change the expected divider voltage.", "Calculate Vout for equal resistors on a 5 V input."),

        "Analog sensors": ("devices that produce a continuously varying electrical signal related to a physical quantity", "raw = adc_read(sensor_pin)", "Repeated readings change consistently when the measured condition changes.", "An analog reading needs units and calibration before it represents a real-world value.", "Compare sensor output at two known conditions and record the raw counts."),

        "Signal filtering": ("processing that reduces unwanted variation while retaining useful changes in a signal", "filtered[n] = alpha * sample[n] + (1-alpha) * filtered[n-1]", "A simple low-pass filter smooths rapid noise but responds more slowly to changes.", "Over-filtering can hide a real fast event.", "Compare raw and smoothed readings from the same short sample."),

        "Sensor calibration": ("mapping sensor output to known reference values so readings have useful units", "scale = (known_high - known_low) / (raw_high - raw_low)", "A calibrated mapping estimates the measured value between its reference points.", "Calibration outside the measured range is extrapolation and may be inaccurate.", "Use two known points to map a raw reading into the target units."),

        "Transistor drivers": ("switch circuits that let a small controller signal control a larger load current", "gpio -> base_resistor -> transistor -> low_voltage_load", "The transistor carries the load current while the GPIO supplies only the control signal.", "A missing common reference or undersized transistor can prevent safe switching.", "Choose a driver after comparing its current rating with the load requirement."),

        "Relay switching": ("electrically controlled contacts that switch a separate circuit using a coil", "controller -> driver -> relay_coil; contacts -> isolated_demo_load", "The control side operates the coil while the contacts switch the intended load path.", "A relay coil needs a driver and suppression; never assume a GPIO can drive it directly.", "Mark coil, driver, contact, and supply sides on a low-voltage diagram."),

        "Flyback diodes": ("diodes placed across inductive loads to limit the voltage spike when current is switched off", "diode.cathode = supply_positive; diode.anode = switched_low_side", "The diode conducts the coil's decaying current and protects the switching device.", "Reversed diode polarity can short the supply when the driver turns on.", "Draw the correct diode polarity across a relay coil."),

        "Separate load power": ("power arrangement that supplies high-current loads without routing their current through logic pins", "controller_ground --- load_supply_ground  # shared reference when required", "The load has a suitable supply path and the control signal has a valid reference.", "A shared ground does not mean the controller pin should carry the load current.", "Trace the load-current path separately from the GPIO control path."),

        "Op-amp basics": ("an amplifier that compares its inputs and uses feedback to control its output", "v_out = gain * (v_plus - v_minus)  # within supply rails", "Negative feedback can set a stable closed-loop gain within the amplifier's limits.", "An op-amp output cannot exceed its supply rails and real parts have input limits.", "Identify the two inputs, output, and feedback path in a simple circuit."),

        "Amplifier gain": ("the ratio of output signal size to input signal size", "gain = v_out / v_in", "A gain of 10 turns a 0.1 V signal into about 1 V before clipping or loading effects.", "Excessive gain clips the output at its supply limit.", "Calculate the output for a stated input and gain, then check the rail limit."),

        "RC filters": ("resistor-capacitor networks whose frequency response depends on their time constant", "cutoff_hz = 1 / (2 * pi * resistance_ohms * capacitance_farads)", "A first-order low-pass RC filter attenuates frequencies above its cutoff.", "Component tolerances and load impedance shift the practical cutoff.", "Estimate the cutoff for a supplied resistor and capacitor pair."),

        "Noise and grounding": ("unwanted electrical variation and the reference paths used to measure signals", "measure_noise = max(samples) - min(samples)", "A consistent reference and short signal return path can reduce measured noise.", "Randomly connecting additional grounds can create loops or new interference paths.", "Compare a short and long sensor lead and report the observed noise range."),

        "UART communication": ("an asynchronous serial link that sends framed data over transmit and receive lines", "connect(board_a.tx, board_b.rx); connect(board_a.rx, board_b.tx)", "Both devices exchange data when baud rate, framing, voltage, and ground reference agree.", "Connecting TX to TX or ignoring logic-level differences prevents reliable communication.", "Draw the crossed TX/RX wiring and list the matching serial settings."),

        "I2C bus": ("a two-wire addressed bus using SDA for data and SCL for clock", "i2c_scan()  # report acknowledged device addresses", "Devices share SDA/SCL and respond to their assigned address.", "Missing pull-ups or duplicate addresses can stop communication.", "Label SDA, SCL, pull-ups, and one device address on a bus sketch."),

        "SPI bus": ("a synchronous serial interface using clock, controller-out, controller-in, and chip-select signals", "transfer(data, chip_select='sensor_0')", "Only the selected peripheral responds while clocked data is transferred.", "Sharing data/clock lines without separate chip select can select multiple devices.", "Draw the common SPI signals and one peripheral's chip-select line."),

        "Logic-level compatibility": ("matching signal voltage ranges between the output of one device and input of another", "safe = (tx_voltage <= receiver_abs_max)", "A compatible interface stays within the receiver's guaranteed and absolute maximum limits.", "A signal that works once can still overstress an input beyond its rating.", "Compare two device datasheets and decide whether level shifting is needed."),

        "Power budgeting": ("adding expected current demands and checking supply, regulator, and thermal capacity", "total_current = sum(load_currents)\npower_watts = voltage * total_current", "The chosen supply supports peak load demand with an appropriate margin.", "Using average current alone can miss startup or actuator peaks.", "Sum the stated loads and compare their peak with the supply rating."),

        "Schematic review": ("checking a circuit drawing for correct connectivity, values, polarity, and ratings before assembly", "review = ['nets', 'values', 'polarities', 'ratings', 'power']", "Each component and connection has a clear, verified role before the prototype is powered.", "A neat drawing can still contain an electrically incorrect node or missing return.", "Review a provided schematic and identify one connection to verify."),

        "Prototype test plans": ("repeatable checks with inputs, expected results, and recorded outcomes for a prototype", "test = {'input': 'known 1.0 V', 'expected': 'ADC count in range'}", "A test passes only when the observed result meets the stated expected range.", "A single successful demo does not cover boundary or failure conditions.", "Write one normal test and one boundary test for a sensor input."),

        "Fault isolation": ("a stepwise method for narrowing a fault to a power, connection, component, or signal path", "check_power(); check_ground(); trace_signal(); test_component()", "Changing one check at a time identifies the likely failing section without random rewiring.", "Replacing parts before measuring can hide the original cause and introduce new faults.", "Trace a simulated no-output fault from supply through the signal path."),

    }

    level_scenarios = {

        1: "A learner is building a protected LED indicator from a 5 V bench supply.",

        2: "A technician is comparing how a small lamp circuit behaves when one branch opens.",

        3: "A product lab is checking component choices against a supplied low-voltage design.",

        4: "A student is translating a schematic into a safe, verifiable breadboard prototype.",

        5: "A repair bench needs repeatable measurements before replacing a component.",

        6: "A controller input and indicator need predictable digital timing and states.",

        7: "A microcontroller board must read a switch and drive a low-current output.",

        8: "A monitoring prototype must turn a sensor signal into stable, calibrated readings.",

        9: "A small actuator must be switched without overloading its controller pin.",

        10: "A sensor signal needs conditioning before it reaches a controller input.",

        11: "A board and sensor need a reliable, voltage-compatible data connection.",

        12: "A product team is validating a low-voltage electronics prototype before a demo.",

    }

    rules = {}

    base_positions = (1, 3, 0, 2, 1)

    for level, concepts in enumerate(LEVEL_CONCEPTS["electronics"], 1):

        rules[level] = []

        for concept_index, concept in enumerate(concepts):

            data = facts[concept]

            answer_positions = tuple(

                (position + concept_index) % 4 for position in base_positions

            )

            rules[level].append((

                (concept.casefold(),),

                lambda matched, details=data, scenario=level_scenarios[level], positions=answer_positions: _guide(

                    matched, details[0], scenario, details[1], details[2], details[3], details[4],

                    quiz_answer_positions=positions,

                ),

            ))

    return rules





def _robotics_rules():

    return {

        1: [

            (("voltage",), lambda c: _guide(c, "electric potential difference: the push available to move charge between two points.", "A learner checks a 5 V supply before powering a low-voltage LED circuit.", "Set a multimeter to DC volts and place probes across the supply rails.", "A healthy 5 V source reads close to 5 V with the red probe on positive and black probe on ground.", "Do not measure voltage with probes placed in series; that can short the supply.", "Measure a battery and label its positive and ground rails.", quiz_factory=_electronics_quiz)),

            (("current",), lambda c: _guide(c, "the rate of electric charge flow through a complete circuit, measured in amperes.", "A learner checks whether an LED branch is below its safe current limit.", "Break the LED branch and place the multimeter in series on the milliamp range.", "The meter reports one current value for that series path.", "Never connect an ammeter directly across a voltage source.", "Sketch the one series path where you would place an ammeter.", quiz_factory=_electronics_quiz)),

            (("resistance", "ohm"), lambda c: _guide(c, "opposition to current flow, measured in ohms; a resistor limits current in an LED circuit.", "A learner chooses a resistor to protect an LED on a 5 V breadboard supply.", "resistor_ohms = (5 - 2) / 0.01  # 300 ohms minimum", "A resistor near or above 300 ohms keeps a 2 V LED near 10 mA from a 5 V supply.", "Do not assume resistor colour bands or LED forward voltage without checking the component data.", "Calculate the resistor for a 5 V supply, 2 V LED, and 10 mA target.", quiz_factory=_electronics_quiz)),

            (("circuit", "led"), lambda c: _guide(c, "a closed path from supply positive through a current-limiting resistor and LED back to ground.", "A learner builds a visible LED indicator without damaging the LED.", "5V -> 330 ohm resistor -> LED anode; LED cathode -> GND", "The LED lights only when its polarity is correct and the circuit has a complete return path.", "Do not omit the resistor or reverse the LED polarity.", "Draw the LED, resistor, positive rail, and ground in their correct order.", quiz_factory=_electronics_quiz)),

            (("breadboard",), lambda c: _guide(c, "a solderless prototyping board whose connected rows and power rails let components form temporary circuits.", "A learner moves an LED leg and resistor to separate breadboard rows to create a valid series path.", "Use continuity mode to confirm which five-hole rows and rail segments are connected before wiring.", "Components in the same connected row share one electrical node; separate rows are needed across a component.", "Do not assume a split power rail is connected across its center gap.", "Mark two connected rows and one split rail segment on your breadboard diagram.", quiz_factory=_electronics_quiz)),

            (("multimeter", "meter use",), lambda c: _guide(c, "a handheld instrument that measures voltage in parallel, current in series, and resistance on an unpowered component.", "A learner checks a battery and resistor with the correct meter mode and probe sockets.", "Select DC volts, check the probe jacks, then measure across the battery terminals.", "A correctly ranged meter shows supply voltage without opening the circuit.", "Move the red lead from the current jack before measuring voltage; verify the selected mode and safe range.", "Name the mode, probe placement, and jack for a voltage measurement and a current measurement.", quiz_factory=_electronics_quiz)),

        ],

        2: [(("arduino", "raspberry", "gpio", "digital", "microcontroller"), lambda c: _guide(

            c, "a microcontroller input/output pin used to read a digital signal or control a device.",

            "A button should switch an LED on when pressed and off when released.",

            "pinMode(buttonPin, INPUT_PULLUP);\npinMode(ledPin, OUTPUT);\ndigitalWrite(ledPin, digitalRead(buttonPin) == LOW);",

            "With INPUT_PULLUP, a pressed button reads LOW; the LED follows the button state.",

            "Account for active-low wiring and never connect a motor directly to a GPIO pin.",

            "Read the button state and verify both pressed and released behavior before connecting the LED.",

        ))],

        3: [(("pwm", "analog", "potentiometer", "ldr", "sensor"), lambda c: _guide(

            c, "a sensor or signal-reading method that measures changing input and can control output intensity.",

            "A small robot should slow a motor when a light sensor detects a dark area.",

            "reading = analogRead(sensorPin);\nbrightness = map(reading, 0, 1023, 0, 255);\nanalogWrite(ledPin, brightness);",

            "The analog reading is scaled to the PWM output range before it controls brightness.",

            "Check the board's actual input/output ranges; PWM output is not the same as a true analog voltage.",

            "Record sensor readings in bright and dim conditions, then choose a threshold from measured values.",

        ))],

        4: [(("motor", "driver", "speed"), lambda c: _guide(

            c, "a motor-control method that uses a driver to switch direction and regulate supplied power.",

            "A mobile robot needs to vary wheel speed without drawing motor current through its controller pin.",

            "driver.setSpeed(160);\ndriver.forward();",

            "The driver supplies motor current while the controller sends a low-current control signal.",

            "Never power a DC motor directly from a microcontroller pin; use a suitable driver and supply.",

            "Test forward, stop, and reverse at low speed with the robot safely lifted.",

        ))],

        5: [(("ultrasonic", "infrared", "ir sensor", "distance", "proximity", "sensor"), lambda c: _guide(

            c, "a distance or proximity sensor used to detect nearby obstacles.",

            "A robot should stop before reaching a wall.",

            "if distance_cm < 20:\n    stop_motors()",

            "The robot stops when the measured distance crosses the chosen safety threshold.",

            "Sensor readings can be noisy or unreliable on angled, soft, or reflective surfaces.",

            "Take repeated readings at known distances and choose a threshold with a safety margin.",

        ))],

        6: [(("servo", "stepper", "actuator"), lambda c: _guide(

            c, "an actuator that moves to a commanded angle or advances in controlled steps.",

            "A small robot arm needs to point a sensor at repeatable positions.",

            "servo.write(90);  // move to the middle position",

            "The servo moves toward its commanded angle within its mechanical range.",

            "Do not command beyond mechanical limits or assume every actuator has the same range.",

            "Move through a few safe positions and note the relationship between command and motion.",

        ))],

        7: [(("obstacle", "state-based", "avoidance", "recovery"), lambda c: _guide(

            c, "a state-based control rule that selects a safe action based on sensor readings.",

            "A robot detects an obstacle ahead and must stop, turn, and then check whether the path is clear.",

            "if front_blocked:\n    state = 'turning'\nelif state == 'turning' and path_clear:\n    state = 'moving'",

            "The robot changes behavior based on its current state and verified sensor conditions.",

            "Avoid scattered one-off conditions that can make the robot switch rapidly between actions.",

            "Draw the states and transitions for clear path, obstacle found, turning, and recovery.",

        ))],

        8: [(("imu", "accelerometer", "gyroscope", "calibration", "tilt"), lambda c: _guide(

            c, "an inertial measurement component used to estimate motion or orientation from calibrated readings.",

            "A balancing robot measures tilt before correcting its motor output.",

            "tilt_change = current_angle - calibrated_level",

            "Subtracting the calibrated level reduces the sensor's resting offset.",

            "Raw accelerometer readings alone can be noisy during movement; calibrate and filter thoughtfully.",

            "Record stationary readings first, then compare them with readings at known tilt angles.",

        ))],

        9: [(("pid", "proportional", "integral", "derivative", "tuning"), lambda c: _guide(

            c, "a feedback controller that combines present error, accumulated error, and error change.",

            "A robot wheel should hold a target speed despite changes in floor resistance.",

            "error = target - measured\noutput = kp*error + ki*error_sum + kd*(error - previous_error)",

            "The controller adjusts output using the current error and its recent history.",

            "Changing all gains at once makes it hard to identify why behavior became unstable.",

            "Tune one term at a time on a safe setup and record overshoot and settling time.",

        ))],

        10: [(("ros", "node", "topic", "service", "message"), lambda c: _guide(

            c, "a ROS communication building block that connects robot software components.",

            "A sensor node publishes readings that a navigation node subscribes to.",

            "ros2 topic list",

            "The command lists active topics so you can confirm the expected communication channel exists.",

            "Check topic names, message types, and publisher/subscriber availability before debugging control logic.",

            "Trace one sensor message from its publisher to the node that consumes it.",

        ))],

        11: [(("slam", "navigation", "a*", "path", "localization", "map", "obstacle"), lambda c: _guide(

            c, "a mapping or path-planning method that helps a robot estimate position and choose a route.",

            "A mobile robot needs a collision-free route from its current map cell to a target.",

            "priority = distance_so_far + estimated_distance_to_goal",

            "A* prioritizes paths using the cost so far plus an estimate of remaining distance.",

            "A poor heuristic or stale map can produce inefficient or unsafe routes.",

            "Compare a planned path with obstacles on the supplied map and identify where it needs replanning.",

        ))],

        12: [(("integration", "capstone", "testing", "end-to-end", "avoidance"), lambda c: _guide(

            c, "the process of combining robot sensors, control, and actuation into a tested whole.",

            "An obstacle-avoiding robot must detect a barrier, choose a route, move, and recover safely.",

            "assert obstacle_detected\nassert motor_command == 'stop'\nassert next_state == 'turning'",

            "A useful integration test checks the sensor input, state transition, and resulting motor command.",

            "A successful unit test for one component does not prove the whole robot behaves safely.",

            "Test a clear path, an obstacle, and a sensor failure; record the expected safe response.",

        ))],

    }





def _cyber_rules():

    return {

        1: [(("ip", "tcp", "udp", "dns", "port"), lambda c: _guide(

            c, "a networking concept used to identify hosts, resolve names, or deliver traffic to services.",

            "An administrator checks why a local training service cannot be reached by its expected name.",

            "hostname = 'training.local'\naddress = resolve_from_local_hosts_file(hostname)",

            "Name resolution maps the training hostname to its configured local address.",

            "A port number identifies a service endpoint; it does not prove the service is safe or reachable.",

            "Trace a provided local hostname to its address and identify which transport the sample service uses.",

        ))],

        2: [(("linux", "permission", "process", "command line", "local administration"), lambda c: _guide(

            c, "a Linux administration skill for inspecting files, permissions, or running processes safely.",

            "A defender checks which local account owns a supplied log file and who can read it.",

            "ls -l /var/log/training/auth.log",

            "The listing shows the file owner, group, and permission bits for review.",

            "Do not change permissions broadly; grant only the access required for the task.",

            "Read the permission string and state which users can read the sample file.",

        ))],

        3: [(("cia", "confidentiality", "integrity", "availability", "threat", "hash", "encrypt", "security fundamental"), lambda c: _guide(

            c, "a security principle for protecting information and reasoning about risks and safeguards.",

            "A team stores password verifiers and needs to protect them if the database is exposed.",

            "stored = password_hash(password, unique_salt)",

            "A password verifier should use a purpose-built slow password hash, not reversible encryption.",

            "Hashing and encryption solve different problems; a hash is not a way to recover the original password.",

            "For a sample data asset, name one confidentiality, integrity, and availability risk.",

        ))],

        4: [(("http", "cookie", "session", "web basics", "secure web configuration"), lambda c: _guide(

            c, "a web communication or state mechanism that should be configured to protect user sessions.",

            "A site keeps a user signed in after login using a browser cookie.",

            "Set-Cookie: sessionid=...; Secure; HttpOnly; SameSite=Lax",

            "The flags limit script access, require HTTPS, and reduce cross-site cookie sending.",

            "A session identifier is a credential; do not expose it in URLs or logs.",

            "Inspect a provided local response and identify the session cookie protections present.",

        ))],

        5: [(("injection", "broken authentication", "owasp", "vulnerable test", "defensive remediation"), lambda c: _guide(

            c, "a web risk to identify and remediate in a deliberately vulnerable local training app.",

            "A local demo login builds a query from a user-provided string.",

            "cursor.execute('SELECT id FROM users WHERE name = %s', [username])",

            "A parameterized query treats the supplied value as data rather than SQL syntax.",

            "Do not test real third-party systems; use only deliberately vulnerable apps in an authorized local lab.",

            "Review the lab code for string-built queries and replace them with parameterized handling.",

        ))],

        6: [(("xss", "cross-site scripting", "csrf", "misconfiguration", "secure configuration"), lambda c: _guide(

            c, "a web defense that prevents untrusted content or requests from changing user state unsafely.",

            "A local demo displays a comment supplied by a user.",

            "element.textContent = comment",

            "textContent displays the comment as text instead of interpreting it as executable markup.",

            "Escaping output for one context does not automatically protect every HTML, URL, or script context.",

            "Use the supplied local test case to confirm user input is shown as text and state-changing forms use CSRF protection.",

        ))],

        7: [(("log", "failed-login", "brute-force", "incident report"), lambda c: _guide(

            c, "a defensive log-review technique for identifying unusual authentication activity.",

            "A local training log shows repeated failed logins for one account over a short period.",

            "failed = events[events['result'] == 'failed']\ncounts = failed.groupby('account').size()",

            "The grouped count highlights accounts with repeated failures for investigation.",

            "A high failure count is a signal to investigate, not proof of a successful compromise.",

            "Build a short timeline from the provided local events and note what evidence is still missing.",

        ))],

        8: [(("python", "parsing", "port check", "port-check", "structured", "defensive output", "local-only"), lambda c: _guide(

            c, "a Python technique for parsing supplied local data and reporting a defensive finding.",

            "An analyst needs to summarize repeated events from a provided authentication log.",

            "from collections import Counter\ncounts = Counter(event['account'] for event in events if event['result'] == 'failed')",

            "The counter reports failed-event totals by account for triage.",

            "Validate log fields and timestamps; malformed or missing values can skew the summary.",

            "Run the parser only against the supplied local log and compare one total manually.",

        ))],

        9: [(("wireshark", "packet", "network scanning", "protocol filtering", "authorized local scanning"), lambda c: _guide(

            c, "a packet-analysis step for understanding traffic in an authorized capture or lab.",

            "A defender reviews a provided packet capture to find DNS requests from the lab client.",

            "dns",

            "The display filter narrows the capture to DNS packets for inspection.",

            "A capture shows only observed traffic; absence from a capture does not prove an event never occurred.",

            "Filter the provided capture and record source, destination, protocol, and timestamp.",

        ))],

        10: [(("threat model", "siem", "trust boundary", "asset", "defensive alert"), lambda c: _guide(

            c, "a planning method for identifying assets, trust boundaries, and useful defensive alerts.",

            "A team maps how a local application handles sign-in and stores account records.",

            "asset -> trust_boundary -> threat -> mitigation -> detection",

            "The map connects important assets with realistic risks and controls.",

            "A threat model is only useful when assumptions and system boundaries are explicit.",

            "Draw one trust boundary and pair a realistic threat with a mitigation and alert.",

        ))],

        11: [(("incident", "threat hunting", "threat-hunting", "evidence", "triage", "containment", "recovery", "log"), lambda c: _guide(

            c, "a defensive response step for reviewing evidence, containing risk, and restoring normal service.",

            "A responder receives supplied synthetic logs showing suspicious local account activity.",

            "record = {'time': event_time, 'source': 'provided-log', 'observation': finding}",

            "A timestamped evidence record helps build a reproducible incident timeline.",

            "Preserve evidence and follow the approved playbook; do not investigate by accessing unrelated systems.",

            "Separate confirmed facts from hypotheses in a short incident timeline.",

        ))],

        12: [(("penetration", "assessment", "report", "authorized lab", "findings", "risk rating"), lambda c: _guide(

            c, "a scoped security assessment step carried out only in an explicitly authorized lab.",

            "A training team reviews a deliberately vulnerable local app and needs a useful remediation report.",

            "finding = {'asset': 'local-lab-app', 'risk': 'high', 'evidence': 'provided test case'}",

            "A good report links scoped evidence to impact and a practical remediation.",

            "Never test real or third-party systems without explicit authorization; keep the exercise inside the lab.",

            "Write one finding with scope, evidence, impact, remediation, and a safe retest plan.",

        ))],

    }





def _web_rules():

    return {

        1: [(("dns", "http", "https", "client-server", "browser", "web"), lambda c: _guide(

            c, "a part of the browser-to-server request path that helps a page load.",

            "A learner opens a local site and checks how its name resolves and what the server returns.",

            "Browser -> DNS lookup -> HTTPS request -> server response -> rendered page",

            "The browser resolves the name, requests a resource, receives a response, and renders it.",

            "HTTPS protects transport; it does not guarantee the site content itself is trustworthy.",

            "Use browser developer tools on a local page to identify one request and its status code.",

        ))],

        2: [(("html", "semantic", "form", "input", "accessibility"), lambda c: _guide(

            c, "an HTML structure or control that gives page content clear meaning and usable interaction.",

            "A customer signs up using a form that should work with a keyboard and assistive technology.",

            '<label for="email">Email</label>\n<input id="email" name="email" type="email" required>',

            "The label names the input, type=email provides appropriate input behavior, and required marks it mandatory.",

            "A placeholder is not a replacement for a persistent label.",

            "Navigate the form with a keyboard and confirm every field has a clear accessible name.",

        ))],

        3: [(("css", "selector", "box model", "flexbox", "grid", "media quer"), lambda c: _guide(

            c, "a CSS rule or layout technique for styling and arranging elements across screen sizes.",

            "A product grid should display three cards on desktop and one column on a narrow phone.",

            ".cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }\n@media (max-width: 600px) { .cards { grid-template-columns: 1fr; } }",

            "The grid uses three equal columns by default and switches to one column below 600px.",

            "Fixed widths can cause overflow; test the layout at narrow and wide viewports.",

            "Resize the page and check whether content stays readable without horizontal scrolling.",

        ))],

        4: [(("javascript", "variable", "function", "array", "object", "dom"), lambda c: _guide(

            c, "a JavaScript building block for storing values, organizing data, or changing page content.",

            "A landing page needs to show a different greeting when a visitor clicks a button.",

            "const button = document.querySelector('#welcome');\nbutton.addEventListener('click', () => {\n  document.querySelector('#message').textContent = 'Welcome!';\n});",

            "Clicking the button updates the message element's text.",

            "Check that the selected element exists before attaching events on pages where it may be absent.",

            "Add a second button and update a different message without duplicating unrelated logic.",

        ))],

        5: [(("scope", "closure", "event", "error handling"), lambda c: _guide(

            c, "a JavaScript rule for where values are available and how browser actions or failures are handled.",

            "A support widget needs a private message count that increments when its button is clicked.",

            "function makeCounter() {\n  let count = 0;\n  return () => ++count;\n}",

            "The returned function retains access to count through a closure.",

            "Do not assume block-scoped variables are available outside their block; handle expected failures explicitly.",

            "Create two counters and verify that each one keeps its own independent value.",

        ))],

        6: [(("promise", "async", "await", "fetch", "event loop"), lambda c: _guide(

            c, "a JavaScript pattern for waiting on network or timer work without blocking the page.",

            "A product page loads inventory and should show a useful message if the request fails.",

            "const response = await fetch('/api/inventory');\nif (!response.ok) throw new Error('Request failed');\nconst items = await response.json();",

            "The code checks the HTTP response before parsing its JSON body.",

            "fetch does not reject on HTTP 404/500 by itself; check response.ok.",

            "Test success, an HTTP error, and a network failure, then confirm each has a clear UI state.",

        ))],

        7: [(("git", "commit", "branch", "pull request", "npm"), lambda c: _guide(

            c, "a collaboration or package-management practice that makes project changes easier to review and repeat.",

            "A teammate adds a feature without changing the shared main branch until it is reviewed.",

            "git switch -c feature/customer-banner\nnpm test\ngit add . && git commit -m \"Add customer banner\"",

            "The feature branch isolates work, tests provide a check, and the commit records a focused change.",

            "Avoid committing unrelated changes or secrets; keep each commit easy to understand.",

            "Describe a small change in a pull request with its purpose and the checks you ran.",

        ))],

        8: [(("django", "routing", "view", "template", "rest", "json", "backend"), lambda c: _guide(

            c, "a backend component that routes a request, handles data, and returns a page or JSON response.",

            "An operations team needs to create and list service requests through a small Django app.",

            "def request_list(request):\n    items = ServiceRequest.objects.all()\n    return JsonResponse({'items': list(items.values('id', 'title'))})",

            "The view queries records and returns a JSON object for the client.",

            "Validate user input and use the appropriate response type for the route.",

            "Trace one request from URL pattern through its view to the response body.",

        ))],

        9: [(("database", "relational", "join", "index", "migration", "orm"), lambda c: _guide(

            c, "a database design or query technique for storing related records and retrieving them reliably.",

            "An operations app needs to list service requests together with the staff member assigned to each one.",

            "ServiceRequest.objects.select_related('assignee').all()",

            "select_related fetches the related assignee in the same SQL query for a foreign-key relationship.",

            "An index can speed reads but adds storage and write cost; measure before adding one.",

            "Compare query results and query counts before and after loading related records efficiently.",

        ))],

        10: [(("auth", "session", "jwt", "password", "csrf", "xss", "security"), lambda c: _guide(

            c, "an application security practice that protects identity, requests, or rendered user content.",

            "A staff portal must keep sign-in state private and safely display a submitted comment.",

            "from django.contrib.auth.hashers import make_password\nstored = make_password(password)",

            "A password hash is stored instead of the original password; the framework verifies it later.",

            "Never store plain-text passwords or render untrusted input as executable HTML.",

            "Check a local demo for password hashing, CSRF protection, and escaped output.",

        ))],

        11: [(("react", "component", "state", "api integration"), lambda c: _guide(

            c, "a React UI building block or state pattern for keeping the screen in sync with data.",

            "A service-request console should refresh its list after a request is marked complete.",

            "const [requests, setRequests] = useState([]);\nsetRequests(current => current.filter(item => item.id !== completedId));",

            "The state setter creates a new list without the completed request, prompting React to re-render.",

            "Do not mutate state arrays in place; React may not detect the change reliably.",

            "Update one record and confirm unrelated list items remain unchanged.",

        ))],

        12: [(("docker", "environment", "render", "test", "deployment", "performance"), lambda c: _guide(

            c, "a deployment or testing practice that helps an application run reliably outside a developer's machine.",

            "A small team needs to deploy a tested app without embedding credentials in its source code.",

            "DATABASE_URL = os.environ['DATABASE_URL']",

            "The app reads its database setting from the environment, keeping secrets out of source files.",

            "Test the production build and configuration; a successful local run does not prove deployment works.",

            "List one smoke test and one performance check you would run after deployment.",

        ))],

    }





_COURSE_RULES = {

    "data_analytics": _data_rules(),

    "ai_ml": _ai_rules(),

    "robotics": _robotics_rules(),

    "electronics": _electronics_rules(),

    "cybersecurity": _cyber_rules(),

    "web_dev": _web_rules(),

}

