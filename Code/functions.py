import pandas as pd
import numpy as np 
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 80)


def create_new_df(df):
    df_charge_off = df[df['charge_off'] == 1 ]
    df_non_charge_off = df[df['charge_off'] == 0 ]

    new_df = pd.DataFrame(df.groupby('year').mean()['int_rate'])
    new_df['year'] = new_df.index

    years = sorted(df.year.unique()) 
    prob = []
    for i in years: 
        coff = len(df[df.year == i][df.charge_off == 1])
        total = len(df[df.year == i])
        prob.append(float(coff)/float(total))

    new_df['c_off_pct'] = prob


    new_df['charge_off_int_rates'] = df_charge_off.groupby('year').mean()['int_rate']
    new_df['non_charge_off_int_rates'] = df_non_charge_off.groupby('year').mean()['int_rate']
    new_df['year_wise_charge_off_ratio'] = df['year'].groupby(df['charge_off']).value_counts(normalize=True)[1].sort_index()


    df['recoveries'] = df['recoveries'] + df['collection_recovery_fee']
    new_df['c_off_rec'] = df_charge_off.groupby('year')['recoveries'].mean().sort_index()

    new_df['year_wise_rec_ratio'] = new_df['c_off_rec']/sum(new_df['c_off_rec'])

    new_df['year_wise_rec_ratio'] = round(new_df['year_wise_rec_ratio'], 2)
    new_df['year_wise_charge_off_ratio'] = round(new_df['year_wise_charge_off_ratio'], 2)


    rec_df = pd.DataFrame(columns = ['Charged_off', 'Non_Charged_off'], index = ['Recoveries = 0', 'Recoveries > 0'])

    rec_df.loc['Recoveries = 0']['Charged_off'] = len(df[df['recoveries'] == 0.0 ][df['charge_off'] == 1])
    rec_df.loc['Recoveries > 0']['Charged_off'] = len(df[df['recoveries'] > 0.0 ][df['charge_off'] == 1])
    rec_df.loc['Recoveries = 0']['Non_Charged_off'] = len(df[df['recoveries'] == 0.0 ][df['charge_off'] == 0])
    rec_df.loc['Recoveries > 0']['Non_Charged_off'] = len(df[df['recoveries'] > 0.0 ][df['charge_off'] == 0])



    new_df['no_charge_offs'] = df_charge_off.groupby('year')['charge_off'].value_counts().values
    new_df['no_loans'] = df.groupby('year')['charge_off'].count()
    new_df['no_recoveries'] = df_charge_off[df_charge_off.recoveries > 0.0].groupby('year')['recoveries'].count()
    new_df['pct_loans_recovered'] = new_df['no_charge_offs']/new_df['no_recoveries']

    
    df_charge_off['loss'] = -((df_charge_off.total_pymnt + df_charge_off.recoveries)/ df_charge_off.funded_amnt - 1)
    df_charge_off['no_rec_loss'] = -((df_charge_off.total_pymnt)/ df_charge_off.funded_amnt - 1)


    return df_charge_off, new_df,rec_df ,df_non_charge_off


#Stacked bar graph 

    
    
def plot_ir(df, df_charge_off, new_df,rec_df ,df_non_charge_off ):

    plt.figure(figsize=(11,6))
    x, y, hue = "year", "Proportion of Loans", "charge_off"

    (df[x]
     .groupby(df[hue])
     .value_counts(normalize=True)
     .rename(y)
     .reset_index()
     .pipe((sns.barplot, "data"), x=x, y=y, hue=hue))

    plt.xlabel('Year', fontsize = 12 )
    plt.ylabel('Proportion of Loans', fontsize = 12)
    plt.gcf().autofmt_xdate()
    plt.title ('Proportion of Loans Charged Off Over Time',fontsize = 15)
    plt.grid(alpha =.6, linestyle ='--') 


    plt.figure(figsize=(11,6))
    plt.plot(new_df['year'], new_df['non_charge_off_int_rates'], label = 'non_charge_off_int_rates' )
    plt.plot(new_df['year'], new_df['charge_off_int_rates'], label = 'charge_off_int_rates' )

    plt.legend(loc='upper left',fontsize = 'large')
    plt.xlabel('Year', fontsize = 12 )
    plt.ylabel('Interest Rates', fontsize = 12)
    plt.title ('Interest Rates for Charged Off and Non Charged Off loans',fontsize = 15)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.gcf().autofmt_xdate()
    plt.grid(alpha =.6, linestyle ='--') 
    
