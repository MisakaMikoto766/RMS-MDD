# RMS-MDD

This is the code repository for the paper "RMS-MDD: A Comprehensive Benchmark for Medical Dialogue Diagnosis
in Real-World Medical Scenarios"

<img src="https://s2.loli.net/2024/09/19/ZR5L4XBMvcxHW1z.png" alt="models.png" style="zoom:80%;" />

## 📝Prepare the environment

### 😊Requirements

All codes are tested under Python 3.9.0, PyTorch 2.1.1.

numpy == 1.26.3

pillow == 10.2.0

scikit-learn ==1.5.1

transformers == 4.43.0

tqdm == 4.66.5

ms-swift == 2.2.5 

### 🛠️Guide to installing SWIFT

step1 Activate your conda environment

```bash
conda create --name swift python=3.9.0 && conda activate swift
```

step2 Clone SWIFT source code

```bash
git clone --branch v2.2.5 --single-branch https://github.com/modelscope/swift.git
```

step3 Install SWIFT

```bash
cd /swift && pip install -e .[llm]
```

## 📦Download the datasets

The datasets can be downloaded from the following URLs.

| Dataset     | URLs                                                         |
| ----------- | ------------------------------------------------------------ |
| DX-dialog   | https://drive.google.com/file/d/1CdanTdbDJSaZ7tmlF48si9qXQsK7_Po_/view?usp=sharing |
| IMCS-dialog | https://drive.google.com/file/d/1mhQuNvbgQNusPKTuiipQllm0TW3bDbuK/view?usp=sharing |
| MDD-dialog  | https://drive.google.com/file/d/1mhQuNvbgQNusPKTuiipQllm0TW3bDbuK/view?usp=sharing |

After the datasets are downloaded, please put each of them into a specified directory of the project.

## 🔖Preprocess datasets into a uniform formation

For different datasets, we provide the preprocessing code. You can run them to process all datasets into a uniform formation. 

```shell
python data_standard.py --dataset data_sample
```

The processed dataset can also be downloaded directly from [here](https://drive.google.com/file/d/1LXvLdXvF5HcX8OnJVmY5FQgVUfhXKj_z/view?usp=sharing).

Get the standard labels in the dataset.

```shell
python get_lables.py --dataset_dir dataset_directory
```

You can use the following commands to generate the required formats of large language models for different datasets.

```shell
python data_preprocess.py --dataset data_sample
```

# 💻Inference

-----------------------

You can inference the model with the following command:

```
bash ./deploy.sh model_type model_id_or_path
```

You can replace SYSTEM_PROMPT in inference.py with the corresponding instructions and perform inference.

```
bash ./run.sh dataset_file output_file
```

