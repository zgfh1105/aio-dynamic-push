import os

import yaml

from common.logger import log


class ConfigReaderForYml(object):
    def __init__(self, config_file_name="config.yml"):
        config_file_path = os.path.join(os.getcwd(), config_file_name)
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"No such file: {config_file_name}")
        with open(config_file_path, "r", encoding="utf-8") as file:
            self._config = yaml.safe_load(file)

    def get_common_config(self) -> dict:
        result = self._config.get("common", {})
        log.info("已加载 common 配置（不输出配置内容，避免泄露密钥）")
        return result

    def get_query_task_config(self) -> list:
        result = self._config.get("query_task", [])
        enabled = [item.get("name", "<未命名>") for item in result if item.get("enable", False)]
        log.info("已加载 %d 个查询任务，启用：%s（不记录 Cookie 等凭证）", len(result), enabled)
        return result

    def get_push_channel_config(self) -> list:
        result = self._config.get("push_channel", [])
        enabled = [item.get("name", "<未命名>") for item in result if item.get("enable", False)]
        log.info("已加载 %d 个推送通道，启用：%s（不记录 Token/Secret）", len(result), enabled)
        return result


global_config = ConfigReaderForYml()
