"""
Performance monitoring and optimization utilities

This module provides tools for monitoring application performance,
identifying bottlenecks, and implementing optimizations.

@author AI Job Readiness Team
@version 1.0.0
"""

import time
import asyncio
import psutil
import logging
from typing import Any, Dict, List, Optional, Callable, Union
from functools import wraps
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict, deque
import threading

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    function_name: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    error_message: Optional[str] = None


class PerformanceMonitor:
    """Monitor application performance metrics"""
    
    def __init__(self, max_metrics: int = 1000):
        self.metrics: deque = deque(maxlen=max_metrics)
        self.function_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "total_calls": 0,
            "total_time": 0.0,
            "avg_time": 0.0,
            "min_time": float('inf'),
            "max_time": 0.0,
            "success_count": 0,
            "error_count": 0,
            "memory_usage": 0.0,
            "cpu_usage": 0.0
        })
        self.lock = threading.Lock()
    
    def record_metric(self, metric: PerformanceMetrics):
        """Record a performance metric"""
        with self.lock:
            self.metrics.append(metric)
            
            # Update function statistics
            stats = self.function_stats[metric.function_name]
            stats["total_calls"] += 1
            stats["total_time"] += metric.execution_time
            stats["avg_time"] = stats["total_time"] / stats["total_calls"]
            stats["min_time"] = min(stats["min_time"], metric.execution_time)
            stats["max_time"] = max(stats["max_time"], metric.execution_time)
            stats["memory_usage"] = metric.memory_usage
            stats["cpu_usage"] = metric.cpu_usage
            
            if metric.success:
                stats["success_count"] += 1
            else:
                stats["error_count"] += 1
    
    def get_function_stats(self, function_name: Optional[str] = None) -> Dict[str, Any]:
        """Get performance statistics for a function or all functions"""
        with self.lock:
            if function_name:
                return dict(self.function_stats.get(function_name, {}))
            return {name: dict(stats) for name, stats in self.function_stats.items()}
    
    def get_slow_functions(self, threshold: float = 1.0) -> List[Dict[str, Any]]:
        """Get functions that exceed the execution time threshold"""
        slow_functions = []
        for name, stats in self.function_stats.items():
            if stats["avg_time"] > threshold:
                slow_functions.append({
                    "function_name": name,
                    "avg_time": stats["avg_time"],
                    "max_time": stats["max_time"],
                    "total_calls": stats["total_calls"],
                    "success_rate": stats["success_count"] / stats["total_calls"] if stats["total_calls"] > 0 else 0
                })
        return sorted(slow_functions, key=lambda x: x["avg_time"], reverse=True)
    
    def get_recent_metrics(self, minutes: int = 5) -> List[PerformanceMetrics]:
        """Get metrics from the last N minutes"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [metric for metric in self.metrics if metric.timestamp >= cutoff_time]
    
    def clear_metrics(self):
        """Clear all stored metrics"""
        with self.lock:
            self.metrics.clear()
            self.function_stats.clear()


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def monitor_performance(function_name: Optional[str] = None):
    """Decorator to monitor function performance"""
    def decorator(func):
        name = function_name or f"{func.__module__}.{func.__name__}"
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            start_cpu = psutil.Process().cpu_percent()
            
            try:
                result = await func(*args, **kwargs)
                success = True
                error_message = None
            except Exception as e:
                success = False
                error_message = str(e)
                raise
            finally:
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                end_cpu = psutil.Process().cpu_percent()
                
                metric = PerformanceMetrics(
                    function_name=name,
                    execution_time=end_time - start_time,
                    memory_usage=end_memory - start_memory,
                    cpu_usage=end_cpu - start_cpu,
                    success=success,
                    error_message=error_message
                )
                performance_monitor.record_metric(metric)
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            start_cpu = psutil.Process().cpu_percent()
            
            try:
                result = func(*args, **kwargs)
                success = True
                error_message = None
            except Exception as e:
                success = False
                error_message = str(e)
                raise
            finally:
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                end_cpu = psutil.Process().cpu_percent()
                
                metric = PerformanceMetrics(
                    function_name=name,
                    execution_time=end_time - start_time,
                    memory_usage=end_memory - start_memory,
                    cpu_usage=end_cpu - start_cpu,
                    success=success,
                    error_message=error_message
                )
                performance_monitor.record_metric(metric)
            
            return result
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class SystemMonitor:
    """Monitor system resources and performance"""
    
    def __init__(self):
        self.cpu_history = deque(maxlen=100)
        self.memory_history = deque(maxlen=100)
        self.disk_history = deque(maxlen=100)
        self.network_history = deque(maxlen=100)
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available / (1024**3)  # GB
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free = disk.free / (1024**3)  # GB
            
            # Network I/O
            network = psutil.net_io_counters()
            
            # Process info
            process = psutil.Process()
            process_memory = process.memory_info().rss / (1024**2)  # MB
            process_cpu = process.cpu_percent()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "percent": cpu_percent,
                    "count": cpu_count,
                    "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
                },
                "memory": {
                    "percent": memory_percent,
                    "available_gb": round(memory_available, 2),
                    "total_gb": round(memory.total / (1024**3), 2)
                },
                "disk": {
                    "percent": disk_percent,
                    "free_gb": round(disk_free, 2),
                    "total_gb": round(disk.total / (1024**3), 2)
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv
                },
                "process": {
                    "memory_mb": round(process_memory, 2),
                    "cpu_percent": process_cpu,
                    "threads": process.num_threads(),
                    "open_files": len(process.open_files()) if hasattr(process, 'open_files') else 0
                }
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {"error": str(e)}
    
    def record_metrics(self):
        """Record current metrics to history"""
        metrics = self.get_system_metrics()
        if "error" not in metrics:
            self.cpu_history.append(metrics["cpu"]["percent"])
            self.memory_history.append(metrics["memory"]["percent"])
            self.disk_history.append(metrics["disk"]["percent"])
            self.network_history.append({
                "bytes_sent": metrics["network"]["bytes_sent"],
                "bytes_recv": metrics["network"]["bytes_recv"]
            })
    
    def get_historical_metrics(self, minutes: int = 5) -> Dict[str, List[float]]:
        """Get historical metrics for the last N minutes"""
        return {
            "cpu": list(self.cpu_history),
            "memory": list(self.memory_history),
            "disk": list(self.disk_history),
            "network": list(self.network_history)
        }
    
    def get_average_metrics(self) -> Dict[str, float]:
        """Get average metrics over the recorded history"""
        return {
            "avg_cpu": sum(self.cpu_history) / len(self.cpu_history) if self.cpu_history else 0,
            "avg_memory": sum(self.memory_history) / len(self.memory_history) if self.memory_history else 0,
            "avg_disk": sum(self.disk_history) / len(self.disk_history) if self.disk_history else 0
        }


# Global system monitor instance
system_monitor = SystemMonitor()


class DatabasePerformanceMonitor:
    """Monitor database performance specifically"""
    
    def __init__(self):
        self.query_times = deque(maxlen=1000)
        self.connection_pool_stats = {}
        self.slow_queries = deque(maxlen=100)
    
    def record_query_time(self, query: str, execution_time: float, success: bool = True):
        """Record database query execution time"""
        self.query_times.append({
            "query": query[:100] + "..." if len(query) > 100 else query,
            "execution_time": execution_time,
            "success": success,
            "timestamp": datetime.now()
        })
        
        # Track slow queries
        if execution_time > 1.0:  # Queries taking more than 1 second
            self.slow_queries.append({
                "query": query,
                "execution_time": execution_time,
                "timestamp": datetime.now()
            })
    
    def get_query_stats(self) -> Dict[str, Any]:
        """Get database query statistics"""
        if not self.query_times:
            return {"total_queries": 0}
        
        times = [q["execution_time"] for q in self.query_times]
        success_count = sum(1 for q in self.query_times if q["success"])
        
        return {
            "total_queries": len(self.query_times),
            "success_rate": success_count / len(self.query_times),
            "avg_execution_time": sum(times) / len(times),
            "min_execution_time": min(times),
            "max_execution_time": max(times),
            "slow_queries_count": len(self.slow_queries)
        }
    
    def get_slow_queries(self) -> List[Dict[str, Any]]:
        """Get list of slow queries"""
        return list(self.slow_queries)


# Global database performance monitor
db_performance_monitor = DatabasePerformanceMonitor()


class PerformanceOptimizer:
    """Optimize application performance based on metrics"""
    
    @staticmethod
    def analyze_bottlenecks() -> Dict[str, Any]:
        """Analyze performance bottlenecks"""
        analysis = {
            "slow_functions": performance_monitor.get_slow_functions(threshold=0.5),
            "system_metrics": system_monitor.get_system_metrics(),
            "query_stats": db_performance_monitor.get_query_stats(),
            "recommendations": []
        }
        
        # Generate recommendations
        recommendations = []
        
        # Check CPU usage
        if analysis["system_metrics"].get("cpu", {}).get("percent", 0) > 80:
            recommendations.append("High CPU usage detected. Consider optimizing CPU-intensive operations.")
        
        # Check memory usage
        if analysis["system_metrics"].get("memory", {}).get("percent", 0) > 85:
            recommendations.append("High memory usage detected. Consider implementing memory optimization.")
        
        # Check slow queries
        if analysis["query_stats"].get("avg_execution_time", 0) > 0.5:
            recommendations.append("Slow database queries detected. Consider adding indexes or optimizing queries.")
        
        # Check slow functions
        if len(analysis["slow_functions"]) > 0:
            recommendations.append(f"Found {len(analysis['slow_functions'])} slow functions. Consider optimization.")
        
        analysis["recommendations"] = recommendations
        return analysis
    
    @staticmethod
    def get_optimization_suggestions() -> List[Dict[str, str]]:
        """Get specific optimization suggestions"""
        suggestions = []
        
        # Database optimizations
        suggestions.extend([
            {
                "category": "Database",
                "suggestion": "Add indexes on frequently queried columns",
                "impact": "High",
                "effort": "Medium"
            },
            {
                "category": "Database",
                "suggestion": "Use connection pooling for better resource management",
                "impact": "High",
                "effort": "Low"
            },
            {
                "category": "Database",
                "suggestion": "Implement query caching for repeated queries",
                "impact": "Medium",
                "effort": "Medium"
            }
        ])
        
        # Application optimizations
        suggestions.extend([
            {
                "category": "Application",
                "suggestion": "Implement async/await for I/O operations",
                "impact": "High",
                "effort": "Medium"
            },
            {
                "category": "Application",
                "suggestion": "Add response caching for static data",
                "impact": "Medium",
                "effort": "Low"
            },
            {
                "category": "Application",
                "suggestion": "Implement pagination for large datasets",
                "impact": "High",
                "effort": "Low"
            }
        ])
        
        # System optimizations
        suggestions.extend([
            {
                "category": "System",
                "suggestion": "Configure appropriate worker processes",
                "impact": "High",
                "effort": "Low"
            },
            {
                "category": "System",
                "suggestion": "Enable gzip compression for responses",
                "impact": "Medium",
                "effort": "Low"
            }
        ])
        
        return suggestions


# Utility functions for performance monitoring
async def start_performance_monitoring():
    """Start background performance monitoring"""
    async def monitor_loop():
        while True:
            try:
                system_monitor.record_metrics()
                await asyncio.sleep(60)  # Record metrics every minute
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(60)
    
    # Start monitoring in background
    asyncio.create_task(monitor_loop())


def get_performance_summary() -> Dict[str, Any]:
    """Get comprehensive performance summary"""
    return {
        "function_stats": performance_monitor.get_function_stats(),
        "system_metrics": system_monitor.get_system_metrics(),
        "database_stats": db_performance_monitor.get_query_stats(),
        "optimization_analysis": PerformanceOptimizer.analyze_bottlenecks(),
        "suggestions": PerformanceOptimizer.get_optimization_suggestions()
    }
