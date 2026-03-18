"""Convert anomaly CSVs to dashboard JSON files.

Usage:
    python dashboard/scripts/prepare_data.py
"""
import json
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANOMALY_DIR = Path(r"C:\Users\ksaen\OneDrive - ACC-Chulalongkorn University\research\ai-assisted\setsmart-projects\agentic-factor-investing\results\anomalies")
OUT_DIR = ROOT / "src" / "lib" / "data"

# ── Group mapping (from visualize_anomalies_v2.R lines 35-90) ──────────

GROUPS = [
    {
        "name": "Fama-French Six",
        "factors": ["mkt", "smb", "hml", "rmw", "cma", "umd"],
        "labels": ["MKT", "SMB", "HML", "RMW", "CMA", "UMD"],
    },
    {
        "name": "q-Factors (HXZ)",
        "factors": ["me", "ia", "roe"],
        "labels": ["ME", "IA", "ROE"],
    },
    {
        "name": "Behavioral (DHS)",
        "factors": ["pead", "fin"],
        "labels": ["PEAD", "FIN"],
    },
    {
        "name": "QMJ",
        "factors": ["qmj", "prof", "grow", "safe"],
        "labels": ["QMJ", "PROF", "GROW", "SAFE"],
    },
    {
        "name": "Low-Risk",
        "factors": ["bab", "vol", "ivol", "max"],
        "labels": ["BAB", "VOL", "IVOL", "MAX"],
    },
    {
        "name": "Momentum",
        "factors": ["mom6", "mom1"],
        "labels": ["MOM6", "MOM1"],
    },
    {
        "name": "Value",
        "factors": ["sp", "ocp", "dp", "cfp", "a_me", "ebp",
                     "bm_adj_sga", "bm_adj_sga2", "ep"],
        "labels": ["SP", "OCP", "DP", "CFP", "A/ME", "EBP",
                    "BM SGA", "BM SGA2", "EP"],
    },
    {
        "name": "Profitability",
        "factors": ["rec_turnover", "cfoa", "ato", "ol", "ti_bi",
                     "pm", "cbop", "gpa", "roe_ann", "roa_ann",
                     "cto", "gmar", "rnoa",
                     "sue", "rs", "roeq", "roaq", "gpq", "earn_acc", "nei"],
        "labels": ["REC TURN", "CFOA", "ATO", "OL", "TI/BI",
                    "PM", "CBOP", "GPA", "ROE", "ROA",
                    "CTO", "GMAR", "RNOA",
                    "SUE", "RS", "ROE-q", "ROA-q", "GP-q", "EARN-ACC", "NEI"],
    },
    {
        "name": "Investment",
        "factors": ["eiss", "nsi", "oa", "nxf", "ivg", "ivc",
                     "ig", "noa", "dpia", "poa",
                     "ccc", "accrq"],
        "labels": ["EISS", "NSI", "OA", "NXF", "IVG", "IVC",
                    "IG", "NOA", "DPIA", "POA",
                    "CCC", "ACCRQ"],
    },
    {
        "name": "Quality",
        "factors": ["acc_qmj", "dcfoa", "lev", "lev_full", "dgpoa",
                     "dgmar", "droa", "droe", "zscore_book", "zscore_mkt",
                     "evol", "zscore_q", "cfvol",
                     "oscore", "diss", "npop"],
        "labels": ["ACC", "DCFOA", "LEV", "LEV FULL", "DGPOA",
                    "DGMAR", "DROA", "DROE", "Z BOOK", "Z MKT",
                    "EVOL", "Z-q", "CFVOL",
                    "OSCORE", "DISS", "NPOP"],
    },
    {
        "name": "Trading / Liquidity",
        "factors": ["turn", "str", "illiq"],
        "labels": ["TURN", "STR", "ILLIQ"],
    },
]

# 11-color palette with wider hue range for dot plot legibility
GROUP_COLORS = {
    "Fama-French Six":     "#1e3a5f",
    "q-Factors (HXZ)":     "#2d7d9a",
    "Behavioral (DHS)":          "#7b2d8e",
    "QMJ":                 "#c4523e",
    "Low-Risk":            "#2a8a4a",
    "Momentum":            "#d4a017",
    "Value":               "#3a7ca5",
    "Profitability":       "#e07830",
    "Investment":          "#5b6abf",
    "Quality":             "#8a6d5b",
    "Trading / Liquidity": "#888888",
}


def build_factor_to_group():
    """Return dict: factor_name -> {group, label, group_index, factor_index}."""
    mapping = {}
    for gi, grp in enumerate(GROUPS):
        for fi, fac in enumerate(grp["factors"]):
            mapping[fac] = {
                "group": grp["name"],
                "label": grp["labels"][fi],
                "group_index": gi,
                "factor_index": fi,
            }
    return mapping


