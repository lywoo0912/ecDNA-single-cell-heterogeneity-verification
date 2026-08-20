import os
import pandas as pd
import scipy.io as sio
import scipy.sparse as sp
import anndata as ad
from pyensembl import EnsemblRelease


#1) barcodes / features / matrix gzip
def export_10x_files(adata, outdir):
    # 1. Count Matrix 저장 (genes x cells로 전치해서 10x 형식 맞춤)
    mtx_path = os.path.join(outdir, "matrix.mtx")
    sio.mmwrite(mtx_path, sp.csr_matrix(adata.X.T))

    # 2. barcode(세포 이름) 저장
    barcodes_path = os.path.join(outdir, "barcodes.tsv")
    pd.Series(adata.obs_names).to_csv(barcodes_path, index=False, header=False)

    # 3. feature(유전자 이름) 저장 — 3열 포맷
    features_path = os.path.join(outdir, "features.tsv")
    df_features = pd.DataFrame({
        'id': adata.var_names,
        'symbol': adata.var_names,
        'type': 'Gene Expression'
    })
    df_features.to_csv(features_path, sep='\t', index=False, header=False)

    # 4. 압축 (R의 Read10X()가 gzip 형식을 기대함)
    os.system(f"gzip -f {mtx_path}")
    os.system(f"gzip -f {barcodes_path}")
    os.system(f"gzip -f {features_path}")

    print("Done")


#2) cell_annotation txt파일
def export_cell_annotations(adata, outdir, cellline):
    ann_df = pd.DataFrame({
        "cell": adata.obs_names,
        "group": cellline
    })

    ann_path = os.path.join(outdir, "cell_annotations.txt")
    ann_df.to_csv(ann_path, sep="\t", index=False, header=False)

    print(f"세포 수: {len(ann_df)}")


#3) gene_order txt파일
def export_gene_order(adata, outdir, ensembl_release):
    data = EnsemblRelease(ensembl_release)

    gene_orders = []
    cnt = 0

    for gene_name in adata.var_names:
        try:
            genes = data.genes_by_name(gene_name)
            if genes:
                gene = genes[0]
                chr_name = "chr" + gene.contig
                start = gene.start
                end = gene.end
                gene_orders.append([gene_name, chr_name, start, end])
        except ValueError:
            cnt += 1
            pass

    print(f"매핑 실패한 유전자 수: {cnt} / {adata.n_vars}")

    gene_order_df = pd.DataFrame(gene_orders)
    gene_order_path = os.path.join(outdir, "gene_order.txt")
    gene_order_df.to_csv(gene_order_path, sep="\t", index=False, header=False)

    print(f"매핑된 유전자 수: {len(gene_order_df)}")
    

adata = ad.read_h5ad(snakemake.input[0])
outdir = snakemake.output[0]
os.makedirs(outdir, exist_ok=True)

export_10x_files(adata, outdir)
export_cell_annotations(adata, outdir, snakemake.params.cellline)
export_gene_order(adata, outdir, snakemake.params.ensembl_release)