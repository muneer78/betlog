import pandas as pd
import numpy as np

def clean_dataframe(df):
    cols = ['Amount', 'Odds']
    df[cols] = df[cols].astype('float').fillna(0)
    df['Date'] = pd.to_datetime(arg=df['Date'], format='%m/%d/%Y')
    
    df['CleanedOdds'] = df['Odds'].abs()

    df['PotentialProfit'] = np.where(df['Odds'] > 0, ((df['CleanedOdds'] / 100) * df['Amount']), (100 / df['CleanedOdds']) * df['Amount'])
    df['PotentialProfit'] = df['PotentialProfit'].round(2)

    cols2 = ['PotentialProfit', 'CleanedOdds']
    df[cols2] = df[cols2].apply(pd.to_numeric, errors='coerce', axis=1)

    df['PotentialPayout'] = df['PotentialProfit'] + df['Amount'].apply(pd.to_numeric, errors='coerce')
    df.loc[df['FreeBet'] == 'N', 'PotentialPayout'] = df['PotentialPayout']
    df.loc[df['FreeBet'] == 'Y', 'PotentialPayout'] = df['PotentialProfit']
    df['PotentialPayout'] = df['PotentialPayout'].round(2)

    df['ImpliedProbability'] = np.where(df['Odds'] > 0, ((100 / (100 + df['CleanedOdds']))), ((df['CleanedOdds'])/(100+(df['CleanedOdds'])))).round(2)

    df['Expected Value'] = np.ceil(df['ImpliedProbability'] * df['Amount']) - ((1 - df['ImpliedProbability']) * df['Amount'])
    df['Expected Value'] = df['Expected Value'].apply(pd.to_numeric, errors='coerce')
    df['Expected Value'] = df['Expected Value'].round(2)

    df['ImpliedProbability'] = (df['ImpliedProbability']*100).apply(pd.to_numeric, errors='coerce')
    df['ImpliedProbability'] = (df['ImpliedProbability']).round(2)

    df['ActualPayout'] = np.nan
    df['ActualPayout'] = df['ActualPayout'].apply(pd.to_numeric, errors='coerce')
    df['ActualPayout'] = df['ActualPayout'].astype('float')

    for i, row in df.iterrows():
        if row['Result'] == 'L' and row['FreeBet'] == 'N':
            df.at[i, 'ActualPayout'] = row['Amount'] * -1
        elif row['Result'] == 'L' and row['FreeBet'] == 'Y':
            df.at[i, 'ActualPayout'] = 0
        elif row['Result'] == 'W' and row['FreeBet'] == 'Y':
            df.at[i, 'ActualPayout'] = row['PotentialProfit']
        elif row['Result'] == 'W' and row['FreeBet'] == 'N':
            df.at[i, 'ActualPayout'] = row['PotentialPayout']
        elif row['Result'] == 'Pe':
            df.at[i, 'ActualPayout'] = 0
        elif row['Result'] == 'P':
            df.at[i, 'ActualPayout'] = row['PushAmount']

def format_currency(df, currency_columns):
    for col in currency_columns:
        df[col] = df[col].apply(lambda x: "${:,.2f}".format(x) if pd.notnull(x) else '')

def main():
    df = pd.read_csv('bet.csv')

    clean_dataframe(df)
    
    df_copy = df.copy()

    currency_columns = ['Amount', 'PushAmount', 'PotentialProfit', 'PotentialPayout', 'Expected Value', 'ActualPayout']
    format_currency(df_copy, currency_columns)

    df_copy.to_csv('betlog.csv', index=False)

    df3 = df[["Sport", "Amount", "ActualPayout"]]
    df3 = df3.groupby("Sport").sum().reset_index()
    df3["ROI"] = (df3["ActualPayout"] / df3["Amount"] * 100).round(2)
    df3 = df3.reindex(columns=["Sport", "ActualPayout", "Amount", "ROI"]).round(2)

    df4 = df.groupby(['Sport'])['ActualPayout'].sum().reset_index().round(2)
    df5 = df.groupby(['Sport'])['Amount'].sum().reset_index().round(2)
    df6 = df.groupby(df['Date'].dt.strftime('%Y-%m'))['ActualPayout'].sum().reset_index().round(2).sort_values(by=['Date'])
    df7 = df.groupby(['Sportsbook'])['ActualPayout'].sum().reset_index().round(2)
    df8 = df.groupby(['Sportsbook'])['Amount'].sum().reset_index().round(2)
    df9 = df.groupby(['System'])['ActualPayout'].sum().reset_index().round(2)
    df10 = df.groupby(['BetType'])['ActualPayout'].sum().reset_index().round(2)
    df11 = df.groupby(['BetType'])['Amount'].sum().reset_index().round(2)
    df12 = df.groupby(['FreeBet'])['ActualPayout'].sum().reset_index().round(2)
    df13 = df.groupby(['FreeBet'])['Amount'].sum().reset_index().round(2)

    list_of_dfs = [df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13]
    for df in list_of_dfs:
        df.rename(columns={'Amount': 'MoneyRisked', 'ActualPayout': 'Profit'}, inplace=True)
        format_currency(df, ['Profit', 'MoneyRisked', 'TotalWon', 'TotalRisked'])

    titles = [
        "ROI By Sport", "Profit by Sport", "Risk by Sport", "Profit by Month",
        "Profit by Sportsbook", "Risk by Sportsbook", "Profit by System",
        "Profit by Bet Type", "Risk by Bet Type", "Total ROI", "Total Win Percentage",
        "Profit by Free Bet vs. Money Bet", "Risk by Free Bet vs. Money Bet"
    ]

    with open('analytics.csv', 'w+') as f:
        for i, df in enumerate(list_of_dfs):
            f.write(titles[i] + "\n")  # Write the title
            df.to_csv(f, index=False)
            f.write("\n")

if __name__ == "__main__":
    main()
