from datetime import datetime

def write_error(error_message: str) -> None:
    with open("src/utils/logs/error.log" , 'a') as error_writer:
        error_writer.write(datetime.now().strftime("%d de %B de %Y, %I:%M %p") + error_message)
        

def write_usage(usage_command: str) -> None:
    with open("src/utils/logs/usage.log" , 'a') as error_writer:
        error_writer.write(f"{datetime.now().strftime("%d de %B de %Y, %I:%M %p")}: {usage_command}\n")
