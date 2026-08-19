## Required Data & Setups
### 1. COLO320 scRNA-seq Raw data (1.2GB)
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE160148<br>
- matrix.mtx.gz / barcode.tsv.gz / features.tsv.gz 다운로드 후 하나의 폴더로 묶음 <br>
- config.yaml의 colo320_raw_10x에 폴더경로 지정<br>

### 2. Geneformer 설치 (2.4GB)
~~~bash
git lfs install
git clone https://hugginface.co/ctheodoris/Geneformer
~~~

### 3. pyensembl release 75(GRch37/hg19) 주석 데이터 (1.2GB)
~~~bash
pyemsembl install --release 75 --species human
~~~

### 4. Conda env
본 Snakemake pipeline은 두 개의 conda 환경을 사용<br>

**Python(python_env) - Scanpy 전처리, Geneformer 관련 스크립트**<br>
**R(r_env) - inferCNV, copyKAT, 통계/시각화 스크립트**

