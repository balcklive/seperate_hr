# 节点名称

职位要求生成节点

# 节点作用

与用户交互，根据与用户交互的内容生成职位格式化的职位要求json

# 场景一
    直接读取用户输入的job description，假定该jd已经非常详尽，然后将其转换成标准的json格式
    输出格式：
      {
          "session_id": "",
          "requirements" :
                  {
                          "title": "title of the job",
                          "description": "some description about the job",
                          "must_have":    {
                                  "technical_skills": [],
                                  "domain_experience": [],
                                  "soft_skills": []
                          },
                          "nice_to_have": []
                  }
  }

# 场景二
    用户没有详尽的job description，节点会通过对话的方式引导用户生成jd，节点首先会生成一系列带选项的提问，输出的格式如下：
    {
  "session_id": "",
  "questions_with_options": [
    {
      "question": "What is the primary role type for this position?",
      "options": [
        {"text": "Technical/Engineering", "value": "technical", "description": "Software development, data engineering, DevOps roles"},
        {"text": "Product Management", "value": "product", "description": "Product strategy, roadmap planning, stakeholder management"},
        {"text": "Design", "value": "design", "description": "UI/UX design, visual design, user research"},
        {"text": "Sales/Marketing", "value": "sales_marketing", "description": "Business development, digital marketing, customer acquisition"},
        {"text": "Operations", "value": "operations", "description": "Business operations, project management, process optimization"},
        {"text": "Other", "value": "other", "description": "Other role types not listed above"}
      ],
      "allow_custom_input": true,
      "required": true
    },
    {
      "question": "What is the experience level required?",
      "options": [
        {"text": "Entry Level (0-2 years)", "value": "entry", "description": "Fresh graduates or professionals with minimal experience"},
        {"text": "Mid Level (3-5 years)", "value": "mid", "description": "Professionals with solid foundation and some leadership experience"},
        {"text": "Senior Level (6-10 years)", "value": "senior", "description": "Experienced professionals with team leadership capabilities"},
        {"text": "Principal/Staff Level (10+ years)", "value": "principal", "description": "Industry experts with strategic thinking and mentorship abilities"}
      ],
      "allow_custom_input": true,
      "required": true
    }
  ]
  }
  用户会根据提问选择回应的选项以：What is the primary role type for this position?:Technical/Engineering;的格式进行回复。随后节点会根据用户的回复，补全职位要求的信息。当用户明确表示没有更多信息提供时，则直接使用目前已有的信息生成职位说明

# 基于OpenAI Agents框架的实现流程设计

## 节点规划

### 1. 主控节点（Orchestrator Node）
- **作用**：判断用户输入属于哪个场景，并决定后续流程
- **输入**：用户的职位描述或对话内容
- **输出**：场景判断结果 + 路由到相应节点

### 2. JD解析节点（JD Parser Node）
- **作用**：处理场景一 - 解析详细的职位描述
- **输入**：完整的职位描述文本
- **输出**：标准化的JSON格式职位要求
- **触发条件**：主控节点判断为场景一

### 3. 对话引导节点（Conversation Guide Node）
- **作用**：处理场景二 - 通过对话引导用户生成JD
- **输入**：用户初始输入或对话历史
- **输出**：结构化问题选项或最终JD
- **触发条件**：主控节点判断为场景二

### 4. 问题生成子节点（Question Generator Sub-Node）
- **作用**：生成带选项的提问
- **输入**：当前对话状态
- **输出**：questions_with_options格式的问题
- **触发条件**：对话引导节点需要生成新问题

### 5. 回复解析子节点（Response Parser Sub-Node）
- **作用**：解析用户的选择回复
- **输入**：用户回复（如"Technical/Engineering"）
- **输出**：解析后的选项值
- **触发条件**：对话引导节点收到用户回复

## Handoff使用场景

```
主控节点 → Handoff → JD解析节点（场景一）
主控节点 → Handoff → 对话引导节点（场景二）
对话引导节点 → Handoff → 问题生成子节点（需要新问题）
对话引导节点 → Handoff → 回复解析子节点（需要解析回复）
```

## 具体工作流程

### 场景一流程：
```
用户输入 → 主控节点 → Handoff → JD解析节点 → 输出结果
```

### 场景二流程：
```
用户输入 → 主控节点 → Handoff → 对话引导节点
对话引导节点 → Handoff → 问题生成子节点 → 返回问题
用户回答 → 对话引导节点 → Handoff → 回复解析子节点 → 更新状态
（循环直到完成）→ 生成最终JD
```

## 核心工具函数设计

### 场景判断工具
```python
def determine_scenario(user_input: str) -> str:
    """判断用户输入属于哪个场景"""
    # 分析用户输入的详细程度
    # 返回 "detailed_jd" 或 "need_conversation"
```

### JD解析工具
```python
def parse_detailed_jd(jd_text: str) -> dict:
    """解析详细的职位描述"""
    # 使用LLM提取结构化信息
    # 返回标准JSON格式
```

### 问题生成工具
```python
def generate_structured_questions() -> dict:
    """生成结构化的问题选项"""
    # 返回包含问题选项的JSON
```

### 用户回复解析工具
```python
def parse_user_response(response: str) -> dict:
    """解析用户的选择回复"""
    # 解析 "问题:选项" 格式
    # 更新职位信息
```

### 格式转换工具
```python
def format_final_output(jd_data: dict) -> dict:
    """统一输出格式"""
    # 确保输出符合文档要求的JSON格式
```

## 实现优势

1. **模块化设计**：每个节点职责明确，易于维护和扩展
2. **灵活协作**：通过handoff实现节点间的无缝协作
3. **状态管理**：支持复杂的多轮对话和状态跟踪
4. **标准化输出**：确保所有输出符合文档要求的JSON格式
5. **可扩展性**：易于添加新的问题类型或解析逻辑
