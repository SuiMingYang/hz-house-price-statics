
import pandas as pd
import pandas_profiling

data=pd.read_csv("./data_history/houseprice.csv")
print(data.describe())
profile = data.profile_report(title='houseprice')
profile.to_file(output_file='./houseprice.html')




