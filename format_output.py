def format_and_print_history(data):
    """
    format the session history and print to the terminal
    
    Args:
        data (list): results from database, each factor is a tuple, 
        which include session_id and created_at
    """
    if not data:
        print("No sessions found in the database.")
        return

    # print the title
    print("\n{:<15}{}".format("Session ID", "Created At"))
    print("-" * 40)  # dividing line

    # print each message
    for session_id, created_at in data:
        print("{:<15}{}".format(session_id, created_at))

    print("-" * 40)