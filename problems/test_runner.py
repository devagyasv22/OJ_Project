import subprocess
import os
import uuid
from pathlib import Path
from django.conf import settings

def run_test_cases(language, code, problem_id):
    test_case_dir = os.path.join(os.path.dirname(__file__), 'testcases', f'problem_{problem_id}')
    results = []
    i = 1
    BASE = Path(settings.BASE_DIR)
    uid = str(uuid.uuid4())

    if language == 'cpp':
        ext = 'cpp'
        source_path = BASE / f"temp_{uid}.cpp"
        executable_path = BASE / f"temp_{uid}_exec"
        source_path.write_text(code)

        compile_result = subprocess.run(['g++', str(source_path), '-o', str(executable_path)], capture_output=True)
        if compile_result.returncode != 0:
            return [{
                'testcase': 0,
                'passed': False,
                'error': compile_result.stderr.decode()
            }]

    elif language == 'java':
        ext = 'java'
        class_name = f"Main{uid.replace('-', '')}"
        code = code.replace('class Main', f'class {class_name}')
        source_path = BASE / f"{class_name}.java"
        source_path.write_text(code)

        compile_result = subprocess.run(['javac', str(source_path)], capture_output=True)
        if compile_result.returncode != 0:
            return [{
                'testcase': 0,
                'passed': False,
                'error': compile_result.stderr.decode()
            }]

    else:  # Python
        ext = 'py'
        source_path = BASE / f"temp_{uid}.py"
        source_path.write_text(code)

    while True:
        input_file = os.path.join(test_case_dir, f'input{i}.txt')
        output_file = os.path.join(test_case_dir, f'output{i}.txt')

        if not os.path.exists(input_file) or not os.path.exists(output_file):
            break

        with open(input_file, 'r') as f_in:
            expected_output = open(output_file, 'r').read().strip()
            try:
                if language == 'cpp':
                    result = subprocess.run(
                        [str(executable_path)],
                        input=f_in.read(),
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                elif language == 'java':
                    result = subprocess.run(
                        ['java', '-cp', str(BASE), class_name],
                        input=f_in.read(),
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                else:  
                    result = subprocess.run(
                        ['python3', str(source_path)],
                        input=f_in.read(),
                        capture_output=True,
                        text=True,
                        timeout=2
                    )

                actual_output = result.stdout.strip()
                results.append({
                    'testcase': i,
                    'passed': actual_output == expected_output,
                    'expected': expected_output,
                    'actual': actual_output
                })

            except subprocess.TimeoutExpired:
                results.append({
                    'testcase': i,
                    'passed': False,
                    'error': 'Time Limit Exceeded'
                })

        i += 1

    return results
