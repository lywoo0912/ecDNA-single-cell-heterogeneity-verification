# Aim3: Geneformer foundation model로 transcriptome에서 ecDNA score 예측
## L1: Frozen embedding UMAP 시각화
목적: Copy number 추정없이, 발현패턴(raw expression)만으로 세포의 ecDNA carrier정도를 시각적으로 구분할 수 있는지 탐색한다.<br>
("발현만으로 만든 UMAP 공간 안에서 ecDNA copy number가 높은 세포끼리 뭉쳐있는 영역이 존재하는가?")<br>

방법:<br>
1. Pretrained Geneformer(V2-140M, cancer-tuned)로 DM세포(27,783개)의 frozen embedding(768차원) 추출 - CN정보 없이 발현량만 입력으로 사용<br>
2. UMAP으로 2차원 축소<br>
3. 각 점(세포)을 inferCNV로 추정한 carrier_score(ecDNA amplicon locus CN, 연속값)으로 색칠<br>

<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/4184290e-853b-4078-9c1d-6cdf4055c095" /><br>
결과:<br>

- UMAP 상에서 carrier_score 색깔이 뚜렷한 클러스터로 분리되지 않고, 전체적으로 고르게 섞여서 분포함.<br>
- Embedding 품질 자체는 신뢰할 수 있음(Trustworthiness = 0.952 - 원래 768차원 구조를 왜곡없이 반영)<br>
- 즉, 발현기반 embedding의 2D 시각화만으로는 ecDNA 상태가 뚜렷이 구분되지 않음.<br>

해석:<br>
- UMAP의 2개 축은 이 데이터에서 가장 지배적인 변동(ex. batch)을 보여주는 것이기 때문에, ecDNA CN관련 정보는 768차원 전체에 약하게 분산되어 있을 수 있다.<br>
- 이게 지배적인 축을 차지할만큼 강하진 않더라도 Ridge regression처럼 768차원을 다 조합하는 모델은 그 약한 신호들을 모아서 높은 예측력을 만들어 낼 수 있다.<br>

[부가 탐색]: UMAP의 클러스터가 batch, 시퀀싱 depth, mitochondrial %, doublet score, cell cycle 중 무엇을 기준으로 만들어졌는지 확안했으나 모두 뚜렷한 대응관계를 찾지 못했다.<br>

## L2: Linear probing
목적: Frozen Geneformer embedding으로 세포별 ecDNA copy number 수준(연속값)을 얼마나 정밀하게 예측할 수 있는지 정량적으로 검증한다.<br>

방법:<br>
1. Train/Test을 barcode로부터 rep을 추출하여 batch(rep)단위로 분할(Train: rep1~rep6; 21,012개 / Test: rep7~rep8; 6,771개)<br>
2. StandardScaler로 768차원 embedding 수치 정규화<br>
3. GroupKFold를 이용해 Train set을 3분할하여 최적의 alpha값을 찾고 RidgeCV 훈련
4. Test set의 예측값과 실제 carrier_score 사이 상관관계 측정
