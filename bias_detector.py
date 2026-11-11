"""
Behavioral Bias Detector - Core Logic
Analyzes pricing structures against behavioral economics frameworks
Based on Kahneman & Tversky prospect theory and behavioral pricing research
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class BiasScore:
    """Represents a bias detection result"""
    name: str
    score: float  # 0-100
    confidence: float  # 0-1
    indicators: List[str]
    explanation: str


class BiasMatcher:
    """
    Detects behavioral biases in pricing structures.
    Uses keyword matching, pattern analysis, and feature detection.
    """

    def __init__(self):
        """Initialize bias detection patterns and rules"""
        self.bias_patterns = self._initialize_patterns()

    def _initialize_patterns(self) -> Dict:
        """Define keyword patterns and rules for each bias type"""
        return {
            "anchoring": {
                "keywords": [
                    "original price", "was", "save", "discount", "regular price",
                    "list price", "suggested retail", "full price", "reduced from",
                    "msrp", "normally", "standard price", "before", "marked down"
                ],
                "patterns": [
                    r"\$\d+\s*-\s*\$\d+",  # Price range
                    r"save\s*\$?\d+",  # Save X
                    r"\d+%\s*off",  # X% off
                ],
                "description": "Anchoring effect: Initial price reference influences perception of value"
            },
            "sunk_cost": {
                "keywords": [
                    "battle pass", "season pass", "subscription", "yearly",
                    "commitment", "locked in", "membership", "pass", "recurring",
                    "renewable", "ongoing", "continuous", "maintain"
                ],
                "patterns": [
                    r"(?:per|per )?month|weekly|daily|annual",
                    r"subscription|pass|membership",
                    r"auto-renew|auto-renews",
                ],
                "description": "Sunk Cost Fallacy: Recurring costs create psychological investment"
            },
            "loss_aversion": {
                "keywords": [
                    "limited time", "offer expires", "going away", "disappears",
                    "don't miss", "won't be back", "ending", "final", "last chance",
                    "exclusive", "exclusive offer", "only while supplies", "running out",
                    "hurry", "urgent", "act now", "before it's gone"
                ],
                "patterns": [
                    r"limit\w*\s+(?:time|quantity|offer)",
                    r"(?:end|expir|remov|disappear).*\w+",
                    r"(?:don't|never)\s+miss",
                ],
                "description": "Loss Aversion: Fear of missing out or losing the opportunity"
            },
            "fomo_scarcity": {
                "keywords": [
                    "limited", "rare", "scarce", "exclusive", "only", "few left",
                    "limited stock", "running out", "sold out soon", "hot item",
                    "in demand", "popular", "trending", "exclusive access",
                    "vanity", "prestige", "status", "elite", "vip"
                ],
                "patterns": [
                    r"(?:only|just|just only)\s+\d+\s+(?:left|remain)",
                    r"limited\s+(?:edition|quantity|time|access)",
                    r"\d+%\s+off.*limited",
                ],
                "description": "FOMO & Scarcity: Artificial scarcity creates urgency and perceived value"
            },
            "endowment_effect": {
                "keywords": [
                    "bundle", "package", "combo", "set", "collection", "package deal",
                    "included", "bonus", "free item", "free", "gift", "extra",
                    "premium bundle", "deluxe", "ultimate", "pro", "plus"
                ],
                "patterns": [
                    r"bundle.*for\s*\$?\d+",
                    r"(?:free|bonus|included)\s+\w+",
                    r"value.*\$?\d+",
                ],
                "description": "Endowment Effect: Bundled items feel more valuable than separate"
            },
            "status_quo_bias": {
                "keywords": [
                    "default", "standard", "basic", "free tier", "entry level",
                    "most popular", "recommended", "suggested", "starter",
                    "tier", "plan", "level", "upgrade"
                ],
                "patterns": [
                    r"(?:most\s+)?popular|recommended|default",
                    r"upgrade.*(?:from|to)",
                    r"(?:basic|standard|free)\s+(?:plan|tier|version)",
                ],
                "description": "Status Quo Bias: Default options attract more selections"
            },
            "social_proof": {
                "keywords": [
                    "popular", "bestselling", "most purchased", "trusted by",
                    "customer favorite", "top rated", "5 stars", "loved by",
                    "award", "recognition", "experts recommend", "used by",
                    "millions of users", "join", "community", "trending"
                ],
                "patterns": [
                    r"(?:\d+(?:,\d+)?\s+)?(?:users|customers|people)",
                    r"\d+\s*(?:star|rating)",
                    r"(?:award|winner|recognized|trusted)",
                ],
                "description": "Social Proof: Others' choices validate purchases"
            },
            "decoy_pricing": {
                "keywords": [
                    "tier", "plan", "option", "three tier", "three price",
                    "good", "better", "best", "bronze", "silver", "gold",
                    "standard", "pro", "enterprise", "vs", "comparison"
                ],
                "patterns": [
                    r"(?:good|better|best)\s+(?:plan|option|tier|price)",
                    r"(?:bronze|silver|gold|platinum)",
                    r"compare.*plan",
                ],
                "description": "Decoy Pricing: Middle option makes expensive option seem better value"
            },
            "dual_currency": {
                "keywords": [
                    "coins", "credits", "gems", "points", "tokens", "bucks",
                    "premium", "premium currency", "battle pass", "robux",
                    "v-bucks", "moneyboosters", "virtual currency",
                    "in-game currency", "premium points"
                ],
                "patterns": [
                    r"(?:coins|gems|credits|points|tokens|bucks|v-bucks)",
                    r"(?:\d+\s+)?(?:premium|virtual|in-game)\s+(?:currency|coins)",
                ],
                "description": "Dual Currency: Abstract currency obscures true spending"
            },
            "artificial_scarcity": {
                "keywords": [
                    "limited edition", "exclusive", "collector", "rare",
                    "seasonal", "battle pass", "event", "only", "available",
                    "never again", "one-time", "permanent", "forever gone",
                    "battlepass", "cosmetic", "skin", "cosmetics"
                ],
                "patterns": [
                    r"limited\s+edition|exclusive\s+(?:event|item|cosmetic)",
                    r"available.*(?:for|until)\s+(?:\d+\s+)?(?:days|hours|weeks)",
                    r"(?:seasonal|event|battle\s+pass)",
                ],
                "description": "Artificial Scarcity: Time/quantity limits drive urgency and spending"
            },
        }

    def detect_bias(self, pricing_text: str, bias_type: str) -> BiasScore:
        """
        Detect presence of a specific bias in pricing text.

        Args:
            pricing_text: Description of pricing structure
            bias_type: Type of bias to detect

        Returns:
            BiasScore with detection results
        """
        if bias_type not in self.bias_patterns:
            raise ValueError(f"Unknown bias type: {bias_type}")

        patterns = self.bias_patterns[bias_type]
        text_lower = pricing_text.lower()

        # Keyword matching
        matched_keywords = []
        for keyword in patterns["keywords"]:
            if keyword in text_lower:
                matched_keywords.append(keyword)

        keyword_score = min(len(matched_keywords) * 8, 50)  # Up to 50 from keywords

        # Pattern matching
        pattern_matches = []
        for pattern in patterns["patterns"]:
            if re.search(pattern, text_lower, re.IGNORECASE):
                pattern_matches.append(pattern)
                keyword_score += 15  # Boost from pattern match

        keyword_score = min(keyword_score, 100)

        # Confidence based on number of indicators
        total_indicators = len(matched_keywords) + len(pattern_matches)
        confidence = min(total_indicators / 5, 1.0)  # Saturate at 5+ indicators

        indicators = matched_keywords[:3]  # Show top 3 indicators

        return BiasScore(
            name=bias_type.replace("_", " ").title(),
            score=keyword_score,
            confidence=confidence,
            indicators=indicators,
            explanation=patterns["description"]
        )

    def analyze_pricing(self, pricing_text: str) -> Tuple[List[BiasScore], float]:
        """
        Analyze pricing structure for all biases.

        Args:
            pricing_text: Full pricing description

        Returns:
            Tuple of (list of BiasScores, overall manipulation score 0-100)
        """
        bias_scores = []

        for bias_type in self.bias_patterns.keys():
            score = self.detect_bias(pricing_text, bias_type)
            bias_scores.append(score)

        # Calculate overall manipulation score
        # Average score, weighted by confidence
        if bias_scores:
            weighted_sum = sum(s.score * s.confidence for s in bias_scores)
            total_confidence = sum(s.confidence for s in bias_scores)
            overall_score = weighted_sum / total_confidence if total_confidence > 0 else 0
        else:
            overall_score = 0

        # Sort by score descending
        bias_scores.sort(key=lambda x: x.score, reverse=True)

        return bias_scores, overall_score

    def get_summary(self, overall_score: float) -> str:
        """Generate summary of manipulation level"""
        if overall_score < 20:
            return "Low: Minimal bias exploitation detected"
        elif overall_score < 40:
            return "Moderate: Some behavioral pricing tactics present"
        elif overall_score < 60:
            return "High: Multiple bias exploitation tactics employed"
        elif overall_score < 80:
            return "Very High: Extensive behavioral pricing optimization"
        else:
            return "Extreme: Aggressive multi-bias exploitation strategy"


# Pre-loaded examples
EXAMPLES = {
    "Fortnite Battle Pass": {
        "description": "Fortnite Battle Pass",
        "text": """
        Fortnite Battle Pass ($9.99/season, seasonal 10-week duration):
        - Limited-time exclusive cosmetics and skins
        - Exclusive battle pass items never available again after season ends
        - V-Bucks premium currency system ($9.99 for 1000 V-Bucks)
        - Bundle deals: Save money when buying cosmetics together
        - Rare exclusive skins that create status among players
        - Free tier with limited rewards to encourage paid upgrade
        - "Most Popular" pricing tier at $9.99
        - Limited-time cosmetics available only during specific events
        - Seasonal progression system creates sunk cost with ongoing play
        - Friend influence: See others with exclusive cosmetics
        - Time pressure: Battle pass expires at season end
        - Dual currency system obfuscates true USD spending
        """
    },
    "FIFA Ultimate Team": {
        "description": "FIFA Ultimate Team (EA Sports)",
        "text": """
        FIFA Ultimate Team:
        - FIFA Points premium currency (real money)
        - Limited card packs ($4.99-$19.99) with random contents
        - Rare "Team of the Week" cards available briefly
        - Collectible card game with trading market
        - Squad building creates sunk cost investment
        - "Most Purchased" tier for popular card packs
        - Seasonal card rotation creates urgency to buy
        - Players show off teams in online multiplayer (social proof)
        - Weekly limited-time special promotions
        - Expensive star player cards drive spending
        - Random loot boxes create gambling-like mechanics
        - "Flash sales" on limited-time player cards
        """
    },
    "Netflix": {
        "description": "Netflix Subscription",
        "text": """
        Netflix Subscription Plans:
        - Three-tier pricing: Basic ($6.99), Standard ($15.49), Premium ($22.99)
        - Monthly recurring subscription (auto-renews)
        - Standard tier marked as "Most Popular"
        - Sharing restrictions create family pressure to upgrade
        - Free trial period creates commitment
        - Binge-watch psychology creates sunk cost
        - Exclusive content not available elsewhere
        - "Cancel anytime" messaging reduces abandonment
        - Regular price increases grandfather existing users
        - New releases create FOMO and retention
        """
    },
    "Amazon Prime": {
        "description": "Amazon Prime Membership",
        "text": """
        Amazon Prime Membership:
        - Annual ($139) or monthly ($14.99) subscription options
        - Bundle value: Free shipping, Prime Video, Prime Music, etc.
        - Recommended upgrade from free Amazon account
        - Monthly commitment with auto-renewal
        - Exclusive Prime Day deals create scarcity and urgency
        - Free trial creates sunk cost when users download app
        - Endowment effect: Bundle makes individual services seem valuable
        - Switching costs: Difficult to leave after using multiple services
        - Status symbol: Prime badge on purchases
        - Student discount creates youth market lock-in
        """
    },
    "Coffee Subscription": {
        "description": "Typical Coffee Subscription Service",
        "text": """
        Daily Coffee Shop Subscription Model:
        - Loyalty card: Buy 10 coffees, get 1 free
        - Subscription membership ($9.99/month) for daily discounts
        - Tiered loyalty: Silver ($0.50 off), Gold ($1.00 off)
        - Limited-time seasonal flavors (Pumpkin Spice September-October)
        - "Save $15/month" anchor messaging for subscription
        - Gamification: Collect stamps, unlock tiers
        - Mobile app rewards create habit formation
        - Social proof: "#1 Coffee Shop in the City" signs
        - Free upgrade offer "just for you" to drive trial
        - Birthday bonus creates gift reciprocity
        """
    }
}
