## A session measure based on the Theory of Planned Behavior (*TPB*)
---

#### 1. Introduction
---

######      We propose a novel user model based on TPB for multi-query sessions, namely sTPB. This repository contains the source-code of the Python-based implementation of sTPB.

#### 2. Requirements
---

- ######  python>=3.0

- ###### numpy == 1.25.2

- ###### sklearn == 1.11.2

- ###### json == 2.0.9

#### 3. Data Preparation
---

###### 	 Preprocess the dataset TianGongQref into the the following format:

```json
{
        "session_id": 215,
        "max_query_rank": 3.0,
        "satisfaction": 4,
        "expertise": 2,
        "success": 4,
        "trigger": 0,
        "queries": [
            {
                "query_id": 2068,
                "satisfaction": 3,
                "max_stop_rank": 2,
                "rel_list": [
                    0,
                    2,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ]
            },
            {
                "query_id": 2069,
                "satisfaction": 3,
                "max_stop_rank": 2,
                "rel_list": [
                    0,
                    2,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ]
            },
            {
                "query_id": 2077,
                "satisfaction": 4,
                "max_stop_rank": 2,
                "rel_list": [
                    0,
                    3,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ]
            }
        ]
    }
```

#### 4. Parameter Settings for sTPB Framework

The performance gains are computed via linear normalization, with the unit cost set to 1.0. We recommend the following default parameter configurations:

R₁ = 10, R₂ = 1

b₁ = 0.5, b₂ = 0.5

For the two expectation management modes:

- Risk-seeking mode: R₃ = 10

- Risk-averse mode: R₃ = 20

- b₃ = 5

These values serve as default settings for the sTPB model and can be further adjusted based on specific application requirements.

#### 5. Results
---

​	The results of sTPB compared with baseline metrics are shown in the following table:

| user model | Best-fit parameters                      | $MSE_e$             | $MSE_q$             | Spearman's $\rho$   | Pearson's $r$       |
| :--------- | ---------------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| sDCG       | $b$=1.50 (0.02), $bq$=2.10 (0.01)         | 1.698               | 0.887               | 0.362               | 0.365               |
| sRBP       | $p$, $b$=0.90, 0.75                      | $\underline{0.692}$ | $\underline{0.332}$ | 0.395 | 0.398        |
| sINST      | $T$=2.64 (0.05),  $\kappa$=1.30   | 0.875               | 0.849               | $\underline{0.397}$         | $\underline{0.401}$ |
| sTPB       | $G$=2.10 (0.12), $C$=12.50, $\gamma$=0.045 | $\mathbf{0.241}$    | $\mathbf{0.035}$    | $\mathbf{0.414}$    | $\mathbf{0.418}$    |

#### 6. Quick Start
---
 
###### To use sTPB, run the script (run.sh) as follows:  

```sh
python3 run.py --G_0 2.5 --C_0 10.0 --gamma 0.1  --bounded_rationality [0.25,10,0.25,1,5,-10,20] --N 10
```





