"""
生成器模块单元测试
"""

import unittest
from src.generator.v2t import V2TGenerator
from src.generator.t2v import T2VGenerator  # 这里导入的类名是正确的

class TestGenerators(unittest.TestCase):

    def test_v2t_generator_initialization(self):
        """测试V2T生成器能否正常初始化"""
        generator = V2TGenerator()
        self.assertIsNotNone(generator.client)
        self.assertIn('structure_description', generator.prompts)  # 改用您yml中实际存在的key

    def test_t2v_generator_output_structure(self):
        """测试T2V生成器输出结构是否正确"""
        generator = T2VGenerator()  # 这里修正：T2vGenerator() -> T2VGenerator()
        result = generator.generate_from_text("一个简单流程")
        self.assertTrue(result['success'])
        self.assertIn('nodes', result['data'])
        self.assertIn('edges', result['data'])
        self.assertIsInstance(result['data']['nodes'], list)

if __name__ == '__main__':
    unittest.main()
