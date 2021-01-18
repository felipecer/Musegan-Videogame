# Musegan-Videogame

## Description

This is a replica of MuseGAN, a Deep Learning model to generate multitrack music. We trained this model using video game music and using Pytorch.

Follow this [link](https://github.com/salu133445/musegan) to the original content. 

You can find more video game music at https://www.vgmusic.com/

Brief description files and folders.

* td-dataset: dataset in midi format.
* td-dataset-preprocesado: dataset in npz format. It contains a subset of td-dataset according to the criteria described in MuSnesGan.ipynb

## Train this model
If you wish to train this model, run the code on MuSnesGan.ipynb feeding it with the td-dataset provided or your own generated dataset.

## Generate your own dataset

### Download more tracks.

If you want to download aditional tracks feel free to use our webscrapping script (it only works for [VGMusic](https://www.vgmusic.com/) webpage).

### Prepare new training data
  * Use generar_info_csv.py to generate a csv containing general information about the midi files, such as the time signature and time signature changes.
  * Drop items on the generated csv that don't meet the criteria for data preprocessing and save it to a csv file. For more information about data preprocessing refer to the original repo.
  * Run preprocess.py to generate the dataset (it needs the aforementioned csv to generate new files) 
