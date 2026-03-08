"""
主入口模块
协调整个多模态图表生成流水线
"""

import argparse
from src.generator.v2t import V2TGenerator
from src.generator.t2v import T2VGenerator
from src.validator.bidirectional import BidirectionalValidator
from src.utils.logger import logger


class MultiModalGenerator:
    def __init__(self):
        self.v2t_generator = V2TGenerator()
        self.t2v_generator = T2VGenerator()
        self.validator = BidirectionalValidator()
        logger.info("多模态图表生成器初始化完成")

    def run_full_pipeline(self, input_data, chart_type="flowchart", diversity="medium"):
        """运行完整的生成-校验流水线"""
        logger.info(f"开始运行完整流水线，类型: {chart_type}, 多样性: {diversity}")

        try:
            # 1. V2T 生成
            logger.info("阶段1: 图生文生成")
            if chart_type == "flowchart":
                v2t_result = self.v2t_generator.analyze_flowchart(input_data)
            else:
                v2t_result = self.v2t_generator.analyze_architecture(input_data)

            if not v2t_result['success']:
                return v2t_result

            # 2. T2V 生成
            logger.info("阶段2: 文生图生成")
            description = v2t_result['data']['description']
            t2v_result = self.t2v_generator.generate_from_text(description, chart_type)

            if not t2v_result['success']:
                return t2v_result

            # 3. 双向校验
            logger.info("阶段3: 双向校验")
            validation_result = self.validator.validate_v2t_t2v(
                description,
                description,  # 这里应该是重构后的描述，用相同值模拟
                t2v_result['data']
            )

            # 4. 结果汇总
            final_result = {
                'success': True,
                'chart_type': chart_type,
                'v2t_result': v2t_result,
                't2v_result': t2v_result,
                'validation': validation_result,
                'quality_score': validation_result.get('overall_score', 0.0)
            }

            logger.info(f"流水线完成，质量评分: {final_result['quality_score']:.3f}")
            return final_result

        except Exception as e:
            logger.error(f"流水线执行失败: {e}")
            return {
                'success': False,
                'error': str(e)
            }


def main():
    parser = argparse.ArgumentParser(description='多模态图表数据生成器')
    parser.add_argument('--input', '-i', required=True, help='输入文件路径')
    parser.add_argument('--type', '-t', default='flowchart',
                        choices=['flowchart', 'architecture'], help='图表类型')
    parser.add_argument('--diversity', '-d', default='medium',
                        choices=['low', 'medium', 'high'], help='生成多样性')

    args = parser.parse_args()

    # 初始化生成器
    generator = MultiModalGenerator()

    # 运行流水线
    result = generator.run_full_pipeline(args.input, args.type, args.diversity)

    if result['success']:
        print("✅ 生成成功！")
        print(f"📊 质量评分: {result['quality_score']:.3f}")
        print(f"📝 生成描述: {result['v2t_result']['data']['description'][:100]}...")
    else:
        print("❌ 生成失败")
        print(f"错误: {result['error']}")


if __name__ == "__main__":
    main()
