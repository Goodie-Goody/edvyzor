## Early Detection System for WAEC Scores

### Overview
Welcome to the Early Detection System for WAEC Scores! This proof of concept/demonstration project leverages Supabase, Jupyter Notebook, Streamlit, and Power BI to manage, analyze, and visualize data seamlessly. Note: The data used here may not be representative of real-world scenarios for Nigerian schools.

### Architecture
- **Supabase**: Acts as the primary database to store and manage school data.
- **Jupyter Notebook**: Fetches data from Supabase, builds, and trains machine learning models.
- **Streamlit App**: Deploys the trained model for making real-time predictions and user interactions.
- **Supabase**: Stores predictions back into the database.
- **Power BI**: Connects to Supabase via ODBC to visualize data and embed within the Streamlit app.

### Setup Instructions

#### Requirements
- Python 3.7+
- Streamlit
- Supabase Python Client
- Pandas
- Requests
- Power BI
- PostgreSQL ODBC Driver

#### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/waec-prediction.git
   cd waec-prediction
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Supabase**:
   - Set up your Supabase project and obtain the API URL and service role key.
   - Download sample data with 5 rows for testing.
   - Update the `config.py` file with your Supabase credentials.
   - Implement RLS (Row Level Security) policies and configure user roles to access these policies.

4. **Run Streamlit App**:
   ```bash
   streamlit run app.py
   ```

5. **Docker Setup**:
   - Update the Dockerfile with your Supabase URL and service role key.
   - Ensure to remove the service role key from documentation in the Docker .yml file before reuploading to GitHub.
   - Test the setup using Docker Compose.
   - Use Fly.io secrets to upload the Supabase URL and service role key:
     ```bash
     fly secrets set SUPABASE_URL=your_url SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
     ```

### Detailed Workflow

#### Data Ingestion:
- **Supabase Workflow**: We configured Supabase starting from table creation, merging data into the `merged_students` table, and setting up user roles with specific access permissions.
- **Client Access**: Using the Supabase Python Client, a `create_client` method was used to access the `merged_students` table. The service role key was utilized to bypass any RLS policy during data access.

#### Model Training:
- **Jupyter Notebook**: The notebook fetched data from Supabase using the Supabase client. The role service key was used here to bypass RLS policies, ensuring unrestricted data access.
- **Training**: The machine learning model was then trained using this data. [Access the Jupyter Notebook here](#).

#### Real-Time Predictions:
- **Streamlit Integration**: The trained model was deployed on Streamlit for real-time predictions. Users interact with the app, make predictions, and store results back into Supabase.

#### Data Visualization:
- **ODBC Connection**: Power BI connected to Supabase via ODBC to fetch data for visualization.
- **Publishing**: Visualizations were published to Power BI Service. An embed code was generated to display these dynamic visualizations within the Streamlit app.

### Infrastructure and Tools

#### Fly.io:
- **Infrastructure**: Fly.io was chosen for its ability to seamlessly deploy and scale our application. Fly.io offers excellent speed, adaptability, and supports modern deployment workflows.
- **Cost-Effectiveness**: Fly.io is quite affordable, making it a suitable option for projects with limited budgets, such as those in Nigerian schools.
- **Supabase**: Supabase was selected due to its speed, adaptability, and being open-source. Supabase integrates well with Fly.io, providing a robust backend for data management.
- **Generous Free Tier**: Supabase offers a generous free tier, which is highly beneficial for Nigerian schools that may have limited financial resources.

### Features
- **Real-Time Data Handling**: Seamlessly manage and store data with Supabase.
- **Machine Learning**: Build and train models in Jupyter Notebook.
- **Interactive Interface**: Deploy models and interact with data using Streamlit.
- **Dynamic Visualization**: Visualize data and predictions in Power BI.

### Contributing
We welcome contributions! Please read our contribution guidelines before submitting a pull request.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgements
A big thank you to everyone who has contributed to this project and to the tools we used: Supabase, Jupyter Notebook, Streamlit, and Power BI.
