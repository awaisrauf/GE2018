# Predicting 2018 Pakistani Election using a Novel Rigged Model
<p align="center">
  <img src="https://raw.githubusercontent.com/awaisrauf/GE2018/master/imgs/map.jpg" alt="prediction"  />
 
  ```
  Election results as predicted by this model before elections vs original results.
  ```
</p>

## Introduction

This repository contains code for the election prediction model that was used to predict 2018's general election of Pakistan and won first prize in nation-wide data science competiton. Paper based on this model is accepted in the special issue of Spriger's journal on Big Data and Politics. Find more about this model [here](https://awaisrauf.github.io/election_prediction).
<p align="center">
  <img src="https://raw.githubusercontent.com/awaisrauf/GE2018/master/imgs/cermony.jpg" alt="cermony"  />
</p>


## Prerequisites

* scipy 0.18.1
* matplotlib 2.0.0
* pandas 0.19.2
* tqdm 4.28.1
* numpy 1.11.3
* bayesian_optimization 0.6.0
* thesis 0.0.01

## License

This repository is licensed under the terms of the GNU AGPLv3 license.

## How to run the code
```
cd GE2018
pip install -r requirements.txt
python main.py
```


## Reference
Please cite this.
```
@article{awais2019leveraging,
  title={Leveraging big data for politics: predicting general election of Pakistan using a novel rigged model},
  author={Awais, Muhammad and Hassan, Saeed-Ul and Ahmed, Ali},
  journal={Journal of Ambient Intelligence and Humanized Computing},
  pages={1--9},
  year={2019},
  publisher={Springer}
}
```
