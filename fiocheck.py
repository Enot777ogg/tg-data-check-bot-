import pandas as pd

DATA_FILE = "leaks.csv"

def search_fio(fio: str):
    try:
        df = pd.read_csv(DATA_FILE)
        df['ФИО'] = df['ФИО'].str.lower().str.strip()
        fio = fio.lower().strip()

        result = df[df['ФИО'] == fio]
        if result.empty:
            return None
        else:
            return result.to_dict(orient='records')
    except Exception as e:
        return f"Ошибка при чтении базы: {e}"
