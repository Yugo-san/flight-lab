import torch, numpy as np
from ml.model import FlightRanker
X = np.random.rand(1000, 6).astype(np.float32)
y = (1 - X[:, 3])*0.4 + (1 - X[:, 4])*0.3 + (1 - X[:, 5])*0.2 + X[:, 1]*0.1
y = np.clip(y, 0, 1).reshape(-1, 1)
model = FlightRanker()
opt = torch.optim.Adam(model.parameters(), lr=0.01)
for _ in range(150):
    opt.zero_grad()
    loss = ((model(torch.tensor(X)) - torch.tensor(y))**2).mean()
    loss.backward(); opt.step()
torch.save(model.state_dict(), "ml/weights.pth", _use_new_zipfile_serialization=False)
print(f"✅ Модель обучена. Loss: {loss.item():.4f}")