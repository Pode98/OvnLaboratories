
import pandas as pd
import matplotlib.pyplot as plt
import json

df = pd.read_csv('../resources/sales_data.csv')
profit_list = df['total_profit'].values
months = df['month_number'].values
plt.figure()
plt.plot(months, profit_list, label='Month-wise Profit data of last year')
plt.xlabel('Month number')
plt.ylabel('Profit [$]')
plt.xticks(months)
plt.title('Company profit per month')
plt.yticks([100e3, 200e3, 300e3, 400e3, 500e3])
plt.show()


df = pd.read_csv('../resources/sales_data.csv')
profit_list = df['total_profit'].values
months = df['month_number'].values
plt.figure()
plt.plot(months, profit_list, label='Profit data of last 1 year', color='r', marker='o', markerfacecolor='k',
         linestyle='--', linewidth=3)
plt.xlabel('Month Number')
plt.ylabel('Profit in dollar')
plt.legend(loc='lower right')
plt.title('Company Sales data of last year')
plt.xticks(months)
plt.yticks([100e3, 200e3, 300e3, 400e3, 500e3])
plt.show()


df = pd.read_csv('../resources/sales_data.csv')
months = df['month_number'].values
face_cream_sales_data = df['facecream'].values
face_wash_sales_data = df['facewash'].values
tooth_paste_sales_data = df['toothpaste'].values
bathing_soap_sales_data = df['bathingsoap'].values
shampoo_sales_data = df['shampoo'].values
moisturizer_sales_data = df['moisturizer'].values
plt.figure()
plt.plot(months , face_cream_sales_data ,label='Face cream Sales Data', marker='o', linewidth=3)
plt.plot(months , face_wash_sales_data ,label='Face wash Sales Data', marker='o', linewidth=3)
plt.plot(months , tooth_paste_sales_data ,label='ToothPaste Sales Data', marker='o', linewidth=3)
plt.plot(months , bathing_soap_sales_data ,label='Bathing Soap Sales Data', marker='o', linewidth=3)
plt.plot(months , shampoo_sales_data ,label='Shampoo Sales Data', marker='o', linewidth=3)
plt.plot(months , moisturizer_sales_data ,label='Moisturizer Sales Data', marker='o', linewidth=3)
plt.xlabel('Month Number')
plt.ylabel('Sales units in number')
plt.legend(loc='upper left')
plt.xticks(months)
plt.yticks([1e3, 2e3, 4e3, 6e3, 8e3, 10e3, 12e3, 15e3, 18e3])
plt.title('Sales data')
plt.show()


df = pd.read_csv('../resources/sales_data.csv')
months = df['month_number'].tolist()
tooth_paste_sales_data = df['toothpaste'].values
plt.figure()
plt.scatter(months , tooth_paste_sales_data , label='Tooth paste sales data')
plt.xlabel('Month Number')
plt.ylabel('Number of units sold')
plt.legend(loc='upper left')
plt.title('Tooth paste sales data')
plt.xticks(months)
plt.grid(True, linewidth=0.5, linestyle='--')
plt.show()

df = pd.read_csv('../resources/sales_data.csv')
months = df['month_number'].tolist()
bathing_soap_sales_data = df['bathingsoap'].tolist()
plt.bar(months , bathing_soap_sales_data)
plt.xlabel('Month Number')
plt.ylabel('Sales units in number')
plt.xticks(months)
plt.grid(True, linewidth=0.5, linestyle="--")
plt.title('Bathing soap sales data')
plt.savefig('sales_data_of_bathing_soap.png', dpi=150)
plt.show()

folder_in=''
df = pd.read_csv(folder_in + 'sales_data.csv')
profit_list = df['total_profit'].values
plt.figure()
profit_range = [150e3, 175e3, 200e3, 225e3, 250e3, 300e3, 350e3]
plt.hist(profit_list , profit_range , label='Profit data')
plt.xlabel('profit range [$]')
plt.ylabel('Actual Profit [$]')
plt.legend(loc='upper left')
plt.xticks(profit_range)
plt.title('Profit data')
plt.show()


folder_in=''
df = pd.read_csv(folder_in + 'sales_data.csv')
months = df['month_number'].values
bathing_soap = df['bathingsoap'].values
face_wash_sales_data = df['facewash'].values
f, axs = plt.subplots(2, 1, sharex=True)
axs[0].plot(months, bathing_soap, label='Bathing soap Sales Data',color='k', marker='o', linewidth=3)
axs[0].set_title('Sales data of a Bathing soap')
axs[0].grid(True, linewidth=0.5, linestyle='--')
axs [0]. legend ()
axs[1].plot(months, face_wash_sales_data, label='Face Wash Sales Data',color='r', marker='o', linewidth=3)
axs[1].set_title('Sales data of a face wash')
axs[1].grid(True, linewidth=0.5, linestyle='--')
axs[1].legend()
plt.xticks(months)
plt.xlabel('Month Number')
plt.ylabel('Sales units in number')
plt.show()




json_obj = '{ "Name":"David", "Class":"I", "Age":6 }'
python_obj = json.loads(json_obj)
print('\nJSON data:')
print(python_obj)
print('\nName:', python_obj['Name'])
print('Class:', python_obj['Class'])
print('Age:', python_obj['Age'])


python_obj = { 'name': 'David','class': 'I','age': 6 }
print(type(python_obj))
# convert into JSON:
j_data = json.dumps(python_obj)
# result is a JSON string:
print(j_data)

python_dict = {'name': 'David', 'age': 6, 'class': 'I'}
python_list = ['Red', 'Green', 'Black']
python_str = 'Python Json'
python_int = 1234
python_float = 21.34
python_t = True


python_f = False
python_n = None
json_dict = json.dumps(python_dict)
json_list = json.dumps(python_list)
json_str = json.dumps(python_str)
json_num1 = json.dumps(python_int)
json_num2 = json.dumps(python_float)
json_t = json.dumps(python_t)
json_f = json.dumps(python_f)
json_n = json.dumps(python_n)
print('json dict:', json_dict)
print('jason list:', json_list)
print('json string:', json_str)
print('json number1:', json_num1)
print('json number2:', json_num2)
print('json true:', json_t)
print('json false:', json_f)
print('json null:', json_n)

j_str = {'4':5, '6': 7, '1': 3, '2': 4}
print('Original String:', j_str)
print('\nJSON data:')
print(json.dumps(j_str, sort_keys=True, indent=4))


with open('../resources/states.json') as f:
    state_data = json.load(f)
print('Original JSON keys: ', [state.keys()for state in state_data['states']][0])
for state in state_data['states']:
    del state['area_codes']
print('\nModified JSON keys: ', [state.keys() for state in state_data['states']][0])
with open('new_states.json', 'w') as f:
    json.dump(state_data, f, indent=2)
with open('new_states.json') as f:
    state_data = json.load(f)
print('\nReloaded JSON keys: ', [state.keys() for state in state_data['states']][0])