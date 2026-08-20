import anndata as ad
import scanpy as sc
import matplotlib.pyplot as plt

adata = ad.read_h5ad(snakemake.input[0])

adata.var_names_make_unique()
sc.pp.filter_cells(adata, min_genes=2000)
sc.pp.filter_genes(adata, min_cells=20)

adata.var["mt"] = adata.var_names.str.startswith("MT-")
sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], percent_top=None, log1p=False, inplace=True)

# "n_genes_by_counts", "total_counts", "pct_counts_mt" 바이올린 플롯 그리기
violin = sc.pl.violin(adata, ["n_genes_by_counts", "total_counts", "pct_counts_mt"], jitter=0.4, multi_panel=True, show=False)
violin.savefig(snakemake.output.violin)

# histogram, scatter 플롯 그리기
f, ax = plt.subplots(1, 3, figsize=(30, 10))
ax[0].hist(adata.obs["total_counts"])
ax[0].set_xlabel("Total Counts")
ax[0].set_ylabel("Frequency")

ax[1].hist(adata.obs["n_genes_by_counts"])
ax[1].set_xlabel("Number of genes")
ax[1].set_ylabel("Frequency")

scatter = ax[2].scatter(adata.obs["total_counts"],
              adata.obs["n_genes_by_counts"],
              c=adata.obs["pct_counts_mt"],
              cmap="viridis",
              s=10)
ax[2].set_xlabel("Total Counts")
ax[2].set_ylabel("Number of genes")
plt.colorbar(scatter, ax=ax[2], label="pct_counts_mt")

f.savefig(snakemake.output.histscatter)

# Mitochondrial scatter plot 그리기
mito_scatter = sc.pl.scatter(adata, x="total_counts", y="pct_counts_mt", show=False)
mito_scatter.figure.savefig(snakemake.output.mito_scatter) # type: ignore

# total_counts, n_genes_by_counts, Mitochondrial QC
adata = adata[(adata.obs.n_genes_by_counts > 3000) &
              (adata.obs.pct_counts_mt < 17.5) &
              (adata.obs.total_counts > 10000), :].copy()

adata.layers["counts"] = adata.X.copy()

# scrublet QC(doublet 제거, score>=0.6 수동 cutoff)
sc.pp.scrublet(adata, expected_doublet_rate=0.1)
scrublet_plot = sc.pl.scrublet_score_distribution(adata, show=False, return_fig=True)
scrublet_plot.savefig(snakemake.output.scrublet)

adata.obs["predicted_doublet"] = adata.obs["doublet_score"] >= 0.6
adata = adata[~adata.obs["predicted_doublet"]].copy()
adata.write_h5ad(snakemake.output.adata)
