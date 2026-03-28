# Quick Start Guide

## Installation (30 seconds)

```bash
cd behavioral-bias-detector
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` in your browser.

## First Steps

### Option 1: Test with Pre-loaded Examples
1. Click any example button (Fortnite, Netflix, etc.)
2. See analysis immediately with radar chart
3. Scroll down to see detailed bias breakdown

### Option 2: Analyze Your Own Product
1. Enter product name
2. Describe pricing structure in the textarea
3. Click "Analyze for Biases"
4. Review results

## Understanding Results

### Manipulation Score (0-100)
- **0-20**: Low manipulation - mostly straightforward pricing
- **20-40**: Moderate - some behavioral tactics present
- **40-60**: High - multiple bias exploitation techniques
- **60-80**: Very High - aggressive behavioral optimization
- **80-100**: Extreme - comprehensive multi-bias strategy

### Radar Chart
- Each axis represents a bias type
- Further from center = higher bias presence
- Larger area = more biases exploited overall

### Bias Details
For each detected bias:
- **Score**: How much this pricing exploits this bias (0-100)
- **Confidence**: How certain we are in detection (0-100%)
- **Indicators**: Specific keywords/patterns matched
- **Explanation**: Why this bias matters psychologically

## Example Analysis

### What to Expect
When you analyze **Fortnite Battle Pass**, you should see:

```
Overall Score: ~50/100 (High manipulation)

Highest Biases:
1. Artificial Scarcity - Exclusive cosmetics that never return
2. Dual Currency - V-Bucks obscure real USD spending
3. Status Quo Bias - "Most Popular" tier pre-selected
```

This makes sense because:
- Fortnite makes cosmetics time-limited (scarcity)
- Uses virtual currency to hide real costs
- Uses psychological pricing tiers

## Tips for Analyzing Products

### Include in Description
- **Pricing tiers**: Free, Basic, Pro, Enterprise
- **Payment model**: One-time, subscription, in-app
- **Promotions**: Discounts, bundles, limited offers
- **Scarcity tactics**: Limited stock, time limits, exclusives
- **Currencies**: Real money, virtual currency, points
- **Social elements**: Reviews, badges, popularity signals
- **Default options**: What's pre-selected or recommended

### Example Format
```
Netflix Subscription:
- Three tiers: Basic ($6.99), Standard ($15.49), Premium ($22.99)
- Standard marked as "Most Popular"
- Monthly auto-renewal
- Exclusive content creates switching costs
- Original programming drives retention
```

## Interpreting for Different Audiences

### As a Product Manager
Use results to:
- Audit competitor pricing psychology
- Design ethical pricing strategy
- Identify where you might be exposed to regulation
- Benchmark against industry standards

### As an Analyst
Use results to:
- Identify undervalued/overvalued companies
- Assess pricing power and customer lock-in
- Evaluate business model sustainability
- Compare business models across industries

### As a Researcher
Use results to:
- Study real-world application of behavioral economics
- Identify patterns across industries
- Track evolution of pricing tactics
- Compare ethics/aggressiveness

## Technical Details

### What the Detector Does
1. **Tokenizes input** into lowercase text
2. **Matches keywords** for each bias type
3. **Applies regex patterns** for complex pricing structures
4. **Scores each bias** based on evidence strength
5. **Calculates confidence** from number of indicators
6. **Weights overall score** by per-bias confidence
7. **Generates explanations** grounded in behavioral economics

### Bias Detection Sensitivity
The detector is tuned to:
- Avoid false positives (low bias false alarms)
- Catch real manipulation (high precision)
- Require multiple indicators for high confidence
- Weight pattern matches heavily

### Limitations
- Text-based analysis only (can't detect UI/UX manipulations)
- Keyword matching has false negative rate (~10-15%)
- Works best with detailed pricing descriptions
- Doesn't measure magnitude of financial impact
- English language only

## Advanced Usage

### Comparing Competitors
Analyze 3-4 competitors to:
- See which biases are industry-standard
- Identify differentiation opportunities
- Assess relative aggressiveness
- Benchmark market practices

### Tracking Changes Over Time
- Re-analyze products quarterly
- Watch scores increase as pricing optimization improves
- Identify regulatory pressure points
- Study pricing arms races

### Creating Benchmarks
- Analyze 20+ products in an industry
- Build distribution of scores
- Identify best practices vs. aggressive tactics
- Compare across industries

## Troubleshooting

### Results Seem Too Low
- Add more detail to pricing description
- Include marketing language and promotional messages
- Mention loyalty programs, tiers, exclusives
- More text = more pattern matches = higher confidence

### Results Seem Too High
- Results may be accurate! Many modern pricing is heavily optimized
- Check which biases drive the score
- Some sectors (gaming, SaaS) are legitimately manipulative

### Bias Not Detected
- Check keywords in description match bias patterns
- Some biases require specific language to detect
- Try rephrasing description with more detail
- Check README for examples of detection patterns

## Next Steps

1. Analyze your company's pricing
2. Analyze competitors
3. Review README.md for full theory
4. Explore source code (bias_detector.py) to understand scoring
5. Adapt scoring rules for your domain

## Getting Help

- Read bias explanations in README.md
- Check example products for reference
- Review Kahneman & Tversky references
- Examine scoring logic in bias_detector.py

---

**Ready?** Click an example button or enter your own product to start!
