from functions.get_file_content import get_file_content

def run_file_test(folder, file, full_content=False):
    result = get_file_content(folder, file)
    if result.startswith("Error"):
        print(result)
    elif full_content==True:
        print(result)
    else:
        print(f"{file} length: {len(result)}")
        print(f"{file} truncated: {'truncated' in result}")
    

run_file_test("calculator", "lorem.txt")                    # summary
run_file_test("calculator", "main.py", full_content=True)   # full print
run_file_test("calculator", "pkg/calculator.py", full_content=True)
run_file_test("calculator", "/bin/cat")                     # error
run_file_test("calculator", "pkg/does_not_exist.py")        # error

