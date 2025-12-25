In recent times, young adults have found managing their finances increasingly difficult. This trend can be attributed to a lack of professional, 
personalized advice. Without access to professional advice, financial decisions become stressful, leading to poor financial decisions and overall 
negative views towards finances. 

Budget Buddy is an AI-powered web app that assists users in getting a better hold on their finances by providing the personalized advice they 
need. Using streamlit, the site collects the financial data of users and, through the power of Gemini-AI, offers users personalized budget advice 
based on the user’s financial situation. 

The main component of Budget Buddy is the Budget Advisor, which collects financial information – such as income, expenses, savings, debt, and goals 
– and uses this information to generate personalized budgeting advice on how to save, spend, and plan more effectively. The advice includes an 
actionable plan and resource suggestions tailored to the user’s location and financial situation. 

In addition, the app contains a secondary side bar tool: The Stock Advisor. The Stock Advisor allows users to input a stock ticker and retrieves 
historical price data. It then uses linear regression to predict the stock’s next closing price based on past trends. Based on the prediction, it 
gives a basic recommendation on whether to consider investing or not. 

Together, these features empower users to take charge of their daily budgeting and future financial growth. We’re offering the guidance of a 
financial advisor without the cost, and making personalized support available to people who might not otherwise have it. 

However this project has much room for improvement, such as fine-tuning the Stock Advisor by using more complex models like LSTMs to account for 
the seasonality of stock behavior; adding monthly check-ins and progress reports; a portal to display the user’s information and keep track of 
their finances.

**Note**: Budget Buddy is an educational tool/project and does not provide professional financial advice. Stock predictions are especially limited 
due to the simplicity of the model and should not be used for real investment decisions. Budget Buddy does not store user data, however the data 
is sent to Gemini-AI, therefore the user should be aware the information they are providing to Budget Buddy is also being shared with Gemini-AI. 
For these reasons, I advise to not share personal data with Budget Buddy.
