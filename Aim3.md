# Aim3: Geneformer foundation model로 transcriptome에서 ecDNA score 예측
## L1: Frozen embedding UMAP 시각화
### [목적] Copy number 추정없이, 발현패턴(raw expression)만으로 나온 Geneformer embedding에서 세포의 ecDNA carrier정도를 시각적으로 구분할 수 있는지 탐색한다.<br>
("발현만으로 만든 UMAP 공간 안에서 ecDNA copy number가 높은 세포끼리 뭉쳐있는 영역이 존재하는가?")<br>
(UMAP 공간 자체는 발현량만으로 구성하고, carrier_score는 결과 검증을 위한 색칠 라벨로만 사용)<br>

### [방법]<br>
1. Pretrained Geneformer(V2-104M, cancer-tuned)로 DM세포(27,783개)의 frozen embedding(768차원) 추출 - CN정보 없이 발현량만 입력으로 사용<br>
2. UMAP으로 2차원 축소<br>
3. 각 점(세포)을 inferCNV로 추정한 carrier_score(ecDNA amplicon locus CN, 연속값)으로 색칠<br>

<img width="900" height="400" alt="leiden score" src="https://github.com/user-attachments/assets/cec73f70-23b9-498f-8654-dc565224e96f" /><br>
<img width="500" height="400" alt="phase_on_leiden" src="https://github.com/user-attachments/assets/d0c99f52-9d1d-4dfb-a88b-9ef66c7b81b0" />
<img width="500" height="400" alt="paga" src="https://github.com/user-attachments/assets/6cbf41a8-0754-46d6-8717-5a2a7ee6706c" />

### [결과]<br>
***Carrier_score plot***
- UMAP 상에서 carrier_score 색깔이 뚜렷한 클러스터로 분리되지 않고, 전체적으로 고르게 섞여서 분포함.<br>
- Embedding 품질 자체는 신뢰할 수 있음(Trustworthiness = 0.952 - 원래 768차원 구조를 왜곡없이 반영)<br>
- 즉, 발현기반 embedding의 2D 시각화만으로는 ecDNA 상태가 뚜렷이 구분되지 않음.<br>
---
***Leiden plot***
- 각 클러스터의 발현량 top rank genes를 wilcoxon test로 뽑아봤을 때, 8번 클러스터에서 MYC가 1등, 5번 클러스터에서 4개의 amplicon genes, 나머지 클러스터에서는 amplicon genes가 검출되지 않았다.<br>
- Leiden 9개 클러스터의 marker gene을 확인한 결과, 8개 클러스터(0, 1, 2, 3, 4, 6, 7, 8)가 표준 cell-cycle 유전자 세트(S-phase, G2M)와 일치하였고, PAGA connectivity graph도 G1->S->G2M 인접 구조로 실제 cell cycle 진행 순서를 따라가는 것을 보인다. -> UMAP/Leiden의 주된 클러스터링 축이 cell cycle임을 확인<br>
- 8번 클러스터는 phase 분석 결과 G2M 91%로 9개 클러스터 중 가장 순수한 cell-cycle 클러스터로 보임. 즉, MYC 1등 발현은 ecDNA copy number 때문이 아니라, G2M기에 선택적으로 활성화되는 전사 프로그램(CENPF/TOP2A/CCNB1)으로 인한 것으로 확인하였다.<br>
- ***<ins>5번 클러스터는 phase 비율이 42%로 9개 클러스터 중 가장 약하고 carrier_score도 나머지 클러스터 대비 유의하게 높다. cell cycle을 통제한 OLS Regression에서 carrier_score가 높은 것은 cell cycle과는 독립적으로 유의한 것으로 나타났으며, 5번 클러스터는 cell-cycle과 무관한 통계적으로 검증된 ecDNA-high subpopulation으로 해석하였다.</ins>***<br>