def plot_rec(df, df_charge_off, new_df,rec_df ,df_non_charge_off ):
    labels = new_df['year']
    men_means = new_df['year_wise_charge_off_ratio']
    women_means = new_df['year_wise_rec_ratio']


    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(10,5))

    rects1 = ax.bar(x - width/2, men_means, width, label='Charge Offs')
    rects2 = ax.bar(x + width/2, women_means, width, label='Recoveries')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Year wise percentage', fontsize = 12)
    ax.set_title('% Charge Offs and Recoveries', fontsize = 15)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 1),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    plt.grid(alpha =.6, linestyle ='--') 

    plt.show()



    plt.figure(figsize=(12,6))
    plt.plot(new_df['year'], new_df['pct_loans_recovered']) 
    plt.title("Percentage of Loans Recovered After Charge Off",fontsize = 15)
    plt.xlabel('Year', fontsize = 12 )
    plt.ylabel('Percentage of Recovered Loans', fontsize = 12)

    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.gcf().autofmt_xdate()
    plt.grid(alpha =.6, linestyle ='--') 
    
    
    

def plot_loss(df, df_charge_off, new_df,rec_df ,df_non_charge_off ):
    plt.figure(figsize=(11,6))
    sns.lineplot('year','loss',data=df_charge_off)
    plt.ylabel('Average Loss', fontsize = 12)
    plt.title("Yearly Charge Off Loss Curve",fontsize = 15)
    plt.xlabel('Year', fontsize = 12 )

    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.gcf().autofmt_xdate()
    plt.grid(alpha =.6, linestyle ='--') 

def plot_cum_loss(df, df_charge_off, new_df,rec_df ,df_non_charge_off ):
    plt.figure(figsize=(11,6))
    sns.lineplot('year',df_charge_off['loss'].cumsum(),data=df_charge_off, label = 'Recoveries Adjusted Cum Loss')
    sns.lineplot('year',df_charge_off['no_rec_loss'].cumsum(),data=df_charge_off, label = 'Actual Cum Loss')
    plt.ylabel('Average Loss', fontsize = 12)
    plt.title("Cumulative Loss",fontsize = 15)
    plt.xlabel('Year', fontsize = 12 )

    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.gcf().autofmt_xdate()
    plt.grid(alpha =.6, linestyle ='--') 

def plot_grade(df, df_charge_off, new_df,rec_df ,df_non_charge_off ):
    df_charge_off.boxplot(figsize=(11,6),by='grade',column='loss')
    plt.title ("Charge Off Loss with respect to Grade of Borrower",fontsize = 15)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.grid(alpha =.6, linestyle ='--') 
    plt.xlabel('Grade', fontsize = 12 )
    plt.ylabel('Charge Off Loss', fontsize = 12)
    plt.gcf().autofmt_xdate()
    plt.grid(alpha =.6, linestyle ='--') 
    
def plot_term(df, df_charge_off, new_df,rec_df ,df_non_charge_off ):
    #year and avg loan amount based on income class 
    plt.figure(figsize=(11,6))
    sns.barplot('year','loss',data=df_charge_off,hue='term')
    plt.ylabel('Average Loss',fontsize = 12)
    plt.title('Charge Off Loss with respect to term',fontsize = 15)

    plt.gcf().autofmt_xdate()
    plt.grid(alpha =.6, linestyle ='--') 
    plt.show()


