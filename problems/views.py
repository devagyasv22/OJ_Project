# problems/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import Problem
from .testcases_model import TestCase
from .test_runner import run_test_cases
from compiler.forms import CodeSubmissionForm
from compiler.models import CodeSubmission
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import traceback
import uuid
import subprocess
from pathlib import Path
import google.generativeai as genai
# import google.generativeai as genai
from django.conf import settings

# Configure Gemini API once using settings
genai.configure(api_key=settings.GEMINI_API_KEY)


# AI REVIEW ENDPOINT

import traceback

import traceback
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ai_review_code(request, problem_id):  
    print(f"AI Review called with method: {request.method}, problem_id: {problem_id}")
    
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    code = request.POST.get("code")
    result = request.POST.get("result", "")

    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)

    try:
        # Check API key before calling
        from django.conf import settings
        print("Gemini API Key present:", bool(getattr(settings, "GEMINI_API_KEY", None)))
        genai.configure(api_key=settings.GEMINI_API_KEY)

        prompt = (
            f"Review this solution:\n{code}\n\n"
            f"Test Case Result: {result}\n"
            f"Provide helpful improvement suggestions."
        )

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        print("Full Gemini response object:", response)

        feedback_text = ""
        if hasattr(response, "text"):
            feedback_text = response.text.strip()
        elif hasattr(response, "candidates"):
            feedback_text = "".join(
                part.text for part in response.candidates[0].content.parts
            )

        if not feedback_text:
            return JsonResponse({"error": "Empty AI response"}, status=502)

        return JsonResponse({"feedback": feedback_text})

    except Exception as e:
        print("AI review error:", repr(e))
        traceback.print_exc()
        return JsonResponse({"error": repr(e)}, status=500)




# PROBLEM LIST & DETAIL
def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problems/problem_list.html', {'problems': problems})


def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    form = CodeSubmissionForm()
    return render(request, 'problems/problem_detail.html', {
        'problem': problem,
        'form': form,
        'testcases': TestCase.objects.filter(problem=problem),
        'submission': None,
    })



# SUBMIT CODE HANDLER
def submit_code(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    form = CodeSubmissionForm(request.POST or None)
    testcases = TestCase.objects.filter(problem=problem)

    context = {
        'problem': problem,
        'form': form,
        'testcases': testcases,
        'custom_output': None,
        'results': None,
        'submission': None,
    }

    if request.method == 'POST' and form.is_valid():
        submission = form.save(commit=False)
        submission.problem = problem
        action = request.POST.get('action')

        if action == 'custom':
            custom_input = form.cleaned_data.get('input_data', '') or ''
            context['custom_output'] = run_code(submission.language, submission.code, custom_input)

        elif action == 'run_all':
            results = run_test_cases(submission.language, submission.code, problem_id)
            all_passed = bool(results) and all(tc.get("passed", False) for tc in results)
            
            submission.output_data = str(results)
            submission.passed = all_passed
            submission.save()

            context['results'] = results
            context['submission'] = submission

    return render(request, 'problems/problem_detail.html', context)


# -------------------------
# RUN CODE UTILITY
# -------------------------
def run_code(language, code, input_data):
    base_path = Path(settings.BASE_DIR)
    uid = str(uuid.uuid4())

    extensions = {'cpp': 'cpp', 'py': 'py', 'java': 'java'}
    ext = extensions.get(language, 'txt')

    code_path = base_path / f"temp_{uid}.{ext}"
    input_path = base_path / f"input_{uid}.txt"
    output_path = base_path / f"output_{uid}.txt"

    code_path.write_text(code)
    input_path.write_text(input_data or "")

    try:
        if language == 'cpp':
            exe = base_path / f"prog_{uid}"
            compile_proc = subprocess.run(
                ['g++', str(code_path), '-o', str(exe)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if compile_proc.returncode != 0:
                return f"Compilation Error:\n{compile_proc.stderr}"
            try:
                subprocess.run(
                    [str(exe)],
                    stdin=open(input_path, 'r'),
                    stdout=open(output_path, 'w'),
                    timeout=2
                )
            except subprocess.TimeoutExpired:
                return "Time Limit Exceeded"

        elif language == 'py':
            try:
                subprocess.run(
                    ['python3', str(code_path)],
                    stdin=open(input_path, 'r'),
                    stdout=open(output_path, 'w'),
                    timeout=2
                )
            except subprocess.TimeoutExpired:
                return "Time Limit Exceeded"

        elif language == 'java':
            java_file = base_path / f"Main_{uid}.java"
            java_file.write_text(code)
            compile_proc = subprocess.run(
                ['javac', str(java_file)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if compile_proc.returncode != 0:
                return f"Compilation Error:\n{compile_proc.stderr}"
            try:
                subprocess.run(
                    ['java', '-cp', str(base_path), f"Main_{uid}"],
                    stdin=open(input_path, 'r'),
                    stdout=open(output_path, 'w'),
                    timeout=2
                )
            except subprocess.TimeoutExpired:
                return "Time Limit Exceeded"

        else:
            return "Unsupported language"

        return output_path.read_text()

    finally:
        # Optional: cleanup temporary files
        pass
