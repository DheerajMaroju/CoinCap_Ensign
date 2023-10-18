* Change the API keys for Ensign and Coincap in Publisher and Subscriber
* Change directory to the working directory.
* Execute subscriber.py using the following command:
   * python subscriber.py
* Execute publisher.py using the following command:
   * python publisher.py
* The data must start coming and the following files will be generated and updated eventually:
   * Profits.csv (takes ~20 minutes for the file to start updating)
   * price_history.csv
* Once the files are generated, execute the api.py file.
* Access the UI on excel sheet here and make a choice from the dropdown
   * any asset: look at the historical price and prediction for the next minute
   * top_5_profitable: to fetch the top 5 profit making assets along with the profit% for the next timestamp
   * top_5_loss_making: to fetch the top 5 loss making assets along with the loss% for the next timestamp
   * Note: 
      * Refresh the page if the values are not updating
      * Make sure the API is up and running.


Link to access the GitHub repository: https://github.com/DheerajMaroju/CoinCap_Ensign