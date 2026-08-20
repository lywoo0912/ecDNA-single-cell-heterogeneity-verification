import scanpy as sc
import anndata as ad
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

emb_clcancer = pd.read_csv(os.path.join(snakemake.input.emb_clcancer, f"{snakemake.params.cellline}_emb_clcancer.csv"))
emb_cols = [c for c in emb_clcancer.columns if c not in ["Unnamed: 0.1", "Unnamed: 0", "barcode"]]
X = emb_clcancer[emb_cols].values

a = ad.AnnData(
    X=X,
    obs=pd.DataFrame({"barcode" : emb_clcancer["barcode"].values})
)
a.obs_names = a.obs["barcode"].values

# KNN + leiden
sc.pp.neighbors(a, use_rep="X", n_neighbors=15)
sc.tl.leiden(a, resolution=0.5, flavor="igraph", n_iterations=2, random_state=42)
sc.tl.umap(a, random_state=42)

# carrier_score(ecDNA score) 붙이기
carrier_df = pd.read_csv(os.path.join(snakemake.input.sanitycheck_dir, "amplicon_ecdna_scores.csv"))
carrier_map = carrier_df.set_index("barcode")["amplicon1_ecdna_score"]
a.obs["amplicon1_ecdna_score"] = a.obs_names.map(carrier_map)

# 좌: Leiden 클러스터, 우: ecDNA score — 같은 UMAP 좌표 위에서 비교
umap = sc.pl.umap(a, color=["leiden", "amplicon1_ecdna_score"], cmap="viridis", size=5, ncols=2, show=False, return_fig=True)
umap.savefig(snakemake.output.umap)

# 클러스터별 마커 유전자 
expr = sc.read_h5ad(snakemake.input.geneform_adata)
expr = expr[a.obs_names].copy()
expr.obs["leiden"] = a.obs["leiden"].values

sc.pp.normalize_total(expr, target_sum=1e4)
sc.pp.log1p(expr)
sc.tl.rank_genes_groups(expr, groupby="leiden", method="wilcoxon", n_genes=20)

for cl in expr.obs["leiden"].cat.categories:
    print(cl, list(expr.uns["rank_genes_groups"]["names"][cl][:15]))
    

#=====================================================================
#=====================================================================
# cell cycle score 계산 (표준 Tirosh et al. gene set)

s_genes = ['MCM5','PCNA','TYMS','FEN1','MCM2','MCM4','RRM1','UNG','GINS2','MCM6',
           'CDCA7','DTL','PRIM1','UHRF1','HELLS','RFC2','RPA2','NASP','RAD51AP1',
           'GMNN','WDR76','SLBP','CCNE2','UBR7','POLD3','MSH2','ATAD2','RAD51',
           'RRM2','CDC45','CDC6','EXO1','TIPIN','DSCC1','BLM','CASP8AP2','USP1',
           'CLSPN','POLA1','CHAF1B','BRIP1','E2F8']
g2m_genes = ['HMGB2','CDK1','NUSAP1','UBE2C','BIRC5','TPX2','TOP2A','NDC80','CKS2',
             'NUF2','CKS1B','MKI67','TMPO','CENPF','TACC3','FAM64A','SMC4','CCNB2',
             'CKAP2L','CKAP2','AURKB','BUB1','KIF11','ANP32E','TUBB4B','GTSE1',
             'KIF20B','HJURP','CDCA3','HN1','CDC20','TTK','CDC25C','KIF2C','RANGAP1',
             'NCAPD2','DLGAP5','CDCA2','CDCA8','ECT2','KIF23','HMMR','AURKA','PSRC1',
             'ANLN','LBR','CKAP5','CENPE','CTCF','NEK2','G2E3','GAS2L3','CBX5','CENPA']
s_genes = [g for g in s_genes if g in expr.var_names]
g2m_genes = [g for g in g2m_genes if g in expr.var_names]

sc.tl.score_genes_cell_cycle(expr, s_genes=s_genes, g2m_genes=g2m_genes)

# a(임베딩 UMAP 좌표)에서 좌표 가져오기
umap_coords = a[expr.obs_names].obsm["X_umap"]
leiden = expr.obs["leiden"].values
phase = expr.obs["phase"].values

# leiden UMAP 위에 각 클러스터 중심마다 dominant phase(%) 텍스트로 표시
fig, ax = plt.subplots(figsize=(8, 7))
sc.pl.umap(a, color="leiden", ax=ax, show=False, size=5)

for cl in expr.obs["leiden"].cat.categories:
    mask = leiden == cl
    cx, cy = umap_coords[mask, 0].mean(), umap_coords[mask, 1].mean()
    phase_pct = pd.Series(phase[mask]).value_counts(normalize=True) * 100
    dom_phase = phase_pct.idxmax()
    ax.text(cx, cy, f"{cl}: {dom_phase} ({phase_pct.max():.0f}%)",
            fontsize=10, fontweight="bold", ha="center",
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="black", boxstyle="round"))

plt.title("Leiden cluster별 dominant cell-cycle phase")
plt.show()
fig.savefig(snakemake.output.cellcycle_umap)

## graph(clusters) connectivity
sc.tl.paga(a, groups="leiden")
paga_fig, paga_ax = plt.subplots(figsize=(8, 7))
sc.pl.paga(a, color="leiden", ax=paga_ax, show=False)
paga_fig.savefig(snakemake.output.paga)
