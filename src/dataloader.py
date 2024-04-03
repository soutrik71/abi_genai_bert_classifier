import torch
from torch.utils.data import DataLoader, Dataset


class QuestionClassficationDataset(Dataset):

    def __init__(self, question, targets, max_len, tokenizer):
        self.question = question
        self.targets = targets
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.question)

    def __getitem__(self, item):
        review = str(self.question[item])
        if self.targets is not None:
            target = self.targets[item]

        # token encoder
        encoding = self.tokenizer.encode_plus(
            review,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            pad_to_max_length=True,
            return_attention_mask=True,
            truncation=True,
            return_tensors="pt",
        )

        if self.targets is not None:
            return {
                "review_text": review,
                "input_ids": encoding["input_ids"].squeeze(),
                "attention_mask": encoding["attention_mask"].squeeze(),
                "targets": torch.tensor(target, dtype=torch.float),
            }

        else:

            return {
                "review_text": review,
                "input_ids": encoding["input_ids"].squeeze(),
                "attention_mask": encoding["attention_mask"],
            }


def create_data_loader(
    question=None,
    targets=None,
    max_len=None,
    batch_size=None,
    shuffle=None,
    num_workers=4,
    pin_memory=True,
    tokenizer=None,
):
    dataset = QuestionClassficationDataset(
        question=question,
        targets=targets,
        max_len=max_len,
        tokenizer=tokenizer,
    )

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
