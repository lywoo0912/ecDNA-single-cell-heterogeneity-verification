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
Amplicon: chr8의 amplicon 좌표 내에 존재하는 COLO320DM, COLO320HSR 세포<br>
Control: chr8의 amplicon 좌표 밖의 세포<br>
<img width="550" height="350" alt="image" src="https://github.com/user-attachments/assets/bb425e3c-b841-440e-825a-05100fa54331" /><br>
- Amplicon이 Control보다 per-cell CN score가 더 큰 것을 확인할 수 있다.<br>

<img width="550" height="250" alt="image" src="https://github.com/user-attachments/assets/62206fe6-9523-47e1-8882-73029f08898a" /><br>
- 실제 amplicon영역 좌표에서 per-cell CN score가 peak를 찍는 것을 확인할 수 있다.<br>
---
✅ Step2에서 확보한 ecDNA amplicon 좌표에서 추정 CN이 실제로 spike하는 것을 확인했다.<br>
⚠️ 현재 Amplicon은 DM & HSR 세포 혼재상태. 실제로 DM 분산이 HSR 분산보다 큰 지 검증해야한다. -> Aim2<br>

### [Step5: CopyKAT & Robustness 검증]<br>
Robustness 검증 방법: 두 가지 도구의 DM세포 copy number 추정값을 correlation으로 비교<br>
- Pearson Correlation: 0.7779062<br>
- Spearman Correlation: 0.7486532<br>

✅ inferCNV와 CopyKAT의 DM 세포별 MYC amplicon 신호는 Pearson: 0.7779062, Spearman: 0.7486532로 강한 양의 상관관계를 보였다.
두 지표가 근접한 값을 보인다는 점은 이 관계가 소수 극단치에 좌우되지 않고 안정적임을 의미하며, 서로 다른 두 CN 추정 방법이 일관된 신호를 포착하고 있음을 뒷받침한다.<br>
⚠️ inferCNV과 CopyKAT의 DM세포에 대한 GMM check결과, 두 가지 방법 모두 Carrier/Non-carrier로 나뉘는 구간이 있다기보다는 연속분포 형태를 띄는 것으로 나타났다.<br>

   






