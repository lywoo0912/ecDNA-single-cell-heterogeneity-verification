# ecDNA-single-cell-heterogeneity-verification

## Goal: 암세포 집단 안에서 ecDNA가 세포마다 얼마나 다르게 분포하는가를 single-cell transcriptome으로부터 정량화한다.<br>
### 🎯 [Background]<br>
암세포 안에는 ecDNA(extrachromosomal DNA)라는 정상 chromosome 밖에 떠다니는 원형 DNA조각이 있다.<br>
이는 MYC, EGFR, MYCN 같은 oncogene을 수십~수백 copy가지고 있어 암을 강하게 drive하는 요인으로 여겨진다.<br>
ecDNA는 centromere가 없어서 세포분열 때 딸세포에 랜덤하게 분배되는 성질을 가지고 있어 같은 tumor, 심지어 같은 cell line 안에서도 세포마다 ecDNA copy수가 천차만별이다. 이러한 "세포 간 불균일성(cell-to-cell heterogeneiry)"이 drug resistance와 tumor evolution의 핵심으로 최근 주목받고 있다.<br>
<br>
하지만 ecDNA를 세포 하나하나에서 직접 측정하려면 비싼 실험이 필요하기 때문에 scRNA-seq을 통해 copy number를 추정하는 도구를 활용하여 scRNA-seq만으로 ecDNA의 single-cell heterogeneiry를 얼마나 잡아낼 수 있을것인가를 알아보고자 한다.<br>

### 🎯 [Hypothesis]<br>
ecDNA는 centromere없이 무작위 분배되므로, ecDNA가 위치한 genomic locus의 세포 간 copy number(variance)은 일반 chromosomal amplification locus보다 클 것이다.<br>

### 🎯 [Aims]<br>
Aim1: 세포별 ecDNA copy number 추정<br>
Aim2: Heterogeneiry 정량화 & 가설 검증<br>
Aim3: Foundation model로 transcriptome에서 carrier예측 - 세포가 ecDNA를 많이 가졌는지를 copy number 추정없이 발현패턴만으로 알아낼 수 있는지를 Geneformer와 같은 foundation model로 탐색한다.<br>
