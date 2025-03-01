# Video Subtitle Extraction System

[![Render Status](https://img.shields.io/badge/Render-deployed-success)](https://render.com)
[![Django Version](https://img.shields.io/badge/Django-4.2.4-brightgreen)](https://www.djangoproject.com/)
[![Celery Version](https://img.shields.io/badge/Celery-5.3.1-green)](https://docs.celeryq.dev/)

A Django-based video processing system that automatically extracts subtitles using CCExtractor and indexes them in DynamoDB for fast search capabilities.

## Key Features
- 🎥 Video upload and storage in AWS S3
- 📝 Automatic subtitle extraction using CCExtractor
- 🔍 Keyword search across video subtitles
- 🚀 Scalable architecture with Celery and Redis
- ☁️ Cloud-native deployment on Render
- 📦 Docker container support

## Project Structure
```
humblebee-main/
├── render.yaml            # Render service configuration
├── Dockerfile             # Docker build configuration
├── requirements.txt      # Python dependencies
├── manage.py              # Django management script
├── Procfile               # Process definitions
│
├── humblebee/             # Django project core
│   ├── settings.py        # Application configuration
│   ├── celery_define.py   # Celery task configuration
│   └── ...                # Other Django core files
│
└── videosubtitleapp/      # Main application
    ├── tasks.py           # Celery tasks for subtitle processing
    ├── models.py          # Video model definition
    ├── views.py           # Application view logic
    └── templates/         # HTML templates
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/humblebee-main.git
cd humblebee-main
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**  
Create a `.env` file with these configurations:
```ini
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_STORAGE_BUCKET_NAME=your_bucket_name
CELERY_BROKER_URL=redis://your-redis-url
DJANGO_SECRET_KEY=your_secret_key
```

## Configuration

### Required Services
- AWS S3 Bucket for media storage
- Redis instance for Celery broker
- DynamoDB table for subtitle indexing

### Environment Variables
| Variable | Description |
|----------|-------------|
| `AWS_*` | AWS credentials for S3 access |
| `CELERY_BROKER_URL` | Redis connection URL |
| `DYNAMODB_TABLE_NAME` | DynamoDB table name for subtitles |

## Deployment

1. **Docker Build**
```bash
docker build -t humblebee .
```

2. **Render Services**  
The system is configured for Render deployment with:
- Web service (Django)
- Worker service (Celery)
- Redis instance

Deploy using the `render.yaml` configuration file.

## Usage

1. **Upload Videos**
   - Access the web interface at `/`
   - Upload MP4 video files through the web form

2. **Search Subtitles**
   - Use the search form with keywords
   - Get timestamps for keyword occurrences

## Development

Run the Django development server:
```bash
python manage.py runserver
```

Start Celery worker:
```bash
celery -A humblebee worker -l info -P eventlet
```

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments
- CCExtractor for subtitle extraction
- Django framework for web interface
- Celery for distributed task processing
- AWS for cloud storage and database services
