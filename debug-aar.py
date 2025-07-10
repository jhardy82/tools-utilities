#!/usr/bin/env python3
"""Simplified AAR Monitor Test - Sacred Geometry Framework
Debug version to identify hanging issues
"""

import logging
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_aar_components():
    """Test each AAR component separately"""
    logger.info("[TEST] Starting AAR component testing")

    # Test 1: Basic imports
    try:
        import psutil

        logger.info("[TEST] psutil import: SUCCESS")
    except ImportError as e:
        logger.error(f"[TEST] psutil import: FAILED - {e}")
        return False

    # Test 2: Basic system metrics
    try:
        logger.info("[TEST] Testing CPU metrics...")
        cpu = psutil.cpu_percent(interval=0.1)
        logger.info(f"[TEST] CPU: {cpu}%")
    except Exception as e:
        logger.error(f"[TEST] CPU metrics: FAILED - {e}")
        return False

    # Test 3: Memory metrics
    try:
        logger.info("[TEST] Testing memory metrics...")
        memory = psutil.virtual_memory()
        logger.info(f"[TEST] Memory: {memory.percent}%")
    except Exception as e:
        logger.error(f"[TEST] Memory metrics: FAILED - {e}")
        return False

    # Test 4: Disk metrics
    try:
        logger.info("[TEST] Testing disk metrics...")
        disk_path = os.path.splitdrive(os.getcwd())[0] + os.sep if os.name == 'nt' else '/'
        disk = psutil.disk_usage(disk_path)
        logger.info(f"[TEST] Disk: {disk.percent}% on {disk_path}")
    except Exception as e:
        logger.error(f"[TEST] Disk metrics: FAILED - {e}")
        try:
            disk = psutil.disk_usage('.')
            logger.info(f"[TEST] Disk (fallback): {disk.percent}%")
        except Exception as e2:
            logger.error(f"[TEST] Disk fallback: FAILED - {e2}")
            return False

    # Test 5: Process enumeration
    try:
        logger.info("[TEST] Testing process enumeration...")
        processes = list(psutil.process_iter(["pid", "name"]))
        logger.info(f"[TEST] Found {len(processes)} processes")
    except Exception as e:
        logger.error(f"[TEST] Process enumeration: FAILED - {e}")
        return False

    # Test 6: File system operations
    try:
        logger.info("[TEST] Testing file system operations...")
        workspace = sys.argv[1] if len(sys.argv) > 1 else '.'
        files = os.listdir(workspace)
        logger.info(f"[TEST] Workspace files: {len(files)} items")
    except Exception as e:
        logger.error(f"[TEST] File system: FAILED - {e}")
        return False

    logger.info("[TEST] All AAR components tested successfully")
    return True


def test_minimal_cycle():
    """Test a minimal monitoring cycle"""
    logger.info("[CYCLE] Starting minimal AAR cycle")

    try:
        # Minimal metrics collection
        import psutil
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': psutil.virtual_memory().percent,
            'process_count': len(list(psutil.process_iter()))
        }

        logger.info(f"[CYCLE] Metrics collected: {metrics}")
        logger.info("[CYCLE] Minimal cycle completed successfully")
        return True

    except Exception as e:
        logger.error(f"[CYCLE] Minimal cycle failed: {e}")
        return False


if __name__ == "__main__":
    logger.info("[START] AAR Debug Test")

    # Run component tests
    if not test_aar_components():
        logger.error("[FAIL] Component tests failed")
        sys.exit(1)

    # Run minimal cycle test
    if not test_minimal_cycle():
        logger.error("[FAIL] Minimal cycle test failed")
        sys.exit(1)

    logger.info("[SUCCESS] All AAR tests passed")
    print("AAR system components are working correctly")
