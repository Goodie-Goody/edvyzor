## Early Detection System for final exam scores

### Overview
Welcome to the Early Detection System for WAEC Scores! This proof of concept/demonstration project leverages Supabase, Jupyter Notebook, Streamlit, and Power BI to manage, analyze, and visualize data seamlessly.

**Note:** The data used here may not be representative of intended use case (Nigerian secondary schools).

### Architecture
- **Supabase**: Acts as the primary database to store and manage school data.
- **Jupyter Notebook**: Fetches data from Supabase, builds, and trains machine learning models, hosted in VS code.
- **Streamlit App**: Deploys and hosts the trained model for making real-time predictions and user interactions.
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

Follow these steps to set up the WAEC Prediction project on your local machine and deploy it.

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/waec-prediction.git
cd waec-prediction
```

## 2. Supabase Setup

1. [Open a Supabase account](https://supabase.io/).
2. Upload the data and perform the necessary data transformations.
   - **Note**: [Link to specific transformation instructions if needed.](workflow-supabase.txt)
3. Copy your Supabase URL and Service Role Key credentials.

## 3. Jupyter Notebook Configuration

1. Use the Supabase credentials to connect to the relevant table schema in your Jupyter Notebook.
2. Run the notebook; upon completion, a folder named `saved_models` containing your model should be created.

## 4. Docker Setup

1. [Ensure Docker is installed on your machine](https://docs.docker.com/get-docker/).
2. Your repository contains the `Dockerfile` and `.yml` file. Ensure the `Dockerfile` is configured as follows:

   ```dockerfile
   # Use an official Python runtime as a parent image
   FROM python:3.8-slim

   # Set the working directory in the container
   WORKDIR /app

   # Copy the current directory contents into the container at /app
   COPY . /app

   # Install any needed packages specified in requirements.txt
   RUN pip install --no-cache-dir -r requirements.txt

   # Make port 80 available to the outside world
   EXPOSE 80

   # Define environment variables
   ENV SUPABASE_URL=your_supabase_url
   ENV SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

   # Run your application
   CMD ["python", "your_script.py"]
   ```

3. Build and run the Docker container:

   ```bash
   docker-compose up --build
   ```

## 5. Fly.io Setup

1. [Open an account on Fly.io](https://fly.io/) and link your project.
2. Remove all instances of the keys from the `.env` file.
3. Upload the keys as Fly.io secrets:

   ```bash
   fly secrets set SUPABASE_URL=your_url SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
   ```

4. Launch the app on Fly.io:

   ```bash
   fly launch
   ```

## 6. Visualization with Power BI

Use Power BI to create visualizations and embed them using the Power BI service.

### Infrastructure and Tools

#### Fly.io:
- **Infrastructure**: Fly.io was chosen for its ability to seamlessly deploy and scale our application. Fly.io offers excellent speed, adaptability, and supports modern deployment workflows.
- **Cost-Effectiveness**: Fly.io is quite affordable, making it a suitable option for projects with limited budgets, such as those in Nigerian schools.
- **Supabase**: Supabase was selected due to its speed, adaptability, and being open-source. Supabase integrates well with Fly.io, providing a robust backend for data management.
- **Generous Free Tier**: Supabase offers a generous free tier, which is highly beneficial for Nigerian schools that may have limited financial resources.

### Features
- **Real-Time Data Handling**: Seamlessly manage and store data with Supabase.
- **Machine Learning**: Build and train models in Jupyter Notebook.
- **Interactive Interface**: Deploy models and interact with data using Streamlit deployed on Fly.io.
- **Dynamic Visualization**: Visualize data and predictions in Power BI.

### License
This project is licensed under the MIT License. See the LICENSE file for [details](LICENSE).

### Acknowledgements
A big thank you to everyone who has contributed to this project and to the creators of the tools we used: Supabase, Jupyter Notebook, Scikit-Learn, Python, Streamlit, and Power BI.
