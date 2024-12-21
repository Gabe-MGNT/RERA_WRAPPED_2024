import pandas as pd

df_f = pd.read_csv("./csv_files/incident_notifies2.csv")
pb_resolve_df = pd.read_csv("./csv_files/pb_resolve2.csv", parse_dates=['begin_date', 'end_date'])
pb_resolve_df['duration'] = pd.to_timedelta(pb_resolve_df['duration'])
pb_resolve_df.dropna(inplace=True)

df_f['date'] = pd.to_datetime(df_f['time_posted'])

# Ajouter des colonnes pour le mois et l'année
df_f['month'] = df_f['date'].dt.month
df_f['year'] = df_f['date'].dt.year

all_types = df_f['label'].fillna('')
all_types = all_types.values

all_types_split = [a.split(',') for a in all_types]
all_types_split_flat = [item for sublist in all_types_split for item in sublist if item]
all_types_split_unique = list(set(all_types_split_flat))

years = df_f['year'].unique()
years.sort()
months = df_f['month'].unique()
months.sort()
