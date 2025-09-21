import pandas as pd

def clean_cat_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the Schrödinger's Cat Café dataset.
    Returns a cleaned DataFrame.
    """

    # 1. Drop duplicate rows
    df = df.drop_duplicates()

    # 2. Handle missing values (none expected, but good practice)
    df = df.dropna()  # or use df.fillna(method='ffill') for imputation

    # 3. Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # 4. Validate numeric ranges (clip outliers)
    df['box_temperature_(°c)'] = df['box_temperature_(°c)'].clip(0, 50)
    df['quantum_entanglement_index'] = df['quantum_entanglement_index'].clip(0, 1)
    df['radioactive_decay_rate'] = df['radioactive_decay_rate'].clip(0, 1)
    df['wavefunction_stability'] = df['wavefunction_stability'].clip(0, 1)
    df['alive_probability'] = df['alive_probability'].clip(0, 1)
    df['cat_mood_score'] = df['cat_mood_score'].clip(0, 100)
    df['quantum_sass_index'] = df['quantum_sass_index'].clip(0, 10)

    # 5. Validate categorical values
    valid_materials = ['Cardboard', 'Lead', 'Graphene', 'Velvet', 'Quantum Foam']
    df = df[df['box_material'].isin(valid_materials)]

    # 6. Convert observer presence to boolean
    df['observer_presence'] = df['observer_presence'].astype(bool)

    return df