def load_metadata(path):
    """Load metadata CSV into list of dicts."""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_returns(path):
    """Load standard returns CSV. Returns (dates, columns, rows)."""
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        columns = header[1:]  # skip unnamed date column
        dates = []
        rows = []
        for row in reader:
            dates.append(row[0])
            rows.append(row[1:])
    return dates, columns, rows


# ── Practitioner-friendly factor descriptions ───────────────────────────

DESCRIPTIONS = {
    # Fama-French Six
    "mkt": "Market excess return: return on the value-weighted market portfolio minus the risk-free rate.",
    "smb": "Small Minus Big: return spread between small-cap and large-cap stocks.",
    "hml": "High Minus Low: return spread between high and low book-to-market stocks.",
    "rmw": "Robust Minus Weak: return spread between firms with high and low operating profitability.",
    "cma": "Conservative Minus Aggressive: return spread between firms with low and high asset growth.",
    "umd": "Up Minus Down: momentum factor based on past 12-month returns (skipping the most recent month).",
    # q-Factors (HXZ)
    "me": "Size factor from the q-factor model: small minus big market equity.",
    "ia": "Investment factor from the q-factor model: low minus high total asset growth.",
    "roe": "Profitability factor from the q-factor model: high minus low return on equity.",
    # Behavioral
    "pead": "Post-Earnings Announcement Drift (DHS long-horizon factor): stocks with positive earnings surprises continue to outperform.",
    "fin": "Composite Financing (DHS short-horizon factor): firms issuing equity and debt tend to underperform.",
    # QMJ
    "qmj": "Quality Minus Junk: composite of profitability, growth, safety, and payout signals.",
    "prof": "QMJ profitability component: composite of margin, return, and cash flow measures.",
    "grow": "QMJ growth component: composite of multi-year growth in profitability measures.",
    "safe": "QMJ safety component: composite of leverage, distress risk, and return volatility.",
    # Low-Risk
    "bab": "Betting Against Beta: leveraged low-beta stocks minus de-leveraged high-beta stocks.",
    "vol": "Volatility: low total return volatility minus high volatility stocks.",
    "ivol": "Idiosyncratic Volatility: low residual volatility (after removing market exposure) minus high.",
    "max": "Lottery Demand: stocks with low maximum daily returns minus those with high max returns.",
    # Momentum
    "mom6": "Six-month momentum: stocks with high past 6-month returns minus low.",
    "mom1": "One-month short-term reversal: last month's losers minus last month's winners.",
    # Value
    "sp": "Sales-to-Price: firms with high revenue relative to market value versus low.",
    "ocp": "Operating Cash Flow to Price: firms with high operating cash flow relative to market value.",
    "dp": "Dividend-to-Price: high dividend yield stocks versus low.",
    "cfp": "Cash Flow to Price: earnings plus depreciation relative to market value.",
    "a_me": "Assets-to-Market: total assets (debt + equity) relative to market value.",
    "ebp": "Enterprise Book-to-Price: enterprise book value over enterprise market value — a leverage-adjusted value measure.",
    "bm_adj_sga": "Intangible-Adjusted Book-to-Market: book value adjusted for capitalized SG&A (intangible capital).",
    "bm_adj_sga2": "Conservative Intangible-Adjusted B/M: book value plus 30% of SG&A relative to market value.",
    "ep": "Earnings-to-Price: net income relative to market value.",
    # Profitability
    "rec_turnover": "Receivables Turnover: revenue divided by accounts receivable — measures collection efficiency.",
    "cfoa": "Cash Flow to Assets: operating cash flow divided by total assets.",
    "ato": "Asset Turnover: revenue divided by total assets — a DuPont efficiency component.",
    "ol": "Operating Leverage: ratio of fixed operating costs (COGS + SG&A) to total assets.",
    "ti_bi": "Tax-to-Book Income: taxable income relative to book income — a measure of earnings quality.",
    "pm": "Profit Margin: net income divided by revenue. Reversed in Thailand (high margin underperforms).",
    "cbop": "Cash-Based Operating Profitability: gross profit plus depreciation minus SG&A, scaled by assets.",
    "gpa": "Gross Profitability: gross profit (revenue minus COGS) divided by total assets.",
    "roe_ann": "Return on Equity: annual net income divided by book equity.",
    "roa_ann": "Return on Assets: annual net income divided by total assets.",
    "cto": "Capital Turnover: revenue divided by operating assets (PP&E + inventory + receivables).",
    "gmar": "Gross Margin: gross profit as a percentage of revenue.",
    "rnoa": "Return on Net Operating Assets: EBIT divided by net operating assets.",
    # Investment
    "eiss": "Equity Issuance: change in shares outstanding scaled by assets — firms issuing equity tend to underperform.",
    "nsi": "Net Stock Issuance: percentage change in shares outstanding — a market-timing signal.",
    "oa": "Operating Accruals: the non-cash component of earnings (net income minus operating cash flow) scaled by assets.",
    "nxf": "Net External Financing: combined equity and debt issuance scaled by assets.",
    "ivg": "Inventory Growth (scaled): change in inventory relative to total assets.",
    "ivc": "Inventory Growth (percentage): percentage change in inventory — a demand disappointment signal.",
    "ig": "Investment Growth: year-over-year total asset growth — the core investment anomaly.",
    "noa": "Net Operating Assets: cumulative investment proxy based on operating assets minus operating liabilities.",
    "dpia": "PP&E Growth: year-over-year growth in property, plant, and equipment.",
    "poa": "Physical Investment: capital expenditure proxy (change in PP&E plus depreciation) scaled by assets.",
    # Quality
    "acc_qmj": "Accruals Quality: the non-cash component of earnings — low accruals signal higher earnings quality.",
    "dcfoa": "Change in Cash Flow to Assets: year-over-year improvement in operating cash flow generation.",
    "lev": "Low Leverage: firms with low long-term debt relative to assets (safer balance sheets).",
    "lev_full": "Low Full Leverage: firms with low total debt (including short-term and preferred) relative to assets.",
    "dgpoa": "Change in Gross Profitability: year-over-year improvement in gross profit to assets.",
    "dgmar": "Change in Gross Margin: year-over-year improvement in gross profit as a share of revenue.",
    "droa": "Change in ROA: year-over-year improvement in return on assets.",
    "droe": "Change in ROE: year-over-year improvement in return on equity.",
    "zscore_book": "Altman Z-Score (book): financial distress measure using only accounting data.",
    "zscore_mkt": "Altman Z-Score (market): financial distress measure using market value of equity.",
    # Quality (additional)
    "evol": "Earnings Volatility: 20-quarter standard deviation of quarterly ROE — stable earners outperform.",
    "zscore_q": "Altman Z-Score (quarterly): financial distress measure updated quarterly using accounting data.",
    "cfvol": "Cash Flow Volatility: 16-quarter standard deviation of operating cash flow to sales — stable cash flows signal quality.",
    "oscore": "Ohlson O-Score: accounting-based probability of bankruptcy; low-distress firms outperform.",
    "diss": "Debt Issuance: log change in long-term debt — firms reducing debt outperform those increasing it.",
    "npop": "Net Payout to Price: count of years with positive net payout relative to price — consistent payout signals quality.",
    # Profitability (quarterly)
    "sue": "Standardized Unexpected Earnings: quarterly earnings surprise scaled by historical standard deviation — earnings momentum.",
    "rs": "Revenue Surprise: year-over-year sales change scaled by historical standard deviation — revenue momentum.",
    "roeq": "Quarterly ROE: quarterly earnings divided by book equity — more timely signal than annual ROE.",
    "roaq": "Quarterly ROA: quarterly earnings divided by total assets — more timely signal than annual ROA.",
    "gpq": "Quarterly Gross Profitability: gross profit divided by lagged total assets, updated quarterly.",
    "earn_acc": "Earnings Acceleration: second derivative of quarterly earnings — positive values signal accelerating profitability.",
    "nei": "Number of Earnings Increases: count of year-over-year earnings increases in the past 8 quarters (earnings streak).",
    # Investment (quarterly)
    "ccc": "Cash Conversion Cycle: days inventory outstanding plus days receivables outstanding minus days payable outstanding — high CCC signals capital inefficiency.",
    "accrq": "Quarterly Accruals: quarterly earnings minus operating cash flow divided by assets — high accruals signal lower earnings quality.",
    # Trading / Liquidity
    "turn": "Share Turnover: trading volume relative to market value — low turnover stocks tend to earn a premium.",
    "str": "Short-Term Reversal: last month's return — losers bounce back, winners pull back.",
    "illiq": "Illiquidity: Amihud's measure of price impact — illiquid stocks earn a premium.",
}


