# DataViz for Creatives - Repository Guide

## Overview

This repository contains a Streamlit-based data visualization application called "DataViz for Creatives" that allows users to upload data files (CSV or Excel), process and analyze the data, and create visualizations. The application also integrates with OpenAI's GPT-4o model to provide AI-assisted data analysis.

The application is structured as a Python-based web application that runs on Streamlit, with modular utilities for data processing, visualization, and AI analysis.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple modular architecture:

1. **Frontend and Backend**: Streamlit handles both the frontend UI and backend processing in a unified Python codebase.
2. **Utilities**: Modular Python modules handle specific functionality (data processing, visualization, AI analysis).
3. **Data Flow**: User uploads data → Data is processed → User selects visualization options → Visualizations are generated → Optional AI analysis is performed.

The architecture deliberately keeps everything in Python without requiring separate frontend/backend services or databases, making it lightweight and easy to deploy.

## Key Components

### 1. Main Application (app.py)

The central entry point that defines the Streamlit UI and overall application flow. It handles:
- Page configuration and layout
- File uploading functionality
- Session state management for persistent data
- Routing between different app sections

### 2. Data Processing Module (utils/data_processor.py)

Handles all data-related operations including:
- Reading and parsing CSV and Excel files
- Generating statistics and insights from the data
- Identifying column types (numeric, categorical, datetime)
- Preparing data for visualization

### 3. Visualization Module (utils/visualization.py)

Manages the creation of data visualizations using Plotly:
- Offers various chart types (bar charts, line charts, etc.)
- Dynamically presents appropriate visualization options based on data types
- Handles the rendering of interactive visualizations
- Customizes visualization appearance and features

### 4. AI Assistant Module (utils/ai_assistant.py)

Integrates with OpenAI's API to provide AI-powered data analysis:
- Connects to the OpenAI API using the gpt-4o model
- Processes user queries about their data
- Prepares data samples for API submission
- Formats and returns AI-generated insights

## Data Flow

1. **Data Ingestion**:
   - User uploads CSV or Excel file through Streamlit interface
   - File is read using pandas and stored in session state

2. **Data Processing**:
   - The data_processor module analyzes the uploaded data
   - Generates statistics and identifies column types
   - Prepares the data for visualization

3. **Visualization Generation**:
   - User selects visualization type and parameters
   - visualization module generates the appropriate chart
   - Interactive visualization is displayed to the user

4. **AI Analysis** (optional):
   - User submits a question about their data
   - Data sample is prepared and sent to OpenAI API
   - AI response is displayed to the user
   - Chat history is maintained in session state

## External Dependencies

The application relies on several key Python libraries:

1. **Streamlit** (v1.45.1+): Powers the web interface and interactive elements
2. **Pandas** (v2.2.3+): Handles data manipulation and processing
3. **Plotly** (v6.1.1+): Creates interactive data visualizations
4. **OpenAI** (v1.81.0+): Connects to the OpenAI API for AI-assisted analysis
5. **NumPy** (v2.2.6+): Supports numerical operations

The application requires an OpenAI API key stored as an environment variable (`OPENAI_API_KEY`) to enable the AI assistant functionality.

## Deployment Strategy

The application is configured for deployment on Replit with:

1. **Python Environment**:
   - Python 3.11 is specified as the runtime
   - Dependencies are managed through pyproject.toml

2. **Streamlit Configuration**:
   - Streamlit is configured to run on port 5000
   - Headless server mode is enabled
   - Custom theming is applied through .streamlit/config.toml

3. **Replit Configuration**:
   - The .replit file specifies how to run the application
   - Deployment target is set to "autoscale"
   - Run command is configured to launch the Streamlit server

4. **Workflow**:
   - A parallel workflow is defined to run the Streamlit application
   - The application is exposed on port 5000

The application doesn't currently use a database for persistence - all data is handled in-memory during the user session. For future scaling, consider adding a database integration.

## Development Guidelines

When extending this application:

1. **Maintain Modularity**: Keep related functionality in dedicated utility modules
2. **Session State Management**: Use Streamlit's session state for data persistence between interactions
3. **User Experience**: Focus on keeping the interface intuitive for creative professionals
4. **AI Integration**: Use the GPT-4o model for AI analysis unless specifically requested otherwise
5. **Visualization Flexibility**: Support different data types and visualization needs

## Potential Enhancements

1. **Data Persistence**: Add database integration for saving visualizations and analysis
2. **Export Functionality**: Enhance options for exporting visualizations and insights
3. **User Authentication**: Add multi-user support with saved preferences
4. **Advanced Visualizations**: Expand the range of visualization types
5. **Collaborative Features**: Add ability to share and collaborate on visualizations