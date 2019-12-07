# Do this for fun
import PySimpleGUI as sg
import database as db

# Type Definition
menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

# TODO: Determined family only info
family_layout = [sg.Text('Family Type', font='Any 12'),
                 sg.Combo(('Couple', 'PrimarySubscriberAndOneDependent', 'PrimarySubscriberAndTwoDependents',
                           'PrimarySubscriberAndThreeOrMoreDependents',
                           'CoupleAndOneDependent', 'CoupleAndTwoDependents', 'CoupleAndThreeOrMoreDependents'),
                          enable_events=True, key='Family_Type', font='Any 12',
                          size=(28, 7))],

# Layout Design
# sg.change_look_and_feel('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Menu(menu_def, tearoff=True)],

          [sg.Text('Healthcare Insurance Database System\n', font=("Helvetica", 16))],

          [sg.Text('State Code', font='Any 12'),
           sg.Combo(('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
                     'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM',
                     'NY',
                     'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
                     'WI', 'WY'),
                    enable_events=True, key='State', font='Any 12', size=(10, 5)),
           sg.Text("HIOS ID", font='Any 12'), sg.InputText(key='HIOS', size=(20, 1)),
           sg.Text("Plan ID", font='Any 12'), sg.InputText(key='Plan', size=(20, 1))],

          [sg.Text('Insurance Type', font='Any 12'),
           sg.Radio('Dental Only', 'Radio1', default=False, enable_events=True, key='Dental', font='Any 12',
                    size=(10, 1)),
           sg.Radio('Medical', 'Radio1', default=False, enable_events=True, key='Medical', font='Any 12',
                    tooltip='Contains both medical and dental plan', size=(10, 1))],
          [sg.Text('Subscriber Type', font='Any 12'),
           sg.Radio('Individual', 'Radio2', default=False, enable_events=True, key='Individual', font='Any 12',
                    size=(10, 1)),
           sg.Radio('Family', 'Radio2', default=False, enable_events=True, key='Family', font='Any 12', size=(10, 1))],

          [sg.Text('Cover Range', font='Any 12'),
           sg.Radio('Adult-Only', 'Radio3', default=False, enable_events=True, key='Adult', font='Any 12',
                    size=(10, 1)),
           sg.Radio('Child-Only', 'Radio3', default=False, enable_events=True, key='Child', font='Any 12',
                    size=(10, 1)),
           sg.Radio('Adult&Child', 'Radio3', default=False, enable_events=True, key='Adult_Child', font='Any 12',
                    size=(10, 1))],

          [sg.Text('Metal Level', font='Any 12'), sg.Combo(('Platinum', 'Gold', 'Silver', 'Bronze', 'Catastrophic',
                                                            'High(Dental Only Applicable)',
                                                            'Low(Dental Only Applicable)'),
                                                           enable_events=True, key='Metal_Level', font='Any 12',
                                                           size=(18, 7)),
           sg.Text('Monthly Premium', font='Any 12'), sg.Combo(('Lowest', 'Moderate', 'Highest'),
                                                               enable_events=True, key='Monthly_Premium', font='Any 12',
                                                               size=(15, 3))],

          [sg.Text('Maximum Out of Pocket', font='Any 12'), sg.InputText(key='MOOP', size=(9, 1)),
           sg.Text('Primary Subscriber Age', font='Any 12', size=(20, 1)), sg.InputText(key='Age', size=(5, 1))],

          [sg.Frame('Family Only', family_layout, font='Any 12')],

          [sg.Text('Advanced Search Options', font='Any 12')],
          [sg.Checkbox('Wellness Program', default=False, enable_events=True, key='Wellness', font='Any 12',
                       size=(15, 1)),
           sg.Checkbox('Tobacco Usage', default=False, enable_events=True, key='Tobacco', font='Any 12',
                       size=(12, 1)),
           sg.Checkbox('Pregnancy', default=False, enable_events=True, key='Pregnancy', font='Any 12', size=(10, 1)),
           sg.Checkbox('National Network', default=False, enable_events=True, key='National_Network', font='Any 11',
                       size=(13, 1)),
           sg.Checkbox('Out of Country', default=False, enable_events=True, key='Out_of_Country', font='Any 11',
                       size=(11, 1))],

          [sg.Text('Exchange Preference', font='Any 12'),
           sg.Combo(('On Exchange', 'Off Exchange', 'Both'), enable_events=True, key='Exchange', font='Any 12',
                    size=(10, 3)),
           sg.Text('Disease', font='Any 12'),
           sg.Combo(
               ('Asthma', 'Heart Disease', 'Fracture', 'Diabetes', 'Depression', 'Weight Loss', 'High Blood Pressure',
                'High Cholesterol'), enable_events=True, key='Disease', font='Any 12',
               size=(14, 5))
           ],
          # TODO: TO BE DETERMINED THE COPAY AND COIN OPTIONS
          [sg.Text('Copay Preference', font='Any 12'),
           sg.Combo(('No Charge', 'No Charge after deductible', 'Copay with deductible'), enable_events=True,
                    key='Copay', font='Any 12', size=(18, 3)),

           sg.Text('Coinsurance Preference', font='Any 12'),
           sg.Combo(('No Charge', 'No Charge after deductible', 'Fixed %',
                     'Fixed % of Coinsurance after deductible'), enable_events=True, key='Coin', font='Any 12',
                    size=(20, 5))],

          [sg.Button('Search', font='Any 12'), sg.Button('Cancel', font='Any 12')],

          [sg.Text('\n\n\n\n\n\n\nCopyright: Liangbin Zhu, Yujue Wang @ 2019FALL RPI', font=("Helvetica", 8))]]


