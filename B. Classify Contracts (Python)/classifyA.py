# --------------------------------------------------------------------------------------------
# This script defines a function to re-classify credit contracts into cost and investment
# categories (see Theoretical Framework). It inputs the contract file
# 'operacao_gleba_master', cleaned in STATA, and outputs a reduced re-classified file
# mapping contract_recipient_id to the corrected classification type A, 'classifyA'.
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# SETUP
# --------------------------------------------------------------------------------------------

# Dependencies
import pandas as pd
import unicodedata

# Path definitions
CSV_PATH = "/Users/carlotaloranlopez/Desktop/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/CONTRACT/operacao_gleba_master.csv"
OUTPUT_PATH = "/Users/carlotaloranlopez/Desktop/CREDIT_DEFOREST/DATA/DATA_CLEAN/CREDIT/CONTRACT/classifyA.csv"

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

# Thresholds for numeric indicators of investment (by ChatGPT)
LOAN_SIZE_THRESHOLD = 50000
PRED_PROD_THRESHOLD = 100000
FARM_AREA_THRESHOLD = 50

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
    "14": None
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
    Rules:
    - Default: custeio
    - Investimento if:
        - Program mapping enforces it, OR
        - Keywords indicate capital investment, OR
        - Numeric thresholds exceeded
    """

    # Program-based rule
    prog = str(row.get("cd_programa", "")).lower()
    mapped = program_mapping.get(prog, None)
    if mapped is not None:
        return mapped

    # Text-based rule
    parts = [str(row[col]) for col in CATEGORICAL_COLS if col in row]
    text = normalize_text(" ".join(parts))

    investment_keywords = [ # by ChatGPT
        "maquina", "trator", "implemento", "tecnologia",
        "reforma", "infraestrutura", "melhoria", "equipamento",
        "benfeitoria", "instalacao", "capital"
    ]

    if any(kw in text for kw in investment_keywords):
        return "investimento"

    # Numeric rules
    if (
        row.get("vl_parc_credito", 0) > LOAN_SIZE_THRESHOLD or
        row.get("vl_prev_prod", 0) > PRED_PROD_THRESHOLD or
        row.get("vl_area_informada", 0) > FARM_AREA_THRESHOLD
    ):
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

output_df = df[["contract_recipient_id", "cd_finalidade_corrected"]].copy()

output_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
print(f"CSV saved to: {OUTPUT_PATH}")

# Optional sanity check
print("\n=== Corrected contract counts ===")
print(output_df["cd_finalidade_corrected"].value_counts())
