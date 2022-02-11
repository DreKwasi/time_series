import vaex as vx

path = r"C:\Users\mpharma\Projects\Time_Series_Analysis\Data\consumption_data.csv.hdf5"

# Imports data
# @st.cache(allow_output_mutation=True)
def load_data(path=path):

    data = vx.open(path)

    # Place all Column Names in a List
    col_names = data.get_column_names()
    # Renaming all columns to fit Vaex standards
    for i in col_names:
        data.rename(i,i.replace(" ", "_").replace("-","_"))

    col_names = data.get_column_names()

# Filtering Data to relevant Columns
    df = data.copy()[[col_names[2], col_names[4], col_names[5], col_names[6], 
                col_names[9], col_names[10], col_names[11], col_names[12], col_names[13],
                col_names[14], col_names[15],col_names[41], col_names[43], col_names[44], col_names[50]]]

# Sort Time Series
    df = df.sort(by='Sale_Date', ascending=True)
    return df
