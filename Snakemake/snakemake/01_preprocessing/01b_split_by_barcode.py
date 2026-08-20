import anndata as ad

adata = ad.read_h5ad(snakemake.input[0])
prefix = snakemake.params.barcode_prefix

adata = adata[adata.obs_names.str.startswith(prefix)].copy()
adata.write_h5ad(snakemake.output[0])
