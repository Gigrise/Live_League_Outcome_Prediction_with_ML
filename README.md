# Live_League_Outcome_Prediction_with_ML
> Predicting match outcome using Machine Learning Model in real time.

The goal of the project is to evaluate current match as accurate as possible to predict the outcome of the game in real time.

It might be usefull for the players that easily loose hope to win, since the odds might be not that low one would think.

Currently the model is trained for the match state at 15 minutes mark and matches between challenger level players.
Hence the most accurate result will be achieved at 15:00 and in a high rank match.
I plan to build 2 more models for 5 and 10 minute mark to display intermediate predictions, to improve overall interpetability.
Although gathering data is timeconsuming since API provided by RIOT GAMES is limited by 100 requests per 1 min.


# Files info:

| Plugin | Description |
| ------ | ------ |
| Challenger_Ranked_Games_15minute.csv | initial data for building the model. [Source](https://www.kaggle.com/datasets/benfattori/league-of-legends-diamond-games-first-15-minutes) |
| building_model.py | Training the Model |
| functions_to_extract_info_from_json.py | collection of functions to parse JSON format that got retrieved via REST API |
| main.py | retrieving live match data, predicting and displaying outcome |
| Dash_Output.py | same but in browser |
| random_forest.joblib | the model itself |


# How to use:
1. Start the league match.
2. Run Dash_Output.py in any Python IDE.
3. Open http://127.0.0.1:8050 in browser.
4. Enjoy real time game evaluation.

# Example:

[![IMAGE ALT TEXT](http://img.youtube.com/vi/uKWreTQVlNI/maxresdefault.jpg)](http://www.youtube.com/watch?v=uKWreTQVlNI "League of Legends Win Prediction in Real Time")
https://www.youtube.com/watch?v=uKWreTQVlNI


# Some insights about current model:

![Feature_Importance](https://user-images.githubusercontent.com/34164295/172269850-20342cc0-e74d-4aa1-a38c-a7b97ab84d52.png)

Confusion matrix:

|  | Pred_Loss | Predicted_Win |
| ------ | ------ |  ------ |
| Actual_Win  | 2141 |  500 |
| Actual_Loss |539 | 2187 |


Classification report:

              precision    recall  f1-score   support

           0       0.80      0.81      0.80      2641
           1       0.81      0.80      0.81      2726

    accuracy                           0.81      5367
    macro avg      0.81      0.81      0.81      5367
    weighted avg   0.81      0.81      0.81      5367


