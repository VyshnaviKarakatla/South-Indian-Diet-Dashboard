#Importing pandas library
import pandas as pd

#Load and preprocess a diet CSV file
person_data=pd.read_csv('south_indian_diet.csv')

#Remove duplicate rows
person_data.drop_duplicates()

#Handle missing or inconsistent values
person_data.fillna('None')

#Standardize date format
person_data['Date']=pd.to_datetime(person_data['Date'])

#Validate numeric fields (height, weight, calories, protein)
person_data['Height_cm'].dtype #int
person_data['Weight_kg'].dtype #float
person_data['Calories'].dtype #int
person_data['Protein_g'].dtype #0

#abnormal values will be stored in protein
protein=[]
for i in person_data['Protein_g']:
    if not i.isdigit():
        protein.append(i) #12s
        protein_dype_0=[]
        for j in protein:
            protein_dype_0.extend(j)
protein_dype_0
cleaned_value=[]
for integer in protein_dype_0:
    if integer.isdigit():
        cleaned_value.append(integer)
final_number = int("".join(cleaned_value))
date_value=person_data['Protein_g']=='12s'
person_data.loc[date_value, 'Protein_g'] = final_number
person_data
#we need to chnage dtype as float
person_data['Protein_g']=person_data['Protein_g'].astype(float)

#change height from cm to m
#Divide value to 100 gives cm in m
height_in_m=person_data['Height_cm']/100
person_data['Height_cm']=height_in_m


#BMI Calculation
#Formula to Calulate BMI
#BMI = weight in kilograms ÷ (height in meters × height in meters)
bmi=person_data['Weight_kg']/(height_in_m*height_in_m)
result=[]
for i in bmi:
    result.append(i)
for i in result:
    if i < 18.5:
        print('Underweight')
        break
    elif int(i) in range(18, 25):   # <- minimal fix
        print('normal Weight')
        break
    elif int(i) in range(25, 30):   # <- minimal fix
        print('Overweight')
        break
    elif i >= 30:
        print('Obese')
        break
    else:
        print('None')
        break
print(f"Your BMI value is {i}")
print("Final Conclusion:", ['Underweight' if i<18.5 else 'Normal weight' if i<25 else 'Overweight' if i<30 else 'Obese'])
person_data['C & P']=person_data['Calories']+person_data['Protein_g']
protein_calories=person_data['Protein_g']*4
protein_calories
calories_per_day=(protein_calories/person_data['Calories'])*100
calories_per_day_list=[]
for i in calories_per_day:
    calories_per_day_list.append(i)

#Calorie sufficiency per day
protein_percent = (person_data['Protein_g'] * 4 / person_data['Calories']) * 100
for id, val in enumerate(calories_per_day_list, start=1):
    if val >= 20:
        print(f"Day {id}: Protein intake is Sufficient ✅ ({val}%)")
    else:
        print(f"Day {id}: Protein intake is Insufficient ❌ ({val}%)")

#Total calories per week
week1_calories=person_data['Calories'].head(7).sum()
week2_calories=person_data['Calories'].tail(7).sum()

#Consistency calorie check week wise
goal_calorie_per_week1=1400*7
goal_calorie_per_week2=1400*7

#Total protein per week
week1_protein=person_data['Protein_g'].head(7).sum()
week2_protein=person_data['Protein_g'].tail(7).sum()

#Consistency protein check week wise
goal_protein_per_week1=60*7
goal_protein_per_week2=60*7

#Calorie increase/decrease week by week
if week1_calories>week2_calories:
    print('Calories Dcreased from last week')
elif week1_calories<week2_calories:
    print('Calories Increased from last week')
else:
    print('Equal Calories')

#Trend check
print("\n--- Weekly Trend ---")

print("Calories trend:", "📈 Increased" if week2_calories > week1_calories else "📉 Decreased" if week2_calories < week1_calories else "➖ No Change")
print("Protein trend:", "📈 Improved" if week2_protein > week1_protein else "📉 Dropped" if week2_protein < week1_protein else "➖ No Change")

import matplotlib.pyplot as plt

# Week column
person_data['Week'] = person_data['Date'].dt.isocalendar().week
weekly_avg = person_data.groupby('Week')[['Calories','Protein_g']].mean()

# Add first plot (Trend line)
fig = plt.figure(figsize=(5,5))
plt.plot(weekly_avg['Calories'], weekly_avg['Protein_g'],color='y',marker='o')
plt.title('Average weekly trend')
plt.xlabel('Calories (kcal)')
plt.ylabel('Protein (g)')

# Add second plot (Scatter)
fig = plt.figure(figsize=(5,5))
plt.scatter(person_data['Calories'], person_data['Protein_g'])
plt.title('Relationship: Calories vs Protein')
plt.xlabel('Calories (kcal)')
plt.ylabel('Protein (g)')
plt.show()

#Meal wise bar (high protein vs low protein)
meal_protein = person_data.groupby('Meal')['Protein_g'].mean().sort_values(ascending=False)
fig = plt.figure(figsize=(12,5))
plt.bar(meal_protein.index, meal_protein)
plt.title('Meal wise protein')
plt.xlabel('Meal')
plt.ylabel('Avg protein')
plt.xticks(rotation=60)
plt.show()
