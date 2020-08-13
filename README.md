# olist-datascience

*Data Science - Study of the olist ecommerce database using a decision tree classifier.*

* [Datasets](https://www.kaggle.com/olistbr/brazilian-ecommerce)

## Usability

*- Create a new environment for this project*

```bash
conda create --name olist-env python=3.8

source activate olist-env
```

*- Install library package*

```bash
pip install git+https://github.com/diegodamas/olist-datascience/tree/master/src.git
```

*- Upload Data*

```bash
python src/upload.py
```

*-Make an active base sale*

```bash
  python src/train/etl.py --date_init "2017-06-01" --date_end "2018-06-01"
```

*-Train model*

```bash
  python src/train/model.py --date_init "2017-06-01" --date_end "2018-06-01"
```

*-Predict*

```bash
  python src/predict/predict.py --date_init "2017-06-01" --date_end "2018-06-01"
```
