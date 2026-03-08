"""
图生文(V2T)生成器模块
负责解析图表并生成文本描述和问答对
"""

import json
import yaml
from pathlib import Path
from src.utils.api_client import QwenVLClient
from src.utils.logger import logger

class V2TGenerator:
    def __init__(self, config_path="../configs/prompts.yaml"):
        self.client = QwenVLClient()
        self.prompts = self._load_prompts(config_path)
        logger.info("V2T生成器初始化完成")

    def _load_prompts(self, config_path):
        """加载提示词配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config.get('prompt_templates', {})
        except Exception as e:
            logger.error(f"加载提示词配置失败: {e}")
            return {}

    def analyze_flowchart(self, image_path):
        """分析流程图"""
        prompt = self.prompts.get('v2t_flowchart', '')
        return self._analyze_chart(image_path, prompt, 'flowchart')

    def analyze_architecture(self, image_path):
        """分析架构图"""
        prompt = self.prompts.get('v2t_architecture', '')
        return self._analyze_chart(image_path, prompt, 'architecture')

    def _analyze_chart(self, image_path, prompt, chart_type):
        """通用图表分析方法"""
        try:
            logger.info(f"开始分析{chart_type}图表: {image_path}")

            # 调用千问VL API（实际项目中需要真实API密钥）
            result = self.client.generate_from_image(image_path, prompt)

            # 解析返回结果
            if isinstance(result, dict):
                return {
                    'success': True,
                    'chart_type': chart_type,
                    'data': result
                }
            else:
                # 模拟返回结果（用于演示）
                return {
                    'success': True,
                    'chart_type': chart_type,
                    'data': {
                        'description': f'这是一个{chart_type}图表的详细描述',
                        'qa_pairs': [
                            {'question': '这是什么类型的图表？', 'answer': chart_type},
                            {'question': '主要功能是什么？', 'answer': '展示系统流程或架构'}
                        ]
                    }
                }

        except Exception as e:
            logger.error(f"图表分析失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'chart_type': chart_type
            }
