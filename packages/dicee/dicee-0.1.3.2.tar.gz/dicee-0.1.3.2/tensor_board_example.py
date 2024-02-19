import torch
import torch.nn as nn
from torch.nn import functional as F

# hyperparameters
batch_size = 512  # how many independent sequences will we process in parallel?
block_size = 64  # what is the maximum context length for predictions?
max_iters = 2000  # number of parameter updates
eval_interval = 300
learning_rate = 1e-2
device = 'cuda' if torch.cuda.is_available() else 'cpu'
eval_iters = 200
# ------------
torch.manual_seed(1)

# wget https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt
# with open('input.txt', 'r', encoding='utf-8') as f:
#    text = f.read()
#############################################################
# text=> Sequence of triples represented as characters

############################################################
with open("KGs/Countries-S1/train.txt", "r") as f:
    text = "\n".join([i for i in f.readlines()])

# here are all the unique characters that occur in this text
chars = sorted(list(set(text)))
vocab_size = len(chars)
# create a mapping from characters to integers
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s]  # encoder: take a string, output a list of integers
decode = lambda l: ''.join([itos[i] for i in l])  # decoder: take a list of integers, output a string

# Train and test splits
data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9 * len(data))  # first 90% will be train, rest val
train_data = data[:n]
val_data = data[n:]
###################################################
# Understanding a single data point (x,y)
x = train_data[:block_size]
y = train_data[1:block_size + 1]
print(x.shape, y.shape)
for t in range(block_size):
    context = x[:t + 1]
    target = y[t]
    print(f"Given ({context}), target ({target})")


###################################################


# data loading
def get_batch(split):
    # generate a small batch of data of inputs x and targets y
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i + block_size] for i in ix])
    y = torch.stack([data[i + 1:i + block_size + 1] for i in ix])
    x, y = x.to(device), y.to(device)
    return x, y


@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split)
            logits, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out


n_embd = 4
n_layer = 2
n_head = 2
dropout = 0.0


class Head(nn.Module):
    """ one head of self-attention """

    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # input of size (batch, time-step, channels)
        # output of size (batch, time-step, head size)

        # b denotes the batch size
        # t denotes the number of tokens representing a single input (i.e., tokens of a sentence)
        batch_size, token_size, dims = x.shape

        # (1) Linear Transformation: (batch_size, token_size, k)
        k = self.key(x)
        # (2) Linear Transformation: (batch_size, token_size, k)
        q = self.query(x)
        # (3) Linear Transformation perform: (batch_size, token_size, k) the weighted aggregation of the values
        v = self.value(x)  # (B,T,hs)

        # (4) Compute attention scores/similarities("affinities"): (batch_size, token_size, token_size)
        # (batch_size, token_size, k) @ (batch_size, k, token_size) -> (batch_size, token_size, token_size)
        # wei captures similarity between each tokens
        wei = q @ k.transpose(-2, -1) * k.shape[-1] ** -0.5

        # (5) MASK similarities between tokens by incorporating the sequential aspect of the inputs
        # (batch_size, token_size, token_size)
        wei = wei.masked_fill(self.tril[:token_size, :token_size] == 0, float('-inf'))
        # (6) Normalize similarities :(batch_size, token_size, token_size)
        wei = F.softmax(wei, dim=-1)
        wei = self.dropout(wei)
        # (7) Matrix multiplication:between the weighted aggregation of the values
        # (batch_size, token_size, token_size) @ (batch_size, token_size, k) -> (batch_size, token_size, k)
        out = wei @ v
        return out


class MultiHeadAttention(nn.Module):
    """ multiple heads of self-attention in parallel """

    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(head_size * num_heads, n_embd)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.dropout(self.proj(out))
        return out


class FeedForward(nn.Module):
    """ a simple linear layer followed by a non-linearity """

    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.ReLU(),
            nn.Linear(4 * n_embd, n_embd),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.net(x)


class Block(nn.Module):
    """ Transformer block: communication followed by computation """

    def __init__(self, n_embd:int, n_head:int):
        # n_embd: embedding dimension, n_head: the number of heads we'd like
        super().__init__()
        head_size = n_embd // n_head
        self.multi_head_attention = MultiHeadAttention(n_head, head_size)
        self.ffwd = FeedForward(n_embd)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

    def forward(self, x):
        x = x + self.multi_head_attention(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x


class GPTLanguageModel(nn.Module):

    def __init__(self):
        super().__init__()
        # each token directly reads off the logits for the next token from a lookup table
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
        self.position_embedding_table = nn.Embedding(block_size, n_embd)
        self.blocks = nn.Sequential(*[Block(n_embd, n_head=n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd)  # final layer norm
        self.lm_head = nn.Linear(n_embd, vocab_size)

        # better init, not covered in the original GPT video, but important, will cover in followup video
        self.apply(self._init_weights)

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, idx, targets=None):
        # b denotes the number of input points
        # t denotes the number of tokens representing a single input (i.e., tokens of a sentence)

        b, t = idx.shape
        # (1) Get Token embeddings: (b,t,d)
        tok_emb = self.token_embedding_table(idx)
        # (2) Get Position embeddings: (t,d)
        pos_emb = self.position_embedding_table(torch.arange(t))
        # (3) (1) + (2)
        x = tok_emb + pos_emb
        # (4) Apply n_layer residual blocks of [MultiHeadAttention + Normalize + FF + Normalize]
        x = self.blocks(x)
        # (5) Normalize (4)
        x = self.ln_f(x)
        # (6) Predictions (b, t,vocab_size)
        logits = self.lm_head(x)

        if targets is None:
            loss = None
        else:
            b, t, d = logits.shape
            logits = logits.view(b * t, d)
            targets = targets.view(b * t)
            loss = F.cross_entropy(logits, targets)

        return logits, loss

    def generate(self, idx, max_new_tokens):
        # idx is (B, T) array of indices in the current context
        for _ in range(max_new_tokens):
            # crop idx to the last block_size tokens
            idx_cond = idx[:, -block_size:]
            # get the predictions
            logits, loss = self(idx_cond)
            # focus only on the last time step
            logits = logits[:, -1, :]  # becomes (B, C)
            # apply softmax to get probabilities
            probs = F.softmax(logits, dim=-1)  # (B, C)
            # sample from the distribution
            idx_next = torch.multinomial(probs, num_samples=1)  # (B, 1)
            # append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1)  # (B, T+1)
        return idx


model = GPTLanguageModel()
with torch.no_grad():
    print(f"A batch loss with random weights of GPT:", model(*get_batch("train"))[1])
    print(f"Theoretical loss with random weights:", -torch.log(torch.tensor(1 / vocab_size)))
    print(f"Estimate losses on train and val", estimate_loss())

# print the number of parameters in the model
print(sum(p.numel() for p in model.parameters()) / 1e6, 'M parameters')

# create a PyTorch optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

for iter in range(max_iters):

    # every once in a while evaluate the loss on train and val sets
    if iter % eval_interval == 0 or iter == max_iters - 1:
        losses = estimate_loss()
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")

    # sample a batch of data
    xb, yb = get_batch('train')

    # evaluate the loss
    logits, loss = model(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

# generate from the model
context = torch.zeros((1, 1), dtype=torch.long, device=device)
print(decode(model.generate(context, max_new_tokens=500)[0].tolist()))
# open('more.txt', 'w').write(decode(m.generate(context, max_new_tokens=10000)[0].tolist()))
