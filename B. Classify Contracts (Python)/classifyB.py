# --------------------------------------------------------------------------------------------
# This script defines a function to re-classify credit contracts into cost and investment
# categories (see Theoretical Framework). It inputs the contract file
# 'operacao_gleba_master', cleaned in STATA, and outputs a reduced re-classified file
# mapping contract_recipient_id to the corrected classification type B, 'classifyB.csv'.
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# SETUP
# --------------------------------------------------------------------------------------------

# Dependencies
import pandas as pd
import unicodedata

# Path definitions
CSV_PATH = "/Users/carlotaloranlopez/Desktop/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/CONTRACT/operacao_gleba_master.csv"
OUTPUT_PATH = "/Users/carlotaloranlopez/Desktop/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/CONTRACT/classifyB.csv"

# Columns used for purpose / rules
CATEGORICAL_COLS = [
    "cd_programa",
    "cd_modalidade",
    "cd_produto",
    "cd_categ_emitente"
]
NUMERIC_COLS = [
    "vl_juros",
    "vl_prev_prod",
    "vl_parc_credito",
    "vl_rec_proprio",
    "vl_area_informada"
]

# --------------------------------------------------------------------------------------------
# Stricter numeric thresholds
# --------------------------------------------------------------------------------------------

# Define thresholds (by ChatGPT)
LOAN_SIZE_THRESHOLD = 120000
PRED_PROD_THRESHOLD = 250000
FARM_AREA_THRESHOLD = 120

# Program restrictions
program_mapping = {
    "abc+": "investimento",
    "ftra": "custeio",
    "funcafé": None,
    "inovagro": "investimento",
    "moderagro": "investimento",
    "moderfrota": "investimento",
    "no program": None,
    "procab-agro": "custeio",
    "prodecoop": "investimento",
    "proirriga": "investimento",
    "pronaf": None,
    "pronamp": None,
    "Other": None
}

# --------------------------------------------------------------------------------------------
# Function definitions
# --------------------------------------------------------------------------------------------

def normalize_text(s):
    if isinstance(s, str):
        s = s.lower().strip()
        s = unicodedata.normalize("NFKD", s)
        s = "".join(c for c in s if not unicodedata.combining(c))
    return s


def classify(row):
    """
    Rules (Type B very strict):
    - Default: custeio
    - Investimento if:
        - Program mapping enforces it, OR
        - Durable capital keywords + at least one numeric signal, OR
        - All three numeric investment thresholds are exceeded
    """

    # Program-based rule (dominant)
    prog = str(row.get("cd_programa", "")).lower()
    mapped = program_mapping.get(prog, None)
    if mapped is not None:
        return mapped

    # Text-based rule (by ChatGPT)
    parts = [str(row[col]) for col in CATEGORICAL_COLS if col in row]
    text = normalize_text(" ".join(parts))

    investment_keywords = [
        "trator", "colheitadeira",
        "equipamento pesado", "irrigacao",
        "silo", "armazenagem",
        "galpao", "infraestrutura",
        "instalacao fixa",
        "benfeitoria permanente",
        "ampliacao", "modernizacao"
    ]

    exclusion_keywords = [
        "insumo", "semente", "fertilizante",
        "defensivo", "manutencao", "reparo",
        "substituicao", "capital de giro",
        "custeio", "safra", "ciclo",
        "curto prazo", "operacional"
    ]

    # Meet numeric signals (by ChatGPT)
    numeric_signals = 0

    if row.get("vl_parc_credito", 0) >= LOAN_SIZE_THRESHOLD:
        numeric_signals += 1
    if row.get("vl_prev_prod", 0) >= PRED_PROD_THRESHOLD:
        numeric_signals += 1
    if row.get("vl_area_informada", 0) >= FARM_AREA_THRESHOLD:
        numeric_signals += 1

    # Keyword and numeric confirmation
    if (
        any(kw in text for kw in investment_keywords) and
        not any(kw in text for kw in exclusion_keywords) and
        numeric_signals >= 1
    ):
        return "investimento"

    # Numeric-only rule: require ALL signals
    if numeric_signals == 3:
        return "investimento"

    return "custeio"


# --------------------------------------------------------------------------------------------
# Reclassify contracts
# --------------------------------------------------------------------------------------------

# Load data
df = pd.read_csv(CSV_PATH)

# Clean categorical columns
for col in CATEGORICAL_COLS:
    if col in df.columns:
        df[col] = df[col].fillna("missing").astype(str)

# Clean numeric columns
for col in NUMERIC_COLS:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Apply classification
df["cd_finalidade_corrected"] = df.apply(classify, axis=1)


# --------------------------------------------------------------------------------------------
# Save reduced output (contract_recipient_id + corrected classification)
# --------------------------------------------------------------------------------------------

# Save csv
output_df = df[["contract_recipient_id", "cd_finalidade_corrected"]].copy()
output_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
print(f"CSV saved to: {OUTPUT_PATH}")

# Print output
print("\n=== Corrected contract counts ===")
print(output_df["cd_finalidade_corrected"].value_counts())
