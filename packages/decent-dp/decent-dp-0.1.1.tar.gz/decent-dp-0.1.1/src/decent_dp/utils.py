from loguru import logger
import os

def setupenv():
    local_world_size = os.environ['LOCAL_WORLD_SIZE']
    local_rank = os.environ['LOCAL_RANK']
    gpus = os.environ.get('CUDA_VISIBLE_DEVICES', '')
    if gpus:
        if not (len(gpus.split(',')) == int(local_world_size)):
            logger.error('LOCAL_WORLD_SIZE and CUDA_VISIBLE_DEVICES are not consistent')
            raise ValueError()
        os.environ['CUDA_VISIBLE_DEVICES'] = gpus.split(',')[local_rank]
    else:
        os.environ['rdzv_backend'] = 'gloo'
    
    return int(os.environ['RANK']), int(os.environ['WORLD_SIZE'])
