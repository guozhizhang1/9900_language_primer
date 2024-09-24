from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 假设我们用一个列表存储组和学生的信息
groups = [
    {"id": 1, "groupName": "Group 1", "members": [1, 2, 3]},
    {"id": 2, "groupName": "Group 2", "members": [4, 5]},
]
students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "David"},
    {"id": 5, "name": "Eve"},
]

# 添加主页路由
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/groups', methods=['GET'])
def get_groups():
    """
    Route to get all groups
    return: Array of group objects
    """
    # 返回所有组信息
    return jsonify(groups)


@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Route to get all students
    return: Array of student objects
    """
    # 返回所有学生信息
    return jsonify(students)


@app.route('/api/groups', methods=['POST'])
def create_group():
    """
    Route to add a new group
    param groupName: The name of the group (from request body)
    param members: Array of member names (from request body)
    return: The created group object
    """
    # 获取请求体中的数据
    group_data = request.json
    group_name = group_data.get("groupName")
    group_members = group_data.get("members")

    # 检查是否提供了groupName和members
    if not group_name or not group_members:
        abort(400, "Missing group name or members")

    # 初始化成员ID列表
    member_ids = []

    # 遍历成员名字，检查学生是否存在，不存在则添加
    for member_name in group_members:
        # 检查是否有同名学生存在
        student = next((s for s in students if s['name'] == member_name), None)
        if student:
            # 如果学生已存在，将其ID添加到member_ids
            member_ids.append(student['id'])
        else:
            # 如果学生不存在，创建新学生并添加到students列表
            new_student_id = len(students) + 1
            new_student = {"id": new_student_id, "name": member_name}
            students.append(new_student)
            member_ids.append(new_student_id)

    # 自动生成新的组ID
    new_group_id = len(groups) + 1

    # 创建新组对象并添加到groups列表
    new_group = {
        "id": new_group_id,
        "groupName": group_name,
        "members": member_ids  # 存储成员的ID
    }
    groups.append(new_group)

    # 返回创建的组信息
    return jsonify(new_group), 201


@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """
    Route to delete a group by ID
    param group_id: The ID of the group to delete
    return: Empty response with status code 204
    """
    # 查找要删除的组
    group = next((g for g in groups if g['id'] == group_id), None)

    # 如果组不存在，返回404错误
    if group is None:
        abort(404, "Group not found")

    # 删除组
    groups.remove(group)

    # 返回204状态码
    return '', 204

@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """
    Route to get a group by ID (for fetching group members)
    param group_id: The ID of the group to retrieve
    return: The group object with member details
    """
    # 查找指定ID的组
    group = next((g for g in groups if g['id'] == group_id), None)

    # 如果组不存在，返回404错误
    if group is None:
        abort(404, "Group not found")

    # 根据组成员的ID查找学生信息
    member_details = [s for s in students if s['id'] in group['members']]

    # 返回包含成员详细信息的组
    return jsonify({
        "id": group['id'],
        "groupName": group['groupName'],
        "members": member_details
    })


if __name__ == '__main__':
    app.run(port=3902, debug=True)