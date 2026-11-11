# Behavioral Bias Detector

A web application that analyzes any product's pricing structure to identify and score behavioral economics biases it exploits.

The scores and confidence values are keyword/regex heuristics, not calibrated probabilities or a validated measure of consumer harm. No labeled evaluation dataset is included.

## Overview

This tool applies frameworks from behavioral economics and behavioral finance to detect manipulation tactics in pricing strategies. It bridges gaming monetization research with broader consumer economics and financial psychology.

**Purpose:** Identify which cognitive biases a pricing strategy targets, score the manipulation intensity (0-100), and explain the psychological mechanisms at work.

**Use Cases:**
- Product managers evaluating pricing psychology
- Analysts assessing fair pricing vs. manipulation
- Researchers studying behavioral economics in practice
- Students learning behavioral pricing tactics
- Regulators evaluating consumer protection concerns

## Theoretical Foundation

### Behavioral Economics Framework

The detector is built on seminal work in behavioral economics:

- **Kahneman & Tversky (1979) - Prospect Theory**: Foundational framework showing how people make decisions under risk/uncertainty, with emphasis on loss aversion and reference points (anchoring)
- **Thaler (1980) - Mental Accounting**: How consumers organize, code, and evaluate financial activities
- **Ariely (2008) - Predictably Irrational**: Empirical demonstrations of systematic irrationality in economic behavior

### Behavioral Biases Detected

1. **Anchoring Effect**
   - Initial price reference influences perception of value
   - Mechanism: "Save $100!" anchors to original price, making discount seem larger
   - Example: "Was $199.99, now $99.99" anchors perception to $199

2. **Sunk Cost Fallacy**
   - Recurring costs create psychological investment and lock-in
   - Mechanism: Monthly subscriptions create habit and switching costs
   - Example: "Only $9.99/month" feels small but commits $120/year

3. **Loss Aversion**
   - Fear of missing out or losing the opportunity drives spending
   - Mechanism: Fear of loss is psychologically 2-3x stronger than pleasure of gain
   - Example: "Limited time offer ends tonight" triggers urgency

4. **FOMO & Scarcity**
   - Artificial scarcity creates urgency and perceived value
   - Mechanism: Limited quantity or time increases perceived value
   - Example: "Only 3 left in stock" or "Seasonal item, available October only"

5. **Endowment Effect**
   - Bundled items feel more valuable than the sum of parts
   - Mechanism: Ownership increases perceived value of items
   - Example: $49.99 bundle of items worth $20 individually

6. **Status Quo Bias**
   - Default options attract disproportionate selections
   - Mechanism: Inertia favors existing state; switching requires effort
   - Example: "Standard Plan" pre-selected in tier comparison

7. **Social Proof**
   - Others' choices validate purchases
   - Mechanism: Uncertainty drives conformity to group behavior
   - Example: "5★ from 50,000 reviews" or "Most Popular" badge

8. **Decoy Pricing**
   - Middle-priced option makes expensive option seem better value
   - Mechanism: Asymmetric dominance principle
   - Example: Good $9.99 / Better $14.99 / Best $19.99 (Best seems like best value)

9. **Dual Currency Obfuscation**
   - Abstract currency (coins, gems, V-Bucks) obscures true spending
   - Mechanism: Psychological distance reduces pain of payment
   - Example: 1000 V-Bucks seems arbitrary; $9.99 is clearer
   - Finance parallel: Credit cards reduce pain vs. cash

10. **Artificial Scarcity**
    - Time/quantity limits drive urgency and spending
    - Mechanism: Combines scarcity + loss aversion + endowment
    - Example: "Battle Pass expires December 31" + "Exclusive cosmetics never return"

## Features

### Web Interface
- **Input Form**: Enter any product/service and describe its pricing structure
- **Pre-loaded Examples**: Fortnite Battle Pass, FIFA Ultimate Team, Netflix, Amazon Prime, Coffee subscription
- **Interactive Analysis**: Real-time bias detection with confidence scores
- **Visual Heatmap**: Radar chart showing which biases are most present
- **Detailed Explanations**: Each detected bias includes explanation and supporting indicators

### Detection Engine
- **Keyword Pattern Matching**: Identifies bias-indicative language
- **Regex Pattern Recognition**: Detects pricing structures and promotional language
- **Confidence Scoring**: Weights results by number and quality of indicators
- **Manipulation Score**: 0-100 overall rating with interpretation guide

### Output
- **Per-Bias Scoring**: 0-100 score for each of 10 biases
- **Confidence Levels**: 0-100% confidence in each detection
- **Supporting Indicators**: Actual keywords/patterns matched
- **Bias Explanations**: Grounded in behavioral economics research
- **Overall Manipulation Summary**: "Low" through "Extreme" rating with interpretation

## Installation

### Requirements
- Python and pip; the pinned dependencies and API tests were verified with Python 3.9.
- A browser. The radar chart loads Chart.js from a CDN and needs network access.

### Setup

```bash
# From a new checkout; skip these two commands if already in the repository
git clone https://github.com/TheCromazone/behavioral-bias-detector.git
cd behavioral-bias-detector

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Run the Flask app
python app.py
```

The app starts on `http://localhost:5000` with Flask's development server and debug mode. On Windows, activate with `.venv\Scripts\Activate.ps1` instead. If port 5000 is occupied, use `python -m flask --app app run --port 5001`.

### Check the API

```bash
python -m unittest discover -s tests -v
```

The tests run in process without starting a server. They cover all five examples and malformed inputs. `/api/analyze` expects a JSON object with a string `pricing_text`; `/api/example` expects a string `example_name`. Invalid bodies return a JSON error with HTTP 400, and unknown example names return HTTP 404.

