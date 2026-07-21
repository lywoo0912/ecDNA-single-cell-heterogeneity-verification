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
<img width="550" height="250" alt="dm_chr8_profile" src="https://github.com/user-attachments/assets/72695d0a-92a3-451b-83f9-d202a1aa724b" /><br>
✅ chr8 부위의 유전자별 CN 추정값을 그래프로 나타낸 결과, AA 좌표 내 영역에서 실제로 spike가 있음을 확인했다.<br>
✅ ecDNA MYC locus에 실제로 증폭신호가 있다.<br>

---
### [Step5: CopyKAT 실행 & 두 방법 일치도 확인]<br>
inferCNV로 살행했을 때 나온 amplicon 영역 내 유전자 15개 중 CopyKAT 실행 결과와 겹치는 유전자(7개)로 correlation을 보았다.<br>
| Pearson | Spearman |
| --- | --- |
| 0.778 | 0.750 | <br>
- Pearson: 절대적인 값 자체가 얼마나 비례해서 움직이는가를 본다.<br>
- Spearman: 값의 절대적인 크기, 간격이 아닌 순위를 본다.<br>

✅ Pearson과 Spearman의 값이 비슷하게 높다는 것은 절대적인 CN값이 비슷하고, outlier에도 크게 영향을 받지 않았으며, 전반적인 순위/크기 관계가 일관된다는 것을 말한다.<br>
✅ 따라서, inferCNV와 CopyKAT의 CN 추정값이 높은 확률로 일치한다는 것을 확인했다.<br>

<br>
<img width="400" height="300" alt="infercnv_ecdna_presmooth" src="https://github.com/user-attachments/assets/b326bba4-a2d6-4796-aa83-b2c2118adbd9" />
<img width="400" height="300" alt="copykat_dm_amplicon_score_distribution" src="https://github.com/user-attachments/assets/eedbcf13-1f97-4ab8-b8a2-861fe1f7d412" /><br>
⚠️ Aim3 이후의 과정에서 DM세포를 ecDNA Carrier/Non-carrier로 나눈 정답 label이 필요하다.<br>
⚠️ inferCNV의 histogram에서는 Carrier/Non-carrier로 나눌만한 봉우리가 2개 발견된 반면, CopyKAT에서는 하나의 봉우리인 연속분포를 보였다.<br>
✅ inferCNV의 valley(-0.2765)를 경계로 CN score가 -0.2765보다 크면 Carrier, 작거나 같으면 Non-carrier로 분류하였다.



