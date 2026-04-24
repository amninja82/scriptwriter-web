"""
创意引导模块
对话式需求采集系统
"""
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import os
import json


class IdeaGuide:
    """创意引导类"""
    
    def __init__(self):
        self.steps = [
            "idea",           # 创意输入
            "genre",          # 题材类型
            "audience",       # 受众群体
            "episodes",       # 集数/时长
            "style",          # 风格偏好
            "reference"       # 对标作品
        ]
        
        self.current_step = 0
        self.collected_info = {}
        self.conversation_history = []
    
    def get_current_step(self) -> str:
        """获取当前步骤"""
        if self.current_step >= len(self.steps):
            return "completed"
        return self.steps[self.current_step]
    
    def get_step_question(self) -> str:
        """获取当前步骤的问题"""
        step = self.get_current_step()
        
        questions = {
            "idea": """🎬 欢迎使用多智能体编剧系统！

请告诉我你的创作创意，可以是一句话、一个想法或一个场景。

例如：
- "我想写一个古代宫廷悬疑剧"
- "关于未来世界的爱情故事"
- "一个侦探破案的悬疑剧"
- "家庭伦理剧，关于母女关系"

请开始描述你的创意 👇
""",
            
            "genre": """很好！让我再了解一下题材类型。

这个剧本属于哪种类型？
- 悬疑
- 爱情
- 科幻
- 历史/古装
- 现代都市
- 喜剧
- 动作
- 家庭伦理
- 青春校园
- 其他（请说明）

请选择或描述 👇
""",
            
            "audience": """明白了！那目标观众是谁呢？

- 18-25岁（青年群体）
- 25-35岁（青年职场）
- 35-50岁（成熟观众）
- 全年龄层
- 特定群体（请说明）

请选择或描述 👇
""",
            
            "episodes": """收到！这个剧本的规模是？

电视剧：
- 10-20集（短剧）
- 20-40集（中篇）
- 40+集（长篇）

电影：
- 90分钟（标准）
- 120分钟（长片）

网剧/短视频：
- 3-5分钟（短视频）
- 10-15分钟（微短剧）
- 其他（请说明时长）

请选择或说明 👇
""",
            
            "style": """了解！风格偏好是？

- 悬疑紧张
- 温馨治愈
- 欢脱搞笑
- 现实主义
- 浪漫唯美
- 黑暗压抑
- 其他（请描述）

请选择或描述 👇
""",
            
            "reference": """最后一个问题！

有没有对标的作品或参考？
这可以帮助我们更好地把握风格和定位。

例如：
- 类似《琅琊榜》
- 参考《甄嬛传》
- 像《流浪地球》
- 无对标

请提供或跳过 👇
"""
        }
        
        return questions.get(step, "")
    
    def process_answer(self, answer: str) -> Dict:
        """处理用户回答"""
        step = self.get_current_step()
        
        # 保存回答
        self.collected_info[step] = answer
        
        # 记录对话历史
        self.conversation_history.append({
            "step": step,
            "question": self.get_step_question(),
            "answer": answer
        })
        
        # 移动到下一步
        self.current_step += 1
        
        # 检查是否完成
        if self.current_step >= len(self.steps):
            return {
                "status": "completed",
                "message": "✅ 信息收集完成！正在生成需求报告...",
                "collected_info": self.collected_info
            }
        else:
            return {
                "status": "continue",
                "next_question": self.get_step_question(),
                "collected_info": self.collected_info
            }
    
    def get_summary(self) -> str:
        """获取收集信息摘要"""
        summary = "📋 需求采集摘要\n\n"
        
        labels = {
            "idea": "创意构思",
            "genre": "题材类型",
            "audience": "受众群体",
            "episodes": "规模时长",
            "style": "风格偏好",
            "reference": "对标作品"
        }
        
        for step, answer in self.collected_info.items():
            label = labels.get(step, step)
            summary += f"**{label}**: {answer}\n\n"
        
        return summary
    
    def reset(self):
        """重置引导"""
        self.current_step = 0
        self.collected_info = {}
        self.conversation_history = []


class IdeaGuideAgent:
    """创意引导 Agent"""
    
    def __init__(self):
        self.guide = IdeaGuide()
        
        # 加载配置
        workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
        config_path = os.path.join(workspace_path, "config/scriptwriter_llm_config.json")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        
        api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
        base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
        
        self.llm = ChatOpenAI(
            model=cfg['config'].get("model"),
            api_key=api_key,
            base_url=base_url,
            temperature=0.7,
            timeout=600
        )
    
    def start_guide(self) -> str:
        """开始引导"""
        self.guide.reset()
        return self.guide.get_step_question()
    
    def next_step(self, user_input: str) -> Dict:
        """下一步"""
        result = self.guide.process_answer(user_input)
        
        if result["status"] == "completed":
            # 生成需求报告
            summary = self.guide.get_summary()
            
            # 使用 LLM 生成结构化需求
            prompt = f"""
基于以下用户回答，生成一个结构化的剧本创作需求：

{summary}

请按照以下格式输出：
```json
{{
    "idea": "核心创意",
    "genre": "题材类型",
    "audience": "受众群体",
    "episodes": "集数/时长",
    "style": "风格偏好",
    "reference": "对标作品",
    "key_points": ["核心看点1", "核心看点2", "核心看点3"],
    "suggested_title": "建议剧名"
}}
```
"""
            
            try:
                response = self.llm.invoke([HumanMessage(content=prompt)])
                result["requirement_report"] = summary
                result["structured_requirement"] = response.content
                
                # 尝试解析 JSON
                try:
                    import re
                    json_match = re.search(r'```json\s*(.*?)\s*```', response.content, re.DOTALL)
                    if json_match:
                        result["requirement_data"] = json.loads(json_match.group(1))
                except:
                    pass
                    
            except Exception as e:
                result["error"] = f"生成需求报告失败: {str(e)}"
        
        return result
    
    def get_collected_info(self) -> Dict:
        """获取收集的信息"""
        return self.guide.collected_info
    
    def is_completed(self) -> bool:
        """是否完成"""
        return self.guide.get_current_step() == "completed"


def create_idea_guide() -> IdeaGuideAgent:
    """创建创意引导实例"""
    return IdeaGuideAgent()
