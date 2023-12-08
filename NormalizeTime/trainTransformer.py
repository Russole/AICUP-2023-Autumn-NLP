import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, GPTNeoXForCausalLM, AutoConfig
from tqdm import tqdm
import pickle
from torchdataset import GPTDataset
import os
import math

torch.cuda.empty_cache()
special_token_dict : dict = {
    "bos_token" : "<|endoftext|>",
    "sep_token" : "<|SEP|>", 
    "eos_token" : "<|END|>",
    "pad_token" : "<|PAD|>"
    }
ROOT = ".\\NormalizeTime"
EXTENDSION = '.txt'
BATCH_SIZE = 32
SAVE_PATH = os.path.join(ROOT, 'saved_model')
EPOCHS = 10
PRETRAIN_MODEL_NAME = "EleutherAI/pythia-70m"
CACHE_PATH = os.path.join(ROOT, 'cache_model')
MODEL_NAME = None
if MODEL_NAME is None and "/" in PRETRAIN_MODEL_NAME:
    MODEL_NAME = PRETRAIN_MODEL_NAME.split('/')[1]
else:
    MODEL_NAME = PRETRAIN_MODEL_NAME
MODEL_NAME = f"{MODEL_NAME}_SpecialTimeSeries"
TRAIN_ROOT = os.path.join(ROOT, "TrainingData")

print(f"Current ROOT = {ROOT}")
print(f"BATCH_SIZE = {BATCH_SIZE}")
print(f"EPOCHS = {EPOCHS}")
print(f"Pretrain Model Name = {PRETRAIN_MODEL_NAME}")
print(f"Check point model root = {SAVE_PATH}")
print(f"Cache path = {CACHE_PATH}")
print(f"Check point model name = {MODEL_NAME}")

train_datas = []
for dat_file in os.listdir(TRAIN_ROOT):
    with open(os.path.join(TRAIN_ROOT, dat_file), 'rb') as f:
        loaded_datas = pickle.load(f)
        print(f'The number of {dat_file} = {len(loaded_datas)}')
        train_datas += loaded_datas
train_datas = list(set(train_datas)) # remove duplicate data
print(f'The total number of trainingdata = {len(train_datas)}')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Current Device = {device}")
tokenizer = AutoTokenizer.from_pretrained(
  PRETRAIN_MODEL_NAME,
  cache_dir=CACHE_PATH,
)
tokenizer.add_special_tokens(special_token_dict)
config = AutoConfig.from_pretrained(PRETRAIN_MODEL_NAME,
                                    bos_token_id=tokenizer.bos_token_id,
                                    eos_token_id=tokenizer.eos_token_id,
                                    pad_token_id=tokenizer.pad_token_id,
                                    sep_token_id=tokenizer.sep_token_id,
                                    output_hidden_states=False)

dataset = GPTDataset(datas=train_datas, 
                     tokenizer=tokenizer, 
                     special_token_dict=special_token_dict)

dataloader = DataLoader(dataset=dataset, 
                        shuffle=True, batch_size=BATCH_SIZE,
                          collate_fn=dataset.collate_batch)

model : GPTNeoXForCausalLM = GPTNeoXForCausalLM.from_pretrained(PRETRAIN_MODEL_NAME, 
                                                                cache_dir = CACHE_PATH, 
                                                                config = config)

param_optimizer = list(model.named_parameters())
no_decay = ['bias', 'LayerNorm.weight']
grouped_optimizer_parameter = [
    {'params' : [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay_rate' : 0.01},
    {'params' : [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay_rate' : 0.01}
    ]
opti = torch.optim.AdamW(grouped_optimizer_parameter, lr= 3e-5)
model = model.to(device)

print(f"Save Tokenizer...")
tokenizer.save_pretrained(os.path.join(SAVE_PATH, f"{MODEL_NAME}_Tokenizer"))
print(f'Done!')
step = 1
current = None
revision_temp = None
for epoch in range(EPOCHS):
    save_tokenizer = True
    model.train()
    total_loss = 0.
    sample_num = 0
    train_process = tqdm(dataloader, desc=f"epoch : {epoch}, (Step = {step})")
    for seqs, labels, masks in train_process:
        seqs, labels, masks = seqs.to(device), labels.to(device), masks.to(device)
        model.zero_grad()
        outputs = model(seqs, labels = labels, attention_mask = masks)
        logits = outputs.logits
        loss = outputs.loss
        loss = loss.mean()
        loss_val = loss.item()
        sample_num += logits.shape[0]
        total_loss += loss_val
        if math.isnan(loss_val) or math.isinf(loss_val):
            break
        loss.backward()
        opti.step()
        train_process.set_postfix({f"Loss" : total_loss / sample_num})
        step += 1
    if epoch > 5:
        model.save_pretrained(os.path.join(SAVE_PATH, f"{MODEL_NAME}_{epoch}"))
model.save_pretrained(os.path.join(SAVE_PATH, f"{MODEL_NAME}_{epoch}"))
print(f"Done!")