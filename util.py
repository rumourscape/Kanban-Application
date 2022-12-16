import pandas as pd


def export_to_csv(card_list, list_title):
    df = pd.DataFrame.from_records(card_list)
    file_name = f'{list_title}.csv'
    df.to_csv(file_name, index=False)

    print(file_name)
    return file_name