🏍️ Bike Resale Price Prediction System

A full-stack Machine Learning–powered Bike Resale Price Prediction System designed to estimate the current market resale value of a used motorcycle based on important factors such as brand, model, engine capacity, bike age, kilometers driven, number of owners, condition, and original launch price.

The project combines a trained machine learning model with a FastAPI backend and a modern HTML/CSS/JavaScript frontend to provide an interactive resale-value prediction experience.

🚀 Project Overview

The Bike Resale Price Prediction System aims to solve a practical problem faced by bike owners and buyers:

"What is my bike worth in the current used-bike market?"

Instead of relying only on manual estimation, the application uses a machine learning model trained on used-bike data to estimate the resale price.

The system provides:

🏍️ Bike brand and model selection
⚙️ Engine-capacity selection
📅 Bike-age based analysis
🛣️ Kilometers-driven analysis
👥 Previous-owner information
🔧 Bike-condition information
💰 Original launch-price input
🤖 Machine-learning-based resale prediction
📉 Depreciation analysis
📊 Personalized depreciation visualization
🖼️ Bike image display after analysis
🔌 FastAPI REST backend
💻 Interactive web frontend
✨ Key Features
🤖 Machine Learning Prediction

The core of the application is a trained machine learning model that predicts the estimated resale value of a bike.

The prediction considers multiple factors:

Feature	Description
🏷️ Brand	Manufacturer of the bike
🏍️ Model	Specific bike model
⚙️ Engine CC	Engine displacement
📅 Age	Age of the bike in months
🛣️ Kilometers Driven	Total distance travelled
👥 Owners	Number of previous owners
🔧 Condition	Current bike condition
💰 Launch Price	Original price of the bike

The trained model is stored in the models/ directory and is loaded by the backend during prediction.

🔄 Prediction Workflow

The complete prediction process follows this workflow:

User Opens Application
        ↓
Select Bike Brand
        ↓
Select Bike Model
        ↓
Select Engine Capacity
        ↓
Enter Bike Details
        ↓
Validate Input
        ↓
Send Request to FastAPI
        ↓
Machine Learning Model
        ↓
Predict Resale Price
        ↓
Calculate Depreciation
        ↓
Display Result
        ↓
Generate Personalized Chart
💰 Resale Price Prediction

After submitting the bike information, the system displays:

Estimated Market Resale Price

The result section provides:

💰 Estimated resale price
📉 Depreciation amount
📊 Depreciation percentage
💎 Value retained percentage
🏍️ Selected bike information

Example:

Estimated Market Resale Price

₹XX,XXX

Honda Activa 125

Depreciation       ₹XX,XXX
Depreciation Rate  XX.XX%
Value Retained     XX.XX%
📉 Personalized Depreciation Analysis

The application generates a personalized depreciation chart using:

Original launch price
Current bike age
Predicted resale value

The visualization shows how the estimated bike value changes with age.

Original Price
     │
     │\
     │ \
     │  \
     │   \
     │    ● ← Your Bike
     │     \
     │      \
     │       \
     └──────────────────
          Bike Age

The chart includes:

📈 Bike-value curve
💰 Original price
💵 Current predicted value
📍 Current bike marker
📅 Bike age
📊 Value grid
📝 Personalized explanation
🖼️ Bike Image Integration

The frontend can display an image of the analyzed bike after a successful prediction.

The image system supports:

1. Local Images

Exact bike images can be placed inside:

frontend/images/bikes/

Example:

frontend/images/bikes/honda-activa-125.jpg
frontend/images/bikes/honda-shine.jpg
frontend/images/bikes/hero-splendor.jpg
2. Wikimedia Commons

If an exact local image is not available, the frontend can search Wikimedia Commons for a suitable image based on the selected:

Brand + Model
3. Fallback Image

If no suitable online image is found, a fallback motorcycle image can be displayed.

The image is intentionally loaded after successful prediction, so selecting a bike does not automatically trigger the image search.

🔌 FastAPI Backend

The backend is built using FastAPI and provides REST API endpoints for the frontend.

The main backend responsibilities include:

Loading the trained ML model
Loading bike datasets
Providing available brands/models
Providing engine capacities
Processing prediction requests
Returning prediction results
Backend health monitoring
📡 API Workflow

The frontend communicates with the backend through HTTP requests.

Frontend
   │
   │ HTTP Request
   ▼
FastAPI Backend
   │
   ▼
Machine Learning Model
   │
   ▼
Prediction
   │
   │ JSON Response
   ▼
Frontend
🩺 Backend Health Check

The frontend checks the backend health endpoint when the application starts.

The backend can also report the number of available bike variants.

Example console output:

Bike Resale Prediction API connected successfully.

Available bike variants: 387
🏍️ Dynamic Bike Selection

The application provides dependent dropdowns.

