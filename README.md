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

#### 4. Results
---

​	The results of sTPB compared with baseline metrics are shown in the following table:

| user model | Best-fit parameters                      | $MSE_e$             | $MSE_q$             | Spearman's $\rho$   | Pearson's $r$       |
| :--------- | ---------------------------------------- | ------------------- | ------------------- | ------------------- | ------------------- |
| sDCG       | $b$=1.48 (0.02), $bq$=1.80 (0.01)         | 1.964               | 1.081               | 0.362               | 0.366               |
| sRBP       | $p$, $b$=0.85, 0.60                      | $\underline{0.531}$ | $\underline{0.251}$ | $\underline{0.385}$ | 0.385               |
| sINST      | $T$=2.78 (0.05),  $\kappa$=1.38 (0.04)   | 0.875               | 0.338               | 0.384               | $\underline{0.387}$ |
| sTPB       | $G$=0.77 (0.05), $C$=6.00,$\gamma$=0.095 | $\mathbf{0.253}$    | $\mathbf{0.044}$    | $\mathbf{0.407}$    | $\mathbf{0.410}$    |

#### 5. Quick Start
---

###### To use sTPB, run the script (run.sh) as follows:

```sh
python3 run.py --G_0 1.0 --C_0 6.0 --gamma 1.0  --bounded_rationality [0.25,10,0.25,10,4,7.5] --N 10
```





