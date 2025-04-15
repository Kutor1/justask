def format_and_print_history(data):
    """
    美化数据库查询结果并打印到命令行。
    
    Args:
        data (list): 数据库查询结果，每个元素是一个元组，包含 session_id 和 created_at。
    """
    if not data:
        print("No sessions found in the database.")
        return

    # 打印标题行
    print("\n{:<15}{}".format("Session ID", "Created At"))
    print("-" * 40)  # 分隔线

    # 打印每一行数据
    for session_id, created_at in data:
        print("{:<15}{}".format(session_id, created_at))

    print("-" * 40)  # 底部分隔线