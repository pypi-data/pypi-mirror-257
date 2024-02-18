from torch.optim.lr_scheduler import CosineAnnealingLR, StepLR, ConstantLR
from .utils import exists

# Code Referenced From LAVIS
def cosine_lr_schedule(optimizer, epoch, max_epoch, init_lr, min_lr):
    """Decay the learning rate"""
    lr = (init_lr - min_lr) * 0.5 * (
        1.0 + math.cos(math.pi * epoch / max_epoch)
    ) + min_lr
    for param_group in optimizer.param_groups:
        param_group["lr"] = lr
        
def warmup_lr_schedule(optimizer, step, max_step, init_lr, max_lr):
    """Warmup the learning rate"""
    lr = min(max_lr, init_lr + (max_lr - init_lr) * step / max(max_step, 1))
    for param_group in optimizer.param_groups:
        param_group["lr"] = lr

class LinearWarmupCosineLRScheduler():
    def __init__(
        self,
        optimizer,
        max_epoch,
        min_lr,
        init_lr,
        warmup_steps=0,
        warmup_start_lr=-1,
        **kwargs
    ):
        #super.__init__(optimizer)
        self.optimizer = optimizer

        self.max_epoch = max_epoch
        self.min_lr = min_lr

        self.init_lr = init_lr
        self.warmup_steps = warmup_steps
        self.warmup_start_lr = warmup_start_lr if warmup_start_lr >= 0 else init_lr

    def step(self, cur_epoch, cur_step):
        # assuming the warmup iters less than one epoch
        if cur_epoch == 0:
            warmup_lr_schedule(
                step=cur_step,
                optimizer=self.optimizer,
                max_step=self.warmup_steps,
                init_lr=self.warmup_start_lr,
                max_lr=self.init_lr,
            )
        else:
            cosine_lr_schedule(
                epoch=cur_epoch,
                optimizer=self.optimizer,
                max_epoch=self.max_epoch,
                init_lr=self.init_lr,
                min_lr=self.min_lr,
            )

class Scheduler(object):
    def __init__(self, optimizer, config):
        '''
            supported scheduler types: cos_lr, step_lr, const_lr
        '''
        if config.scheduler_type == 'cos_lr':
            self.scheduler = CosineAnnealingLR(optimizer, T_max = config.T_max, eta_min = config.eta_min)
        elif config.scheduler_type == 'step_lr':
            self.scheduler = StepLR(optimizer, step_size = config.step_size, gamma = config.gamma)
        elif config.scheduler_type == 'const_lr':
            self.scheduler = ConstantLR(optimizer, factor = config.factor, total_iters = config.total_iters)
        elif config.scheduler_type == 'warmup_cos_lr':
            self.scheduler = LinearWarmupCosineLRScheduler(optimizer, max_epoch = config.T_max, 
                                                        min_lr = config.eta_min, init_lr = config.lr, 
                                                        warmup_steps = config.warmup_steps, warmup_start_lr = config.eta_min)
        else:
            self.scheduler = None
        
    def step(self):
        if exists(self.scheduler):
            self.scheduler.step()