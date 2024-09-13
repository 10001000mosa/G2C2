import pandas as pd
import os

def process_file(filepath):
    # Read the CSV file into a DataFrame
    csatracker = pd.read_csv(filepath)
    
    # Cleaning database
    columns_to_drop = [
        'name', 'start', 'end', 'today', 'intro_002', 'intro_001', 'other_changes', 'specifics',
        '_validation_status', '_notes', '_status', '_submitted_by', '_uuid', '__version__',
        '_tags', '_index', 'thank'
    ]
    csatracker = csatracker.drop(columns=columns_to_drop, errors='ignore')  # Ignore if columns not found
    
    # Define a function to clean column names
    def clean_column_names(columns):
        return [col.replace('-', '_').replace('/', '_') for col in columns]

    # Recode column names
    csatracker.columns = clean_column_names(csatracker.columns)

    # Calculate variable 'csatracking' = 1 if any of the activities = 1 or 'csa_other' is not empty
    csatracker['csatracking'] = csatracker[['csa_voting', 'csa_community_level_organizing',
                                            'csa_social_media_advocacy', 'csa_meetings_with_governments_to_advocate_fo',
                                            'csa_other_advocacy_initiatives_as_organized_']].max(axis=1)
    
    csatracker.loc[csatracker['csa_other'].notna() & (csatracker['csa_other'] != ''), 'csatracking'] = 1

    # Calculate variable 'trainning_outcomes' score
    csatracker['trainning_outcomes'] = csatracker[['engagement', 'friends_people', 'new_org', 'global_mov', 'fundraise']].sum(axis=1)

    # Trimming before export
    csatracker.columns = clean_column_names(csatracker.columns)
    columns_to_drop = ['csa', 'csa_registering_to_vote', 'csa_voting',
                       'csa_community_level_organizing', 'csa_social_media_advocacy',
                       'csa_meetings_with_governments_to_advocate_fo',
                       'csa_other_advocacy_initiatives_as_organized_', 'csa_other',
                       'engagement', 'friends_people', 'new_org', 'global_mov', 'fundraise',
                       '_id']
    csatracker = csatracker.drop(columns=columns_to_drop, errors='ignore')  # Ignore if columns not found

    # Count the number of 1s in the 'csatracking' column
    num_participants = csatracker['csatracking'].sum()
    print(f"The number of females aged 10-24 who participate in civil society activities following soft skills/life skills training or initiatives from USG assisted programs is {num_participants}")

    # Group by 'region' and calculate the sum of 'csatracking' for each region
    region_breakdown = csatracker.groupby('region')['csatracking'].sum().reset_index()

    # Calculate the total number of participants
    total_participants = region_breakdown['csatracking'].sum()

    # Calculate the percentage of participants for each region
    region_breakdown['percentage'] = (region_breakdown['csatracking'] / total_participants) * 100

    for index, row in region_breakdown.iterrows():
        print(f"Region: {row['region']}, Participants: {row['csatracking']}, Percentage: {row['percentage']:.1f}%")

    # Save the DataFrame as a CSV file
    processed_filename = os.path.join('processed', 'processed_data.csv')
    csatracker.to_csv(processed_filename, index=False)

    return processed_filename
