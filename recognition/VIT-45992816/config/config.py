import torch
import torchvision.transforms as transforms
from argparse import Namespace


class Config:
    lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR
    lr_scheduler_params = {
        'T_max': 10,
        'eta_min': 1e-6
    }
    random_seed = 0
    plot_train_batch_count = 5
    custom_augment = transforms.Compose([
    ])

    def _get_opt(self):
        config_dict = {name:getattr(self, name) for name in dir(self) if name[0] != '_'}
        return Namespace(**config_dict)

if __name__ == '__main__':
    config = Config()
    print(config._get_opt())