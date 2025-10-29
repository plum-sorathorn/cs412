# File: models.py
# Author: Sorathorn Thongpitukthavorn (plum@bu.edu), 9/23/2025
# Description: contains models for voter analytics webapp

import csv
from datetime import datetime
from django.db import models

# Create your models here.
class Voter(models.Model):
    ''' structure of each voter's data attributes '''

    # name
    last_name = models.TextField(blank=True)
    first_name = models.TextField(blank=True)

    # address
    street_number = models.TextField(blank=True)
    street_name = models.TextField(blank=True)
    apartment_number = models.TextField(blank=True)
    zip_code = models.TextField(blank=True)

    # dates
    date_of_birth = models.DateField(blank=True)
    date_of_registration = models.DateField(blank=True)
    party_affliation = models.TextField(blank=True)

    # idk
    precinct_number = models.TextField(blank=True)

    # voting history
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    # voter score
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        ''' return string representation of this voter's info '''
        return f'{self.first_name}, {self.last_name}, {self.zip_code}, {self.date_of_birth}, {self.v20state}' 
        
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    filename = "C:/newton_voters.csv"
    
    # Use 'with open' for proper file handling
    with open(filename, 'r') as f:
        # Use csv.reader for robust CSV parsing
        reader = csv.reader(f)
        next(reader) # discard headers
        
        created_count = 0
        
        for fields in reader:
            if not fields: # Skip empty lines
                continue
            
            # Helper to convert "TRUE" or "FALSE" strings to Python bools
            def str_to_bool(s):
                return s.strip().upper() == 'TRUE' if s.strip() else False

            try:
                # 1. Clean up and convert data types before creating the model
                voter = Voter(
                    last_name=fields[1].strip(),
                    first_name=fields[2].strip(),

                    street_number=fields[3].strip(),
                    street_name=fields[4].strip(),
                    apartment_number=fields[5].strip(),
                    zip_code=fields[6].strip(),

                    # Date Conversion: 'YYYY-MM-DD' string to datetime.date object
                    date_of_birth=datetime.strptime(fields[7].strip(), '%Y-%m-%d').date() if fields[7].strip() else None,
                    date_of_registration=datetime.strptime(fields[8].strip(), '%Y-%m-%d').date() if fields[8].strip() else None,
                    party_affliation=fields[9].strip(),

                    precinct_number=fields[10].strip(),

                    # Boolean Conversion
                    v20state=str_to_bool(fields[11]),
                    v21town=str_to_bool(fields[12]),
                    v21primary=str_to_bool(fields[13]),
                    v22general=str_to_bool(fields[14]),
                    v23town=str_to_bool(fields[15]),

                    # Integer Conversion
                    voter_score=int(fields[16].strip()) if fields[16].strip() else 0,
                )
                
                # 2. COMMIT to database
                voter.save() 
                created_count += 1
                print(f'Created voter: {voter}')
                
            except Exception as e:
                print(f"Skipped record due to error: {e} with fields: {fields}")
        
    print(f'Done. Created {created_count} voters.')