Brand → Model → Engine Capacity
Select Brand
     ↓
Available Models Loaded
     ↓
Select Model
     ↓
Available Engine Capacities Loaded
     ↓
Select Engine

This prevents users from manually entering invalid combinations.

🛡️ Input Validation

The frontend validates the submitted bike information before sending the prediction request.

Examples of validation include:

Engine capacity must be greater than 0
Bike age must be at least 1 month
Bike age cannot exceed 180 months
Kilometers driven cannot be negative
Kilometers driven cannot exceed 500,000
Number of owners must be at least 1
Launch price must be greater than 0
Required fields must be completed

Invalid input is displayed through a clear error message instead of being sent to the prediction API.

📊 Exploratory Data Analysis

The project includes exploratory data analysis and generated visualizations.

The project contains analysis plots such as:

Age vs Price
Brand vs Price
Condition vs Price
Correlation Matrix
Depreciation Curve
Engine CC vs Price
Kilometers vs Price
Price Distribution

These visualizations help understand relationships between bike characteristics and resale prices.

🧹 Data Processing

The machine learning workflow includes dedicated scripts for preparing and cleaning the bike dataset.

The ml/ directory contains scripts for:

🔍 Inspecting the dataset
🧹 Cleaning data
📊 Exploratory data analysis
⚙️ Preparing model-ready data
🤖 Training the model
🧪 Testing the model
🏆 Comparing models
🏆 Model Comparison

The project includes a model-comparison stage to evaluate different machine learning approaches.

The comparison results are stored in:

data/model_comparison.csv

This allows the machine learning workflow to compare model performance before selecting the model used for prediction.

🧠 Machine Learning Pipeline

The overall ML pipeline can be represented as:

Raw Bike Dataset
       ↓
Data Inspection
       ↓
Data Cleaning
       ↓
Exploratory Data Analysis
       ↓
Feature Preparation
       ↓
Model Comparison
       ↓
Model Training
       ↓
Model Testing
       ↓
Final Trained Model
       ↓
FastAPI Prediction API
🛠️ Technology Stack
🤖 Machine Learning
Python
Pandas
NumPy
Scikit-learn
Joblib
🔌 Backend
Python
FastAPI
Uvicorn
REST API
Pydantic
💻 Frontend
HTML5
CSS3
JavaScript
Fetch API
SVG-based visualization
Lucide Icons
📊 Data & Visualization
Pandas
Matplotlib
Seaborn
CSV datasets
SVG chart rendering
🧰 Development Tools
Git
GitHub
Visual Studio Code
Python Virtual Environment
📂 Project Structure
bike-resale-project/
│
├── backend/
│   └── main.py
│
├── data/
│   ├── bike_master.csv
│   ├── bike_variants.csv
│   ├── bikes_model_ready.csv
│   ├── model_comparison.csv
│   └── used_bikes_clean.csv
│
├── frontend/
│   ├── plots/
│   │   ├── brand_vs_price.png
│   │   ├── condition_vs_price.png
│   │   ├── correlation_matrix.png
│   │   └── depreciation_curve.png
│   │
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── ml/
│   ├── clean_data.py
│   ├── compare_models.py
│   ├── eda.py
│   ├── inspect_data.py
│   ├── prepare_data.py
│   ├── test_model.py
│   ├── train_model.py
│   └── plots/
│
├── models/
│   └── bike_resale_model.pkl
│
├── .gitignore
├── folder-structure.txt
├── project_structure.txt
├── requirements.txt
└── README.md
⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone <YOUR_GITHUB_REPOSITORY_URL>

Navigate into the project:

cd bike-resale-project
🐍 2️⃣ Create Virtual Environment

Create a Python virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

You should then see something similar to:

(venv) PS C:\...\bike-resale-project>
📦 3️⃣ Install Dependencies

Install the required Python packages:

pip install -r requirements.txt
🧠 4️⃣ Machine Learning Pipeline

If you want to reproduce the ML workflow, the scripts inside ml/ can be executed in the appropriate pipeline order:

inspect_data.py
      ↓
clean_data.py
      ↓
eda.py
      ↓
prepare_data.py
      ↓
compare_models.py
      ↓
train_model.py
      ↓
test_model.py

The trained model is stored in:

models/bike_resale_model.pkl
🔌 5️⃣ Start the Backend

From the project root, start FastAPI using Uvicorn.

For example:

uvicorn backend.main:app --reload

The API will normally be available at:

http://127.0.0.1:8000

FastAPI's interactive documentation can be accessed through:

http://127.0.0.1:8000/docs
💻 6️⃣ Start the Frontend

Open the frontend using a local web server.

For example, from the project directory:

python -m http.server 5500 --directory frontend

Then open:

http://127.0.0.1:5500

⚠️ Running the HTML directly using file:// is not recommended. Use a local HTTP server so the frontend can communicate reliably with the backend.

