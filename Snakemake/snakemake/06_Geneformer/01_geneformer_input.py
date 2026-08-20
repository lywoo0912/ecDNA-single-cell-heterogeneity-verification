from pyensembl import EnsemblRelease
import anndata as ad
import numpy as np

# geneformer input 형식 맞추기
adata = ad.read_h5ad(snakemake.input.adata)
data = EnsemblRelease(snakemake.params.ensembl_release)

ensembl_ids = []
for gene_name in adata.var_names:
    try:
        genes = data.genes_by_name(gene_name)
        ensembl_ids.append(genes[0].gene_id if genes else None)
    except ValueError:
        ensembl_ids.append(None)

adata.var["ensembl_id"] = ensembl_ids
n_before = adata.n_vars
adata = adata[:, adata.var["ensembl_id"].notna()].copy()
print(f"Ensembl ID 매핑 실패로 제거된 유전자 수: {n_before - adata.n_vars}")

adata.obs["n_counts"] = np.array(adata.layers["counts"].sum(axis=1)).flatten()
adata.write_h5ad(snakemake.output.geneform_adata, compression="gzip")

