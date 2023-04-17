import torch
from pytorch_lightning import LightningDataModule
from torchvision.datasets import MNIST, FashionMNIST
from torchvision import transforms
from torch.utils.data import random_split, DataLoader
from data.dm_interface import BuildInDataModuleI


class CatImg:
    def __init__(self):
        pass

    def __call__(self, img):
        return torch.cat([img, img, img], dim=0)


class MNISTDataModule(LightningDataModule):

    def __init__(self, data_dir: str = "../data", batch_size: int = 32, num_workers: int = 6):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.num_workers = num_workers

        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,)),
            # transforms.Lambda(lambda x: torch.cat([x, x, x], dim=0))
            CatImg()
        ])

        self.mnist_predict = None
        self.mnist_test = None
        self.mnist_val = None
        self.mnist_train = None

    def prepare_data(self):
        # download
        MNIST(self.data_dir, train=True, download=True)
        MNIST(self.data_dir, train=False, download=True)

    def setup(self, stage: str):
        # Assign train/val datasets for use in dataloaders
        if stage == "fit":
            mnist_full = MNIST(self.data_dir, train=True, transform=self.transform)
            self.mnist_train, self.mnist_val = random_split(mnist_full, [55000, 5000])

        # Assign test dataset for use in dataloader(s)
        if stage == "test":
            self.mnist_test = MNIST(self.data_dir, train=False, transform=self.transform)

        # if stage == "predict":
        #     self.mnist_predict = MNIST(self.data_dir, train=False, transform=self.transform)

    def train_dataloader(self):
        return DataLoader(self.mnist_train, batch_size=self.batch_size, shuffle=True, num_workers=self.num_workers)

    def val_dataloader(self):
        return DataLoader(self.mnist_val, batch_size=self.batch_size, num_workers=self.num_workers)

    def test_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=self.batch_size, num_workers=self.num_workers)

    # def predict_dataloader(self):
    #     return DataLoader(self.mnist_predict, batch_size=self.batch_size, num_workers=self.num_workers)


class FashionMNISTDataModule(BuildInDataModuleI):
    def __init__(self, data_dir: str = "../data", batch_size: int = 32, num_workers: int = 6):
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,)),
            CatImg()
        ])

        super().__init__(FashionMNIST, data_dir, transform, transform, batch_size, num_workers)
