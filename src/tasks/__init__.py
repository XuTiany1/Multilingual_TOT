def get_task(name):
    if name == 'MGSM':
        from src.tasks.MGSM import MgsmTask
        return MgsmTask()
    else:
        raise NotImplementedError