### [해석]<br>
- UMAP의 2개 축은 이 데이터에서 가장 지배적인 변동(ex. cell cycle)을 보여주는 것이기 때문에, ecDNA CN관련 정보는 768차원 전체에 약하게 분산되어 있을 수 있다.<br>
- carrier_score 자체도 cell cycle(S_score, G2M_score)로 설명되는 분산이 R<sup>2</sup>=0.003에 불과해, ecDNA CN 정보는 cell cycle 축과 독립적임을 확인하였다.<br>
- ecDNA CN 정보가 지배적인 축을 차지할만큼 강하진 않더라도 Ridge regression처럼 768차원을 다 조합하는 모델은 그 약한 신호들을 모아서 높은 예측력을 만들어 낼 수 있다.<br>
- <ins>[추가검증]: 이 가설은 cell-cycle 성분을 제거한 residual carrier_score에 대해 아래 L2의 동일한 Ridge pipeline을 재실행하여 검증하였다. 결과는 (Pearson: 0.799 -> 0.798, Spearman: 0.783 -> 0.782)으로 예측력이 원본 대비 거의 그대로 유지되었으므로, Ridge의 예측력은 cell-cycle을 경유한 confound가 아니라, 순수하게 ecDNA 특이적인 신호에서 나온 것임을 검증하였다.</ins><br>


---

## L2: Linear probing
### [목적]: Frozen Geneformer embedding으로 세포별 ecDNA copy number 수준(연속값)을 얼마나 정밀하게 예측할 수 있는지 정량적으로 검증한다.<br>

### [방법1]<br>
1. Train/Test을 barcode로부터 rep을 추출하여 batch(rep)단위로 분할(Train: rep1 ~ rep6; 21,012개 / Test: rep7 ~ rep8; 6,771개)<br>
2. StandardScaler로 768차원 embedding 수치 정규화<br>
3. GroupKFold를 이용해 Train set을 3분할하여 최적의 alpha값을 찾고 RidgeCV 훈련
4. Test set의 예측값과 실제 carrier_score 사이 상관관계 측정<br>

| Pearson correlation | 0.799 | 
| --- | --- |
| Spearman correlation | 0.783 |<br>

### [방법1 보강 - Ablation study]<br>
Amplicon genes(18개)을 제외하고 Geneformer tokenizing/embedding을 진행<br>
이유: 예측대상인 carrier_score는 MYC locus genes의 자체 발현량으로 계산된 값. Geneformer의 tokenizer는 세포 안 유전자들의 발현량을 순위로 정렬한다. 만약 MYC locus genes에 해당하는 유전자의 발현량이 가장 많다면 1순위로 책정할 것. 그러면 Test set에서도 MYC locus genes의 순위만 보고 carrier_score를 결정해버린다.<br>

"즉, 다른 유전자들의 발현 패턴을 종합적으로 분석한 것이 아니게 된다."<br>

| Pearson correlation | 0.794 |
| --- | --- |
| Spearman correlation | 0.778 |<br>

### [해석]<br>
: MYC locus genes을 제외했음에도 상관관계가 거의 그대로 유지된다. 이는 전사체 전반에 ecDNA copy number와 상관된 독립적인 signature가 분산되어 존재한다는 해석을 뒷받침한다.<br>
"즉, Geneformer embedding은 MYC/ecDNA locus 자체를 직접 보지 않고도, 나머지 발현 패턴만으로 CN 수준을 거의 동일하게 예측할 수 있었다."

--- 

### [종합 결론]
이 프로젝트의 결과는 DNA-level 데이터없이 기존에 쌓인 scRNA-seq 데이터만으로도 ecDNA 탐색 부담을 근사적으로 스크리닝할 수 있는 가능성을 시사한다. 이를 통해 대규모 public scRNA-seq atlas에서 ecDNA 후보를 저비용으로 찾아내는데 활용될 수 있다.<br>

다만, 지금은 COLO320DM이라는 하나의 cell line에 대해서만 결과를 보았다는 점이 한계이다. ecDNA를 포함한 세포의 scRNA-seq 데이터 자체를 구하는데 어려움이 있긴 하지만 여러 cell line들에 대해서의 검증이 필요하다.

