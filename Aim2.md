# Aim2: Heterogeneity 정량화 & 가설 검증<br>
> **가설: ecDNA는 centromere 없이 무작위 분배되므로, ecDNA가 위치한 genomic locus의 세포 간 copy number 분산은 일반 chromosomal amplification locus보다 클 것이다.**<br>

<img width="600" height="450" alt="dm_cell_ecdna_vs_linear_amplification" src="https://github.com/user-attachments/assets/cca91799-d7a1-4e96-9ea5-a2bb5d89e4b4" /><br>
- amplicon1_ecDNA: ['chr8:127437994-129010064', 'chr8:130278183-130286722']<br>
- amplicon2_linear: ['chr13:72865257-74155264']<br>
- amplicon3_linear: ['chr1:149609621-150774220']<br>
- amplicon4_linear: ['chr2:127156013-127674680', 'chr2:127677272-131355936']<br>

**🚩 DM세포의 Amplification은 ecDNA 구간, 3가지 linear amplification 구간이 있다.**<br>
**🚩 ecDNA구간의 copy number분산과 각각의 linear amplification구간의 copy number분산을 비교하였다.**<br>

<img width="450" height="450" alt="step5_variance_barplot_presmooth" src="https://github.com/user-attachments/assets/b5df7aca-9016-461c-b102-336aa4fc8040" /><br>


✅ ecDNA의 CN분산이 amplicon2_linear의 약 1.56배, amplicon3_linear의 약 6.58배, amplicon4_linear의 약 6.99배이다.<br>
✅ 따라서, ecDNA가 위치한 genomic locus의 CN 분산이 일반 chromosomal amplification locus의 CN 분산보다 크다는 것이 증명되었다.<br>
⚠️ 추가적으로 왜 amplicon2_la는 amplicon3_la, amplicon4_la에 비해서 큰 분산을 가지는지 알아볼 필요가 있다.



