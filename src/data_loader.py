import os
import cv2
import numpy as np
import pandas as pd
from torch.utils.data import Dataset

class ECGDataset(Dataset):
    def __init__(self, dataframe, img_folder, transform=None, is_test=False):
        self.df = dataframe
        self.img_folder = img_folder
        self.transform = transform
        self.is_test = is_test

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        img_id = self.df.iloc[idx]["image_id"]
        img_path = os.path.join(self.img_folder, img_id + ".png")
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
        if self.transform:
            image = self.transform(image)
        image = np.expand_dims(image, axis=0)
        if self.is_test or ("ecg_data" not in self.df.columns):
            signal = np.zeros(1000, dtype=np.float32)
        else:
            signal_data = self.df.iloc[idx]["ecg_data"]
            if isinstance(signal_data, str):
                signal = np.array(eval(signal_data), dtype=np.float32) # Expect a stringified list
            else:
                signal = np.zeros(1000, dtype=np.float32)
        return image, signal
