## Predicting Probability of Default of Lending Club loans

### Lending Club
Lending Club is a peer to peer lending company based in the United States, in which investors provide funds for potential borrowers and investors earn a profit depending on the risk they take (the borrowers credit score). Lending Club provides the "bridge" between investors and borrowers. For such companies who are in the lending business, calculating the probability of default can help estimate the expected income in the near term. For banks this can be used to ensure that they meet the regulatory capital requirements. 

### Project Objective
Build a machine learning model to predict the probability of deafult in the next month for lending club,s loan portfolio. 

### Data Source
I am using this data set : https://www.kaggle.com/husainsb/lendingclub-issued-loans

### Defining Default 
A loan can go through different statuses during its life cycle. 
- When the borrower is paying as per schedule, then the loan is in 'Current' status. 
- When the borrower is late on any interest payments, the loan moves to D30 status which means that he is more than 30 days late on his payments. This now becomes a 'NPL' or a Non performing loan. 
- If he does not pay the second EMI as well, the loan moves into D60 status. 
- Similarly , D60 is followed by D90, D120 and D180. 

If he wants to go to current status, he would have to repay all of the missed interest payments. If the borrower pays only some portion of the interest, he moves from D180 to D60 or D30 based on the amount he paid. If the borrower does not pay, the loan is moved into 'Charge off' status. This means that the company thinks the customer is never going to pay back so they just charge off the loan from their books. This is the stage where the borrower's collateral (Eg. for mortgage loans it is the home equity) is sold to recover the missing payments. 

In this project I am going to estimate the probability of final default or charge off of the loan. (not the intermediate default stages like D30, D60 etc.). I do this because when the customer starts defaulting, there is still hope to recover the lost payments but once he is charged off, the company really looses money.  Hence I consider this to be more useful estimate for the company. 

