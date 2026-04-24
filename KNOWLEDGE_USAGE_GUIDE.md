# 编剧智能体知识库使用指南

## 一、已上传的知识库数据集

系统已成功上传以下6个专业知识库：

### 1. scriptwriter_knowledge（主知识库）
**内容**：编剧智能体核心知识库
**包含**：
- 14种题材分类（按叙事内核和环境时代）
- 角色设计12要素
- 世界观与高概念设定要求
- 戏剧化冲突要求
- 故事钩子要求
- 情绪价值点要求
- 主题设定
- 发行类型确认
- 剧本格式标准
- 输出内容规范

**使用场景**：所有创作环节都会参考此知识库

---

### 2. genre_knowledge（影视类型知识库）
**内容**：7种影视类型的创作特点
**包含**：
- 网络短剧（微短剧）：极致节奏、爽点串联
- 电视剧集：稳健铺陈、多线并行
- 网络剧集：网感强、圈层化
- 院线电影：高度凝练、强闭环
- 网络大电影：黄金3分钟、套路化
- 动画剧集：世界观优先、IP化
- 院线动画电影：合家欢、强情感

**使用场景**：项目创建时选择类型、创作中符合类型特点

---

### 3. hook_knowledge（故事钩子知识库）
**内容**：7种故事钩子分类和6大黄金法则
**包含**：
- 悬念钩子：抛谜不解谜
- 危机钩子：生死倒计时
- 反差钩子：极致违和感
- 反常钩子：违背常理
- 情感钩子：极致情绪戳心
- 利益钩子：巨额诱惑
- 宿命钩子：先亮结局

**黄金法则**：
- 短平快，绝不拖沓
- 极致化，不做温和表达
- 钩子绑定主线，拒绝噱头
- 只抛问题，不给出答案
- 用画面代替台词
- 共情优先，猎奇其次

**使用场景**：故事开篇设计、吸引观众注意力

---

### 4. emotion_knowledge（情绪价值点知识库）
**内容**：9大类情绪价值点
**包含**：
- 亲情类：守护与牺牲、亏欠与救赎、平凡陪伴、原生家庭伤痛
- 爱情/友情类：双向奔赴、爱而不得、背叛与原谅、挚友并肩
- 自我认同与成长：平凡人逆袭、与自我和解、被否定后证明
- 现实困境与生存：底层生存无奈、对抗不公、时代洪流
- 正义坚守与牺牲：孤勇坚守、为信仰牺牲、善良不被辜负
- 遗憾与和解：与过往和解、接受不圆满、失而复得
- 孤独与被理解：极致孤独、终于被看见
- 微光善意：陌生人温柔、人性闪光
- 爽剧情绪宣泄：碾压式复仇、绝对优势、天降救星、逆袭打脸

**使用场景**：情感戏设计、观众共情、爽点设计

---

### 5. worldview_knowledge（世界观与高概念设定知识库）
**内容**：5类世界观和6类高概念设定
**世界观分类**：
- 现实写实类：贴合现实，社会议题
- 奇幻架空类：虚构世界，规则自洽
- 科幻未来类：科技逻辑，未来想象
- 历史重构类：历史骨架，艺术细节
- 超现实隐喻类：荒诞外壳，现实痛点

**高概念设定**：
- 规则类：核心规则，冲突来源
- 身份反转类：身份极端反转，悬念贯穿
- 核心困境类：极端真实困境，共情突出
- 世界观叠加类：跨界创意，规则碰撞
- 情感锚点类：极致情感，治愈感人
- 宿命对抗类：对抗宿命，成长弧光

**使用场景**：世界观架构、高概念设计

---

### 6. conflict_knowledge（戏剧化冲突知识库）
**内容**：戏剧冲突的4类分类和9大实现手法
**按对抗主体分类**：
- 人与自我：内心矛盾、人性抉择
- 人与人：个体对抗、群体冲突
- 人与社会：对抗规则、时代冲突
- 人与自然/命运：对抗天灾、宿命

**实现手法**：
1. 对立双方极致化，拉满基础张力
2. 目标与障碍完全对立，零和解空间
3. 冲突层层升级，困境不断加码
4. 多重冲突叠加交织，拒绝单一单薄
5. 制造两难抉择，戳中人心
6. 以价值观冲突替代单纯肢体对抗
7. 节奏张弛有度，蓄势后集中爆发
8. 冲突绑定人物弧光，双向赋能
9. 伏笔+反转，打破观众预期

**使用场景**：冲突设计、剧情张力营造

---

## 二、如何使用知识库

### 方式1：通过智能体自动调用
智能体在创作过程中会自动从知识库中检索相关信息，例如：
- 创建项目时：查询影视类型知识库，确保符合类型特点
- 构思开篇：查询故事钩子知识库，设计吸引人的开篇
- 设计冲突：查询冲突知识库，构建戏剧张力
- 塑造人物：查询角色设计要素，完善人物小传
- 构建世界观：查询世界观知识库，搭建完整世界生态
- 设计情感戏：查询情绪价值点知识库，戳中观众共情

### 方式2：通过工具手动调用
智能体提供了以下工具供您手动使用：

1. **search_knowledge** - 搜索知识库
   ```python
   # 搜索特定主题
   result = search_knowledge(query="如何设计短剧开篇")
   ```

