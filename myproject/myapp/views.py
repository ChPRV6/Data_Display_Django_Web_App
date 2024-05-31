import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            try:
                summary = generate_summary_report(uploaded_file)
                return render(request, 'summary.html', {'summary': summary.to_dict(orient='records')})
            except Exception as e:
                return HttpResponse(f'Error processing file: {e}')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def generate_summary_report(file):
    try:
        data = pd.read_csv(file)
    except pd.errors.ParserError:
        raise Exception("Failed to read the CSV file. Please check the file format.")
    
    summary = data.groupby(['Cust State', 'DPD']).size().reset_index(name='Count')
    summary.rename(columns={'Cust State': 'State'}, inplace=True)
    return summary