# ==========================================================================================================
# Implementation function
# Function for processing user interface return values
def values_processing(values):
    input_dict = {
        "State": '',
        "HIOS": '',
        "Plan_Id": '',
        "Dental": False,
        "Medical": False,
        "Individual": False,
        "Family": False,
        "Adult": False,
        "Child": False,
        "Adult_Child": False,
        "Metal_Level": '',
        "Month_Premium": '',
        "MOOP": '',
        "Age": '',
        "Family_Type": '',
        "Wellness": False,
        "Tobacco": False,
        "Pregnancy": False,
        "National_Network": False,
        "Out_of_Country": False,
        "Exchange": '',
        "Disease": '',
        "Copay": '',
        "Coin": ''
    }

    if values['State']:
        input_dict['State'] = values['State']
    elif values['HIOS']:
        input_dict['HIOS'] = values['HIOS']
    elif values['Plan']:
        input_dict['Plan_Id'] = values['Plan']
    elif values['Dental']:
        input_dict['Dental'] = True
    elif values['Medical']:
        input_dict['Medical'] = True
    elif values['Individual']:
        input_dict['Individual'] = True
    elif values['Family']:
        input_dict['Family'] = True
    elif values['Adult']:
        input_dict['Adult'] = True
    elif values['Child']:
        input_dict['Child'] = True
    elif values['Adult_Child']:
        input_dict['Adult_Child'] = True
    elif values['Metal_Level']:
        input_dict['Metal_Level'] = values['Metal_Level']
    elif values['Monthly_Premium']:
        input_dict['Monthly_Premium'] = values['Monthly_Premium']
    elif values['MOOP']:
        input_dict['MOOP'] = values['MOOP']
    elif values['Age']:
        input_dict['Age'] = values['Age']
    elif values['Family_Type']:
        input_dict['Family_Type'] = values['Family_Type']
    elif values['Wellness']:
        input_dict['Wellness'] = True
    elif values['Tobacco']:
        input_dict['Tobacco'] = True
    elif values['Pregnancy']:
        input_dict['Pregnancy'] = True
    elif values['National_Network']:
        input_dict['National_Network'] = True
    elif values['Out_of_Country']:
        input_dict['Out_of_Country'] = True
    elif values['Exchange']:
        input_dict['Exchange'] = values['Exchange']
    elif values['Disease']:
        input_dict['Disease'] = values['Disease']
    elif values['Copay']:
        input_dict['Copay'] = values['Copay']
    elif values['Coin']:
        input_dict['Coin'] = values['Coin']
    return input_dict


# ==========================================================================================================
# Create the Window
window = sg.Window('Insurance Finder', layout, size=(800, 600))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    elif event == 'Search':
        parameters = values_processing(values)
        # TODO: Transforming input to sql executable string
        executable_str = db.SQLConstructor(parameters).get_str()
        # TODO: Query goes here
        number_result = 1
        result = "CDPHP student plan"
        sg.Popup('Search Results', 'We found %d insurance for you\n%s' % (number_result, result))

window.close()
