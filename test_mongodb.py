# test_mongodb.py
from pymongo import MongoClient
import datetime

# 连接字符串（记得把 your-secret-key 换成真实密码）
uri = "mongodb+srv://Olympics:your-secret-key@cluster0.oxulaan.mongodb.net/olympics2026?retryWrites=true&w=majority"

try:
    # 连接
    client = MongoClient(uri)
    
    # 测试连接
    client.admin.command('ping')
    print("✅ 成功连接到 MongoDB Atlas!")
    
    # 选择数据库
    db = client["olympics2026"]
    
    # 插入测试数据
    test_result = db.test.insert_one({
        "message": "连接测试成功",
        "timestamp": datetime.datetime.utcnow()
    })
    print(f"✅ 插入测试数据成功，ID: {test_result.inserted_id}")
    
    # 读取测试数据
    test_data = db.test.find_one()
    print(f"✅ 读取测试数据: {test_data}")
    
    # 创建 houses 集合
    house_data = {
        "_id": "A3",
        "name": "Bari",
        "color": "#FFD733",
        "points": 0
    }
    
    # 检查是否已存在
    if not db.houses.find_one({"_id": "A3"}):
        db.houses.insert_one(house_data)
        print("✅ 创建 houses 集合并添加测试数据")
    else:
        print("ℹ️ houses 集合已存在")
    
    print("\n🎉 所有测试通过！可以开始写主程序了！")
    
except Exception as e:
    print(f"❌ 连接失败: {e}")
    print("\n请检查：")
    print("1. 密码是否正确")
    print("2. IP白名单是否设置了 0.0.0.0/0")
    print("3. 用户名是否为 'Olympics'")