🔄 Complete Application Flow
                    🏍️ USER
                       │
                       ▼
              ┌─────────────────┐
              │   Web Interface  │
              └────────┬────────┘
                       │
                       ▼
              Select Bike Details
                       │
                       ▼
              ┌─────────────────┐
              │ Input Validation│
              └────────┬────────┘
                       │
                       ▼
                 HTTP Request
                       │
                       ▼
              ┌─────────────────┐
              │     FastAPI     │
              │     Backend     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  ML Prediction  │
              │     Model       │
              └────────┬────────┘
                       │
                       ▼
               Predicted Price
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
      💰 Price Result      📉 Depreciation
                                  │
                                  ▼
                           📊 Personalized
                               Chart
📁 Dataset

The project contains multiple processed datasets under:

data/

Including:

bike_master.csv
bike_variants.csv
bikes_model_ready.csv
used_bikes_clean.csv
model_comparison.csv

These datasets support the data-cleaning, analysis, model-training, and prediction workflow.

🧪 Testing

The project includes:

ml/test_model.py

which can be used to test the trained machine learning model.

The backend also performs validation for prediction requests and returns appropriate API errors when invalid data is supplied.

📊 Generated Visualizations

The project contains multiple analytical plots.

Frontend visualizations
frontend/plots/
Machine learning visualizations
ml/plots/

These plots provide insights into:

📅 Age and resale price
🛣️ Kilometers and resale price
⚙️ Engine capacity and resale price
🏷️ Brand and resale price
🔧 Condition and resale price
💰 Price distribution
📊 Feature correlations
📉 Depreciation patterns
🛡️ Error Handling

The application includes error handling across the frontend and backend.

Frontend handling includes:

API connection errors
Invalid prediction responses
Invalid form inputs
Model-loading failures
Engine/model loading failures
Image-search failures

The application displays user-friendly messages instead of exposing raw technical errors.

🎨 User Interface

The frontend provides an interactive bike-analysis experience featuring:

🏍️ Bike selection
🎯 Structured input forms
💰 Prediction result cards
📊 Depreciation visualization
🖼️ Bike imagery
⏳ Loading states
⚠️ Error states
📱 Responsive design
✨ Interactive controls
🔄 Dynamic dropdowns

The interface is designed to make a machine-learning prediction understandable to a normal user rather than presenting only a raw model output.

🚀 Future Improvements

Possible future improvements include:

📱 Mobile application
☁️ Cloud deployment
🌐 Production hosting
🔐 User authentication
💾 Prediction history
📊 Advanced analytics dashboard
🏍️ More bike datasets
🤖 Advanced ML models
📈 Market trend prediction
📍 Location-based resale estimation
💹 Real-time used-bike market data
🧠 Automated model retraining
📦 Docker deployment
⚙️ CI/CD pipeline
🧪 Automated testing
🌍 Multi-language support
📚 Learning Outcomes

This project demonstrates practical experience with:

🤖 Machine learning
🐍 Python programming
📊 Data preprocessing
🧹 Data cleaning
📈 Exploratory data analysis
🧠 Model training
🏆 Model comparison
🧪 Model testing
🔌 REST API development
⚡ FastAPI
💻 HTML/CSS/JavaScript
🔄 Frontend-backend integration
📊 Data visualization
🗃️ Dataset management
🐙 Git and GitHub
🏗️ Full-stack ML application architecture
🌟 Why This Project?

The project demonstrates how a machine learning model can be transformed into a usable real-world application.

Instead of keeping the ML model isolated inside a Python notebook, this project connects:

📊 Data
   +
🤖 Machine Learning
   +
⚡ FastAPI
   +
💻 Web Frontend
   +
📈 Visualization
   =
🏍️ Real-World Prediction Application
📌 Project Status

🟢 Completed & Functional

The current version includes:

✅ Machine learning prediction
✅ FastAPI backend
✅ Dynamic bike selection
✅ Engine-capacity selection
✅ Input validation
✅ Resale-price calculation
✅ Depreciation calculation
✅ Personalized depreciation chart
✅ Bike image integration
✅ EDA visualizations
✅ Model training/testing workflow
✅ Git/GitHub project setup
👨‍💻 Developer

Ayanangshu Goswami

🎓 B.Tech — Information Technology

Interested in:

🤖 Machine Learning
🧠 Artificial Intelligence
💻 Full-Stack Development
🐍 Python
⚡ Backend Engineering
📊 Data Science
🏗️ Software Engineering
⭐ Support the Project

If you find this project interesting or useful:

⭐ Give the repository a star on GitHub!

🍴 Fork the project
🐛 Report issues
💡 Suggest improvements
🤝 Contribute to the project

🏍️ Built with Python + Machine Learning + FastAPI + JavaScript

Predict smarter. Understand depreciation. Make better bike resale decisions. 🚀