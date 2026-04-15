import torch
from ml.model import FlightRanker
model = FlightRanker()
model.load_state_dict(torch.load("ml/weights.pth", map_location="cpu", weights_only=True))
model.eval()
def score_flight(req, f):
    feat = [req["budget"]/90000, req["days"]/14, {"пляж":0.8,"горы":0.6,"шоппинг":0.5,"город":0.7}.get(req["interests"][0],0.5), f[2]/90000, f[3]/14, f[4]]
    with torch.no_grad():
        return model(torch.tensor(feat, dtype=torch.float32).unsqueeze(0)).item()