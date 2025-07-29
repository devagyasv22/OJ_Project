from django.shortcuts import render, get_object_or_404
from .models import Problem
import os
from django.shortcuts import render, redirect
from compiler.forms import CodeSubmissionForm
from compiler.models import CodeSubmission
import uuid, subprocess
from pathlib import Path
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .testcases_model import TestCase
import os
from .testcases_model import TestCase
from .test_runner import run_test_cases


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai

genai.configure(api_key="AIzaSyDC5cf4YCC0-nST3vlNHiY0cU7Of73Yq50")

@csrf_exempt
def ai_review(request):
    print(f"AI Review called with method: {request.method}")
    
    if request.method == "POST":
        code = request.POST.get("code")
        result = request.POST.get("result")
        
        print(f"Code length: {len(code) if code else 0}")
        print(f"Result: {result}")

        if not code:
            return JsonResponse({"error": "No code provided"}, status=400)

        try:
            prompt = f"Review this solution:\n{code}\n\nTest Case Result: {result}\nProvide helpful improvement suggestions."

            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            
            print(f"AI response received: {len(response.text) if response.text else 0} characters")

            return JsonResponse({"feedback": response.text})
        
        except Exception as e:
            print(f"Error in AI review: {str(e)}")
            return JsonResponse({"error": f"AI review failed: {str(e)}"}, status=500)
    elif request.method == "GET":
        return JsonResponse({
            "error": "This endpoint is for AI code review via POST requests only",
            "message": "Please use the AI Review button on a problem page"
        }, status=405)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problems/problem_list.html', {'problems': problems})

def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    form = CodeSubmissionForm()
    testcases = problem.testcases.all()  # Related name from your TestCase model
    submission=None
    return render(request, 'problems/problem_detail.html', {
    'problem': problem,
    'form': form,
    'testcases': TestCase.objects.filter(problem=problem),
    "submission": submission,
})




from .testcases_model import TestCase

def submit_code(request, problem_id):
    problem    = get_object_or_404(Problem, id=problem_id)
    form       = CodeSubmissionForm(request.POST or None)
    testcases  = TestCase.objects.filter(problem=problem)
    
    # Prepare context with defaults
    custom_output = None
    results       = None
    submission    = None

    if request.method == 'POST' and form.is_valid():
        submission = form.save(commit=False)
        submission.problem = problem

        action = request.POST.get('action')
        
        # 1) Custom input run
        if action == 'custom':
            custom_input   = form.cleaned_data.get('input_data', '') or ''
            custom_output  = run_code(submission.language,
                                      submission.code,
                                      custom_input)
            # We do NOT save submission for custom runs

        # 2) Run all testcases
        elif action == 'run_all':
            results = run_test_cases(submission.language, submission.code, problem_id)
            
            # Calculate overall pass status
            if not results:
                # No test cases found
                all_passed = False
                print("No test cases found for this problem")
            else:
                # Check if all test cases passed
                all_passed = all(tc.get("passed", False) for tc in results)
                print("results:", results)
                print("all_passed calculated:", all_passed)
            
            submission.output_data = str(results)
            submission.passed = all_passed
            submission.save()

    # Render same template with everything—no separate result.html
    return render(request, 'problems/problem_detail.html', {
        'problem':       problem,
        'form':          form,
        'testcases':     testcases,
        'custom_output': custom_output,
        'results':       results,
        'submission':    submission,
    })


def run_code(language, code, input_data):
    BASE = Path(settings.BASE_DIR)
    uid  = str(uuid.uuid4())
    ext  = 'cpp' if language=='cpp' else 'py' if language=='py' else 'java'
    code_path  = BASE / f"temp_{uid}.{ext}"
    input_path = BASE / f"input_{uid}.txt"
    output_path= BASE / f"output_{uid}.txt"

    code_path.write_text(code)
    input_path.write_text(input_data or "")

    if language == 'cpp':
        exe = BASE / f"prog_{uid}"
        proc = subprocess.run(
            ['g++', str(code_path), '-o', str(exe)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            return f"Compilation Error:\n{proc.stderr}"
        subprocess.run([str(exe)], stdin=open(input_path,'r'), stdout=open(output_path,'w'))

    elif language == 'py':
        subprocess.run(['python3', str(code_path)],
                       stdin=open(input_path,'r'), stdout=open(output_path,'w'))

    else:  # java
        java_file = BASE / f"Main_{uid}.java"
        java_file.write_text(code)
        cp = subprocess.run(
            ['javac', str(java_file)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if cp.returncode != 0:
            return f"Compilation Error:\n{cp.stderr}"
        subprocess.run(['java','-cp',str(BASE),f"Main_{uid}"],
                       stdin=open(input_path,'r'), stdout=open(output_path,'w'))

    return output_path.read_text()