def compute_simple_stats(returns_vals):
    """Compute simple t-stat, annualized return/vol, and max drawdown."""
    import math
    vals = [v for v in returns_vals if v is not None]
    n = len(vals)
    if n < 24:
        return None, None, None, None
    mu = sum(vals) / n
    var = sum((v - mu) ** 2 for v in vals) / (n - 1)
    sd = math.sqrt(var)
    se = sd / math.sqrt(n)
    t_stat = mu / se if se > 0 else None
    ann_ret = mu * 12
    ann_vol = sd * math.sqrt(12)

    # Max drawdown from cumulative returns
    cum = 1.0
    peak = 1.0
    max_dd = 0.0
    for v in vals:
        cum *= (1 + v)
        if cum > peak:
            peak = cum
        dd = (peak - cum) / peak
        if dd > max_dd:
            max_dd = dd

    return t_stat, ann_ret, ann_vol, max_dd


def build_factors_json(metadata_rows, ftg, returns_series):
    """Build factors.json: list of factor objects with metadata + group info."""
    factors = []
    for row in metadata_rows:
        name = row["name"]
        if name not in ftg:
            continue
        ginfo = ftg[name]

        # Compute simple t-stat and annualized stats from returns
        series = returns_series.get(name, [])
        simple_t, ann_ret, ann_vol, max_dd = compute_simple_stats(series)

        factors.append({
            "name": name,
            "group": ginfo["group"],
            "label": ginfo["label"],
            "groupIndex": ginfo["group_index"],
            "factorIndex": ginfo["factor_index"],
            "description": DESCRIPTIONS.get(name, ""),
            "formula": row.get("formula", ""),
            "direction": row.get("direction", ""),
            "reference": row.get("reference", ""),
            "notes": row.get("notes", ""),
            "hlzPass": simple_t is not None and abs(simple_t) > 3.0,
            "tStat": round(simple_t, 6) if simple_t is not None else None,
            "annRet": round(ann_ret, 6) if ann_ret is not None else None,
            "annVol": round(ann_vol, 6) if ann_vol is not None else None,
            "sharpe": round(ann_ret / ann_vol, 6) if ann_ret is not None and ann_vol and ann_vol > 0 else None,
            "maxDrawdown": round(max_dd, 6) if max_dd is not None else None,
        })
    factors.sort(key=lambda f: (f["groupIndex"], f["factorIndex"]))
    return factors


