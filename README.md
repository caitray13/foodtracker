FoodTracker is a voice based app which takes a voice recording (from S3 bucket) of what a person ate in the day, transcribes the file (using AWS Transcribe, extracts the food items and the weight of each, and calculates the macros from it (calories, protein, etc.)\

App takes two arguments; a job name and the name of the voice recording S3.\
For the model I used Dizex/FoodBaseBERT from HuggingFace.\
For nutritional info I used https://api.nal.usda.gov\


Instructions to run in Docker container:
1. Create env file and provide variables
2. At root of project run docker-compose up


Still TODO:
- IOS app to take the voice recording and upload to S3.
- Fiish the macro calcluation part (right now only the entity extraction is done)
- Make the model better (e.g. get better at handling numbers such as "140" and transcribe as literal number not "one hundred and forty" as this messes up the calculations further downstream since we ignore the "one hundred" right now.)