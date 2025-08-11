import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

class MiningModels:
    def __init__(self):
        self.init_models()
        
    def init_models(self):
        np.random.seed(42)
        n_samples = 100
        X = np.column_stack([
            np.random.uniform(200, 1500, n_samples),  # Depth
            np.random.uniform(5, 150, n_samples),     # Rock strength (Rc)
            np.random.uniform(0.4, 0.9, n_samples),   # Humidity coefficient
            np.random.uniform(1.5, 12, n_samples),    # Width
            np.random.uniform(0.1, 1.0, n_samples)    # Fracturing
        ])
        y = 30 + 0.05 * X[:, 0] - 0.3 * X[:, 1] + 20 * X[:, 2] + 5 * X[:, 3] + 10 * X[:, 4] + np.random.normal(0, 5, n_samples)

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.rf_model.fit(X_scaled, y)

        self.nn_model = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)
        self.nn_model.fit(X_scaled, y)
        
    def predict_rf(self, depth, rc, humidity, width, fracture):
        X = np.array([[depth, rc, humidity, width, fracture]])
        X_scaled = self.scaler.transform(X)
        return self.rf_model.predict(X_scaled)[0]
        
    def predict_nn(self, depth, rc, humidity, width, fracture):
        X = np.array([[depth, rc, humidity, width, fracture]])
        X_scaled = self.scaler.transform(X)
        return self.nn_model.predict(X_scaled)[0]