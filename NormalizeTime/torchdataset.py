import torch
from torch.utils.data import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
class GPTDataset(Dataset):

    def __init__(self, datas : list, tokenizer : AutoTokenizer, special_token_dict : dict) -> None:
        super().__init__()
        self.datas = datas
        self.tokenizer = tokenizer
        self.special_token_dict = special_token_dict
        self.pad_idx = tokenizer.pad_token_id
    
    def __len__(self):
        return len(self.datas)
    
    def __getitem__(self, index):
        return self.datas[index]
    
    def collate_batch(self, datas):
        tokens_list, labels_list, attnetion_mask_list = [], [], []
        for data in datas:
            encode_seq = self.tokenizer(data)
            index_tks = torch.tensor(encode_seq['input_ids'])
            attention_mask = torch.tensor(encode_seq['attention_mask'])
            
            tokens_list.append(index_tks)
            labels_list.append(index_tks)
            attnetion_mask_list.append(attention_mask)
        return self.pad_sequence(non_id_tks=tokens_list, non_labels_tks=labels_list, non_atn_msk=attnetion_mask_list)
    def pad_sequence(self, non_id_tks, non_labels_tks, non_atn_msk):
        max_size = max([len(ele) for ele in non_id_tks])

        pad_batch_1 = torch.stack([torch.concat([t, torch.LongTensor([self.pad_idx] * (max_size - len(t)))]) for t in non_id_tks])
        pad_batch_2 = torch.stack([torch.concat([t, torch.LongTensor([self.pad_idx] * (max_size - len(t)))]) for t in non_labels_tks])
        pad_batch_3 = torch.stack([torch.concat([t, torch.LongTensor([0] * (max_size - len(t)))]) for t in non_atn_msk])
        
        return pad_batch_1, pad_batch_2, pad_batch_3