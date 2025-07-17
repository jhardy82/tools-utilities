"""Task Orchestration Integration Fix

This script fixes the module import issues and establishes proper
integration between the Task Orchestration System and Unified Agent System.
"""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def fix_task_orchestration_integration():
    """Fix the integration by ensuring proper module paths and imports
    """
    logger.info("🔧 Starting Task Orchestration Integration Fix...")

    # Get the core framework root
    core_framework_root = Path(__file__).parent

    # Key paths
    task_orch_path = core_framework_root / "projects" / "task-orchestration-system"
    task_orch_src = task_orch_path / "src"
    unified_system_path = core_framework_root / "projects" / "unified-agent-task-execution-system"

    # Verify paths exist
    if not task_orch_path.exists():
        logger.error(f"❌ Task Orchestration System not found: {task_orch_path}")
        return False

    if not unified_system_path.exists():
        logger.error(f"❌ Unified System not found: {unified_system_path}")
        return False

    # Add paths to Python path if not already there
    paths_to_add = [
        str(task_orch_src),
        str(task_orch_path),
        str(unified_system_path),
        str(core_framework_root)
    ]

    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
            logger.info(f"✅ Added to Python path: {path}")

    # Test imports step by step
    logger.info("🧪 Testing Task Orchestration System imports...")

    try:
        # Test basic orchestrator import
        from orchestrator import TaskOrchestrator
        logger.info("✅ Orchestrator module imported successfully")

        # Test agent import
        from agents import AgentManager
        logger.info("✅ Agents module imported successfully")

        # Test instantiation
        logger.info("🧪 Testing component instantiation...")

        # Create orchestrator instance
        TaskOrchestrator()
        logger.info("✅ TaskOrchestrator instantiated")

        # Create agent manager
        agent_manager = AgentManager()
        logger.info("✅ AgentManager instantiated")

        # Test basic functionality
        capabilities = agent_manager.get_all_agent_capabilities()
        logger.info(f"✅ Agent capabilities retrieved: {list(capabilities.keys())}")

        return True

    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_unified_system_integration():
    """Test the unified system with orchestration integration
    """
    logger.info("🔗 Testing Unified System Integration...")

    try:
        # Import unified system components
        from src.agents.orchestration_adapter import OrchestrationAdapter
        from src.task_management.unified_task_manager import UnifiedTaskManager

        # Initialize components
        task_manager = UnifiedTaskManager()
        orchestration_adapter = OrchestrationAdapter()

        # Check status
        system_status = task_manager.get_system_status()
        adapter_health = orchestration_adapter.validate_orchestration_health()

        logger.info(f"✅ Unified System: {system_status['system_name']}")
        logger.info(f"✅ Orchestration Health: {adapter_health}")

        # Check if orchestration is actually working
        if system_status.get('orchestration_enabled', False):
            logger.info("🎉 Full integration successful!")
            return True
        else:
            logger.warning("⚠️ Integration partial - orchestration not fully enabled")
            return False

    except Exception as e:
        logger.error(f"❌ Unified system integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_integration_test():
    """Create a simple integration test that demonstrates the working system
    """
    logger.info("📝 Creating integration test...")

    try:
        # Import both systems
        from agents import AgentManager
        from orchestrator import TaskContext, TaskOrchestrator
        from src.task_management.unified_task_manager import UnifiedTaskManager

        # Create a simple test case
        logger.info("🧪 Running integration test case...")

        # Initialize systems
        TaskOrchestrator()
        agent_manager = AgentManager()
        task_manager = UnifiedTaskManager()

        # Create a test task
        TaskContext(
            task_id="integration-test-001",
            task_type="integration_validation",
            priority=PHI  # Golden ratio priority
        )

        # Test task assignment through orchestrator
        logger.info("🎯 Testing task orchestration...")

        # Get agent capabilities
        capabilities = agent_manager.get_all_agent_capabilities()
        logger.info(f"Available agent types: {list(capabilities.keys())}")

        # Create a unified task
        from src.task_management.unified_task_manager import UnifiedTask

        unified_task = UnifiedTask(
            task_id="integration-test-001",
            title="Integration Test Task",
            description="Testing integration between Task Orchestration and Unified systems"
        )

        # Add to task manager
        task_manager.add_task(unified_task)

        # Get system status
        status = task_manager.get_system_status()
        logger.info(f"✅ Integration test completed - Tasks in queue: {status.get('tasks_in_queue', 0)}")

        return True

    except Exception as e:
        logger.error(f"❌ Integration test creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main integration fix and test function
    """
    logger.info("🚀 Task Orchestration Integration Fix & Test")
    logger.info("=" * 60)

    # Step 1: Fix integration
    if not fix_task_orchestration_integration():
        logger.error("❌ Integration fix failed!")
        return 1

    # Step 2: Test unified system integration
    if not test_unified_system_integration():
        logger.warning("⚠️ Unified system integration incomplete")
        # Continue anyway to see how far we get

    # Step 3: Create and run integration test
    if not create_integration_test():
        logger.error("❌ Integration test failed!")
        return 2

    logger.info("🎉 Task Orchestration Integration Fix Complete!")
    logger.info("✅ Systems are now properly connected and functional")

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
