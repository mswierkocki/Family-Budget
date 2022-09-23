#!./manage.py shell
# this script is intended to use in django manage shell

import random
from re import L
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware


from django_seed import Seed
from faker import Faker

from budget_app.models import Profile, Budget, Income, Expense, ExpenseCategory


class BudgetSeeder():
  """ Run after creation .run"""
  _counter = 0
  get_random_profile = lambda x=None: (BudgetSeeder.profiles[random.randint(0, BudgetSeeder.profiles_len)])
  
  @staticmethod
  def get_budget_name(x=None):
      BudgetSeeder._counter+=1
      return 'Budget: '+str(BudgetSeeder._counter)
    
  def __init__(self,add_income,add_expense,randomize_shared = False,insert_budgets = 0,insert_profile = 0):
    """_summary_

    Args:
        add_income (_type_): _description_
        add_expense (_type_): _description_
        randomize_shared (bool, optional): _description_. Defaults to False.
        insert_budgets (int, optional): _description_. Defaults to 0.
        insert_profile (int, optional): _description_. Defaults to 0.
    """
    self.fake = Faker()
    self.add_income=add_income
    self.add_expense=add_expense
    self.insert_profile = insert_profile
    self.insert_budgets = insert_budgets
    self.randomize_shared = randomize_shared
    
    BudgetSeeder._counter = Budget.objects.count()
    BudgetSeeder.profiles = list(Profile.objects.all())
    BudgetSeeder.profiles_len = len(BudgetSeeder.profiles) - 1 
    
  def __del__(self):
      del BudgetSeeder._counter
      del BudgetSeeder.profiles
      del BudgetSeeder.profiles_len
      
  def run_budget(self):
    inserted = 0
    if self.insert_budgets>0:
      budget_seeder = Seed.seeder()
      budget_seeder.add_entity(Budget, self.insert_budgets, {
      'name': BudgetSeeder.get_budget_name,
      'owner': lambda x:BudgetSeeder.get_random_profile(),
    })	
      inserted=budget_seeder.execute()
    print("{} Budgets inserted".format(inserted))
    return inserted
  def run_profile(self):
    inserted = 0
    if self.insert_profile > 0: 
      print("insetring profiles".format(self))
      profile_seeder = Seed.seeder()
      profile_seeder.add_entity(User, 3)
      inserted=profile_seeder.execute()
    print("{} profiles inserted".format(inserted))
    return inserted
  def run_randomize(self):
    if self.randomize_shared:
      print("Randomizing shared in budgets")
      for budget in Budget.objects.all():
        l = BudgetSeeder.profiles[:]
        l.remove(budget.owner)
        random.shuffle(l)
        pr_len = len(l)-1
        c = random.randint(0,pr_len)
        while c>0:
            budget.shared.add(l[c])
            c-=1
        budget.save()
  def run(self):
    self.run_profile()
    self.run_budget()
    self.run_randomize()
    
    seeded = Seed.seeder()
    """
    
    """
          
	
    '''
    '''
    bg_list = list(Budget.objects.all())
    bg_list_len = len(bg_list)-1
    get_rng_budget = lambda x=None: (bg_list[random.randint(0, bg_list_len)])
    seeded.add_entity(Income, self.add_income, {
    'date': lambda x: make_aware(self.fake.date_time_this_month()),
    'value': lambda x: random.random()*100,
    'category': lambda x: (Income.Category.choices[random.randint(0, len(Income.Category.choices)-1)][0]),
    'budget':get_rng_budget
    })
    seeded.add_entity(Expense, self.add_expense, {
    'date':  lambda x: make_aware(self.fake.date_time_this_month()),
    'value': lambda x: random.random()*100,
    'category': lambda x: (ExpenseCategory.objects.all()[random.randint(0, ExpenseCategory.objects.count()-1)]),
    'budget':get_rng_budget
    })
    inserted=seeded.execute()
    print(inserted)

    """
import budget_seeder
bs = budget_seeder.BudgetSeeder(1000,1000,True,20)
bs.run()

import importlib
importlib.reload(budget_seeder)

    """
