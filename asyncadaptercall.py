import asyncio
import os

async def run_python_file(file):
    command = f"python {file}"
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    print(f"Output for {file}:\n{stdout.decode()}")
    if stderr:
        print(f"Error for {file}:\n{stderr.decode()}")

async def run_all_python_files(folder):
    files = [file for file in os.listdir(folder) if file.endswith(".py")]
    tasks = [run_python_file(os.path.join(folder, file)) for file in files]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    folder_path = "adapter"  # Replace with the path to your folder containing Python files
    asyncio.run(run_all_python_files(folder_path))