from strhub.models.utils import load_from_checkpoint
import torch

tamil_parseq = load_from_checkpoint(r"model_weights\parseq_improved.ckpt").eval().to("cpu")
torch.save(tamil_parseq,r"model_weights\parseq_tamil_improved.pt")