import torch
import pandas as pd
import os
from tqdm import tqdm
from utils import make_prediction
from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizer, AutoConfig, GPTNeoForCausalLM

MODEL_ROOT = '.\\NormalizeTime'
SAVE_DIR = "saved_model"
CHECKED_MODEL = "pythia-70m_TimeSeries_9"
TOKENIZER = 'pythia-70m_TimeSeries_Tokenizer'
SAVE_PATH = os.path.join(MODEL_ROOT, SAVE_DIR)
BATCH_SIZE = 128
NER_OUTPUT_ROOT = ".\\upload_answer\\un_norm"
NER_OUTPUT_FILE = "answer.txt"
INFER_OUTPUT_ROOT = ".\\upload_answer\\norm"
INFER_OUTPUT_FILE = "answer.txt"

special_token_dict : dict = {
    "bos_token" : "<|endoftext|>",
    "sep_token" : "<|SEP|>", 
    "eos_token" : "<|END|>",
    "pad_token" : "<|PAD|>"
    }

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(f'Current Device = {device}')
TOKENIZER_FILE = os.path.join(SAVE_PATH, TOKENIZER)
print(f'Loading tokenizer from {TOKENIZER_FILE}')
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_FILE)
print(f'DONE!')
tokenizer.padding_side = 'left'
MODEL_FILE = os.path.join(SAVE_PATH, CHECKED_MODEL)
print(f'Loading Model from {MODEL_FILE}')
config = AutoConfig.from_pretrained(MODEL_FILE,
                                    bos_token_id=tokenizer.bos_token_id,
                                    eos_token_id=tokenizer.eos_token_id,
                                    pad_token_id=tokenizer.pad_token_id,
                                    sep_token_id=tokenizer.sep_token_id,
                                    output_hidden_states=False)
model : GPTNeoForCausalLM = AutoModelForCausalLM.from_pretrained(MODEL_FILE, 
                                                                 config = config).to(device)

valid_data = pd.read_csv(os.path.join(NER_OUTPUT_ROOT, NER_OUTPUT_FILE), sep='\t', names=['fid', 'phi', 'st_idx', 'ed_idx', 'content', 'normalized'])
ORG_LEN = len(valid_data)
input_data = valid_data[(valid_data['phi'] == "DATE") | (valid_data['phi'] == "TIME") | ((valid_data['phi'] == "DURATION"))]
valid_data = valid_data.drop(input_data.index)
input_data = input_data.reset_index()
valid_list = input_data['content']
outputs = []
with torch.no_grad():
    model.eval()
    for i in tqdm(range(0, len(valid_list), BATCH_SIZE), desc="Infering..."):
        datas = valid_list[i : i + BATCH_SIZE]
        outputs += make_prediction(model=model, tokenizer=tokenizer, datas=datas)
input_data['normalized'] = outputs
set_data = valid_data[valid_data['phi'] == 'SET']
valid_data = valid_data.drop(set_data.index, axis=0)
set_data['normalized'] = ["R2" for _ in range(len(set_data))]
result_df = pd.concat([valid_data, input_data, set_data], ignore_index=True)

assert len(result_df) == ORG_LEN, 'ERROR pls check'

with open(os.path.join(INFER_OUTPUT_ROOT, INFER_OUTPUT_FILE), 'w', encoding='utf-8')as f:
    for index, row in result_df.iterrows():
        if (pd.isna(row['normalized'])):
            result_str = f"{row['fid']}\t{row['phi']}\t{row['st_idx']}\t{row['ed_idx']}\t{row['content']}"
        else:
            result_str = f"{row['fid']}\t{row['phi']}\t{row['st_idx']}\t{row['ed_idx']}\t{row['content']}\t{row['normalized']}"
        f.write(result_str)
        f.write('\n')