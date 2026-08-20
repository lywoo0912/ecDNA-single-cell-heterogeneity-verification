library(copykat)
library(Seurat)
# ---------------------------------------------------------------
# copykat 1.2.5 버그 패치: cell.line="yes" (pure cell line mode) 사용 시
# baseline.synthetic()이 expr.relat은 data.frame()으로 감싸면서 barcode의
# "-"를 "."로 바꿔버리는데, cl(클러스터 할당)의 이름은 그대로 둬서
# 이후 이름 매칭(names(CL) %in% colnames(norm.mat.relat))이 전부 실패하고
# CL이 빈 벡터가 되어 "Error in min(clu):max(clu)"로 터짐.
# check.names=FALSE로 이름 변형을 막아서 수정.
# ---------------------------------------------------------------

baseline.synthetic.patched <- function(norm.mat=norm.mat, min.cells=10, n.cores){
  d <- parallelDist::parDist(t(norm.mat), threads = n.cores)
  km <- 6
  fit <- hclust(d, method="ward.D2")
  ct <- cutree(fit, k=km)

  while(!all(table(ct)>min.cells)){
    km <- km -1
    ct <- cutree(fit, k=km)
    if(km==2){
      break
    }
  }

  expr.relat <- NULL
  syn <- NULL
  for(i in min(ct):max(ct)){
    data.c1 <- norm.mat[, which(ct==i)]
    sd1 <- apply(data.c1,1,sd)
    set.seed(123)
    syn.norm <- sapply(sd1,function(x)(x<- rnorm(1,mean = 0,sd=x)))
    relat1 <- data.c1 -syn.norm
    expr.relat <- rbind(expr.relat, t(relat1))
    syn <- cbind(syn,syn.norm)
    i <- i+1
  }

  reslt <- list(data.frame(t(expr.relat), check.names = FALSE), data.frame(syn), ct)
  names(reslt) <- c("expr.relat","syn.normal", "cl")

  return(reslt)
}
assignInNamespace("baseline.synthetic", baseline.synthetic.patched, ns = "copykat")


#===================================================

outdir <- snakemake@output[[1]]
raw <- Read10X(data.dir = snakemake@input[[1]])

dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
setwd(outdir)

# ---------------------------------------------------------------
# 2 chunk로 나눠서 각각 copykat 실행
# (cell.line="yes"가 큰 세포 수에서 baseline 추정이 무거워지는 걸 완화)
# ---------------------------------------------------------------
n.chunks <- 2
set.seed(42)
cell.order <- sample(colnames(raw))
chunk.id <- cut(seq_along(cell.order), breaks = n.chunks, labels = FALSE)

for (i in seq_len(n.chunks)) {
  chunk.cells <- cell.order[chunk.id == i]
  raw.chunk <- as.matrix(raw[, chunk.cells])

  # zero-variance 유전자 검증 
  var_by_gene <- apply(raw.chunk, 1, var)
  n_zero_var <- sum(var_by_gene == 0, na.rm = TRUE)
  n_na_var   <- sum(is.na(var_by_gene))
  cat("chunk", i, "- 세포 수:", ncol(raw.chunk),
      "/ zero-variance 유전자:", n_zero_var,
      "/ NA-variance 유전자:", n_na_var, "\n")

  bad_genes <- names(var_by_gene)[is.na(var_by_gene) | var_by_gene == 0]
  if (length(bad_genes) > 0) {
    cat("  ->", length(bad_genes), "개 유전자 제거 후 진행\n")
    raw.chunk <- raw.chunk[!(rownames(raw.chunk) %in% bad_genes), ]
  }

  copykat.test <- copykat(
      rawmat=raw.chunk,
      id.type="S",
      ngene.chr=5,
      win.size=25,
      KS.cut=0.1,
      cell.line="yes",
      plot.genes=FALSE,
      genome="hg20",
      n.cores=8,
      sam.name=paste0(snakemake@params$cellline, "_chunk", i, "_")
  )

  rm(copykat.test)
  gc()
}

