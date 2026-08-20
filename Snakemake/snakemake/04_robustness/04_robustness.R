library(data.table)

infercnv_obj <- readRDS(file.path(snakemake@input$infercnv_dir, "15_no_subclustering.infercnv_obj"))
expr <- infercnv_obj@expr.data

# 원본(step4_2_copykat.R)의 MYC 주변 하드코딩 15유전자 리스트
amplicon_genes <- c("RP11-103H7.1", "RP11-103H7.2", "FAM84B", "RP11-89K10.1",
                     "RP11-351C8.1", "PCAT1", "PCAT2", "CASC19", "CCAT1", "CASC8",
                     "RP11-382A18.2", "POU5F1B", "CASC11", "MYC", "PVT1")

infer_genes <- intersect(amplicon_genes, rownames(expr))
cat("inferCNV에 존재하는 amplicon 유전자:", length(infer_genes), "/", length(amplicon_genes), "\n")
infercnv_score <- colMeans(expr[infer_genes, , drop=FALSE])

outdir <- snakemake@output[[1]]
dir.create(outdir, recursive=TRUE, showWarnings=FALSE)

# copykat은 chunk1/chunk2로 나뉘어 있으므로 각각 읽어서 병합
copykat_score <- NULL
for (i in 1:2) {
    f <- file.path(snakemake@input$copykat, paste0(snakemake@params$cellline, "_chunk", i, "__copykat_raw_results_gene_by_cell.txt"))
    CNAmat <- fread(f, sep="\t", header=TRUE, data.table=FALSE)
    cell_cols <- 8:ncol(CNAmat)
    chunk_genes <- intersect(amplicon_genes, CNAmat$hgnc_symbol)
    rows <- CNAmat$hgnc_symbol %in% chunk_genes
    chunk_score <- colMeans(CNAmat[rows, cell_cols, drop=FALSE])
    copykat_score <- c(copykat_score, chunk_score)
}
cat("copykat 세포 수:", length(copykat_score), "\n")

common_cells <- intersect(names(infercnv_score), names(copykat_score))
cat("공통 세포 수:", length(common_cells), "\n")

x <- infercnv_score[common_cells]
y <- copykat_score[common_cells]

pearson_test <- cor.test(x, y, method="pearson")
spearman_test <- cor.test(x, y, method="spearman")
print(pearson_test)
print(spearman_test)

out_png <- file.path(outdir, paste0(snakemake@params$cellline, "_infercnv_vs_copykat_scatter.png"))
png(out_png, width=700, height=700)
plot(x, y,
     xlab = "inferCNV amplicon score",
     ylab = "CopyKAT amplicon score",
     main = paste(snakemake@params$cellline, ": inferCNV vs CopyKAT"),
     pch = 16, cex = 0.3, col = rgb(0, 0, 0, 0.15))
abline(lm(y ~ x), col = "red", lwd = 2)
dev.off()

saveRDS(list(pearson=pearson_test, spearman=spearman_test), file.path(outdir, "robustness_correlation.rds"))