Local environments, Python caches, and `.env` files are ignored by Git. The application does not persist analyses; save any research data separately.

## Usage

### Web Interface

1. **Enter Product Details**
   - Product/Service Name (e.g., "Fortnite Battle Pass")
   - Pricing Structure (describe tiers, currencies, promotions, etc.)

2. **Analyze**
   - Click "Analyze for Biases"
   - Review overall Manipulation Score (0-100)
   - Examine radar chart showing which biases are present

3. **Interpret Results**
   - Each bias shows score, confidence, indicators
   - Read explanations for behavioral mechanisms
   - Use findings to evaluate pricing fairness

### Pre-loaded Examples

Click any example button to auto-fill and analyze:
- **Fortnite Battle Pass**: Gaming with V-Bucks, seasonal exclusives
- **FIFA Ultimate Team**: Loot boxes, rare cards, trading market
- **Netflix**: Subscription tiers, "Most Popular" anchoring
- **Amazon Prime**: Annual/monthly toggle, bundled benefits
- **Coffee Subscription**: Loyalty program, limited-time drinks

## Architecture

### Core Components

**`bias_detector.py`** - Detection Engine
- `BiasMatcher` class: Analyzes text for bias patterns
- `BiasScore` dataclass: Structured detection results
- Keyword patterns and regex for each bias type
- `analyze_pricing()`: Main analysis method
- Pre-loaded example data

**`app.py`** - Flask Backend
- `/` - Main page with examples
- `/api/analyze` - POST endpoint for bias analysis
- `/api/example` - Load pre-configured examples
- `/api/examples` - List all examples

**`templates/index.html`** - Interactive Frontend
- Form input for pricing structure
- Example selection
- Results display with radar chart
- Detailed bias breakdown
- Responsive mobile design

**`static/style.css`** - Professional Styling
- Modern gradient design
- Color-coded bias severity
- Responsive grid layout
- Accessible typography

## Example Analyses

### Fortnite Battle Pass
```
Overall Manipulation Score: 78/100 ("Very High")

Top Biases Detected:
- FOMO & Scarcity: 92/100 (exclusive seasonal cosmetics never return)
- Sunk Cost Fallacy: 85/100 (monthly pass commitment)
- Dual Currency: 80/100 (V-Bucks obscure USD spending)
- Artificial Scarcity: 75/100 (battle pass expires)
- Anchoring: 60/100 (seasonal pricing consistency)
```

### Netflix
```
Overall Manipulation Score: 52/100 ("High")

Top Biases Detected:
- Status Quo Bias: 72/100 ("Standard" pre-selected, most popular)
- Sunk Cost Fallacy: 68/100 (monthly auto-renewal)
- Endowment Effect: 55/100 (bundle combines video, music, ads)
- Social Proof: 48/100 (community of users, shared shows)
```

## Detection Logic

The detector uses a scoring system combining multiple signals:

1. **Keyword Matching** (0-50 points)
   - Each bias-indicative keyword adds 8 points
   - Capped at 50 to require pattern confirmation

2. **Regex Pattern Matching** (+15 points each)
   - Complex patterns (price ranges, discount language) add 15 points
   - Multiple patterns compound evidence

3. **Confidence Calculation** (0-1.0)
   - Based on number of unique indicators
   - 5+ indicators = 100% confidence
   - Saturates at 5 to prevent over-confidence

4. **Overall Score** (0-100)
   - Weighted average of all 10 bias scores
   - Weighted by per-bias confidence
   - Results interpreted into summary categories

## Portfolio Value

### For Quantitative Analyst / Finance Roles

**Demonstrates:**
- Understanding of behavioral finance and market psychology
- Ability to operationalize economic theory into scoring systems
- Natural language processing and pattern recognition
- Pricing strategy analysis
- Risk/manipulation quantification

**Research Foundation:**
- Based on thesis research: "The Transition from Loot Boxes to Battle Passes in Video Games" (Matthew Cromaz, Reed College 2023)
- Applies Kahneman & Tversky prospect theory to real products
- Bridges gaming monetization with consumer finance

**Application to Finance:**
- Stock option pricing exploits anchoring (exercise prices)
- Mutual fund fee structures exploit inattention and status quo
- Credit card promotions exploit loss aversion and scarcity
- Insurance pricing leverages mental accounting
- Retirement plan design exploits status quo bias

### For Product Management / Growth Roles

**Demonstrates:**
- Deep understanding of behavioral pricing psychology
- Ability to identify and quantify manipulation in competitor products
- Framework for ethical pricing strategy design
- Consumer psychology and behavioral science application
- Data-driven product analysis

## References

**Foundational Theory:**
- Kahneman, D., & Tversky, A. (1979). "Prospect Theory: An Analysis of Decision under Risk" - *Econometrica*
- Tversky, A., & Kahneman, D. (1985). "The Framing of Decisions and the Psychology of Choice"
- Thaler, R. H. (1985). "Mental Accounting and Consumer Choice"

**Behavioral Pricing:**
- Ariely, D. (2008). *Predictably Irrational: The Hidden Forces That Shape Our Decisions*
- Poundstone, W. (2010). *Priceless: The Myth of Fair Value (and How to Take Advantage of It)*
- Cialdini, R. (1984). *Influence: The Psychology of Persuasion*

**Game Monetization:**
- Seif El-Nasr, M., et al. (2015). "Engagement in Games: Developing Engagement Strategies for a Digital Game"
- Zendle, D., et al. (2020). "Loot Boxes Are Psychologically Akin to Gambling" - *Royal Society Open Science*

## License

Educational and research use. Created as portfolio piece demonstrating behavioral economics application.

## Author

Created by Matthew Cromaz
Based on behavioral economics research and thesis work on game monetization strategies.
