# Calibration Tracker

A web application designed for Brose test engineers to track and manage equipment calibration and validation processes. The application provides an intuitive interface to monitor calibration status, track intervals, and manage equipment maintenance schedules.

## Features

- **Equipment Management**: Create, update, and delete equipment entries
- **Calibration Tracking**: Monitor calibration dates and automatic interval calculations
- **Status Monitoring**: Real-time status indicators (OK, DUE SOON, EXPIRED)
- **Equipment Information**: Track essential details including:
  - Equipment name and SAP number
  - Serial number and location
  - Responsible person assignment
  - Calibration intervals and last calibration date
  - Calibration provider and pricing information
- **Real-time Updates**: WebSocket support for live notifications across connected clients
- **Responsive Web Interface**: Clean, user-friendly HTML templates for easy navigation

## Tech Stack

- **Backend**: FastAPI
- **Server**: Uvicorn
- **Database**: SQLAlchemy ORM
- **Frontend**: Jinja2 templates, HTML/CSS
- **Real-time Communication**: WebSockets
- **Form Handling**: Python Multipart

## Project Structure

```
calibration_app/
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
└── app/
    ├── main.py                    # FastAPI application entry point
    ├── models.py                  # SQLAlchemy database models
    ├── schemas.py                 # Pydantic validation schemas
    ├── crud.py                    # Database operations
    ├── database.py                # Database configuration
    ├── routes/
    │   └── equipment.py           # Equipment management routes
    ├── templates/
    │   ├── base.html              # Base template
    │   ├── index.html             # Equipment list page
    │   ├── create_equipment.html  # Equipment creation form
    │   └── edit_equipment.html    # Equipment editing form
    └── static/
        └── images/                # Static image assets
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd calibration_app
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`
   - The API documentation is available at `http://localhost:8000/docs`

## API Endpoints

### Equipment Management

- **GET /**: Display all equipment entries
- **GET /create**: Show equipment creation form
- **POST /create**: Create a new equipment entry
- **POST /calibrate/{equipment_id}**: Update calibration date for equipment
- **POST /delete/{equipment_id}**: Delete equipment entry
- **POST /edit/{equipment_id}**: Update equipment information
- **WebSocket /ws**: WebSocket connection for real-time updates

## Database Schema

### Equipment Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Equipment name |
| brose_sap | String | SAP identifier (unique) |
| serial_number | String | Equipment serial number (unique) |
| location | String | Physical location |
| responsible_person | String | Person responsible for maintenance |
| last_calibration | Date | Last calibration date |
| interval_days | Integer | Calibration interval in days |
| calibration_location | String | Where calibration is performed |
| calibration_provider | String | Organization providing calibration |
| calibration_price | Integer | Cost of calibration |

### Computed Properties

- **next_calibration**: Calculated as `last_calibration + interval_days`
- **status**: 
  - `EXPIRED`: Next calibration date has passed
  - `DUE SOON`: Due within 30 days
  - `OK`: Not due for more than 30 days

## Usage Example

1. **Add Equipment**: Navigate to "Create Equipment" and fill in the equipment details
2. **View Status**: Check the main page to see all equipment with their current calibration status
3. **Update Calibration**: Click "Calibrate" to update the last calibration date
4. **Delete Equipment**: Click "Delete" to remove equipment from tracking

## Requirements

See [requirements.txt](requirements.txt) for complete list of dependencies:
- fastapi
- uvicorn
- sqlalchemy
- jinja2
- python-multipart
- websockets

## License

This project is proprietary and intended for use by Brose test engineers.
