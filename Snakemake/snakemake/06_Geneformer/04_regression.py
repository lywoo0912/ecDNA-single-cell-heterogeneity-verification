import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import RidgeCV
from scipy.stats import pearsonr, spearmanr


emb_clcancer = pd.read_csv(os.path.join(snakemake.input.emb_clcancer, f"{snakemake.params.cellline}_emb_clcancer.csv"))
carrier_df = pd.read_csv(os.path.join(snakemake.input.sanitycheck_dir, "amplicon_ecdna_scores.csv"))

merged = emb_clcancer.merge(carrier_df[['barcode', 'amplicon1_ecdna_score']], on="barcode", how="inner")
print(len(merged))

emb_cols = [c for c in emb_clcancer.columns if c not in ["Unnamed: 0.1", "Unnamed: 0", "barcode"]]
X = merged[emb_cols].values
y = merged["amplicon1_ecdna_score"].values

merged["rep"] = merged["barcode"].str.extract(r"(rep\d+)")

all_reps = sorted(merged["rep"].unique())
test_reps = all_reps[-2:]
train_reps = [r for r in all_reps if r not in test_reps]

train_barcode = merged["rep"].isin(train_reps).values
test_barcode = merged["rep"].isin(test_reps).values

X_train, y_train = X[train_barcode], y[train_barcode]
X_test, y_test = X[test_barcode], y[test_barcode]
groups_train = merged.loc[train_barcode, "rep"].values

print("train 세포 수:", len(X_train), "test 세포 수:", len(X_test))

#=================================================================
#=================================================================
# RidgeCV Regression

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

cv_splits = list(GroupKFold(n_splits=3).split(X_train_scaled, y_train, groups=groups_train))
ridge = RidgeCV(alphas=[0.1, 1.0, 10.0, 100.0], cv=cv_splits)
ridge.fit(X_train_scaled, y_train)

y_pred = ridge.predict(X_test_scaled)
pearson, _ = pearsonr(y_test, y_pred)
spearman, _ = spearmanr(y_test, y_pred)

print(f"Pearson correlation: {pearson:.3f} / Spearman correlation: {spearman:.3f}")
print("Alpha:", ridge.alpha_)

# pearson, spearman 수치 barplot으로 그리기
metrics = ["Pearson", "Spearman"]
values = [pearson, spearman]

plt.figure(figsize=(5, 5))
bars = plt.bar(metrics, values, color=["steelblue", "tomato"])
plt.ylim(0, 1)
plt.ylabel("correlation coefficient")
plt.title(f"{snakemake.params.cellline}: Geneformer embedding -> ecDNA score (Ridge)")
for bar, v in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width() / 2, v, f"{v:.3f}", ha="center", va="bottom")
plt.tight_layout()
plt.savefig(snakemake.output[0])