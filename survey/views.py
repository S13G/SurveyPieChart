import base64

from django.shortcuts import render
from matplotlib.patches import Shadow

from .forms import SurveyForm
from .models import Survey
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import PIL.Image


# Create your views here.


def home(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            # Save the survey answers to the database
            question = form.cleaned_data['question']
            answer = form.cleaned_data['answer']
            user = request.user
            survey = Survey(question=question, answer=answer, user=user)
            survey.save()
            return render(request, 'survey_results.html')
    else:
        form = SurveyForm()
    return render(request, 'home.html', {'form': form})


def survey_results(request):
    data = Survey.objects.values('question', 'answer', 'user')
    df = pd.DataFrame.from_records(data)
    answer_counts = df.answer.value_counts()
    answer_percentages = answer_counts / df.answer.count() * 100
    plt.pie(answer_percentages, labels=answer_counts.index, autopct='%.1f%%', radius=1.2)
    plt.legend(answer_counts.index, loc="best")
    plt.title("Survey Results")
    plt.gcf().set_facecolor("#F5F5F5")

    # Save the chart to a file-like buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Embed the buffer in a `data:` URL
    image_data = base64.b64encode(buffer.getvalue()).decode()
    chart = f'data:image/png;base64,{image_data}'

    # Render the template
    return render(request, 'survey_results.html', {'chart': chart})



# def survey_results(request):
#     data = Survey.objects.values('question', 'answer', 'user')
#     df = pd.DataFrame.from_records(data)
#     answer_counts = df.answer.value_counts()
#     answer_percentages = answer_counts / df.answer.count() * 100
#
#     # Create a pie chart
#     fig = plt.figure()
#     fig.set_size_inches(10, 10, forward=True)
#     explode = [0 for _ in range(len(answer_counts))]
#     explode[i] = 0.1
#     colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ffcccc']
#     plt.pie(answer_percentages, labels=answer_counts.index, autopct='%.1f%%', colors=colors, explode=explode)
#     plt.gca().add_patch(Shadow(offset=(2, 2), alpha=0.3))
#     plt.title("Survey Results")
#     plt.legend(answer_counts.index, loc="best")
#     plt.gcf().set_facecolor("#F5F5F5")
#
#     # Save the chart to a file-like buffer
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#
#     # Embed the buffer in a `data:` URL
#     image_data = base64.b64encode(buffer.getvalue()).decode()
#     chart = f'data:image/png;base64,{image_data}'
#
#     # Render the template
#     return render(request, 'survey_results.html', {'chart': chart})
