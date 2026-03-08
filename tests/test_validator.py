"""
双向校验器单元测试 - 验证核心创新算法
"""

import unittest
from src.validator.bidirectional import BidirectionalValidator

class TestBidirectionalValidator(unittest.TestCase):

    def setUp(self):
        """初始化校验器"""
        self.validator = BidirectionalValidator(similarity_threshold=0.8)

    def test_semantic_similarity_high(self):
        """测试高相似度文本计算"""
        text1 = "这是一个包含开始、处理和结束节点的流程图"
        text2 = "该流程图有开始节点、处理节点和结束节点"
        similarity = self.validator._calculate_semantic_similarity(text1, text2)
        self.assertGreater(similarity, 0.7)  # 应该识别为高度相似

    def test_semantic_similarity_low(self):
        """测试低相似度文本计算"""
        text1 = "这是一个流程图"
        text2 = "今天天气真好"  # 完全无关的文本
        similarity = self.validator._calculate_semantic_similarity(text1, text2)
        self.assertLess(similarity, 0.3)  # 应该识别为不相似

    def test_validation_pass(self):
        """测试校验通过的情况"""
        # 使用一个肯定会通过的模拟结果
        result = self.validator.validate_v2t_t2v("流程A", "流程A", {})
        self.assertTrue(result['passed'])
        self.assertGreaterEqual(result['overall_score'], 0.8)

    def test_validation_fail(self):
        """测试校验不通过的情况"""
        # 创建一个模拟的低分结果
        validator_low_threshold = BidirectionalValidator(similarity_threshold=0.95) # 设置极高的阈值
        result = validator_low_threshold.validate_v2t_t2v("流程A", "流程B", {})
        self.assertFalse(result['passed'])
        self.assertLess(result['overall_score'], 0.95)

if __name__ == '__main__':
    unittest.main()