def build_returns_json(dates, columns, rows):
    """Build returns.json: {dates: [...], series: {factor: [values]}}."""
    # Filter to July 2001 onward
    start_idx = None
    for i, d in enumerate(dates):
        if d >= "2001-07":
            start_idx = i
            break
    if start_idx is None:
        raise ValueError("No dates >= 2001-07 found")

    filtered_dates = dates[start_idx:]
    series = {}
    for ci, col in enumerate(columns):
        vals = []
        for ri in range(start_idx, len(rows)):
            raw = rows[ri][ci]
            vals.append(float(raw) if raw else None)
        series[col] = vals

    # Pre-compute cumulative returns per factor
    cumulative = {}
    for col, vals in series.items():
        cum = []
        total = 1.0
        for v in vals:
            if v is not None:
                total *= (1 + v)
            cum.append(round(total, 6))
        cumulative[col] = cum

    return {
        "dates": filtered_dates,
        "series": {k: [round(v, 8) if v is not None else None for v in vs]
                   for k, vs in series.items()},
        "cumulative": cumulative,
    }


def build_groups_json():
    """Build groups.json: ordered list of group definitions."""
    return [
        {
            "name": grp["name"],
            "factors": grp["factors"],
            "labels": grp["labels"],
            "color": GROUP_COLORS[grp["name"]],
            "index": i,
        }
        for i, grp in enumerate(GROUPS)
    ]


def _float(val):
    """Parse float or return None."""
    if not val or val == "":
        return None
    try:
        return round(float(val), 6)
    except (ValueError, TypeError):
        return None


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ftg = build_factor_to_group()

    # returns.json (build first — factors needs the series for t-stat computation)
    dates, columns, rows = load_returns(
        ANOMALY_DIR / "th_anomalies_standard.csv"
    )
    returns = build_returns_json(dates, columns, rows)

    # factors.json (uses returns series for simple t-stat computation)
    meta_rows = load_metadata(ANOMALY_DIR / "th_anomalies_metadata.csv")
    factors = build_factors_json(meta_rows, ftg, returns["series"])
    with open(OUT_DIR / "factors.json", "w", encoding="utf-8") as f:
        json.dump(factors, f, indent=2)
    print(f"factors.json: {len(factors)} factors")
    with open(OUT_DIR / "returns.json", "w", encoding="utf-8") as f:
        json.dump(returns, f)
    print(f"returns.json: {len(returns['dates'])} months, "
          f"{len(returns['series'])} factors")

    # groups.json
    groups = build_groups_json()
    with open(OUT_DIR / "groups.json", "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=2)
    print(f"groups.json: {len(groups)} groups")


if __name__ == "__main__":
    main()
