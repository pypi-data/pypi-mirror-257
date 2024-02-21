import torch
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class GD_output:
    parameters: dict = None
    per_step_objectives: torch.Tensor = None
    per_epoch_objectives: torch.Tensor = None
    epoch_step_nums: torch.Tensor = None
    grad_steps: range = None
    lr: float = None
    num_steps: int = None
    decay_rate: float = None
    batch_size: int = None
    num_epochs: int = None
    max_steps: int = None
    type_flag: str = None
    
    def __str__(self):
        print_string = ''
        if self.type_flag == 'gd':
            print_string += 'GRADIENT DESCENT OUTPUT'
            print_string += f'\nlearning rate: {self.lr}, decay rate: {self.decay_rate}, gradient steps: {self.num_steps}'
            for key, parameter in self.parameters.items():
                print_string += f'\n\nparameter {key}:\n{parameter}'
            print_string += f'\n\nobjectives:\n{self.objectives}'
            return print_string
        else:
            print_string += 'STOCHASTIC GRADIENT DESCENT OUTPUT'
            print_string += f'\nlearning rate: {self.lr}, decay rate: {self.decay_rate},' \
                f' batch size: {self.batch_size}, number of epochs: {self.num_epochs}'
            for key, parameter in self.parameters.items():
                print_string += f'\n\nparameter {key}:\n{parameter}'
            print_string += f'\n\nper-step objectives:\n{self.per_step_objectives}'
            print_string += f'\n\nper-epoch mean objectives:\n{self.per_epoch_objectives}'
            print_string += f'\n\nepochs began/completed on the follow gradient steps:\n{self.epoch_step_nums}'
            return print_string