import pickle
import numpy as np
import pandas as pd
import os

class SalaryPredictor:
    """Handles ML-based salary prediction"""
    
   
    def __init__(self): 
        """Load all pickle files using paths relative to this file."""
        
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        
        self.models_dir = os.path.join(current_dir, 'ml_models')
        
        try:

            
            self.model = pickle.load(open(os.path.join(self.models_dir, 'salary_prediction_model.pkl'), 'rb'))
            self.dept_map = pickle.load(open(os.path.join(self.models_dir, 'department_mapping.pkl'), 'rb'))
            self.desig_map = pickle.load(open(os.path.join(self.models_dir, 'designation_mapping.pkl'), 'rb'))
            self.mlb = pickle.load(open(os.path.join(self.models_dir, 'skills_mlb.pkl'), 'rb'))
            self.feature_columns = pickle.load(open(os.path.join(self.models_dir, 'feature_columns.pkl'), 'rb'))
            self.grade_map = pickle.load(open(os.path.join(self.models_dir, 'grade_mapping.pkl'), 'rb'))
            
            print("✓ All ML models loaded successfully!")
            
        except FileNotFoundError as e:
            
            print(f"❌ Error loading pickle files: {e}")
            print(f"   Please ensure all pickle files are in '{self.models_dir}' folder")
            raise
        
    def prepare_input(self, grade, skills_list, department_id, designation_id):

        
        
        grade_encoded = self.grade_map.get(grade, 0)
        
        # 2. Encode Skills Using MultiLabelBinarizer
        skills_binary = self.mlb.transform([skills_list])[0]
        
        # 3. Target Encoding for Department & Designation
        dept_te = self.dept_map.get(department_id, np.mean(list(self.dept_map.values())))
        desig_te = self.desig_map.get(designation_id, np.mean(list(self.desig_map.values())))
        
        # 4. Combine All Inputs
        data_dict = {"grade_encoded": grade_encoded}
        
        # Add skills columns
        for idx, skill_name in enumerate(self.mlb.classes_):
            data_dict[f"skill_{skill_name}"] = skills_binary[idx]
        
        # Add target-encoded values
        data_dict["department_id_te"] = dept_te
        data_dict["designation_id_te"] = desig_te
        
        # Convert to DataFrame
        df_input = pd.DataFrame([data_dict])
        
        # 5. Reindex columns into exact training order
        df_input = df_input.reindex(columns=self.feature_columns, fill_value=0)
        
        return df_input
    
    def predict_salary(self, grade, skills_str, department_id, designation_id):

        
        # Parse skills string into list
        if isinstance(skills_str, str):
            skills_list = [s.strip() for s in skills_str.split(',')]
        else:
            skills_list = []
        
        # Prepare input
        X_input = self.prepare_input(grade, skills_list, department_id, designation_id)
        
        # Predict
        predicted_salary = self.model.predict(X_input)[0]
        
        return round(predicted_salary, 2)




if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTING ML SALARY PREDICTOR")
    print("="*70)
    
    # Initialize predictor
    predictor = SalaryPredictor()
    
    # Test inputs
    test_grade = 2
    test_skills = "8,15"
    test_dept_id = 24
    test_desig_id = 7
    
    print("\nTest Inputs:")
    print(f"  Grade: {test_grade}")
    print(f"  Skills: {test_skills}")
    print(f"  Department ID: {test_dept_id}")
    print(f"  Designation ID: {test_desig_id}")
    
    # Predict
    salary = predictor.predict_salary(test_grade, test_skills, test_dept_id, test_desig_id)
    
    print("\n" + "="*70)
    print(f"  ⭐ Predicted Salary: ${salary:,.2f}")
    print("="*70)