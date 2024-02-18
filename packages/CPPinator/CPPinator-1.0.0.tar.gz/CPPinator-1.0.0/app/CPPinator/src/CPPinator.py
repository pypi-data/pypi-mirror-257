import os
import subprocess
import time


def compile_and_run_cpp_files(directory_path):
    """Compile and run all the .cpp files in the specified directory. The compiled executable is deleted after running the program. The time taken to compile and run each .cpp file is printed, along with the output of the program. If any .cpp file fails to compile or run, the error message is printed, and the total time taken is also printed. The function assumes that the C++ compiler (g++) is installed and added to the system PATH.

    Args:
        directory_path (str): The path of the directory containing the .cpp files.
    """

    a_exe = 'a.exe'  # Name of the compiled executable

    # Change the current working directory to the specified path
    print("Changing working directory...")
    if not os.path.exists(directory_path):
        print(
            f"The specified directory \033[94m{directory_path}\033[0m does not exist.")
        return
    os.chdir(directory_path)
    print(f"Current working directory: \033[94m{os.getcwd()}\033[0m\n")

    # Get all the .cpp files in the directory
    cpp_files = [f for f in os.listdir() if f.endswith(".cpp")]
    if not cpp_files:
        print("No .cpp files found in the directory.")
        return
    print("List of .cpp files:\n")
    for i, cpp_file in enumerate(cpp_files):
        print(f"{i+1}) \033[94m{cpp_file}\033[0m")

    total_time = 0  # Total time taken to compile & run all the .cpp files

    # Run all the .cpp files
    print("\nRunning .cpp files:\n")
    success = True  # Flag to check if all the .cpp files ran successfully
    problem_files = []  # List of .cpp files that failed to compile/run
    for i, cpp_file in enumerate(cpp_files):

        start_time = time.time()

        # Compile the C++ file
        compile_command = ['g++', cpp_file, '-o', a_exe]
        compile_process = subprocess.Popen(
            subprocess.list2cmdline(compile_command),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        _, compile_errors = compile_process.communicate()

        # Compilation successful
        if compile_process.returncode == 0:
            # Run the compiled executable
            run_command = [a_exe]
            run_process = subprocess.Popen(
                subprocess.list2cmdline(run_command),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            run_output, run_errors = run_process.communicate()

            end_time = time.time()
            time_s = round((end_time - start_time), 2)
            total_time += time_s

            if run_errors:
                print(f"Errors while running {cpp_file}:")
                print(run_errors.decode())
            else:
                # Enclose the file name in blue color, and the time taken in seconds in grey color
                print(
                    f"{i+1}) \033[94m{cpp_file}\033[0m \033[90m({time_s}s)\033[0m")
                print(run_output.decode())  # Print the output of the program

        # Compilation failed
        else:
            print(f"Failed to compile {cpp_file}:")
            print(compile_errors.decode())
            success = False
            problem_files.append(cpp_file)

    # Delete the compiled executable
    os.remove(a_exe)

    total_time = round(total_time, 2)

    if success:
        print(
            f"✅ \033[92mRan all C++ files successfully.\033[0m \033[90m({total_time}s)\033[0m")
    else:
        print(
            f"❌ \033[91mSome C++ files failed to compile/run.\033[0m \033[90m({total_time}s)\033[0m")
        print("Problem files:")
        for i, problem_file in enumerate(problem_files):
            print(f"{i+1}) \033[94m{problem_file}\033[0m")


if __name__ == "__main__":

    compile_and_run_cpp_files(directory_path='./Basic Problems/')
