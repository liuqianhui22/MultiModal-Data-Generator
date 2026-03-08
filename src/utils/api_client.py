
"""
API客户端模块 - 模拟千问VL API调用
在实际项目中需要替换为真实的API调用逻辑
"""

import time
import random
from src.utils.logger import logger

class QwenVLClient:
    def __init__(self, api_key=None, endpoint=None):
        self.api_key = api_key or "mock_api_key_for_demo"
        self.endpoint = endpoint or "https://mock.qwen-vl.api"
        self.temperature = 0.6
        logger.info("QwenVL客户端初始化完成")

    def set_temperature(self, temperature):
        """设置生成温度"""
        self.temperature = temperature
        logger.info(f"设置生成温度: {temperature}")

    def generate_from_image(self, image_path, prompt):
        """
        模拟图生文API调用
        在实际项目中需要实现真实的API调用
        """
        logger.info(f"模拟调用V2T API: {image_path}")

        # 模拟API调用延迟
        time.sleep(0.1)

        # 返回模拟数据
        return {
            "description": "这是一个系统架构图，包含前端、后端、数据库等组件",
            "qa_pairs": [
                {"question": "这个系统包含哪些组件？", "answer": "前端、后端、数据库、缓存"},
                {"question": "数据流向是怎样的？", "answer": "前端→后端→数据库"}
            ]
        }

    def generate_from_text(self, text_description):
        """
        模拟文生图API调用
        在实际项目中需要实现真实的API调用
        """
        logger.info("模拟调用T2V API")

        # 模拟API调用延迟
        time.sleep(0.1)

        # 返回模拟数据
        return {
            "nodes": ["component_a", "component_b", "component_c"],
            "edges": [
                {"from": "component_a", "to": "component_b"},
                {"from": "component_b", "to": "component_c"}
            ],
            "graph_type": "architecture"
        }

    def check_api_status(self):
        """检查API状态"""
        return {
            "status": "healthy",
            "version": "1.0",
            "model": "qwen-vl-plus"
        }
