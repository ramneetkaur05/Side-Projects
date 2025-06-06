import pandas as pd
import numpy as np
import itertools

#Loading data
file_path = "JPMC Tasks/Customer_Loan_Data.csv"
df = pd.read_csv(file_path)

#loading only fico scores
fico_scores = df["fico_score"].sort_values().reset_index(drop=True)

def calculate_total_mse(data, bucket_edges):
    """
    divides the fico scores into k buckets
    assigns each bucketa. mean
    then calculates the MSE
    """
    total_mse = 0
    for i in range(len(bucket_edges)-1):
        #find elements in the current bucket
        bucket_data = data[(data >= bucket_edges[i]) & (data < bucket_edges[i+1])]
        if len(bucket_data) == 0:
            continue
        bucket_mean = np.mean(bucket_data)
        mse = np.mean(bucket_data - bucket_mean ** 2)
        total_mse += mse * len(bucket_data) #weighted error
    
    return total_mse


#optimal FICO score boundaries for 3 buckets
def find_best_mse_split(data, k):

    #CONSIDERING UNIQUW FICO SCORES AS. BOUNDARIES
    unique_scores = sorted(data.unique())

    #need to choose (k-1) split ponts
    best_mse = float('inf')
    best_edges = None
    for splits in itertools.combinations(unique_scores[1:-1], k-1):
        #creating ful list of edges
        bucket_edges = [min(data)] + list(splits) + [max(data) + 1]
        mse = calculate_total_mse(data, bucket_edges)

        if mse < best_mse:
            best_mse = mse
            best_edges = bucket_edges

    return best_edges, best_mse


#assigning ratings based on created buckets
def assign_ratings(data, bucket_edges):
    ratings = []
    for score in data:
        for i in range(len(bucket_edges) - 1):
            if bucket_edges[i] <= score < bucket_edges[i+1]:
                ratings.append(i+1)
                break
    return np.array(ratings)


"""
    TESINGS
        1. CHECKINNG AVERAGE FICO SCORE/RATING
        2. CHECKING DEFAULT/RATING
        3. PRINT HOW MANY BORROWERS FALL INTO EACH RATING

"""

#TESTING 1
for rating in sorted(df['fico_rating'].unique()):
    avg_score = df[df['fico_rating'] == rating]['fico_score'].mean()
    print(f"Rating {rating}: Avg FICO = {avg_score:.2f}")

#TESTING 2
for rating in sorted(df['fico_rating'].unique()):
    group = df[df['fico_rating'] == rating]
    default_rate = group['default'].mean()
    print(f"Rating {rating}: Default Rate = {default_rate:.2%}")

#TESTING 3
for rating in sorted(df['fico_rating'].unique()):
    group = df[df['fico_rating'] == rating]
    default_rate = group['default'].mean()
    print(f"Rating {rating}: Default Rate = {default_rate:.2%}")
