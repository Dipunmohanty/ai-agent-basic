from functions.run_python_file import run_python_file


res1 = run_python_file("calculator", "main.py")
print(res1)
res2 = run_python_file("calculator", "main.py", ["3 + 5"])
print(res2)
res3 = run_python_file("calculator", "tests.py")
print(res3)
res4 = run_python_file("calculator", "../main.py")
print(res4)
res5 = run_python_file("calculator", "nonexistent.py")
print(res5)
res6 = run_python_file("calculator", "lorem.txt")
print(res6)