library(yaml)

amplicons <- yaml::read_yaml(snakemake@input$amplicons)[[snakemake@params$cellline]]

gene_order <- read.table(file.path(snakemake@input$infer_10x, "gene_order.txt"), sep = "\t", header = FALSE, row.names = 1, col.names = c("gene", "chr", "start", "stop"))


get_amplicon_genes <- function(segs, gene_order) {
    in_amplicon <- rep(FALSE, nrow(gene_order))
    for (seg in segs) {
    in_amplicon <- in_amplicon |
        (gene_order$chr == seg["chr"] &
        gene_order$stop  >= as.numeric(seg["start"]) &
        gene_order$start <= as.numeric(seg["stop"]))
    }
    rownames(gene_order)[in_amplicon]
}

amplicon_genes <- list()
for (type_name in names(amplicons)) {
    for (amp_name in names(amplicons[[type_name]])) {
        amplicon_genes[[amp_name]] <- get_amplicon_genes(amplicons[[type_name]][[amp_name]], gene_order)
    }
}

#=================================================
# amplicon1_ecdna -> chr8 / amplicon2_linear -> chr13 / amplicon3_linear -> chr1 / amplicon4_linear -> chf2 염색체 전체 profile

amplicon_control_genes <- list()
for (type_name in names(amplicons)) {
    if (type_name != "ecdna") next

    for (amp_name in names(amplicons[[type_name]])) {
        segs <- amplicons[[type_name]][[amp_name]]
        chrs <- unique(sapply(segs, function(s) s$chr))
        chr_idx <- gene_order$chr %in% chrs
        amplicon_control_genes[[amp_name]] <- rownames(gene_order)[chr_idx & !(rownames(gene_order) %in% amplicon_genes[[amp_name]])]
    }
}

outdir <- snakemake@output[[1]]
dir.create(outdir, recursive=TRUE, showWarnings=FALSE)
infercnv_obj <- readRDS(file.path(snakemake@input$infercnv_dir, "15_no_subclustering.infercnv_obj"))
expr <- infercnv_obj@expr.data


for (amp_name in names(amplicon_genes)) {
  amplicon_genes[[amp_name]]   <- intersect(amplicon_genes[[amp_name]], rownames(expr))
}

amplicon_scores <- list()
for (amp_name in names(amplicon_control_genes)) {
  amplicon_control_genes[[amp_name]] <- intersect(amplicon_control_genes[[amp_name]], rownames(expr))

  amplicon_scores[[paste0(amp_name, "_score")]] <- colMeans(expr[amplicon_genes[[amp_name]], , drop=FALSE])
  amplicon_scores[[paste0(amp_name, "_control_score")]] <- colMeans(expr[amplicon_control_genes[[amp_name]], , drop=FALSE])
}


saveRDS(list(
    scores = amplicon_scores,
    genes = amplicon_genes),
 file.path(snakemake@output[[1]], "amplicon_scores.rds"))

# --- Aim1: inferCNV ecDNA score 분포 히스토그램 + GMM valley (carrier 분류 근거) ---
library(mclust)

infer_09 <- readRDS(file.path(snakemake@input$infercnv_dir, "09_apply_max_centered_expr_threshold.infercnv_obj"))
expr_09 <- infer_09@expr.data
ecdna_score_presmooth <- colMeans(expr_09[amplicon_genes[["amplicon1_ecdna"]], , drop=FALSE])

write.csv(data.frame(barcode=names(ecdna_score_presmooth), amplicon1_ecdna_score=as.numeric(ecdna_score_presmooth)), file.path(snakemake@output[[1]], "amplicon_ecdna_scores.csv"), row.names=FALSE)

png(file.path(outdir, paste0(snakemake@params$cellline, "_infercnv_ecdna_score_distribution.png")), width=900, height=600)
hist(
    ecdna_score_presmooth,
    breaks=100,
    freq=FALSE,
    main="inferCNV ecDNA amplicon score distribution (per-cell)",
    xlab="inferCNV centered expression score",
    col="grey85",
    border=NA
)
lines(density(ecdna_score_presmooth), col="red", lwd=2)
dev.off()

fit_ecdna <- Mclust(ecdna_score_presmooth, G=1:2)
png(file.path(outdir, paste0(snakemake@params$cellline, "_infercnv_ecdna_gmm_classification.png")), width=900, height=600)
plot(fit_ecdna, what = "classification")
dev.off()

saveRDS(fit_ecdna, file.path(outdir, "ecdna_score_gmm_fit.rds"))

# --- 염색체 전체 프로파일 (position vs 평균 CN, 앰플리콘 영역 빨간 음영) ---
plot_chr_profile <- function(chr_name, segs, out_png, main_title) {
  chr_genes <- rownames(gene_order)[gene_order$chr == chr_name]
  chr_genes <- intersect(chr_genes, rownames(expr))
  chr_order <- chr_genes[order(gene_order[chr_genes, "start"])]
  chr_mean  <- rowMeans(expr[chr_order, , drop = FALSE])
  chr_pos   <- gene_order[chr_order, "start"]

  png(out_png, width = 1200, height = 500)
  plot(chr_pos, chr_mean, type = "l",
       xlab = paste(chr_name, "position"), ylab = "mean relative CN (across cells)",
       main = main_title)
  for (seg in segs) {
    if (seg["chr"] == chr_name) {
      rect(as.numeric(seg["start"]), min(chr_mean), as.numeric(seg["stop"]), max(chr_mean),
           col = rgb(1, 0, 0, 0.15), border = NA)
    }
  }
    lines(chr_pos, chr_mean)
    dev.off()
}


for (amp_name in names(amplicon_control_genes)) {   
  segs <- amplicons[["ecdna"]][[amp_name]]
  chrs <- unique(sapply(segs, function(s) s$chr))

  for (chr_name in chrs) {
    out_png <- file.path(outdir, paste0(snakemake@params$cellline, "_", chr_name, "_profile.png"))
    plot_chr_profile(chr_name, segs, out_png, paste(snakemake@params$cellline, chr_name, "profile"))
  }
}