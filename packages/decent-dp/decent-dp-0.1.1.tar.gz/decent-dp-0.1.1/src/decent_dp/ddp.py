from functools import partial
from loguru import logger
from typing import Callable, Iterator, List, Optional, Tuple
import torch
from torch import Tensor
from torch.nn import Module
import torch.distributed as dist
from torch.distributed import Work
from torch.nn.parameter import Parameter
from decent_dp.topo import TopologyReg, Topology

class DecentralizedDataParallel(Module):
    def __init__(self,
                 model: Module,
                 topology: str = 'ring'):
        super(DecentralizedDataParallel, self).__init__()
        if torch.cuda.is_available():
            model = model.cuda()
        self._model = model
        
        self._rank: int = -1
        self._world_size: int = -1
        self._topo: Optional[Topology] = None
        self._params: List[Tensor] = list([x for x in self._model.parameters() if x.requires_grad])
        self._used_param_ids: List[int] = []
        self._used_params: List[Tensor] = []
        self._buffers: List[Tensor] = []
        self._step: int = -1
        self._comm_op: Optional[Work] = None
        self._is_initialized: bool = False
        self._total_used_params: int = 0
        self._total_used_params_b: int = 0
        self._is_gpu_available = torch.cuda.is_available()
        self._optim_hook: Optional[Callable] = None
        
        self._initialize_ddp()
        self._initialize_topo(topology)
        self._create_hooks()
        self._sync_at_start()
    
    def _initialize_ddp(self):
        if not (dist.is_available() and dist.is_initialized()):
            logger.error('PyTorch distributed is not initialized')
            raise RuntimeError()
        self._rank = dist.get_rank()
        self._world_size = dist.get_world_size()
        if self._rank == 0:
            logger.info("Using Decentralized Data Parallel")
    
    def _initialize_topo(self, topology: str):
        self._topo = TopologyReg.registry[topology]()
        self._topo.create_edges()
    
    @torch.no_grad()
    def _sync_at_start(self):
        for param in self._params:
            dist.broadcast(param, 0)
    
    @torch.no_grad()
    def global_avg(self):
        torch._foreach_mul_([x.data for x in self._used_params], 1 / self._world_size)
        dist.all_reduce_coalesced([x.data for x in self._used_params], op=dist.ReduceOp.SUM)
    
    def _create_hooks(self):
        for pid, param in enumerate(self._params):
            param.register_post_accumulate_grad_hook(
                partial(
                    lambda data, pid: self._ddp_fn(data, pid),
                    pid=pid
                ))
    
    @torch.no_grad()
    def _ddp_fn(self, _: Tensor, pid: int):
        if not self._is_initialized:
            self._used_param_ids.append(pid)
        else:
            self._total_used_params -= 1
            if self._total_used_params == 0:
                self._total_used_params = self._total_used_params_b
                if self._comm_op is not None:
                    self._comm_op.wait()
                    self._comm_op = None
                    edge = self._topo.get_current_edge(self._step)
                    weight = edge['weights'][edge['ranks'].index(self._rank)]

                    if self._optim_hook is not None:
                        self._optim_hook(edge, weight)

                    torch._foreach_mul_(self._used_params, weight - (1 - weight) / (len(edge['ranks']) - 1))
                    torch._foreach_add_(self._used_params, self._buffers)

    
    def _initialize_params(self):
        self._total_used_params = len(self._used_param_ids)
        self._total_used_params_b = self._total_used_params

        self._used_param_ids = sorted(list(set(self._used_param_ids)))
        self._used_params = [self._params[i] for i in self._used_param_ids]
        verify = [[[i, self._params[i].numel()] for i in self._used_param_ids]]
        result = [None] if self._rank != 0 else verify
        dist.broadcast_object_list(result, src=0)

        if not all([x == y for x, y in zip(verify[0], result[0])]):
            logger.error('Number/Order of elements in used parameters is different on different nodes')
            raise RuntimeError()

        self._buffers = [torch.empty_like(p, device=p.device, requires_grad=False) for p in self._used_params]
        for i in range(len(self._used_params)):
            self._used_params[i].__setattr__("buffer", self._buffers[i])

    @torch.no_grad()
    def sync(self):
        self._step += 1
        if not self._is_initialized:
            self._initialize_params()
            self._is_initialized = True
        torch._foreach_copy_(self._buffers, self._used_params)
        edge = self._topo.get_current_edge(self._step)
        weight = edge['weights'][edge['ranks'].index(self._rank)]
        torch._foreach_mul_(self._buffers, (1 - weight) / (len(edge['ranks']) - 1))
        self._comm_op = dist.all_reduce_coalesced(
            self._buffers,
            op=dist.ReduceOp.SUM,
            group=edge['group'],
            async_op=True
        )
    
    def register_optim_hook(self, hook: Callable):
        self._optim_hook = hook

    def train(self, mode: bool = True):
        self._model.train(mode)
    
    def eval(self):
        self._model.eval()

    def forward(self, *args, **kwargs):
        return self._model(*args, **kwargs)

    def parameters(self, recurse: bool = True) -> Iterator[Parameter]:
        yield from self._model.parameters(recurse)
    
    def named_parameters(self, prefix: str = '', recurse: bool = True, remove_duplicate: bool = True) -> Iterator[Tuple[str, Parameter]]:
        return super().named_parameters(prefix, recurse, remove_duplicate)
