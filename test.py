from utils.helpers import *
from config.paths_config import *
# from utils.helpers import find_similar_users

print(find_similar_users(11880,USER_WEIGHTS_PATH,USER2USER_ENCODED,USER2USER_DECODED))
# # print(similar_users)
# user_pref = get_user_preferences(11880 , RATING_DF, DF , plot=False)
# print(user_pref)


# from pipeline.prediction_pipeline import  hybrid_recommendation

# print(hybrid_recommendation(11880))