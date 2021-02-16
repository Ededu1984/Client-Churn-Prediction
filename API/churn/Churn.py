import pickle




class churn(object):

    def __init__(self): 
        self.home_path = '/home/edson/Projetos_DS/Client-Churn-Prediction/'
        self.transformation_surname    = pickle.load(open (self.home_path + "parameter/transformation_surname.pkl", "rb"))
        self.transformation_geography  = pickle.load(open (self.home_path + "parameter/transformation_geography.pkl", "rb"))
        self.transformation_gender     = pickle.load(open (self.home_path + "parameter/transformation_gender.pkl", "rb"))
        self.transformation_score_cond = pickle.load(open (self.home_path + "parameter/transformation_score_cond.pkl", "rb"))
        self.transformation_age_range  = pickle.load(open (self.home_path + "parameter/transformation_age_range.pkl", "rb"))

    def feature_engineering(self, df1):
        df1['Score_cond'] = df1['CreditScore'].apply(lambda x: 'Bad' if x<629 else('Fair' if 630 < x < 689 else('Good' if 690<x<719 else 'Excellent')))
        df1['Age_range'] = df1['Age'].apply(lambda x: 'Young adults' if 18<=x<=29 else('Middle-aged adults' if 30<=x<=45 else 'Old-aged adults'))
        
        return df1

    def encoding(self, df2):

        # Encoding
        df2['Surname'] = self.transformation_surname.fit_transform(df2['Surname'].values)
        df2['Geography'] = self.transformation_geography.fit_transform(df2['Geography'].values)
        df2['Gender'] = self.transformation_gender.fit_transform(df2['Gender'].values)
        df2['Score_cond'] = self.transformation_score_cond.fit_transform(df2['Score_cond'].values)
        df2['Age_range'] = self.transformation_age_range.fit_transform(df2['Age_range'].values)

        columns_selected_boruta = ['RowNumber', 'CreditScore', 'Geography', 'Gender', 'Age', 'Balance', 'NumOfProducts', 'IsActiveMember', 'Age_range']

        return df2[columns_selected_boruta]



    def get_prediction(self, model, original_data, test_data):
        # Prediction
        pred = model.predict(test_data)

        # join pred into the original data
        original_data['prediction'] = pred 

        return original_data.to_json(orient='records')