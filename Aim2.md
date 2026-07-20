# Aim2: Heterogeneity 정량화 & 가설 검증<br>
> 가설: ecDNA는 centromere 없이 무작위 분배되므로, ecDNA가 위치한 genomic locus의 세포 간 copy number 분산은 일반 chromosomal amplification locus보다 클 것이다.<br>
- amplicon1_ecDNA: ['chr8:127437994-129010064', 'chr8:130278183-130286722']<br>
- amplicon2_linear: ['chr13:72865257-74155264']<br>
- amplicon3_linear: ['chr1:149609621-150774220']<br>
- amplicon4_linear: ['chr2:127156013-127674680', 'chr2:127677272-131355936']<br>

**DM세포의 Amplification은 ecDNA 구간, 3가지 linear amplification 구간이 있다.**<br>
**ecDNA구간의 copy number분산과 각각의 linear amplification구간의 copy number분산을 비교하였다.**<br>

<img width="450" height="450" alt="step5_variance_barplot" src="https://github.com/user-attachments/assets/41f69419-8621-424e-baf7-d75cd232d9b2" /><br>

✅ Amplicon3_linear와 Amplicon4_linear는 ecDNA보다 분산이 더 작으므로 위의 가설이 증명되었다.<br>
⚠️ 하지만, Amplicon2_linear는 ecDNA보다 CN분산이 컸다. 이는 가설과는 반대되는 현상이다.<br>


