import gzip
import scipy.io as sio
import anndata as ad
import pandas as pd

path = snakemake.params.raw_10x


def header_skiprows(fname):
    # GEO 원본 barcodes.tsv.gz/features.tsv.gz에 "x" 헤더 줄이 섞여있는 경우가 있음
    # (matrix.mtx.gz의 세포/유전자 수와 맞지 않게 됨) -> 있으면 1줄 건너뛰고 읽음
    with gzip.open(fname, "rt") as f:
        first_line = f.readline().strip()
    return 1 if first_line in ("x", "\tx") else 0


mat = sio.mmread(f"{path}/matrix.mtx.gz").T.tocsr()
barcodes = pd.read_csv(f"{path}/barcodes.tsv.gz", header=None, sep="\t",
                        skiprows=header_skiprows(f"{path}/barcodes.tsv.gz"))[0].values
features = pd.read_csv(f"{path}/features.tsv.gz", header=None, sep="\t",
                        skiprows=header_skiprows(f"{path}/features.tsv.gz"))

adata = ad.AnnData(X=mat)
adata.obs_names = barcodes
adata.var_names = features[1].values
adata.var["gene_index"] = features[0].values

adata.write_h5ad(snakemake.output[0])
