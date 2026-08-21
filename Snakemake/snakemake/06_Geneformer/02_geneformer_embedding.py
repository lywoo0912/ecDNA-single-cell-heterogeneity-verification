import os
from geneformer import TranscriptomeTokenizer, EmbExtractor
import anndata as ad
import pandas as pd

adata = ad.read_h5ad(snakemake.input.adata)
adata.obs["barcode"] = adata.obs_names
carrier_df = pd.read_csv(os.path.join(snakemake.input.sanitycheck_dir, "amplicon_ecdna_scores.csv"))
carrier_barcodes = set(carrier_df["barcode"])
print(len(carrier_barcodes))

intersect_adata = adata[adata.obs_names.isin(carrier_barcodes)].copy()
print(f'최종 사용 세포 수: {intersect_adata.n_obs}')
carrier_df_indexed = carrier_df.set_index("barcode")
score_cols = [c for c in carrier_df.columns if c != "barcode"]
for col in score_cols:
    intersect_adata.obs[col] = intersect_adata.obs_names.map(carrier_df_indexed[col])

intersect_adata.write_h5ad(snakemake.input.adata)

#==================================================================================
# Geneformer Tokenizer
input_dir = os.path.dirname(snakemake.input.adata)

tk = TranscriptomeTokenizer(
    custom_attr_name_dict={"barcode" : "barcode"},
    nproc=4,
    model_version="V2",
    special_token=True,
    model_input_size=4096,
    token_dictionary_file="/home/kkangne0912/ecdna/Snakemake/Geneformer/geneformer/token_dictionary_gc104M.pkl",
    gene_median_file="/home/kkangne0912/ecdna/Snakemake/Geneformer/geneformer/gene_median_dictionary_gc104M.pkl",
    gene_mapping_file="/home/kkangne0912/ecdna/Snakemake/Geneformer/geneformer/ensembl_mapping_dict_gc104M.pkl"
)

tk.tokenize_data(
    data_directory=input_dir,
    output_directory=snakemake.output.geneformer_tokenized,
    output_prefix=snakemake.params.cellline,
    file_format="h5ad"
)

# Geneformer embedding extract
embex = EmbExtractor(
    model_type="Pretrained",
    model_version="V2",
    emb_mode="cls",
    max_ncells=None,
    emb_layer=-1,
    emb_label=["barcode"],
    forward_batch_size=10,
    nproc=4,
    token_dictionary_file="/home/kkangne0912/ecdna/Snakemake/Geneformer/geneformer/token_dictionary_gc104M.pkl"
)

os.makedirs(snakemake.output.geneformer_embedding, exist_ok=True)

embs = embex.extract_embs(
    model_directory="/home/kkangne0912/ecdna/Snakemake/Geneformer/Geneformer-V2-104M_CLcancer",
    input_data_file=os.path.join(snakemake.output.geneformer_tokenized, f"{snakemake.params.cellline}.dataset"),
    output_directory=snakemake.output.geneformer_embedding,
    output_prefix=f"{snakemake.params.cellline}_emb_clcancer"
)