2. **add_knowledge_content** - 添加知识到知识库
   ```python
   # 添加新的知识内容
   result = add_knowledge_content(
       content="新的编剧技巧...",
       dataset="scriptwriter_knowledge"
   )
   ```

3. **upload_text_file_to_knowledge** - 上传文本文件到知识库
   ```python
   # 上传本地文件
   result = upload_text_file_to_knowledge(
       file_path="/path/to/file.txt",
       dataset="scriptwriter_knowledge"
   )
   ```

4. **upload_url_to_knowledge** - 上传URL内容到知识库
   ```python
   # 上传网页内容
   result = upload_url_to_knowledge(
       url="https://example.com/article",
       dataset="scriptwriter_knowledge"
   )
   ```

5. **batch_upload_files_to_knowledge** - 批量上传文件
   ```python
   # 批量上传多个文件
   result = batch_upload_files_to_knowledge(
       file_paths=["/path/file1.txt", "/path/file2.txt"],
       dataset="scriptwriter_knowledge"
   )
   ```

6. **list_knowledge_datasets** - 列出知识库数据集
   ```python
   # 查看所有数据集
   result = list_knowledge_datasets()
   ```

7. **delete_knowledge_document** - 删除知识库文档
   ```python
   # 删除指定文档
   result = delete_knowledge_document(
       doc_id="文档ID",
       dataset="scriptwriter_knowledge"
   )
   ```

---

## 三、如何更新知识库

### 更新现有内容
当您需要更新知识库中的内容时：

1. **删除旧文档**（可选）
   ```python
   result = delete_knowledge_document(
       doc_id="旧文档ID",
       dataset="scriptwriter_knowledge"
   )
   ```

2. **添加新内容**
   ```python
   result = add_knowledge_content(
       content="更新后的内容...",
       dataset="scriptwriter_knowledge"
   )
   ```

### 上传新内容
当您有新的编剧知识需要添加：

**场景1：添加文本内容**
```python
result = add_knowledge_content(
    content="这里填写新的编剧知识...",
    dataset="scriptwriter_knowledge"
)
```

**场景2：上传本地文件**
1. 将文件保存到 `/tmp/` 或指定目录
2. 使用上传工具：
```python
result = upload_text_file_to_knowledge(
    file_path="/tmp/新编剧技巧.txt",
    dataset="scriptwriter_knowledge"
)
```

**场景3：上传网页内容**
```python
result = upload_url_to_knowledge(
    url="https://example.com/screenwriting-tips",
    dataset="scriptwriter_knowledge"
)
```

**场景4：批量上传多个文件**
```python
result = batch_upload_files_to_knowledge(
    file_paths=[
        "/tmp/技巧1.txt",
        "/tmp/技巧2.txt",
        "/tmp/技巧3.txt"
    ],
    dataset="scriptwriter_knowledge"
)
```

---

## 四、知识库维护建议

### 1. 定期更新
- 每季度检查知识库内容，确保信息时效性
- 根据最新影视作品和市场反馈更新创作技巧

### 2. 分类管理
- 按主题添加内容到对应数据集
- 不同类型的知识不要混用数据集

### 3. 内容质量
- 添加前确保内容准确、实用
- 避免重复内容上传

### 4. 文档大小
- 单次上传建议不超过 50KB
- 大文档建议拆分后分批上传

---

## 五、常见问题

### Q1: 如何查看当前知识库有哪些内容？
```python
result = list_knowledge_datasets()
# 会返回所有数据集及其文档数量
```

### Q2: 如何搜索特定主题的内容？
```python
result = search_knowledge(query="如何设计人物弧光")
# 会返回最相关的内容片段
```

### Q3: 上传的文件格式有什么要求？
- 支持 .txt、.md、.docx 等文本格式
- 建议使用 UTF-8 编码
- 文件大小建议不超过 50KB

### Q4: 如何删除不需要的内容？
```python
# 先查询文档ID
result = search_knowledge(query="要删除的内容")
# 从结果中获取 doc_id，然后删除
delete_knowledge_document(doc_id="...", dataset="...")
```

### Q5: 知识库更新后，智能体是否会立即生效？
是的，知识库内容更新后，智能体在下次创作时会自动检索最新内容。

---

## 六、快速开始示例

### 示例1：添加新的编剧技巧
```
你：我有一些关于悬疑剧伏笔设计的技巧，想添加到知识库
智能体：好的，请提供技巧内容，我会帮你添加到对应的知识库数据集中
你：[提供内容]
智能体：✅ 已成功添加到 scriptwriter_knowledge 数据集
```

### 示例2：上传学习资料
```
你：我下载了一些编剧课程笔记，想上传到知识库
智能体：好的，请将文件保存到 /tmp/ 目录，然后告诉我文件路径
你：文件在 /tmp/编剧课程笔记.txt
智能体：✅ 已成功上传文件，包含 15 个知识块
```

### 示例3：查询特定技巧
```
你：我想了解如何设计短剧的开篇钩子
智能体：[自动检索 hook_knowledge 和 genre_knowledge，返回详细建议]
```

---

## 七、联系方式

如需帮助或有任何问题，请直接与智能体对话，它会为您提供详细的操作指导。
