infer_09 <- readRDS(file.path(snakemake@input$infercnv_dir, "09_apply_max_centered_expr_threshold.infercnv_obj"))
expr_09 <- infer_09@expr.data

amplicon_data <- readRDS(file.path(snakemake@input$sanitycheck_dir, "amplicon_scores.rds"))
amplicon_genes <- amplicon_data$genes

amp_names <- names(amplicon_genes)[sapply(amplicon_genes, length) > 0]

scores <- list()
for (amp_name in amp_names) {
    score <- colMeans(expr_09[amplicon_genes[[amp_name]], , drop=FALSE])
    scores[[paste0(amp_name, "_var")]] <- var(score)
    scores[[paste0(amp_name, "_mean")]] <- mean(score)
}
vars <- sapply(amp_names, function(n) scores[[paste0(n, "_var")]])
means <- sapply(amp_names, function(n) scores[[paste0(n, "_mean")]])

outdir <- snakemake@output[[1]]
dir.create(outdir, recursive=TRUE, showWarnings=FALSE)

n_amp <- length(amp_names)
max_label_chars <- max(nchar(amp_names))
png_width <- max(900, n_amp * 220)          
bottom_margin <- max_label_chars * 0.5 + 2

out_png <- file.path(outdir, paste0(snakemake@params$cellline, "_heterogeneity_barplot.png"))
png(out_png, width=1200, height=600)
par(mfrow=c(1, 2), mar=c(7, 4, 4, 2))

bp1 <- barplot(vars, col = "steelblue", main = "Variance by amplicon", ylab = "variance", ylim=c(0, max(vars) * 1.2), las=2)
text(x = bp1, y = vars, labels = round(vars, 4), pos = 3)
bp2 <- barplot(means, col = "tomato", main = "Mean by amplicon", ylab = "mean", ylim=c(0, max(means) * 1.2), las=2)
text(x = bp2, y = means, labels = round(means, 4), pos = 3)

dev.off()