def plot_purpose(df, df_charge_off, new_df,rec_df ,df_non_charge_off ):
    #year and avg loan amount based on income class 
    plt.figure(figsize=(11,6))
    sns.barplot('year','annual_inc',data=df,hue='charge_off')
    plt.title('Charge Off Loss with respect to Income', fontsize = 15)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.grid(alpha =.6, linestyle ='--') 
    plt.xlabel('Year', fontsize = 12 )
    plt.ylabel('Avergae Annual Income', fontsize = 12)
    plt.gcf().autofmt_xdate()


    plt.figure(figsize=(11,6))
    sns.countplot(x="purpose",  data=df_charge_off)
    plt.xlabel('Purpose of Loan', fontsize = 12 )
    plt.ylabel('Number of Charge Offs', fontsize = 12)
    plt.title('Charge Off wrt Purpose of Loan', fontsize = 15)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.grid(alpha =.6, linestyle ='--') 
    plt.gcf().autofmt_xdate()
    plt.show()

def plot_tot_pay(df, df_charge_off, new_df,rec_df ,df_non_charge_off ):
    plt.figure(figsize=(14,5))
    sns.barplot('year','total_pymnt',data=df,hue='charge_off')
    plt.xlabel('Year', fontsize = 12 )
    plt.ylabel('Total Pyment Done', fontsize = 12)
    plt.title('Charge Off wrt Payments Done', fontsize = 15)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.grid(alpha =.6, linestyle ='--') 
    plt.gcf().autofmt_xdate()
    plt.show()


   
def plot_revol(df, df_charge_off, new_df,rec_df ,df_non_charge_off ):
    #year and avg loan amount based on income class 
    plt.figure(figsize=(11,6))
    sns.barplot('year','revol_util',data=df,hue='charge_off')
    plt.xlabel('Year', fontsize = 12 )
    plt.ylabel('Revolving Utilization', fontsize = 12)
    plt.title('Charge Off wrt Revolving Utilization', fontsize = 15)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.grid(alpha =.6, linestyle ='--') 
    plt.gcf().autofmt_xdate()
    plt.show()



    #year and avg loan amount based on income class 
    plt.figure(figsize=(11,6))
    sns.barplot('year','revol_bal',data=df,hue='charge_off')
    plt.xlabel('Year', fontsize = 12 )
    plt.ylabel('Revolving Balance', fontsize = 12)
    plt.title('Charge Off wrt Revolving Balance', fontsize = 15)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.grid(alpha =.6, linestyle ='--') 
    plt.gcf().autofmt_xdate()
    plt.show()





    #year and avg loan amount based on income class 
    plt.figure(figsize=(14,5))
    sns.barplot('year','tot_coll_amt',data=df,hue='charge_off')
    plt.xlabel('Year', fontsize = 12 )
    plt.ylabel('Collateral Amount', fontsize = 12)
    plt.title('Charge Off wrt Total Collateral Amount', fontsize = 15)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.grid(alpha =.6, linestyle ='--') 
    plt.gcf().autofmt_xdate()
    plt.show()






    #year and avg loan amount based on income class 
    plt.figure(figsize=(14,5))
    sns.barplot('year','tot_cur_bal',data=df,hue='charge_off')
    plt.xlabel('Year', fontsize = 12 )
    plt.ylabel('Total Balance', fontsize = 12)
    plt.title('Charge Off wrt Total Balance', fontsize = 15)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.grid(alpha =.6, linestyle ='--') 
    plt.gcf().autofmt_xdate()
    plt.show()

    plt.figure(figsize=(14,5))
    sns.barplot('year','loan_amnt',data=df,hue='charge_off')
    plt.xlabel('Year', fontsize = 12 )
    plt.ylabel('Loan Amount', fontsize = 12)
    plt.title('Charge Off wrt Amount Borrowed', fontsize = 15)
    plt.xticks(fontsize = 10)
    plt.yticks(fontsize = 10)
    plt.grid(alpha =.6, linestyle ='--') 
    plt.gcf().autofmt_xdate()
    plt.show()
