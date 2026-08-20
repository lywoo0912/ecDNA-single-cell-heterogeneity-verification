library(infercnv)
library(Seurat)

raw <- Read10X(data.dir=snakemake@input$infer_10x)
out_dir <- snakemake@output[[1]]

infercnv_obj <- CreateInfercnvObject(
    raw_counts_matrix=raw,
    annotations_file=file.path(snakemake@input$infer_10x, "cell_annotations.txt"),
    delim="\t",
    gene_order_file=file.path(snakemake@input$infer_10x, "gene_order.txt"),
    ref_group_names=NULL
)

infercnv_obj <- infercnv::run(
    infercnv_obj,
    cutoff=0.1,
    out_dir=out_dir,
    num_threads=10,
    analysis_mode="samples",
    cluster_by_groups=FALSE,
    denoise=TRUE,
    HMM=FALSE,
    plot_steps=FALSE,
    output_format="png"
)

