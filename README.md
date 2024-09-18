# RMS-MDD

<img src="C:\Users\22331\AppData\Roaming\Typora\typora-user-images\image-20240918192327414.png" alt="image-20240918192327414" style="zoom:80%;" />

# Environment

All codes are tested under Python 3.9.0, PyTorch 2.1.1.

numpy == 1.26.3

pillow == 10.2.0

scikit-learn ==1.5.1

transformers == 4.43.0

tqdm == 4.66.5

ms-swift == 2.2.5 


# Dataset Download/Preprocess MIMIC-III 50Data
To download MIMIC-III dataset, you must first obtain its license. Once you have acquired the license and downloaded the dataset, please follow [caml-mimic](https://github.com/jamesmullenbach/caml-mimic) to preprocess the dataset.

You should obtain **train_full.csv**, **test_full.csv**, **dev_full.csv**, **train_50.csv**, **test_50.csv**, **dev_50.csv** after preprocessing.
Please put them under **sample_data/mimic3**.
Then you should use **preprocess/generate_data_new.ipynb** for generating json format dataset.

```
sample_data
|   D_ICD_DIAGNOSES.csv
|   D_ICD_PROCEDURES.csv
|   ICD9_descriptions (already in repo)
└───mimic3/
|   |   NOTEEVENTS.csv
|   |   DIAGNOSES_ICD.csv
|   |   PROCEDURES_ICD.csv
|   |   *_hadm_ids.csv (already in repo)
```

# Preprocess MIMIC-III rare 50 Dataset

Run command below and rare50 data will be created like mimic3-50l_xxx.json and xxx_50l.csv. paper

```python
python collectrare50data.py
```

# Modify constant

-----------------------

Modify constant.py : change DATA_DIR to where your preprocessed data located.

To enable wandb, modify wandb.init(project="PROJECTNAME", entity="WANDBACCOUNT") in run_coder.py.

# Word embedding

Please download [word2vec_sg0_100.model](https://github.com/aehrc/LAAT/blob/master/data/embeddings/word2vec_sg0_100.model) from LAAT.
You need to change the path of word embedding.

# Use our code
MIMIC-III 50:
```python
python main.py --version mimic3 --combiner lstm --rnn_dim 256 --num_layers 2 --decoder MultiLabelMultiHeadLAATV2 --attention_head 8 --attention_dim 512 --learning_rate 5e-4 --train_epoch 20 --batch_size 8 --gradient_accumulation_steps 8 --xavier --main_code_loss_weight 0.0 --rdrop_alpha 5.0 --est_cls 1  --term_count 8  --sort_method random --neg_sample_K 1024 --right_drop 0.4
```

MIMIC-III rare 50：

```python
python test_main.py --version mimic3 --combiner lstm --rnn_dim 256 --num_layers 2 --decoder MultiLabelMultiHeadLAATV2 --attention_head 8 --attention_dim 512 --learning_rate 5e-4 --batch_size 8 --gradient_accumulation_steps 8 --xavier --main_code_loss_weight 0.0 --rdrop_alpha 5.0 --est_cls 1  --term_count 8  --sort_method random --model_path ./model_best_path
```



