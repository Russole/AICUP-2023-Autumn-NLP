# AICUP-2023-Autumn-NLP-隱私保護與醫學數據標準化競賽：解碼臨床病例、讓數據說故事   
### 隊伍:Team_4706
## 運行環境  
### 使用 Anaconda 建立環境 :
conda env create -f environments.yml  
conda activate AI_CUP_Fall  
### 安裝pytorch:
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

## 資料  
#### 子任務一
#### [資料下載網址](https://drive.google.com/file/d/1bHMaHu4DJlKLL4uS9KBW9aDWngNlL2zz/view?usp=sharing) 
請先下載資料並解壓縮，解壓縮後的檔案全部存放在./NER_Dataset資料夾中 
## 訓練 
#### 子任務一
運行debertav3-full-data-2-chatgpt-5-training.ipynb，會將./NER_Dataset中的資料讀取到模型進行訓練
#### 子任務二
請依序輸入以下指令，執行如下檔案
- python ./NormalizeTime/mockNomalizedTimeData.py
- python ./NormalizeTime/trainTransformer.py
 
## 預測
#### 子任務一
#### [權重下載網址](https://drive.google.com/file/d/138w6WqmUpF9DkZcPv_d0enoVVOEOkFCh/view?usp=sharing)  
請先下載權重並解壓縮，解壓縮後的檔案全部存放在./AI_CUP_3/infer_model/deberta-v3-large_full-data-2_gpt-5 資料夾中

連結有提供子任務一的模型權重  
- debertav3-post-ver3-infer.ipynb，產生的Infer資料會存在 ./upload_answer/NER
- Search_PHI.ipynb，找到的PHI資料會存在./Search_Phi_Result/FULL
- Ensemble_answer.ipynb，會將上述2個程式的結果連接在一起，並存放在./upload_answer/un_norm，此為最終子任務一的結果
#### 子任務二
#### [權重下載網址](https://huggingface.co/WenTee/NormalizeTimePythia-70m)
請先下載權重model.safetensors，將檔案存放在./NormalizeTime/saved_model/pythia-70m_TimeSeries_9資料夾中

連結有提供子任務二的模型權重  
請輸入以下指令，運算結果會存放在./upload_answer/norm，此為最終子任務二的結果
- python ./NormalizeTime/inferTransformer.py
