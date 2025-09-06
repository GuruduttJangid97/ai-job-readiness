#!/usr/bin/env python3
"""
Master Test Runner for Role Management System

This script runs all test suites for the Role Management System in sequence,
providing a comprehensive validation of the entire system.

Usage:
    python tests/run_tests.py [--skip-api] [--skip-performance] [--skip-security] [--skip-integration]

Author: AI Job Readiness Team
Version: 2.0.0
"""

import asyncio
import argparse
import sys
import time
from typing import List, Dict, Any
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import test modules from organized structure
from tests.unit.test_roles_simple import test_role_system
from tests.performance.test_role_performance import PerformanceTester
from tests.security.test_role_security import SecurityTester

# Optional imports for tests that may have missing dependencies
try:
    from tests.integration.test_role_integration import IntegrationTester
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Integration tests not available: {e}")
    INTEGRATION_AVAILABLE = False

try:
    from tests.api.test_role_api import APITester
    API_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ API tests not available: {e}")
    API_AVAILABLE = False


class TestRunner:
    """Master test runner for all role management tests."""
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.start_time = time.time()
    
    async def run_basic_tests(self) -> Dict[str, Any]:
        """Run basic functionality tests."""
        print("🧪 Running Basic Functionality Tests")
        print("=" * 50)
        
        start_time = time.time()
        try:
            await test_role_system()
            duration = time.time() - start_time
            return {
                "name": "Basic Functionality",
                "status": "PASSED",
                "duration": duration,
                "message": "All basic functionality tests passed"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "name": "Basic Functionality",
                "status": "FAILED",
                "duration": duration,
                "message": f"Basic functionality tests failed: {str(e)}"
            }
    
    async def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance tests."""
        print("\n⚡ Running Performance Tests")
        print("=" * 50)
        
        start_time = time.time()
        try:
            tester = PerformanceTester()
            await tester.run_all_performance_tests()
            duration = time.time() - start_time
            return {
                "name": "Performance Tests",
                "status": "PASSED",
                "duration": duration,
                "message": "All performance tests passed"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "name": "Performance Tests",
                "status": "FAILED",
                "duration": duration,
                "message": f"Performance tests failed: {str(e)}"
            }
    
    async def run_security_tests(self) -> Dict[str, Any]:
        """Run security tests."""
        print("\n🔒 Running Security Tests")
        print("=" * 50)
        
        start_time = time.time()
        try:
            tester = SecurityTester()
            await tester.run_all_security_tests()
            duration = time.time() - start_time
            return {
                "name": "Security Tests",
                "status": "PASSED",
                "duration": duration,
                "message": "All security tests passed"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "name": "Security Tests",
                "status": "FAILED",
                "duration": duration,
                "message": f"Security tests failed: {str(e)}"
            }
    
    async def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests."""
        print("\n🔗 Running Integration Tests")
        print("=" * 50)
        
        if not INTEGRATION_AVAILABLE:
            return {
                "name": "Integration Tests",
                "status": "SKIPPED",
                "duration": 0,
                "message": "Integration tests not available (missing dependencies)"
            }
        
        start_time = time.time()
        try:
            tester = IntegrationTester()
            await tester.run_all_integration_tests()
            duration = time.time() - start_time
            return {
                "name": "Integration Tests",
                "status": "PASSED",
                "duration": duration,
                "message": "All integration tests passed"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "name": "Integration Tests",
                "status": "FAILED",
                "duration": duration,
                "message": f"Integration tests failed: {str(e)}"
            }
    
    async def run_api_tests(self) -> Dict[str, Any]:
        """Run API tests."""
        print("\n🌐 Running API Tests")
        print("=" * 50)
        
        if not API_AVAILABLE:
            return {
                "name": "API Tests",
                "status": "SKIPPED",
                "duration": 0,
                "message": "API tests not available (missing dependencies)"
            }
        
        start_time = time.time()
        try:
            tester = APITester()
            await tester.run_all_api_tests()
            duration = time.time() - start_time
            return {
                "name": "API Tests",
                "status": "PASSED",
                "duration": duration,
                "message": "All API tests passed"
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "name": "API Tests",
                "status": "FAILED",
                "duration": duration,
                "message": f"API tests failed: {str(e)}"
            }
    
    def print_summary(self):
        """Print test summary."""
        total_duration = time.time() - self.start_time
        passed = sum(1 for result in self.results if result["status"] == "PASSED")
        failed = sum(1 for result in self.results if result["status"] == "FAILED")
        total = len(self.results)
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Total Duration: {total_duration:.2f}s")
        print("=" * 60)
        
        print("\nTest Name                 Status     Duration")
        print("-" * 50)
        for result in self.results:
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            print(f"{result['name']:<25} {status_icon} {result['status']:<8} {result['duration']:.2f}s")
        
        if failed > 0:
            print(f"\n💥 {failed} test(s) failed. Please check the output above for details.")
        else:
            print("\n🎉 All tests passed successfully!")
    
    async def run_all_tests(self, skip_api=False, skip_performance=False, 
                          skip_security=False, skip_integration=False):
        """Run all test suites."""
        print("🚀 Starting Role Management System Test Suite")
        print("=" * 60)
        
        # Run basic functionality tests (always run)
        result = await self.run_basic_tests()
        self.results.append(result)
        
        # Run performance tests
        if not skip_performance:
            result = await self.run_performance_tests()
            self.results.append(result)
        else:
            print("\n⏭️ Skipping Performance Tests")
        
        # Run security tests
        if not skip_security:
            result = await self.run_security_tests()
            self.results.append(result)
        else:
            print("\n⏭️ Skipping Security Tests")
        
        # Run integration tests
        if not skip_integration:
            result = await self.run_integration_tests()
            self.results.append(result)
        else:
            print("\n⏭️ Skipping Integration Tests")
        
        # Run API tests
        if not skip_api:
            result = await self.run_api_tests()
            self.results.append(result)
        else:
            print("\n⏭️ Skipping API Tests")
        
        # Print summary
        self.print_summary()


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run Role Management System Tests")
    parser.add_argument("--skip-api", action="store_true", help="Skip API tests")
    parser.add_argument("--skip-performance", action="store_true", help="Skip performance tests")
    parser.add_argument("--skip-security", action="store_true", help="Skip security tests")
    parser.add_argument("--skip-integration", action="store_true", help="Skip integration tests")
    parser.add_argument("--only-unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--only-performance", action="store_true", help="Run only performance tests")
    parser.add_argument("--only-security", action="store_true", help="Run only security tests")
    parser.add_argument("--only-integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--only-api", action="store_true", help="Run only API tests")
    
    args = parser.parse_args()
    
    # Handle "only" options
    if args.only_unit:
        args.skip_api = True
        args.skip_performance = True
        args.skip_security = True
        args.skip_integration = True
    elif args.only_performance:
        args.skip_api = True
        args.skip_security = True
        args.skip_integration = True
    elif args.only_security:
        args.skip_api = True
        args.skip_performance = True
        args.skip_integration = True
    elif args.only_integration:
        args.skip_api = True
        args.skip_performance = True
        args.skip_security = True
    elif args.only_api:
        args.skip_performance = True
        args.skip_security = True
        args.skip_integration = True
    
    runner = TestRunner()
    await runner.run_all_tests(
        skip_api=args.skip_api,
        skip_performance=args.skip_performance,
        skip_security=args.skip_security,
        skip_integration=args.skip_integration
    )


if __name__ == "__main__":
    asyncio.run(main())
