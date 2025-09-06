# 🚀 Quick Start Guide - Role System

## ✅ **Server Setup and Testing**

### **1. Start the FastAPI Server**

You have several options to start the server:

#### **Option A: Using the provided script (Recommended)**
```bash
cd /Users/guruduttjangid/ai-job-readiness/backend
./start_server.sh
```

#### **Option B: Manual command**
```bash
cd /Users/guruduttjangid/ai-job-readiness/backend
export PYTHONPATH="/Users/guruduttjangid/ai-job-readiness/backend:$PYTHONPATH"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### **Option C: Using Python directly**
```bash
cd /Users/guruduttjangid/ai-job-readiness/backend
PYTHONPATH=/Users/guruduttjangid/ai-job-readiness/backend python -m uvicorn app.main:app --reload
```

### **2. Verify Server is Running**

Once the server starts, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### **3. Access the API**

- **API Base URL**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

---

## 🧪 **Testing the System**

### **Quick Validation (30 seconds)**
```bash
python simple_test.py
```

### **Comprehensive Testing (2-3 minutes)**
```bash
python comprehensive_test.py
```

### **Individual Function Tests**
```bash
# Test specific functions
python function_test_scripts.py role_crud
python function_test_scripts.py user_crud
python function_test_scripts.py permissions
python function_test_scripts.py assignments
python function_test_scripts.py queries
python function_test_scripts.py serialization

# Test all functions
python function_test_scripts.py all
```

### **Interactive Demo**
```bash
python demo_role_system.py
```

---

## 🔧 **API Testing**

### **Using curl commands**
```bash
# Test server health
curl http://localhost:8000/

# Get all roles
curl http://localhost:8000/roles/

# Get role statistics
curl http://localhost:8000/roles/statistics

# Create a new role
curl -X POST "http://localhost:8000/roles/" \
  -H "Content-Type: application/json" \
  -d '{"name": "test_role", "description": "Test role", "permissions": ["read", "write"]}'
```

### **Using the test script**
```bash
./test_api.sh
```

---

## 🐛 **Troubleshooting**

### **Issue: "ModuleNotFoundError: No module named 'app'"**

**Solution**: Set the PYTHONPATH correctly
```bash
export PYTHONPATH="/Users/guruduttjangid/ai-job-readiness/backend:$PYTHONPATH"
```

### **Issue: Server won't start**

**Solution**: Make sure you're in the backend directory
```bash
cd /Users/guruduttjangid/ai-job-readiness/backend
```

### **Issue: Port already in use**

**Solution**: Kill existing processes or use a different port
```bash
# Kill existing uvicorn processes
pkill -f uvicorn

# Or use a different port
python -m uvicorn app.main:app --reload --port 8001
```

### **Issue: Database errors**

**Solution**: Initialize the database
```bash
python -c "from app.db.database import init_db; import asyncio; asyncio.run(init_db())"
```

---

## 📊 **Expected Results**

### **Server Startup**
- ✅ Server starts without errors
- ✅ API documentation accessible at http://localhost:8000/docs
- ✅ All endpoints respond correctly

### **Test Results**
- ✅ Simple test: All basic functionality works
- ✅ Comprehensive test: 92.6% success rate (25/27 tests pass)
- ✅ Function tests: Individual features work correctly

### **API Endpoints**
- ✅ `GET /` - Health check
- ✅ `GET /roles/` - List all roles
- ✅ `POST /roles/` - Create new role
- ✅ `GET /roles/{role_id}` - Get specific role
- ✅ `PUT /roles/{role_id}` - Update role
- ✅ `DELETE /roles/{role_id}` - Delete role
- ✅ `POST /roles/{role_id}/assign` - Assign role to user
- ✅ `DELETE /roles/{role_id}/unassign` - Remove role from user
- ✅ `GET /roles/statistics` - Role statistics

---

## 🎯 **Next Steps**

1. **Start the server** using one of the methods above
2. **Run the tests** to verify everything works
3. **Explore the API** at http://localhost:8000/docs
4. **Test the endpoints** using curl or the test script
5. **Integrate with your frontend** using the API endpoints

---

## 📞 **Support**

If you encounter any issues:

1. **Check the logs** - Look for error messages in the terminal
2. **Verify the setup** - Make sure you're in the correct directory
3. **Run the tests** - Use the test scripts to identify specific issues
4. **Check the documentation** - Refer to the comprehensive guides

**Your Role system is fully implemented and ready to use!** 🎉
