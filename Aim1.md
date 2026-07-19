# Aim1: 세포별 ecDNA copy number 추정<br>
## [Steps]<br>
1. COLO320DM & COLO320HSR scRNA-seq 데이터 확보<br>
2. Amplicon Repository을 통한 Amplicon 좌표 확보<br>
3. Scanpy scRNA-seq 데이터 전처리<br>
4. inferCNV 실행 & Sanity check<br>
5. CopyKAT 실행 & 두 방법 일치도 확인<br>
---
### [Step1 & 2: 데이터 확보]<br>
COLO320DM & COLO320HSR scRNA-seq 데이터 cell x genes = (72049, 32739) 확보<br>
Amplicon 좌표: chr8	127437994	129010064, chr8	130278183	130286722 확보<br>

---
### [Step3: Scanpy 데이터 전처리]<br>
<전처리 내용><br>
1. filter_cells: 최소 2000개 이상의 유전자를 가진 세포만 남김<br>
2. filter_genes: 최소 20개 이상의 세포에 나타나는 유전자만 남김<br>
3. Mithocondrial QC: 미토콘드리아 비율이 높은 세포는 죽은 세포이므로 pct_counts_mt(미토콘드리아 비율) < 17.5 & n_genes_by_counts(검출된 유전자 수) > 2000 & total_counts(총 umi 카운트) > 10000로 필터링<br>
4. Scrublet 실행 및 threshold 조정: doublet score가 0.6이상인 세포 제거<br>
전처리 후 cell x genes = (62599, 25870)<br>
<img width="500" height="200" alt="image" src="https://github.com/user-attachments/assets/c1645d61-c661-4a6a-acc9-4b09e4317805" /><br>
<img width="500" height="200" alt="image" src="https://github.com/user-attachments/assets/3dc9e4da-a1f2-4129-bbab-d3e5537d4731" /><br>
---
### [Step4: inferCNV & Sanity Check: 이 locus에 실제로 증폭신호가 있는가?]<br>
<img width="600" height="400" alt="dm_chr8_amplicon_vs_dm_chr8)non_amplicon_boxplot" src="https://github.com/user-attachments/assets/a4d6358d-b16a-49c1-ac61-53a2d80d6c1a" />
<img width="550" height="250" alt="dm_chr8_profile" src="https://github.com/user-attachments/assets/72695d0a-92a3-451b-83f9-d202a1aa724b" />
<img width="600" height="500" alt="infer_dm_amplicon_score_distribution" src="https://github.com/user-attachments/assets/ad4a5afc-0e43-4c89-b477-e9f3500d73ac" />
<img width="600" height="500" alt="copykat_dm_amplicon_score_distribution" src="https://github.com/user-attachments/assets/eedbcf13-1f97-4ab8-b8a2-861fe1f7d412" />


