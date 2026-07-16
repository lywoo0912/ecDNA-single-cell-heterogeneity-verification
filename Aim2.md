# Aim2: Heterogeneity 정량화 & 가설 검증<br>
가설: ecDNA는 centromere 없이 무작위 분배되므로, ecDNA가 위치한 genomic locus의 세포 간 copy number 분산은 일반 chromosomal amplification locus보다 클 것이다.<br>
- Amplicon score: 각 세포의 amplicon genes에 대한 copy number 평균<br>
- Amplicon genes(15개): ["RP11-103H7.1", "RP11-103H7.2", "FAM84B", "RP11-89K10.1", "RP11-351C8.1", "PCAT1", "PCAT2", "CASC19", "CCAT1", "CASC8", "RP11-382A18.2", "POU5F1B", "CASC11", "MYC", "PVT1"]<br>
- Amplicon은 DM & HSR세포 혼재 상태 - DM세포: 27881개 / HSR세포: 34718개<br>
***
<img width="600" height="350" alt="image" src="https://github.com/user-attachments/assets/e91652e9-e170-4abd-8100-147d8b939440" /><br>
✅ DM-only의 y축 Density의 스케일은 0-3.5인 반면, HSR-only의 스케일은 0-6이므로 HSR세포의 CN값 밀도가 더 높고 분산은 더 작다는 것을 알 수 있다.<br>
✅ 히스토그램의 x축 amplicon score범위도 DM-only가 HSR-only보다 더 크기 때문에 DM세포의 ecDNA copy number 분산이 더 크다.<br>
***
<img width="600" height="350" alt="image" src="https://github.com/user-attachments/assets/84c72c0e-95c0-407b-aa89-b03f080ea227" /><br>
✅ Amplicon의 DM세포와 HSR세포를 나누어서 boxplot으로 보았을 때 DM-Amplicon의 박스크기(분산)가 HSR-Amplicon보다 더 큰 것을 볼 수 있다.<br>
✅ DM-Amplicon가 DM-Control의 boxplot보다 박스크기(분산)와 중앙값이 더 컸고, 이를 통해 amplicon 좌표 영역 내의 DM세포에서 ecDNA copy number가 더 높고 분산도 더 큰 것을 확인했다.<br>

| | DM-Amplicon | DM-Control | HSR-Amplicon | HSR-Control |
| --- | --- | --- | --- | --- |
| Mean | 1.111492 | 0.9973724 | 0.9253412 | 1.007498 |
| Var | 0.01383859 | 0.001879742 | 0.00459466 | 0.001400314 |


✅ Amplicon 영역 내 DM세포의 CN분산이 HSR세포보다 약 3배가량 더 큰 것으로 나타나 위의 가설을 검증하였다. 즉, amplicon 영역 내의 MYC locus(15개 유전자)의 copy number가 세포 별로 들어가있는 편차가 크고 이에 따라 ecDNA는 무작위로 딸세포로 분배되었다라는 사실을 확인할 수 있다.<br>
