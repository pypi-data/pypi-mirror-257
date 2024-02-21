
### GPU 自动选择、排队
- gpu_queue(config: Union[DictConfig, dict] = {})：设置处理器
    ```
    支持自动选择和手动选择、排队和不排队

    Args:
        config (dict, optional): Defaults to {}.
            queuing: 是否排队，依赖 Redis，默认为 True
            visible_devices: 可见的 GPU 序号，用逗号分隔，默认为 -1, 表示全部可见
            memo: 备注
    Returns:
        Union[DictConfig, dict]: config
    ```
