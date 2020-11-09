from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Sum

import pytz
import datetime
import matplotlib.pyplot as plt

from .models import Statement

tz = pytz.timezone('Asia/Bangkok')
dateTime = datetime.datetime.now(tz)
date = datetime.date.today()
start_week = date - datetime.timedelta(date.weekday())
end_week = start_week + datetime.timedelta(7)
# Create your views here.
def index(request):
    try:
        statements = Statement.objects.filter(statement_date__range=[start_week, end_week]).order_by('statement_date')
        total_profit = statements.aggregate(profit=Sum('statement_income')-Sum('statement_expense'))
        total_income = statements.aggregate(income=Sum('statement_income'))
        total_expense = statements.aggregate(expense=Sum('statement_expense'))

        if total_income['income'] == None:
            total_income['income'] = 0.0
        if total_expense['expense'] == None:
            total_expense['expense'] = 0.0
        if total_profit['profit'] == None:
            total_profit['profit'] = 0.0

        fig,ax=plt.subplots()
        ax.bar(['Income','Expense'], [abs(total_income['income']),total_expense['expense']], color=['green','red'])
        ax.set_title('Your total income vs. total expense')
        plt.savefig("static/images/graph.jpg")
    except TypeError:
        print('No Data')
    context = {
        'start_week': start_week,
        'end_week': end_week,
        'profit': total_profit['profit'],
        'income': total_income['income'],
        'expense': total_expense['expense'],
        'statement': statements,
    }
    return render(request, 'frontend/index.html', context)

def add_item(request):
    description = request.POST['description']
    itemtype = request.POST['type']
    date = request.POST['expense_date']
    if itemtype == 'Income':
        income = request.POST['amount']
        expense = 0.00
    else:
        income = 0.00
        expense = request.POST['amount']
    Statement.objects.create(statement_description=description, statement_income=income, statement_expense=expense, statement_date=date)
    
    statements = Statement.objects.filter(statement_date__range=[start_week, end_week]).order_by('statement_date')
    total_profit = statements.aggregate(profit=Sum('statement_income')-Sum('statement_expense'))
    total_income = statements.aggregate(income=Sum('statement_income'))
    total_expense = statements.aggregate(expense=Sum('statement_expense'))
    fig,ax=plt.subplots()
    ax.bar(['Income','Expense'], [abs(total_income['income']),total_expense['expense']],color=['green','red'])
    ax.set_title('Your total income vs. total expense')
    plt.savefig("static/images/graph.jpg")
    return redirect('/')

def remove_item(request):
    Id = request.POST.get('delete-id')
    Statement.objects.filter(id=Id).delete()
    return redirect('/')

def list_item(request):
    try:
        statements = Statement.objects.all().order_by('statement_date')
        total_profit = statements.aggregate(profit=Sum('statement_income')-Sum('statement_expense'))
        total_income = statements.aggregate(income=Sum('statement_income'))
        total_expense = statements.aggregate(expense=Sum('statement_expense'))
    except TypeError:
        print('No data')
    context = {
        'profit': total_profit['profit'],
        'income': total_income['income'],
        'expense': total_expense['expense'],
        'statement': statements,
    }
    return render(request, 'frontend/list.html', context)