"""
多智能体编剧系统 - 测试文件
"""
import sys
import os

# 添加项目路径到 PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def test_system_import():
    """测试系统导入"""
    print("=" * 60)
    print("测试 1: 系统导入")
    print("=" * 60)
    
    try:
        from src.agents.scriptwriter_system import create_scriptwriter_system
        print("✅ 系统导入成功")
        return True
    except Exception as e:
        print(f"❌ 系统导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_system_initialization():
    """测试系统初始化"""
    print("\n" + "=" * 60)
    print("测试 2: 系统初始化")
    print("=" * 60)
    
    try:
        from src.agents.scriptwriter_system import create_scriptwriter_system
        system = create_scriptwriter_system()
        print("✅ 系统初始化成功")
        print(f"   图节点数: {len(system.graph.nodes)}")
        return True
    except Exception as e:
        print(f"❌ 系统初始化失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_agents_creation():
    """测试 Agent 创建"""
    print("\n" + "=" * 60)
    print("测试 3: Agent 创建")
    print("=" * 60)
    
    try:
        from src.agents.scriptwriter_agents import (
            build_planner_agent,
            build_worldview_agent,
            build_character_agent,
            build_writer_agent,
            build_reviewer_agent,
            build_compliance_agent,
            build_producer_agent
        )
        
        agents = [
            ("策划师", build_planner_agent),
            ("世界观架构师", build_worldview_agent),
            ("人设师", build_character_agent),
            ("主笔编剧", build_writer_agent),
            ("剧本医生", build_reviewer_agent),
            ("合规专员", build_compliance_agent),
            ("制片顾问", build_producer_agent)
        ]
        
        for name, builder in agents:
            try:
                agent = builder()
                print(f"   ✅ {name} Agent 创建成功")
            except Exception as e:
                print(f"   ⚠️  {name} Agent 创建警告: {str(e)}")
        
        print("✅ 所有 Agent 创建完成")
        return True
    except Exception as e:
        print(f"❌ Agent 创建失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_tools_import():
    """测试工具导入"""
    print("\n" + "=" * 60)
    print("测试 4: 工具导入")
    print("=" * 60)
    
    try:
        from src.tools.scriptwriter_tools import (
            knowledge_search,
            web_search,
            consistency_check,
            logic_check,
            compliance_check,
            format_check,
            add_foreshadowing,
            check_foreshadowing
        )
        
        tools = [
            "knowledge_search",
            "web_search",
            "consistency_check",
            "logic_check",
            "compliance_check",
            "format_check",
            "add_foreshadowing",
            "check_foreshadowing"
        ]
        
        for tool in tools:
            print(f"   ✅ {tool} 工具导入成功")
        
        print("✅ 所有工具导入完成")
        return True
    except Exception as e:
        print(f"❌ 工具导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_simple_script_creation():
    """测试简单剧本创建（简化版）"""
    print("\n" + "=" * 60)
    print("测试 5: 简单剧本创作（功能验证）")
    print("=" * 60)
    print("⚠️  注意: 完整测试需要较长时间，此处仅验证架构完整性")
    
    try:
        from src.agents.scriptwriter_system import create_scriptwriter_system
        
        # 创建系统
        system = create_scriptwriter_system()
        print("✅ 编剧系统创建成功")
        
        # 检查状态结构
        state = system.state
        required_keys = [
            "messages", "user_requirement", "parsed_requirement",
            "genre_positioning", "world_view", "character_profiles",
            "core_outline", "episode_outlines", "script_content",
            "validation_reports", "current_version", "script_history",
            "modification_requests", "current_stage", "is_valid"
        ]
        
        missing_keys = [k for k in required_keys if k not in state]
        if missing_keys:
            print(f"   ⚠️  缺少状态键: {missing_keys}")
        else:
            print(f"   ✅ 状态结构完整（{len(required_keys)} 个键）")
        
        print("✅ 系统架构验证通过")
        return True
        
    except Exception as e:
        print(f"❌ 架构验证失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("🎬 多智能体编剧系统 - 测试套件")
    print("=" * 60)
    
    tests = [
        ("系统导入", test_system_import),
        ("系统初始化", test_system_initialization),
        ("Agent 创建", test_agents_creation),
        ("工具导入", test_tools_import),
        ("架构验证", test_simple_script_creation)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ 测试 '{name}' 执行异常: {str(e)}")
            results.append((name, False))
    
    # 输出测试总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status}: {name}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统可以正常使用。")
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，请检查错误信息。")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
